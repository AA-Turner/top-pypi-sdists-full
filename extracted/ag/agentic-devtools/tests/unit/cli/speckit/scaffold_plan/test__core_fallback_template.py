"""Tests for ``_core_fallback_template``."""

from pathlib import Path
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.speckit.scaffold_plan import _core_fallback_template


class TestCoreFallbackTemplate:
    """_core_fallback_template resolves the specify-cli bundled plan template."""

    def test_returns_none_when_specify_cli_not_installed(self) -> None:
        with patch.dict("sys.modules", {"specify_cli": None}):
            result = _core_fallback_template()

        assert result is None

    def test_returns_template_path_when_present(self, tmp_path: Path) -> None:
        core_pack = tmp_path / "specify_cli" / "core_pack" / "templates"
        core_pack.mkdir(parents=True)
        template = core_pack / "plan-template.md"
        template.write_text("# Plan Template", encoding="utf-8")

        fake_module = MagicMock(__file__=str(tmp_path / "specify_cli" / "__init__.py"))
        with patch.dict("sys.modules", {"specify_cli": fake_module}):
            result = _core_fallback_template()

        assert result == template

    def test_returns_none_when_template_file_missing(self, tmp_path: Path) -> None:
        fake_module = MagicMock(__file__=str(tmp_path / "specify_cli" / "__init__.py"))
        with patch.dict("sys.modules", {"specify_cli": fake_module}):
            result = _core_fallback_template()

        assert result is None
