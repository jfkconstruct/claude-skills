"""Risk register for release_gate.py, one hard-failing check per named risk.

Run: python -m pytest test_release_gate.py -q
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))
from release_gate import DEFAULT_KINDS, load_evidence, verify  # noqa: E402

HERE = Path(__file__).parent


def facts_json(tmp_path, data):
    p = tmp_path / "facts.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    return p


# invented id released
def test_invented_ref_is_rejected():
    reasons = verify("Ship #42 today.", "pending: #41, #43")
    assert reasons == ["ref not in evidence: #42"]


# invented date released
def test_invented_date_is_rejected():
    reasons = verify("Demo is on 2026-09-24.", "day: 2026-09-19")
    assert reasons == ["date not in evidence: 2026-09-24"]


# good claim blocked
def test_grounded_claim_is_verified():
    ev = "day 2026-09-19; pending #41; url https://example.org/view/41; commit a1b2c3d"
    assert verify("Read #41 at https://example.org/view/41 today (2026-09-19), commit a1b2c3d.", ev) == []


# policy text used as evidence
def test_excluded_keys_never_ground(tmp_path):
    p = facts_json(tmp_path, {"history": ["2024-01-01 #7 shipped"], "pending": ["#9"]})
    ev = load_evidence([p])
    assert verify("Reshipping #7 from 2024-01-01.", ev) == [
        "date not in evidence: 2024-01-01",
        "ref not in evidence: #7",
    ]
    assert verify("Read #9.", ev) == []


# required item unnamed
def test_require_pattern():
    assert verify("Nothing to read.", "pending /view/5", require=[r"/view/\d+"]) == [
        "required pattern absent: /view/\\d+"
    ]
    assert verify("Read /view/5.", "pending /view/5", require=[r"/view/\d+"]) == []


# empty producer output released
def test_empty_claim_is_rejected():
    assert verify("   ", "anything") == ["empty claim"]


# opt-in kinds stay off by default (false rejections on prose numbers)
def test_number_and_path_are_opt_in():
    claim = "Coverage rose to 87% in src/app/main.py."
    assert verify(claim, "no numbers here") == []
    reasons = verify(claim, "no numbers here", kinds=DEFAULT_KINDS + ("number", "path"))
    assert reasons == ["number not in evidence: 87%", "path not in evidence: src/app/main.py"]


# rejection recovers to the fallback and the claim is ledgered for audit
def test_cli_rejects_to_fallback_and_ledgers(tmp_path):
    claim = tmp_path / "claim.md"
    claim.write_text("Ship #99.", encoding="utf-8")
    fallback = tmp_path / "fallback.md"
    fallback.write_text("Nothing found.", encoding="utf-8")
    facts = facts_json(tmp_path, {"pending": ["#1"]})
    ledger = tmp_path / "gate.jsonl"
    run = subprocess.run(
        [sys.executable, str(HERE / "release_gate.py"), "--claim", str(claim), "--evidence", str(facts),
         "--fallback", str(fallback), "--ledger", str(ledger), "--label", "test"],
        capture_output=True, text=True,
    )
    assert run.returncode == 1
    assert run.stdout == "Nothing found."
    assert "REJECTED" in run.stderr and "#99" in run.stderr
    row = json.loads(ledger.read_text(encoding="utf-8").strip())
    assert row["verdict"] == "rejected" and row["state"] == "recovered"
    assert row["rejected_claim"] == "Ship #99." and row["label"] == "test"


# a verified claim passes through unchanged
def test_cli_verified_prints_claim(tmp_path):
    claim = tmp_path / "claim.md"
    claim.write_text("Ship #1.", encoding="utf-8")
    facts = facts_json(tmp_path, {"pending": ["#1"]})
    run = subprocess.run(
        [sys.executable, str(HERE / "release_gate.py"), "--claim", str(claim), "--evidence", str(facts)],
        capture_output=True, text=True,
    )
    assert run.returncode == 0 and run.stdout == "Ship #1."


# unknown kind fails loudly, never releases
def test_unknown_kind_is_usage_error(tmp_path):
    claim = tmp_path / "claim.md"
    claim.write_text("x", encoding="utf-8")
    facts = facts_json(tmp_path, {})
    run = subprocess.run(
        [sys.executable, str(HERE / "release_gate.py"), "--claim", str(claim), "--evidence", str(facts),
         "--kinds", "date,bogus"],
        capture_output=True, text=True,
    )
    assert run.returncode == 2 and run.stdout == ""


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
