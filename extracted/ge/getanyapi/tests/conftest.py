"""Shared test fixtures and a mock-transport harness for the getanyapi SDK.

Every test injects an ``httpx.MockTransport`` via ``http_client=`` so no real
network call happens. ``Recorder`` captures the requests the client made so
assertions can check the wire shape (method, path, query, body, headers).
"""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

import httpx


class Recorder:
    """Collects requests and serves scripted responses for MockTransport."""

    def __init__(
        self, responder: Callable[[httpx.Request], httpx.Response]
    ) -> None:
        self.requests: list[httpx.Request] = []
        self._responder = responder

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        return self._responder(request)

    @property
    def last(self) -> httpx.Request:
        return self.requests[-1]


def make_sync_client(
    responder: Callable[[httpx.Request], httpx.Response],
    **kwargs: Any,
) -> tuple[Any, Recorder]:
    from getanyapi import AnyAPI

    recorder = Recorder(responder)
    transport = httpx.MockTransport(recorder)
    client = AnyAPI(
        api_key="test-key",
        http_client=httpx.Client(transport=transport),
        **kwargs,
    )
    return client, recorder


def make_async_client(
    responder: Callable[[httpx.Request], httpx.Response],
    **kwargs: Any,
) -> tuple[Any, Recorder]:
    from getanyapi import AsyncAnyAPI

    recorder = Recorder(responder)
    transport = httpx.MockTransport(recorder)
    client = AsyncAnyAPI(
        api_key="test-key",
        http_client=httpx.AsyncClient(transport=transport),
        **kwargs,
    )
    return client, recorder


def run_envelope(
    data: Any,
    *,
    cost_usd: float = 0.001,
    items: int = 1,
    found: bool = True,
    replayed: bool = False,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a /v1/run response body (SPEC 4 fixture shape).

    ``items`` is always emitted: the gateway's field carries no ``omitempty``, so a
    body without it is not a body the wire can produce.
    """
    output = (
        {"found": True, "data": data}
        if found
        else {"found": False, "data": None}
    )
    body: dict[str, Any] = {
        "output": output,
        "provider": "AnyAPI",
        "costUsd": cost_usd,
        "items": items,
        "replayed": replayed,
    }
    if extra:
        body.update(extra)
    return body


def json_response(
    status: int,
    body: Any,
    *,
    headers: dict[str, str] | None = None,
) -> httpx.Response:
    return httpx.Response(
        status,
        content=json.dumps(body).encode(),
        headers={"content-type": "application/json", **(headers or {})},
    )
