import pytest

from agentic_devtools.cli.workflows.create_epic.registry import acquire_tree_lock


def test_acquire_tree_lock_is_released(tmp_path):
    tree_id = "12345678-1234-5678-1234-567812345678"
    with acquire_tree_lock(tree_id, common_dir=tmp_path / ".git"):
        with pytest.raises(RuntimeError, match="already held"):
            with acquire_tree_lock(tree_id, common_dir=tmp_path / ".git"):
                pass
    with acquire_tree_lock(tree_id, common_dir=tmp_path / ".git"):
        pass
