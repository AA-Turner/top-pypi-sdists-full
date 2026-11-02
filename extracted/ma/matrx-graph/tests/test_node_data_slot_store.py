"""Integration tests for NodeDataSlotStore — the sample-data spine (spec §7).

Skipped automatically when MATRX_GRAPH_TEST_DB is unset. To run locally:

    export MATRX_GRAPH_TEST_DB=1
    # ensure `.env` has SUPABASE_MATRIX_* set for matrx-orm
    # ensure migration 0022_node_data_slot.sql has been applied
    uv run --package matrx-graph pytest \
        packages/matrx-graph/tests/test_node_data_slot_store.py -v

Same production-refusal posture as test_postgres_checkpointer.py: the
module fixture registers the DB and HARD-FAILS through tests/_db_guard.py
if the connection fingerprint matches production. Each test creates and
archives its own definition rows.
"""

from __future__ import annotations

import os
from uuid import uuid4

import pytest

# Load the repo .env HERE, above the gate. The skip decision below reads
# process env, and other suites (anything importing aidream.config) load .env
# as an import side effect — so without this line the same commit skips when
# this file is collected alone and runs when it is collected second.
# Guard: scripts/check_test_gate_determinism.py
from dotenv import load_dotenv

load_dotenv()


pytestmark = [
    pytest.mark.skipif(
        not os.environ.get("MATRX_GRAPH_TEST_DB"),
        reason="Set MATRX_GRAPH_TEST_DB=1 to run NodeDataSlotStore integration tests.",
    ),
    # All tests share matrx-orm's registered asyncpg pool. Keep that pool on one
    # event loop instead of tearing its SSL transports down between test loops.
    pytest.mark.asyncio(loop_scope="session"),
]

TEST_USER_ID = os.environ.get("MATRX_GRAPH_TEST_USER_ID", "87a6e699-3622-4869-8843-d0867456c0dd")
TEST_ORGANIZATION_ID = os.environ.get(
    "MATRX_GRAPH_TEST_ORGANIZATION_ID", "3e790542-fdaf-40b2-8bf3-658bf94fe67f"
)


@pytest.fixture(scope="module", autouse=True)
def _bootstrap_db() -> None:
    """Register the aidream database so matrx-orm's pool can be acquired.

    HARD-FAILS via the production refusal gate if SUPABASE_MATRIX_* points
    at the production project — this suite writes real workflow.* rows
    (see tests/_db_guard.py; escape hatch MATRX_ALLOW_PROD_DB_TESTS=1).
    """
    from dotenv import load_dotenv

    load_dotenv()

    from matrx_orm import register_platform_db

    register_platform_db(
        "supabase_automation_matrix",
        package="matrx-graph tests",
        additional_schemas=["auth"],
    )

    from ._db_guard import assert_not_production_db

    assert_not_production_db("supabase_automation_matrix")

    # Registration configures the connection only. These tests bootstrap the
    # package's standalone schema, so wire Models that match that schema rather
    # than aidream's host-enriched Models.
    from matrx_graph.db import configure_standalone_db, reset_for_tests

    reset_for_tests()
    configure_standalone_db("supabase_automation_matrix")


async def _make_definition():
    from matrx_graph import Definition
    from matrx_graph.db import DefinitionStore

    store = DefinitionStore()
    row = await store.create(
        name=f"slot-test-{uuid4()}", definition=Definition(), user_id=TEST_USER_ID
    )
    return store, row


async def test_upsert_get_delete_roundtrip():
    from matrx_graph.db import NodeDataSlotStore

    def_store, definition = await _make_definition()
    slots = NodeDataSlotStore()
    try:
        stored = await slots.upsert_slot(
            definition_id=definition.id,
            node_id="n1",
            slot="last_test_output",
            value={"summary": "hello", "items": [1, 2]},
            emissions={"true": {"went": "this way"}},
            output_kind="json",
            source="node_test",
            user_id=TEST_USER_ID,
            captured_by=TEST_USER_ID,
        )
        assert stored.slot == "last_test_output"
        assert stored.value == {"summary": "hello", "items": [1, 2]}
        assert stored.emissions == {"true": {"went": "this way"}}
        assert stored.output_kind == "json"
        assert stored.source == "node_test"
        assert stored.created_by == TEST_USER_ID

        # Upsert REPLACES — one row per (definition, node, slot), no history.
        replaced = await slots.upsert_slot(
            definition_id=definition.id,
            node_id="n1",
            slot="last_test_output",
            value={"summary": "replaced"},
            source="node_test",
            user_id=TEST_USER_ID,
        )
        assert replaced.value == {"summary": "replaced"}
        assert replaced.emissions == {}
        assert replaced.created_by == TEST_USER_ID

        rows = await slots.get_slots(definition.id, "n1")
        assert len(rows) == 1
        assert rows[0].value == {"summary": "replaced"}

        assert await slots.delete_slot(definition.id, "n1", "last_test_output") is True
        assert await slots.delete_slot(definition.id, "n1", "last_test_output") is False
        assert await slots.get_slots(definition.id, "n1") == []
    finally:
        await def_store.archive(definition.id)


async def test_get_slots_whole_definition_and_node_gc():
    from matrx_graph.db import NodeDataSlotStore

    def_store, definition = await _make_definition()
    slots = NodeDataSlotStore()
    try:
        for node_id, slot in (
            ("a", "declared_sample"),
            ("a", "last_test_output"),
            ("b", "last_live_output"),
        ):
            await slots.upsert_slot(
                definition_id=definition.id,
                node_id=node_id,
                slot=slot,
                value={"from": slot},
                source="declared" if slot == "declared_sample" else "node_test",
                user_id=TEST_USER_ID,
            )

        rows = await slots.get_slots(definition.id)
        assert {(r.node_id, r.slot) for r in rows} == {
            ("a", "declared_sample"),
            ("a", "last_test_output"),
            ("b", "last_live_output"),
        }

        # Node 'b' removed from the draft → its slots go too (spec §7.2).
        removed = await slots.delete_missing_nodes(definition.id, ["a"])
        assert removed == 1
        rows = await slots.get_slots(definition.id)
        assert {r.node_id for r in rows} == {"a"}
    finally:
        await def_store.archive(definition.id)


async def test_invalid_slot_and_missing_user_are_rejected():
    from matrx_graph.db import NodeDataSlotStore

    slots = NodeDataSlotStore()
    with pytest.raises(ValueError, match="unknown node_data_slot"):
        await slots.upsert_slot(
            definition_id=str(uuid4()),
            node_id="n1",
            slot="nonsense_mandate",
            value={},
            source="declared",
            user_id=TEST_USER_ID,
        )
    with pytest.raises(ValueError, match="unknown node_data_slot"):
        await slots.delete_slot(str(uuid4()), "n1", "nonsense_mandate")
    with pytest.raises(ValueError, match="created_by is required"):
        await slots.upsert_slot(
            definition_id=str(uuid4()),
            node_id="n1",
            slot="declared_sample",
            value={},
            source="declared",
            user_id="",
        )


async def test_oversized_value_rejected_with_size_in_error():
    from matrx_graph.db import (
        MAX_SLOT_VALUE_BYTES,
        NodeDataSlotStore,
        SlotValueTooLargeError,
    )

    slots = NodeDataSlotStore()
    huge = {"blob": "x" * (MAX_SLOT_VALUE_BYTES + 1)}
    with pytest.raises(SlotValueTooLargeError) as exc_info:
        await slots.upsert_slot(
            definition_id=str(uuid4()),
            node_id="n1",
            slot="declared_sample",
            value=huge,
            source="declared",
            user_id=TEST_USER_ID,
        )
    # The error must NAME the offending size and the cap.
    assert str(MAX_SLOT_VALUE_BYTES) in str(exc_info.value)
    assert exc_info.value.size_bytes > MAX_SLOT_VALUE_BYTES


async def test_adopt_live_outputs_takes_latest_clean_executor_outcome():
    from matrx_graph.checkpoint import PostgresCheckpointer
    from matrx_graph.checkpoint.protocol import NodeOutcome
    from matrx_graph.db import NodeDataSlotStore, RunStore

    def_store, definition = await _make_definition()
    run_store = RunStore()
    checkpointer = PostgresCheckpointer()
    slots = NodeDataSlotStore()

    run_id = await run_store.create(
        definition_id=definition.id,
        definition_hash="slot-test-hash",
        inputs={},
        user_id=TEST_USER_ID,
        organization_id=TEST_ORGANIZATION_ID,
    )
    try:
        # step 0: a clean outcome for n1.
        await checkpointer.record_outcome(
            NodeOutcome(
                run_id=run_id,
                step=0,
                node_id="n1",
                attempt=1,
                output={"stage": "early"},
                output_kind="json",
            )
        )
        # step 1: a NEWER clean outcome for n1 — this one must win.
        await checkpointer.record_outcome(
            NodeOutcome(
                run_id=run_id,
                step=1,
                node_id="n1",
                attempt=1,
                output={"stage": "late"},
                output_kind="json",
            )
        )
        # n2 failed — error present → never adopted.
        await checkpointer.record_outcome(
            NodeOutcome(
                run_id=run_id,
                step=1,
                node_id="n2",
                attempt=1,
                output={},
                error={"error_type": "Boom", "error_message": "no"},
            )
        )
        # n3 was user-skipped — non-executor source → never adopted.
        await checkpointer.record_outcome(
            NodeOutcome(
                run_id=run_id,
                step=1,
                node_id="n3",
                attempt=1,
                output={"placeholder": True},
                source="user_skip",
            )
        )

        adopted = await slots.adopt_live_outputs(
            run_id=run_id, definition_id=definition.id, user_id=TEST_USER_ID
        )
        assert adopted == 1

        rows = await slots.get_slots(definition.id, "n1")
        assert len(rows) == 1
        assert rows[0].slot == "last_live_output"
        assert rows[0].value == {"stage": "late"}
        assert rows[0].output_kind == "json"
        assert rows[0].source == "live_run"
        assert rows[0].created_by == TEST_USER_ID
        assert await slots.get_slots(definition.id, "n2") == []
        assert await slots.get_slots(definition.id, "n3") == []

        # Re-adoption is an idempotent upsert — still exactly one row.
        adopted_again = await slots.adopt_live_outputs(
            run_id=run_id, definition_id=definition.id, user_id=TEST_USER_ID
        )
        assert adopted_again == 1
        assert len(await slots.get_slots(definition.id, "n1")) == 1
    finally:
        await def_store.archive(definition.id)
