"""The executor marks ONLY its own send as banking discarded attempts (cost adversary pass 5, F7).

``BANKS_DISCARDED_ATTEMPTS`` tells a provider dispatch that its caller banks the billed empty attempts
it discards (the loop puts them in the usage history). ``_send_once_banking_discarded_attempts`` sets it
for one send and resets it. An unconditional ``BANKS_DISCARDED_ATTEMPTS.set(True)`` left just before
that wrapper in ``_execute_until_complete_inner`` made the reset restore True: after the executor's
first send every later direct dispatch in the same context (a tool's STT / rerank / media call) was
treated as banked, so its billed discarded attempt was never filed. The earlier test called the helper
alone; this one runs the REAL executor (mock provider, in-memory store) and reads the flag after it.
"""

from __future__ import annotations

import uuid

import pytest

from matrx_ai._ext import configure_ext

pytestmark = pytest.mark.usefixtures("client_host_sandbox")

from test_execute_with_store import (  # noqa: E402
    _MOCK_MODEL,
    FakeEmitter,
    InMemoryStore,
    StaticCatalog,
)


@pytest.mark.asyncio
async def test_after_the_executor_runs_a_direct_dispatch_is_not_treated_as_banked(monkeypatch):
    import matrx_ai.orchestrator.executor as executor_mod
    from matrx_connect.context.app_context import AppContext, set_app_context

    from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
    from matrx_ai.orchestrator.requests import AIMatrixRequest
    from matrx_ai.providers.unified_client import BANKS_DISCARDED_ATTEMPTS, UnifiedAIClient

    configure_ext(
        conversation_store=InMemoryStore(),
        model_catalog=StaticCatalog([_MOCK_MODEL]),
        api_key_resolver=lambda name: "not-a-real-key",
    )
    set_app_context(
        AppContext(
            emitter=FakeEmitter(),
            user_id=str(uuid.uuid4()),
            request_id=str(uuid.uuid4()),
            conversation_id=str(uuid.uuid4()),
            is_internal_agent=True,
            store=True,
            source_app="client_host_tests",
            source_feature="test",
        )
    )

    seen_during_send: list[bool] = []
    import matrx_ai.orchestrator.send_once as send_once_mod

    real_send_once = send_once_mod.send_once

    async def _spy(*args, **kwargs):
        seen_during_send.append(BANKS_DISCARDED_ATTEMPTS.get())
        return await real_send_once(*args, **kwargs)

    monkeypatch.setattr(send_once_mod, "send_once", _spy)

    config = UnifiedConfig(
        model="mock-model",
        messages=MessageList(_messages=[UnifiedMessage(role="user", content=[TextContent(text="hello")])]),
        metadata={"mock": {"latency_ms": 1, "ttft_ms": 0, "chunks": 1, "mode": "text", "text": "hi"}},
    )
    request = AIMatrixRequest(conversation_id=str(uuid.uuid4()), config=config, request_id=str(uuid.uuid4()))

    assert BANKS_DISCARDED_ATTEMPTS.get() is False
    await executor_mod.execute_until_complete(request, UnifiedAIClient())

    assert seen_during_send and all(seen_during_send), f"the executor's own send must bank: {seen_during_send}"
    assert BANKS_DISCARDED_ATTEMPTS.get() is False, (
        "after the executor's send the flag is still True in this context: a later direct dispatch "
        "(a tool's STT / rerank / media call) is treated as banked and its billed discarded attempt is never filed"
    )
