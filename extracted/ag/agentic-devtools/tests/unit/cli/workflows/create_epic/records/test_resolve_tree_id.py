import pytest

from agentic_devtools.cli.workflows.create_epic.records import resolve_tree_id
from agentic_devtools.epic_tree.models import EpicTree


def test_resolve_tree_id_normalizes_uuid():
    assert resolve_tree_id("12345678-1234-5678-1234-567812345678".upper()) == "12345678-1234-5678-1234-567812345678"


def test_resolve_tree_id_rejects_missing_value():
    with pytest.raises(ValueError, match="does not contain"):
        resolve_tree_id({})


def test_resolve_tree_id_rejects_malformed_uuid():
    with pytest.raises(ValueError, match="Invalid"):
        resolve_tree_id("not-a-uuid")


def test_resolve_tree_id_reads_epic_tree_without_identity():
    tree = EpicTree.model_validate(
        {"schemaVersion": "1.0", "epic": {"ref": "e", "title": "E", "body": "", "features": []}}
    )
    with pytest.raises(ValueError, match="does not contain"):
        resolve_tree_id(tree)
