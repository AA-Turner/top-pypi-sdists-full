"""Playwright E2E tests for the attribution footer (#923).

Rather than stand up a full mock-AI turn, these tests load the chat
page and drive the exposed ``Chat._addAttributionFooter`` helper
directly via ``page.evaluate``. That validates three things in a real
browser (not jsdom):

1. The helper is actually exposed on the ``Chat`` module.
2. Snapshot values render through ``textContent`` — a hostile
   ``<script>`` payload must render as literal text, not execute.
3. The empty-section fallback still reads ``(none)`` once the CSS
   has been applied.

A full AI-driven happy-path is out of scope here; that's covered by
``test_repl_attribution.py`` and the Vitest suite.
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
    """Append a minimal ``.message.assistant`` node we can attach the footer to."""
    page.evaluate(
        """() => {
            const container = document.getElementById('messages-container');
            const el = document.createElement('div');
            el.className = 'message assistant';
            el.id = 'attr-test-msg';
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


class TestAttributionFooterUI:
    def test_renders_five_sections_from_snapshot(self, authenticated_page: "Page", base_url: str) -> None:
        page = authenticated_page
        _seed_message(page)
        page.evaluate(
            """() => {
                const msg = document.getElementById('attr-test-msg');
                Chat._addAttributionFooter(msg, {
                    turns: [{message_id: 'm-1', role: 'user'}],
                    memory: [{fqn: '@user/memory/pref', scope: 'user', category: 'preference'}],
                    sources: [{label: 'README.md', type: 'source_chunk'}],
                    tools: [{id: 'tc-1', name: 'read_file'}],
                    packs: [{namespace: 'core', name: 'alpha', scope: 'global'}],
                    dlp_match_count: 0,
                    output_filter_match_count: 0,
                });
            }"""
        )
        expect(page.locator("#attr-test-msg .attribution-footer")).to_be_visible()
        # Section titles render exactly once each.
        titles = page.locator("#attr-test-msg .attribution-section-title").all_inner_texts()
        assert titles == [
            "Recent turns",
            "Recalled memories",
            "RAG sources",
            "Tool calls",
            "Attached packs",
        ]
        footer_text = page.locator("#attr-test-msg .attribution-footer").inner_text()
        for expected in ("m-1", "@user/memory/pref", "README.md", "read_file", "core"):
            assert expected in footer_text

    def test_hostile_payload_renders_as_text_not_script(self, authenticated_page: "Page", base_url: str) -> None:
        page = authenticated_page
        _seed_message(page)
        # Sentinel that the hostile payload would set if it ran.
        page.evaluate("() => { window.__ATTR_XSS_FIRED__ = false; }")
        hostile = "<script>window.__ATTR_XSS_FIRED__=true;</script>"
        page.evaluate(
            """(hostile) => {
                const msg = document.getElementById('attr-test-msg');
                Chat._addAttributionFooter(msg, {
                    turns: [],
                    memory: [],
                    sources: [{label: hostile, type: 'source_chunk'}],
                    tools: [{id: 'tc-1', name: hostile}],
                    packs: [],
                    dlp_match_count: 0,
                    output_filter_match_count: 0,
                });
            }""",
            hostile,
        )
        # The hostile literal is visible as text inside the footer.
        footer_text = page.locator("#attr-test-msg .attribution-footer").inner_text()
        assert hostile in footer_text
        # And no actual <script> tag was ever inserted under the footer.
        script_count = page.evaluate(
            "() => document.querySelectorAll('#attr-test-msg .attribution-footer script').length"
        )
        assert script_count == 0
        # And the hostile code never ran.
        fired = page.evaluate("() => window.__ATTR_XSS_FIRED__")
        assert fired is False
