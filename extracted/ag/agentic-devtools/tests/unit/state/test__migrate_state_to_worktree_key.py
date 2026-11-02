"""Tests for agentic_devtools.state._migrate_state_to_worktree_key."""

import json
from unittest.mock import patch

import pytest

from agentic_devtools import state


def _write_identity(agdt_dir) -> None:
    agdt_dir.mkdir(parents=True, exist_ok=True)
    (agdt_dir / "identity.json").write_text(
        json.dumps({"identity": "ama", "email": "ama@example.com"}),
        encoding="utf-8",
    )


def test_migrate_state_to_worktree_key_merges_into_destination(tmp_path, monkeypatch) -> None:
    """Move committed state to the new scope while preserving destination values."""
    monkeypatch.delenv("AGENTIC_DEVTOOLS_STATE_DIR", raising=False)
    agdt_dir = tmp_path / ".agdt"
    workflows_dir = agdt_dir / "workflows"
    old_dir = workflows_dir / "ama" / "OLD"
    new_dir = workflows_dir / "ama" / "NEW"
    old_dir.mkdir(parents=True)
    new_dir.mkdir(parents=True)
    _write_identity(agdt_dir)
    source_state = {"source": "kept", "nested": {"source": "kept", "conflict": "source"}}
    destination_state = {"destination": "kept", "nested": {"destination": "kept", "conflict": "destination"}}
    (new_dir / "state.json").write_text(json.dumps(destination_state), encoding="utf-8")

    with patch.object(state, "read_and_validate_pin_file", return_value=None):
        state._migrate_state_to_worktree_key(old_dir, "NEW", source_state)

    migrated = json.loads((new_dir / "state.json").read_text(encoding="utf-8"))
    assert migrated == {
        "source": "kept",
        "destination": "kept",
        "nested": {"source": "kept", "destination": "kept", "conflict": "destination"},
    }


def test_migrate_state_to_worktree_key_recursively_merges_nested_mappings(tmp_path, monkeypatch) -> None:
    """Destination conflicts win while source-only workflow context fields are retained."""
    monkeypatch.delenv("AGENTIC_DEVTOOLS_STATE_DIR", raising=False)
    agdt_dir = tmp_path / ".agdt"
    old_dir = agdt_dir / "workflows" / "ama" / "OLD"
    new_dir = agdt_dir / "workflows" / "ama" / "NEW"
    old_dir.mkdir(parents=True)
    new_dir.mkdir(parents=True)
    _write_identity(agdt_dir)
    source_state = {
        "workflow": {
            "context": {
                "source_only": "preserved",
                "conflict": "source",
                "nested": {"source_only": "preserved", "conflict": "source"},
            }
        }
    }
    destination_state = {
        "workflow": {
            "context": {
                "destination_only": "preserved",
                "conflict": "destination",
                "nested": {"destination_only": "preserved", "conflict": "destination"},
            }
        }
    }
    (new_dir / "state.json").write_text(json.dumps(destination_state), encoding="utf-8")

    with patch.object(state, "read_and_validate_pin_file", return_value=None):
        state._migrate_state_to_worktree_key(old_dir, "NEW", source_state)

    migrated = json.loads((new_dir / "state.json").read_text(encoding="utf-8"))
    assert migrated == {
        "workflow": {
            "context": {
                "source_only": "preserved",
                "destination_only": "preserved",
                "conflict": "destination",
                "nested": {
                    "source_only": "preserved",
                    "destination_only": "preserved",
                    "conflict": "destination",
                },
            }
        }
    }


def test_migrate_state_to_worktree_key_keeps_cleared_context_keys_removed(tmp_path, monkeypatch) -> None:
    """Counterparts cleared in the source cannot reappear from destination state."""
    monkeypatch.delenv("AGENTIC_DEVTOOLS_STATE_DIR", raising=False)
    agdt_dir = tmp_path / ".agdt"
    old_dir = agdt_dir / "workflows" / "ama" / "OLD"
    new_dir = agdt_dir / "workflows" / "ama" / "PR42"
    old_dir.mkdir(parents=True)
    new_dir.mkdir(parents=True)
    _write_identity(agdt_dir)
    (new_dir / "state.json").write_text(
        json.dumps({"issue_key": "stale", "pull_request_id": 1, "jira": {"issue_key": "stale", "summary": "keep"}}),
        encoding="utf-8",
    )

    with patch.object(state, "read_and_validate_pin_file", return_value=None):
        state._migrate_state_to_worktree_key(
            old_dir,
            "PR42",
            {"pull_request_id": 42, "jira": {"summary": "source"}},
            clear_destination_keys=("issue_key", "jira.issue_key"),
            override_destination_keys=("pull_request_id",),
        )

    migrated = json.loads((agdt_dir / "workflows" / "ama" / "PR42" / "state.json").read_text(encoding="utf-8"))
    assert migrated == {"pull_request_id": 42, "jira": {"summary": "keep"}}


def test_migrate_state_to_worktree_key_overrides_updated_nested_context(tmp_path, monkeypatch) -> None:
    """The updated nested issue key overrides a stale destination value."""
    monkeypatch.delenv("AGENTIC_DEVTOOLS_STATE_DIR", raising=False)
    agdt_dir = tmp_path / ".agdt"
    old_dir = agdt_dir / "workflows" / "ama" / "OLD"
    new_dir = agdt_dir / "workflows" / "ama" / "PROJECT-2"
    old_dir.mkdir(parents=True)
    new_dir.mkdir(parents=True)
    _write_identity(agdt_dir)
    (new_dir / "state.json").write_text(
        json.dumps({"pull_request_id": 99, "jira": {"issue_key": "PROJECT-1", "summary": "keep"}}),
        encoding="utf-8",
    )

    with patch.object(state, "read_and_validate_pin_file", return_value=None):
        state._migrate_state_to_worktree_key(
            old_dir,
            "PROJECT-2",
            {"jira": {"issue_key": "PROJECT-2"}},
            clear_destination_keys=("pull_request_id",),
            override_destination_keys=("jira.issue_key",),
        )

    migrated = json.loads((new_dir / "state.json").read_text(encoding="utf-8"))
    assert migrated == {"jira": {"issue_key": "PROJECT-2", "summary": "keep"}}


def test_migrate_state_to_worktree_key_replaces_scalar_parent_for_nested_override(tmp_path, monkeypatch) -> None:
    """A nested override replaces a scalar destination parent when its source value exists."""
    monkeypatch.delenv("AGENTIC_DEVTOOLS_STATE_DIR", raising=False)
    agdt_dir = tmp_path / ".agdt"
    old_dir = agdt_dir / "workflows" / "ama" / "OLD"
    new_dir = agdt_dir / "workflows" / "ama" / "PROJECT-2"
    old_dir.mkdir(parents=True)
    new_dir.mkdir(parents=True)
    _write_identity(agdt_dir)
    (new_dir / "state.json").write_text(json.dumps({"jira": "stale"}), encoding="utf-8")

    with patch.object(state, "read_and_validate_pin_file", return_value=None):
        state._migrate_state_to_worktree_key(
            old_dir,
            "PROJECT-2",
            {"jira": {"issue_key": "PROJECT-2", "summary": "source"}},
            override_destination_keys=("jira.issue_key",),
        )

    migrated = json.loads((new_dir / "state.json").read_text(encoding="utf-8"))
    assert migrated == {"jira": {"issue_key": "PROJECT-2", "summary": "source"}}


def test_nested_override_keeps_scalar_parent_when_source_lacks_override_path(tmp_path, monkeypatch) -> None:
    """A scalar destination parent wins if the source lacks the explicitly overridden path."""
    monkeypatch.delenv("AGENTIC_DEVTOOLS_STATE_DIR", raising=False)
    agdt_dir = tmp_path / ".agdt"
    old_dir = agdt_dir / "workflows" / "ama" / "OLD"
    new_dir = agdt_dir / "workflows" / "ama" / "PROJECT-2"
    old_dir.mkdir(parents=True)
    new_dir.mkdir(parents=True)
    _write_identity(agdt_dir)
    (new_dir / "state.json").write_text(json.dumps({"jira": "stale"}), encoding="utf-8")

    with patch.object(state, "read_and_validate_pin_file", return_value=None):
        state._migrate_state_to_worktree_key(
            old_dir,
            "PROJECT-2",
            {"jira": {"summary": "source"}},
            override_destination_keys=("jira.issue_key",),
        )

    migrated = json.loads((new_dir / "state.json").read_text(encoding="utf-8"))
    assert migrated == {"jira": "stale"}


def test_migrate_state_to_worktree_key_skips_pinned_state_dir(tmp_path, monkeypatch) -> None:
    """Pinned state directories are unaffected by worktree-key changes."""
    monkeypatch.delenv("AGENTIC_DEVTOOLS_STATE_DIR", raising=False)
    old_dir = tmp_path / ".agdt" / "workflows" / "ama" / "OLD"
    old_dir.mkdir(parents=True)

    with patch.object(state, "read_and_validate_pin_file", return_value=tmp_path / "pinned"):
        state._migrate_state_to_worktree_key(old_dir, "NEW", {"key": "value"})

    assert not (old_dir.parent / "NEW" / "state.json").exists()


def test_migrate_state_to_worktree_key_skips_environment_state_dir(tmp_path, monkeypatch) -> None:
    """An explicit state directory does not follow bootstrap worktree changes."""
    old_dir = tmp_path / ".agdt" / "workflows" / "ama" / "OLD"
    old_dir.mkdir(parents=True)
    monkeypatch.setenv("AGENTIC_DEVTOOLS_STATE_DIR", str(old_dir))

    state._migrate_state_to_worktree_key(old_dir, "NEW", {"key": "value"})

    assert not (old_dir.parent / "NEW" / "state.json").exists()


@pytest.mark.parametrize(
    "state_dir",
    [
        pytest.param("plain", id="not-workflows"),
        pytest.param("not-agdt/workflows/ama/OLD", id="invalid-agdt-layout"),
    ],
)
def test_migrate_state_to_worktree_key_skips_nonstandard_state_paths(tmp_path, monkeypatch, state_dir: str) -> None:
    """State paths outside the standard workflow layout are not migrated."""
    monkeypatch.delenv("AGENTIC_DEVTOOLS_STATE_DIR", raising=False)
    path = tmp_path / state_dir
    path.mkdir(parents=True)

    state._migrate_state_to_worktree_key(path, "NEW", {"key": "value"})

    assert not (tmp_path / ".agdt" / "workflows" / "ama" / "NEW" / "state.json").exists()


def test_migrate_unscoped_state_uses_bootstrap_identity(tmp_path, monkeypatch) -> None:
    """An unscoped source migrates using the legacy identity in bootstrap."""
    monkeypatch.delenv("AGENTIC_DEVTOOLS_STATE_DIR", raising=False)
    agdt_dir = tmp_path / ".agdt"
    old_dir = agdt_dir / "workflows" / "_unscoped"
    old_dir.mkdir(parents=True)
    (agdt_dir / "runtime-bootstrap.json").write_text(
        json.dumps({"identity": "ama"}),
        encoding="utf-8",
    )

    with patch.object(state, "read_and_validate_pin_file", return_value=None):
        state._migrate_state_to_worktree_key(old_dir, "NEW", {"key": "value"})

    migrated = json.loads((agdt_dir / "workflows" / "ama" / "NEW" / "state.json").read_text(encoding="utf-8"))
    assert migrated == {"key": "value"}


def test_migrate_unscoped_state_uses_identity_cache(tmp_path, monkeypatch) -> None:
    """An unscoped source migrates using the cached identity when available."""
    monkeypatch.delenv("AGENTIC_DEVTOOLS_STATE_DIR", raising=False)
    agdt_dir = tmp_path / ".agdt"
    old_dir = agdt_dir / "workflows" / "_unscoped"
    old_dir.mkdir(parents=True)
    _write_identity(agdt_dir)

    with patch.object(state, "read_and_validate_pin_file", return_value=None):
        state._migrate_state_to_worktree_key(old_dir, "NEW", {"key": "value"})

    migrated = json.loads((agdt_dir / "workflows" / "ama" / "NEW" / "state.json").read_text(encoding="utf-8"))
    assert migrated == {"key": "value"}


@pytest.mark.parametrize(
    "bootstrap_content",
    ["{malformed", "[]", '{"identity": 7}'],
)
def test_migrate_unscoped_state_skips_invalid_identity(tmp_path, monkeypatch, bootstrap_content: str) -> None:
    """Missing or invalid identity data leaves state in its unscoped directory."""
    monkeypatch.delenv("AGENTIC_DEVTOOLS_STATE_DIR", raising=False)
    agdt_dir = tmp_path / ".agdt"
    old_dir = agdt_dir / "workflows" / "_unscoped"
    old_dir.mkdir(parents=True)
    (agdt_dir / "runtime-bootstrap.json").write_text(bootstrap_content, encoding="utf-8")

    with patch.object(state, "read_and_validate_pin_file", return_value=None):
        state._migrate_state_to_worktree_key(old_dir, "NEW", {"key": "value"})

    assert not (agdt_dir / "workflows" / "ama" / "NEW" / "state.json").exists()


def test_migrate_state_to_worktree_key_uses_unscoped_path_for_unsafe_key(tmp_path, monkeypatch) -> None:
    """Unsafe worktree keys never become directory names."""
    monkeypatch.delenv("AGENTIC_DEVTOOLS_STATE_DIR", raising=False)
    agdt_dir = tmp_path / ".agdt"
    old_dir = agdt_dir / "workflows" / "ama" / "OLD"
    old_dir.mkdir(parents=True)
    _write_identity(agdt_dir)

    with patch.object(state, "read_and_validate_pin_file", return_value=None):
        state._migrate_state_to_worktree_key(old_dir, "../escape", {"key": "value"})

    assert json.loads((agdt_dir / "workflows" / "_unscoped" / "state.json").read_text(encoding="utf-8")) == {
        "key": "value"
    }
    assert not (tmp_path / "escape" / "state.json").exists()


def test_migrate_state_to_worktree_key_skips_when_destination_is_current_dir(tmp_path, monkeypatch) -> None:
    """An already-active worktree scope needs no migration."""
    monkeypatch.delenv("AGENTIC_DEVTOOLS_STATE_DIR", raising=False)
    agdt_dir = tmp_path / ".agdt"
    current_dir = agdt_dir / "workflows" / "ama" / "CURRENT"
    current_dir.mkdir(parents=True)
    _write_identity(agdt_dir)

    with patch.object(state, "read_and_validate_pin_file", return_value=None):
        state._migrate_state_to_worktree_key(current_dir, "CURRENT", {"key": "value"})

    assert not (current_dir / "state.json").exists()


@pytest.mark.parametrize("destination_content", ["{malformed", "[]"])
def test_migrate_state_to_worktree_key_recovers_invalid_destination_json(
    tmp_path, monkeypatch, destination_content: str
) -> None:
    """Invalid destination JSON is replaced by the committed source state."""
    monkeypatch.delenv("AGENTIC_DEVTOOLS_STATE_DIR", raising=False)
    agdt_dir = tmp_path / ".agdt"
    old_dir = agdt_dir / "workflows" / "ama" / "OLD"
    new_dir = agdt_dir / "workflows" / "ama" / "NEW"
    old_dir.mkdir(parents=True)
    new_dir.mkdir(parents=True)
    _write_identity(agdt_dir)
    (new_dir / "state.json").write_text(destination_content, encoding="utf-8")

    with patch.object(state, "read_and_validate_pin_file", return_value=None):
        state._migrate_state_to_worktree_key(old_dir, "NEW", {"key": "value", "nested": {"source": "kept"}})

    assert json.loads((new_dir / "state.json").read_text(encoding="utf-8")) == {
        "key": "value",
        "nested": {"source": "kept"},
    }


def test_migrate_state_to_worktree_key_preserves_non_mapping_destination_values(tmp_path, monkeypatch) -> None:
    """A destination scalar value takes precedence over a source mapping."""
    monkeypatch.delenv("AGENTIC_DEVTOOLS_STATE_DIR", raising=False)
    agdt_dir = tmp_path / ".agdt"
    old_dir = agdt_dir / "workflows" / "ama" / "OLD"
    new_dir = agdt_dir / "workflows" / "ama" / "NEW"
    old_dir.mkdir(parents=True)
    new_dir.mkdir(parents=True)
    _write_identity(agdt_dir)
    (new_dir / "state.json").write_text(json.dumps({"nested": "existing"}), encoding="utf-8")

    with patch.object(state, "read_and_validate_pin_file", return_value=None):
        state._migrate_state_to_worktree_key(
            old_dir,
            "NEW",
            {"nested": {"source": "ignored"}},
            override_destination_keys=("other.field",),
        )

    assert json.loads((new_dir / "state.json").read_text(encoding="utf-8")) == {"nested": "existing"}


def test_migrate_state_to_worktree_key_skips_nested_clear_under_scalar(tmp_path, monkeypatch) -> None:
    """A nested clear leaves an existing non-mapping parent untouched."""
    monkeypatch.delenv("AGENTIC_DEVTOOLS_STATE_DIR", raising=False)
    agdt_dir = tmp_path / ".agdt"
    old_dir = agdt_dir / "workflows" / "ama" / "OLD"
    new_dir = agdt_dir / "workflows" / "ama" / "NEW"
    old_dir.mkdir(parents=True)
    new_dir.mkdir(parents=True)
    _write_identity(agdt_dir)
    (new_dir / "state.json").write_text(json.dumps({"jira": "not-a-mapping"}), encoding="utf-8")

    with patch.object(state, "read_and_validate_pin_file", return_value=None):
        state._migrate_state_to_worktree_key(
            old_dir,
            "NEW",
            {"new": "value"},
            clear_destination_keys=("jira.issue_key",),
        )

    assert json.loads((new_dir / "state.json").read_text(encoding="utf-8")) == {
        "jira": "not-a-mapping",
        "new": "value",
    }
