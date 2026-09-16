import agentic_devtools.cli.workflows.create_epic.registry as registry


def test_registry_path_is_in_shared_directory(monkeypatch, tmp_path):
    monkeypatch.setattr(registry, "_shared_dir", lambda: tmp_path)
    assert registry._registry_path() == tmp_path / "epic-tree-bindings.json"
