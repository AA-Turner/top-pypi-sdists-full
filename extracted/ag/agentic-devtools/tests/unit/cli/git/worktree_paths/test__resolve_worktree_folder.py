"""Tests for _resolve_worktree_folder."""

import pytest

from agentic_devtools.cli.git import worktree_paths


class TestResolveWorktreeFolder:
    """Tests for _resolve_worktree_folder."""

    def test_key_absent_defaults_to_wt(self) -> None:
        """An absent config key resolves to the default sibling wt folder."""
        assert worktree_paths._resolve_worktree_folder("ignored", key_present=False) == "wt"

    def test_none_value_opts_out_to_direct_sibling(self) -> None:
        """An explicit null value opts out to the legacy direct-sibling layout."""
        assert worktree_paths._resolve_worktree_folder(None, key_present=True) is None

    @pytest.mark.parametrize("raw_value", ["", "   "])
    def test_blank_string_opts_out_to_direct_sibling(self, raw_value: str) -> None:
        """A blank/whitespace-only string opts out the same as null."""
        assert worktree_paths._resolve_worktree_folder(raw_value, key_present=True) is None

    def test_valid_string_is_trimmed_and_validated(self) -> None:
        """A valid string is trimmed and passed through validation."""
        assert worktree_paths._resolve_worktree_folder("  custom-wt  ", key_present=True) == "custom-wt"

    def test_rejects_boolean_value(self) -> None:
        """A boolean value is rejected even though bool is technically an int subclass."""
        with pytest.raises(ValueError, match="booleans are not allowed"):
            worktree_paths._resolve_worktree_folder(False, key_present=True)

    @pytest.mark.parametrize("raw_value", [0, 1.5, {}])
    def test_rejects_non_string_non_null_values(self, raw_value: object) -> None:
        """Any non-string, non-null, non-boolean value is rejected with its type named."""
        with pytest.raises(ValueError, match=f"got {type(raw_value).__name__}"):
            worktree_paths._resolve_worktree_folder(raw_value, key_present=True)
