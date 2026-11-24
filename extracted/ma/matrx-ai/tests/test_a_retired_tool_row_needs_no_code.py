"""A soft-deleted ``tool.definition`` row is retired: the drift gate never demands code for it.

Live 2026-11-03: ``sandbox_maintenance`` (definition ``deleted_at`` set, binding inactive) failed every
production boot as ``missing_in_code``.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.tools.validation import runner
from matrx_ai.tools.validation.engine import FindingKind, validate


@pytest.mark.asyncio
async def test_a_soft_deleted_definition_is_not_demanded(monkeypatch: pytest.MonkeyPatch) -> None:
    import matrx_ai.tools.tool_binding_db as binding_db
    import matrx_ai.tools.tool_def_db as def_db

    defs = [
        SimpleNamespace(id="t1", name="retired_tool", source_kind="native", parameters={}, description="",
                        is_active=True, validation_exempt=False, deleted_at="2026-11-02T07:49:19Z"),
        SimpleNamespace(id="t2", name="live_tool", source_kind="native", parameters={}, description="",
                        is_active=True, validation_exempt=False, deleted_at=None),
    ]
    bindings = [SimpleNamespace(tool_id="t1", executor_name="aidream", is_active=False),
                SimpleNamespace(tool_id="t2", executor_name="aidream", is_active=True)]

    async def load_all_tools() -> list[Any]:
        return defs

    async def load_all() -> list[Any]:
        return bindings

    monkeypatch.setattr(def_db.tool_def_manager_instance, "load_all_tools", load_all_tools)
    monkeypatch.setattr(binding_db.tool_binding_manager_instance, "load_all", load_all)

    rows = await runner.fetch_db_rows()
    report = validate({}, rows, owner_executors={"aidream"})
    missing = {f.tool_name for f in report.findings if f.kind == FindingKind.MISSING_IN_CODE}
    assert "retired_tool" not in missing
    assert "live_tool" in missing  # the gate still fails a live row with no code
