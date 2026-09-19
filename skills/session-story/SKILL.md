---
name: session-story
description: Extract a build session's story (narrative, problem-solving, wrong turns, the user's judgment calls, receipts) into blog-post source material at stories/. Use at the end of any substantive build session, when the user says "capture this session" or "story of what we did", or when mining an old transcript for a post. Raw material, never a drafted post.
---

# Session story extraction

Turn the session that just happened into durable source material for a blog post. This is UPSTREAM of `/proof` (which drafts posts from receipts): a story file holds the narrative and the judgment, so a post can be written weeks later by a session that was not there.

FORMAT.md in this directory is the locked output format. `examples/2026-07-31-rung2-gifs.md` is the canonical worked example, extracted live from the session that created this skill. Match its altitude: beats, not a work log; verbatim quotes, not paraphrase.

## Procedure

0. Score first, write second (story signal gate, : stop low signal at the source). Draft the full story into the scratchpad, then run `python scripts/story_gate.py gate <scratch>.md --slug YYYY-MM-DD-<slug>`. Exit 0 (PROMOTE or HOLD) = go on to step 1 with that text. Exit 1 (KILL) = the gate has written its one line to `stories/gate-ledger.md`; write NO file under stories/, NO INDEX line, and say so in one sentence (slug, score, reason). A KILL is usually no receipt (no commit or decision ref) or a raw pack with no judgment: fill the Hook and The invariant, cite the commits, and re-score before giving up on a session you were in. `story_mine.py --out` and `--queue-draft` run the same gate on their own writes.
1. Output path: `stories/YYYY-MM-DD-<slug>.md` (repo root). One file per story; a session with two unrelated arcs gets two files.
2. Fill every FORMAT.md section from the session in context. Running after the fact, or wanting the receipts without paying for them in context, start from the pack: `python scripts/story_mine.py --latest` (also `--session <id-prefix>`, `--date YYYY-MM-DD`, `--list` to find one). The pack is the deterministic half: the user's turns verbatim, a beat scaffold, tool errors, commits across every repo the session touched, token spend. It deliberately leaves Hook, The world before, The invariant and Leftovers empty; those are judgment.
3. Hard rules:
   - **the user's words verbatim.** His reactions, corrections, and one-liners are the judgment payload ("would rather him go into a dungeon" is worth more than any summary of it). Quote, don't polish.
   - **Failures stay in.** The wrong turn, the probe that lied, the cache that bit: the debugging IS the story. A story with no friction is a press release, bounce it.
   - **Numbers carry sources.** Commit hashes, file sizes, token counts, wall-clock. Unverifiable claims get cut, not hedged.
   - **Voice-neutral.** This is source material; the user's voice gets applied at drafting time (`/proof` or a writing session with `feedback_the user-content-voice-buildinpublic`). No em dashes even here.
   - **The invariant is required.** One to three sentences on what transfers beyond this session. If you cannot name one, say so explicitly; that is itself information.
4. Append one line to `stories/INDEX.md`: `- [date] <slug>: <one-line hook> (status: raw)`.
5. Commit: `process: session story <slug>`.

## Relationship to the judgment-extraction loop

The format encodes a compressed version of the user's recursive judgment extraction (experience -> externalize -> tension -> invariant -> compress -> codify): Beats = experience externalized, Taste moments = the judgment located, The invariant = the compression, this skill = the codify step. The full ChatGPT-authored articulation is inspo, not canon; do not import its prose into stories.

## Known gotchas

- The SessionEnd pack captures receipts only; Hook, wrong turns, invariant and leftovers must be written by the session that lived them BEFORE /clear, or they are gone.
- Local sweep drafts hit a ceiling (12 drafts, 0 pass): texture targets produced a metronome, then 85% long sentences, so the sweep prompt is spec-only and a bounced draft is edited by hand.

## Improvement backlog

- Dead-session judgment fill, tagged [auto-judgment, unverified], still owed .
