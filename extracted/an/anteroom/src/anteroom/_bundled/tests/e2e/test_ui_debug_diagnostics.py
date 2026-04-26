from __future__ import annotations

import pytest

pytestmark = [pytest.mark.e2e]

try:
    from playwright.sync_api import Page  # noqa: F401

    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

requires_playwright = pytest.mark.skipif(not HAS_PLAYWRIGHT, reason="playwright not installed")


class TestDebugDiagnosticsStaticAssets:
    def test_debug_diagnostics_js_hooks_present(self, base_url: str) -> None:
        import httpx

        app = httpx.get(f"{base_url}/js/app.js", follow_redirects=True)
        chat = httpx.get(f"{base_url}/js/chat.js", follow_redirects=True)
        assert app.status_code == 200
        assert chat.status_code == 200
        assert "isDebugMode" in app.text
        assert "X-Anteroom-Debug" in chat.text
        assert "debug_summary" in chat.text
        assert "renderDebugSummary" in chat.text

    def test_debug_diagnostics_css_hooks_present(self, base_url: str) -> None:
        import httpx

        resp = httpx.get(f"{base_url}/css/style.css", follow_redirects=True)
        assert resp.status_code == 200
        assert ".debug-summary" in resp.text
        assert ".debug-summary-row" in resp.text


@requires_playwright
class TestDebugDiagnosticsDom:
    def test_debug_summary_event_renders_collapsible_block(self, page: "Page", base_url: str) -> None:
        page.goto(f"{base_url}/?debug=1")
        page.evaluate(
            """() => {
                const container = document.getElementById('messages-container');
                container.innerHTML = '';
                Chat._handleSSEEvent('queued_message', {content: 'queued', position: 1, queue_depth: 0});
                Chat._handleSSEEvent('debug_summary', {
                    total_duration_seconds: 2.0,
                    stop_reason: 'completed',
                    final_phase: 'streaming',
                    model: {provider: 'openai', name: 'gpt-test'},
                    counters: {tokens: 2, token_chars: 20},
                    tools: [{name: 'bash', status: 'success', duration_seconds: 0.2}],
                    redaction: {raw_tool_output: 'omitted'},
                });
            }"""
        )

        block = page.locator(".debug-summary")
        assert block.count() == 1
        assert "Debug diagnostics" in block.text_content()
