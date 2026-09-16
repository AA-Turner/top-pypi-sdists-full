import agentic_devtools.cli.workflows.create_epic.registry as registry


def test_shared_dir_uses_common_directory(monkeypatch, tmp_path):
    monkeypatch.setattr(registry, "_git_common_dir", lambda: tmp_path / ".git")
    assert registry._shared_dir() == tmp_path / ".agdt" / "create-epic"
