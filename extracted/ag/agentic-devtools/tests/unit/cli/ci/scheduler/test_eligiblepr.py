"""Tests for EligiblePR dataclass."""

from agentic_devtools.cli.ci.scheduler import EligiblePR


class TestEligiblePR:
    """Tests for the EligiblePR frozen dataclass."""

    def test_create_instance(self) -> None:
        pr = EligiblePR(number=2020, created_at="2024-01-01T00:00:00Z")
        assert pr.number == 2020
        assert pr.created_at == "2024-01-01T00:00:00Z"

    def test_labels_to_propagate_defaults_to_empty(self) -> None:
        pr = EligiblePR(number=2020, created_at="2024-01-01T00:00:00Z")
        assert pr.labels_to_propagate == ()

    def test_labels_to_propagate_is_preserved(self) -> None:
        pr = EligiblePR(
            number=2020,
            created_at="2024-01-01T00:00:00Z",
            labels_to_propagate=("ai-auto-merge-allowed",),
        )
        assert pr.labels_to_propagate == ("ai-auto-merge-allowed",)

    def test_frozen(self) -> None:
        pr = EligiblePR(number=2020, created_at="2024-01-01T00:00:00Z")
        import pytest

        with pytest.raises(AttributeError):
            pr.number = 2021  # type: ignore[misc]

    def test_equality(self) -> None:
        pr1 = EligiblePR(number=2020, created_at="2024-01-01T00:00:00Z")
        pr2 = EligiblePR(number=2020, created_at="2024-01-01T00:00:00Z")
        assert pr1 == pr2
