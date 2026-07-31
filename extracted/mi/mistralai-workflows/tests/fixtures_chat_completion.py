from __future__ import annotations

from mistralai.workflows import activity, workflow

_CHAT_RESPONSE = {
    "id": "cmpl-test",
    "object": "chat.completion",
    "created": 1730000000,
    "model": "mistral-small-latest",
    "usage": {"prompt_tokens": 3, "completion_tokens": 2, "total_tokens": 5},
    "choices": [
        {
            "index": 0,
            "message": {"role": "assistant", "content": "hi there"},
            "finish_reason": "stop",
        }
    ],
}


@activity(name="chat_completion")
async def chat_completion_activity() -> str:
    import httpx

    from mistralai.workflows.client import get_mistral_client

    client = get_mistral_client(api_key="test-key", server_url="http://test.local")
    client.sdk_configuration.async_client._transport = httpx.MockTransport(
        lambda _request: httpx.Response(200, json=_CHAT_RESPONSE)
    )

    response = await client.chat.complete_async(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": "hi"}],
    )
    return response.choices[0].message.content


@workflow.define(name="chat_completion_workflow")
class ChatCompletionWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        return await chat_completion_activity()
