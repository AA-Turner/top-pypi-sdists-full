"""The stale tool-call sweep settles every non-terminal row, 'pending' included.

PB-08 defect 58: Tidewell's ``agent`` row read ``pending`` (the column default,
written over its completion by a grouped flush) and stayed non-terminal after
its run ended; the sweep only looked for ``running``.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.tools import logger as tool_logger


async def test_the_sweep_asks_for_pending_and_running_rows(monkeypatch: pytest.MonkeyPatch) -> None:
    seen: dict = {}
    pending_row = SimpleNamespace(id="row-1", status="pending")

    class _ToolCalls:
        async def filter_items(self, **filters):
            seen.update(filters)
            statuses = filters.get("status__in") or [filters.get("status")]
            return [pending_row] if "pending" in statuses else []

    monkeypatch.setattr(tool_logger, "_cxm", lambda: SimpleNamespace(tool_call=_ToolCalls()))
    monkeypatch.setattr(
        "matrx_ai.db.cx_managers.server_maintenance_available", lambda: True
    )
    settled: list[str] = []

    async def _abandon(self, row_id, **kw):
        settled.append(row_id)

    monkeypatch.setattr(tool_logger.ToolExecutionLogger, "log_abandoned", _abandon)
    count = await tool_logger.ToolExecutionLogger().abandon_stale_running_rows(older_than_seconds=60)
    assert settled == ["row-1"], f"a stale 'pending' row was not settled (filters {seen})"
    assert count == 1
