import asyncio
from typing import Literal

import pydantic

import mistralai.workflows as workflows
from mistralai.workflows import workflow
from mistralai.workflows.core.logging import Env, LogFormat, LogLevel, setup_logging

with workflow.unsafe.imports_passed_through():
    import structlog

logger = structlog.getLogger(__name__)


class AppConfig(pydantic.BaseModel):
    env: Env = Env.DEV
    temporal_server_url: str = "localhost:7233"
    temporal_namespace: str = "default"
    log_format: str = "console"
    log_level: str = "DEBUG"
    app_version: str = "local_test"


class Message(pydantic.BaseModel):
    role: Literal["user", "assistant"]
    content: str


class EmptyModel(pydantic.BaseModel):
    pass


class TestMessages:
    responses = [
        Message(
            role="assistant",
            content="Hi there! How can I help you?",
        ),
        Message(
            role="assistant",
            content="I'm just a bot, but I'm doing great! How about you?",
        ),
    ]


# --- Activities ---
@workflows.activity()
async def fetch_chatbot_response_activity(index: int) -> Message:
    if index < len(TestMessages.responses):
        return TestMessages.responses[index]
    return Message(role="assistant", content="I'm sorry, I don't understand.")


# --- Workflow ---
@workflows.workflow.define(
    name="simple-chatbot-workflow",
    workflow_description="A simple chatbot with predefined answers.",
)
class SimpleChatbotWorkflow:
    def __init__(self) -> None:
        self.messages: list[Message] = []
        self._action_occurred: bool = False
        self._index: int = 0
        self._continue = True
        logger.debug("Workflow initialized.")

    async def _run_impl(self) -> None:
        while self._continue:
            logger.debug("Waiting for user message...")
            await workflows.workflow.wait_condition(lambda: self._action_occurred)
            self._action_occurred = False

    @workflows.workflow.entrypoint
    async def run(self) -> None:
        await self._run_impl()

    async def _update_response_update_impl(self, message: Message) -> Message:
        self.messages.append(message)
        assistant_message = await fetch_chatbot_response_activity(self._index)
        self.messages.append(assistant_message)
        self._index += 1
        self._action_occurred = True
        return assistant_message

    @workflows.workflow.update(name="discuss", description="Discuss with the chatbot.")
    async def update_response_update(self, message: Message) -> Message:
        return await self._update_response_update_impl(message)

    async def _stop_impl(self) -> None:
        logger.debug("Stopping workflow...")
        self._continue = False
        self._action_occurred = True

    @workflows.workflow.signal(name="stop_discussion", description="Stop the workflow.")
    async def stop(self) -> None:
        await self._stop_impl()


# --- Main for local worker (optional, good for quick testing) ---
if __name__ == "__main__":
    app_cfg = AppConfig()
    setup_logging(
        log_format=LogFormat(app_cfg.log_format),
        log_level=LogLevel(app_cfg.log_level),
        app_version=app_cfg.app_version,
    )
    asyncio.run(workflows.run_worker(workflows=[SimpleChatbotWorkflow]))
