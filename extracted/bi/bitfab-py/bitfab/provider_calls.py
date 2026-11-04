from __future__ import annotations

import contextlib
import contextvars
import dataclasses
import functools
import inspect
import json
import sys
import threading
import time
import uuid
import weakref
from collections.abc import AsyncIterator, Awaitable, Callable, Iterator, Mapping
from dataclasses import dataclass, field
from typing import Any

from bitfab import finalizers, subtree
from bitfab.client_patching import (
    NODE_OMITS_CALL,
    NODE_RECORDS_CALL,
    PatchingFinder,
    hand_stream_to_node,
    renamed,
    take_node_ownership,
)

CREATE = "create"
PARSE = "parse"
STREAM = "stream"
GENERATE_CONTENT = "generate_content"
GENERATE_CONTENT_STREAM = "generate_content_stream"
PATCHED_MARKER = "_bitfab_provider_call_patched"
CALL_MARKER = "_bitfab_provider_call"
OPENROUTER_HOSTNAME = "openrouter.ai"
RESPONSE_DONE_EVENTS = frozenset(
    {"response.completed", "response.incomplete", "response.failed"}
)
TRANSCRIPT_DONE_EVENT = "transcript.text.done"
MESSAGE_STREAM_REQUESTS = (
    "_MessageStreamManager__api_request",
    "_AsyncMessageStreamManager__api_request",
)

_LANGCHAIN_CHAT_MODEL_FRAMES = frozenset(
    {"_generate_with_cache", "_agenerate_with_cache", "stream", "astream"}
)

_lock = threading.Lock()
_wrapper_call: contextvars.ContextVar[WrapperCall | None] = contextvars.ContextVar(
    "bitfab_provider_wrapper_call", default=None
)


@dataclass(frozen=True)
class ProviderCall:
    provider: str
    module: str
    classes: tuple[str, ...]
    handles: Callable[[Any], bool]
    is_response: Callable[[Any], bool]
    prompt: Callable[[Mapping[str, Any]], str | None]
    usage: Callable[[Mapping[str, Any], Any], dict[str, Any]]
    method: str = CREATE
    stream_summary: Callable[[list[Any]], Any] | None = None
    always_streams: bool = False
    observe: Callable[[Any, StreamRecording], Any] | None = None


@dataclass
class WrapperCall:
    recorded_responses: list[Any] = field(default_factory=list)

    def recorded(self) -> bool:
        return bool(self.recorded_responses)


@dataclass(frozen=True)
class StreamSpan:
    session: subtree.Session
    span_id: str
    parent_span_id: str
    started_at: str


@dataclass(frozen=True)
class StreamOutcome:
    result: Any
    contexts: list[dict[str, Any]] | None
    prompt: str | None
    error: str | None


@dataclass
class StreamRecording:
    call: ProviderCall
    span_name: str
    request: Mapping[str, Any]
    spans: tuple[StreamSpan, ...]
    started_monotonic: float
    events: list[Any] = field(default_factory=list)
    finished: bool = False
    outcome: StreamOutcome | None = None
    listeners: list[Callable[[StreamOutcome], None]] = field(default_factory=list)
    lock: threading.Lock = field(default_factory=threading.Lock)

    def item(self, event: Any) -> None:
        self.events.append(event)

    def finish(self, error: BaseException | None) -> None:
        with self.lock:
            if self.finished:
                return
            self.finished = True
        try:
            outcome = _stream_outcome(self, error)
        except Exception:
            outcome = StreamOutcome(None, None, None, _error_text(error))
        with contextlib.suppress(Exception), subtree.uncaptured():
            _emit_stream(self, outcome)
        with self.lock:
            self.outcome = outcome
            listeners, self.listeners = self.listeners, []
        for listener in listeners:
            _notify(listener, outcome)

    def when_done(self, listener: Callable[[StreamOutcome], None]) -> None:
        with self.lock:
            if self.outcome is None:
                self.listeners.append(listener)
                return
        _notify(listener, self.outcome)


def _notify(listener: Callable[[StreamOutcome], None], outcome: StreamOutcome) -> None:
    with contextlib.suppress(Exception), subtree.uncaptured():
        listener(outcome)


@contextlib.contextmanager
def wrapper_call() -> Iterator[WrapperCall]:
    call = WrapperCall()
    token = _wrapper_call.set(call)
    try:
        yield call
    finally:
        _wrapper_call.reset(token)


def _mark_recorded(response: Any) -> None:
    call = _wrapper_call.get()
    if call is not None:
        call.recorded_responses.append(response)


def _field(value: Any, key: str) -> Any:
    if value is None:
        return None
    if isinstance(value, Mapping):
        return value.get(key)
    found = getattr(value, key, None)
    if found is not None:
        return found
    extra = getattr(value, "model_extra", None)
    return extra.get(key) if isinstance(extra, dict) else None


def _number(value: Any) -> int | float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return value


def _text(value: Any) -> str | None:
    return value if isinstance(value, str) and value else None


def _as_text(content: Any) -> str:
    return content if isinstance(content, str) else json.dumps(content, default=str)


def _present(values: Mapping[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in values.items() if value is not None}


def _plain(value: Any) -> dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    dump = getattr(value, "model_dump", None)
    if callable(dump):
        with contextlib.suppress(Exception):
            dumped = dump()
            if isinstance(dumped, dict):
                return dumped
    return {}


def _rendered_messages(messages: Any) -> list[dict[str, str]]:
    if not isinstance(messages, (list, tuple)):
        return []
    rendered = []
    for message in messages:
        role = _field(message, "role")
        if isinstance(role, str):
            rendered.append(
                {"role": role, "content": _as_text(_field(message, "content"))}
            )
    return rendered


def _system_message(content: Any) -> list[dict[str, str]]:
    if content is None or content == "" or content == []:
        return []
    return [{"role": "system", "content": _as_text(content)}]


def _user_turns(content: Any) -> list[dict[str, str]]:
    if content is None or content == "" or content == []:
        return []
    if isinstance(content, (list, tuple)) and all(
        isinstance(item, str) for item in content
    ):
        return [{"role": "user", "content": item} for item in content]
    return [{"role": "user", "content": _as_text(content)}]


def _encoded(rendered: list[dict[str, str]]) -> str | None:
    return json.dumps(rendered) if rendered else None


def _sum_tokens(*counts: int | float | None) -> int | float | None:
    present = [count for count in counts if count is not None]
    return sum(present) if present else None


def _last_with(events: list[Any], key: str) -> Any:
    return next(
        (event for event in reversed(events) if _field(event, key) is not None), None
    )


def _is_openrouter_resource(resource: Any) -> bool:
    base_url = getattr(getattr(resource, "_client", None), "base_url", None)
    host = getattr(base_url, "host", None)
    return isinstance(host, str) and (
        host == OPENROUTER_HOSTNAME or host.endswith(f".{OPENROUTER_HOSTNAME}")
    )


def _any_resource(_resource: Any) -> bool:
    return True


def _is_chat_completion(response: Any) -> bool:
    return isinstance(_field(response, "choices"), (list, tuple))


def _chat_completion_prompt(request: Mapping[str, Any]) -> str | None:
    return _encoded(_rendered_messages(request.get("messages")))


def _chat_completion_usage(request: Mapping[str, Any], response: Any) -> dict[str, Any]:
    usage = _field(response, "usage")
    return _present(
        {
            "model": _text(_field(response, "model")) or _text(request.get("model")),
            "upstreamProvider": _text(_field(response, "provider")),
            "inputTokens": _number(_field(usage, "prompt_tokens")),
            "outputTokens": _number(_field(usage, "completion_tokens")),
            "cachedInputTokens": _number(
                _field(_field(usage, "prompt_tokens_details"), "cached_tokens")
            ),
            "reasoningTokens": _number(
                _field(_field(usage, "completion_tokens_details"), "reasoning_tokens")
            ),
            "costUsd": _number(_field(usage, "cost")),
        }
    )


def _chat_stream_summary(chunks: list[Any]) -> Any:
    if not chunks:
        return None
    last = _last_with(chunks, "usage") or chunks[-1]
    assembled = finalizers.openai_chunks(chunks)
    message: dict[str, Any] = {"role": "assistant", "content": assembled["text"]}
    if assembled["tool_calls"]:
        message["tool_calls"] = [
            {"type": "function", "function": tool_call}
            for tool_call in assembled["tool_calls"]
        ]
    return {
        "object": "chat.completion",
        "model": _field(last, "model"),
        "provider": _field(last, "provider"),
        "choices": [
            {
                "index": 0,
                "message": message,
                "finish_reason": assembled["finish_reason"],
            }
        ],
        "usage": _field(last, "usage"),
    }


def _is_embedding_list(response: Any) -> bool:
    return _field(response, "object") == "list" and isinstance(
        _field(response, "data"), (list, tuple)
    )


def _embedding_prompt(request: Mapping[str, Any]) -> str | None:
    return _encoded(_user_turns(request.get("input")))


def _embedding_usage(request: Mapping[str, Any], response: Any) -> dict[str, Any]:
    usage = _field(response, "usage")
    input_tokens = _number(_field(usage, "prompt_tokens"))
    return _present(
        {
            "model": _text(_field(response, "model")) or _text(request.get("model")),
            "upstreamProvider": _text(_field(response, "provider")),
            "inputTokens": input_tokens,
            "outputTokens": 0 if input_tokens is not None else None,
            "costUsd": _number(_field(usage, "cost")),
        }
    )


def _is_transcription(response: Any) -> bool:
    return isinstance(_field(response, "text"), str)


def _transcription_prompt(request: Mapping[str, Any]) -> str | None:
    return _encoded(_user_turns(request.get("prompt")))


def _transcription_usage(request: Mapping[str, Any], response: Any) -> dict[str, Any]:
    usage = _field(response, "usage")
    return _present(
        {
            "model": _text(_field(response, "model")) or _text(request.get("model")),
            "inputTokens": _number(_field(usage, "input_tokens")),
            "outputTokens": _number(_field(usage, "output_tokens")),
            "audioSeconds": _number(_field(usage, "seconds")),
        }
    )


def _transcription_stream_summary(events: list[Any]) -> Any:
    return next(
        (
            event
            for event in reversed(events)
            if _field(event, "type") == TRANSCRIPT_DONE_EVENT
        ),
        None,
    )


def _is_anthropic_message(response: Any) -> bool:
    return _field(response, "type") == "message" and isinstance(
        _field(response, "content"), (list, tuple)
    )


def _anthropic_prompt(request: Mapping[str, Any]) -> str | None:
    return _encoded(
        _system_message(request.get("system"))
        + _rendered_messages(request.get("messages"))
    )


def _anthropic_usage(request: Mapping[str, Any], response: Any) -> dict[str, Any]:
    usage = _field(response, "usage")
    uncached = _number(_field(usage, "input_tokens"))
    cache_read = _number(_field(usage, "cache_read_input_tokens"))
    cache_creation = _number(_field(usage, "cache_creation_input_tokens"))
    return _present(
        {
            "model": _text(_field(response, "model")) or _text(request.get("model")),
            "inputTokens": _sum_tokens(uncached, cache_read, cache_creation),
            "outputTokens": _number(_field(usage, "output_tokens")),
            "cachedInputTokens": cache_read,
        }
    )


def _anthropic_stream_summary(events: list[Any]) -> Any:
    start = next(
        (event for event in events if _field(event, "type") == "message_start"), None
    )
    message = _field(start, "message")
    if message is None:
        return None
    usage = _plain(_field(message, "usage"))
    for event in events:
        if _field(event, "type") == "message_delta":
            usage.update(_present(_plain(_field(event, "usage"))))
    assembled = finalizers.anthropic_events(events)
    return {
        "type": "message",
        "role": "assistant",
        "model": _field(message, "model"),
        "content": [{"type": "text", "text": assembled["text"]}],
        "stop_reason": assembled["stop_reason"],
        "usage": usage,
    }


def _is_openai_response(response: Any) -> bool:
    return _field(response, "object") == "response"


def _openai_responses_prompt(request: Mapping[str, Any]) -> str | None:
    request_input = request.get("input")
    turns = (
        [{"role": "user", "content": request_input}]
        if isinstance(request_input, str)
        else _rendered_messages(request_input)
    )
    return _encoded(_system_message(request.get("instructions")) + turns)


def _openai_responses_usage(
    request: Mapping[str, Any], response: Any
) -> dict[str, Any]:
    usage = _field(response, "usage")
    return _present(
        {
            "model": _text(_field(response, "model")) or _text(request.get("model")),
            "inputTokens": _number(_field(usage, "input_tokens")),
            "outputTokens": _number(_field(usage, "output_tokens")),
            "cachedInputTokens": _number(
                _field(_field(usage, "input_tokens_details"), "cached_tokens")
            ),
            "reasoningTokens": _number(
                _field(_field(usage, "output_tokens_details"), "reasoning_tokens")
            ),
            "costUsd": _number(_field(usage, "cost")),
        }
    )


def _openai_responses_stream_summary(events: list[Any]) -> Any:
    done = next(
        (
            event
            for event in reversed(events)
            if _field(event, "type") in RESPONSE_DONE_EVENTS
        ),
        None,
    )
    return _field(done, "response")


def _is_gemini_response(response: Any) -> bool:
    return _field(response, "usage_metadata") is not None or isinstance(
        _field(response, "candidates"), (list, tuple)
    )


def _gemini_content_text(content: Any) -> str | None:
    if content is None or isinstance(content, str):
        return content
    parts = _field(content, "parts")
    if isinstance(parts, (list, tuple)):
        texts = [_field(part, "text") for part in parts]
        if all(isinstance(text, str) for text in texts):
            return "".join(texts)
    text = _field(content, "text")
    return text if isinstance(text, str) else _as_text(content)


def _gemini_turns(contents: Any) -> list[dict[str, str]]:
    if contents is None:
        return []
    items = contents if isinstance(contents, (list, tuple)) else [contents]
    return [
        {
            "role": _text(_field(item, "role")) or "user",
            "content": _gemini_content_text(item) or "",
        }
        for item in items
    ]


def _gemini_prompt(request: Mapping[str, Any]) -> str | None:
    config = request.get("config")
    system = _gemini_content_text(
        _field(config, "system_instruction") or _field(config, "systemInstruction")
    )
    return _encoded(_system_message(system) + _gemini_turns(request.get("contents")))


def _gemini_model(request: Mapping[str, Any], response: Any) -> str | None:
    model = _text(_field(response, "model_version")) or _text(request.get("model"))
    return model.rsplit("/", 1)[-1] if model else None


def _gemini_usage(request: Mapping[str, Any], response: Any) -> dict[str, Any]:
    usage = _field(response, "usage_metadata")
    thoughts = _number(_field(usage, "thoughts_token_count"))
    return _present(
        {
            "model": _gemini_model(request, response),
            "inputTokens": _sum_tokens(
                _number(_field(usage, "prompt_token_count")),
                _number(_field(usage, "tool_use_prompt_token_count")),
            ),
            "outputTokens": _sum_tokens(
                _number(_field(usage, "candidates_token_count")), thoughts
            ),
            "cachedInputTokens": _number(_field(usage, "cached_content_token_count")),
            "reasoningTokens": thoughts,
        }
    )


def _gemini_chunk_text(chunk: Any) -> str:
    candidates = _field(chunk, "candidates")
    if not isinstance(candidates, (list, tuple)) or not candidates:
        return ""
    return _gemini_content_text(_field(candidates[0], "content")) or ""


def _gemini_stream_summary(chunks: list[Any]) -> Any:
    if not chunks:
        return None
    last = _last_with(chunks, "usage_metadata") or chunks[-1]
    return {
        "model_version": _field(last, "model_version"),
        "text": "".join(_gemini_chunk_text(chunk) for chunk in chunks),
        "usage_metadata": _field(last, "usage_metadata"),
    }


def _observed_iterator(iterator: Any, recording: StreamRecording) -> Iterator[Any]:
    error: BaseException | None = None
    try:
        for item in iterator:
            recording.item(item)
            yield item
    except GeneratorExit:
        raise
    except BaseException as raised:
        error = raised
        raise
    finally:
        recording.finish(error)


async def _observed_async_iterator(
    iterator: Any, recording: StreamRecording
) -> AsyncIterator[Any]:
    error: BaseException | None = None
    try:
        async for item in iterator:
            recording.item(item)
            yield item
    except GeneratorExit:
        raise
    except BaseException as raised:
        error = raised
        raise
    finally:
        recording.finish(error)


def _observed(iterator: Any, recording: StreamRecording) -> Any:
    if hasattr(iterator, "__anext__"):
        return _observed_async_iterator(iterator, recording)
    return _observed_iterator(iterator, recording)


def _finishing_close(close: Callable[[], Any], recording: StreamRecording) -> Any:
    if inspect.iscoroutinefunction(close):

        async def async_close() -> Any:
            try:
                return await close()
            finally:
                recording.finish(None)

        return async_close

    def sync_close() -> Any:
        try:
            return close()
        finally:
            recording.finish(None)

    return sync_close


def observed_stream(stream: Any, recording: StreamRecording) -> Any:
    try:
        if hasattr(stream, "__dict__") and hasattr(stream, "_iterator"):
            stream._iterator = _observed(stream._iterator, recording)
            close = getattr(stream, "close", None)
            if callable(close):
                stream.close = _finishing_close(close, recording)
            return stream
        if hasattr(stream, "__anext__") or hasattr(stream, "__next__"):
            return _observed(stream, recording)
    except Exception:
        pass
    recording.finish(None)
    return stream


def _opened_stream(open_stream: Callable[[], Any], recording: StreamRecording) -> Any:
    try:
        stream = open_stream()
    except BaseException as error:
        recording.finish(error)
        raise
    return observed_stream(stream, recording)


async def _awaited_stream(request: Awaitable[Any], recording: StreamRecording) -> Any:
    try:
        stream = await request
    except BaseException as error:
        recording.finish(error)
        raise
    return observed_stream(stream, recording)


def _observed_message_stream_manager(manager: Any, recording: StreamRecording) -> Any:
    for attribute in MESSAGE_STREAM_REQUESTS:
        request = getattr(manager, "__dict__", {}).get(attribute)
        if request is None:
            continue
        if inspect.isawaitable(request):
            setattr(manager, attribute, _awaited_stream(request, recording))
        else:
            setattr(
                manager,
                attribute,
                functools.partial(_opened_stream, request, recording),
            )
        return manager
    recording.finish(None)
    return manager


def _error_text(error: BaseException | None) -> str | None:
    return f"{type(error).__name__}: {error}" if error is not None else None


def _stream_outcome(
    recording: StreamRecording, error: BaseException | None
) -> StreamOutcome:
    call = recording.call
    summary = (
        call.stream_summary(recording.events)
        if call.stream_summary and recording.events
        else None
    )
    duration_ms = round((time.monotonic() - recording.started_monotonic) * 1000)
    contexts = (
        [context_from_response(call, recording.request, summary, duration_ms)]
        if summary is not None
        else None
    )
    return StreamOutcome(
        result=summary,
        contexts=contexts,
        prompt=call.prompt(recording.request) or None,
        error=_error_text(error),
    )


def _emit_stream(recording: StreamRecording, outcome: StreamOutcome) -> None:
    for span in recording.spans:
        try:
            span.session.emit(
                span_id=span.span_id,
                parent_span_id=span.parent_span_id,
                span_name=recording.span_name,
                inputs=dict(recording.request),
                result=outcome.result,
                error=outcome.error,
                started_at=span.started_at,
                ended_at=span.session.now(),
                span_type="llm",
                contexts=outcome.contexts,
                prompt=outcome.prompt,
            )
        finally:
            _trace_completion(span.session).end(span.session.trace_id, span.span_id)


def _trace_completion(session: subtree.Session) -> Any:
    return session.owner.http_client.trace_completion


def _held_stream_span(session: subtree.Session) -> StreamSpan:
    span = StreamSpan(
        session=session,
        span_id=str(uuid.uuid4()),
        parent_span_id=subtree.current_parent_span_id(session),
        started_at=session.now(),
    )
    _trace_completion(session).start(session.trace_id, span.span_id)
    return span


def _own_stream_spans() -> tuple[StreamSpan, ...]:
    return tuple(
        _held_stream_span(session)
        for session in subtree.active_sessions()
        if session.owner is not None
    )


def _start_recording(
    call: ProviderCall, span_name: str, request: Mapping[str, Any], node_owned: bool
) -> StreamRecording:
    subtree.mark_usage_recorded()
    recording = StreamRecording(
        call=call,
        span_name=span_name,
        request=request,
        spans=(),
        started_monotonic=time.monotonic(),
    )
    if not (node_owned and hand_stream_to_node(recording)):
        recording.spans = _own_stream_spans()
    _mark_recorded(recording)
    return recording


def _observe(call: ProviderCall, stream: Any, recording: StreamRecording) -> Any:
    observed = (call.observe or observed_stream)(stream, recording)
    _finish_when_dropped(observed, recording)
    return observed


def _finish_when_dropped(stream: Any, recording: StreamRecording) -> None:
    with contextlib.suppress(TypeError):
        weakref.finalize(stream, recording.finish, None).atexit = False


def _streamed_call(
    call: ProviderCall,
    span_name: str,
    original: Callable[..., Any],
    node_owned: bool,
) -> Callable[..., Any]:
    if is_async_create(original):

        async def async_run(resource: Any, *args: Any, **kwargs: Any) -> Any:
            recording = _start_recording(call, span_name, kwargs, node_owned)
            try:
                stream = await original(resource, *args, **kwargs)
            except BaseException as error:
                recording.finish(error)
                raise
            return _observe(call, stream, recording)

        return async_run

    def run(resource: Any, *args: Any, **kwargs: Any) -> Any:
        recording = _start_recording(call, span_name, kwargs, node_owned)
        try:
            stream = original(resource, *args, **kwargs)
        except BaseException as error:
            recording.finish(error)
            raise
        return _observe(call, stream, recording)

    return run


OPENROUTER = ProviderCall(
    provider="openrouter",
    module="openai.resources.chat.completions.completions",
    classes=("Completions", "AsyncCompletions"),
    handles=_is_openrouter_resource,
    is_response=_is_chat_completion,
    prompt=_chat_completion_prompt,
    usage=_chat_completion_usage,
    stream_summary=_chat_stream_summary,
)

OPENAI_CHAT = dataclasses.replace(OPENROUTER, provider="openai", handles=_any_resource)

OPENROUTER_EMBEDDINGS = ProviderCall(
    provider="openrouter",
    module="openai.resources.embeddings",
    classes=("Embeddings", "AsyncEmbeddings"),
    handles=_is_openrouter_resource,
    is_response=_is_embedding_list,
    prompt=_embedding_prompt,
    usage=_embedding_usage,
)

OPENAI_EMBEDDINGS = dataclasses.replace(
    OPENROUTER_EMBEDDINGS, provider="openai", handles=_any_resource
)

OPENAI_TRANSCRIPTIONS = ProviderCall(
    provider="openai",
    module="openai.resources.audio.transcriptions",
    classes=("Transcriptions", "AsyncTranscriptions"),
    handles=_any_resource,
    is_response=_is_transcription,
    prompt=_transcription_prompt,
    usage=_transcription_usage,
    stream_summary=_transcription_stream_summary,
)

ANTHROPIC = ProviderCall(
    provider="anthropic",
    module="anthropic.resources.messages.messages",
    classes=("Messages", "AsyncMessages"),
    handles=_any_resource,
    is_response=_is_anthropic_message,
    prompt=_anthropic_prompt,
    usage=_anthropic_usage,
    stream_summary=_anthropic_stream_summary,
)

OPENAI_RESPONSES = ProviderCall(
    provider="openai",
    module="openai.resources.responses.responses",
    classes=("Responses", "AsyncResponses"),
    handles=_any_resource,
    is_response=_is_openai_response,
    prompt=_openai_responses_prompt,
    usage=_openai_responses_usage,
    stream_summary=_openai_responses_stream_summary,
)

GEMINI = ProviderCall(
    provider="gemini",
    module="google.genai.models",
    classes=("Models", "AsyncModels"),
    handles=_any_resource,
    is_response=_is_gemini_response,
    prompt=_gemini_prompt,
    usage=_gemini_usage,
    method=GENERATE_CONTENT,
    stream_summary=_gemini_stream_summary,
)

PROVIDER_CALLS = (
    OPENROUTER,
    OPENAI_CHAT,
    dataclasses.replace(OPENROUTER, method=PARSE),
    dataclasses.replace(OPENAI_CHAT, method=PARSE),
    OPENROUTER_EMBEDDINGS,
    OPENAI_EMBEDDINGS,
    OPENAI_TRANSCRIPTIONS,
    ANTHROPIC,
    dataclasses.replace(ANTHROPIC, method=PARSE),
    dataclasses.replace(
        ANTHROPIC,
        method=STREAM,
        always_streams=True,
        observe=_observed_message_stream_manager,
    ),
    OPENAI_RESPONSES,
    dataclasses.replace(OPENAI_RESPONSES, method=PARSE),
    GEMINI,
    dataclasses.replace(GEMINI, method=GENERATE_CONTENT_STREAM, always_streams=True),
)
_BY_MODULE: dict[str, tuple[ProviderCall, ...]] = {}
for _call in PROVIDER_CALLS:
    _BY_MODULE[_call.module] = (*_BY_MODULE.get(_call.module, ()), _call)
_METHODS = frozenset(call.method for call in PROVIDER_CALLS)


def context_from_response(
    call: ProviderCall, request: Mapping[str, Any], response: Any, duration_ms: int
) -> dict[str, Any]:
    return {
        "provider": call.provider,
        **call.usage(request, response),
        "durationMs": duration_ms,
    }


def request_of(args: tuple[Any, ...], kwargs: Mapping[str, Any]) -> Mapping[str, Any]:
    if "model" in kwargs or not args or not isinstance(args[0], Mapping):
        return kwargs
    return args[0]


def record_completion(
    call: ProviderCall,
    span: Any,
    request: Mapping[str, Any],
    response: Any,
    duration_ms: int,
) -> None:
    if not call.is_response(response):
        return
    with contextlib.suppress(Exception):
        prompt = call.prompt(request)
        if prompt:
            span.set_prompt(prompt)
        span.add_context(context_from_response(call, request, response, duration_ms))


def record_auto_traced_completion(
    call: ProviderCall,
    span: Any,
    request: Mapping[str, Any],
    response: Any,
    duration_ms: int,
) -> None:
    record_completion(call, span, request, response, duration_ms)
    subtree.mark_usage_recorded()
    _mark_recorded(response)


def _langchain_handler_records_call() -> bool:
    frame = sys._getframe(1)
    while frame is not None:
        if frame.f_code.co_name in _LANGCHAIN_CHAT_MODEL_FRAMES and str(
            frame.f_globals.get("__name__", "")
        ).startswith("langchain_core."):
            handlers = getattr(frame.f_locals.get("run_manager"), "handlers", None)
            return any(
                getattr(handler, "records_llm_calls", False)
                for handler in handlers or ()
            )
        frame = frame.f_back
    return False


def framework_records_call() -> bool:
    session = subtree.current_session()
    if session is not None and subtree.framework_llm_call_open(session):
        return True
    return _langchain_handler_records_call()


def _streams(call: ProviderCall, kwargs: Mapping[str, Any]) -> bool:
    return call.always_streams or bool(kwargs.get("stream"))


def _recorded_call(
    calls: tuple[ProviderCall, ...],
    span_name: str,
    original: Callable[..., Any],
    resource: Any,
    kwargs: Mapping[str, Any],
) -> Any:
    session = subtree.current_session()
    owner = getattr(session, "owner", None)
    ownership = take_node_ownership()
    call = next((call for call in calls if call.handles(resource)), None)
    if (
        session is None
        or owner is None
        or call is None
        or ownership == NODE_OMITS_CALL
        or (_streams(call, kwargs) and call.stream_summary is None)
        or framework_records_call()
    ):
        return None
    if ownership != NODE_RECORDS_CALL and (
        call.method in session.exclude
        or span_name in session.exclude
        or not subtree.admits_llm_call(session)
    ):
        return None
    if _streams(call, kwargs):
        return _streamed_call(call, span_name, original, ownership == NODE_RECORDS_CALL)
    if ownership == NODE_RECORDS_CALL:
        return owner._provider_auto_run(call, span_name, original)
    return owner._provider_auto_traced_call(call, span_name, original)


def is_async_create(original: Callable[..., Any]) -> bool:
    return inspect.iscoroutinefunction(inspect.unwrap(original))


def _patched_method(
    calls: tuple[ProviderCall, ...],
    cls: type,
    method: str,
    original: Callable[..., Any],
) -> Any:
    span_name = f"{cls.__name__}.{method}"

    if is_async_create(original):

        @functools.wraps(original)
        async def async_patched(self: Any, *args: Any, **kwargs: Any) -> Any:
            recorded = _recorded_call(calls, span_name, original, self, kwargs)
            if recorded is None:
                return await original(self, *args, **kwargs)
            return await recorded(self, *args, **kwargs)

        patched: Callable[..., Any] = async_patched
    else:

        @functools.wraps(original)
        def sync_patched(self: Any, *args: Any, **kwargs: Any) -> Any:
            recorded = _recorded_call(calls, span_name, original, self, kwargs)
            if recorded is None:
                return original(self, *args, **kwargs)
            return recorded(self, *args, **kwargs)

        patched = sync_patched

    renamed(patched, method, CALL_MARKER)
    setattr(patched, CALL_MARKER, calls[0])
    return patched


def patch_client_class(calls: tuple[ProviderCall, ...], cls: type) -> None:
    with _lock:
        if cls.__dict__.get(PATCHED_MARKER) is True:
            return
        for method in dict.fromkeys(call.method for call in calls):
            original = cls.__dict__.get(method)
            if inspect.isfunction(original):
                method_calls = tuple(call for call in calls if call.method == method)
                setattr(
                    cls, method, _patched_method(method_calls, cls, method, original)
                )
        setattr(cls, PATCHED_MARKER, True)


def patch_module(module: Any) -> None:
    calls = _BY_MODULE.get(getattr(module, "__name__", ""), ())
    for class_name in dict.fromkeys(name for call in calls for name in call.classes):
        cls = getattr(module, class_name, None)
        if inspect.isclass(cls):
            patch_client_class(
                tuple(call for call in calls if class_name in call.classes), cls
            )


def instrument_loaded_clients() -> None:
    for module_name in _BY_MODULE:
        module = sys.modules.get(module_name)
        if module is None:
            continue
        with contextlib.suppress(Exception):
            patch_module(module)


def call_for_function(calls: tuple[ProviderCall, ...], fn: Any) -> ProviderCall:
    resource = getattr(fn, "__self__", None)
    return next((call for call in calls if call.handles(resource)), calls[-1])


def provider_of(fn: Any) -> ProviderCall | None:
    call = getattr(fn, CALL_MARKER, None)
    return call if isinstance(call, ProviderCall) else None


def resolve_call_target(fn: Any) -> Any:
    if provider_of(fn) is not None:
        return fn
    resource = getattr(fn, "__self__", None)
    name = getattr(getattr(fn, "__func__", None), "__name__", None)
    if resource is None or name not in _METHODS:
        return None
    instrument_loaded_clients()
    cls = type(resource)
    patched = getattr(cls, name, None)
    if provider_of(patched) is None:
        return None
    return patched.__get__(resource, cls)


_finder = PatchingFinder(lambda fullname: fullname in _BY_MODULE, patch_module)


def install_import_hook() -> None:
    _finder.install()
