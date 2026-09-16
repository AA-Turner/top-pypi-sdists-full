import pytest

import agentic_devtools.cli.workflows.create_epic.registry as registry


def test_atomic_write_cleans_up_after_failure(tmp_path, monkeypatch):
    path = tmp_path / "registry.json"
    monkeypatch.setattr(registry.os, "replace", lambda *_args: (_ for _ in ()).throw(OSError("replace failed")))
    with pytest.raises(OSError, match="replace failed"):
        registry._atomic_write(path, {"schemaVersion": "1.0", "bindings": {}})
    assert not list(tmp_path.glob(".registry.json.*"))


def test_atomic_write_preserves_error_when_cleanup_fails(tmp_path, monkeypatch):
    path = tmp_path / "registry.json"
    monkeypatch.setattr(registry.os, "replace", lambda *_args: (_ for _ in ()).throw(OSError("replace failed")))
    monkeypatch.setattr(registry.os, "unlink", lambda *_args: (_ for _ in ()).throw(OSError("cleanup failed")))
    with pytest.raises(OSError, match="replace failed"):
        registry._atomic_write(path, {"schemaVersion": "1.0", "bindings": {}})
