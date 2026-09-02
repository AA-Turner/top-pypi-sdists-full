"""Tests for check_extras_resolution.main."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from tests.scripts.check_extras_resolution import checker


def test_main_returns_zero_when_no_extras_declared(tmp_path: Path, monkeypatch, capsys) -> None:
    """When no extras are declared there is nothing to resolve and main succeeds trivially."""
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text('[project]\nname = "example"\n')
    monkeypatch.setattr(checker, "REPO_ROOT", tmp_path)

    assert checker.main() == 0
    assert "nothing to check" in capsys.readouterr().out


def test_main_returns_zero_when_extras_do_not_regress(tmp_path: Path, monkeypatch) -> None:
    """main() succeeds when every resolved extra matches or upgrades the base resolution."""
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text('[project]\nname = "example"\n\n[project.optional-dependencies]\nbrowser = ["playwright"]\n')
    monkeypatch.setattr(checker, "REPO_ROOT", tmp_path)

    responses = {
        ".": {"requests": "2.31.0"},
        ".[browser]": {"requests": "2.31.0", "playwright": "1.40.0"},
    }
    with patch.object(checker, "resolve_dry_run", side_effect=lambda req, _python: responses[req]):
        assert checker.main() == 0


def test_main_returns_one_when_extra_downgrades_a_package(tmp_path: Path, monkeypatch, capsys) -> None:
    """main() fails and reports the regression when an extra downgrades a base package."""
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        '[project]\nname = "example"\n\n[project.optional-dependencies]\nlangchain = ["langchain-core"]\n'
    )
    monkeypatch.setattr(checker, "REPO_ROOT", tmp_path)

    responses = {
        ".": {"langgraph": "1.2.11"},
        ".[langchain]": {"langgraph": "1.0.1"},
    }
    with patch.object(checker, "resolve_dry_run", side_effect=lambda req, _python: responses[req]):
        assert checker.main() == 1

    captured = capsys.readouterr()
    assert "langgraph" in captured.err
    assert "1.2.11" in captured.err
    assert "1.0.1" in captured.err
