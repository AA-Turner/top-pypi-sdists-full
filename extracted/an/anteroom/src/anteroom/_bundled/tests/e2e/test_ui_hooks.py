"""Playwright E2E coverage for hook_outcome SSE event and .hook-outcome-notice rendering (#1491).

Tests that:
- A pre-tool hook block renders a .hook-outcome-notice card in the chat stream
- The card shows the tool name
- A post-tool hook block is distinguished from a pre-tool block
- The reason/message is rendered in the card when present
"""

from __future__ import annotations

import importlib.util

import pytest

pytestmark = [pytest.mark.e2e]

try:
    import playwright  # noqa: F401

    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

requires_playwright = pytest.mark.skipif(not HAS_PLAYWRIGHT, reason="playwright not installed")
requires_app_deps = pytest.mark.skipif(
    importlib.util.find_spec("filetype") is None,
    reason="app test dependency filetype not installed",
)


def _setup_chat_dom(page) -> None:
    """Ensure a #chat-messages container exists for renderHookOutcome()."""
    page.evaluate(
        """() => {
            let cm = document.getElementById('chat-messages');
            if (!cm) {
                cm = document.createElement('div');
                cm.id = 'chat-messages';
                document.body.appendChild(cm);
            }
        }"""
    )


@requires_playwright
@requires_app_deps
class TestHookOutcomeNoticeRendering:
    """Verify the .hook-outcome-notice card is rendered when hook_outcome SSE fires."""

    def test_pre_tool_hook_block_renders_notice_card(self, authenticated_page) -> None:
        """A pre-tool hook deny should render a .hook-outcome-notice in the chat."""
        page = authenticated_page
        _setup_chat_dom(page)

        result = page.evaluate(
            """() => {
                App._testDeliverHookOutcome({
                    tool_name: 'bash',
                    outcome: 'deny',
                    approval_decision: 'hook_denied',
                    message: 'Network access blocked by security policy',
                });
                const notices = document.querySelectorAll('.hook-outcome-notice');
                if (notices.length === 0) return { found: false };
                const last = notices[notices.length - 1];
                return {
                    found: true,
                    titleText: last.querySelector('.hook-outcome-title')?.textContent || '',
                    reasonText: last.querySelector('.hook-outcome-reason')?.textContent || '',
                    hasIcon: !!last.querySelector('.hook-outcome-icon'),
                };
            }"""
        )

        assert result["found"] is True, ".hook-outcome-notice card was not rendered"
        assert "bash" in result["titleText"], f"Expected tool name in title; got {result['titleText']!r}"
        assert "Hook blocked" in result["titleText"] or "blocked" in result["titleText"].lower(), (
            f"Expected 'blocked' in title; got {result['titleText']!r}"
        )
        assert "Network access blocked by security policy" in result["reasonText"], (
            f"Expected reason text in card; got {result['reasonText']!r}"
        )
        assert result["hasIcon"] is True, ".hook-outcome-icon element missing"

    def test_post_tool_hook_block_shows_blocked_output_title(self, authenticated_page) -> None:
        """A post-tool hook deny (post_hook_denied) renders 'blocked output' title."""
        page = authenticated_page
        _setup_chat_dom(page)

        result = page.evaluate(
            """() => {
                App._testDeliverHookOutcome({
                    tool_name: 'write_file',
                    outcome: 'deny',
                    approval_decision: 'post_hook_denied',
                    message: 'Output contains sensitive data',
                });
                const notices = document.querySelectorAll('.hook-outcome-notice');
                if (notices.length === 0) return { found: false };
                const last = notices[notices.length - 1];
                return {
                    found: true,
                    titleText: last.querySelector('.hook-outcome-title')?.textContent || '',
                    reasonText: last.querySelector('.hook-outcome-reason')?.textContent || '',
                };
            }"""
        )

        assert result["found"] is True, ".hook-outcome-notice card was not rendered"
        assert "write_file" in result["titleText"], f"Expected tool name in title; got {result['titleText']!r}"
        assert "output" in result["titleText"].lower() or "blocked" in result["titleText"].lower(), (
            f"Expected post-hook framing in title; got {result['titleText']!r}"
        )
        assert "Output contains sensitive data" in result["reasonText"], (
            f"Expected reason text in card; got {result['reasonText']!r}"
        )

    def test_hook_outcome_no_message_renders_title_only(self, authenticated_page) -> None:
        """A hook block with no message renders the title but no reason element."""
        page = authenticated_page
        _setup_chat_dom(page)

        result = page.evaluate(
            """() => {
                App._testDeliverHookOutcome({
                    tool_name: 'read_file',
                    outcome: 'deny',
                    approval_decision: 'hook_denied',
                    message: '',
                });
                const notices = document.querySelectorAll('.hook-outcome-notice');
                if (notices.length === 0) return { found: false };
                const last = notices[notices.length - 1];
                return {
                    found: true,
                    titleText: last.querySelector('.hook-outcome-title')?.textContent || '',
                    hasReason: !!last.querySelector('.hook-outcome-reason'),
                };
            }"""
        )

        assert result["found"] is True, ".hook-outcome-notice card was not rendered"
        assert "read_file" in result["titleText"], f"Expected tool name in title; got {result['titleText']!r}"
        assert result["hasReason"] is False, "No reason element should be added when message is empty"

    def test_multiple_hook_blocks_each_render_a_notice(self, authenticated_page) -> None:
        """Two successive hook blocks each produce their own notice card."""
        page = authenticated_page
        _setup_chat_dom(page)

        # Remove prior notices so the count is predictable
        page.evaluate(
            """() => {
                document.querySelectorAll('.hook-outcome-notice').forEach(el => el.remove());
            }"""
        )

        result = page.evaluate(
            """() => {
                App._testDeliverHookOutcome({
                    tool_name: 'bash',
                    outcome: 'deny',
                    approval_decision: 'hook_denied',
                    message: 'first block',
                });
                App._testDeliverHookOutcome({
                    tool_name: 'grep',
                    outcome: 'deny',
                    approval_decision: 'hook_denied',
                    message: 'second block',
                });
                const notices = document.querySelectorAll('.hook-outcome-notice');
                return {
                    count: notices.length,
                    firstTool: notices[0]?.querySelector('.hook-outcome-title')?.textContent || '',
                    secondTool: notices[1]?.querySelector('.hook-outcome-title')?.textContent || '',
                };
            }"""
        )

        assert result["count"] == 2, f"Expected 2 notice cards; got {result['count']}"
        assert "bash" in result["firstTool"], f"First card should mention bash; got {result['firstTool']!r}"
        assert "grep" in result["secondTool"], f"Second card should mention grep; got {result['secondTool']!r}"
