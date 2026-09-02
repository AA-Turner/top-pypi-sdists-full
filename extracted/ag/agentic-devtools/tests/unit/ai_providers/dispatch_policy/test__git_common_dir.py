from pathlib import Path
from types import SimpleNamespace

import pytest

from agentic_devtools.ai_providers.dispatch_policy import DispatchStateError, _git_common_dir


def test_git_common_dir_raises_on_transient_oserror(monkeypatch) -> None:
    import agentic_devtools.ai_providers.dispatch_policy as policy_module

    def _raise(*_args, **_kwargs):
        raise OSError("Resource temporarily unavailable")

    monkeypatch.setattr(policy_module.subprocess, "run", _raise)
    with pytest.raises(DispatchStateError, match="git rev-parse --git-common-dir failed with OS error"):
        _git_common_dir()


def test_git_common_dir_returns_none_when_git_not_installed(monkeypatch) -> None:
    import agentic_devtools.ai_providers.dispatch_policy as policy_module

    def _raise(*_args, **_kwargs):
        raise FileNotFoundError("git: No such file or directory")

    monkeypatch.setattr(policy_module.subprocess, "run", _raise)
    assert _git_common_dir() is None


def test_git_common_dir_returns_none_on_not_a_git_repository(monkeypatch) -> None:
    import agentic_devtools.ai_providers.dispatch_policy as policy_module

    monkeypatch.setattr(
        policy_module.subprocess,
        "run",
        lambda *_args, **_kwargs: SimpleNamespace(
            returncode=128,
            stdout="",
            stderr="fatal: not a git repository (or any of the parent directories): .git",
        ),
    )
    assert _git_common_dir() is None


def test_git_common_dir_raises_on_transient_nonzero_exit(monkeypatch) -> None:
    import agentic_devtools.ai_providers.dispatch_policy as policy_module

    monkeypatch.setattr(
        policy_module.subprocess,
        "run",
        lambda *_args, **_kwargs: SimpleNamespace(returncode=1, stdout="", stderr="I/O error"),
    )
    with pytest.raises(DispatchStateError, match="git rev-parse --git-common-dir failed"):
        _git_common_dir()


def test_git_common_dir_returns_none_on_zero_exit_with_empty_stdout(monkeypatch) -> None:
    import agentic_devtools.ai_providers.dispatch_policy as policy_module

    monkeypatch.setattr(
        policy_module.subprocess,
        "run",
        lambda *_args, **_kwargs: SimpleNamespace(returncode=0, stdout=""),
    )
    assert _git_common_dir() is None


def test_git_common_dir_returns_absolute_path(monkeypatch, tmp_path: Path) -> None:
    import agentic_devtools.ai_providers.dispatch_policy as policy_module

    absolute = tmp_path / "repo" / ".git"
    monkeypatch.setattr(
        policy_module.subprocess,
        "run",
        lambda *_args, **_kwargs: SimpleNamespace(returncode=0, stdout=str(absolute)),
    )
    assert _git_common_dir() == absolute


def test_git_common_dir_resolves_relative_path_against_current_working_directory(monkeypatch, tmp_path: Path) -> None:
    import agentic_devtools.ai_providers.dispatch_policy as policy_module

    nested = tmp_path / "repo" / "nested" / "module"
    nested.mkdir(parents=True)
    monkeypatch.setattr(
        policy_module.subprocess,
        "run",
        lambda *_args, **_kwargs: SimpleNamespace(returncode=0, stdout="../../.git"),
    )
    monkeypatch.chdir(nested)
    assert _git_common_dir() == (tmp_path / "repo" / ".git").resolve()


def test_git_common_dir_resolves_simple_relative_path(monkeypatch, tmp_path: Path) -> None:
    import agentic_devtools.ai_providers.dispatch_policy as policy_module

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        policy_module.subprocess,
        "run",
        lambda *_args, **_kwargs: SimpleNamespace(returncode=0, stdout=".git"),
    )
    assert _git_common_dir() == (tmp_path / ".git").resolve()
