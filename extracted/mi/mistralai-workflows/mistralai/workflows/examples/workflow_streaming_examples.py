import asyncio
from typing import AsyncGenerator, List

import temporalio.activity
from pydantic import BaseModel, Field

import mistralai.workflows as workflows
from mistralai.workflows import workflow
from mistralai.workflows.core.task import Task

with workflow.unsafe.imports_passed_through():
    import structlog

logger = structlog.get_logger()


class StreamingParams(BaseModel):
    text: str = Field(description="Text to process")
    model: str = Field(description="Model to use", default="test-model")
    items: List[str] = Field(description="List of items to process", default_factory=list)


class StreamingResult(BaseModel):
    processed_text: str = Field(description="Processed text result")
    token_count: int = Field(description="Number of tokens processed")
    items_processed: int = Field(description="Number of items processed", default=0)


class TokenStreamState(BaseModel):
    """State for tracking token streaming progress."""

    tokens: List[str] = Field(default_factory=list)
    current_token: str = ""


async def simulate_llm_token_generator(text: str) -> AsyncGenerator[str, None]:
    """Simulate an LLM token generator"""
    words = text.split()
    for word in words:
        await asyncio.sleep(0.05)  # Simulate streaming delay
        yield word


@workflows.activity()
async def streaming_tokens_activity(params: StreamingParams) -> StreamingResult:
    """
    Example of streaming tokens from a generator using Task API.

    This pattern uses Task to emit lifecycle events and stream progress updates.
    """
    initial_state = TokenStreamState()

    async with Task[TokenStreamState](type="token-stream", state=initial_state) as task:
        state = task.state
        assert state is not None
        async for token in simulate_llm_token_generator(params.text):
            await task.update_state({"tokens": state.tokens + [token], "current_token": token})
            state = task.state
            assert state is not None

    final_state = task.state
    assert final_state is not None
    processed_text = " ".join(final_state.tokens)
    return StreamingResult(processed_text=processed_text, token_count=len(final_state.tokens))


class ProgressState(BaseModel):
    """State for tracking processing progress."""

    processed_words: List[str] = Field(default_factory=list)
    progress_idx: int = 0
    progress_total: int = 0


@workflows.activity()
async def streaming_tokens_with_progress_activity(params: StreamingParams) -> StreamingResult:
    """
    Example of explicit progress tracking with Task API.

    This pattern gives you full control over state updates and progress tracking.
    """
    words = params.text.split()
    initial_state = ProgressState(progress_total=len(words))

    async with Task[ProgressState](type="progress-stream", state=initial_state) as task:
        state = task.state
        assert state is not None
        for i, word in enumerate(words):
            await task.update_state(
                {
                    "processed_words": state.processed_words + [word],
                    "progress_idx": i + 1,
                }
            )
            state = task.state
            assert state is not None
            await asyncio.sleep(0.1)

    final_state = task.state
    assert final_state is not None
    return StreamingResult(processed_text=" ".join(final_state.processed_words), token_count=len(words))


@workflows.activity(retry_policy_max_attempts=3, retry_policy_backoff_coefficient=1)
async def streaming_with_retry_activity(params: StreamingParams) -> StreamingResult:
    """Activity that fails on first two attempts then succeeds."""
    attempt = temporalio.activity.info().attempt

    tokens = list(params.text)

    if attempt <= 2:
        logger.info("Will fail", attempt=attempt)
        raise ValueError(f"Simulated failure on attempt {attempt}")

    logger.info("Will succeed", attempt=attempt)
    return StreamingResult(processed_text=" ".join(tokens), token_count=len(tokens))


@workflows.workflow.define(
    name="streaming-tokens-example", workflow_description="Example workflow for streaming tokens"
)
class StreamingTokensWorkflow:
    @workflows.workflow.entrypoint
    async def run(self, params: StreamingParams) -> StreamingResult:
        return await streaming_tokens_activity(params)


@workflows.workflow.define(
    name="streaming-tokens-with-progress-example",
    workflow_description="Example workflow using streaming tokens with progress",
)
class StreamingTokensWithProgressWorkflow:
    @workflows.workflow.entrypoint
    async def run(self, params: StreamingParams) -> StreamingResult:
        return await streaming_tokens_with_progress_activity(params)


@workflows.workflow.define(
    name="streaming-with-retry-example",
    workflow_description="Example workflow using streaming with retry",
)
class StreamingWithRetryWorkflow:
    @workflows.workflow.entrypoint
    async def run(self, params: StreamingParams) -> StreamingResult:
        return await streaming_with_retry_activity(params)


class SignalStreamingParams(BaseModel):
    max_signals: int = Field(default=3, description="Maximum signals to process before auto-completing")


class SignalStreamingResult(BaseModel):
    signals_received: int = Field(description="Number of signals processed")
    messages: List[str] = Field(description="Processed messages")


class SignalTaskState(BaseModel):
    status: str = "idle"
    message: str = ""


class SimpleChildParams(BaseModel):
    message: str = Field(description="Message to process")


@workflows.activity()
async def process_signal_activity(message: str) -> str:
    """Activity that emits CUSTOM_TASK events via Task API when processing a signal."""
    async with Task[SignalTaskState](type="signal-task", state=SignalTaskState()) as task:
        await task.update_state({"status": "processing", "message": message})
        await asyncio.sleep(0.05)
    return f"Processed: {message}"


@workflows.workflow.define(
    name="simple-child-workflow",
    workflow_description="Simple child workflow for testing sub-workflow streaming",
)
class SimpleChildWorkflow:
    """A simple child workflow that just processes a message."""

    @workflows.workflow.entrypoint
    async def run(self, params: SimpleChildParams) -> str:
        return f"Child processed: {params.message}"


@workflows.workflow.define(
    name="signal-streaming-workflow",
    workflow_description="Workflow that emits CUSTOM_TASK events when signals are received",
)
class SignalStreamingWorkflow:
    """Simple workflow that emits CUSTOM_TASK events when signals are received.

    Useful for testing live streaming with interactive signal-based control.
    Uses a queue to avoid race conditions when signals arrive during activity execution.
    """

    def __init__(self) -> None:
        self._message_queue: List[str] = []
        self._subworkflow_queue: List[str] = []
        self._done: bool = False
        self._continue_as_new: bool = False

    @workflows.workflow.signal()
    async def send_message(self, message: str) -> None:
        self._message_queue.append(message)

    @workflows.workflow.signal()
    async def trigger_subworkflow(self, message: str) -> None:
        """Signal to trigger a sub-workflow."""
        self._subworkflow_queue.append(message)

    @workflows.workflow.signal()
    async def complete(self) -> None:
        self._done = True

    @workflows.workflow.signal()
    async def trigger_continue_as_new(self) -> None:
        self._continue_as_new = True

    @workflows.workflow.entrypoint
    async def run(self, params: SignalStreamingParams) -> SignalStreamingResult:
        messages: List[str] = []

        while not self._done and len(messages) < params.max_signals:
            await workflows.workflow.wait_condition(
                lambda: (
                    bool(self._message_queue) or bool(self._subworkflow_queue) or self._done or self._continue_as_new
                )
            )

            if self._done:
                break

            if self._continue_as_new:
                workflows.workflow.continue_as_new(params)

            # Process sub-workflow requests first
            if self._subworkflow_queue:
                subworkflow_message = self._subworkflow_queue.pop(0)
                child_result = await workflows.workflow.execute_workflow(
                    SimpleChildWorkflow,
                    SimpleChildParams(message=subworkflow_message),
                )
                messages.append(child_result)

            # Process regular messages
            elif self._message_queue:
                message = self._message_queue.pop(0)
                result = await process_signal_activity(message)
                messages.append(result)

        return SignalStreamingResult(signals_received=len(messages), messages=messages)
