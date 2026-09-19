---
name: release-gate
description: "Put a read-only grounding check between 'the agent says done' and 'the result ships'. Every date, id, URL, hash (optionally path and number) in the output must appear in the evidence the producer was given, or the output is rejected and a deterministic fallback ships instead. Use when: releasing a subagent's brief, report, PR description, changelog, status update, or any artifact that cites specifics; wiring a cron or pipeline that publishes model output unread. Triggers: 'gate this before it ships', 'verify the claim', 'is this grounded', 'release gate', 'the agent invented a date'."
---

# Release Gate

The producer's claim is never the release.

Three events are easy to collapse into one and must stay separate:

1. The work is correct.
2. The producer says it is done.
3. The system releases the result.

An agent that writes its own status brief will, some nights, invent a ticket number, a
milestone, or a date that looks right. If the brief is written straight to disk, that
invention ships with the same authority as a real fact. This skill owns event 3 with a
verifier that cannot be talked into anything, because it is not a model.

## When to use

- A model produces an artifact that cites specifics (ids, dates, URLs, commits, paths) and
  something downstream will act on it: a daily brief, a PR description, a release note, a
  customer-facing summary, a handoff packet, a scheduled report.
- The producer runs unattended (cron, pipeline, overnight batch) and nobody reads the
  output before it lands.
- You have a second model "reviewing" the first and the reviews cost tokens, drift, and
  cannot be reproduced.

## Avoid

- Judging quality, tone, or completeness. This gate checks that specifics are grounded,
  nothing else. Pair it with a critique pass for quality.
- Gating free prose that has no evidence set. With nothing to ground against, every date
  is "invented"; define the evidence first or do not gate.
- Actions with side effects that already happened. The gate must run before the write,
  the publish, or the send; verifying after the fact only tells you what to apologize for.

## Prerequisites

- Python 3.10+. No third-party packages; tests use pytest.
- A **claim**: the artifact about to ship, as a text file.
- An **evidence set**: the inputs the producer was allowed to cite, as one or more files.
  JSON dicts are serialized with policy-like keys dropped (see below); everything else is
  read as text.
- A **fallback**: a deterministic artifact that ships when the claim is rejected. Usually
  "Nothing found" plus the raw facts. It must never come from the producer.

## Procedure

1. **Split the producer from the release.** The producer returns the claim alone. Its
   reasoning, chain of thought, or self-assessment never enters the gate; a verifier that
   reads "I checked this carefully" is a verifier that can be persuaded.
2. **Freeze the evidence set.** Serialize exactly what the producer was handed: collected
   facts, the day's date, the diff, the issue body. Exclude policy documents, prompt seeds,
   and the whole history; those would ground any date or id that ever existed. The script
   drops the JSON keys `system_prompt`, `policy`, `seed`, `history`, `constitution` by
   default (`--exclude-key` adds more).
3. **Run the gate.**

   ```
   python release_gate.py --claim brief.md --evidence facts.json --fallback nothing.md --ledger gate.jsonl --label cmo
   ```

   Exit 0 prints the claim (release). Exit 1 prints the fallback and lists every
   ungrounded token on stderr (recover). Exit 2 is a usage error and releases nothing.
4. **Recover to the fallback, never retry.** A retry re-runs the producer that just
   invented something, with the same inputs and the same incentive. The fallback is the
   same path an empty producer response already takes, so recovery costs no new code.
5. **Ledger every verdict.** Each run appends `verdict`, `state`, `reject_reasons`, and
   on rejection the full `rejected_claim`. False rejections are read from the ledger, not
   hidden as producer failures. After two weeks, read the rejected rows and decide whether
   a token kind is too strict for your artifact before loosening anything.
6. **Add a required pattern where silence is itself an invention.** If pending items exist,
   the brief must name one: `--require "/view/\d+"`. A producer that says "nothing to
   read" while the queue is full is rejected the same way as one that invents an id.

## Token kinds

| Kind | Matches | Default |
|---|---|---|
| `date` | `YYYY-MM-DD` | on |
| `url` | `http://` or `https://` up to whitespace or a closing bracket | on |
| `ref` | `#123`, `ABC-123` (ticket style) | on |
| `hash` | 7 to 40 hex characters (commits, content hashes) | on |
| `path` | `dir/file.ext` | off |
| `number` | bare integers, decimals, percents | off |

`path` and `number` are opt-in (`--kinds date,url,ref,hash,path,number`) because prose
carries numbers and paths that were never meant as citations; turn them on for
artifacts like changelogs where every figure should trace to the diff.

Every match must appear verbatim in the evidence text. Substring matching is deliberate:
it is cheap, has no false negatives on the tokens it knows, and its false positives are
visible in the ledger.

## Why deterministic, not a second model

A second model reviewing the first costs tokens on every run, can be argued into passing
a claim by the claim itself, and gives non-reproducible rejections you cannot audit. A
regex grounding check by different code is more independent than a second copy of the
same weights, costs nothing, and every rejection is replayable from the ledger row.

The underlying result (arXiv 2609.20474, "How Do Agent Harnesses Create Value? Planning
Information and Release Control in Stateful LLM Agents") is that a read-only verifier
seeing only the objective, required outputs, evidence, and artifact captured nearly all
of the false-pass reduction of a full harness for under a cent per episode. The
limitation the paper names, that terminal verification arrives after side effects, is
handled here by running the gate before the only write.

## Wiring into an agent loop

```python
from release_gate import verify, load_evidence

claim = producer(facts)                       # CLAIMED, not released
reasons = verify(claim, load_evidence([facts_path]), require=[r"/view/\d+"] if facts["pending"] else None)
if reasons:
    ledger.append({"verdict": "rejected", "reject_reasons": reasons, "rejected_claim": claim})
    claim = fallback(facts)                   # deterministic, never the producer again
else:
    ledger.append({"verdict": "verified"})
write_brief(claim)                            # the only side effect, after the verdict
```

## Tests

`python -m pytest test_release_gate.py -q` runs the risk register: invented ref, invented
date, grounded claim passes, excluded keys never ground, required pattern, empty claim,
opt-in kinds stay off, CLI rejects to fallback and ledgers the claim, CLI passes a verified
claim through unchanged, unknown kind fails loudly.

Open risk, waived until the ledger has rows: correct-but-unusual output (a real date the
collector did not capture) reads as a false rejection. The ledger is where you find it.

## Example

Claim from an overnight brief:

> Read "Why the retry loop lies" at /view/41 today, then ship it by 2026-09-24.

Evidence: `{"day": "2026-09-19", "pending": [{"id": 41, "title": "Why the retry loop lies"}]}`.

Result: `REJECTED`, `date not in evidence: 2026-09-24`. The producer invented a deadline.
The fallback brief ships ("1 pending post: Why the retry loop lies, /view/41"), the rejected claim
sits in the ledger, and the next morning the operator sees a grounded brief instead of a
plausible one.
