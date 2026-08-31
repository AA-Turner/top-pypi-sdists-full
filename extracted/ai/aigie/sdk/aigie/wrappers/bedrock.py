"""Tracing wrapper for the AWS Bedrock runtime client.

`wrap_bedrock` patches `invoke_model`, `invoke_model_with_response_stream` and
`converse` on the client the customer built, emits one finalized `llm` span per
call, and otherwise leaves the call alone - same arguments, same return value,
same exceptions.

Three things worth knowing about the shape here:

- **Reading a response consumes it.** `response["body"]` is a `StreamingBody`
  and reads exactly once, so the span puts a fresh stream over the same bytes
  back before returning.
- **A streamed span is emitted when the stream ends**, not when the call that
  returned it did.
- **The system prompt reaches the span under `system_prompt`.** The two invoke
  methods carry it inside the request body under `system`, `converse` takes it
  as its own argument; both are flattened to text under the one name every
  reader downstream looks for.
- **`converse_stream` is not traced.** It needs a collector for the converse
  event shape, which `_BedrockCollector` does not speak.
"""

from __future__ import annotations

import json
import logging
from collections.abc import Callable
from typing import Any

from aigie._system_prompt import system_prompt_text
from aigie.wrappers._base import (
    contained,
    emit_span_now,
    new_provider_run_context,
    opening_stream,
    traced_provider_call,
)
from aigie.wrappers._bedrock_body import (
    chunk_payload,
    chunk_text,
    extract_metrics,
    parse_json,
    reusable_body,
)
from aigie.wrappers._bedrock_usage import (
    PROVIDER as _PROVIDER,
)
from aigie.wrappers._bedrock_usage import (
    counts as token_counts,
)
from aigie.wrappers._bedrock_usage import (
    record_usage,
    usage_dict,
    usage_from,
    usage_from_metrics,
)
from aigie.wrappers._client_patch import bind_options, patch_method, unpatch_all
from aigie.wrappers._span_input import publish_system_prompt, snapshot
from aigie.wrappers._stream import TracedStream

logger = logging.getLogger(__name__)

_TRACED_METHODS = ("invoke_model", "invoke_model_with_response_stream", "converse")


def wrap_bedrock(
    client: Any,
    name: str | None = None,
    metadata: dict[str, Any] | None = None,
    tags: list[str] | None = None,
) -> Any:
    """
    Wrap AWS Bedrock Runtime client for automatic tracing

    Args:
        client: Bedrock Runtime client instance
        name: Optional span name
        metadata: Additional metadata
        tags: Tags to apply

    Returns:
        The same client, with its invoke methods traced. Returned untouched if
        no Aigie client has been initialized.

    Example:
        >>> import boto3
        >>> from aigie.wrappers import wrap_bedrock
        >>>
        >>> client = boto3.client('bedrock-runtime', region_name='us-east-1')
        >>> traced_client = wrap_bedrock(client)
        >>>
        >>> response = traced_client.invoke_model(
        ...     modelId='anthropic.claude-v2',
        ...     body=json.dumps({'prompt': 'Hello!'})
        ... )
    """
    from aigie.client import get_aigie

    if get_aigie() is None:
        logger.debug("[wrapper] No Aigie client - returning the Bedrock client untraced")
        return client

    patch_method(client, "invoke_model", bind_options(_invoke_model, name, metadata, tags))
    patch_method(
        client,
        "invoke_model_with_response_stream",
        bind_options(_invoke_stream, name, metadata, tags),
    )
    patch_method(client, "converse", bind_options(_converse, name, metadata, tags))
    return client


def unwrap_bedrock(client: Any) -> bool:
    """Restore the client's own invoke methods. True if anything was restored."""
    return unpatch_all(client, _TRACED_METHODS)


def _call_metadata(
    model_id: str,
    metadata: dict[str, Any] | None,
    kwargs: dict[str, Any],
) -> dict[str, Any]:
    """The span metadata every Bedrock call starts with."""
    return {
        **(metadata or {}),
        "model": model_id,
        "provider": _PROVIDER,
        "contentType": kwargs.get("contentType", "application/json"),
    }


def _open_span(
    kwargs: dict[str, Any],
    name: str | None,
    metadata: dict[str, Any] | None,
    tags: list[str] | None,
    *,
    streaming: bool = False,
) -> tuple[str, Any] | None:
    """Open the span for one Bedrock call. The three traced methods' shared head.

    `None` when the span could not be opened - a `modelId` whose `__str__`
    raises is enough. This runs before the provider is reached, so the caller
    gets their call untraced rather than getting our exception.
    """
    try:
        model_id = kwargs.get("modelId", "unknown")
        call_metadata = _call_metadata(model_id, metadata, kwargs)
        extra_tags = ["streaming"] if streaming else []
        if streaming:
            call_metadata["streaming"] = True
        run_ctx = new_provider_run_context(
            name or f"bedrock:{model_id}",
            span_type="llm",
            metadata=call_metadata,
            tags=[*(tags or []), _PROVIDER, "aws", *extra_tags],
        )
    except Exception as e:  # noqa: BLE001 - kwargs are the customer's, not ours
        logger.debug("[wrapper] Could not open a Bedrock span: %s", e)
        return None
    return model_id, run_ctx


def _invoke_model(
    original: Callable,
    name: str | None,
    metadata: dict[str, Any] | None,
    tags: list[str] | None,
) -> Callable:
    """Build the traced replacement for `invoke_model`."""

    def traced_invoke_model(*args: Any, **kwargs: Any) -> Any:
        opened = _open_span(kwargs, name, metadata, tags)
        if opened is None:
            return original(*args, **kwargs)
        model_id, run_ctx = opened
        _read_input(run_ctx, _invoke_input, kwargs.get("body"))

        with traced_provider_call(run_ctx):
            response = original(*args, **kwargs)
            contained("reading the Bedrock response", _record_response, run_ctx, response, model_id)
            return response

    return traced_invoke_model


def _invoke_stream(
    original: Callable,
    name: str | None,
    metadata: dict[str, Any] | None,
    tags: list[str] | None,
) -> Callable:
    """Build the traced replacement for `invoke_model_with_response_stream`."""

    def traced_invoke_model_with_response_stream(*args: Any, **kwargs: Any) -> Any:
        opened = _open_span(kwargs, name, metadata, tags, streaming=True)
        if opened is None:
            return original(*args, **kwargs)
        model_id, run_ctx = opened
        _read_input(run_ctx, _invoke_input, kwargs.get("body"))

        with opening_stream(run_ctx):
            response = original(*args, **kwargs)

        # A stream we could not wrap emits nothing downstream, and the provider
        # has already been called and billed - so close the span here instead of
        # losing it. The non-stream path gets this from `traced_provider_call`.
        try:
            wrapped = _replace_stream(response, run_ctx, model_id)
        except Exception as e:  # noqa: BLE001 - a provider can return anything
            logger.debug("[wrapper] Could not wrap the Bedrock stream: %s", e)
            wrapped = False
        if not wrapped:
            run_ctx.metadata.setdefault("status", "success")
            emit_span_now(run_ctx)
        return response

    return traced_invoke_model_with_response_stream


def _converse(
    original: Callable,
    name: str | None,
    metadata: dict[str, Any] | None,
    tags: list[str] | None,
) -> Callable:
    """Build the traced replacement for `converse`.

    `converse` is not `invoke_model` with a different name: the prompt arrives as
    a `system=` argument beside the messages rather than inside a JSON body, and
    the response is already a dict. So it gets its own input and output readers
    instead of reusing the body-parsing ones.
    """

    def traced_converse(*args: Any, **kwargs: Any) -> Any:
        opened = _open_span(kwargs, name, metadata, tags)
        if opened is None:
            return original(*args, **kwargs)
        model_id, run_ctx = opened
        _read_input(run_ctx, _converse_input, kwargs)

        with traced_provider_call(run_ctx):
            response = original(*args, **kwargs)
            contained(
                "reading the Bedrock converse response",
                _record_converse_response,
                run_ctx,
                response,
                model_id,
            )
            return response

    return traced_converse


def _replace_stream(response: Any, run_ctx: Any, model_id: str) -> bool:
    """Put a traced stream in place of the response's event stream.

    False when the response carries nothing iterable to wrap - the caller then
    has to close the span itself, because nothing downstream will.
    """
    if not isinstance(response, dict) or "body" not in response:
        return False
    collector = _BedrockCollector(run_ctx, model_id)
    traced = TracedStream(
        run_ctx,
        response["body"],
        collect=collector.collect,
        finish=collector.finish,
    )
    try:
        response["body"] = traced
    except Exception as e:  # noqa: BLE001 - a response object can refuse in any way
        logger.debug("[wrapper] Could not install the Bedrock stream: %s", e)

    if response.get("body") is not traced:
        # The assignment did not take - whether it raised or was quietly
        # ignored. The caller keeps their own stream, so ours must never close
        # it or emit for it; the call is recorded by our caller instead.
        traced.disarm()
        return False
    return True


class _BedrockCollector:
    """Accumulates a Bedrock event stream into the span it belongs to."""

    def __init__(self, run_ctx: Any, model_id: str) -> None:
        self._run_ctx = run_ctx
        self._model_id = model_id
        # A list, not `self._text += ...`: in-place concat has no fast path for an
        # instance attribute, so appending per chunk is O(n) instead of O(n^2).
        self._parts: list[str] = []
        self._counts: tuple[int, int] | None = None

    def collect(self, event: Any) -> None:
        parsed = chunk_payload(event)
        self._parts.append(chunk_text(parsed))
        found = usage_from_metrics(parsed)
        if found:
            self._counts = found

    def finish(self) -> None:
        self._run_ctx.metadata["output"] = "".join(self._parts)
        if self._counts is None:
            return
        record_usage(self._run_ctx, usage_dict(*self._counts), self._model_id)


def _record_response(run_ctx: Any, response: Any, model_id: str) -> None:
    """Read output, token counts and cost off an `invoke_model` response."""
    parsed = parse_json(reusable_body(response))
    run_ctx.metadata["output"] = parsed
    run_ctx.metadata.update(extract_metrics(parsed))

    record_usage(run_ctx, usage_from(parsed, response), model_id)


def _record_converse_response(run_ctx: Any, response: Any, model_id: str) -> None:
    """Read output, token counts and cost off a `converse` response."""
    if not isinstance(response, dict):
        return
    # Each read is contained on its own: an `output` of an unexpected shape must
    # not take the token counts and the cost down with it, because the call is
    # billed either way.
    contained("reading the Bedrock converse output", _record_converse_output, run_ctx, response)
    contained(
        "reading the Bedrock converse usage", _record_converse_usage, run_ctx, response, model_id
    )


def _record_converse_output(run_ctx: Any, response: dict[str, Any]) -> None:
    """The assistant's message, and why the model stopped."""
    message = (response.get("output") or {}).get("message") or {}
    run_ctx.metadata["output"] = snapshot(message)
    if response.get("stopReason") is not None:
        run_ctx.metadata["stopReason"] = response["stopReason"]


def _record_converse_usage(run_ctx: Any, response: dict[str, Any], model_id: str) -> None:
    """Token counts and cost, read independently of the output."""
    reported = response.get("usage") or {}
    found = token_counts(reported, "inputTokens", "outputTokens")
    if found is None:
        return
    record_usage(run_ctx, usage_dict(*found, reported_total=reported.get("totalTokens")), model_id)


def _read_input(run_ctx: Any, read: Callable[[Any], Any], source: Any) -> None:
    """Record what the call was asked, contained.

    This runs before the provider is reached and outside `traced_provider_call`,
    so anything raising here would replace the customer's call rather than cost
    us a span - the one thing instrumentation may never do.
    """
    contained("reading the Bedrock request", _set_input, run_ctx, read, source)


def _set_input(run_ctx: Any, read: Callable[[Any], Any], source: Any) -> None:
    run_ctx.metadata["input"] = read(source)
    _stamp_system_prompt(run_ctx)


def _stamp_system_prompt(run_ctx: Any) -> None:
    """Copy the span input's prompt onto span metadata.

    Both readers are load-bearing and they are not the same one: the span view
    reads `input.system_prompt`, the judges read metadata. Every other provider
    writes both.
    """
    span_input = run_ctx.metadata.get("input")
    if not isinstance(span_input, dict):
        return
    # Only text is published onward: a caller's own body key can be any shape,
    # and every reader of the metadata key expects a string.
    own = span_input.get("system_prompt")
    if isinstance(own, str) and own:
        run_ctx.metadata["system_prompt"] = own


def _invoke_input(body: Any) -> Any:
    """The span's input for an `invoke_model` call, with the prompt surfaced.

    Anthropic-on-Bedrock carries the system prompt inside the request body under
    `system`, as either a string or a list of content blocks, and every reader
    downstream looks for `system_prompt`.

    A body that already carries a `system_prompt` of its own is not deferred to:
    Bedrock rejects the request outright (`ValidationException: system_prompt:
    Extra inputs are not permitted`), so that key is a leftover rather than
    something the model was told, and letting it win would hand the judges a
    prompt the model never received.
    """
    parsed = _parse_bedrock_input(body)
    if not isinstance(parsed, dict):
        return parsed
    system_text = system_prompt_text(parsed.get("system"))
    return {**parsed, "system_prompt": system_text} if system_text else parsed


def _converse_input(kwargs: dict[str, Any]) -> dict[str, Any]:
    """The span's input for a `converse` call.

    Every argument rather than an allowlist: the invoke path captures its
    request body whole, and `additionalModelRequestFields` - where extended
    thinking and `top_k` live - would be exactly what an allowlist dropped.
    `system` is kept as sent as well as republished as text, because a
    `cachePoint` block flattens to nothing and would otherwise vanish.
    `modelId` is already span metadata.
    """
    span_input: dict[str, Any] = {
        key: snapshot(value)
        for key, value in kwargs.items()
        if key != "modelId" and value is not None
    }
    span_input.setdefault("messages", [])
    contained(
        "reading the Bedrock system prompt", publish_system_prompt, span_input, kwargs.get("system")
    )
    return span_input


def _parse_bedrock_input(body: Any) -> Any:
    """Parse Bedrock input from body"""
    if not body:
        return None

    try:
        if isinstance(body, str):
            return json.loads(body)
        if isinstance(body, bytes):
            return json.loads(body.decode("utf-8"))
        return body
    except Exception as e:  # noqa: BLE001 - the raw body is better than no input
        logger.debug("[wrapper] Could not decode the Bedrock request body: %s", e)
        return body


def create_traced_bedrock(
    region_name: str,
    aws_access_key_id: str | None = None,
    aws_secret_access_key: str | None = None,
    name: str | None = None,
    metadata: dict[str, Any] | None = None,
    tags: list[str] | None = None,
) -> Any:
    """
    Create traced Bedrock client

    Args:
        region_name: AWS region
        aws_access_key_id: AWS access key ID
        aws_secret_access_key: AWS secret access key
        name: Optional span name
        metadata: Additional metadata
        tags: Tags to apply

    Returns:
        Traced Bedrock client

    Example:
        >>> from aigie.wrappers import create_traced_bedrock
        >>>
        >>> client = create_traced_bedrock(region_name='us-east-1')
    """
    try:
        import boto3

        client = boto3.client(
            "bedrock-runtime",
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

        return wrap_bedrock(client, name=name, metadata=metadata, tags=tags)

    except ImportError as err:
        raise ImportError("boto3 not found. Install with: pip install boto3") from err
