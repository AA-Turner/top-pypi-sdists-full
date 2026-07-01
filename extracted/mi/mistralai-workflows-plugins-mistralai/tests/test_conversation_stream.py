from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from dataclasses import dataclass
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from mistralai.client import models as mistralai_models
from mistralai.client.models.completionresponsestreamchoice import CompletionResponseStreamChoice
from mistralai.client.models.deltamessage import DeltaMessage
from mistralai.client.models.toolcall import ToolCall as DeltaToolCall
from mistralai.client.utils import eventstreaming


@dataclass
class _Chunk:
    data: object


class _FakeEventStream:
    """Mimics the iterable/context-manager surface of EventStreamAsync."""

    def __init__(self, chunks: list[_Chunk]) -> None:
        self._chunks = chunks
        self._index = 0

    async def __aenter__(self) -> "_FakeEventStream":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        pass

    def __aiter__(self) -> "_FakeEventStream":
        return self

    async def __anext__(self) -> _Chunk:
        if self._index >= len(self._chunks):
            raise StopAsyncIteration
        chunk = self._chunks[self._index]
        self._index += 1
        return chunk


def _function_call_chunk(
    output_index: int = 0,
    tool_call_id: str | None = None,
    name: str | None = None,
    arguments: str | None = None,
    id: str | None = None,
) -> _Chunk:
    return _Chunk(
        data=mistralai_models.FunctionCallEvent.model_construct(
            output_index=output_index,
            tool_call_id=tool_call_id,
            name=name,
            arguments=arguments,
            id=id or "",
            type="function.call.delta",
        )
    )


def _tool_execution_chunk(
    output_index: int = 0,
    name: str | None = None,
    arguments: str | None = None,
    id: str | None = None,
) -> _Chunk:
    return _Chunk(
        data=mistralai_models.ToolExecutionDeltaEvent.model_construct(
            output_index=output_index,
            name=name,
            arguments=arguments,
            id=id,
            type="tool.execution.delta",
        )
    )


def _tool_execution_done_chunk(output_index: int = 0) -> _Chunk:
    return _Chunk(
        data=mistralai_models.ToolExecutionDoneEvent.model_construct(
            output_index=output_index,
            id="",
            name="",
            type="tool.execution.done",
        )
    )


def _response_started_chunk(conversation_id: str = "conv-1") -> _Chunk:
    return _Chunk(
        data=mistralai_models.ResponseStartedEvent.model_construct(
            conversation_id=conversation_id,
            type="conversation.response.started",
            created_at=0,
        )
    )


def _mock_task_cls():
    """Returns a class that mimics Task as a no-op async context manager."""

    class _FakeTask:
        def __class_getitem__(cls, item):
            return cls

        def __init__(self, **kwargs):
            pass

        async def __aenter__(self):
            mock = MagicMock()
            mock.set_state = AsyncMock()
            return mock

        async def __aexit__(self, *args):
            pass

    return _FakeTask


def _chat_completion_chunk(content: str | list[mistralai_models.ContentChunk]) -> _Chunk:
    delta = DeltaMessage.model_construct(
        role="assistant",
        content=content,
    )
    choice = CompletionResponseStreamChoice.model_construct(
        index=0,
        delta=delta,
        finish_reason=None,
    )
    return _Chunk(
        data=mistralai_models.CompletionEvent.model_construct(
            data=mistralai_models.CompletionChunk.model_construct(
                id="cmpl-1",
                model="test-model",
                choices=[choice],
            )
        ).data
    )


def _response_done_chunk() -> _Chunk:
    return _Chunk(
        data=mistralai_models.ResponseDoneEvent.model_construct(
            type="conversation.response.done",
            created_at=0,
            usage=None,
        )
    )


class _FiniteSseResponse:
    def __init__(self) -> None:
        self.closed = False

    async def aiter_bytes(self) -> AsyncIterator[bytes]:
        yield b"data: {}\n\n"

    async def aclose(self) -> None:
        self.closed = True


class _HangingSseResponse:
    def __init__(self) -> None:
        self.closed = False
        self.started = asyncio.Event()

    async def aiter_bytes(self) -> AsyncIterator[bytes]:
        self.started.set()
        await asyncio.Event().wait()
        yield b""

    async def aclose(self) -> None:
        self.closed = True


@pytest.mark.asyncio
class TestStreamLifecycle:
    """Tests that generated SDK streams are closed by the plugin helpers."""

    async def test_conversation_stream_closes_sdk_response_after_completion(self) -> None:
        response = _FiniteSseResponse()
        stream = eventstreaming.EventStreamAsync(response, lambda _: _response_done_chunk())

        with patch("mistralai.workflows.plugins.mistralai.utils.Task", _mock_task_cls()):
            from mistralai.workflows.plugins.mistralai.utils import handle_conversation_stream

            await handle_conversation_stream(stream)  # type: ignore[arg-type]

        assert response.closed is True

    async def test_chat_stream_closes_sdk_response_after_completion(self) -> None:
        response = _FiniteSseResponse()
        stream = eventstreaming.EventStreamAsync(response, lambda _: _chat_completion_chunk("Hello"))

        with patch("mistralai.workflows.plugins.mistralai.utils.Task", _mock_task_cls()):
            from mistralai.workflows.plugins.mistralai.utils import handle_chat_stream

            result = await handle_chat_stream(stream)  # type: ignore[arg-type]

        assert result.content == "Hello"
        assert response.closed is True

    async def test_chat_stream_closes_sdk_response_when_cancelled_during_pending_read(self) -> None:
        response = _HangingSseResponse()
        stream = eventstreaming.EventStreamAsync(response, lambda _: _chat_completion_chunk("Hello"))

        with patch("mistralai.workflows.plugins.mistralai.utils.Task", _mock_task_cls()):
            from mistralai.workflows.plugins.mistralai.utils import handle_chat_stream

            task = asyncio.create_task(handle_chat_stream(stream))  # type: ignore[arg-type]
            await response.started.wait()
            task.cancel()

            with pytest.raises(asyncio.CancelledError):
                await task

        assert response.closed is True


@pytest.mark.asyncio
class TestFunctionCallEventStreaming:
    """Tests that FunctionCallEvent arguments are correctly accumulated."""

    async def test_first_chunk_args_preserved(self) -> None:
        """First chunk carries partial args + subsequent chunks carry rest -> all concatenated."""
        chunks = [
            _response_started_chunk(),
            _function_call_chunk(name="my_tool", tool_call_id="tc-1", arguments='{"enabled'),
            _function_call_chunk(arguments='": true}'),
            _response_done_chunk(),
        ]
        stream = _FakeEventStream(chunks)

        with patch("mistralai.workflows.plugins.mistralai.utils.Task", _mock_task_cls()):
            from mistralai.workflows.plugins.mistralai.utils import handle_conversation_stream

            result = await handle_conversation_stream(stream)  # type: ignore[arg-type]

        fc_outputs = [o for o in (result.outputs or []) if isinstance(o, mistralai_models.FunctionCallEntry)]
        assert len(fc_outputs) == 1
        assert fc_outputs[0].arguments == '{"enabled": true}'

    async def test_single_chunk_full_args(self) -> None:
        """Single chunk with all args -> preserved in full."""
        chunks = [
            _response_started_chunk(),
            _function_call_chunk(name="my_tool", tool_call_id="tc-1", arguments='{"key": "value"}'),
            _response_done_chunk(),
        ]
        stream = _FakeEventStream(chunks)

        with patch("mistralai.workflows.plugins.mistralai.utils.Task", _mock_task_cls()):
            from mistralai.workflows.plugins.mistralai.utils import handle_conversation_stream

            result = await handle_conversation_stream(stream)  # type: ignore[arg-type]

        fc_outputs = [o for o in (result.outputs or []) if isinstance(o, mistralai_models.FunctionCallEntry)]
        assert len(fc_outputs) == 1
        assert fc_outputs[0].arguments == '{"key": "value"}'

    async def test_first_chunk_empty_args(self) -> None:
        """First chunk has empty args + subsequent chunks have args -> works (regression guard)."""
        chunks = [
            _response_started_chunk(),
            _function_call_chunk(name="my_tool", tool_call_id="tc-1", arguments=""),
            _function_call_chunk(arguments='{"enabled": true}'),
            _response_done_chunk(),
        ]
        stream = _FakeEventStream(chunks)

        with patch("mistralai.workflows.plugins.mistralai.utils.Task", _mock_task_cls()):
            from mistralai.workflows.plugins.mistralai.utils import handle_conversation_stream

            result = await handle_conversation_stream(stream)  # type: ignore[arg-type]

        fc_outputs = [o for o in (result.outputs or []) if isinstance(o, mistralai_models.FunctionCallEntry)]
        assert len(fc_outputs) == 1
        assert fc_outputs[0].arguments == '{"enabled": true}'


@pytest.mark.asyncio
class TestToolExecutionDeltaEventStreaming:
    """Tests that ToolExecutionDeltaEvent arguments are correctly accumulated."""

    async def test_first_chunk_args_preserved(self) -> None:
        """First chunk carries partial args + subsequent chunks carry rest -> all concatenated."""
        chunks = [
            _response_started_chunk(),
            _tool_execution_chunk(name="web_search", id="te-1", arguments='{"enabled'),
            _tool_execution_chunk(arguments='": true}'),
            _tool_execution_done_chunk(),
            _response_done_chunk(),
        ]
        stream = _FakeEventStream(chunks)

        with patch("mistralai.workflows.plugins.mistralai.utils.Task", _mock_task_cls()):
            from mistralai.workflows.plugins.mistralai.utils import handle_conversation_stream

            result = await handle_conversation_stream(stream)  # type: ignore[arg-type]

        te_outputs = [o for o in (result.outputs or []) if isinstance(o, mistralai_models.ToolExecutionEntry)]
        assert len(te_outputs) == 1
        assert te_outputs[0].arguments == '{"enabled": true}'

    async def test_single_chunk_full_args(self) -> None:
        """Single chunk with all args -> preserved in full."""
        chunks = [
            _response_started_chunk(),
            _tool_execution_chunk(name="web_search", id="te-1", arguments='{"key": "value"}'),
            _tool_execution_done_chunk(),
            _response_done_chunk(),
        ]
        stream = _FakeEventStream(chunks)

        with patch("mistralai.workflows.plugins.mistralai.utils.Task", _mock_task_cls()):
            from mistralai.workflows.plugins.mistralai.utils import handle_conversation_stream

            result = await handle_conversation_stream(stream)  # type: ignore[arg-type]

        te_outputs = [o for o in (result.outputs or []) if isinstance(o, mistralai_models.ToolExecutionEntry)]
        assert len(te_outputs) == 1
        assert te_outputs[0].arguments == '{"key": "value"}'

    async def test_first_chunk_empty_args(self) -> None:
        """First chunk has empty args + subsequent chunks have args -> works (regression guard)."""
        chunks = [
            _response_started_chunk(),
            _tool_execution_chunk(name="web_search", id="te-1", arguments=""),
            _tool_execution_chunk(arguments='{"enabled": true}'),
            _tool_execution_done_chunk(),
            _response_done_chunk(),
        ]
        stream = _FakeEventStream(chunks)

        with patch("mistralai.workflows.plugins.mistralai.utils.Task", _mock_task_cls()):
            from mistralai.workflows.plugins.mistralai.utils import handle_conversation_stream

            result = await handle_conversation_stream(stream)  # type: ignore[arg-type]

        te_outputs = [o for o in (result.outputs or []) if isinstance(o, mistralai_models.ToolExecutionEntry)]
        assert len(te_outputs) == 1
        assert te_outputs[0].arguments == '{"enabled": true}'


@pytest.mark.asyncio
class TestListContentDeltaChatStream:
    """Tests that list-type content deltas in chat completions are handled correctly."""

    async def test_text_chunk_in_list_extracted(self) -> None:
        """TextChunk items in a list-type delta should be extracted and appended to content."""
        text_chunk = mistralai_models.TextChunk.model_construct(text="Hello", type="text")
        chunks = [
            _chat_completion_chunk([text_chunk]),
            _chat_completion_chunk("! How can I help?"),
        ]
        stream = _FakeEventStream(chunks)

        with patch("mistralai.workflows.plugins.mistralai.utils.Task", _mock_task_cls()):
            from mistralai.workflows.plugins.mistralai.utils import handle_chat_stream

            result = await handle_chat_stream(stream)  # type: ignore[arg-type]

        assert result.content == "Hello! How can I help?"

    async def test_think_chunk_ignored_text_chunk_extracted(self) -> None:
        """ThinkChunk items should be skipped while TextChunk items are extracted."""
        think_chunk = mistralai_models.ThinkChunk.model_construct(
            thinking=[mistralai_models.TextChunk.model_construct(text="reasoning...", type="text")],
            type="thinking",
        )
        text_chunk = mistralai_models.TextChunk.model_construct(text="Hello", type="text")
        chunks = [
            _chat_completion_chunk([think_chunk, text_chunk]),
            _chat_completion_chunk(" world"),
        ]
        stream = _FakeEventStream(chunks)

        with patch("mistralai.workflows.plugins.mistralai.utils.Task", _mock_task_cls()):
            from mistralai.workflows.plugins.mistralai.utils import handle_chat_stream

            result = await handle_chat_stream(stream)  # type: ignore[arg-type]

        assert result.content == "Hello world"


def _message_output_chunk(content: str | mistralai_models.TextChunk) -> _Chunk:
    return _Chunk(
        data=mistralai_models.MessageOutputEvent.model_construct(
            id="msg-1",
            content=content,
            type="message.output.delta",
            created_at=0,
            output_index=0,
            role="assistant",
        )
    )


def _chat_completion_chunk_with_tool_call(
    tool_calls: list[DeltaToolCall],
    content: str | None = None,
) -> _Chunk:
    delta = DeltaMessage.model_construct(
        role="assistant",
        content=content,
        tool_calls=tool_calls,
    )
    choice = CompletionResponseStreamChoice.model_construct(
        index=0,
        delta=delta,
        finish_reason=None,
    )
    return _Chunk(
        data=mistralai_models.CompletionEvent.model_construct(
            data=mistralai_models.CompletionChunk.model_construct(
                id="cmpl-1",
                model="test-model",
                choices=[choice],
            )
        ).data
    )


@pytest.mark.asyncio
class TestTextChunkContentConversationStream:
    """Tests that TextChunk-type content deltas in conversation stream are handled correctly."""

    async def test_text_chunk_content_extracted(self) -> None:
        text_chunk = mistralai_models.TextChunk.model_construct(text="Hello", type="text")
        chunks = [
            _response_started_chunk(),
            _message_output_chunk(text_chunk),
            _message_output_chunk(" world"),
            _response_done_chunk(),
        ]
        stream = _FakeEventStream(chunks)

        with patch("mistralai.workflows.plugins.mistralai.utils.Task", _mock_task_cls()):
            from mistralai.workflows.plugins.mistralai.utils import handle_conversation_stream

            result = await handle_conversation_stream(stream)  # type: ignore[arg-type]

        msg_outputs = [o for o in (result.outputs or []) if isinstance(o, mistralai_models.MessageOutputEntry)]
        assert len(msg_outputs) == 1
        assert msg_outputs[0].content == "Hello world"


@pytest.mark.asyncio
class TestFunctionCallNameOverwrite:
    """Tests that subsequent deltas don't overwrite an already-set function name."""

    async def test_garbage_name_ignored_on_subsequent_delta(self) -> None:
        chunks = [
            _response_started_chunk(),
            _function_call_chunk(name="get_order_status", tool_call_id="tc-1", arguments='{"order'),
            _function_call_chunk(name="Handoff to shipment-ops-agent", arguments='_id": "123"}'),
            _response_done_chunk(),
        ]
        stream = _FakeEventStream(chunks)

        with patch("mistralai.workflows.plugins.mistralai.utils.Task", _mock_task_cls()):
            from mistralai.workflows.plugins.mistralai.utils import handle_conversation_stream

            result = await handle_conversation_stream(stream)  # type: ignore[arg-type]

        fc_outputs = [o for o in (result.outputs or []) if isinstance(o, mistralai_models.FunctionCallEntry)]
        assert len(fc_outputs) == 1
        assert fc_outputs[0].name == "get_order_status"
        assert fc_outputs[0].arguments == '{"order_id": "123"}'


@pytest.mark.asyncio
class TestToolExecutionNameOverwrite:
    """Tests that subsequent deltas don't overwrite an already-set tool execution name."""

    async def test_garbage_name_ignored_on_subsequent_delta(self) -> None:
        chunks = [
            _response_started_chunk(),
            _tool_execution_chunk(name="web_search", id="te-1", arguments='{"query'),
            _tool_execution_chunk(name="You can search for...", arguments='": "test"}'),
            _tool_execution_done_chunk(),
            _response_done_chunk(),
        ]
        stream = _FakeEventStream(chunks)

        with patch("mistralai.workflows.plugins.mistralai.utils.Task", _mock_task_cls()):
            from mistralai.workflows.plugins.mistralai.utils import handle_conversation_stream

            result = await handle_conversation_stream(stream)  # type: ignore[arg-type]

        te_outputs = [o for o in (result.outputs or []) if isinstance(o, mistralai_models.ToolExecutionEntry)]
        assert len(te_outputs) == 1
        assert te_outputs[0].name == "web_search"
        assert te_outputs[0].arguments == '{"query": "test"}'


@pytest.mark.asyncio
class TestChatStreamToolCallNameOverwrite:
    """Tests that handle_chat_stream doesn't overwrite function names on subsequent deltas."""

    async def test_garbage_name_ignored_on_subsequent_delta(self) -> None:
        tc_first = DeltaToolCall.model_construct(
            id="tc-1",
            type="function",
            index=0,
            function=mistralai_models.FunctionCall.model_construct(
                name="get_order_status",
                arguments='{"order',
            ),
        )
        tc_second = DeltaToolCall.model_construct(
            id="tc-1",
            type="function",
            index=0,
            function=mistralai_models.FunctionCall.model_construct(
                name="Handoff to shipment-ops-agent",
                arguments='_id": "123"}',
            ),
        )
        chunks = [
            _chat_completion_chunk_with_tool_call([tc_first]),
            _chat_completion_chunk_with_tool_call([tc_second]),
        ]
        stream = _FakeEventStream(chunks)

        with patch("mistralai.workflows.plugins.mistralai.utils.Task", _mock_task_cls()):
            from mistralai.workflows.plugins.mistralai.utils import handle_chat_stream

            result = await handle_chat_stream(stream)  # type: ignore[arg-type]

        assert result.tool_calls is not None
        assert len(result.tool_calls) == 1
        assert result.tool_calls[0].function.name == "get_order_status"
        assert result.tool_calls[0].function.arguments == '{"order_id": "123"}'
