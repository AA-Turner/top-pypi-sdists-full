"""Tests for ``_read_modify_write_state_at`` (directory-pinned state transaction)."""

import json
from unittest.mock import patch

import pytest

from agentic_devtools.adapters.pull_request_create import _read_modify_write_state_at


def _write_state(tmp_path, data=None) -> None:
    (tmp_path / "state.json").write_text(json.dumps(data or {}), encoding="utf-8")


def test_mutates_and_saves(tmp_path) -> None:
    _write_state(tmp_path, {"existing": "value"})
    with _read_modify_write_state_at(tmp_path) as state:
        state["new_key"] = 42

    data = json.loads((tmp_path / "state.json").read_text(encoding="utf-8"))
    assert data == {"existing": "value", "new_key": 42}


def test_skips_save_on_exception(tmp_path) -> None:
    _write_state(tmp_path, {"safe": True})

    def _mutate_and_fail() -> None:
        with _read_modify_write_state_at(tmp_path) as state:
            state["bad"] = True
            raise RuntimeError("boom")

    pytest.raises(RuntimeError, _mutate_and_fail)

    data = json.loads((tmp_path / "state.json").read_text(encoding="utf-8"))
    assert data == {"safe": True}


def test_no_write_when_state_unchanged(tmp_path) -> None:
    """No content is written and mark_dirty is not called when nothing changed."""
    _write_state(tmp_path, {"existing": "value"})
    state_file = tmp_path / "state.json"
    before = state_file.stat().st_mtime_ns
    with patch("agentic_devtools.cli.git.agdt_branch.mark_dirty") as mock_mark_dirty:
        with _read_modify_write_state_at(tmp_path) as state:
            assert state == {"existing": "value"}

    mock_mark_dirty.assert_not_called()
    assert state_file.stat().st_mtime_ns == before


def test_marks_dirty_after_successful_save(tmp_path) -> None:
    _write_state(tmp_path, {})
    with patch("agentic_devtools.cli.git.agdt_branch.mark_dirty") as mock_mark_dirty:
        with _read_modify_write_state_at(tmp_path) as state:
            state["new_key"] = "value"

    mock_mark_dirty.assert_called_once_with()


def test_missing_agdt_branch_module_is_tolerated(tmp_path) -> None:
    """A minimal install without ``agdt_branch`` must not fail the save."""
    _write_state(tmp_path, {})
    with patch.dict("sys.modules", {"agentic_devtools.cli.git.agdt_branch": None}):
        with _read_modify_write_state_at(tmp_path) as state:
            state["new_key"] = "value"

    data = json.loads((tmp_path / "state.json").read_text(encoding="utf-8"))
    assert data == {"new_key": "value"}


def test_corrupted_json_treated_as_empty(tmp_path) -> None:
    (tmp_path / "state.json").write_text("{not valid json", encoding="utf-8")
    with _read_modify_write_state_at(tmp_path) as state:
        assert state == {}
        state["key"] = "value"

    data = json.loads((tmp_path / "state.json").read_text(encoding="utf-8"))
    assert data == {"key": "value"}
