"""Tests for check_extras_resolution.get_declared_extras."""

from __future__ import annotations

from pathlib import Path

from tests.scripts.check_extras_resolution import checker


def test_get_declared_extras_returns_sorted_extra_names(tmp_path: Path, monkeypatch) -> None:
    """Extras declared in pyproject.toml are returned sorted by name."""
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        "[project]\n"
        'name = "example"\n'
        "\n"
        "[project.optional-dependencies]\n"
        'zeta = ["z-pkg>=1.0"]\n'
        'alpha = ["a-pkg>=1.0"]\n'
    )
    monkeypatch.setattr(checker, "REPO_ROOT", tmp_path)

    assert checker.get_declared_extras() == ["alpha", "zeta"]


def test_get_declared_extras_returns_empty_list_when_no_extras_declared(tmp_path: Path, monkeypatch) -> None:
    """No [project.optional-dependencies] table means no extras to check."""
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text('[project]\nname = "example"\n')
    monkeypatch.setattr(checker, "REPO_ROOT", tmp_path)

    assert checker.get_declared_extras() == []
