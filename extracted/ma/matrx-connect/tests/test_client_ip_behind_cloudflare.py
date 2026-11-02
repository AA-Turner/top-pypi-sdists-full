"""The client IP is the person, never the Cloudflare edge — and never a typed header.

2026-09-30: production runs Cloudflare -> ALB -> uvicorn, and uvicorn trusts only
the ALB, so ``request.client.host`` was always a Cloudflare edge: 90% of
``ops.api_request_log`` addresses were edges (one edge = 25,832 rows) and guest
minting, request logs and a per-IP rate limit all keyed on them. A sibling reader
took the LEFT-MOST ``X-Forwarded-For`` — a value the caller types — for secure
delivery's IP pinning.

The rule (``matrx_connect.client_ip``): a Cloudflare peer's ``CF-Connecting-IP`` is
the client; any other peer IS the client; ``X-Forwarded-For`` is never read.
"""

from __future__ import annotations

import pytest
from matrx_connect import client_ip, is_cloudflare_ip, resolve_client_ip
from matrx_connect.client_ip import CLOUDFLARE_IP_RANGES
from matrx_connect.middleware.auth import AuthMiddleware
from starlette.requests import Request

CF_EDGE_V4 = "172.70.42.17"  # inside 172.64.0.0/13
CF_EDGE_V6 = "2a06:98c1:3120::7"  # inside 2a06:98c0::/29
REAL_USER = "203.0.113.45"
REAL_USER_V6 = "2001:db8::abcd"
ATTACKER = "198.51.100.9"
VICTIM_PINNED = "192.0.2.77"


def _request(peer: str | None, headers: dict[str, str]) -> Request:
    return Request(
        {
            "type": "http",
            "method": "GET",
            "path": "/",
            "query_string": b"",
            "headers": [(k.lower().encode(), v.encode()) for k, v in headers.items()],
            "client": (peer, 443) if peer else None,
        }
    )


def test_edge_peer_with_cf_connecting_ip_is_the_real_person() -> None:
    req = _request(CF_EDGE_V4, {"CF-Connecting-IP": REAL_USER})
    assert client_ip(req) == REAL_USER


def test_ipv6_edge_peer_with_cf_connecting_ip_is_the_real_person() -> None:
    req = _request(CF_EDGE_V6, {"CF-Connecting-IP": REAL_USER_V6})
    assert client_ip(req) == REAL_USER_V6


def test_ipv4_mapped_edge_peer_is_recognized() -> None:
    req = _request(f"::ffff:{CF_EDGE_V4}", {"CF-Connecting-IP": REAL_USER})
    assert client_ip(req) == REAL_USER


def test_non_cloudflare_peer_cannot_spoof_cf_connecting_ip() -> None:
    # The origin is reachable bypassing Cloudflare; the header is attacker-typed there.
    req = _request(ATTACKER, {"CF-Connecting-IP": VICTIM_PINNED})
    assert client_ip(req) == ATTACKER


@pytest.mark.parametrize("peer", [ATTACKER, CF_EDGE_V4])
def test_left_most_x_forwarded_for_never_wins(peer: str) -> None:
    headers = {"X-Forwarded-For": f"{VICTIM_PINNED}, {ATTACKER}", "X-Real-IP": VICTIM_PINNED}
    if peer == CF_EDGE_V4:
        headers["CF-Connecting-IP"] = REAL_USER
    got = client_ip(_request(peer, headers))
    assert got != VICTIM_PINNED
    assert got == (REAL_USER if peer == CF_EDGE_V4 else ATTACKER)


@pytest.mark.parametrize("header", [None, "", "not-an-ip", "1.2.3.4, 5.6.7.8", "999.1.1.1"])
def test_edge_peer_with_missing_or_garbage_header_falls_back_to_the_peer(
    header: str | None,
) -> None:
    headers = {} if header is None else {"CF-Connecting-IP": header}
    assert client_ip(_request(CF_EDGE_V4, headers)) == CF_EDGE_V4


def test_no_peer_is_none() -> None:
    assert client_ip(_request(None, {"CF-Connecting-IP": REAL_USER})) is None
    assert resolve_client_ip(None, {}) is None


def test_ranges_are_parseable_and_cover_both_families() -> None:
    assert is_cloudflare_ip(CF_EDGE_V4)
    assert is_cloudflare_ip(CF_EDGE_V6)
    assert not is_cloudflare_ip(REAL_USER)
    assert not is_cloudflare_ip("garbage")
    assert any(":" in cidr for cidr in CLOUDFLARE_IP_RANGES)
    assert any(":" not in cidr for cidr in CLOUDFLARE_IP_RANGES)


# ── The AppContext the auth middleware mints carries the real person's IP ──


class _App:
    def __init__(self) -> None:
        self.context = None

    async def __call__(self, scope, receive, send) -> None:
        self.context = (scope.get("state") or {}).get("context")
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b"ok"})


async def _ctx_ip(peer: str, headers: dict[str, str]) -> str | None:
    app = _App()
    mw = AuthMiddleware(app, jwt_secret="x" * 64, log_requests=False)
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/files/00000000-0000-4000-8000-000000000000/download",
        "query_string": b"",
        "headers": [(k.lower().encode(), v.encode()) for k, v in headers.items()],
        "client": (peer, 443),
        "state": {},
    }

    async def receive() -> dict:
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message: dict) -> None:
        return None

    await mw(scope, receive, send)
    assert app.context is not None
    return app.context.ip_address


@pytest.mark.asyncio
async def test_middleware_context_ip_is_the_person_behind_the_edge() -> None:
    assert await _ctx_ip(CF_EDGE_V4, {"CF-Connecting-IP": REAL_USER}) == REAL_USER


@pytest.mark.asyncio
async def test_middleware_context_ip_refuses_spoofed_headers_from_a_direct_peer() -> None:
    ip = await _ctx_ip(
        ATTACKER, {"CF-Connecting-IP": VICTIM_PINNED, "X-Forwarded-For": VICTIM_PINNED}
    )
    assert ip == ATTACKER
