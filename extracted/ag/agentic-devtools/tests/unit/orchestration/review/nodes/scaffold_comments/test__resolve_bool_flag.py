"""Tests for ``_resolve_bool_flag()``."""

from __future__ import annotations

from agentic_devtools.orchestration.review.nodes.scaffold_comments import _resolve_bool_flag


class TestResolveBoolFlag:
    """FR-006, NFR-003: boolean flag resolution from get_value() only."""

    def test_returns_true_for_bool_true(self) -> None:
        """Boolean True from get_value is returned directly."""
        assert _resolve_bool_flag({}, "dry_run", lambda _: True) is True

    def test_returns_false_for_bool_false(self) -> None:
        """Boolean False from get_value is returned directly."""
        assert _resolve_bool_flag({}, "dry_run", lambda _: False) is False

    def test_returns_true_for_string_true(self) -> None:
        """String 'true' is treated as True."""
        assert _resolve_bool_flag({}, "dry_run", lambda _: "true") is True

    def test_returns_true_for_string_yes(self) -> None:
        """String 'yes' is treated as True."""
        assert _resolve_bool_flag({}, "dry_run", lambda _: "yes") is True

    def test_returns_true_for_string_one(self) -> None:
        """String '1' is treated as True."""
        assert _resolve_bool_flag({}, "dry_run", lambda _: "1") is True

    def test_returns_false_for_string_false(self) -> None:
        """String 'false' is treated as False."""
        assert _resolve_bool_flag({}, "dry_run", lambda _: "false") is False

    def test_returns_false_for_none(self) -> None:
        """None from get_value is treated as False."""
        assert _resolve_bool_flag({}, "dry_run", lambda _: None) is False

    def test_returns_false_for_non_bool_non_string(self) -> None:
        """Non-bool, non-string values are treated as False."""
        assert _resolve_bool_flag({}, "dry_run", lambda _: 42) is False

    def test_case_insensitive_string(self) -> None:
        """String matching is case-insensitive."""
        assert _resolve_bool_flag({}, "dry_run", lambda _: "TRUE") is True
        assert _resolve_bool_flag({}, "dry_run", lambda _: "True") is True

    def test_strips_whitespace(self) -> None:
        """Whitespace around string value is stripped."""
        assert _resolve_bool_flag({}, "dry_run", lambda _: "  true  ") is True

    def test_passes_correct_state_key(self) -> None:
        """The correct state key is passed to get_value_fn."""
        captured_keys: list[str] = []

        def capture_key(key: str) -> None:
            captured_keys.append(key)
            return None

        _resolve_bool_flag({}, "review.force_rereview", capture_key)
        assert captured_keys == ["review.force_rereview"]

    def test_does_not_read_config_from_state(self) -> None:
        """state['config'] is never consulted for runtime flags."""
        state = {"config": {"dry_run": True, "force_rereview": True}}
        assert _resolve_bool_flag(state, "dry_run", lambda _: None) is False
