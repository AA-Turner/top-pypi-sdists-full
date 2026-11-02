"""A transient authority outage is retried within a bounded budget before any refusal.

Incident 2026-10-19 22:50:51Z (real test PB-08, turn 6, conversation 050f3865-...): the database
stalled for ~30 s on one task (pool pressure, an idle-in-transaction session holding locks, event
loop stalls). The per-request current-login check (``auth.sessions`` row by id) missed its single
5 s deadline once, and an ordinary chat continuation was refused 503 ``session_authority_unavailable``
— one attempt, no second chance, the person's message never reached the server. Every authority
check that can only fail transiently (current login, file-session source, organization membership)
now gets a bounded number of attempts inside a bounded budget; a still-failing check stays the same
honest retryable 503, and a check that DECIDED (revoked, not a member) is never retried.
"""

from __future__ import annotations

import asyncio
import json
import time

import pytest

from matrx_connect.middleware.auth import AuthMiddleware
from tests.test_auth_middleware_organization_admission import (
    JWT_SECRET,
    ORG_ID,
    _App,
    _call,
    _token,
)


def _flaky(failures: int, answer, *, hang: bool = True):
    calls: list[float] = []

    async def resolver(*_args):
        calls.append(time.monotonic())
        if len(calls) <= failures:
            if hang:
                await asyncio.Event().wait()  # a database that stopped answering this once
            raise ConnectionError("synthetic transient pool failure")
        return answer if not callable(answer) else answer(*_args)

    return resolver, calls


@pytest.mark.asyncio
@pytest.mark.parametrize("hang", [True, False], ids=["timeout", "exception"])
async def test_one_missed_login_check_is_retried_and_the_turn_is_admitted(hang: bool) -> None:
    resolver, calls = _flaky(1, True, hang=hang)
    app = _App()
    mw = AuthMiddleware(app, jwt_secret=JWT_SECRET, resolve_current_session=resolver,
                        session_resolve_timeout=0.2, log_requests=False)
    status, _body = await asyncio.wait_for(
        _call(mw, "/ai/conversations/x", {"authorization": f"Bearer {_token()}", "x-organization-id": ORG_ID}), timeout=10)
    assert status == 200, "a single transient miss of the session check refused the person's turn"
    assert app.entered is True
    assert len(calls) == 2


@pytest.mark.asyncio
async def test_a_revoked_login_is_never_retried_into_admission() -> None:
    resolver, calls = _flaky(0, False)
    app = _App()
    mw = AuthMiddleware(app, jwt_secret=JWT_SECRET, resolve_current_session=resolver,
                        session_resolve_timeout=0.2, log_requests=False)
    status, _body = await _call(mw, "/ai/conversations/x", {"authorization": f"Bearer {_token()}", "x-organization-id": ORG_ID})
    # A refused login is anonymous here (each route decides whether it needs a person).
    assert status == 200 and app.entered is True
    assert not getattr(app.context, "is_authenticated", False)
    assert len(calls) == 1  # a decision is final; only "could not decide" is retried


@pytest.mark.asyncio
async def test_a_lasting_outage_stays_an_honest_retryable_503_within_the_budget() -> None:
    resolver, calls = _flaky(10_000, True)
    app = _App()
    mw = AuthMiddleware(app, jwt_secret=JWT_SECRET, resolve_current_session=resolver,
                        session_resolve_timeout=0.2, log_requests=False)
    started = time.monotonic()
    status, body = await asyncio.wait_for(
        _call(mw, "/ai/conversations/x", {"authorization": f"Bearer {_token()}", "x-organization-id": ORG_ID}), timeout=10)
    elapsed = time.monotonic() - started
    assert status == 503
    assert json.loads(body)["code"] == "session_authority_unavailable"
    assert json.loads(body)["retryable"] is True
    assert app.entered is False
    assert len(calls) == 3, f"expected a bounded 3 attempts, saw {len(calls)}"
    assert elapsed < 0.2 * 3 + 1.5, f"retry budget not bounded: {elapsed:.2f}s"


@pytest.mark.asyncio
async def test_one_missed_membership_check_is_retried_before_organization_unverifiable() -> None:
    resolver, calls = _flaky(1, lambda _user, claimed: claimed, hang=False)
    app = _App()
    mw = AuthMiddleware(app, jwt_secret=JWT_SECRET, resolve_active_organization=resolver,
                        organization_resolve_timeout=0.2, log_requests=False)
    status, body = await asyncio.wait_for(
        _call(mw, "/ai/conversations/x",
              {"authorization": f"Bearer {_token()}", "x-organization-id": ORG_ID}), timeout=10)
    assert status == 200, f"a single transient membership miss refused the turn: {body[:200]!r}"
    assert app.entered is True
    assert len(calls) == 2
