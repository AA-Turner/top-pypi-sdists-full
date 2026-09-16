import json

import pytest

import agentic_devtools.cli.workflows.create_epic.registry as registry
import agentic_devtools.epic_tree.loader as loader
from agentic_devtools.epic_tree.loader import migrate_schema_v1_to_v2


def test_migrate_schema_v1_to_v2_persists_uuid(tmp_path):
    path = tmp_path / "tree.json"
    path.write_text(
        json.dumps({"schemaVersion": "1.0", "epic": {"ref": "e", "title": "E", "body": "", "features": []}})
    )
    tree = migrate_schema_v1_to_v2(path)
    document = json.loads(path.read_text())
    assert tree.schemaVersion == "2.0"
    assert document["treeId"] == str(tree.treeId)


def test_migrate_schema_v1_to_v2_dry_run_does_not_write(tmp_path):
    original = {"schemaVersion": "1.0", "epic": {"ref": "e", "title": "E", "body": "", "features": []}}
    path = tmp_path / "tree.json"
    path.write_text(json.dumps(original))
    migrate_schema_v1_to_v2(path, dry_run=True)
    assert json.loads(path.read_text()) == original


@pytest.mark.parametrize(
    "document",
    [
        [],
        {"schemaVersion": "2.0"},
        {"schemaVersion": "3.0", "epic": {}},
        {"schemaVersion": "1.0", "epic": {"title": "missing ref", "body": "", "features": []}},
    ],
)
def test_migrate_schema_v1_to_v2_rejects_invalid_documents(tmp_path, document):
    path = tmp_path / "tree.json"
    path.write_text(json.dumps(document))
    with pytest.raises(ValueError):
        migrate_schema_v1_to_v2(path)


def test_migrate_schema_v1_to_v2_keeps_existing_v2(tmp_path, monkeypatch):
    path = tmp_path / "tree.json"
    document = {
        "schemaVersion": "2.0",
        "treeId": "12345678-1234-5678-1234-567812345678",
        "epic": {"ref": "e", "title": "E", "body": "", "features": []},
    }
    path.write_text(json.dumps(document))
    monkeypatch.setattr(
        registry,
        "reserve_binding",
        lambda *_args, **_kwargs: {"treeId": document["treeId"]},
    )
    monkeypatch.setattr(registry, "promote_binding", lambda *_args, **_kwargs: {})
    tree = migrate_schema_v1_to_v2(path)
    assert str(tree.treeId) == document["treeId"]


def test_migrate_schema_v1_to_v2_promotes_existing_v2_binding(tmp_path, monkeypatch):
    path = tmp_path / "tree.json"
    path.write_text(
        json.dumps(
            {
                "schemaVersion": "2.0",
                "treeId": "12345678-1234-5678-1234-567812345678",
                "epic": {"ref": "e", "title": "E", "body": "", "features": []},
            }
        )
    )
    calls: list[str] = []
    monkeypatch.setattr(
        registry,
        "reserve_binding",
        lambda *_args, **_kwargs: calls.append("reserve") or {"treeId": "12345678-1234-5678-1234-567812345678"},
    )
    monkeypatch.setattr(registry, "promote_binding", lambda *_args, **_kwargs: calls.append("promote") or {})

    migrate_schema_v1_to_v2(path)

    assert calls == ["reserve", "promote"]


def test_migrate_schema_v1_to_v2_cleans_up_after_replace_failure(tmp_path, monkeypatch):
    path = tmp_path / "tree.json"
    path.write_text(
        json.dumps({"schemaVersion": "1.0", "epic": {"ref": "e", "title": "E", "body": "", "features": []}})
    )
    monkeypatch.setattr(
        registry, "reserve_binding", lambda *_args, **_kwargs: {"treeId": "12345678-1234-5678-1234-567812345678"}
    )
    monkeypatch.setattr(registry, "promote_binding", lambda *_args, **_kwargs: {})
    monkeypatch.setattr(loader.os, "replace", lambda *_args: (_ for _ in ()).throw(OSError("replace failed")))
    with pytest.raises(OSError, match="replace failed"):
        migrate_schema_v1_to_v2(path)


def test_migrate_schema_v1_to_v2_preserves_replace_error_when_cleanup_fails(tmp_path, monkeypatch):
    path = tmp_path / "tree.json"
    path.write_text(
        json.dumps({"schemaVersion": "1.0", "epic": {"ref": "e", "title": "E", "body": "", "features": []}})
    )
    monkeypatch.setattr(
        registry, "reserve_binding", lambda *_args, **_kwargs: {"treeId": "12345678-1234-5678-1234-567812345678"}
    )
    monkeypatch.setattr(registry, "promote_binding", lambda *_args, **_kwargs: {})
    monkeypatch.setattr(loader.os, "replace", lambda *_args: (_ for _ in ()).throw(OSError("replace failed")))
    monkeypatch.setattr(loader.os, "unlink", lambda *_args: (_ for _ in ()).throw(OSError("cleanup failed")))
    with pytest.raises(OSError, match="replace failed"):
        migrate_schema_v1_to_v2(path)
