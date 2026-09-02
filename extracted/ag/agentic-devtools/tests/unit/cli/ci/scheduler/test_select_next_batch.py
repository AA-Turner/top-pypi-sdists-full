"""Tests for select_next_batch round-robin scheduling."""

from agentic_devtools.cli.ci.scheduler import EligiblePR, select_next_batch


def _make_prs(*numbers: int) -> list[EligiblePR]:
    """Helper to create EligiblePR list from PR numbers."""
    return [EligiblePR(number=n, created_at=f"2024-01-{i + 1:02d}T00:00:00Z") for i, n in enumerate(numbers)]


class TestSelectNextBatch:
    """Tests for the select_next_batch pure function."""

    def test_empty_list_returns_empty(self) -> None:
        assert select_next_batch([], None, 3) == []

    def test_no_cursor_starts_from_beginning(self) -> None:
        prs = _make_prs(2020, 2021, 2022, 2023)
        assert select_next_batch(prs, None, 2) == [2020, 2021]

    def test_cursor_at_middle_resumes_next(self) -> None:
        prs = _make_prs(2020, 2021, 2022, 2023)
        assert select_next_batch(prs, 2021, 2) == [2022, 2023]

    def test_cursor_at_end_wraps_around(self) -> None:
        prs = _make_prs(2020, 2021, 2022, 2023)
        assert select_next_batch(prs, 2023, 2) == [2020, 2021]

    def test_cursor_not_in_list_starts_from_beginning(self) -> None:
        prs = _make_prs(2020, 2021, 2022)
        assert select_next_batch(prs, 9999, 2) == [2020, 2021]

    def test_batch_size_larger_than_eligible_returns_all(self) -> None:
        prs = _make_prs(2020, 2021, 2022)
        result = select_next_batch(prs, None, 10)
        assert result == [2020, 2021, 2022]

    def test_batch_wraps_to_fill_target(self) -> None:
        prs = _make_prs(2020, 2021, 2022, 2023)
        # Cursor at 2022, batch_size=3 → [2023, 2020, 2021]
        assert select_next_batch(prs, 2022, 3) == [2023, 2020, 2021]

    def test_single_pr_returns_it(self) -> None:
        prs = _make_prs(2020)
        assert select_next_batch(prs, None, 1) == [2020]

    def test_single_pr_with_cursor_on_it_wraps(self) -> None:
        prs = _make_prs(2020)
        assert select_next_batch(prs, 2020, 1) == [2020]

    def test_batch_size_one_default(self) -> None:
        prs = _make_prs(2020, 2021, 2022)
        assert select_next_batch(prs, 2020, 1) == [2021]

    def test_batch_size_clamped_to_max_100(self) -> None:
        prs = _make_prs(1, 2, 3)
        result = select_next_batch(prs, None, 200)
        assert result == [1, 2, 3]  # Capped at len(prs)
