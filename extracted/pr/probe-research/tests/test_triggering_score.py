"""The triggering eval's scorer, deterministically.

The runner needs a key and stays manual, but scoring synthetic JSONL is
offline and sub-second — and the recall/restraint figures it prints are the
numbers quoted in the commit that ships a prose change. An eval that silently
mis-scores produces a figure people quote (the same principle
tests/test_eval_harness.py records for the sibling harness).
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

EVAL = Path(__file__).resolve().parents[1] / "evals" / "triggering"


def _load_score():
    spec = importlib.util.spec_from_file_location("_triggering_score", EVAL / "score.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _row(**kw) -> dict:
    base = {
        "arm": "worktree",
        "model": "judge-model",
        "prose_digest": "abc123",
        "id": "case",
        "category": "positive",
        "sample": 0,
        "expect_probe": True,
        "got_probe": True,
        "pass": True,
    }
    base.update(kw)
    return base


def test_recall_restraint_and_error_exclusion(tmp_path, capsys) -> None:
    rows = [
        _row(id="pos-hit"),  # fired: recall +
        _row(id="pos-miss", got_probe=False, **{"pass": False}),  # missed
        _row(
            id="neg-quiet", category="negative", expect_probe=False, got_probe=False
        ),  # restraint +
        _row(
            id="neg-fired",
            category="negative",
            expect_probe=False,
            got_probe=True,
            **{"pass": False},
        ),  # restraint -
        {
            "arm": "worktree",
            "model": "judge-model",
            "id": "err",
            "category": "positive",
            "sample": 0,
            "error": "boom",
            "pass": False,
        },
    ]
    p = tmp_path / "r.jsonl"
    p.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")

    _load_score().main([str(p)])
    out = capsys.readouterr().out

    # 1 of 2 positives fired; 1 of 2 negatives stayed quiet; the error row is
    # excluded from BOTH denominators and reported as an error, not a miss.
    import re

    assert re.search(r"trigger recall.*?50\.0%\s+n=2", out)
    assert re.search(r"negative restraint.*?50\.0%\s+n=2", out)
    assert "1 errors" in out
    assert "ERROR err: boom" in out


def test_mixed_models_in_one_arm_warn(tmp_path, capsys) -> None:
    rows = [_row(id="a"), _row(id="b", model="other-model")]
    p = tmp_path / "r.jsonl"
    p.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")

    _load_score().main([str(p)])
    assert "WARNING" in capsys.readouterr().out
