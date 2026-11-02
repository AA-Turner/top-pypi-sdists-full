"""A node data slot stores its value as JSON, never as a quoted JSON string (no DB).

2026-10-27: matrx-orm c73b6d29 made a plain ``str`` in a json/jsonb field a JSON STRING
value. ``NodeDataSlotStore.upsert_slot`` pre-serialises ``value``/``emissions`` (so JSON
null survives a NOT NULL column) and handed the text over as a ``str`` — the column then
held ``"{\\"summary\\": ...}"``. The store's own reader json.loads strings, so its
round-trip test stayed green; every other reader saw a string. The text now goes in as
``RawJson``. This runs what upsert_slot hands the ORM through the real field prep and
the pool's json codec, and asserts the column holds the structure.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

import pytest

pytest.importorskip("matrx_orm")

from matrx_orm.core.async_db_manager import _encode_json  # noqa: E402
from matrx_orm.core.fields import JSONBField  # noqa: E402

DEF_ID = "22222222-2222-2222-2222-222222222222"
USER_ID = "33333333-3333-3333-3333-333333333333"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "value",
    [{"summary": "hello", "items": [1, 2]}, [1, "two"], "123", '{"a": 1}', None],
)
async def test_slot_value_is_stored_as_json(monkeypatch, value):
    from matrx_graph.db import _registry
    from matrx_graph.db.node_data_slot_store import NodeDataSlotStore
    from matrx_orm.operations import conflict_writes

    field = JSONBField(null=False)
    seen: dict[str, Any] = {}

    async def capture(model, data, **kwargs):
        seen.update(data)
        return {
            "id": "44444444-4444-4444-4444-444444444444",
            "definition_id": DEF_ID,
            "node_id": "n1",
            "slot": "last_test_output",
            "value": None,
            "emissions": {},
            "output_kind": None,
            "source": "node_test",
            "captured_at": datetime.now(UTC),
            "captured_by": None,
            "created_by": USER_ID,
            "updated_at": datetime.now(UTC),
        }

    monkeypatch.setattr(conflict_writes, "upsert_with_conflict", capture)
    monkeypatch.setattr(_registry, "get_model", lambda name: object)

    await NodeDataSlotStore().upsert_slot(
        definition_id=DEF_ID,
        node_id="n1",
        slot="last_test_output",
        value=value,
        emissions={"true": {"went": "this way"}},
        source="node_test",
        user_id=USER_ID,
    )

    def stored(v: Any) -> Any:
        prepped = field.get_db_prep_value(v)
        assert prepped is not None, "a JSON null must still be written, not dropped"
        return json.loads(_encode_json(prepped))

    assert stored(seen["value"]) == value
    assert stored(seen["emissions"]) == {"true": {"went": "this way"}}
