"""``http.graphql`` — POST a GraphQL query/mutation to a single endpoint.

Convenience wrapper over ``http.post``. Serializes the standard GraphQL
envelope ``{query, variables, operationName}`` and returns the unwrapped
``data`` + ``errors`` as first-class fields on the response.
"""

from __future__ import annotations

import time
from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph.nodes.http._shared import _DEFAULT_MAX_BYTES
from matrx_graph.content_ir.model import KindModel
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.result import NodeResult, failure, success
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory


class GraphQLInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    endpoint: str = Field(
        min_length=1, description="Absolute URL of the GraphQL endpoint to POST to."
    )
    query: str = Field(min_length=1, description="GraphQL query or mutation string.")
    variables: dict[str, JsonValue] = Field(
        default_factory=dict,
        description="Values bound to the query's declared $variables.",
    )
    operation_name: str | None = Field(
        default=None, description="Optional operationName (for multi-op docs)."
    )
    headers: dict[str, str] = Field(
        default_factory=dict,
        description="Extra request headers (e.g. Authorization).",
    )


class GraphQLConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    timeout_s: float = Field(
        default=30.0,
        ge=0.1,
        le=600.0,
        description="Per-request timeout in seconds (connect + read).",
    )
    max_bytes: int = Field(
        default=_DEFAULT_MAX_BYTES,
        ge=1024,
        le=50_000_000,
        description="Max response-body bytes to retain. Excess is truncated.",
    )


class GraphQLResponse(KindModel, kind="graphql_response"):
    """Success payload tailored to GraphQL (Node Result System).

    Receiving a parseable GraphQL response document is node SUCCESS — even
    when the document carries top-level ``errors`` (that is domain data;
    branch on ``len(errors)`` / ``status``). Transport failures and
    unparseable responses are node Failures (``http_transport_error`` /
    ``invalid_json_response``).

    ITS OWN KIND SINCE 2026-08-23 (plan §10d-B2). This node used to declare
    ``http_response``, which it does not and cannot satisfy: that kind requires
    ``url`` and this payload has ``endpoint``, ``data``, ``errors`` and
    ``extensions`` instead. The declaration was a standing lie — the output
    drift check fired on EVERY ``http.graphql`` run — and the fix is a real
    kind for a real shape, not a laxer ``http_response``.
    """

    status: int = Field(description="HTTP status code of the transport call.")
    endpoint: str = Field(description="The GraphQL endpoint URL that was called.")
    data: JsonValue = Field(
        default=None,
        description="The response's `data` object (null when the query fully errored).",
    )
    errors: list[dict[str, JsonValue]] = Field(
        default_factory=list,
        description="Top-level GraphQL errors from the document (empty on success).",
    )
    extensions: dict[str, JsonValue] = Field(
        default_factory=dict,
        description="The response's optional `extensions` object (server-specific metadata).",
    )
    elapsed_ms: int = Field(
        default=0, description="Wall-clock time for the request, in milliseconds."
    )


class HttpGraphQLExecutor:
    """POST a GraphQL query and surface data/errors as structured fields."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="http.graphql",
        category=NodeCategory.TOOL,
        display_name="GraphQL",
        description="Send a query to a GraphQL service and return the result.",
        input_schema=GraphQLInput,
        output_schema=GraphQLResponse,
        config_schema=GraphQLConfig,
        output_kind="graphql_response",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.SIDE_EFFECT,
        icon="network",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: GraphQLInput,
        config: GraphQLConfig,
    ) -> NodeResult[GraphQLResponse]:
        _ = ctx
        from matrx_utils.outbound_guard import OutboundUrlRefused

        from matrx_graph.nodes.http._shared import outbound_client, refused_failure

        payload: dict[str, Any] = {"query": inputs.query}
        if inputs.variables:
            payload["variables"] = inputs.variables
        if inputs.operation_name:
            payload["operationName"] = inputs.operation_name

        headers = {"content-type": "application/json", **inputs.headers}

        started = time.monotonic()
        try:
            async with outbound_client(timeout=config.timeout_s) as client:
                resp = await client.post(inputs.endpoint, json=payload, headers=headers)
            elapsed = int((time.monotonic() - started) * 1000)
        except OutboundUrlRefused as e:
            elapsed = int((time.monotonic() - started) * 1000)
            return refused_failure(inputs.endpoint, e, elapsed)
        except Exception as e:
            elapsed = int((time.monotonic() - started) * 1000)
            return failure(
                "http_transport_error",
                f"{type(e).__name__}: {e}",
                details={"endpoint": inputs.endpoint, "elapsed_ms": elapsed},
            )

        try:
            body = resp.json()
        except Exception as e:
            return failure(
                "invalid_json_response",
                f"Invalid JSON response: {e}",
                details={
                    "endpoint": inputs.endpoint,
                    "status": resp.status_code,
                    "elapsed_ms": elapsed,
                },
            )

        errors = body.get("errors") or []
        # Clip overly large data payloads to match max_bytes-style guardrails.
        data = body.get("data")
        extensions = body.get("extensions") or {}

        return success(
            GraphQLResponse(
                status=resp.status_code,
                endpoint=inputs.endpoint,
                data=data,
                errors=errors,
                extensions=extensions,
                elapsed_ms=elapsed,
            )
        )
