"""A membership lookup that never answers is a bounded, honest 503 — never a hang.

Incident 2026-09-25: files.matrxserver.com's membership resolver
(``iam.has_org_access_for`` through matrx-orm) queued forever behind a wedged
pool lock. ``AuthMiddleware`` awaited it with no deadline, so every signed-in
request that named an organization hung 30–45 s (until the browser gave up) and
the file page showed a gray placeholder with no reason. The request must end in
bounded time with words a person can act on, and a status that says "retry"
(503), not "your request is wrong" (400).
"""

from __future__ import annotations

import asyncio
import json
import time

import pytest

from tests.test_auth_middleware_organization_admission import (
    JWT_SECRET,
    ORG_ID,
    _App,
    _call,
    _token,
)
from matrx_connect.middleware.auth import AuthMiddleware


async def _resolver_that_never_answers(user_id: str, claimed: str | None) -> str | None:
    await asyncio.Event().wait()  # a database that stopped answering
    return claimed


@pytest.mark.asyncio
async def test_hung_membership_lookup_answers_503_in_words_within_the_deadline() -> None:
    app = _App()
    mw = AuthMiddleware(
        app,
        jwt_secret=JWT_SECRET,
        resolve_active_organization=_resolver_that_never_answers,
        organization_resolve_timeout=0.5,
        log_requests=False,
    )
    started = time.monotonic()
    status, body = await asyncio.wait_for(
        _call(
            mw,
            "/files/abc",
            {"authorization": f"Bearer {_token()}", "x-organization-id": ORG_ID},
        ),
        timeout=10,  # the test's backstop; the knob is 0.5 s
    )
    elapsed = time.monotonic() - started
    assert elapsed < 3, f"admission took {elapsed:.1f}s behind a hung resolver"
    assert status == 503
    assert app.entered is False
    detail = json.loads(body)
    assert detail["code"] == "organization_unverifiable"
    assert ORG_ID not in detail["message"]  # the id is a field, never the sentence (VERIFIER-31 D2)
    assert detail["claimed_organization_id"] == ORG_ID
    assert "try again" in detail["user_message"].lower()
