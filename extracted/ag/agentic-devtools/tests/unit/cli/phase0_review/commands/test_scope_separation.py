"""Tests for factual-only review scope."""

from agentic_devtools.cli.phase0_review.commands import run_review


def test_factually_correct_awkward_prose_is_approved(make_review_case, tmp_path):
    payload, integrity = make_review_case(source_updates={"body": "Awkward. Words. Still factual."})
    report = run_review(repo_root=tmp_path, input_path=payload, integrity_path=integrity)
    assert "APPROVED" in report
    assert "quality" not in report.lower()
    assert "testability" not in report.lower()
