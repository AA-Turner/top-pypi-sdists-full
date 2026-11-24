"""A shutdown-cancelled run resumed and ended again: the first end's late marker clear must not wipe the SECOND marker.

The marker carries a unique token and the clear is a conditional update (only while the token still matches), so a
crash in that window still leaves the second end's after-work owed to ``recover_settle_after``. Red before: the clear
was unconditional and wiped the second marker (recovery found nothing, the second after-work was lost).
"""

from __future__ import annotations

from types import SimpleNamespace as NS
from typing import Any

import pytest

pytestmark = pytest.mark.asyncio

RUN = "55555555-5555-4555-8555-555555555555"


class _Query:
    def __init__(self, model: _WfRun) -> None:
        self.model = model

    def limit(self, _n: int) -> _Query:
        return self

    async def values(self, *_cols: str) -> list[dict[str, Any]]:
        marker = self.model.metadata.get("_settle_after")
        if not (isinstance(marker, dict) and marker.get("pending")):
            return []
        return [{"id": RUN, "status": "completed", "metadata": dict(self.model.metadata)}]


class _WfRun:
    def __init__(self) -> None:
        self.metadata: dict[str, Any] = {}

    def filter(self, **_k: Any) -> _Query:
        return _Query(self)

    async def update_where(self, filters: dict[str, Any], **updates: Any) -> Any:
        want = filters.get("metadata__json_contains")
        if want is not None:
            have = self.metadata.get("_settle_after")
            if not (isinstance(have, dict) and have.get("token") == want["_settle_after"]["token"]):
                return NS(rows_affected=0, updated_rows=[])
        merge = updates.get("metadata")
        if merge is not None:
            self.metadata.update(merge.value)
        return NS(rows_affected=1, updated_rows=[])


async def test_the_first_ends_late_clear_leaves_the_second_marker(monkeypatch) -> None:
    from matrx_graph.db import run_store as rs

    model = _WfRun()
    monkeypatch.setattr(rs, "get_model", lambda _key: model)
    ran: list[str] = []

    async def _after(run_id: str, status: str, cancel_reason: Any, row: Any = None) -> None:
        ran.append(status)

    rs.configure_run_settled_after(_after)
    try:
        # End 1 writes marker A; the run is resumed and ends again, writing marker B, BEFORE clear A lands.
        model.metadata["_settle_after"] = {"pending": True, "cancel_reason": None, "token": "A"}
        model.metadata["_settle_after"] = {"pending": True, "cancel_reason": None, "token": "B"}
        await rs._settle_after(RUN, "cancelled", None, marker_token="A")  # the late first clear
        assert model.metadata["_settle_after"]["token"] == "B", "the late clear wiped the newer marker"
        # the process dies here: recovery still owes the second end's work, and clears only its own marker
        ran.clear()
        assert await rs.recover_settle_after(older_than_seconds=0) == 1
        assert ran == ["completed"]
        assert model.metadata["_settle_after"] is None
        assert await rs.recover_settle_after(older_than_seconds=0) == 0
    finally:
        rs.configure_run_settled_after(None)
