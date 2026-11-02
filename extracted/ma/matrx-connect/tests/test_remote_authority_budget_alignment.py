"""A host asking a remote authority never gives up while that authority is still inside its budget.

2026-10-21: the Files service asked aidream's ``/auth/session/status`` with a 3 s deadline per try,
while aidream's own login lookup behind that URL allows 5 s per attempt and three attempts. Whenever
aidream's lookup took longer than 3 s, Files abandoned a check aidream would have answered and
refused the person ``session_authority_unavailable``. The outer side's ONE try now outlasts the inner
side's WHOLE budget, and the outer per-attempt deadline never cuts a remote try short. These numbers
are derived from one formula (``authority_budget_seconds``), so they cannot drift apart silently.
"""

from __future__ import annotations

import asyncio
import time

import httpx
import jwt
import pytest

from matrx_connect.middleware.auth import AuthMiddleware
from matrx_connect.middleware.authority_retry import (
    DEFAULT_SESSION_ATTEMPT_SECONDS,
    authority_budget_seconds,
)
from matrx_connect.middleware.remote_file_session import RemoteFileSessionResolver
from matrx_connect.middleware.remote_session import RemoteSessionResolver
from matrx_connect.middleware.session_authority import SessionAuthorityUnavailable

URL = "https://authority.example/auth/session/status"
SECRET = "synthetic-test-key-not-a-deployment-secret"
SUBJECT = "00000000-0000-4000-8000-000000000001"
SESSION = "00000000-0000-4000-8000-000000000002"
INNER_TOTAL = authority_budget_seconds(DEFAULT_SESSION_ATTEMPT_SECONDS)


def _resolvers():
    return [RemoteSessionResolver(URL), RemoteFileSessionResolver(URL, b"synthetic-signing-key")]


@pytest.mark.parametrize("resolver", _resolvers(), ids=["login", "file-session"])
def test_one_outer_try_outlasts_the_whole_inner_budget(resolver) -> None:
    assert resolver.timeout_seconds > INNER_TOTAL, (
        f"{type(resolver).__name__} gives up after {resolver.timeout_seconds}s per try; the authority "
        f"behind it may take {INNER_TOTAL:.2f}s before it answers"
    )


@pytest.mark.parametrize("resolver", _resolvers(), ids=["login", "file-session"])
def test_the_outer_attempt_never_cuts_a_remote_try_short(resolver) -> None:
    kwargs = {"resolve_current_session": resolver} if isinstance(resolver, RemoteSessionResolver) else {
        "resolve_file_session": resolver}
    mw = AuthMiddleware(lambda *_: None, jwt_secret=SECRET, log_requests=False, **kwargs)
    assert mw._session_resolve_timeout >= resolver.timeout_seconds
    assert authority_budget_seconds(mw._session_resolve_timeout) > INNER_TOTAL


@pytest.mark.asyncio
async def test_a_slow_but_answering_authority_admits_the_person(monkeypatch) -> None:
    """Scaled down: the authority answers in 0.4 s; the host's own attempt deadline is 0.2 s."""
    expires = int(time.time()) + 3600
    token = jwt.encode({"sub": SUBJECT, "session_id": SESSION, "aud": "authenticated", "exp": expires},
                       SECRET, algorithm="HS256")
    calls = 0

    async def slow_authority(_request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        await asyncio.sleep(0.4)  # aidream still inside its own budget
        return httpx.Response(200, json={"user_id": SUBJECT, "session_id": SESSION, "expires_at": expires})

    original = httpx.AsyncClient
    monkeypatch.setattr(httpx, "AsyncClient",
                        lambda **kw: original(**kw, transport=httpx.MockTransport(slow_authority)))
    mw = AuthMiddleware(lambda *_: None, jwt_secret=SECRET, log_requests=False,
                        resolve_current_session=RemoteSessionResolver(URL, timeout_seconds=1.0),
                        session_resolve_timeout=0.2)
    try:
        verified = await asyncio.wait_for(mw.verify_token_raw(token), timeout=10)
    except SessionAuthorityUnavailable:
        verified = "refused"
    assert verified not in (None, "refused"), (
        f"refused after {calls} abandoned tries to an authority that answers in 0.4 s")
    assert calls == 1
