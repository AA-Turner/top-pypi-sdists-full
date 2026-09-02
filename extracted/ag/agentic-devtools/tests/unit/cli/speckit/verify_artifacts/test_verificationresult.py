"""Tests for the ``VerificationResult`` dataclass."""

from agentic_devtools.cli.speckit.verify_artifacts import VerificationResult, Violation


class TestVerificationResultPassed:
    """The ``passed`` property."""

    def test_passed_is_true_when_no_violations(self) -> None:
        result = VerificationResult(violations=[], checks_run=["checklist"])

        assert result.passed is True

    def test_passed_is_false_when_any_violation(self) -> None:
        result = VerificationResult(
            violations=[Violation(check="checklist", artifact="a.md", detail="d")],
            checks_run=["checklist"],
        )

        assert result.passed is False

    def test_passed_is_true_when_no_checks_ran(self) -> None:
        result = VerificationResult(violations=[], checks_run=[])

        assert result.passed is True


class TestVerificationResultToJson:
    """The ``to_json`` serialisation."""

    def test_to_json_includes_passed_checks_and_violations(self) -> None:
        result = VerificationResult(
            violations=[Violation(check="fr-reference", artifact="tasks.md", detail="d")],
            checks_run=["fr-reference"],
        )

        assert result.to_json() == {
            "passed": False,
            "checks_run": ["fr-reference"],
            "violations": [{"check": "fr-reference", "artifact": "tasks.md", "detail": "d"}],
        }

    def test_to_json_copies_checks_run_rather_than_aliasing(self) -> None:
        checks = ["checklist"]
        result = VerificationResult(violations=[], checks_run=checks)

        payload = result.to_json()
        checks.append("mutated")

        assert payload["checks_run"] == ["checklist"]
