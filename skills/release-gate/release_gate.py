"""release_gate.py: a read-only grounding verifier between "the producer says done" and "the result ships".

Three events stay distinct: the work is correct, the producer claims completion, the system
releases the result. This script owns the third one. It never sees the producer's reasoning,
only the claim (the artifact about to ship) and the evidence (the inputs the producer was
allowed to cite). Every specific token in the claim (dates, URLs, ticket refs, commit hashes,
and optionally file paths and numbers) must appear in the evidence, or the claim is rejected.

Deterministic on purpose. A grounding check by different code is more independent than a
second model, costs nothing, and its false rejections are reproducible and auditable.

Usage:
    python release_gate.py --claim brief.md --evidence facts.json
    python release_gate.py --claim pr.md --evidence diff.txt --evidence issue.json --kinds date,url,ref,hash,path
    python release_gate.py --claim out.md --evidence facts.json --require "/view/\\d+" --ledger gate.jsonl

Exit 0: VERIFIED (release). Exit 1: REJECTED (recover to the fallback, never retry the producer).
Exit 2: usage error.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# Each kind is a regex over the claim. A match must appear verbatim in the evidence text.
KINDS: dict[str, re.Pattern[str]] = {
    "date": re.compile(r"\b\d{4}-\d{2}-\d{2}\b"),
    "url": re.compile(r"https?://[^\s)\]>\"']+"),
    "ref": re.compile(r"(?<![\w/])#\d+\b|\b[A-Z][A-Z0-9]{1,9}-\d+\b"),
    "hash": re.compile(r"\b[0-9a-f]{7,40}\b"),
    "path": re.compile(r"(?<![\w.])(?:[\w.-]+/)+[\w.-]+\.[A-Za-z0-9]{1,8}\b"),
    "number": re.compile(r"(?<![\w.-])\d+(?:\.\d+)?%?(?![\w.-])"),
}
DEFAULT_KINDS = ("date", "url", "ref", "hash")

# Keys that never ground a claim when the evidence is JSON: policy text, seeds, and the whole
# history would let the producer cite any date or id that ever existed.
DEFAULT_EXCLUDE_KEYS = ("system_prompt", "policy", "seed", "history", "constitution")


def load_evidence(paths: list[Path], exclude_keys: tuple[str, ...] = DEFAULT_EXCLUDE_KEYS) -> str:
    """Serialize every evidence file into one grounding string.

    JSON files drop the excluded top-level keys first; every other file is read as text.
    """
    parts: list[str] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        if path.suffix.lower() == ".json":
            try:
                data = json.loads(text)
            except json.JSONDecodeError:
                data = None
            if isinstance(data, dict):
                data = {k: v for k, v in data.items() if k not in exclude_keys}
                text = json.dumps(data, ensure_ascii=False, default=str)
        parts.append(text)
    return "\n".join(parts)


def verify(claim: str, evidence: str, kinds: tuple[str, ...] = DEFAULT_KINDS,
           require: list[str] | None = None) -> list[str]:
    """Return the reasons the claim must not be released; an empty list means VERIFIED."""
    if not isinstance(claim, str) or not claim.strip():
        return ["empty claim"]
    reasons: list[str] = []
    for kind in kinds:
        pattern = KINDS.get(kind)
        if pattern is None:
            reasons.append(f"unknown kind: {kind}")
            continue
        for token in sorted(set(pattern.findall(claim))):
            if token not in evidence:
                reasons.append(f"{kind} not in evidence: {token}")
    for rx in require or []:
        if not re.search(rx, claim):
            reasons.append(f"required pattern absent: {rx}")
    return reasons


def ledger_row(claim: str, reasons: list[str], kinds: tuple[str, ...], label: str | None) -> dict:
    return {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "label": label,
        "verdict": "verified" if not reasons else "rejected",
        "state": "released" if not reasons else "recovered",
        "kinds": list(kinds),
        "reject_reasons": reasons,
        # The rejected claim is kept so a false rejection can be audited, not hidden.
        "rejected_claim": None if not reasons else claim,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--claim", required=True, type=Path, help="the artifact about to ship")
    ap.add_argument("--evidence", required=True, type=Path, action="append",
                    help="an input the producer was allowed to cite (repeatable)")
    ap.add_argument("--kinds", default=",".join(DEFAULT_KINDS),
                    help=f"comma list from {sorted(KINDS)} (default {','.join(DEFAULT_KINDS)})")
    ap.add_argument("--exclude-key", action="append", default=list(DEFAULT_EXCLUDE_KEYS),
                    help="JSON top-level key that never grounds a claim (repeatable)")
    ap.add_argument("--require", action="append", default=[],
                    help="regex the claim must match, e.g. a named item id (repeatable)")
    ap.add_argument("--fallback", type=Path, help="printed to stdout instead of the claim on rejection")
    ap.add_argument("--ledger", type=Path, help="append one JSON row per run here")
    ap.add_argument("--label", help="free text for the ledger row (role, run id)")
    args = ap.parse_args(argv)

    kinds = tuple(k.strip() for k in args.kinds.split(",") if k.strip())
    unknown = [k for k in kinds if k not in KINDS]
    if unknown:
        print(f"unknown kinds: {', '.join(unknown)}", file=sys.stderr)
        return 2
    try:
        claim = args.claim.read_text(encoding="utf-8")
        evidence = load_evidence(args.evidence, tuple(args.exclude_key))
    except OSError as exc:
        print(f"cannot read: {exc}", file=sys.stderr)
        return 2

    reasons = verify(claim, evidence, kinds, args.require)
    if args.ledger:
        with args.ledger.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(ledger_row(claim, reasons, kinds, args.label), ensure_ascii=False) + "\n")

    if not reasons:
        print("VERIFIED", file=sys.stderr)
        sys.stdout.write(claim)
        return 0
    print("REJECTED", file=sys.stderr)
    for reason in reasons:
        print(f"  - {reason}", file=sys.stderr)
    if args.fallback:
        sys.stdout.write(args.fallback.read_text(encoding="utf-8"))
    return 1


if __name__ == "__main__":
    sys.exit(main())
