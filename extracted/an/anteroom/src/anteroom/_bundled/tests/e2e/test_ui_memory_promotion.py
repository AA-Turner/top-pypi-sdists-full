"""Playwright E2E tests for the memory promotion / review flows (#920).

Exercises:
- Propose a candidate via ``POST /api/memory/candidates``, see it appear in
  the review queue tab, approve it, confirm it moves to active.
- Reject-with-reason round-trip.
- Save-as-memory affordance on an assistant message opens the form, submits,
  and the new candidate shows up in the review queue.

Requires playwright: ``pip install playwright && playwright install chromium``.
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


class TestMemoryPromotionApi:
    """Smoke-level round-trips that don't need a browser."""

    def test_propose_list_approve(self, api_client: object) -> None:
        import httpx

        client: httpx.Client = api_client  # type: ignore[assignment]

        proposed = client.post(
            "/api/memory/candidates",
            json={
                "content": "approve me",
                "scope": "user",
                "category": "preference",
                "name": "e2e-approve",
                "proposer": "user",
            },
        )
        assert proposed.status_code == 200, proposed.text
        fqn = proposed.json()["fqn"]

        queue = client.get("/api/memory/candidates")
        assert queue.status_code == 200
        assert any(m["fqn"] == fqn for m in queue.json())

        approved = client.post(f"/api/memory/{fqn}/approve", json={})
        assert approved.status_code == 200
        assert approved.json()["metadata"]["memory_status"] == "active"

        # Active listing should now include it; review queue should not.
        active = client.get("/api/memory?status=active")
        assert any(m["fqn"] == fqn for m in active.json())
        queue_after = client.get("/api/memory/candidates")
        assert not any(m["fqn"] == fqn for m in queue_after.json())

    def test_propose_and_reject(self, api_client: object) -> None:
        import httpx

        client: httpx.Client = api_client  # type: ignore[assignment]

        proposed = client.post(
            "/api/memory/candidates",
            json={
                "content": "reject me",
                "scope": "user",
                "category": "preference",
                "name": "e2e-reject",
                "proposer": "user",
            },
        )
        assert proposed.status_code == 200
        fqn = proposed.json()["fqn"]

        rejected = client.post(f"/api/memory/{fqn}/reject", json={"reason": "Not useful"})
        assert rejected.status_code == 200
        assert rejected.json()["metadata"]["memory_status"] == "rejected"

    def test_reject_without_reason_returns_422(self, api_client: object) -> None:
        import httpx

        client: httpx.Client = api_client  # type: ignore[assignment]
        proposed = client.post(
            "/api/memory/candidates",
            json={
                "content": "need-reason",
                "scope": "user",
                "category": "preference",
                "name": "e2e-noreason",
                "proposer": "user",
            },
        )
        fqn = proposed.json()["fqn"]

        # Pydantic min_length=1 → 422 Unprocessable Entity for empty reason.
        resp = client.post(f"/api/memory/{fqn}/reject", json={"reason": ""})
        assert resp.status_code == 422


class TestReviewQueueUI:
    """Real-browser flows for the review queue tab."""

    def test_review_tab_lists_pending_candidate(
        self, authenticated_page: Page, api_client: object, base_url: str
    ) -> None:
        import httpx

        client: httpx.Client = api_client  # type: ignore[assignment]
        client.post(
            "/api/memory/candidates",
            json={
                "content": "pending review",
                "scope": "user",
                "category": "preference",
                "name": "e2e-ui-pending",
                "proposer": "user",
            },
        )

        page = authenticated_page
        page.click("#btn-memory-toggle")
        page.locator('.memory-tab[data-tab="review"]').click()
        expect(page.locator(".memory-review-item")).to_contain_text("@user/memory/e2e-ui-pending")
        # Three action buttons must be rendered per row.
        row = page.locator(".memory-review-item").first
        expect(row.locator(".memory-review-approve")).to_be_visible()
        expect(row.locator(".memory-review-edit-approve")).to_be_visible()
        expect(row.locator(".memory-review-reject")).to_be_visible()

    def test_approve_moves_candidate_to_active(
        self, authenticated_page: Page, api_client: object, base_url: str
    ) -> None:
        import httpx

        client: httpx.Client = api_client  # type: ignore[assignment]
        client.post(
            "/api/memory/candidates",
            json={
                "content": "approve-flow",
                "scope": "user",
                "category": "preference",
                "name": "e2e-ui-approve",
                "proposer": "user",
            },
        )

        page = authenticated_page
        page.click("#btn-memory-toggle")
        page.locator('.memory-tab[data-tab="review"]').click()
        page.locator('.memory-review-item:has-text("e2e-ui-approve") .memory-review-approve').click()
        page.wait_for_timeout(500)

        # Confirm the status flipped via API.
        got = client.get("/api/memory/@user/memory/e2e-ui-approve")
        assert got.status_code == 200
        assert got.json()["metadata"]["memory_status"] == "active"

    def test_reject_requires_reason(self, authenticated_page: Page, api_client: object, base_url: str) -> None:
        import httpx

        client: httpx.Client = api_client  # type: ignore[assignment]
        client.post(
            "/api/memory/candidates",
            json={
                "content": "reject-flow",
                "scope": "user",
                "category": "preference",
                "name": "e2e-ui-reject",
                "proposer": "user",
            },
        )

        page = authenticated_page
        page.click("#btn-memory-toggle")
        page.locator('.memory-tab[data-tab="review"]').click()
        page.locator('.memory-review-item:has-text("e2e-ui-reject") .memory-review-reject').click()
        # Submit without filling reason — should show inline error, no network call.
        page.locator(".memory-reject-form button:has-text('Reject')").click()
        expect(page.locator(".memory-error")).to_contain_text("required")

        # Now fill the reason and submit.
        page.locator(".memory-reject-reason").fill("Not accurate")
        page.locator(".memory-reject-form button:has-text('Reject')").click()
        page.wait_for_timeout(500)

        got = client.get("/api/memory/@user/memory/e2e-ui-reject")
        assert got.json()["metadata"]["memory_status"] == "rejected"


class TestSaveAsMemoryUI:
    """Exercises the Save-as-memory affordance on assistant messages.

    The affordance only appears once a message is persisted and has a stable
    id (chat.js wires it in ``addMessageActions`` when ``msgData.id`` is a
    string). These tests drive the button once a message has landed.
    """

    def test_save_as_memory_button_renders(self, authenticated_page: Page, api_client: object, base_url: str) -> None:
        import httpx

        client: httpx.Client = api_client  # type: ignore[assignment]
        # Create a conversation with an assistant message via API so the
        # message already has a stable id by the time the page loads.
        conv = client.post("/api/conversations", json={"title": "Save-as-memory"})
        assert conv.status_code == 201
        conv_id = conv.json()["id"]
        # Inject a persisted assistant message directly — avoids running
        # a real AI turn from the browser in the test harness.
        client.post(
            f"/api/conversations/{conv_id}/messages",
            json={"role": "assistant", "content": "This is a helpful answer."},
        )

        page = authenticated_page
        page.evaluate("convId => App.loadConversation(convId)", conv_id)
        page.wait_for_selector(".message.assistant .btn-save-memory")
        expect(page.locator(".message.assistant .btn-save-memory")).to_be_visible()

    def test_save_as_memory_submits_candidate(
        self, authenticated_page: Page, api_client: object, base_url: str
    ) -> None:
        import httpx

        client: httpx.Client = api_client  # type: ignore[assignment]
        conv = client.post("/api/conversations", json={"title": "Save-as-memory submit"})
        conv_id = conv.json()["id"]
        client.post(
            f"/api/conversations/{conv_id}/messages",
            json={"role": "assistant", "content": "Prefers dark mode."},
        )

        page = authenticated_page
        page.evaluate("convId => App.loadConversation(convId)", conv_id)
        page.wait_for_selector(".message.assistant .btn-save-memory")
        page.locator(".message.assistant .btn-save-memory").first.click()

        # Form should open in-message.
        page.wait_for_selector(".save-memory-form .save-memory-submit")
        page.locator(".save-memory-scope").select_option("user")
        page.locator(".save-memory-category").select_option("preference")
        page.locator(".save-memory-submit").click()
        page.wait_for_timeout(500)

        # A new candidate should now be in the review queue.
        queue = client.get("/api/memory/candidates")
        assert any("Prefers dark mode." in m.get("content", "") for m in queue.json())
