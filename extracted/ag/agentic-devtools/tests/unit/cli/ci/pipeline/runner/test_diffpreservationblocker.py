"""Tests for DiffPreservationBlocker."""

from agentic_devtools.cli.ci.pipeline.runner import DiffPreservationBlocker


class TestDiffPreservationBlocker:
    """Tests for the persisted diff-preservation blocker contract."""

    def test_declares_expected_required_keys(self) -> None:
        """The TypedDict exposes the persisted baseline fields required across runs."""
        assert DiffPreservationBlocker.__required_keys__ == {
            "baseline_head",
            "baseline_files",
            "baseline_hash",
            "baseline_hash_available",
            "fingerprint_supported",
            "allow_file_removal",
            "intentional_noop",
        }

    def test_declares_optional_backward_compatible_fields(self) -> None:
        """Older persisted blockers may omit the base branch and removal allowlist."""
        assert DiffPreservationBlocker.__optional_keys__ == {
            "baseline_base",
            "baseline_base_sha",
            "allowed_removed_files",
        }
