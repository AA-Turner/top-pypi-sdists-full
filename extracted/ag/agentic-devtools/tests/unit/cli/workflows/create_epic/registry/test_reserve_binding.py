import json

import pytest

import agentic_devtools.cli.workflows.create_epic.registry as registry_module
from agentic_devtools.cli.workflows.create_epic.registry import reserve_binding


def test_reserve_binding_is_reused(tmp_path):
    definition = tmp_path / "tree.json"
    registry = tmp_path / "registry.json"
    first = reserve_binding(definition, registry_path=registry)
    second = reserve_binding(definition, registry_path=registry)
    assert first == second
    assert first["status"] == "pending"


def test_reserve_binding_rejects_conflicting_tree(tmp_path):
    definition = tmp_path / "tree.json"
    registry = tmp_path / "registry.json"
    reserve_binding(definition, tree_id="12345678-1234-5678-1234-567812345678", registry_path=registry)
    with pytest.raises(ValueError):
        reserve_binding(definition, tree_id="87654321-4321-8765-4321-876543218765", registry_path=registry)


def test_reserve_binding_rejects_corrupt_registry(tmp_path):
    registry = tmp_path / "registry.json"
    registry.write_text(json.dumps({"schemaVersion": "bad", "bindings": {}}))
    with pytest.raises(ValueError):
        reserve_binding(tmp_path / "tree.json", registry_path=registry)


@pytest.mark.parametrize(
    "entry",
    [
        {"path": "other", "status": "pending", "treeId": "12345678-1234-5678-1234-567812345678"},
        {"path": "tree.json", "status": "bad", "treeId": "12345678-1234-5678-1234-567812345678"},
        {"path": "tree.json", "status": "pending", "treeId": "bad"},
    ],
)
def test_reserve_binding_rejects_corrupt_entries(tmp_path, entry):
    registry = tmp_path / "registry.json"
    registry.write_text(json.dumps({"schemaVersion": "1.0", "bindings": {"tree.json": entry}}))
    with pytest.raises(ValueError):
        reserve_binding(tmp_path / "tree.json", registry_path=registry)


def test_reserve_binding_rejects_duplicate_tree_id(tmp_path):
    registry = tmp_path / "registry.json"
    existing = {"path": "other", "status": "pending", "treeId": "12345678-1234-5678-1234-567812345678"}
    registry.write_text(json.dumps({"schemaVersion": "1.0", "bindings": {"other": existing}}))
    with pytest.raises(ValueError, match="already bound"):
        reserve_binding(
            tmp_path / "tree.json",
            tree_id=existing["treeId"],
            registry_path=registry,
        )


def test_reserve_binding_rejects_invalid_tree_id(tmp_path):
    with pytest.raises(ValueError, match="must be a UUID"):
        reserve_binding(tmp_path / "tree.json", tree_id="bad", registry_path=tmp_path / "registry.json")


def test_reserve_binding_uses_git_relative_path(tmp_path, monkeypatch):
    result = type("Result", (), {"returncode": 0, "stdout": str(tmp_path) + "\n"})()
    monkeypatch.setattr(registry_module.subprocess, "run", lambda *_args, **_kwargs: result)
    binding = reserve_binding(tmp_path / "nested" / "tree.json", registry_path=tmp_path / "registry.json")
    assert binding["path"] == "nested/tree.json"


def test_reserve_binding_rejects_duplicate_ids_in_registry(tmp_path):
    tree_id = "12345678-1234-5678-1234-567812345678"
    entry = {"path": "one", "status": "pending", "treeId": tree_id}
    registry = tmp_path / "registry.json"
    registry.write_text(
        json.dumps({"schemaVersion": "1.0", "bindings": {"one": entry, "two": {**entry, "path": "two"}}})
    )
    with pytest.raises(ValueError, match="Duplicate"):
        reserve_binding(tmp_path / "tree.json", registry_path=registry)


def test_reserve_binding_uses_absolute_path_when_git_root_is_unavailable(tmp_path, monkeypatch):
    result = type("Result", (), {"returncode": 1, "stdout": ""})()
    monkeypatch.setattr(registry_module.subprocess, "run", lambda *_args, **_kwargs: result)
    path = tmp_path / "tree.json"
    binding = reserve_binding(path, registry_path=tmp_path / "registry.json")
    assert binding["path"] == path.as_posix()
