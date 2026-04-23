"""Tests for hook event taxonomy and config validation boundary (#1494).

Verifies that:
- Phase-1 constants are correct and included in PHASE_1_HOOK_EVENTS
- Phase-2 constants are correct and included in PHASE_2_HOOK_EVENTS
- ALL_HOOK_EVENTS is the union of both sets
- Config validator accepts phase-1 event keys without taxonomy errors
- Config validator rejects phase-2 event keys with a clear "reserved" error
- Config validator rejects unknown event keys with a clear error
"""

from __future__ import annotations

import pytest

from anteroom.services.config_validator import validate_config
from anteroom.services.hooks import (
    ALL_HOOK_EVENTS,
    HOOK_EVENT_APPROVAL_REQUESTED,
    HOOK_EVENT_APPROVAL_RESOLVED,
    HOOK_EVENT_NOTIFICATION,
    HOOK_EVENT_POST_TOOL,
    HOOK_EVENT_PRE_TOOL,
    HOOK_EVENT_SESSION_START,
    HOOK_EVENT_STOP,
    PHASE_1_HOOK_EVENTS,
    PHASE_2_HOOK_EVENTS,
)

# ---------------------------------------------------------------------------
# Taxonomy constants
# ---------------------------------------------------------------------------


def test_phase1_event_values() -> None:
    assert HOOK_EVENT_PRE_TOOL == "pre_tool"
    assert HOOK_EVENT_POST_TOOL == "post_tool"


def test_phase2_event_values() -> None:
    assert HOOK_EVENT_SESSION_START == "session_start"
    assert HOOK_EVENT_STOP == "stop"
    assert HOOK_EVENT_APPROVAL_REQUESTED == "approval_requested"
    assert HOOK_EVENT_APPROVAL_RESOLVED == "approval_resolved"
    assert HOOK_EVENT_NOTIFICATION == "notification"


def test_phase1_set_contains_expected_events() -> None:
    assert HOOK_EVENT_PRE_TOOL in PHASE_1_HOOK_EVENTS
    assert HOOK_EVENT_POST_TOOL in PHASE_1_HOOK_EVENTS
    assert len(PHASE_1_HOOK_EVENTS) == 2


def test_phase2_set_contains_expected_events() -> None:
    assert HOOK_EVENT_SESSION_START in PHASE_2_HOOK_EVENTS
    assert HOOK_EVENT_STOP in PHASE_2_HOOK_EVENTS
    assert HOOK_EVENT_APPROVAL_REQUESTED in PHASE_2_HOOK_EVENTS
    assert HOOK_EVENT_APPROVAL_RESOLVED in PHASE_2_HOOK_EVENTS
    assert HOOK_EVENT_NOTIFICATION in PHASE_2_HOOK_EVENTS
    assert len(PHASE_2_HOOK_EVENTS) == 5


def test_all_events_is_union_of_both_phases() -> None:
    assert ALL_HOOK_EVENTS == PHASE_1_HOOK_EVENTS | PHASE_2_HOOK_EVENTS


def test_phase1_and_phase2_are_disjoint() -> None:
    assert PHASE_1_HOOK_EVENTS.isdisjoint(PHASE_2_HOOK_EVENTS)


# ---------------------------------------------------------------------------
# Config validation — phase-1 events are accepted
# ---------------------------------------------------------------------------


def _minimal_hook_entry(event_key: str) -> dict:
    return {
        event_key: [
            {
                "id": "test-hook",
                "matcher": {"tool_name": "*"},
                "runner": {"type": "command", "command": "/usr/bin/true"},
            }
        ]
    }


def test_pre_tool_event_key_is_accepted() -> None:
    raw = {"hooks": _minimal_hook_entry("pre_tool")}
    result = validate_config(raw)
    taxonomy_errors = [e for e in result.errors if "reserved phase-2" in e.message or "unknown hook event" in e.message]
    assert taxonomy_errors == [], f"unexpected taxonomy errors: {taxonomy_errors}"


def test_post_tool_event_key_is_accepted() -> None:
    raw = {"hooks": _minimal_hook_entry("post_tool")}
    result = validate_config(raw)
    taxonomy_errors = [e for e in result.errors if "reserved phase-2" in e.message or "unknown hook event" in e.message]
    assert taxonomy_errors == [], f"unexpected taxonomy errors: {taxonomy_errors}"


# ---------------------------------------------------------------------------
# Config validation — phase-2 events produce a clear reserved error
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "event_key",
    [
        "session_start",
        "stop",
        "approval_requested",
        "approval_resolved",
        "notification",
    ],
)
def test_phase2_event_key_produces_reserved_error(event_key: str) -> None:
    raw: dict = {"hooks": {event_key: []}}
    result = validate_config(raw)
    errors = [e for e in result.errors if e.path == f"hooks.{event_key}"]
    assert len(errors) == 1, f"expected exactly one error for hooks.{event_key}, got {errors}"
    assert "reserved phase-2" in errors[0].message
    assert "pre_tool" in errors[0].message
    assert "post_tool" in errors[0].message
    assert errors[0].severity == "error"


def test_phase2_error_message_mentions_later_release() -> None:
    raw: dict = {"hooks": {"session_start": []}}
    result = validate_config(raw)
    errors = [e for e in result.errors if e.path == "hooks.session_start"]
    assert errors, "expected an error for hooks.session_start"
    assert "later release" in errors[0].message


# ---------------------------------------------------------------------------
# Config validation — unknown event keys produce a clear error
# ---------------------------------------------------------------------------


def test_unknown_event_key_produces_error() -> None:
    raw: dict = {"hooks": {"on_magic": []}}
    result = validate_config(raw)
    errors = [e for e in result.errors if e.path == "hooks.on_magic"]
    assert len(errors) == 1, f"expected one error for hooks.on_magic, got {errors}"
    assert "unknown hook event" in errors[0].message
    assert errors[0].severity == "error"


def test_unknown_event_error_lists_supported_events() -> None:
    raw: dict = {"hooks": {"on_magic": []}}
    result = validate_config(raw)
    errors = [e for e in result.errors if e.path == "hooks.on_magic"]
    assert errors
    assert "pre_tool" in errors[0].message
    assert "post_tool" in errors[0].message


# ---------------------------------------------------------------------------
# Config validation — mix of valid and invalid keys
# ---------------------------------------------------------------------------


def test_valid_and_invalid_keys_together() -> None:
    raw: dict = {
        "hooks": {
            "pre_tool": [],
            "session_start": [],
            "on_magic": [],
        }
    }
    result = validate_config(raw)
    paths_with_errors = {e.path for e in result.errors if e.severity == "error"}
    assert "hooks.session_start" in paths_with_errors
    assert "hooks.on_magic" in paths_with_errors
    assert "hooks.pre_tool" not in paths_with_errors
