import pytest

from agentic_devtools.cli.workflows.create_epic.registry import promote_binding, reserve_binding


def test_promote_binding_confirms_reservation(tmp_path):
    definition = tmp_path / "tree.json"
    registry = tmp_path / "registry.json"
    reserved = reserve_binding(definition, registry_path=registry)
    promoted = promote_binding(definition, tree_id=reserved["treeId"], registry_path=registry)
    assert promoted["status"] == "confirmed"


def test_promote_binding_requires_reservation(tmp_path):
    with pytest.raises(ValueError, match="No binding"):
        promote_binding(tmp_path / "missing.json", registry_path=tmp_path / "registry.json")


def test_promote_binding_rejects_mismatched_tree_id(tmp_path):
    definition = tmp_path / "tree.json"
    registry = tmp_path / "registry.json"
    reserve_binding(definition, registry_path=registry)
    with pytest.raises(ValueError, match="does not match"):
        promote_binding(
            definition,
            tree_id="87654321-4321-8765-4321-876543218765",
            registry_path=registry,
        )
