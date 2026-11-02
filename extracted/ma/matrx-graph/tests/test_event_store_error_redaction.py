from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

import pytest

from matrx_graph.db.event_store import EventStore


class _Rows:
    def __init__(self, rows: list[dict[str, object]]) -> None:
        self.rows = rows

    def filter(self, **_filters: object) -> _Rows:
        return self

    def order_by(self, *_order: object) -> _Rows:
        return self

    def limit(self, _limit: int) -> _Rows:
        return self

    async def values(self, *_fields: str) -> list[dict[str, object]]:
        return self.rows


@pytest.mark.asyncio
async def test_historical_event_read_redacts_stored_error_prose(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    raw = (
        "\x1b[91mMatrx ORM  |  UnknownDatabaseError\n"
        "dataset is not available to this account\n"
        "Query: INSERT INTO private_rows VALUES ($1)\n"
        "Args: ['private row']\nTraceback: internal.py"
    )
    rows = _Rows(
        [
            {
                "id": UUID("00000000-0000-0000-0000-000000000010"),
                "run_id": UUID("00000000-0000-0000-0000-000000000011"),
                "event_type": "node_failed",
                "step": 1,
                "node_id": "save-row",
                "spec_type": "data.save_row",
                "attempt": 1,
                "duration_ms": 4,
                "checkpoint_id": None,
                "error_type": "UnknownDatabaseError",
                "error_message": raw,
                "payload": {
                    "error_message": raw,
                    "error": {"technical": raw},
                    "wrapper": {"error": {"message": raw}},
                },
                "event_ts": datetime(2026, 9, 17, tzinfo=UTC),
                "seq": 1,
            },
            {
                "id": UUID("00000000-0000-0000-0000-000000000012"),
                "run_id": UUID("00000000-0000-0000-0000-000000000011"),
                "event_type": "node_failed",
                "step": 2,
                "node_id": "validate",
                "spec_type": "data.validate",
                "attempt": 1,
                "duration_ms": 2,
                "checkpoint_id": None,
                "error_type": "ValidationError",
                "error_message": "A required value is missing.",
                "payload": {"error_message": "A required value is missing."},
                "event_ts": datetime(2026, 9, 17, 0, 0, 1, tzinfo=UTC),
                "seq": 2,
            },
        ]
    )
    monkeypatch.setattr("matrx_graph.db._registry.get_model", lambda _name: rows)

    events = await EventStore().list_events("00000000-0000-0000-0000-000000000011")

    assert events[0]["error_message"] == "dataset is not available to this account"
    assert events[0]["payload"]["error_message"] == "dataset is not available to this account"
    assert events[0]["payload"]["error"]["technical"] == "dataset is not available to this account"
    assert (
        events[0]["payload"]["wrapper"]["error"]["message"]
        == "dataset is not available to this account"
    )
    assert "private row" not in str(events[0])
    assert events[1]["error_message"] == "A required value is missing."
