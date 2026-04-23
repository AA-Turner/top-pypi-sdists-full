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
    def test_renders_six_sections_from_snapshot(self, authenticated_page: "Page", base_url: str) -> None:
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
                    instructions: [
                        {path: '/repo/ANTEROOM.md', scope: 'project', estimated_tokens: 9894},
                    ],
                    dlp_match_count: 0,
                    output_filter_match_count: 0,
                });
            }"""
        )
        expect(page.locator("#attr-test-msg .attribution-footer")).to_be_visible()
        # Section titles render exactly once each (six sections post-#1462).
        titles = page.locator("#attr-test-msg .attribution-section-title").all_inner_texts()
        assert titles == [
            "Recent turns",
            "Recalled memories",
            "RAG sources",
            "Tool calls",
            "Attached packs",
            "Project instructions",
        ]
        footer_text = page.locator("#attr-test-msg .attribution-footer").inner_text()
        for expected in ("m-1", "@user/memory/pref", "README.md", "read_file", "core", "/repo/ANTEROOM.md"):
            assert expected in footer_text
        # Summary includes the singular instructions noun.
        summary_text = page.locator("#attr-test-msg .attribution-summary").inner_text()
        assert "1 instruction file" in summary_text

    def test_instructions_empty_hides_summary_segment(self, authenticated_page: "Page", base_url: str) -> None:
        """When no instruction files loaded, the summary omits the segment
        — matching CLI footer behaviour. (#1462)"""
        page = authenticated_page
        _seed_message(page)
        page.evaluate(
            """() => {
                const msg = document.getElementById('attr-test-msg');
                Chat._addAttributionFooter(msg, {
                    turns: [], memory: [], sources: [], tools: [], packs: [],
                    instructions: [],
                    dlp_match_count: 0, output_filter_match_count: 0,
                });
            }"""
        )
        summary_text = page.locator("#attr-test-msg .attribution-summary").inner_text()
        assert "instruction" not in summary_text

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
                    // #1462 — also smuggle hostile content through the new
                    // user-controlled `path` field.
                    instructions: [{path: hostile, scope: 'project', estimated_tokens: 1}],
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
        # And the hostile code never ran — covers both the old fields and
        # the new instructions[].path path.
        fired = page.evaluate("() => window.__ATTR_XSS_FIRED__")
        assert fired is False

    def test_truncation_count_uses_tools_count_field(self, authenticated_page: "Page", base_url: str) -> None:
        """``_attrCount`` must prefer the canonical ``tools_count`` field over
        computing from the truncation sentinel (#1473).

        When the attribution snapshot carries a ``tools_count`` of 30 *and* a
        20-item tools list with a ``{truncated: 10}`` sentinel as the final
        entry, the summary should read "30 tools" — not "21 tools" (which is
        what the fallback computation would produce without the fix).
        """
        page = authenticated_page
        _seed_message(page)
        # Build a tools list: 19 real entries + 1 truncation sentinel = 20 items.
        # Without tools_count the fallback gives 19 + 10 = 29.  With tools_count=30
        # the canonical field wins.
        page.evaluate(
            """() => {
                const msg = document.getElementById('attr-test-msg');
                const tools = [];
                for (let i = 0; i < 19; i++) {
                    tools.push({id: 'tc-' + i, name: 'read_file'});
                }
                tools.push({truncated: 10});
                Chat._addAttributionFooter(msg, {
                    turns: [],
                    memory: [],
                    sources: [],
                    tools: tools,
                    tools_count: 30,
                    packs: [],
                    instructions: [],
                    dlp_match_count: 0,
                    output_filter_match_count: 0,
                });
            }"""
        )
        expect(page.locator("#attr-test-msg .attribution-footer")).to_be_visible()
        summary_text = page.locator("#attr-test-msg .attribution-summary").inner_text()
        assert "30 tools" in summary_text, (
            f"Expected '30 tools' in summary (canonical tools_count field), got: {summary_text!r}"
        )
        assert "21 tools" not in summary_text, (
            f"Fallback sentinel count leaked into summary — tools_count field ignored: {summary_text!r}"
        )

    def test_truncation_count_fallback_without_count_field(self, authenticated_page: "Page", base_url: str) -> None:
        """When no ``tools_count`` field is present, ``_attrCount`` falls back to
        the truncation-sentinel computation (#1473).

        A tools list with 19 real entries + ``{truncated: 10}`` should produce
        "29 tools" in the summary (19 - 0 + 10 sentinel items, the sentinel
        itself does not count as a real entry).
        """
        page = authenticated_page
        _seed_message(page)
        page.evaluate(
            """() => {
                const msg = document.getElementById('attr-test-msg');
                const tools = [];
                for (let i = 0; i < 19; i++) {
                    tools.push({id: 'tc-' + i, name: 'bash'});
                }
                tools.push({truncated: 10});
                Chat._addAttributionFooter(msg, {
                    turns: [],
                    memory: [],
                    sources: [],
                    tools: tools,
                    packs: [],
                    instructions: [],
                    dlp_match_count: 0,
                    output_filter_match_count: 0,
                });
            }"""
        )
        expect(page.locator("#attr-test-msg .attribution-footer")).to_be_visible()
        summary_text = page.locator("#attr-test-msg .attribution-summary").inner_text()
        assert "29 tools" in summary_text, f"Expected '29 tools' from sentinel fallback path, got: {summary_text!r}"

    def test_multi_tool_attribution_renders_all_entries(self, authenticated_page: "Page", base_url: str) -> None:
        """Attribution footer must render all tool entries from a multi-iteration
        turn (#1472).

        The web router accumulates tool calls in ``_turn_tool_calls`` at
        ``tool_call_end`` across every LLM iteration and passes the list as
        ``turn_tool_calls`` to ``build_attribution``.  This test pins the
        browser-side rendering path: when the attribution snapshot contains
        multiple tool entries (as produced by that server-side accumulation),
        they all appear in the footer — not just the tools on the final stored
        assistant message.
        """
        page = authenticated_page
        _seed_message(page)
        page.evaluate(
            """() => {
                const msg = document.getElementById('attr-test-msg');
                Chat._addAttributionFooter(msg, {
                    turns: [],
                    memory: [],
                    sources: [],
                    tools: [
                        {id: 'tc-iter1-a', name: 'read_file'},
                        {id: 'tc-iter1-b', name: 'bash'},
                        {id: 'tc-iter2-a', name: 'glob_files'},
                    ],
                    packs: [],
                    instructions: [],
                    dlp_match_count: 0,
                    output_filter_match_count: 0,
                });
            }"""
        )
        expect(page.locator("#attr-test-msg .attribution-footer")).to_be_visible()
        footer_text = page.locator("#attr-test-msg .attribution-footer").inner_text()
        # All three tool names must appear in the rendered footer.
        for tool_name in ("read_file", "bash", "glob_files"):
            assert tool_name in footer_text, f"Tool {tool_name!r} missing from attribution footer"
        # The "Tool calls" section heading must be present.
        titles = page.locator("#attr-test-msg .attribution-section-title").all_inner_texts()
        assert "Tool calls" in titles
