from __future__ import annotations

import json
from dataclasses import asdict, dataclass, is_dataclass
from enum import Enum
from typing import (
    Any,
    AsyncIterable,
    AsyncIterator,
    Generic,
    Iterable,
    Iterator,
    Literal,
    TypeVar,
)

from . import _linguafranca

T = TypeVar("T")


@dataclass(frozen=True)
class ConversionConfig:
    """Configuration for request conversions.

    Attributes:
        strip_encrypted_reasoning: When ``True``, strips provider-specific
            encrypted reasoning data from request message history. Thinking
            blocks with summaries keep their summaries but lose
            ``encrypted_content``; redacted-thinking blocks are dropped
            entirely. The reasoning/thinking *config* (whether the model
            should think) is preserved.
    """

    strip_encrypted_reasoning: bool = False


def _encode_config(config: ConversionConfig | dict[str, Any] | None) -> str | None:
    if config is None:
        return None
    if isinstance(config, ConversionConfig):
        return json.dumps(asdict(config))
    if isinstance(config, dict):
        return json.dumps(config)
    raise TypeError(f"unsupported config type: {type(config)!r}")


class FormatName(str, Enum):
    """LLM API format identifier.

    Members:
        OPEN_RESPONSES: Open Responses API format.
        OPENAI_CHAT_COMPLETIONS: OpenAI Chat Completions API format.
        ANTHROPIC_MESSAGES: Anthropic Messages API format.
    """

    OPEN_RESPONSES = "open_responses"
    OPENAI_CHAT_COMPLETIONS = "openai_chat_completions"
    ANTHROPIC_MESSAGES = "anthropic_messages"


@dataclass(frozen=True)
class ConversionWarning:
    """A warning emitted when a conversion is lossy.

    Some fields cannot be represented in the target format and are dropped or
    modified. Each warning describes one such case.

    Attributes:
        field: Dot-separated path to the affected field (e.g. ``"choices[1]"``).
        action: The action that was performed: ``"dropped"`` (field removed),
            ``"changed"`` (field value altered), or ``"added"`` (value synthesized).
        message: Human-readable description of what was lost or changed.
    """

    field: str
    action: Literal["dropped", "changed", "added"]
    message: str


@dataclass(frozen=True)
class ConversionResult(Generic[T]):
    """Result of a non-streaming conversion.

    Attributes:
        value: The converted payload.
        warnings: Warnings about lossy parts of the conversion (empty list when
            the conversion is lossless).
    """

    value: T
    warnings: list[ConversionWarning]


def _to_jsonable(value: object) -> Any:
    if is_dataclass(value) and not isinstance(value, type):
        return asdict(value)
    if isinstance(value, dict):
        return value
    if hasattr(value, "model_dump"):
        try:
            return value.model_dump(mode="json")
        except TypeError:
            return value.model_dump()
    raise TypeError(f"unsupported payload type: {type(value)!r}")


def _parse_result(payload: str) -> ConversionResult[Any]:
    data = json.loads(payload)
    warnings = [ConversionWarning(**w) for w in data.get("warnings", [])]
    return ConversionResult(value=data["value"], warnings=warnings)


def _format_value(format_name: FormatName) -> str:
    return str(format_name.value)


def convert_request_json(
    payload: dict[str, Any],
    *,
    source_format: FormatName,
    target_format: FormatName,
    config: ConversionConfig | dict[str, Any] | None = None,
) -> ConversionResult[dict[str, Any]]:
    """Convert an LLM request payload between formats.

    Takes a plain dict and returns a plain dict. For dataclass / Pydantic
    inputs use :func:`convert_request` instead.

    Args:
        payload: Request body as a JSON-compatible dict.
        source_format: Format the payload is currently in.
        target_format: Format to convert to.
        config: Optional conversion configuration. Accepts a
            :class:`ConversionConfig`, a dict, or ``None``.

    Returns:
        A :class:`ConversionResult` whose ``value`` is the converted request
        dict and ``warnings`` lists any lossy-conversion notes.

    Raises:
        SchemaValidationError: If *payload* doesn't match *source_format*.
        InvalidInputError: If a format name is unrecognised.
        UnsupportedConversionError: If the requested conversion isn't supported.

    Example::

        result = lf.convert_request_json(
            {"model": "gpt-4.1-mini", "messages": [{"role": "user", "content": "hi"}]},
            source_format=lf.FormatName.OPENAI_CHAT_COMPLETIONS,
            target_format=lf.FormatName.ANTHROPIC_MESSAGES,
        )
        print(result.value)  # Anthropic Messages dict
    """
    result = _linguafranca.convert_request_json_str(
        json.dumps(payload),
        _format_value(source_format),
        _format_value(target_format),
        _encode_config(config),
    )
    return _parse_result(result)


def convert_response_json(
    payload: dict[str, Any],
    *,
    source_format: FormatName,
    target_format: FormatName,
) -> ConversionResult[dict[str, Any]]:
    """Convert an LLM response payload between formats.

    Takes a plain dict and returns a plain dict. For dataclass / Pydantic
    inputs use :func:`convert_response` instead.

    Args:
        payload: Response body as a JSON-compatible dict.
        source_format: Format the payload is currently in.
        target_format: Format to convert to.

    Returns:
        A :class:`ConversionResult` whose ``value`` is the converted response
        dict and ``warnings`` lists any lossy-conversion notes.

    Raises:
        SchemaValidationError: If *payload* doesn't match *source_format*.
        InvalidInputError: If a format name is unrecognised.
        UnsupportedConversionError: If the requested conversion isn't supported.

    Example::

        result = lf.convert_response_json(
            openai_response,
            source_format=lf.FormatName.OPENAI_CHAT_COMPLETIONS,
            target_format=lf.FormatName.OPEN_RESPONSES,
        )
    """
    result = _linguafranca.convert_response_json_str(
        json.dumps(payload),
        _format_value(source_format),
        _format_value(target_format),
    )
    return _parse_result(result)


def convert_request(
    source: object,
    *,
    source_format: FormatName,
    target_format: FormatName,
    config: ConversionConfig | dict[str, Any] | None = None,
) -> ConversionResult[dict[str, Any]]:
    """Convert an LLM request from any supported Python object.

    Accepts a dict, a dataclass instance (including types from
    ``linguafranca.types``), or a Pydantic model. Serialises the input to JSON
    internally.

    Args:
        source: Request payload as a dict, dataclass, or Pydantic model.
        source_format: Format the payload is currently in.
        target_format: Format to convert to.
        config: Optional conversion configuration. Accepts a
            :class:`ConversionConfig`, a dict, or ``None``.

    Returns:
        A :class:`ConversionResult` with the converted request dict.

    Raises:
        TypeError: If *source* is not a dict, dataclass instance, or Pydantic model.
        SchemaValidationError: If the payload doesn't match *source_format*.
        InvalidInputError: If a format name is unrecognised.
        UnsupportedConversionError: If the requested conversion isn't supported.

    Example::

        from linguafranca.types import (
            ChatCompletionsOpenAiRequest,
            ChatCompletionsMessageUser,
        )

        request = ChatCompletionsOpenAiRequest(
            model="gpt-4.1-mini",
            messages=[ChatCompletionsMessageUser(content="hi", role="user")],
        )
        result = lf.convert_request(
            request,
            source_format=lf.FormatName.OPENAI_CHAT_COMPLETIONS,
            target_format=lf.FormatName.ANTHROPIC_MESSAGES,
        )
    """
    payload = _to_jsonable(source)
    return convert_request_json(
        payload,
        source_format=source_format,
        target_format=target_format,
        config=config,
    )


def convert_response(
    source: object,
    *,
    source_format: FormatName,
    target_format: FormatName,
) -> ConversionResult[dict[str, Any]]:
    """Convert an LLM response from any supported Python object.

    Accepts a dict, a dataclass instance (including types from
    ``linguafranca.types``), or a Pydantic model. Serialises the input to JSON
    internally.

    Args:
        source: Response payload as a dict, dataclass, or Pydantic model.
        source_format: Format the payload is currently in.
        target_format: Format to convert to.

    Returns:
        A :class:`ConversionResult` with the converted response dict.

    Raises:
        TypeError: If *source* is not a dict, dataclass instance, or Pydantic model.
        SchemaValidationError: If the payload doesn't match *source_format*.
        InvalidInputError: If a format name is unrecognised.
        UnsupportedConversionError: If the requested conversion isn't supported.
    """
    payload = _to_jsonable(source)
    return convert_response_json(
        payload,
        source_format=source_format,
        target_format=target_format,
    )


class StreamConversion:
    """Synchronous iterator that converts streaming response events on the fly.

    Iterate over it to receive converted events as dicts. After iteration,
    call :meth:`take_warnings` to retrieve any lossy-conversion warnings that
    accumulated during the stream.

    Example::

        stream = lf.convert_response_stream_json(
            events,
            source_format=lf.FormatName.OPENAI_CHAT_COMPLETIONS,
            target_format=lf.FormatName.OPEN_RESPONSES,
        )
        for event in stream:
            handle(event)
        warnings = stream.take_warnings()
    """

    def __init__(
        self, events: Iterable[object], converter: Any, *, json_events: bool
    ) -> None:
        self._events = events
        self._converter = converter
        self._json_events = json_events

    def __iter__(self) -> Iterator[dict[str, Any]]:
        for event in self._events:
            payload = event if self._json_events else _to_jsonable(event)
            batch = self._converter.transform_json_str(json.dumps(payload))
            for out_event in json.loads(batch):
                yield out_event
        flush_batch = self._converter.flush_json_str()
        for out_event in json.loads(flush_batch):
            yield out_event

    def take_warnings(self) -> list[ConversionWarning]:
        """Return warnings accumulated during streaming and reset the list."""
        payload = self._converter.take_warnings_json_str()
        return [ConversionWarning(**w) for w in json.loads(payload)]


class AsyncStreamConversion:
    """Async iterator that converts streaming response events on the fly.

    Same as :class:`StreamConversion` but consumes an ``AsyncIterable`` of
    events (e.g. from an ``httpx`` or ``aiohttp`` streaming response).

    Example::

        stream = lf.aconvert_response_stream(
            async_events,
            source_format=lf.FormatName.OPENAI_CHAT_COMPLETIONS,
            target_format=lf.FormatName.OPEN_RESPONSES,
        )
        async for event in stream:
            handle(event)
        warnings = stream.take_warnings()
    """

    def __init__(self, events: AsyncIterable[object], converter: Any) -> None:
        self._events = events
        self._converter = converter

    async def __aiter__(self) -> AsyncIterator[dict[str, Any]]:
        async for event in self._events:
            batch = self._converter.transform_json_str(json.dumps(_to_jsonable(event)))
            for out_event in json.loads(batch):
                yield out_event
        flush_batch = self._converter.flush_json_str()
        for out_event in json.loads(flush_batch):
            yield out_event

    def take_warnings(self) -> list[ConversionWarning]:
        """Return warnings accumulated during streaming and reset the list."""
        payload = self._converter.take_warnings_json_str()
        return [ConversionWarning(**w) for w in json.loads(payload)]


def convert_response_stream_json(
    events: Iterable[dict[str, Any]],
    *,
    source_format: FormatName,
    target_format: FormatName,
) -> StreamConversion:
    """Create a streaming converter for response events given as dicts.

    Each dict in *events* must be a valid streaming chunk in *source_format*.
    The returned :class:`StreamConversion` yields converted events as dicts.

    Args:
        events: Iterable of streaming event dicts.
        source_format: Format the events are currently in.
        target_format: Format to convert to.

    Returns:
        A :class:`StreamConversion` you can iterate over.

    Raises:
        UnsupportedConversionError: If the stream conversion pair isn't supported.

    Example::

        def parse_sse(response: httpx.Response):
            for line in response.iter_lines():
                if line.startswith("data: ") and line != "data: [DONE]":
                    yield json.loads(line[6:])

        with httpx.stream("POST", "https://api.openai.com/v1/chat/completions",
                          headers=headers, json={..., "stream": True}) as resp:
            stream = lf.convert_response_stream_json(
                parse_sse(resp),
                source_format=lf.FormatName.OPENAI_CHAT_COMPLETIONS,
                target_format=lf.FormatName.OPEN_RESPONSES,
            )
            for event in stream:
                print(event)
    """
    converter = _linguafranca.create_response_stream_converter(
        _format_value(source_format),
        _format_value(target_format),
    )
    return StreamConversion(events, converter, json_events=True)


def convert_response_stream(
    events: Iterable[object],
    *,
    source_format: FormatName,
    target_format: FormatName,
) -> StreamConversion:
    """Like :func:`convert_response_stream_json` but accepts dataclass or Pydantic events.

    Each event is serialised to JSON internally via :func:`dataclasses.asdict`
    or ``model_dump()``.

    Args:
        events: Iterable of streaming event objects (dataclass or Pydantic).
        source_format: Format the events are currently in.
        target_format: Format to convert to.

    Returns:
        A :class:`StreamConversion` you can iterate over.

    Raises:
        UnsupportedConversionError: If the stream conversion pair isn't supported.
        TypeError: If an event is not a dict, dataclass, or Pydantic model.
    """
    converter = _linguafranca.create_response_stream_converter(
        _format_value(source_format),
        _format_value(target_format),
    )
    return StreamConversion(events, converter, json_events=False)


def aconvert_response_stream(
    events: AsyncIterable[object],
    *,
    source_format: FormatName,
    target_format: FormatName,
) -> AsyncStreamConversion:
    """Async version of :func:`convert_response_stream`.

    Consumes an ``AsyncIterable`` of event objects (dataclass or Pydantic) and
    yields converted event dicts via ``async for``.

    Args:
        events: Async iterable of streaming event objects.
        source_format: Format the events are currently in.
        target_format: Format to convert to.

    Returns:
        An :class:`AsyncStreamConversion` you can ``async for`` over.

    Raises:
        UnsupportedConversionError: If the stream conversion pair isn't supported.

    Example::

        async def parse_sse(response: httpx.Response):
            async for line in response.aiter_lines():
                if line.startswith("data: ") and line != "data: [DONE]":
                    yield json.loads(line[6:])

        async with httpx.AsyncClient() as client:
            async with client.stream("POST", url, headers=headers, json=payload) as resp:
                stream = lf.aconvert_response_stream(
                    parse_sse(resp),
                    source_format=lf.FormatName.OPENAI_CHAT_COMPLETIONS,
                    target_format=lf.FormatName.OPEN_RESPONSES,
                )
                async for event in stream:
                    print(event)
    """
    converter = _linguafranca.create_response_stream_converter(
        _format_value(source_format),
        _format_value(target_format),
    )
    return AsyncStreamConversion(events, converter)


def to_messages_request(
    source: object,
    *,
    source_format: FormatName,
    config: ConversionConfig | dict[str, Any] | None = None,
) -> ConversionResult[dict[str, Any]]:
    """Convenience wrapper: convert a request to Anthropic Messages format.

    Equivalent to calling :func:`convert_request` with
    ``target_format=FormatName.ANTHROPIC_MESSAGES``.

    Args:
        source: Request payload as a dict, dataclass, or Pydantic model.
        source_format: Format the payload is currently in.
        config: Optional :class:`ConversionConfig` or dict to control
            conversion behavior (e.g. ``strip_encrypted_reasoning``).

    Example::

        result = lf.to_messages_request(
            {"model": "gpt-4.1-mini", "messages": [{"role": "user", "content": "hi"}]},
            source_format=lf.FormatName.OPENAI_CHAT_COMPLETIONS,
            config=lf.ConversionConfig(strip_encrypted_reasoning=True),
        )
    """
    return convert_request(
        source,
        source_format=source_format,
        target_format=FormatName.ANTHROPIC_MESSAGES,
        config=config,
    )


def to_messages_response(
    source: object,
    *,
    source_format: FormatName,
) -> ConversionResult[dict[str, Any]]:
    """Convenience wrapper: convert a response to Anthropic Messages format.

    Equivalent to calling :func:`convert_response` with
    ``target_format=FormatName.ANTHROPIC_MESSAGES``.

    Example::

        result = lf.to_messages_response(
            openai_response,
            source_format=lf.FormatName.OPENAI_CHAT_COMPLETIONS,
        )
    """
    return convert_response(
        source,
        source_format=source_format,
        target_format=FormatName.ANTHROPIC_MESSAGES,
    )


def to_chat_completions_request(
    source: object,
    *,
    source_format: FormatName,
    config: ConversionConfig | dict[str, Any] | None = None,
) -> ConversionResult[dict[str, Any]]:
    """Convenience wrapper: convert a request to OpenAI Chat Completions format.

    Equivalent to calling :func:`convert_request` with
    ``target_format=FormatName.OPENAI_CHAT_COMPLETIONS``.

    Args:
        source: Request payload as a dict, dataclass, or Pydantic model.
        source_format: Format the payload is currently in.
        config: Optional :class:`ConversionConfig` or dict to control
            conversion behavior (e.g. ``strip_encrypted_reasoning``).

    Example::

        result = lf.to_chat_completions_request(
            {"model": "claude-3-5-sonnet", "max_tokens": 64,
             "messages": [{"role": "user", "content": "hi"}]},
            source_format=lf.FormatName.ANTHROPIC_MESSAGES,
            config={"strip_encrypted_reasoning": True},
        )
    """
    return convert_request(
        source,
        source_format=source_format,
        target_format=FormatName.OPENAI_CHAT_COMPLETIONS,
        config=config,
    )


def to_chat_completions_response(
    source: object,
    *,
    source_format: FormatName,
) -> ConversionResult[dict[str, Any]]:
    """Convenience wrapper: convert a response to OpenAI Chat Completions format.

    Equivalent to calling :func:`convert_response` with
    ``target_format=FormatName.OPENAI_CHAT_COMPLETIONS``.

    Example::

        result = lf.to_chat_completions_response(
            anthropic_response,
            source_format=lf.FormatName.ANTHROPIC_MESSAGES,
        )
    """
    return convert_response(
        source,
        source_format=source_format,
        target_format=FormatName.OPENAI_CHAT_COMPLETIONS,
    )


# ── Collect stream (stream events → single response) ──


def collect_response_stream_json(
    events: Iterable[dict[str, Any]],
    *,
    format_name: FormatName,
) -> ConversionResult[dict[str, Any]]:
    """Collect streaming response events into a single non-streaming response.

    Takes an iterable of event dicts (e.g. from an SSE stream) and returns the
    complete response. The iterable is consumed lazily — you can pass a
    generator or any iterator, not just a list.

    Args:
        events: Iterable of streaming event dicts.
        format_name: Format the events are in.

    Returns:
        A :class:`ConversionResult` whose ``value`` is the response dict and
        ``warnings`` lists any issues (e.g. missing terminal event).

    Raises:
        SchemaValidationError: If an event doesn't match *format*.
        InvalidInputError: If no events are provided.
        UnsupportedConversionError: If *format* is not yet supported.

    Example::

        result = lf.collect_response_stream_json(
            parsed_sse_events,
            format_name=lf.FormatName.OPEN_RESPONSES,
        )
        print(result.value)  # complete response dict
    """
    collector = _linguafranca.create_response_collector(_format_value(format_name))
    for event in events:
        collector.feed_json_str(json.dumps(event))
    return _parse_result(collector.finalize_json_str())


def collect_response_stream(
    events: Iterable[object],
    *,
    format_name: FormatName,
) -> ConversionResult[dict[str, Any]]:
    """Like :func:`collect_response_stream_json` but accepts dataclass or Pydantic events.

    Each event is serialised to JSON internally via :func:`dataclasses.asdict`
    or ``model_dump()``.

    Args:
        events: Iterable of streaming event objects (dict, dataclass, or Pydantic).
        format_name: Format the events are in.

    Returns:
        A :class:`ConversionResult` with the complete response dict.

    Raises:
        TypeError: If an event is not a dict, dataclass, or Pydantic model.
        SchemaValidationError: If an event doesn't match *format*.
        InvalidInputError: If no events are provided.
        UnsupportedConversionError: If *format* is not yet supported.
    """
    collector = _linguafranca.create_response_collector(_format_value(format_name))
    for event in events:
        collector.feed_json_str(json.dumps(_to_jsonable(event)))
    return _parse_result(collector.finalize_json_str())


async def acollect_response_stream_json(
    events: AsyncIterable[dict[str, Any]],
    *,
    format_name: FormatName,
) -> ConversionResult[dict[str, Any]]:
    """Async version of :func:`collect_response_stream_json`.

    Consumes an ``AsyncIterable`` of event dicts (e.g. from an httpx async
    SSE response) and returns the complete response.

    Args:
        events: Async iterable of streaming event dicts.
        format_name: Format the events are in.

    Returns:
        A :class:`ConversionResult` with the complete response dict.

    Example::

        async def parse_sse(response):
            async for line in response.aiter_lines():
                if line.startswith("data: ") and line != "data: [DONE]":
                    yield json.loads(line[6:])

        result = await lf.acollect_response_stream_json(
            parse_sse(resp),
            format_name=lf.FormatName.OPEN_RESPONSES,
        )
    """
    collector = _linguafranca.create_response_collector(_format_value(format_name))
    async for event in events:
        collector.feed_json_str(json.dumps(event))
    return _parse_result(collector.finalize_json_str())


async def acollect_response_stream(
    events: AsyncIterable[object],
    *,
    format_name: FormatName,
) -> ConversionResult[dict[str, Any]]:
    """Async version of :func:`collect_response_stream`.

    Consumes an ``AsyncIterable`` of event objects (dict, dataclass, or
    Pydantic) and returns the complete response.

    Args:
        events: Async iterable of streaming event objects.
        format_name: Format the events are in.

    Returns:
        A :class:`ConversionResult` with the complete response dict.
    """
    collector = _linguafranca.create_response_collector(_format_value(format_name))
    async for event in events:
        collector.feed_json_str(json.dumps(_to_jsonable(event)))
    return _parse_result(collector.finalize_json_str())


# ── Decompose response (single response → stream events) ──


def decompose_response_to_stream_json(
    response: dict[str, Any],
    *,
    format_name: FormatName,
) -> ConversionResult[list[dict[str, Any]]]:
    """Decompose a non-streaming response into a sequence of stream events.

    Takes a response dict and synthesizes the stream events that a server
    would have produced for that response.

    Args:
        response: Response body as a JSON-compatible dict.
        format_name: Format the response is in.

    Returns:
        A :class:`ConversionResult` whose ``value`` is a list of event dicts.

    Raises:
        SchemaValidationError: If *response* doesn't match *format*.
        UnsupportedConversionError: If *format* is not yet supported.

    Example::

        result = lf.decompose_response_to_stream_json(
            response_dict,
            format_name=lf.FormatName.OPEN_RESPONSES,
        )
        for event in result.value:
            print(event["type"])
    """
    result_str = _linguafranca.decompose_response_to_stream_json_str(
        json.dumps(response),
        _format_value(format_name),
    )
    return _parse_result(result_str)


def decompose_response_to_stream(
    response: object,
    *,
    format_name: FormatName,
) -> ConversionResult[list[dict[str, Any]]]:
    """Like :func:`decompose_response_to_stream_json` but accepts dataclass or Pydantic input.

    Args:
        response: Response payload as a dict, dataclass, or Pydantic model.
        format_name: Format the response is in.

    Returns:
        A :class:`ConversionResult` whose ``value`` is a list of event dicts.

    Raises:
        TypeError: If *response* is not a dict, dataclass, or Pydantic model.
        SchemaValidationError: If the payload doesn't match *format*.
        UnsupportedConversionError: If *format* is not yet supported.
    """
    payload = _to_jsonable(response)
    return decompose_response_to_stream_json(payload, format_name=format_name)
