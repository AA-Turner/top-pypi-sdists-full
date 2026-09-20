from __future__ import annotations

from contextlib import asynccontextmanager

import grpc
import pytest
import xai_sdk
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context
from matrx_connect.emitters import SilentEmitter
from xai_sdk.proto import chat_pb2, chat_pb2_grpc, usage_pb2

from matrx_ai.config import TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.providers.unified_client import UnifiedAIClient
from matrx_ai.providers.xai.xai_api import XAIChat
from matrx_ai.testing.profile_factory import make_profile


@pytest.mark.asyncio
@pytest.mark.parametrize("stream", [False, True])
async def test_xai_dispatch_through_real_sdk_to_local_grpc(monkeypatch, stream):
    received = []
    usage = usage_pb2.SamplingUsage(prompt_tokens=2, completion_tokens=1, total_tokens=3)

    class ChatService(chat_pb2_grpc.ChatServicer):
        async def GetCompletion(self, request, context):
            received.append(request)
            return chat_pb2.GetChatCompletionResponse(
                id="local-response",
                model=request.model,
                outputs=[
                    chat_pb2.CompletionOutput(
                        index=0,
                        finish_reason="REASON_STOP",
                        message=chat_pb2.CompletionMessage(
                            content="local success", role="ROLE_ASSISTANT"
                        ),
                    )
                ],
                usage=usage,
            )

        async def GetCompletionChunk(self, request, context):
            received.append(request)
            yield chat_pb2.GetChatCompletionChunk(
                id="local-response",
                model=request.model,
                outputs=[
                    chat_pb2.CompletionOutputChunk(
                        index=0,
                        finish_reason="REASON_STOP",
                        delta=chat_pb2.Delta(content="local success", role="ROLE_ASSISTANT"),
                    )
                ],
                usage=usage,
            )

    @asynccontextmanager
    async def admit(profile):
        yield

    server = grpc.aio.server()
    chat_pb2_grpc.add_ChatServicer_to_server(ChatService(), server)
    port = server.add_insecure_port("127.0.0.1:0")
    await server.start()
    real_client = xai_sdk.AsyncClient
    monkeypatch.setattr(
        xai_sdk,
        "AsyncClient",
        lambda api_key: real_client(
            api_key=api_key,
            api_host=f"127.0.0.1:{port}",
            use_insecure_channel=True,
            timeout=5,
        ),
    )
    monkeypatch.setattr("matrx_ai.providers.keys.resolve_api_key", lambda *a, **kw: "local-test")
    monkeypatch.setattr("matrx_ai.providers.admission.admit_provider_call", admit)
    provider = XAIChat()
    token = set_app_context(AppContext(emitter=SilentEmitter()))
    profile = make_profile(model_name="local-grok", wire_format="xai_chat")
    config = UnifiedConfig(
        model="local-grok",
        stream=stream,
        messages=[UnifiedMessage(role="user", content=[TextContent(text="hello")])],
    )
    try:
        result = await UnifiedAIClient._dispatch_with_billing_net(
            lambda: provider.execute(config, profile),
            profile=profile,
            provider_client=provider,
        )
        assert len(received) == 1
        assert received[0].model == "local-grok"
        assert result.messages[0].content[0].text == "local success"
        assert result.usage.output_tokens == 1
    finally:
        clear_app_context(token)
        try:
            await provider.client.close()
        finally:
            await server.stop(None)
