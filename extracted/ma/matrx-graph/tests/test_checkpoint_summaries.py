from __future__ import annotations

from uuid import uuid4

import pytest

from matrx_graph.checkpoint import postgres as module


@pytest.mark.asyncio
async def test_checkpoint_summaries_page_without_loading_channel_state(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    run_id = str(uuid4())
    checkpoint_id = str(uuid4())
    selected: tuple[str, ...] = ()

    class Query:
        def filter(self, **kwargs: object) -> Query:
            assert kwargs == {"run_id": run_id}
            return self

        def order_by(self, *columns: str) -> Query:
            assert columns == ("-step", "-created_at")
            return self

        def limit(self, value: int) -> Query:
            assert value == 3
            return self

        def offset(self, value: int) -> Query:
            assert value == 4
            return self

        async def values(self, *columns: str) -> list[dict[str, object]]:
            nonlocal selected
            selected = columns
            return [
                {
                    "id": checkpoint_id,
                    "parent_checkpoint_id": None,
                    "step": 7,
                    "next_invocations": [{"node_id": "draft"}],
                    "interrupt_payload": {"question": "continue?"},
                },
                {
                    "id": str(uuid4()),
                    "parent_checkpoint_id": checkpoint_id,
                    "step": 6,
                    "next_invocations": [],
                    "interrupt_payload": None,
                },
                {
                    "id": str(uuid4()),
                    "parent_checkpoint_id": None,
                    "step": 5,
                    "next_invocations": [],
                    "interrupt_payload": None,
                },
            ]

    query = Query()
    monkeypatch.setattr(module, "get_model", lambda name: query)

    rows, has_more = await module.PostgresCheckpointer().list_checkpoint_summaries(
        run_id,
        limit=2,
        offset=4,
    )

    assert has_more is True
    assert len(rows) == 2
    assert rows[0]["checkpoint_id"] == checkpoint_id
    assert rows[0]["scheduled_node_ids"] == ["draft"]
    assert "channel_values" not in selected
    assert "pending_bindings" not in selected
