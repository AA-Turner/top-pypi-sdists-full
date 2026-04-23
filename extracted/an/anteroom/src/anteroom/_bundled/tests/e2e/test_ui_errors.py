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


def _seed_assistant_message(page: "Page") -> None:
    page.evaluate(
        """() => {
            const container = document.getElementById('messages-container');
            const el = document.createElement('div');
            el.className = 'message assistant';
            const role = document.createElement('div');
            role.className = 'message-role';
            role.textContent = 'ANTEROOM';
            const content = document.createElement('div');
            content.className = 'message-content';
            content.textContent = 'pending';
            el.appendChild(role);
            el.appendChild(content);
            container.appendChild(el);
        }"""
    )


class TestErrorPresentationUI:
    def test_sse_error_renders_compact_actionable_banner(self, authenticated_page: "Page") -> None:
        page = authenticated_page
        _seed_assistant_message(page)
        page.evaluate(
            """() => {
                Chat._handleSSEEvent('error', {
                    message: 'Cannot connect to API (3 attempts).',
                    suggestion: 'Check AI_CHAT_BASE_URL (http://localhost:11434/v1)',
                    display_message: 'Cannot connect to API (3 attempts). — Check AI_CHAT_BASE_URL (http://localhost:11434/v1)',
                });
            }"""
        )
        banner = page.locator(".error-message").last
        expect(banner).to_be_visible()
        expect(banner).to_contain_text("Cannot connect to API (3 attempts).")
        expect(banner).to_contain_text("Check AI_CHAT_BASE_URL")

    def test_hostile_error_text_renders_as_text(self, authenticated_page: "Page") -> None:
        page = authenticated_page
        _seed_assistant_message(page)
        page.evaluate("() => { window.__ERR_BANNER_XSS__ = false; }")
        page.evaluate(
            """() => {
                Chat._handleSSEEvent('error', {
                    display_message: '<img src=x onerror="window.__ERR_BANNER_XSS__=true">',
                });
            }"""
        )
        assert page.evaluate("() => window.__ERR_BANNER_XSS__ === false")
        assert page.locator(".error-message img").count() == 0
