"""THE client-host invariant: a full streaming request WITH a tool call,
using ONLY client seams, raises no DBNotConfiguredError and never touches an
ORM base/instance/model.

This is the contract ``matrx_ai.configure()``'s docstring promises ("any
DBNotConfiguredError raised after a configure() like the above is a matrx-ai
packaging bug") — enforced here by POISONING the DB registry accessors for
the duration of the run: any ``get_base`` / ``get_instance`` / ``get_model``
call fails the test with the call recorded.
"""

from __future__ import annotations

import uuid
from typing import Any

import pytest

from matrx_ai._ext import configure_ext

pytestmark = pytest.mark.usefixtures("client_host_sandbox")


# ── Reuse the reference fakes from the sibling store test ───────────────────

from test_execute_with_store import (  # noqa: E402
    _MOCK_MODEL,
    FakeEmitter,
    InMemoryStore,
    StaticCatalog,
)


@pytest.fixture
def probe_tool_registered():
    """Register a real local tool in the singleton registry; restore after."""
    from matrx_ai.tools.registry import ToolRegistry

    registry = ToolRegistry.get_instance()
    saved_tools = dict(registry._tools)
    saved_by_id = dict(registry._tools_by_id)
    saved_loaded = registry._loaded

    async def _probe(args: dict[str, Any], ctx: Any) -> dict[str, Any]:
        return {"probe": "ran", "args": dict(args or {})}

    registry.register_local(
        "client_host_probe_tool",
        _probe,
        description="conformance probe tool",
        parameters={"anything": {"type": "string", "description": "free"}},
    )
    registry._loaded = True
    try:
        yield registry
    finally:
        registry._tools.clear()
        registry._tools.update(saved_tools)
        registry._tools_by_id.clear()
        registry._tools_by_id.update(saved_by_id)
        registry._loaded = saved_loaded


@pytest.fixture
def poisoned_db_registry(monkeypatch):
    """Any ORM-registry access during the test records the offending key."""
    from matrx_ai.db import _registry as db_registry

    touched: list[str] = []

    def _poison(kind: str, original):
        def _fn(name: str, *args: Any, **kwargs: Any):
            touched.append(f"{kind}:{name}")
            return original(name, *args, **kwargs)

        return _fn

    monkeypatch.setattr(db_registry, "get_base", _poison("base", db_registry.get_base))
    monkeypatch.setattr(
        db_registry, "get_instance", _poison("instance", db_registry.get_instance)
    )
    monkeypatch.setattr(db_registry, "get_model", _poison("model", db_registry.get_model))

    # Modules that bound the accessor at import time bypass the module-attr
    # patch — cover the known import-time bindings too so the invariant has
    # no blind spots.
    from matrx_ai.tools import tool_def_db

    monkeypatch.setattr(
        tool_def_db, "get_base", _poison("base", db_registry.get_base)
    )

    return touched


# ── THE INVARIANT, measured honestly ────────────────────────────────────────
#
# AD182: an IN-PROCESS poison cannot enforce this. The reach happens at module
# scope in the PEP-562 lazy impls, so it fires once per interpreter — any
# earlier test warms it — and modules that bind ``cxm`` at import time keep a
# direct reference that no ``sys.modules`` eviction can reach. The guard below
# therefore shells out to a COLD interpreter, which is the only honest measure.
# Same mechanism as the CLI: `uv run python scripts/engine_boundary_census.py`.


@pytest.mark.xfail(
    strict=True,
    reason=(
        "AD182 / agent-engine-extraction Phase 3. In a cold process the engine "
        "reaches the ORM registry 27 times from exactly TWO modules — "
        "db/_cx_managers_impl.py (24) and db/_conversation_rebuild_impl.py (3) — "
        "both of which materialise ORM classes at MODULE SCOPE, so importing them "
        "at all IS the reach. With no registry (a real client host) the first one "
        "RAISES DBNotConfiguredError, so this path has never actually run ORM-free; "
        "the suite passes only because conftest registers stub models process-wide. "
        "Flips to a real pass the moment the ConversationSink port displaces those "
        "two modules. strict=True so it screams in either direction."
    ),
)
def test_engine_touches_no_orm_in_a_cold_process():
    """THE client-host invariant. Cold subprocess — immune to test ordering."""
    import importlib.util
    from pathlib import Path

    script = Path(__file__).resolve().parents[2] / "scripts" / "engine_boundary_census.py"
    spec = importlib.util.spec_from_file_location("engine_boundary_census", script)
    census = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(census)

    reaches = census.run_census(with_stubs=True)
    detail = "\n".join(f"  {r['kind']}:{r['name']}  <- {r['from']}" for r in reaches)
    assert reaches == [], (
        f"engine reached the ORM registry {len(reaches)} times in a cold run:\n{detail}"
    )


@pytest.mark.asyncio
async def test_streaming_request_with_tool_call_runs_entirely_through_the_store(
    probe_tool_registered, poisoned_db_registry
):
    store = InMemoryStore()
    configure_ext(
        conversation_store=store,
        model_catalog=StaticCatalog([_MOCK_MODEL]),
        api_key_resolver=lambda name: "not-a-real-key",
    )

    emitter = FakeEmitter()
    from matrx_connect.context.app_context import AppContext, set_app_context

    conversation_id = str(uuid.uuid4())
    request_id = str(uuid.uuid4())
    ctx = AppContext(
        emitter=emitter,
        user_id=str(uuid.uuid4()),
        request_id=request_id,
        conversation_id=conversation_id,
        is_internal_agent=True,
        store=True,
        source_app="client_host_tests",
        source_feature="test",
    )
    set_app_context(ctx)

    from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
    from matrx_ai.orchestrator.executor import execute_until_complete
    from matrx_ai.orchestrator.requests import AIMatrixRequest
    from matrx_ai.providers.unified_client import UnifiedAIClient

    config = UnifiedConfig(
        model="mock-model",
        tools=["client_host_probe_tool"],
        messages=MessageList(
            _messages=[
                UnifiedMessage(role="user", content=[TextContent(text="use the probe tool")])
            ]
        ),
        metadata={
            "mock": {
                "latency_ms": 1,
                "ttft_ms": 0,
                "chunks": 1,
                "mode": "text",
                "text": "done — the probe ran",
                "tool_calls": [
                    {"name": "client_host_probe_tool", "arguments": {"anything": "x"}}
                ],
            }
        },
    )
    request = AIMatrixRequest(
        conversation_id=conversation_id,
        config=config,
        request_id=request_id,
    )

    completed = await execute_until_complete(request, UnifiedAIClient())

    # The full round trip happened: tool dispatched, follow-up text returned.
    final_text = "".join(
        c.text
        for m in completed.final_response.messages
        for c in (m.content or [])
        if getattr(c, "text", None)
    )
    assert "done — the probe ran" in final_text

    # The tool call was really executed and logged THROUGH THE STORE.
    assert any(
        row.get("tool_name") == "client_host_probe_tool" for row in store.tool_rows.values()
    ), f"probe tool never reached the store logger; store rows: {store.tool_rows}"
    completed_rows = [
        row
        for row in store.tool_rows.values()
        if row.get("tool_name") == "client_host_probe_tool"
        and row.get("status") == "completed"
    ]
    assert completed_rows, "probe tool row never flipped to completed in the store"

    # Persistence went to the store.
    assert store.completed, "persist_completed_request never ran"

    # NOTE: the zero-ORM INVARIANT is NOT asserted here — an in-process poison
    # cannot enforce it (see the cold-process test above and AD182). What this
    # test proves is the store round trip: tool dispatched, logged, completed,
    # and persisted, entirely through host-injected seams.


@pytest.mark.asyncio
async def test_get_coordinator_short_circuits_with_store(poisoned_db_registry):
    """#4 — a configured conversation_store forces the WriteCoordinator OFF,
    even from inside a live RequestLane (matrx-connect always opens one)."""
    configure_ext(
        conversation_store=InMemoryStore(),
        model_catalog=StaticCatalog([_MOCK_MODEL]),
    )
    from matrx_ai.persistence.queue_helpers import get_coordinator

    assert get_coordinator() is None
    assert poisoned_db_registry == []


@pytest.mark.asyncio
async def test_drain_pending_skips_inbox_with_store(poisoned_db_registry):
    """#5 — the turn-boundary drain never reads cx_pending_injection on a
    client host; in-memory tool mutations still drain."""
    configure_ext(
        conversation_store=InMemoryStore(),
        model_catalog=StaticCatalog([_MOCK_MODEL]),
    )
    from matrx_connect.context.app_context import AppContext, set_app_context

    from matrx_ai.config import MessageList, UnifiedConfig
    from matrx_ai.tools.dynamic_drain import drain_pending

    emitter = FakeEmitter()
    ctx = AppContext(
        emitter=emitter,
        user_id=str(uuid.uuid4()),
        request_id=str(uuid.uuid4()),
        conversation_id=str(uuid.uuid4()),
        is_internal_agent=True,
        store=False,
        source_app="client_host_tests",
        source_feature="test",
    )
    set_app_context(ctx)

    config = UnifiedConfig(model="mock-model", messages=MessageList(_messages=[]))
    out_ctx = await drain_pending(config, ctx)
    assert out_ctx is not None
    assert poisoned_db_registry == []
