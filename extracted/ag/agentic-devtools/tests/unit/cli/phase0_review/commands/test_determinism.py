"""Tests for deterministic and read-only review behavior."""

import hashlib

from agentic_devtools.cli.phase0_review.commands import run_review


def test_repeated_runs_are_identical_and_preserve_all_inputs(make_review_case, tmp_path):
    payload, integrity = make_review_case()
    protected = [
        payload,
        integrity,
        tmp_path / "issue.md",
        tmp_path / "template.md",
        tmp_path / "structure_snapshot.md",
    ]
    before = {path: hashlib.sha256(path.read_bytes()).digest() for path in protected}
    first = run_review(repo_root=tmp_path, input_path=payload, integrity_path=integrity)
    second = run_review(repo_root=tmp_path, input_path=payload, integrity_path=integrity)
    after = {path: hashlib.sha256(path.read_bytes()).digest() for path in protected}
    assert first == second
    assert before == after
