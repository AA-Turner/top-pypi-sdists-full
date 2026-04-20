"""Playwright E2E tests for the auto-propose memory banner (#1454).

Mirrors the lightweight pattern used by ``test_ui_attribution.py`` (#923):
rather than stand up a full mock-AI turn that emits a
``memory_auto_proposed`` SSE event, these tests load the chat page and
drive the exposed ``Chat._addAutoProposeBanner`` helper directly via
``page.evaluate``. That validates three things in a real browser (not
jsdom):

1. The helper is actually exposed on the ``Chat`` module after page load
   (the JS unit tests use an inlined copy and can't catch a missing
   export).
2. User-derived strings render through ``textContent`` — a hostile
   ``<script>``/``<img>`` payload must render as literal text and never
   execute.
3. The Review button reaches into the ``MemoryPanel`` module that ships
   on the same page and successfully opens the panel + switches to the
   review tab. This pins the cross-module wiring that the jsdom unit
   test can only mock.

A full AI-driven happy-path is out of scope; that's covered by the
runner unit tests + the chat-router test_chat_comprehensive coverage.
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


def _seed_message(page: "Page") -> None:
    """Append a minimal ``.message.assistant`` node we can attach the banner to."""
    page.evaluate(
        """() => {
            const container = document.getElementById('messages-container');
            const el = document.createElement('div');
            el.className = 'message assistant';
            el.id = 'ap-test-msg';
            const role = document.createElement('div');
            role.className = 'message-role';
            role.textContent = 'ANTEROOM';
            el.appendChild(role);
            const content = document.createElement('div');
            content.className = 'message-content';
            content.textContent = 'hello';
            el.appendChild(content);
            container.appendChild(el);
        }"""
    )


class TestAutoProposeBannerUI:
    def test_helper_is_exposed_on_chat_module(self, authenticated_page: "Page", base_url: str) -> None:
        """Pin that ``_addAutoProposeBanner`` is reachable via the Chat IIFE."""
        page = authenticated_page
        kind = page.evaluate("() => typeof Chat._addAutoProposeBanner")
        assert kind == "function"

    def test_renders_banner_with_count_and_review_button(self, authenticated_page: "Page", base_url: str) -> None:
        page = authenticated_page
        _seed_message(page)
        page.evaluate(
            """() => {
                const msg = document.getElementById('ap-test-msg');
                Chat._addAutoProposeBanner(msg, [
                    {fqn: '@user/memory/pref-aaa', category: 'preference', content_preview: 'User prefers tabs.'},
                    {fqn: '@user/memory/deci-bbb', category: 'decision', content_preview: 'Use linkerd.'},
                ]);
            }"""
        )
        banner = page.locator("#ap-test-msg .memory-auto-propose-banner")
        expect(banner).to_be_visible()
        text = banner.inner_text()
        assert "2 memories queued for review" in text
        # Review button is present and labelled.
        review_btn = page.locator("#ap-test-msg .memory-auto-propose-review")
        expect(review_btn).to_be_visible()
        expect(review_btn).to_have_text("Review")

    def test_singular_noun_for_one_item(self, authenticated_page: "Page", base_url: str) -> None:
        page = authenticated_page
        _seed_message(page)
        page.evaluate(
            """() => {
                const msg = document.getElementById('ap-test-msg');
                Chat._addAutoProposeBanner(msg, [
                    {fqn: '@user/memory/pref-x', category: 'preference', content_preview: 'X.'},
                ]);
            }"""
        )
        banner = page.locator("#ap-test-msg .memory-auto-propose-banner")
        expect(banner).to_contain_text("1 memory queued for review")

    def test_hostile_payload_renders_as_text_not_script(self, authenticated_page: "Page", base_url: str) -> None:
        """XSS negative — hostile content_preview must not execute."""
        page = authenticated_page
        _seed_message(page)
        # Sentinel that the hostile payload would set if it ran.
        page.evaluate("() => { window._xssSentinel = false; }")
        page.evaluate(
            """() => {
                const msg = document.getElementById('ap-test-msg');
                Chat._addAutoProposeBanner(msg, [
                    {
                        fqn: '@user/memory/pref-x',
                        category: 'preference',
                        content_preview: '<img src=x onerror="window._xssSentinel=true">',
                    },
                ]);
            }"""
        )
        # Sentinel is unchanged → no script ran.
        assert page.evaluate("() => window._xssSentinel === false")
        # And the banner did NOT grow an <img> tag.
        img_count = page.locator("#ap-test-msg .memory-auto-propose-banner img").count()
        assert img_count == 0

    def test_review_button_opens_memory_panel_and_switches_to_review_tab(
        self, authenticated_page: "Page", base_url: str
    ) -> None:
        """Clicking Review must open the memory panel AND select the review tab.

        This pins the cross-module wiring between Chat and MemoryPanel that
        the jsdom unit test can only mock — here we drive the real
        MemoryPanel module that loads with the page.
        """
        page = authenticated_page
        _seed_message(page)
        page.evaluate(
            """() => {
                const msg = document.getElementById('ap-test-msg');
                Chat._addAutoProposeBanner(msg, [
                    {fqn: '@user/memory/pref-x', category: 'preference', content_preview: 'X.'},
                ]);
            }"""
        )
        page.locator("#ap-test-msg .memory-auto-propose-review").click()
        # Memory panel should now be visible (display != "none").
        panel = page.locator("#memory-panel")
        # Wait briefly for openPanel to populate the view (it's async).
        page.wait_for_function(
            "() => { const p = document.getElementById('memory-panel'); return p && p.style.display !== 'none'; }",
            timeout=3000,
        )
        expect(panel).to_be_visible()
        # The review tab should now be the active one.
        active_tab = page.locator(".memory-tab.active")
        # MemoryPanel marks the active tab via the `active` class. The
        # exact selector format is internal but stable.
        active_text = active_tab.first.inner_text() if active_tab.count() > 0 else ""
        assert "review" in active_text.lower(), f"expected review tab active; got: {active_text!r}"
