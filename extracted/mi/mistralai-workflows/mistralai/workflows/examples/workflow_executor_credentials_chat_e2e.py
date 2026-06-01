from datetime import timedelta

from mistralai.client.models import AssistantMessage, SystemMessage, ToolMessage, UserMessage
from pydantic import BaseModel

import mistralai.workflows as workflows
from mistralai.workflows.client import get_mistral_client


class ExecutorCredentialsChatResult(BaseModel):
    response_content: str


@workflows.activity(start_to_close_timeout=timedelta(minutes=2))
async def chat_with_executor_credentials() -> ExecutorCredentialsChatResult:
    client = get_mistral_client(use_executor_credentials=True)
    messages: list[AssistantMessage | SystemMessage | ToolMessage | UserMessage] = [
        UserMessage(content="Reply with exactly: hello"),
    ]
    response = await client.chat.complete_async(
        model="mistral-small-latest",
        messages=messages,
    )
    assert response is not None
    message = response.choices[0].message
    assert message is not None
    content = message.content
    assert isinstance(content, str)
    return ExecutorCredentialsChatResult(response_content=content)


@workflows.workflow.define(
    name="example-executor-credentials-chat-e2e-workflow",
    workflow_description="E2E test: chat completion using executor credentials (staging/prod only)",
    on_behalf_of=True,
)
class ExecutorCredentialsChatE2EWorkflow:
    @workflows.workflow.entrypoint
    async def run(self) -> ExecutorCredentialsChatResult:
        return await chat_with_executor_credentials()
