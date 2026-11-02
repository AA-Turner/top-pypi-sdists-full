"""An ARCHIVED saved result (``workflow.step_result.deleted_at``) is never reused.

2026-10-27: ``scripts/test_run_left_live.py <run> --archive`` could never archive a test run's
saved results — the table had no ``deleted_at``, so ``platform._test_run_archive_one`` skipped it.
The column exists now (0120); this proves the store honours it: an archived row reads as expired
the moment it was archived, the next invocation claims it and pays, and settling revives the row.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from typing import Any

from matrx_graph.once import (
    Claim,
    ClaimPosition,
    PostgresStepResultStore,
    StepResultKey,
    StoredResult,
    acquire,
)

KEY = StepResultKey(
    organization_id="11111111-1111-4111-8111-111111111111", scope="workflow",
    scope_id="33333333-3333-4333-8333-333333333333", step_type="docproc.ingest.from_media_refs",
    result_key="k",
)
RUN = "44444444-4444-4444-8444-444444444444"


class _Model:
    def __init__(self, row: dict[str, Any]) -> None:
        self.row = row
        self.updates: list[dict[str, Any]] = []

    def filter(self, **_kw: Any) -> Any:
        row = self.row

        class _Q:
            async def values(self, *cols: str) -> list[dict[str, Any]]:
                return [{c: row.get(c) for c in cols}]

        return _Q()

    async def update_where(self, filters: dict[str, Any], **fields: Any) -> Any:
        self.updates.append(fields)
        if "succeeded_at" in filters and filters["succeeded_at"] != self.row.get("succeeded_at"):
            return SimpleNamespace(rows_affected=0)
        self.row.update(fields)
        return SimpleNamespace(rows_affected=1)


def _store(model: _Model) -> PostgresStepResultStore:
    store = PostgresStepResultStore()
    store._model = lambda: model  # type: ignore[method-assign]

    async def _intern(_run: str, output: dict[str, Any]) -> dict[str, Any]:
        return output

    store._intern_output = _intern  # type: ignore[method-assign]
    return store


async def test_an_archived_result_is_claimed_and_paid_for_then_revived() -> None:
    done = datetime.now(UTC) - timedelta(hours=1)
    model = _Model({
        "id": "55555555-5555-4555-8555-555555555555", "input_digest": "d", "output": {"chunks": []},
        "origin_run_id": RUN, "succeeded_at": done, "expires_at": None,
        "deleted_at": done + timedelta(minutes=5),
    })
    store = _store(model)
    decision = await acquire(
        store, KEY, digest="d", position=ClaimPosition(run_id=RUN, node_id="read"),
        lease_seconds=30, reuse_changed=False, bypass=False,
    )
    assert isinstance(decision, Claim), "an archived result was reused"
    settled = await store.settle(
        KEY, token=decision.token,
        result=StoredResult(input_digest="d", output={"chunks": []}, output_kind=None, verdict={}, emissions={},
                            origin_run_id=RUN, origin_node_id="read", origin_step=1, origin_dispatch_id="",
                            origin_item_index=0, origin_attempt=1, succeeded_at=datetime.now(UTC), expires_at=None),
    )
    assert settled
    assert model.row["deleted_at"] is None
