"""Tests for deterministic timeout handling."""

from unittest.mock import patch

from agentic_devtools.cli.phase0_review import commands
from agentic_devtools.cli.phase0_review.commands import run_review


def test_run_review_uses_fixed_timeout_finding_without_elapsed_time(make_review_case, tmp_path):
    payload, integrity = make_review_case()
    report = run_review(
        repo_root=tmp_path,
        input_path=payload,
        integrity_path=integrity,
        clock=lambda: 10.0,
        deadline=10.0,
    )
    assert "- [ ] Operational timeout: review exceeded the 120-second ceiling" in report
    assert "- [x] No content-fidelity checks performed" in report
    assert report.endswith("CHANGES REQUESTED")


def test_timeout_checks_cover_each_pipeline_boundary(make_review_case, tmp_path):
    payload, integrity = make_review_case()
    for values in (
        [0, 0, 120],
        [0, 0, 0, 120],
        [0, 0, 0, 0, 120],
        [0, 0, 0, 0, 0, 120],
    ):
        iterator = iter(values)
        report = run_review(
            repo_root=tmp_path,
            input_path=payload,
            integrity_path=integrity,
            clock=lambda: next(iterator),
        )
        assert "Operational timeout" in report


def test_timeout_after_structure_preserves_completed_template_findings(make_review_case, tmp_path):
    payload, integrity = make_review_case()
    calls = 0

    def clock():
        nonlocal calls
        calls += 1
        return 120.0 if calls == 6 else 0.0

    with patch.object(commands, "PROCESSING_TIMEOUT_SECONDS", 120.0):
        report = run_review(
            repo_root=tmp_path,
            input_path=payload,
            integrity_path=integrity,
            clock=clock,
        )
    assert "Operational timeout" in report


def test_timeout_inside_utf8_decode_error_boundaries(make_review_case, tmp_path):
    payload, integrity = make_review_case()
    (tmp_path / "issue.md").write_bytes(b"\xff invalid utf-8")
    for values in ([0, 0, 0, 0, 120],):
        iterator = iter(values)
        report = run_review(
            repo_root=tmp_path,
            input_path=payload,
            integrity_path=integrity,
            clock=lambda: next(iterator),
        )
        assert "Operational timeout" in report

    payload2, integrity2 = make_review_case()
    (tmp_path / "structure_snapshot.md").write_bytes(b"\xff invalid utf-8")
    for values in ([0, 0, 0, 0, 120],):
        iterator = iter(values)
        report = run_review(
            repo_root=tmp_path,
            input_path=payload2,
            integrity_path=integrity2,
            clock=lambda: next(iterator),
        )
        assert "Operational timeout" in report
