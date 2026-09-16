import pytest

import agentic_devtools.cli.workflows.create_epic.registry as registry


def test_git_common_dir_rejects_failed_command(monkeypatch):
    result = type("Result", (), {"returncode": 1, "stdout": ""})()
    monkeypatch.setattr(registry.subprocess, "run", lambda *_args, **_kwargs: result)
    with pytest.raises(RuntimeError, match="common directory"):
        registry._git_common_dir()


def test_git_common_dir_resolves_relative_output(monkeypatch, tmp_path):
    result = type("Result", (), {"returncode": 0, "stdout": ".git\n"})()
    monkeypatch.setattr(registry.subprocess, "run", lambda *_args, **_kwargs: result)
    monkeypatch.chdir(tmp_path)
    assert registry._git_common_dir() == (tmp_path / ".git").resolve()
