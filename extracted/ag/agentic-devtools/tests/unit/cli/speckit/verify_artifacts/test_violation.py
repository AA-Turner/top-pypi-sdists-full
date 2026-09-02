"""Tests for the ``Violation`` dataclass."""

from agentic_devtools.cli.speckit.verify_artifacts import CHECK_REFERENCED_PATH, Violation


class TestViolation:
    """Construction and serialisation."""

    def test_to_dict_returns_all_fields(self) -> None:
        violation = Violation(
            check=CHECK_REFERENCED_PATH,
            artifact="plan.md",
            detail="plan.md (L1) references 'nope.py'.",
        )

        assert violation.to_dict() == {
            "check": CHECK_REFERENCED_PATH,
            "artifact": "plan.md",
            "detail": "plan.md (L1) references 'nope.py'.",
        }

    def test_is_hashable_so_violations_can_be_deduplicated(self) -> None:
        first = Violation(check="checklist", artifact="a.md", detail="d")
        second = Violation(check="checklist", artifact="a.md", detail="d")

        assert len({first, second}) == 1
