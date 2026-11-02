"""THE RECORD-GRANT LANE (W-66, 2026-10-01).

A person given a record by share may act on THAT record in the record's own
organization without being a member of it (access ladder: sharing works at
every level; access never depends on membership). The middleware asks the
host's ``record_grant_admission`` hook — and only after membership refused.

Locked here:
* a non-member whose hook says yes is admitted with the claimed org VERIFIED and
  ``organization_admitted_by == "record_grant"`` (never mistaken for membership)
* a non-member whose hook says no is refused exactly as before (organization_forbidden)
* without a hook, admission is unchanged (organization_forbidden)
* a member never reaches the hook (membership answers first)
* a hook that raises is ``organization_unverifiable`` (503), never an admission
* a path with an encoded separator never reaches the hook
"""

from __future__ import annotations

import json
import time

import jwt
import pytest
from matrx_connect.middleware.auth import AuthMiddleware

JWT_SECRET = "test-secret-do-not-use-in-prod-test-secret-do-not-use-in-prod-AB"
USER_ID = "11111111-1111-4111-8111-111111111111"
MEMBER_ORG = "33333333-3333-4333-8333-333333333333"
RECORD_ORG = "44444444-4444-4444-8444-444444444444"
TURN_PATH = "/api/ai/conversations/75ccac71-9ecd-4d99-b610-8f73bff37307"


class _App:
    def __init__(self) -> None:
        self.entered = False
        self.context = None

    async def __call__(self, scope, receive, send) -> None:
        self.entered = True
        self.context = (scope.get("state") or {}).get("context")
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b"ok"})


def _token() -> str:
    return jwt.encode(
        {"sub": USER_ID, "aud": "authenticated", "exp": int(time.time()) + 3600},
        JWT_SECRET,
        algorithm="HS256",
    )


async def _member_only(user_id: str, claimed: str | None) -> str | None:
    return MEMBER_ORG if claimed == MEMBER_ORG else None


class _Hook:
    def __init__(self, answer: bool | Exception) -> None:
        self.answer = answer
        self.calls: list[tuple[str, str, str, str]] = []

    async def __call__(self, user_id: str, org: str, method: str, path: str) -> bool:
        self.calls.append((user_id, org, method, path))
        if isinstance(self.answer, Exception):
            raise self.answer
        return self.answer


async def _call(mw, path: str, org: str, *, raw_path: bytes | None = None):
    sent: list[dict] = []

    async def send(message: dict) -> None:
        sent.append(message)

    async def receive() -> dict:
        return {"type": "http.request", "body": b"", "more_body": False}

    scope = {
        "type": "http",
        "method": "POST",
        "path": path,
        "raw_path": raw_path if raw_path is not None else path.encode(),
        "query_string": b"",
        "headers": [
            (b"authorization", f"Bearer {_token()}".encode()),
            (b"x-organization-id", org.encode()),
        ],
        "client": ("127.0.0.1", 1),
        "state": {},
    }
    await mw(scope, receive, send)
    status = next(m["status"] for m in sent if m["type"] == "http.response.start")
    body = b"".join(m.get("body", b"") for m in sent if m["type"] == "http.response.body")
    return status, body


def _mw(app, hook=None) -> AuthMiddleware:
    kwargs = {"record_grant_admission": hook} if hook is not None else {}
    return AuthMiddleware(
        app,
        jwt_secret=JWT_SECRET,
        resolve_active_organization=_member_only,
        log_requests=False,
        **kwargs,
    )


@pytest.mark.asyncio
async def test_share_grantee_is_admitted_in_the_records_organization() -> None:
    app, hook = _App(), _Hook(True)
    status, _ = await _call(_mw(app, hook), TURN_PATH, RECORD_ORG)
    assert status == 200 and app.entered
    assert hook.calls == [(USER_ID, RECORD_ORG, "POST", TURN_PATH)]
    ctx = app.context
    assert ctx.organization_id == RECORD_ORG
    assert ctx.organization_admission == "verified"
    assert ctx.metadata["organization_admitted_by"] == "record_grant"


@pytest.mark.asyncio
async def test_hook_refusal_is_the_same_denial_as_before() -> None:
    app = _App()
    status, body = await _call(_mw(app, _Hook(False)), TURN_PATH, RECORD_ORG)
    assert status == 400 and not app.entered
    assert json.loads(body)["code"] == "organization_forbidden"


@pytest.mark.asyncio
async def test_without_a_hook_admission_is_unchanged() -> None:
    app = _App()
    status, body = await _call(_mw(app), TURN_PATH, RECORD_ORG)
    assert status == 400 and not app.entered
    assert json.loads(body)["code"] == "organization_forbidden"


@pytest.mark.asyncio
async def test_a_member_never_reaches_the_hook() -> None:
    app, hook = _App(), _Hook(True)
    status, _ = await _call(_mw(app, hook), TURN_PATH, MEMBER_ORG)
    assert status == 200 and hook.calls == []
    assert "organization_admitted_by" not in (app.context.metadata or {})


@pytest.mark.asyncio
async def test_a_hook_that_raises_is_unverifiable_never_admitted() -> None:
    app = _App()
    status, body = await _call(_mw(app, _Hook(RuntimeError("db down"))), TURN_PATH, RECORD_ORG)
    assert status == 503 and not app.entered
    assert json.loads(body)["code"] == "organization_unverifiable"


@pytest.mark.asyncio
async def test_an_encoded_separator_never_reaches_the_hook() -> None:
    app, hook = _App(), _Hook(True)
    status, _ = await _call(
        _mw(app, hook), TURN_PATH, RECORD_ORG, raw_path=b"/api/ai/conversations%2Fx"
    )
    assert status == 400 and hook.calls == []
