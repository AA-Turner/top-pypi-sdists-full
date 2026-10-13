import pytest
from tests.client_host.test_execute_with_store import *  # noqa

@pytest.mark.asyncio
async def test_probe():
    store = InMemoryStore(); _configure_client_host(store); emitter = FakeEmitter()
    conversation_id, request_id, _u = _set_context(emitter)
    from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
    from matrx_ai.orchestrator.executor import execute_until_complete
    from matrx_ai.orchestrator.requests import AIMatrixRequest
    from matrx_ai.providers.unified_client import UnifiedAIClient
    config = UnifiedConfig(model="mock-model", messages=MessageList(_messages=[UnifiedMessage(role="user", content=[TextContent(text="hi")])]),
        metadata={"mock": {"latency_ms":1,"ttft_ms":0,"chunks":1,"mode":"text","text":"hello"}})
    req = AIMatrixRequest(conversation_id=conversation_id, config=config, request_id=request_id)
    c = await execute_until_complete(req, UnifiedAIClient())
    print("TRIG", c.trigger_message_position, c.result_start_position, c.result_end_position)
    for i,m in enumerate(c.request.config.messages.to_list()) if hasattr(c.request.config.messages,'to_list') else []:
        print("MSG", i, m)
