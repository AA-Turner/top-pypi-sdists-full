import pytest

from agentic_devtools.cli.workflows.create_epic.registry import get_tree_lock_path


def test_get_tree_lock_path_normalizes_uuid(tmp_path):
    path = get_tree_lock_path("12345678-1234-5678-1234-567812345678", common_dir=tmp_path / ".git")
    assert path == tmp_path / ".agdt" / "epic-tree-locks" / "12345678-1234-5678-1234-567812345678.lock"


def test_get_tree_lock_path_rejects_invalid_uuid(tmp_path):
    with pytest.raises(ValueError):
        get_tree_lock_path("bad", common_dir=tmp_path / ".git")
