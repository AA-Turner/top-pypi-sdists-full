"""``http.custom_api`` — request with pluggable auth + retries.

Sits above ``http.get`` / ``http.post`` for cases where a workflow hits a
third-party API that needs bearer tokens, API keys in headers, or query-
string auth, with exponential-backoff retries on 5xx and 429. The plain
GET/POST nodes intentionally stay simple; this node is where we take on
the extra complexity without polluting them.

Auth modes (choose one via ``auth_type``; set ``auth_value`` accordingly):
- ``none``    — no auth header added
- ``bearer``  — ``Authorization: Bearer <auth_value>``
- ``basic``   — ``Authorization: Basic <base64(user:pass)>`` where
                ``auth_value`` = ``user:pass``
- ``api_key_header`` — header named by ``auth_header_name``,
                       value = ``auth_value``
- ``api_key_query``  — query param named by ``auth_param_name``,
                       value = ``auth_value``

Retry policy:
- Triggers on 429, 500, 502, 503, 504, or any transport exception.
- Exponential backoff with jitter: 0.5s, 1s, 2s, 4s, 8s, capped by
  ``max_backoff_s``. Respects ``Retry-After`` (seconds or HTTP-date) when
  present on a 429/503.
- Declared SIDE_EFFECT because retries on non-idempotent POSTs can
  double-submit. For truly idempotent endpoints, set
  ``re_execute_on_resume=False`` on the node (default) so the resume
  path uses the prior outcome instead.
"""

from __future__ import annotations

import asyncio
import base64
import random
import time
from email.utils import parsedate_to_datetime
from typing import Any, ClassVar, Literal

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
from matrx_graph.types.usl import field_extras

_RETRY_STATUSES = frozenset({408, 425, 429, 500, 502, 503, 504})


class CustomApiInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"] = Field(
        default="GET", description="HTTP verb sent to the endpoint (default GET)."
    )
    url: str = Field(min_length=1, description="Absolute URL to request.")
    query: dict[str, TextOrSecret] = Field(
        default_factory=dict,
        description='Query string parameters appended to the URL. A value may be {"$secret": "<name>"}.',
    )
    headers: dict[str, TextOrSecret] = Field(
        default_factory=dict,
        description="Extra request headers (merged with any auth header). A value may be "
        '{"$secret": "<name>"}.',
    )

    json_body: JsonValue = Field(
        default=None,
        description="JSON body. Sets Content-Type: application/json.",
    )
    form: dict[str, TextOrSecret] | None = Field(
        default=None,
        description='Form-encoded body (application/x-www-form-urlencoded). A value may be {"$secret": "<name>"}.',
    )
    text: str | None = Field(
        default=None, description="Raw text body (pair with a Content-Type header)."
    )

    # Auth
    auth_type: Literal["none", "bearer", "basic", "api_key_header", "api_key_query"] = Field(
        default="none",
        description="Auth mode: none · bearer · basic · api_key_header · "
        "api_key_query. Pair with auth_value.",
    )
    auth_value: TextOrSecret | None = Field(
        default=None,
        description="Bearer token, 'user:pass' for basic, or API key string — or "
        '{"$secret": "<name>"} to use a stored secret (recommended: the value is never shown).',
        json_schema_extra=field_extras(widget="password"),
    )
    auth_header_name: str = Field(
        default="X-API-Key",
        description="Header name for ``api_key_header`` auth mode.",
    )
    auth_param_name: str = Field(
        default="api_key",
        description="Query-param name for ``api_key_query`` auth mode.",
    )


class CustomApiConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    timeout_s: float = Field(
        default=30.0,
        ge=0.1,
        le=600.0,
        description="Per-attempt timeout in seconds (connect + read).",
    )
    max_bytes: int = Field(
        default=_DEFAULT_MAX_BYTES,
        ge=1024,
        le=50_000_000,
        description="Max response-body bytes to retain. Excess is truncated.",
    )
    follow_redirects: bool = Field(
        default=True, description="Follow HTTP 3xx redirects automatically."
    )

    max_retries: int = Field(
        default=3,
        ge=0,
        le=10,
        description="Total retries after the initial attempt.",
    )
    backoff_base_s: float = Field(
        default=0.5,
        ge=0.0,
        le=30.0,
        description="Base delay for exponential backoff between retries, in seconds.",
    )
    max_backoff_s: float = Field(
        default=30.0,
        ge=0.1,
        le=300.0,
        description="Ceiling on the backoff delay between retries, in seconds.",
    )
    respect_retry_after: bool = Field(
        default=True,
        description="Honor a server Retry-After header (when present on any "
        "retryable response) instead of the computed backoff delay.",
    )


def _apply_auth(
    inputs: CustomApiInput,
    headers: dict[str, str],
    query: dict[str, str],
    auth_value: str | None,
) -> tuple[dict[str, str], dict[str, str], str | None]:
    """Return (headers, query, derived) with auth applied — ``derived`` is any value built FROM
    the auth value (the base64 basic credential) that must be redacted alongside it."""
    headers = dict(headers)
    query = dict(query)

    if inputs.auth_type == "none" or auth_value is None:
        return headers, query, None

    derived: str | None = None
    if inputs.auth_type == "bearer":
        headers["authorization"] = f"Bearer {auth_value}"
    elif inputs.auth_type == "basic":
        derived = base64.b64encode(auth_value.encode("utf-8")).decode("ascii")
        headers["authorization"] = f"Basic {derived}"
    elif inputs.auth_type == "api_key_header":
        headers[inputs.auth_header_name.lower()] = auth_value
    elif inputs.auth_type == "api_key_query":
        query[inputs.auth_param_name] = auth_value

    return headers, query, derived


def _parse_retry_after(header: str | None) -> float | None:
    """Return seconds to wait per a Retry-After header, or None."""
    if not header:
        return None
    header = header.strip()
    # Numeric seconds
    try:
        return max(0.0, float(header))
    except ValueError:
        pass
    # HTTP-date
    try:
        dt = parsedate_to_datetime(header)
        if dt is None:
            return None
        now = dt.utcnow().timestamp() if dt.tzinfo is None else time.time()
        delta = dt.timestamp() - now
        return max(0.0, delta)
    except (TypeError, ValueError):
        return None


def _backoff_delay(attempt: int, base: float, cap: float) -> float:
    raw = base * (2**attempt)
    jitter = random.uniform(0, base)  # full-jitter-style
    return min(cap, raw) + jitter


class CustomApiExecutor:
    """HTTP request with auth + retry on transient failure.

    Declared SIDE_EFFECT because any non-GET may mutate server state and
    retrying a partially-applied request can double-apply. Workflows that
    know better can pin ``re_execute_on_resume`` per-node.
    """

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="http.custom_api",
        category=NodeCategory.TOOL,
        display_name="Custom API Call",
        description="Call an outside service, with sign-in details and automatic retries.",
        input_schema=CustomApiInput,
        output_schema=HttpResponse,
        config_schema=CustomApiConfig,
        output_kind="http_response",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.SIDE_EFFECT,
        icon="key-round",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: CustomApiInput,
        config: CustomApiConfig,
    ) -> NodeResult[HttpResponse]:
        from matrx_utils.outbound_guard import OutboundUrlRefused

        prepared = await resolve_request_secrets(
            ctx,
            {
                "query": inputs.query,
                "headers": inputs.headers,
                "json_body": inputs.json_body,
                "form": inputs.form,
                "auth_value": inputs.auth_value,
            },
        )
        if isinstance(prepared, Failure):
            return prepared
        parts, found = prepared
        headers, query, derived = _apply_auth(
            inputs, parts["headers"], parts["query"], parts["auth_value"]
        )
        if derived and found:
            found.add("(encoded)", derived)

        kwargs: dict[str, Any] = {
            "params": query or None,
            "headers": headers or None,
        }
        if parts["json_body"] is not None:
            kwargs["json"] = parts["json_body"]
        elif parts["form"] is not None:
            kwargs["data"] = parts["form"]
        elif inputs.text is not None:
            kwargs["content"] = inputs.text

        attempts = config.max_retries + 1

        for attempt in range(attempts):
            started = time.monotonic()
            try:
                with found.active():
                    async with outbound_client(
                        timeout=config.timeout_s,
                        follow_redirects=config.follow_redirects,
                    ) as client:
                        resp = await client.request(inputs.method, inputs.url, **kwargs)
                elapsed = int((time.monotonic() - started) * 1000)

                if resp.status_code not in _RETRY_STATUSES or attempt == attempts - 1:
                    return success(
                        found.redact(
                            build_response_from_httpx(
                                resp, str(resp.url), elapsed, config.max_bytes
                            )
                        )
                    )

                # Retry path
                delay = None
                if config.respect_retry_after:
                    delay = _parse_retry_after(resp.headers.get("retry-after"))
                if delay is None:
                    delay = _backoff_delay(attempt, config.backoff_base_s, config.max_backoff_s)
                await asyncio.sleep(delay)
                continue

            except OutboundUrlRefused as e:
                # A refused address is the same on every attempt — never retried.
                elapsed = int((time.monotonic() - started) * 1000)
                return found.redact(refused_failure(inputs.url, e, elapsed))
            except Exception as e:
                elapsed = int((time.monotonic() - started) * 1000)
                if attempt == attempts - 1:
                    return found.redact(
                        transport_failure(inputs.url, f"{type(e).__name__}: {e}", elapsed)
                    )
                delay = _backoff_delay(attempt, config.backoff_base_s, config.max_backoff_s)
                await asyncio.sleep(delay)

        # Unreachable — the final attempt always returns above.
        return transport_failure(inputs.url, "retry loop exhausted", 0)
