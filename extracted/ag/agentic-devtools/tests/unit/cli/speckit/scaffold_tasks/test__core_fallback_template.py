"""Tests for ``_core_fallback_template``."""

import sys
from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.speckit import scaffold_tasks


def test_core_fallback_template_handles_missing_dependency() -> None:
    with patch("builtins.__import__", side_effect=ImportError):
        assert scaffold_tasks._core_fallback_template() is None


def test_core_fallback_template_returns_installed_template(tmp_path: Path) -> None:
    package_dir = tmp_path / "specify_cli"
    template = package_dir / "core_pack" / "templates" / "tasks-template.md"
    template.parent.mkdir(parents=True)
    template.write_text("# bundled", encoding="utf-8")
    module = type("Module", (), {"__file__": str(package_dir / "__init__.py")})()
    with patch.dict(sys.modules, {"specify_cli": module}):
        assert scaffold_tasks._core_fallback_template() == template.resolve()
