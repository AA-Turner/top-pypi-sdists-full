"""Tests for ``resolve_tasks_template``."""

from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit import scaffold_tasks


def test_resolve_tasks_template_returns_repo_preset(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    preset = repo_root / scaffold_tasks.PRESET_TEMPLATE_RELATIVE_PATH
    preset.parent.mkdir(parents=True)
    preset.write_text("# preset", encoding="utf-8")
    assert scaffold_tasks.resolve_tasks_template(repo_root) == preset.resolve()


def test_resolve_tasks_template_uses_fallback(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    preset = repo_root / scaffold_tasks.PRESET_TEMPLATE_RELATIVE_PATH
    preset.parent.mkdir(parents=True)
    preset.write_text("# preset", encoding="utf-8")
    real_resolve = Path.resolve

    def fake_resolve(self: Path, *args, **kwargs):
        if self == preset:
            return tmp_path / "outside" / "template.md"
        return real_resolve(self, *args, **kwargs)

    monkeypatch.setattr(Path, "resolve", fake_resolve)
    with patch(
        "agentic_devtools.cli.speckit.scaffold_tasks._core_fallback_template", return_value=tmp_path / "fallback.md"
    ):
        assert scaffold_tasks.resolve_tasks_template(repo_root) == tmp_path / "fallback.md"


def test_resolve_tasks_template_without_preset_uses_fallback(tmp_path: Path) -> None:
    with patch(
        "agentic_devtools.cli.speckit.scaffold_tasks._core_fallback_template", return_value=tmp_path / "fallback.md"
    ):
        assert scaffold_tasks.resolve_tasks_template(tmp_path) == tmp_path / "fallback.md"
