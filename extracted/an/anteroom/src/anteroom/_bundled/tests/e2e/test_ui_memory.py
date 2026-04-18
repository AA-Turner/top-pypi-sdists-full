"""Playwright E2E tests for the Memory panel (#1416).

Covers list / create / detail / edit / delete round-trips end to end.

Requires playwright: ``pip install playwright && playwright install chromium``.
The approve / reject review actions are owned by #920 and are intentionally
not exercised here.
"""

from __future__ import annotations

import pytest

HAS_PLAYWRIGHT = True
try:
    from playwright.sync_api import Page, expect
except ImportError:
    HAS_PLAYWRIGHT = False

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.skipif(not HAS_PLAYWRIGHT, reason="playwright not installed"),
]


class TestMemoryApi:
    """Smoke-level API round-trips — these do not need a browser."""

    def test_list_empty(self, api_client: object) -> None:
        import httpx

        client: httpx.Client = api_client  # type: ignore[assignment]
        resp = client.get("/api/memory")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_create_get_delete(self, api_client: object) -> None:
        import httpx

        client: httpx.Client = api_client  # type: ignore[assignment]

        created = client.post(
            "/api/memory",
            json={"content": "dark mode", "scope": "user", "category": "preference", "name": "e2e1"},
        )
        assert created.status_code == 200, created.text
        fqn = created.json()["fqn"]

        got = client.get(f"/api/memory/{fqn}")
        assert got.status_code == 200
        assert got.json()["content"] == "dark mode"

        patched = client.patch(f"/api/memory/{fqn}", json={"content": "dark mode v2"})
        assert patched.status_code == 200
        assert patched.json()["content"] == "dark mode v2"

        deleted = client.delete(f"/api/memory/{fqn}")
        assert deleted.status_code == 200

        after = client.get(f"/api/memory/{fqn}")
        assert after.status_code == 404


class TestMemoryPanel:
    """Real-browser flows for the memory panel.

    These tests drive the panel through the actual topbar toggle button
    (``#btn-memory-toggle``) and the panel's own "+" (New memory) flow,
    not through programmatic ``MemoryPanel.*`` calls — so the tests
    exercise the same code paths a real user would.
    """

    def test_panel_opens_via_toolbar_button(self, authenticated_page: Page, api_client: object, base_url: str) -> None:
        page = authenticated_page
        # The toolbar button must exist in the DOM (panel is otherwise unreachable).
        expect(page.locator("#btn-memory-toggle")).to_be_visible()
        page.click("#btn-memory-toggle")
        expect(page.locator("#memory-panel")).to_be_visible()
        expect(page.locator(".memory-empty")).to_contain_text("No memories found")

    def test_panel_lists_existing_memory(self, authenticated_page: Page, api_client: object, base_url: str) -> None:
        import httpx

        client: httpx.Client = api_client  # type: ignore[assignment]
        created = client.post(
            "/api/memory",
            json={"content": "listed", "scope": "user", "category": "preference", "name": "e2e-list"},
        )
        assert created.status_code == 200

        page = authenticated_page
        page.click("#btn-memory-toggle")
        expect(page.locator(".memory-item-title")).to_contain_text("@user/memory/e2e-list")

    def test_panel_creates_memory_from_ui(self, authenticated_page: Page, api_client: object, base_url: str) -> None:
        import httpx

        client: httpx.Client = api_client  # type: ignore[assignment]
        page = authenticated_page
        page.click("#btn-memory-toggle")
        page.click("#memory-new-btn")
        page.fill("#memory-create-content", "created from the UI")
        page.select_option("#memory-create-scope", "user")
        page.select_option("#memory-create-category", "preference")
        page.fill("#memory-create-name", "e2e-ui-create")
        page.click("#memory-create-save")
        page.wait_for_timeout(500)

        got = client.get("/api/memory/@user/memory/e2e-ui-create")
        assert got.status_code == 200
        assert got.json()["content"] == "created from the UI"

    def test_panel_detail_shows_provenance(self, authenticated_page: Page, api_client: object, base_url: str) -> None:
        import httpx

        client: httpx.Client = api_client  # type: ignore[assignment]
        # Create via API with provenance, then browse the detail view.
        created = client.post(
            "/api/memory",
            json={
                "content": "with prov",
                "scope": "user",
                "category": "preference",
                "name": "e2e-prov",
            },
        )
        assert created.status_code == 200
        # Patch provenance in — memory_service allows provenance metadata
        # via update_memory_metadata.
        patched = client.patch(
            "/api/memory/@user/memory/e2e-prov",
            json={
                "metadata": {
                    "provenance": {
                        "conversation_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                        "message_id": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
                    }
                }
            },
        )
        assert patched.status_code == 200

        page = authenticated_page
        page.click("#btn-memory-toggle")
        page.locator(".memory-item-title:has-text('e2e-prov')").click()
        expect(page.locator(".memory-detail-provenance")).to_contain_text("conversation_id")
        expect(page.locator(".memory-detail-provenance")).to_contain_text("message_id")

    def test_panel_filters_by_scope(self, authenticated_page: Page, api_client: object, base_url: str) -> None:
        import httpx

        client: httpx.Client = api_client  # type: ignore[assignment]
        client.post(
            "/api/memory",
            json={"content": "a", "scope": "user", "category": "preference", "name": "e2e-scope-u"},
        )
        client.post(
            "/api/memory",
            json={"content": "b", "scope": "local", "category": "preference", "name": "e2e-scope-l"},
        )

        page = authenticated_page
        page.click("#btn-memory-toggle")
        page.select_option("#memory-filter-scope", "user")
        # Wait for re-fetch to complete — filter change triggers _refreshList.
        page.wait_for_timeout(500)
        items = page.locator(".memory-item-title").all_text_contents()
        assert any("e2e-scope-u" in t for t in items)
        assert not any("e2e-scope-l" in t for t in items)

    def test_panel_delete_round_trip(self, authenticated_page: Page, api_client: object, base_url: str) -> None:
        import httpx

        client: httpx.Client = api_client  # type: ignore[assignment]
        client.post(
            "/api/memory",
            json={"content": "gone", "scope": "user", "category": "preference", "name": "e2e-del"},
        )

        page = authenticated_page
        page.click("#btn-memory-toggle")
        page.locator(".memory-item-title:has-text('e2e-del')").click()
        page.wait_for_selector(".memory-detail-actions button")
        page.locator(".memory-detail-actions button:has-text('Delete')").click()
        page.wait_for_timeout(500)

        after = client.get("/api/memory/@user/memory/e2e-del")
        assert after.status_code == 404
