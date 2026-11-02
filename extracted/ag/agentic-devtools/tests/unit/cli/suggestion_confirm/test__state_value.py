"""Tests for _state_value."""

from agentic_devtools.cli.suggestion_confirm import _state_value


def test_prefers_canonical_key_before_fallback() -> None:
    state = {"discussion_id": 2, "github": {"comment_id": 9}}

    assert _state_value(state, "discussion_id", "github.comment_id") == 2


def test_falls_back_when_intermediate_value_is_not_a_mapping() -> None:
    state = {"github": "not-a-mapping", "comment_id": 10}

    assert _state_value(state, "github.comment_id", "comment_id") == 10


def test_preserves_explicit_falsey_values_in_preferred_key() -> None:
    state = {"github": {"comment_id": 0}, "comment_id": 10}

    assert _state_value(state, "github.comment_id", "comment_id") == 0


def test_returns_none_when_all_candidates_are_missing_or_none() -> None:
    state = {"github": {"comment_id": None}, "discussion_id": None}

    assert _state_value(state, "github.comment_id", "discussion_id") is None
