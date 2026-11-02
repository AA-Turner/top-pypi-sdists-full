"""``http.get`` — perform a GET request, emit a canonical HttpResponse."""

from __future__ import annotations

import time
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field

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
from matrx_graph.types.usl import field_extras


class HttpGetInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    url: str = Field(min_length=1, description="Absolute URL to GET.")
    query: dict[str, TextOrSecret] = Field(
        default_factory=dict,
        description="Query string parameters appended to the URL. A value may be "
        '{"$secret": "<name>"} to send a stored secret.',
    )
    headers: dict[str, TextOrSecret] = Field(
        default_factory=dict,
        description='Extra request headers. A value may be {"$secret": "<name>"} to send a stored secret; '
        'add "format": "Bearer {}" to wrap it.',
    )


class HttpGetConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    timeout_s: float = Field(
        default=30.0,
        ge=0.1,
        le=600.0,
        description="Per-request timeout in seconds (applies to connect + read).",
        json_schema_extra=field_extras(widget="number"),
    )
    max_bytes: int = Field(
        default=_DEFAULT_MAX_BYTES,
        ge=1024,
        le=50_000_000,
        description="Max body bytes to retain. Excess is truncated.",
    )
    follow_redirects: bool = Field(
        default=True, description="Follow HTTP 3xx redirects automatically."
    )


class HttpGetExecutor:
    """Safe, idempotent-by-declaration HTTP GET."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="http.get",
        category=NodeCategory.TOOL,
        display_name="Fetch from the Web",
        description="Fetch data from a web address.",
        input_schema=HttpGetInput,
        output_schema=HttpResponse,
        config_schema=HttpGetConfig,
        output_kind="http_response",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.IDEMPOTENT,
        icon="download",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: HttpGetInput,
        config: HttpGetConfig,
    ) -> NodeResult[HttpResponse]:
        from matrx_utils.outbound_guard import OutboundUrlRefused

        prepared = await resolve_request_secrets(
            ctx, {"query": inputs.query, "headers": inputs.headers}
        )
        if isinstance(prepared, Failure):
            return prepared
        parts, found = prepared
        started = time.monotonic()
        try:
            with found.active():
                async with outbound_client(
                    timeout=config.timeout_s,
                    follow_redirects=config.follow_redirects,
                ) as client:
                    resp = await client.get(
                        inputs.url, params=parts["query"] or None, headers=parts["headers"] or None
                    )
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
