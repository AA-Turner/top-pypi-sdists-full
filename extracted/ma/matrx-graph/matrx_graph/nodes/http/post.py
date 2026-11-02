"""``http.post`` — POST with JSON, form, or raw body.

Body type is determined by which input field is populated:

- ``json`` (dict) — serialized as JSON with ``Content-Type: application/json``
- ``form`` (dict) — serialized as ``application/x-www-form-urlencoded``
- ``text`` (str) — sent as-is with the caller's ``content_type``

Exactly one of these should be set. If multiple are set, precedence is
``json`` > ``form`` > ``text``.
"""

from __future__ import annotations

import time
from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph.nodes.http._shared import (
    _DEFAULT_MAX_BYTES,
    HttpResponse,
    TextOrSecret,
    build_response_from_httpx,
    outbound_client,
    refused_failure,
    resolve_request_secrets,
    transport_failure,
)
from matrx_graph.types.result import Failure
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.result import NodeResult, success
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory


class HttpPostInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    url: str = Field(min_length=1, description="Absolute URL to POST to.")
    query: dict[str, TextOrSecret] = Field(
        default_factory=dict,
        description='Query string parameters appended to the URL. A value may be {"$secret": "<name>"}.',
    )
    headers: dict[str, TextOrSecret] = Field(
        default_factory=dict,
        description='Extra request headers. A value may be {"$secret": "<name>"} to send a stored secret; '
        'add "format": "Bearer {}" to wrap it.',
    )
    json_body: dict[str, JsonValue] | list[JsonValue] | None = Field(
        default=None,
        description="Body serialized as JSON. Sets Content-Type: application/json. Any value "
        'inside may be {"$secret": "<name>"}.',
    )
    form: dict[str, TextOrSecret] | None = Field(
        default=None,
        description="Body serialized as application/x-www-form-urlencoded. A value may be "
        '{"$secret": "<name>"}.',
    )
    text: str | None = Field(
        default=None,
        description="Raw text body. Pair with an explicit `headers['content-type']`.",
    )


class HttpPostConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    timeout_s: float = Field(
        default=30.0,
        description="Per-request timeout in seconds (connect + read).",
    )
    max_bytes: int = Field(
        default=_DEFAULT_MAX_BYTES,
        description="Max response-body bytes to retain. Excess is truncated.",
    )
    follow_redirects: bool = Field(
        default=True, description="Follow HTTP 3xx redirects automatically."
    )


class HttpPostExecutor:
    """HTTP POST. Declared SIDE_EFFECT — every POST may mutate server state."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="http.post",
        category=NodeCategory.TOOL,
        display_name="Send to the Web",
        description="Send data to a web address.",
        input_schema=HttpPostInput,
        output_schema=HttpResponse,
        config_schema=HttpPostConfig,
        output_kind="http_response",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.SIDE_EFFECT,
        icon="upload",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: HttpPostInput,
        config: HttpPostConfig,
    ) -> NodeResult[HttpResponse]:
        from matrx_utils.outbound_guard import OutboundUrlRefused

        prepared = await resolve_request_secrets(
            ctx,
            {
                "query": inputs.query,
                "headers": inputs.headers,
                "json_body": inputs.json_body,
                "form": inputs.form,
            },
        )
        if isinstance(prepared, Failure):
            return prepared
        parts, found = prepared
        started = time.monotonic()
        kwargs: dict[str, Any] = {
            "params": parts["query"] or None,
            "headers": parts["headers"] or None,
        }

        # Priority: json > form > text. Pydantic validation ensures at most
        # one is non-None in most real workflows, but precedence is explicit.
        if parts["json_body"] is not None:
            kwargs["json"] = parts["json_body"]
        elif parts["form"] is not None:
            kwargs["data"] = parts["form"]
        elif inputs.text is not None:
            kwargs["content"] = inputs.text

        try:
            with found.active():
                async with outbound_client(
                    timeout=config.timeout_s,
                    follow_redirects=config.follow_redirects,
                ) as client:
                    resp = await client.post(inputs.url, **kwargs)
            elapsed = int((time.monotonic() - started) * 1000)
            return success(
                found.redact(
                    build_response_from_httpx(resp, str(resp.url), elapsed, config.max_bytes)
                )
            )
        except OutboundUrlRefused as e:
            elapsed = int((time.monotonic() - started) * 1000)
            return found.redact(refused_failure(inputs.url, e, elapsed))
        except Exception as e:
            elapsed = int((time.monotonic() - started) * 1000)
            return found.redact(transport_failure(inputs.url, f"{type(e).__name__}: {e}", elapsed))
