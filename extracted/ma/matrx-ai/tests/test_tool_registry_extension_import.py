"""ToolRegistry must keep persisted third-party callable paths loadable."""

from __future__ import annotations

import sys

from matrx_ai.tools.registry import ToolRegistry


def test_resolve_callable_loads_an_unloaded_extension_module(tmp_path, monkeypatch) -> None:
    module_name = "test_unloaded_tool_extension"
    (tmp_path / f"{module_name}.py").write_text(
        "async def entry() -> str:\n    return 'loaded'\n",
        encoding="utf-8",
    )
    monkeypatch.syspath_prepend(str(tmp_path))
    sys.modules.pop(module_name, None)

    resolved = ToolRegistry._resolve_callable(f"{module_name}.entry")

    assert callable(resolved)
    assert resolved.__module__ == module_name
