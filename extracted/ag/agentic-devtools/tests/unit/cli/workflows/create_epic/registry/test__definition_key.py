import agentic_devtools.cli.workflows.create_epic.registry as registry


def test_definition_key_falls_back_to_absolute_path(monkeypatch, tmp_path):
    result = type("Result", (), {"returncode": 0, "stdout": str(tmp_path / "other") + "\n"})()
    monkeypatch.setattr(registry.subprocess, "run", lambda *_args, **_kwargs: result)
    path = tmp_path / "tree.json"
    assert registry._definition_key(path) == path.as_posix()
