"""Tests for ``resolve_plan_template``."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.speckit.scaffold_plan import PRESET_TEMPLATE_RELATIVE_PATH, resolve_plan_template


class TestResolvePlanTemplate:
    """resolve_plan_template prefers the repo preset template, then the core-pack fallback."""

    def test_returns_preset_template_when_present(self, tmp_path: Path) -> None:
        preset_path = tmp_path / PRESET_TEMPLATE_RELATIVE_PATH
        preset_path.parent.mkdir(parents=True)
        preset_path.write_text("# Preset", encoding="utf-8")

        result = resolve_plan_template(tmp_path)

        assert result == preset_path.resolve()

    def test_falls_back_to_core_pack_when_preset_missing(self, tmp_path: Path) -> None:
        with patch(
            "agentic_devtools.cli.speckit.scaffold_plan._core_fallback_template",
            return_value=Path("/core/plan-template.md"),
        ) as mock_fallback:
            result = resolve_plan_template(tmp_path)

        mock_fallback.assert_called_once_with()
        assert result == Path("/core/plan-template.md")

    def test_returns_none_when_neither_available(self, tmp_path: Path) -> None:
        with patch("agentic_devtools.cli.speckit.scaffold_plan._core_fallback_template", return_value=None):
            result = resolve_plan_template(tmp_path)

        assert result is None

    def test_falls_back_when_repo_preset_resolves_outside_repo_root(self, tmp_path: Path) -> None:
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        outside = tmp_path / "outside-template.md"
        outside.write_text("# Outside", encoding="utf-8")
        preset_path = repo_root / PRESET_TEMPLATE_RELATIVE_PATH
        preset_path.parent.mkdir(parents=True)
        preset_path.symlink_to(outside)

        with patch(
            "agentic_devtools.cli.speckit.scaffold_plan._core_fallback_template",
            return_value=Path("/core/plan-template.md"),
        ) as mock_fallback:
            result = resolve_plan_template(repo_root)

        mock_fallback.assert_called_once_with()
        assert result == Path("/core/plan-template.md")
