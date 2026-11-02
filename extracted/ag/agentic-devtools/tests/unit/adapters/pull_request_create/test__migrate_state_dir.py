"""Tests for ``_migrate_state_dir`` (stranded-state migration on worktree-key switch)."""

import json

from agentic_devtools.adapters.pull_request_create import _migrate_state_dir


def _write_state(directory, data=None) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "state.json").write_text(json.dumps(data or {}), encoding="utf-8")


def test_copies_stranded_keys_into_new_directory(tmp_path) -> None:
    old_dir = tmp_path / "old"
    new_dir = tmp_path / "new"
    _write_state(old_dir, {"pull_request_id": 42, "github": {"pull_request_number": 42}})
    _write_state(new_dir, {})

    _migrate_state_dir(old_dir, new_dir)

    new_data = json.loads((new_dir / "state.json").read_text(encoding="utf-8"))
    assert new_data == {"pull_request_id": 42, "github": {"pull_request_number": 42}}


def test_existing_keys_in_new_directory_win_on_conflict(tmp_path) -> None:
    old_dir = tmp_path / "old"
    new_dir = tmp_path / "new"
    _write_state(old_dir, {"pull_request_id": 42})
    _write_state(new_dir, {"pull_request_id": 99})

    _migrate_state_dir(old_dir, new_dir)

    new_data = json.loads((new_dir / "state.json").read_text(encoding="utf-8"))
    assert new_data == {"pull_request_id": 99}


def test_no_op_when_old_directory_has_no_state(tmp_path) -> None:
    old_dir = tmp_path / "old"
    new_dir = tmp_path / "new"
    _write_state(old_dir, {})

    _migrate_state_dir(old_dir, new_dir)

    assert not (new_dir / "state.json").exists()


def test_merges_nested_dict_fields_instead_of_dropping_them_on_conflict(tmp_path) -> None:
    """A destination `github` mapping must not shadow nested stranded fields it lacks."""
    old_dir = tmp_path / "old"
    new_dir = tmp_path / "new"
    _write_state(old_dir, {"github": {"pull_request_number": 42}})
    _write_state(new_dir, {"github": {"pull_request_url": "https://example.com/pr/1"}})

    _migrate_state_dir(old_dir, new_dir)

    new_data = json.loads((new_dir / "state.json").read_text(encoding="utf-8"))
    assert new_data == {
        "github": {
            "pull_request_url": "https://example.com/pr/1",
            "pull_request_number": 42,
        }
    }
