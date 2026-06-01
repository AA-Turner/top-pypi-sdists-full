"""
OLD Multi-Turn Chat Workflow Example

This file contains the OLD implementation using workflows.streaming.stream() API.
It is kept for reference to show the old way of coding things.

The new approach uses the Task API from workflows.worker.task instead.

DO NOT USE THIS CODE - it relies on deprecated streaming APIs.

---

OLD CODE (kept for reference):

```python
# 5,707 characters
# we keep it for later comparison with the new DX improvements
import asyncio
import os
from itertools import count
from typing import Any, Literal

from mistralai.client import Mistral
from mistralai.client import models as mistralai_models
from pydantic import BaseModel

import mistralai.workflows as workflows


class LeChatPayloadWorking(BaseModel):
    type: Literal["working"] = "working"
    name: str


class LeChatPayloadUserMessage(mistralai_models.UserMessage):
    type: Literal["user_message"] = "user_message"


class LeChatPayloadAssistantMessage(mistralai_models.AssistantMessage):
    type: Literal["assistant_message"] = "assistant_message"


class LeChatPayloadHumanFeedback(BaseModel):
    type: Literal["human_feedback"] = "human_feedback"
    input_schema: dict
    input: Any | None = None


class SimplifiedLeChatPayloadUserMessageInput(BaseModel):
    content: str


class WaitUserInputUpdateParams(BaseModel):
    custom_task_id: str
    input: Any


class WaitUserInputUpdateResult(BaseModel):
    error: str | None = None


class UserInputRequest(BaseModel):
    custom_task_id: str
    input_schema: type[BaseModel]
    received: bool = False
    input: Any | None = None


class WorkflowParams(LeChatPayloadUserMessage):
    model: str = "mistral-medium-2508"


@workflows.workflow.define(
    name="multi_turn_chat_workflow",
    workflow_description="Multi-turn chat workflow using Mistral AI",
)
class MultiTurnChatWorkflow:
    def __init__(self) -> None:
        self._user_input_requests: dict[str, UserInputRequest] = {}

    @workflows.workflow.entrypoint
    async def run(self, params: WorkflowParams) -> None:
        initial_message = LeChatPayloadUserMessage(content=params.content)

        messages: list[mistralai_models.ChatCompletionRequestMessage] = []
        with workflows.streaming.stream("working") as stream:
            for i in count():
                stream.publish(LeChatPayloadWorking(name=f"Waiting for user input ({i + 1} steps)"))
                if i > 0:
                    with workflows.streaming.stream("human_feedback") as feedback_stream:
                        feedback_stream.publish(
                            LeChatPayloadHumanFeedback(
                                input_schema=SimplifiedLeChatPayloadUserMessageInput.model_json_schema()
                            )
                        )
                        self._user_input_requests[feedback_stream.custom_task_id] = UserInputRequest(
                            custom_task_id=feedback_stream.custom_task_id,
                            input_schema=SimplifiedLeChatPayloadUserMessageInput,
                        )
                        await workflows.workflow.wait_condition(
                            lambda task_id=feedback_stream.custom_task_id: bool(  # type: ignore[misc]
                                self._user_input_requests[task_id].received
                            )
                        )
                        user_input_message = SimplifiedLeChatPayloadUserMessageInput.model_validate(
                            self._user_input_requests[feedback_stream.custom_task_id].input
                        )
                        user_message = LeChatPayloadUserMessage(content=user_input_message.content)
                        feedback_stream.publish(
                            LeChatPayloadHumanFeedback(
                                input_schema=SimplifiedLeChatPayloadUserMessageInput.model_json_schema(),
                                input=user_message,
                            )
                        )
                else:
                    user_message = initial_message

                stream.publish(LeChatPayloadWorking(name=f"Generating assistant response ({i + 1} steps)"))
                messages.append(user_message)
                mistral_assistant_message = await mistral_chat_completion_activity(
                    mistralai_models.ChatCompletionRequest(model=params.model, messages=messages)
                )
                assistant_message: LeChatPayloadAssistantMessage = LeChatPayloadAssistantMessage(
                    content=mistral_assistant_message.content
                )
                messages.append(assistant_message)

    @workflows.workflow.update(name="human_feedback")
    async def human_feedback(self, message: WaitUserInputUpdateParams) -> WaitUserInputUpdateResult:
        user_input_request = self._user_input_requests.get(message.custom_task_id)
        if not user_input_request:
            return WaitUserInputUpdateResult(error=f"Custom task {message.custom_task_id} not found")

        try:
            user_input_request.input_schema.model_validate(message.input)
        except Exception as e:
            return WaitUserInputUpdateResult(error=f"Invalid input: {e}")

        user_input_request.input = message.input
        user_input_request.received = True
        return WaitUserInputUpdateResult()


def get_mistral_client() -> Mistral:
    return Mistral(api_key=os.getenv("MISTRAL_API_KEY"))


@workflows.activity()
async def mistral_chat_completion_activity(
    params: mistralai_models.ChatCompletionRequest,
    mistral_client: Mistral = workflows.Depends(get_mistral_client),
) -> mistralai_models.AssistantMessage:
    assistant_message = mistralai_models.AssistantMessage(content="")
    with workflows.streaming.stream("assistant_message") as stream:
        mistral_stream = await mistral_client.chat.stream_async(
            **params.model_copy(update={"stream": True}).model_dump(by_alias=True)
        )
        async for chunk in mistral_stream.generator:
            if chunk.data.choices[0].delta.content:
                assert isinstance(chunk.data.choices[0].delta.content, str), "Non string content is not supported"
                assert isinstance(assistant_message.content, str), "Non string content is not supported"
                assistant_message.content += chunk.data.choices[0].delta.content
                stream.publish(LeChatPayloadAssistantMessage(content=assistant_message.content))
    return assistant_message


if __name__ == "__main__":
    asyncio.run(workflows.run_worker([MultiTurnChatWorkflow]))
```
"""
