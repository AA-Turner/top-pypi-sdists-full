"""Unit tests for flowtask.parsers.syntax.registry.ComponentSchemaRegistry."""
import logging
from pathlib import Path

import orjson
import pytest

from flowtask.parsers.syntax.registry import ComponentSchemaRegistry


@pytest.fixture
def fake_docs_dir(tmp_path: Path) -> Path:
    """Build a minimal docs/ tree for the registry to read."""
    components = tmp_path / "components"
    components.mkdir()
    (tmp_path / "index.json").write_bytes(orjson.dumps({
        "components": {
            "AddDataset": {
                "schema": "components/AddDataset.schema.json",
                "doc": "components/AddDataset.doc.json",
                "category": "Transformations",
                "description": "test",
            }
        }
    }))
    (components / "AddDataset.schema.json").write_bytes(orjson.dumps({
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "title": "AddDataset",
        "properties": {"dataset": {"type": "string"}},
        "required": ["dataset"],
    }))
    return tmp_path


def test_known_returns_index_keys(fake_docs_dir):
    """known() returns the set of component names from index.json."""
    reg = ComponentSchemaRegistry(docs_dir=fake_docs_dir)
    assert reg.known() == {"AddDataset"}


def test_has_known_and_unknown(fake_docs_dir):
    """has() returns True for known components, False for unknown."""
    reg = ComponentSchemaRegistry(docs_dir=fake_docs_dir)
    assert reg.has("AddDataset") is True
    assert reg.has("DoesNotExist") is False


def test_get_loads_and_caches(fake_docs_dir):
    """get() loads the schema and caches it (second call returns same object)."""
    reg = ComponentSchemaRegistry(docs_dir=fake_docs_dir)
    s1 = reg.get("AddDataset")
    s2 = reg.get("AddDataset")
    assert s1 is s2  # cached — same object
    assert s1["title"] == "AddDataset"
    assert s1["required"] == ["dataset"]


def test_get_unknown_returns_none(fake_docs_dir):
    """get() returns None for unknown components without raising."""
    reg = ComponentSchemaRegistry(docs_dir=fake_docs_dir)
    assert reg.get("DoesNotExist") is None


def test_default_docs_dir_uses_base_dir():
    """Constructor without args sets docs_dir = BASE_DIR / 'docs'."""
    from navconfig import BASE_DIR
    reg = ComponentSchemaRegistry()
    assert reg.docs_dir == BASE_DIR / "docs"


def test_missing_index_does_not_raise(tmp_path, caplog):
    """Missing index.json yields empty known() and None from get(), with a WARNING log."""
    with caplog.at_level(logging.WARNING, logger="FlowTask.Syntax.Registry"):
        reg = ComponentSchemaRegistry(docs_dir=tmp_path)
        assert reg.known() == set()
        assert reg.get("Anything") is None
    assert any("not found" in r.message.lower() for r in caplog.records)


def test_missing_schema_file_returns_none(tmp_path, caplog):
    """Index references a schema file that does not exist on disk."""
    (tmp_path / "components").mkdir()
    (tmp_path / "index.json").write_bytes(orjson.dumps({
        "components": {
            "GhostComponent": {
                "schema": "components/GhostComponent.schema.json",
                "doc": "components/GhostComponent.doc.json",
            }
        }
    }))
    with caplog.at_level(logging.WARNING, logger="FlowTask.Syntax.Registry"):
        reg = ComponentSchemaRegistry(docs_dir=tmp_path)
        assert reg.has("GhostComponent") is True
        assert reg.get("GhostComponent") is None
    assert any("missing on disk" in r.message.lower() for r in caplog.records)
