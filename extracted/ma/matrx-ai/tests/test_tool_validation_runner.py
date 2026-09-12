"""Regression guards for validation declaration-module loading."""

from __future__ import annotations

import sys
from pathlib import Path

from matrx_ai.tools.validation.runner import import_declaration_modules


def test_declaration_module_loader_preserves_custom_and_unloaded_module_behavior(
    tmp_path: Path, monkeypatch
) -> None:
    package = tmp_path / "validation_declarations"
    package.mkdir()
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "ready.py").write_text("VALUE = 42\n", encoding="utf-8")
    (package / "broken.py").write_text("raise RuntimeError('not available')\n", encoding="utf-8")
    monkeypatch.syspath_prepend(str(tmp_path))

    names = (
        "validation_declarations.ready",
        "validation_declarations.missing",
        "validation_declarations.broken",
    )
    try:
        failures = import_declaration_modules(names)

        assert sys.modules["validation_declarations.ready"].VALUE == 42
        assert import_declaration_modules(("validation_declarations.ready",)) == []
        assert any("validation_declarations.missing" in failure for failure in failures)
        assert any("validation_declarations.broken" in failure for failure in failures)
        assert "validation_declarations.broken" not in sys.modules
    finally:
        for name in tuple(sys.modules):
            if name == "validation_declarations" or name.startswith("validation_declarations."):
                sys.modules.pop(name, None)


def test_validation_runner_has_no_unresolved_dynamic_import() -> None:
    """The mandate scanner must see the validation runner's import boundary."""
    from matrx_mandate_scan.adapters.python import scan_source

    source_path = Path(__file__).parents[1] / "matrx_ai/tools/validation/runner.py"
    findings = scan_source(source_path.read_text(encoding="utf-8"), source_path.as_posix()).findings

    assert [finding for finding in findings if finding.code == "UNRESOLVED_IMPORT"] == []
