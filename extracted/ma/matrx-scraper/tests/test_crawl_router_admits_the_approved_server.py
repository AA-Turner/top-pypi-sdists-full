"""The crawl router admits our own servers the same way the other five scraper routers do.

THE FINDING (2026-10-28). Every crawl a RESUMED or worker-run workflow started
died with ``401 token_required`` (workflow runs c498806a / 621a0de7, node
``crawl_sites``, both claimed by the shutdown-resume sweep). A background run
has no person's login token — by design, a stored one expires within the hour —
so aidream's scraper hop presents the approved-server secret plus
``X-Matrx-User-Id`` and ``X-Organization-Id``. The scrape, external, browser,
press-clip and preview routers admit that through ``require_authenticated_or_service``;
the crawl router alone was mounted ``require_authenticated`` (person's JWT only),
so the live scraper accepted the secret on ``/queue/stats`` (200) and refused the
SAME secret on ``/crawler/...`` (401 token_required).

A crawl writes rows owned by a person (``build_user_claims`` needs ``sub``), so the
crawl door also requires the acting user on the service path.
"""

from __future__ import annotations

import importlib

import pytest

fastapi = pytest.importorskip("fastapi", reason="server extra not installed")

from fastapi.testclient import TestClient  # noqa: E402

from matrx_scraper.server.app import create_app  # noqa: E402
from matrx_scraper.server.config import ServerConfig  # noqa: E402

SECRET = "test-approved-server-secret"
ACTING_USER = "88888888-8888-4888-8888-888888888888"
ORG_ID = "99999999-9999-4999-9999-999999999999"
SESSION_ID = "77777777-7777-4777-8777-777777777777"
PATH = f"/api/scraper/crawler/sessions/{SESSION_ID}/previous"


def _client() -> TestClient:
    return TestClient(create_app(ServerConfig(admin_api_token=SECRET)))


@pytest.fixture
def seen(monkeypatch: pytest.MonkeyPatch) -> dict[str, object]:
    """Stand in for the DB read so reaching the handler is observable."""
    captured: dict[str, object] = {}
    crawl_module = importlib.import_module("matrx_scraper.api.crawl_router")

    async def fake_load_previous_session(claims: dict, session_id: str):
        from matrx_connect import get_app_context

        captured["sub"] = claims.get("sub")
        captured["organization_id"] = get_app_context().organization_id
        raise LookupError(f"crawl session {session_id} not found")

    monkeypatch.setattr(crawl_module, "load_previous_session", fake_load_previous_session)
    return captured


def test_a_service_call_with_actor_and_organization_reaches_the_crawl_handler(
    seen: dict[str, object],
) -> None:
    response = _client().get(
        PATH,
        headers={
            "Authorization": f"Bearer {SECRET}",
            "X-Matrx-User-Id": ACTING_USER,
            "X-Organization-Id": ORG_ID,
        },
    )
    # 404 is the stand-in loader's answer: the call got PAST the door.
    assert response.status_code == 404, response.text
    assert seen == {"sub": ACTING_USER, "organization_id": ORG_ID}


def test_a_service_call_naming_no_person_is_refused_at_the_crawl_door(
    seen: dict[str, object],
) -> None:
    response = _client().get(
        PATH, headers={"Authorization": f"Bearer {SECRET}", "X-Organization-Id": ORG_ID}
    )
    assert response.status_code == 400, response.text
    assert seen == {}


def test_a_service_call_naming_no_organization_is_refused_at_the_crawl_door(
    seen: dict[str, object],
) -> None:
    response = _client().get(
        PATH, headers={"Authorization": f"Bearer {SECRET}", "X-Matrx-User-Id": ACTING_USER}
    )
    assert response.status_code == 400, response.text
    assert response.json()["detail"]["code"] == "organization_required"
    assert seen == {}


@pytest.mark.parametrize("bearer", [None, "not-the-secret"])
def test_a_wrong_or_missing_secret_is_still_refused(
    bearer: str | None, seen: dict[str, object]
) -> None:
    headers = {"X-Matrx-User-Id": ACTING_USER, "X-Organization-Id": ORG_ID}
    if bearer:
        headers["Authorization"] = f"Bearer {bearer}"
    response = _client().get(PATH, headers=headers)
    assert response.status_code == 401, response.text
    assert response.json()["detail"]["error"] == "service_credentials_required"
    assert seen == {}


# ── The login branch keeps its account-only rule ─────────────────────────────
# Opening the service lane must not widen the login lane: a guest token (a
# verified JWT with ``is_anonymous: true``) was refused here with
# ``401 account_required`` before, and still is; a person's JWT is admitted.

JWT_KEY = "synthetic-jwt-test-key-at-least-32-bytes-long"
AUTHORITY = "https://authority.example/auth/session/status"


@pytest.fixture
def login_client(monkeypatch: pytest.MonkeyPatch):
    import time
    from uuid import uuid4

    import httpx
    import jwt

    replies: dict[str, dict] = {}
    original = httpx.AsyncClient

    def upstream(request: httpx.Request) -> httpx.Response:
        body = replies[request.headers["authorization"][7:]]
        return httpx.Response(200, json=body, headers={"Cache-Control": "no-store"})

    class AuthorityClient(original):  # type: ignore[misc, valid-type]
        def __init__(self, **kwargs):
            super().__init__(**kwargs, transport=httpx.MockTransport(upstream))

    monkeypatch.setattr(httpx, "AsyncClient", AuthorityClient)

    def token(*, guest: bool) -> str:
        claims = {
            "sub": ACTING_USER,
            "session_id": str(uuid4()),
            "exp": int(time.time()) + 600,
            "aud": "authenticated",
            "is_anonymous": guest,
        }
        value = jwt.encode(claims, JWT_KEY, algorithm="HS256")
        replies[value] = {
            "user_id": ACTING_USER,
            "session_id": claims["session_id"],
            "expires_at": claims["exp"],
        }
        return value

    client = TestClient(
        create_app(
            ServerConfig(
                supabase_jwt_secret=JWT_KEY,
                admin_api_token=SECRET,
                session_authority_url=AUTHORITY,
            )
        )
    )
    return client, token


def test_a_guest_login_is_refused_at_the_crawl_door(login_client, seen) -> None:
    client, token = login_client
    response = client.get(
        PATH,
        headers={"Authorization": f"Bearer {token(guest=True)}", "X-Organization-Id": ORG_ID},
    )
    assert response.status_code == 401, response.text
    assert response.json()["detail"]["error"] == "account_required"
    assert seen == {}


def test_a_persons_login_reaches_the_crawl_handler(login_client, seen) -> None:
    client, token = login_client
    response = client.get(
        PATH,
        headers={"Authorization": f"Bearer {token(guest=False)}", "X-Organization-Id": ORG_ID},
    )
    assert response.status_code == 404, response.text
    assert seen == {"sub": ACTING_USER, "organization_id": ORG_ID}
