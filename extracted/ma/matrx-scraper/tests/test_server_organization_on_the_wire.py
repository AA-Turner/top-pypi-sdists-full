"""Every service-facing scraper router is admitted WITH an organization.

THE FINDING (2026-09-17). All four service-facing routers — scrape, external,
browser, preview — were mounted
``require_authenticated_or_service(..., organization_optional=True)``, on the
reasoning that each write route validates its own request-BODY
``organization_id``. Two things were wrong with that:

* matrx-connect skipped the organization requirement ENTIRELY for a call that
  named no acting user, so a pure server-to-server call was admitted with no
  tenant at all;
* a route that simply did not read the body field then had no tenant, and
  nothing screamed.

Every route behind this dependency does tenant work — a scrape of a customer's
page cached into ``scraper.scrape_parsed_page``, a retry-queue claim, a pooled
browser session driven on a tenant's behalf, a preview that spends an external
fetch and a browser hold — so the organization is required on the wire and no
exemption is declared. Law:
``common-docs/policies/context-is-carried-never-rebuilt.md`` rule 1 — "a
server-to-server call forwards both on the wire and is admitted the same way".
"""

from __future__ import annotations

import pytest

fastapi = pytest.importorskip("fastapi", reason="server extra not installed")

from fastapi.testclient import TestClient  # noqa: E402

from matrx_scraper.server.app import create_app  # noqa: E402
from matrx_scraper.server.config import ServerConfig  # noqa: E402

SECRET = "test-approved-server-secret"
ACTING_USER = "88888888-8888-4888-8888-888888888888"
ORG_ID = "99999999-9999-4999-9999-999999999999"

# One representative route per service-facing router. Each is reached BEFORE
# its handler runs — the refusal happens in the router dependency.
SERVICE_ROUTES = [
    ("scrape", "/api/scraper/page-capture", {"url": "https://example.com/"}),
    ("external", "/api/scraper/batch", {"urls": ["https://example.com/"]}),
    ("browser", "/api/scraper/browser/sessions", {}),
    ("preview", "/api/scraper/preview", {"url": "https://example.com/"}),
]


def _client() -> TestClient:
    # No lifespan: the dependency refuses before any DB/browser wiring is used.
    return TestClient(create_app(ServerConfig(admin_api_token=SECRET)))


@pytest.mark.parametrize("router, path, body", SERVICE_ROUTES)
def test_service_call_without_an_organization_is_refused(
    router: str, path: str, body: dict
) -> None:
    response = _client().post(
        path,
        json=body,
        headers={"Authorization": f"Bearer {SECRET}", "X-Matrx-User-Id": ACTING_USER},
    )
    assert response.status_code == 400, router
    assert response.json()["detail"]["code"] == "organization_required"


@pytest.mark.parametrize("router, path, body", SERVICE_ROUTES)
def test_pure_service_call_without_an_organization_is_refused(
    router: str, path: str, body: dict
) -> None:
    """No acting user either — the exact shape that used to walk straight
    through matrx-connect's organization check."""
    response = _client().post(path, json=body, headers={"Authorization": f"Bearer {SECRET}"})
    assert response.status_code == 400, router
    assert response.json()["detail"]["code"] == "organization_required"


def test_a_service_call_carrying_the_organization_reaches_the_handler(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Positive control — a dependency that refused everything would pass the
    tests above for the wrong reason. The organization is on the context the
    handler runs under."""
    seen: dict[str, object] = {}

    async def fake_preview(url: str) -> dict:
        from matrx_connect import get_app_context

        ctx = get_app_context()
        seen["organization_id"] = ctx.organization_id
        seen["user_id"] = ctx.user_id
        seen["admission"] = ctx.organization_admission
        return {"ok": True, "input": url}

    # `matrx_scraper.api.__init__` rebinds the module name to the router
    # OBJECT, so patch the module itself.
    import importlib

    preview_module = importlib.import_module("matrx_scraper.api.preview_router")
    monkeypatch.setattr(preview_module, "quick_preview", fake_preview)

    response = _client().post(
        "/api/scraper/preview",
        json={"url": "https://example.com/"},
        headers={
            "Authorization": f"Bearer {SECRET}",
            "X-Matrx-User-Id": ACTING_USER,
            "X-Organization-Id": ORG_ID,
        },
    )
    assert response.status_code == 200
    assert response.json()["ok"] is True
    assert seen["organization_id"] == ORG_ID
    assert seen["user_id"] == ACTING_USER
    # This handshake proves no membership — it never claims "verified".
    assert seen["admission"] == "none"
