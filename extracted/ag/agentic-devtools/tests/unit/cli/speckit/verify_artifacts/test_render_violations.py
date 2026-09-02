"""Tests for ``render_violations()``."""

from agentic_devtools.cli.speckit.verify_artifacts import (
    VerificationResult,
    Violation,
    render_violations,
)


class TestRenderViolations:
    """Human-readable rendering of a verification result."""

    def test_reports_no_applicable_checks(self) -> None:
        output = render_violations(VerificationResult(violations=[], checks_run=[]))

        assert "No checks apply to this phase" in output
        assert "Checks run:" not in output

    def test_reports_a_pass(self) -> None:
        output = render_violations(VerificationResult(violations=[], checks_run=["checklist"]))

        assert "Checks run: checklist" in output
        assert "Result: PASS" in output

    def test_reports_a_failure_with_every_violation(self) -> None:
        result = VerificationResult(
            violations=[
                Violation(check="fr-reference", artifact="tasks.md", detail="FR-009 undefined."),
                Violation(check="checklist", artifact="checklists/a.md", detail="No items."),
            ],
            checks_run=["fr-reference", "checklist"],
        )

        output = render_violations(result)

        assert "Result: FAIL — 2 violation(s):" in output
        assert "- [fr-reference] tasks.md: FR-009 undefined." in output
        assert "- [checklist] checklists/a.md: No items." in output

    def test_starts_with_a_markdown_heading(self) -> None:
        output = render_violations(VerificationResult(violations=[], checks_run=["checklist"]))

        assert output.startswith("## SpecKit Artifact Verification")
