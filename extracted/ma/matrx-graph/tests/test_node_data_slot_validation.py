"""Pure-unit guards of NodeDataSlotStore — no database required.

The slot-name and size-cap gates fire BEFORE any connection is acquired, so
they belong in the always-on suite (the DB round-trips live in
test_node_data_slot_store.py behind the MATRX_GRAPH_TEST_DB gate).
"""

from __future__ import annotations

from uuid import uuid4

import pytest

from matrx_graph.db.node_data_slot_store import (
    MAX_SLOT_VALUE_BYTES,
    VALID_SLOTS,
    NodeDataSlotStore,
    SlotValueTooLargeError,
)

pytestmark = pytest.mark.asyncio


async def test_unknown_slot_rejected_before_db() -> None:
    store = NodeDataSlotStore()
    with pytest.raises(ValueError, match="unknown node_data_slot"):
        await store.upsert_slot(
            definition_id=str(uuid4()),
            node_id="n1",
            slot="bogus",
            value={},
            source="declared",
            user_id=str(uuid4()),
        )
    with pytest.raises(ValueError, match="unknown node_data_slot"):
        await store.delete_slot(str(uuid4()), "n1", "bogus")


async def test_blank_user_id_rejected_before_db() -> None:
    store = NodeDataSlotStore()
    with pytest.raises(ValueError, match="created_by is required"):
        await store.upsert_slot(
            definition_id=str(uuid4()),
            node_id="n1",
            slot=VALID_SLOTS[0],
            value={},
            source="declared",
            user_id="",
        )


@pytest.mark.parametrize("field", ["value", "emissions"])
async def test_oversized_payload_rejected_with_size_named(field: str) -> None:
    store = NodeDataSlotStore()
    huge = {"blob": "x" * (MAX_SLOT_VALUE_BYTES + 1)}
    kwargs: dict = dict(
        definition_id=str(uuid4()),
        node_id="n1",
        slot="declared_sample",
        value={} if field == "emissions" else huge,
        emissions=huge if field == "emissions" else None,
        source="declared",
        user_id=str(uuid4()),
    )
    with pytest.raises(SlotValueTooLargeError) as exc_info:
        await store.upsert_slot(**kwargs)
    err = exc_info.value
    assert err.field == field
    assert err.size_bytes > MAX_SLOT_VALUE_BYTES
    # The message must NAME the offending size and the cap — actionable, not vague.
    assert str(err.size_bytes) in str(err)
    assert str(MAX_SLOT_VALUE_BYTES) in str(err)
