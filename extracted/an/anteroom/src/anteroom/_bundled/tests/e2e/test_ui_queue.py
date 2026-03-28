"""Playwright browser tests for queue position feedback in the web UI (#1175).

Tests verify the user-visible queue UX:
- Real send-while-busy flow: badge appears from app's actual queue path
- CSS rendering of queued badge
- Queue constant sanity check

Requires playwright: ``pip install playwright && playwright install chromium``
"""

from __future__ import annotations

import json

import pytest

HAS_PLAYWRIGHT = True
try:
    from playwright.sync_api import Page, Route, expect
except ImportError:
    HAS_PLAYWRIGHT = False

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.skipif(not HAS_PLAYWRIGHT, reason="playwright not installed"),
]


class TestQueueFlowReal:
    """Exercise the real send-while-busy queue path in the browser.

    The approach:
    1. Load a conversation in the browser
    2. Set App.state.isStreaming = true (simulates an active AI turn)
    3. Intercept the chat endpoint to return queued JSON
    4. Send a message via the real UI (fill input + click send)
    5. Assert the .queued-badge appears — created by chat.js sendMessage()

    This tests the actual JS queue code path at chat.js:192-213. The
    isStreaming flag is the same boolean that streamChatResponse() sets
    at chat.js:253 and clears in its finally block at chat.js:326.
    Setting it directly is deterministic — no race against stream teardown.
    """

    def test_send_while_busy_shows_queued_badge(
        self, authenticated_page: Page, api_client: object, base_url: str
    ) -> None:
        """Send a message while isStreaming=true -> queued badge from real app path."""
        import httpx

        client: httpx.Client = api_client  # type: ignore[assignment]
        page = authenticated_page

        # Create a conversation via API
        resp = client.post("/api/conversations", json={"title": "Queue Flow Test"})
        assert resp.status_code == 201
        conv_id = resp.json()["id"]

        # Load the conversation in the browser
        page.evaluate(
            """(convId) => {
                if (typeof App !== 'undefined' && App.loadConversation) {
                    App.loadConversation(convId);
                }
            }""",
            conv_id,
        )
        page.wait_for_timeout(500)

        # Put the app into streaming state — this is the same flag that
        # streamChatResponse() sets at chat.js:253 when a real stream starts.
        # Setting it directly is deterministic and exercises the exact same
        # branch in sendMessage() at chat.js:192.
        page.evaluate("() => { App.state.isStreaming = true; }")

        # Verify the app thinks it's streaming before we proceed
        is_streaming = page.evaluate("() => App.state.isStreaming")
        assert is_streaming is True, "App should be in streaming state"

        # Intercept the chat endpoint to return a queued JSON response.
        # When isStreaming=true, sendMessage() POSTs to the chat endpoint
        # and expects JSON (not SSE). This is the real queue code path.
        def handle_queued(route: Route) -> None:
            route.fulfill(
                status=200,
                headers={"Content-Type": "application/json"},
                body=json.dumps({"status": "queued", "position": 1, "queue_depth": 0}),
            )

        page.route(f"**/api/conversations/{conv_id}/chat", handle_queued)

        # Send a message via the real UI while "busy"
        page.fill("#message-input", "Queued message while AI is working")
        page.click("#btn-send")

        # The queued badge should appear — created by chat.js:206-209
        badge = page.locator(".queued-badge")
        expect(badge.first).to_be_visible(timeout=3000)
        badge_text = badge.first.text_content() or ""
        assert "queued" in badge_text.lower(), f"Badge text was: {badge_text}"
        assert "(1)" in badge_text, f"Expected position (1) in badge, got: {badge_text}"

        # Clean up
        page.unroute(f"**/api/conversations/{conv_id}/chat")
        page.evaluate("() => { App.state.isStreaming = false; }")

    def test_queued_badge_has_pill_styling(self, authenticated_page: Page, base_url: str) -> None:
        """Verify the .queued-badge CSS produces pill-shaped styling in the real browser."""
        page = authenticated_page

        # Inject a badge to test CSS rendering (the real flow is tested above)
        page.evaluate("""() => {
            const container = document.querySelector('#chat-messages') || document.body;
            const div = document.createElement('div');
            div.className = 'message user';
            div.innerHTML = '<span class="message-role">YOU</span>';
            const badge = document.createElement('span');
            badge.className = 'queued-badge';
            badge.textContent = 'queued (1)';
            div.querySelector('.message-role').appendChild(badge);
            container.appendChild(div);
        }""")

        badge = page.locator(".queued-badge")
        expect(badge).to_be_visible()

        border_radius = page.evaluate(
            """() => getComputedStyle(document.querySelector('.queued-badge')).borderRadius"""
        )
        assert border_radius != "0px", f"Expected pill shape, got border-radius: {border_radius}"


class TestQueueConstant:
    """Non-browser sanity checks."""

    def test_queue_max_is_10(self) -> None:
        """Queue max constant matches expected value."""
        from anteroom.routers.chat import MAX_QUEUED_MESSAGES

        assert MAX_QUEUED_MESSAGES == 10
