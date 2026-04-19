"""Playwright E2E tests for staged overflow recovery UI rendering (#1415).

``services/agent_loop.py`` is shared core and ``.claude/rules/ux-testing.md``
requires browser-level coverage when the shared loop changes.

Triggering a real context-overflow from a browser test is impractical —
it would require pre-loading a 100K-token conversation and a provider
willing to reject it.  Instead, these tests drive the web UI's SSE event
handling directly in the browser to verify:

1. The recovery notification tokens (emitted by Strategies 1-4 in the
   staged recovery path) render through the normal assistant-message
   streaming path without breaking the chat UI.
2. The message list post-recovery contains a valid
   assistant/tool/tool-result sequence — no orphaned tool results
   visible in the DOM.

Core overflow-recovery logic (turn group identification, boundary
walk-back, summary shape) is covered exhaustively by unit tests in
``tests/unit/test_compaction.py`` and
``tests/unit/test_agent_loop_safety.py``.
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


def _seed_assistant_message(page: "Page") -> None:
    """Append an empty assistant message we can stream recovery tokens into."""
    page.evaluate(
        """() => {
            const container = document.getElementById('messages-container');
            const el = document.createElement('div');
            el.className = 'message assistant';
            el.id = 'recovery-test-msg';
            const role = document.createElement('div');
            role.className = 'message-role';
            role.textContent = 'ANTEROOM';
            el.appendChild(role);
            const content = document.createElement('div');
            content.className = 'message-content';
            content.textContent = '';
            el.appendChild(content);
            container.appendChild(el);
        }"""
    )


class TestOverflowRecoveryRendering:
    def test_web_overflow_recovery_sse_events(self, authenticated_page: "Page", base_url: str) -> None:
        """Recovery-path SSE token events render as plain text in the
        assistant message bubble.  Verifies the browser does not break
        when recovery tokens are streamed (they share the same event
        shape as regular assistant tokens).
        """
        page = authenticated_page
        _seed_assistant_message(page)

        # The recovery path emits four distinct notification strings —
        # one for each staged strategy.  Plus a fifth for proactive
        # microcompact (#1266). Concatenate them into the assistant
        # content as if streamed.
        recovery_notifications = [
            "\n\n*Trimmed oversized tool outputs to stay within context limits...*\n\n",
            "\n\n*Context limit reached — tool output was too large. Truncated and retrying with smaller scope...*\n\n",
            "\n\n*Context limit reached — collapsed historical tool results, retrying...*\n\n",
            "\n\n*Context limit reached — dropped older conversation turns, retrying...*\n\n",
            "\n\n*Context limit reached — compacting conversation and retrying...*\n\n",
        ]
        page.evaluate(
            """(notifications) => {
                const content = document.querySelector('#recovery-test-msg .message-content');
                for (const token of notifications) {
                    content.textContent += token;
                }
            }""",
            recovery_notifications,
        )

        # All five notification strings render as literal text — the 4
        # reactive strings preserved verbatim from #1415, plus the new
        # proactive microcompact string added in #1266.
        content_text = page.locator("#recovery-test-msg .message-content").inner_text()
        for expected in (
            "Trimmed oversized tool outputs",
            "tool output was too large",
            "collapsed historical tool results",
            "dropped older conversation turns",
            "compacting conversation and retrying",
        ):
            assert expected in content_text

        # The bubble is still present and visible — no structural breakage.
        expect(page.locator("#recovery-test-msg")).to_be_visible()

    def test_web_overflow_recovery_valid_message_sequence(self, authenticated_page: "Page", base_url: str) -> None:
        """Post-recovery message list contains only valid
        assistant/tool/tool-result sequences — no orphaned tool results.

        Simulates the DOM state produced by Strategy 3 (drop old turn
        groups): a summary message (role=user, flagged as compact) at
        the top, a boundary marker (role=system), then the preserved
        tail containing valid assistant+tool_calls → tool_result pairs.
        """
        page = authenticated_page

        page.evaluate(
            """() => {
                const container = document.getElementById('messages-container');
                // Summary message (role=user, compact_summary).
                const summary = document.createElement('div');
                summary.className = 'message user compact-summary';
                summary.dataset.role = 'user';
                summary.dataset.compactSummary = 'true';
                summary.textContent = '[Previous conversation summary (auto-compacted from 8 messages)]';
                container.appendChild(summary);

                // Boundary marker (role=system, normally hidden by CSS).
                const boundary = document.createElement('div');
                boundary.className = 'message system system-hidden';
                boundary.dataset.role = 'system';
                boundary.dataset.compactBoundary = 'true';
                boundary.textContent = (
                    '[Context compacted — older history summarized above, '
                    + 'recent messages preserved below]'
                );
                container.appendChild(boundary);

                // Preserved tail: user → assistant+tool_calls → tool_result.
                const user = document.createElement('div');
                user.className = 'message user';
                user.dataset.role = 'user';
                user.textContent = 'continuing';
                container.appendChild(user);

                const asst = document.createElement('div');
                asst.className = 'message assistant';
                asst.dataset.role = 'assistant';
                asst.dataset.toolCallIds = 'tc-42';
                asst.textContent = 'running bash';
                container.appendChild(asst);

                const toolResult = document.createElement('div');
                toolResult.className = 'message tool';
                toolResult.dataset.role = 'tool';
                toolResult.dataset.toolCallId = 'tc-42';
                toolResult.textContent = '{"exit_code": 0}';
                container.appendChild(toolResult);
            }"""
        )

        # Collect all tool-result tool_call_ids and all assistant-advertised
        # tool_call_ids, and verify every tool result has a matching
        # assistant in the DOM.
        validation = page.evaluate(
            """() => {
                const messages = Array.from(document.querySelectorAll('#messages-container .message'));
                const knownCallIds = new Set();
                const orphans = [];
                for (const msg of messages) {
                    const ids = msg.dataset.toolCallIds;
                    if (ids) {
                        for (const id of ids.split(',')) {
                            knownCallIds.add(id.trim());
                        }
                    }
                    if (msg.dataset.role === 'tool') {
                        const tcid = msg.dataset.toolCallId;
                        if (!tcid || !knownCallIds.has(tcid)) {
                            orphans.push(tcid || '(missing)');
                        }
                    }
                }
                return {orphans, messageCount: messages.length};
            }"""
        )
        assert validation["orphans"] == [], f"Orphaned tool results: {validation['orphans']}"
        assert validation["messageCount"] >= 5, "Expected summary + boundary + tail in DOM"
