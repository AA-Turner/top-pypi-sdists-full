"""An archived organization admits no request — the gate states the database's rule.

The break this catches (2026-10-01): the server admitted ``POST /files/upload``
and ``POST /agent-service/agents`` into an organization archived nine days
earlier, because admission asked only "is this person a member?". The database
asks more: ``iam.has_org_access_for`` joins ``iam.organizations ... archived_at
is null`` (ACCESS LADDER T-33). A resolver that knows the organization is
archived raises ``OrganizationArchived``; these tests prove the middleware turns
that into its own refusal — before routing, for the platform-admin lane too —
with a remedy the person can act on (restore it), and never into "not a
member" (wrong repair) or "could not verify, try again" (an outage it is not).

The resolver here is a stand-in for the host's database read; the host's read
itself is proved against the nightly clone in
``aidream/services/organizations/tests/test_archived_organization_admission_live.py``.
"""

from __future__ import annotations

import json
import time

import jwt
import pytest
from matrx_connect.middleware.auth import AuthMiddleware, OrganizationArchived

JWT_SECRET = "test-secret-do-not-use-in-prod-test-secret-do-not-use-in-prod-AB"
USER_ID = "11111111-1111-4111-8111-111111111111"
LIVE_ORG_ID = "33333333-3333-4333-8333-333333333333"
ARCHIVED_ORG_ID = "66666666-6666-4666-8666-666666666666"


class _App:
    def __init__(self) -> None:
        self.entered = False

    async def __call__(self, scope, receive, send) -> None:
        self.entered = True
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b"ok"})


def _token() -> str:
    return jwt.encode(
        {"sub": USER_ID, "aud": "authenticated", "exp": int(time.time()) + 3600},
        JWT_SECRET,
        algorithm="HS256",
    )


async def _resolver(user_id: str, claimed: str | None) -> str | None:
    """The person is a member of BOTH; one of the two is archived."""
    if claimed == ARCHIVED_ORG_ID:
        raise OrganizationArchived(claimed)
    if claimed == LIVE_ORG_ID and user_id == USER_ID:
        return LIVE_ORG_ID
    return None


async def _admin_lane_admits_everything(user_id: str, organization_id: str) -> bool:
    return True


def _middleware(app: _App, *, admin_lane: bool = False) -> AuthMiddleware:
    return AuthMiddleware(
        app,
        jwt_secret=JWT_SECRET,
        resolve_active_organization=_resolver,
        admin_lane_admission=_admin_lane_admits_everything if admin_lane else None,
        log_requests=False,
    )


async def _call(mw: AuthMiddleware, headers: dict[str, str]) -> tuple[int, dict | bytes]:
    sent: list[dict] = []

    async def send(message: dict) -> None:
        sent.append(message)

    async def receive() -> dict:
        return {"type": "http.request", "body": b"", "more_body": False}

    scope = {
        "type": "http",
        "method": "POST",
        "path": "/files/upload",
        "query_string": b"",
        "headers": [(k.lower().encode(), v.encode()) for k, v in headers.items()],
        "client": ("127.0.0.1", 12345),
        "state": {},
    }
    await mw(scope, receive, send)
    status = next(m["status"] for m in sent if m["type"] == "http.response.start")
    body = b"".join(m.get("body", b"") for m in sent if m["type"] == "http.response.body")
    try:
        return status, json.loads(body)
    except ValueError:
        return status, body


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("organization_id", "expected_status", "expected_entered"),
    [(ARCHIVED_ORG_ID, 400, False), (LIVE_ORG_ID, 200, True)],
)
async def test_a_member_is_refused_in_an_archived_organization_and_admitted_in_a_live_one(
    organization_id: str, expected_status: int, expected_entered: bool
) -> None:
    app = _App()
    status, _ = await _call(
        _middleware(app),
        {"authorization": f"Bearer {_token()}", "x-organization-id": organization_id},
    )
    assert status == expected_status
    assert app.entered is expected_entered


@pytest.mark.asyncio
async def test_the_refusal_names_the_archive_and_the_restore_remedy() -> None:
    app = _App()
    status, body = await _call(
        _middleware(app),
        {"authorization": f"Bearer {_token()}", "x-organization-id": ARCHIVED_ORG_ID},
    )
    assert status == 400
    assert isinstance(body, dict)
    assert body["code"] == "organization_archived"
    assert body["claimed_organization_id"] == ARCHIVED_ORG_ID
    assert "Restore" in body["user_message"]
    # Not "ask an admin to add you" (membership is not the problem) and not
    # "try again" (nothing changes until someone restores it).
    assert "not a member" not in body["message"]
    assert "Try again" not in body["user_message"]


@pytest.mark.asyncio
async def test_the_platform_admin_lane_does_not_open_an_archived_organization() -> None:
    app = _App()
    status, body = await _call(
        _middleware(app, admin_lane=True),
        {
            "authorization": f"Bearer {_token()}",
            "x-organization-id": ARCHIVED_ORG_ID,
            "x-matrx-admin-lane": "1",
        },
    )
    assert status == 400
    assert app.entered is False
    assert isinstance(body, dict) and body["code"] == "organization_archived"
