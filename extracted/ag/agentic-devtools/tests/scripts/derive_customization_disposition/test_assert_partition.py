"""Tests for assert_partition in derive_customization_disposition."""

from __future__ import annotations

import pytest

from tests.scripts.derive_customization_disposition import derive, row


def test_valid_rows_pass() -> None:
    """Three batches, one per row, summing to the row count."""
    rows = [
        row(path="a", batch="stubs", disposition="delete", group="-", target="-"),
        row(path="b", batch="wrappers", disposition="delete", group="-", target="-"),
        row(path="c", batch="residue"),
    ]
    derive.assert_partition(rows, expected_total=3)


def test_unknown_batch_raises() -> None:
    """A row outside the partition is the gap the complement rule exists to prevent."""
    with pytest.raises(ValueError, match="outside the partition"):
        derive.assert_partition([row(batch="other")])


def test_duplicate_file_raises() -> None:
    """Every file must appear exactly once."""
    with pytest.raises(ValueError, match="more than once"):
        derive.assert_partition([row(), row()])


def test_unknown_disposition_raises() -> None:
    """The disposition vocabulary is closed."""
    with pytest.raises(ValueError, match="outside the vocabulary"):
        derive.assert_partition([row(disposition="archive")])


def test_unknown_group_raises() -> None:
    """The eight group names are fixed; later issues select rows by them."""
    with pytest.raises(ValueError, match="outside the eight names"):
        derive.assert_partition([row(group="singleton-c")])


def test_delete_row_with_a_group_raises() -> None:
    """A deleted file has no group, because nothing survives to be grouped."""
    with pytest.raises(ValueError, match="must carry group"):
        derive.assert_partition([row(disposition="delete", group="git-and-pr", batch="residue")])


def test_non_delete_row_with_dash_group_raises() -> None:
    """A surviving (non-delete) row omitted from all group selectors is a derivation error."""
    with pytest.raises(ValueError, match="non-delete rows must carry a named group"):
        derive.assert_partition([row(disposition="skill", group="-", batch="residue")])


def test_wrong_total_raises() -> None:
    """The row count must equal the number of units on disk."""
    with pytest.raises(ValueError, match="does not equal the expected"):
        derive.assert_partition([row()], expected_total=2)
