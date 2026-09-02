"""Tests for batch_branch_name()."""

from agentic_devtools.cli.audit.config import batch_branch_name


class TestBatchBranchName:
    """Shared staging branch-name derivation."""

    def test_uses_first_eight_chars(self) -> None:
        assert batch_branch_name("19de413c0a1b2c3d") == "audit/batch-19de413c"

    def test_short_id_used_as_is(self) -> None:
        assert batch_branch_name("abc") == "audit/batch-abc"

    def test_matches_dispatch_convention(self) -> None:
        # Mirrors the historical f"audit/batch-{batch_id[:8]}" form used by dispatch.
        batch_id = "batch-123"
        assert batch_branch_name(batch_id) == f"audit/batch-{batch_id[:8]}"
