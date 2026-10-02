"""matrx-seo's standalone service under the org-admission gate (API-T03).

The gate (matrx_connect ``AuthMiddleware._organization_admission_failure``,
8e5ee0b93) refuses an authenticated request with no verified organization —
but it only VERIFIES a claimed organization when the host injects a
``resolve_active_organization`` resolver. Before this change, the standalone
SEO service constructed ``AuthMiddleware`` with none: a claimed
``X-Organization-Id`` was trusted as-is, so ANY authenticated caller could
name ANY organization and be admitted into it — worse than the missing-org
defect the gate exists to close, because it never even reaches the "refuse"
branch.

These tests lock:

* a claimed organization the caller is NOT a member of is refused
  (``organization_required``), never silently trusted
* a claimed organization the caller genuinely belongs to is admitted
* ``/me`` — the identity+org probe the console calls BEFORE it can know
  which organization to send — stays reachable with no organization at all,
  exactly like the gate's own ``/auth/`` exemption
* an authenticated request to a real route with NO organization at all is
  refused, same as every other host under this gate
"""

from __future__ import annotations

import time

import jwt
import pytest
from fastapi.testclient import TestClient

JWT_SECRET = "test-secret-do-not-use-in-prod-test-secret-do-not-use-in-prod-CD"
USER_ID = "22222222-2222-4222-8222-222222222222"
MEMBER_ORG_ID = "66666666-6666-4666-8666-666666666666"
FOREIGN_ORG_ID = "77777777-7777-4777-8777-777777777777"


@pytest.fixture
def seo_env(monkeypatch: pytest.MonkeyPatch) -> pytest.MonkeyPatch:
    monkeypatch.setenv("SUPABASE_JWT_SECRET", JWT_SECRET)
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_MATRIX_URL", raising=False)
    return monkeypatch


def _token() -> str:
    payload = {
        "sub": USER_ID,
        "aud": "authenticated",
        "exp": int(time.time()) + 3600,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def _client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    from matrx_seo.standalone import app as app_module

    async def member_only(*args: object) -> bool:
        # call_function(config_name, schema, function_name, user_id, org_id)
        return args[-2:] == (USER_ID, MEMBER_ORG_ID)

    monkeypatch.setattr("matrx_orm.call_function", member_only)
    # Route business logic reaches for a live DB (no DB is registered in this
    # unit-test process) — these tests assert only the ADMISSION GATE's
    # verdict, so a downstream 500 from the unrelated missing-DB is
    # acceptable; it must never surface as an unhandled exception.
    return TestClient(app_module.create_app(), raise_server_exceptions=False)


def test_unverified_claimed_organization_is_refused_not_trusted(
    seo_env: pytest.MonkeyPatch,
) -> None:
    client = _client(seo_env)
    response = client.get(
        "/providers/dataforseo/operations",
        headers={
            "Authorization": f"Bearer {_token()}",
            "X-Organization-Id": FOREIGN_ORG_ID,
        },
    )
    assert response.status_code == 400
    # A claimed-but-unverified organization is `organization_forbidden`, never
    # `organization_required` — the codes were split per SITUATION on
    # 2026-09-07 and this standalone assertion was never brought along, so it
    # had been red at HEAD ever since (found 2026-09-14).
    assert response.json()["code"] == "organization_forbidden"


def test_verified_membership_is_admitted(seo_env: pytest.MonkeyPatch) -> None:
    """Positive control — a resolver that verified nothing would 400 here.

    The route itself needs a live DB for its business logic (out of scope for
    this gate-level test — no DB is registered in this unit-test process), so
    this only asserts the ADMISSION gate let it through: never
    ``organization_required``.
    """
    client = _client(seo_env)
    response = client.get(
        "/providers/dataforseo/operations",
        headers={
            "Authorization": f"Bearer {_token()}",
            "X-Organization-Id": MEMBER_ORG_ID,
        },
    )
    assert response.status_code != 400


def test_authenticated_request_without_any_organization_is_refused(
    seo_env: pytest.MonkeyPatch,
) -> None:
    client = _client(seo_env)
    response = client.get(
        "/providers/dataforseo/operations",
        headers={"Authorization": f"Bearer {_token()}"},
    )
    assert response.status_code == 400
    assert response.json()["code"] == "organization_required"


def test_me_identity_probe_is_reachable_without_an_organization(
    seo_env: pytest.MonkeyPatch,
) -> None:
    """The console calls /me to learn ITS organization — it cannot have sent
    one yet. This must stay reachable, exactly like the gate's own
    documented /auth/ exemption for the sign-in flow."""
    client = _client(seo_env)
    response = client.get("/me", headers={"Authorization": f"Bearer {_token()}"})
    assert response.status_code != 400, response.text


@pytest.mark.parametrize(
    ("memberships", "expected"),
    [([MEMBER_ORG_ID], MEMBER_ORG_ID), ([MEMBER_ORG_ID, "org-b"], ""), ([], "")],
)
def test_me_names_only_a_sole_membership_and_never_guesses(
    seo_env: pytest.MonkeyPatch, memberships: list[str], expected: str
) -> None:
    """No organization selected: /me names the person's ONLY organization, and
    with several (or none) answers empty — never the first, the newest, or any
    other pick."""
    from matrx_seo.standalone import app as app_module

    async def fake_call_function(*args: object, **kwargs: object) -> object:
        if args[2] == "get_user_organizations":
            assert kwargs.get("mode") == "rows"
            return [{"id": org_id} for org_id in memberships]
        return False

    seo_env.setattr("matrx_orm.call_function", fake_call_function)
    client = TestClient(app_module.create_app(), raise_server_exceptions=False)
    response = client.get("/me", headers={"Authorization": f"Bearer {_token()}"})
    assert response.status_code == 200, response.text
    assert response.json()["organization_id"] == expected
