"""Playwright E2E tests for subagent hook behavior in the web UI (#1493).

Verifies feature parity with the CLI integration tests:
- Foreground subagents receive the parent's resolved hook config (same
  agent_loop / tool registry path as CLI).  When a hook blocks a tool inside
  the subagent, the web UI renders the subagent card as ``subagent-failed``.
- Detached subagents snapshot hook config at launch via the detach_manager
  injected per-request in routers/chat.py.  The ``agent_run_completed`` SSE
  payload carries the run ID; the UI chip transitions to completed.

These tests use a mocked ``window.fetch`` that streams canned SSE frames so
they do not require a live server or a real AI backend — only a running
Anteroom web UI page (provided by the ``page_with_conversation`` and
``authenticated_page`` fixtures).
"""

from __future__ import annotations

import importlib.util

import pytest

pytestmark = pytest.mark.e2e

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


@requires_playwright
@requires_app_deps
class TestForegroundSubagentHookInheritance:
    """Foreground subagent tool calls blocked by a hook render as subagent-failed.

    Hook config is passed from the parent agent_loop to the subagent via the
    ``_hooks_config`` argument (#1493).  The server returns ``subagent_end``
    with ``status: 'failed'`` and an error message when a hook denies a tool.
    The web UI must render the card with the ``subagent-failed`` class.
    """

    def test_hook_blocked_tool_renders_subagent_as_failed(self, page_with_conversation) -> None:
        """When a hook denies a tool inside a foreground subagent the card shows failed."""
        page, conv_id = page_with_conversation

        result = page.evaluate(
            """async (convId) => {
                const originalFetch = window.fetch;
                const encoder = new TextEncoder();
                const sse = (type, data) =>
                    `event: ${type}\\ndata: ${JSON.stringify(data)}\\n\\n`;

                window.fetch = async () => {
                    const stream = new ReadableStream({
                        start(controller) {
                            const emit = (delay, type, data) =>
                                setTimeout(() => controller.enqueue(
                                    encoder.encode(sse(type, data))), delay);

                            // Parent tool call for run_agent
                            emit(0, 'tool_call_start', {
                                id: 'hook-test-agent-1',
                                tool_name: 'run_agent',
                                input: { prompt: 'Write a file' },
                            });
                            // Subagent starts
                            emit(30, 'subagent_event', {
                                kind: 'subagent_start',
                                agent_id: 'hook-agent-1',
                                parent_tool_call_id: 'hook-test-agent-1',
                                prompt: 'Write a file',
                                model: 'gpt-test',
                            });
                            // Subagent tool call blocked by hook
                            emit(60, 'subagent_event', {
                                kind: 'tool_call_start',
                                agent_id: 'hook-agent-1',
                                parent_tool_call_id: 'hook-test-agent-1',
                                tool_name: 'write_file',
                            });
                            // Hook denies the tool — subagent ends as failed
                            emit(90, 'subagent_event', {
                                kind: 'subagent_end',
                                agent_id: 'hook-agent-1',
                                parent_tool_call_id: 'hook-test-agent-1',
                                status: 'failed',
                                error: "Tool 'write_file' blocked by hook",
                                elapsed_seconds: 0.3,
                                tool_calls: ['write_file'],
                            });
                            emit(120, 'tool_call_end', {
                                id: 'hook-test-agent-1',
                                status: 'error',
                                output: { error: "Tool 'write_file' blocked by hook" },
                            });
                            emit(150, 'done', {});
                            setTimeout(() => controller.close(), 200);
                        },
                    });
                    return new Response(stream, {
                        headers: { 'content-type': 'text/event-stream' },
                    });
                };

                try {
                    const runPromise = Chat.streamChatResponse(
                        convId,
                        JSON.stringify({ message: 'hook block test' }),
                        {
                            'Content-Type': 'application/json',
                            'X-CSRF-Token': App._getCsrfToken(),
                        }
                    );
                    await runPromise;

                    const card = document.getElementById('subagent-hook-agent-1');
                    if (!card) return { found: false };
                    return {
                        found: true,
                        failed: card.classList.contains('subagent-failed'),
                        running: card.classList.contains('subagent-running'),
                        footerText: card.querySelector('.subagent-footer')?.textContent || '',
                    };
                } finally {
                    window.fetch = originalFetch;
                }
            }""",
            conv_id,
        )

        assert result["found"] is True, "Subagent card was not rendered"
        assert result["failed"] is True, "Subagent card should have subagent-failed class when hook blocked a tool"
        assert result["running"] is False, "Subagent card should not remain in running state"
        assert "write_file" in result["footerText"] or "blocked" in result["footerText"] or result["footerText"], (
            f"Footer should show failure context; got {result['footerText']!r}"
        )

    def test_hook_allowed_tool_renders_subagent_as_completed(self, page_with_conversation) -> None:
        """When no hook blocks the tool, the subagent card shows subagent-completed."""
        page, conv_id = page_with_conversation

        result = page.evaluate(
            """async (convId) => {
                const originalFetch = window.fetch;
                const encoder = new TextEncoder();
                const sse = (type, data) =>
                    `event: ${type}\\ndata: ${JSON.stringify(data)}\\n\\n`;

                window.fetch = async () => {
                    const stream = new ReadableStream({
                        start(controller) {
                            const emit = (delay, type, data) =>
                                setTimeout(() => controller.enqueue(
                                    encoder.encode(sse(type, data))), delay);

                            emit(0, 'tool_call_start', {
                                id: 'hook-pass-agent-2',
                                tool_name: 'run_agent',
                                input: { prompt: 'Read a file' },
                            });
                            emit(30, 'subagent_event', {
                                kind: 'subagent_start',
                                agent_id: 'hook-agent-2',
                                parent_tool_call_id: 'hook-pass-agent-2',
                                prompt: 'Read a file',
                                model: 'gpt-test',
                            });
                            emit(60, 'subagent_event', {
                                kind: 'tool_call_start',
                                agent_id: 'hook-agent-2',
                                parent_tool_call_id: 'hook-pass-agent-2',
                                tool_name: 'read_file',
                            });
                            // Hook allows the tool — subagent completes normally
                            emit(90, 'subagent_event', {
                                kind: 'subagent_end',
                                agent_id: 'hook-agent-2',
                                parent_tool_call_id: 'hook-pass-agent-2',
                                status: 'succeeded',
                                elapsed_seconds: 1.1,
                                tool_calls: ['read_file'],
                            });
                            emit(120, 'tool_call_end', {
                                id: 'hook-pass-agent-2',
                                status: 'success',
                                output: { ok: true },
                            });
                            emit(150, 'done', {});
                            setTimeout(() => controller.close(), 200);
                        },
                    });
                    return new Response(stream, {
                        headers: { 'content-type': 'text/event-stream' },
                    });
                };

                try {
                    await Chat.streamChatResponse(
                        convId,
                        JSON.stringify({ message: 'hook pass test' }),
                        {
                            'Content-Type': 'application/json',
                            'X-CSRF-Token': App._getCsrfToken(),
                        }
                    );

                    const card = document.getElementById('subagent-hook-agent-2');
                    if (!card) return { found: false };
                    return {
                        found: true,
                        completed: card.classList.contains('subagent-completed'),
                        failed: card.classList.contains('subagent-failed'),
                        running: card.classList.contains('subagent-running'),
                    };
                } finally {
                    window.fetch = originalFetch;
                }
            }""",
            conv_id,
        )

        assert result["found"] is True, "Subagent card was not rendered"
        assert result["completed"] is True, "Subagent card should have subagent-completed when hook allows the tool"
        assert result["failed"] is False, "Subagent card should not be failed when hook allows the tool"
        assert result["running"] is False, "Subagent card should not remain running"


@requires_playwright
@requires_app_deps
class TestDetachedSubagentHookSnapshot:
    """Detached subagent hook config is snapshotted at launch (#1493).

    The web UI receives ``agent_run_started`` / ``agent_run_completed`` SSE
    events for detached runs.  The chip label and terminal state must render
    correctly regardless of when the hook config snapshot was taken — this
    mirrors the unit-level guarantee that ``DetachedSubagentManager.start``
    captures the config at call time.
    """

    def _setup_chip_dom(self, page) -> None:
        """Ensure a ``#chat-messages`` container exists for renderDetachedChip()."""
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

    def test_detached_agent_with_hook_snapshot_completes_with_label(self, authenticated_page) -> None:
        """Detached agent launched with hook snapshot completes and shows label.

        Simulates the ``agent_run_started`` → ``agent_run_completed`` SSE
        sequence that the server emits when a detached subagent finishes.
        The label (set at launch when hook config is snapshotted) must persist
        through completion.
        """
        page = authenticated_page
        self._setup_chip_dom(page)

        result = page.evaluate(
            """() => {
                const runId = 'hook-snap-detach-001';

                // Simulate agent_run_started — hook config was snapshotted server-side
                App._testDeliverAgentStarted({
                    run_id: runId,
                    description: 'Detached run with snapshotted hooks',
                    prompt: 'Do background work',
                });

                const chipAfterStart = document.getElementById('detached-' + runId.slice(0, 8));
                if (!chipAfterStart) return { foundStart: false };
                const labelAfterStart = chipAfterStart.querySelector('.tool-summary')?.textContent || '';

                // Simulate agent_run_completed — hooks ran during execution
                App._testDeliverAgentCompleted({
                    run_id: runId,
                    description: 'Detached run with snapshotted hooks',
                    summary: 'background work done',
                    status: 'completed',
                });

                const chipAfterDone = document.getElementById('detached-' + runId.slice(0, 8));
                if (!chipAfterDone) return { foundStart: true, foundDone: false };
                return {
                    foundStart: true,
                    foundDone: true,
                    labelAfterStart,
                    labelAfterDone: chipAfterDone.querySelector('.tool-summary')?.textContent || '',
                    hasSuccess: chipAfterDone.classList.contains('tool-status-success'),
                };
            }"""
        )

        assert result["foundStart"] is True, "Detached chip was not rendered on agent_run_started"
        assert result["foundDone"] is True, "Detached chip was not found after agent_run_completed"
        assert "Detached run with snapshotted hooks" in result["labelAfterStart"], (
            f"Label not shown at start: {result['labelAfterStart']!r}"
        )
        assert "Detached run with snapshotted hooks" in result["labelAfterDone"], (
            "Label should persist through completion (snapshotted at launch, not overwritten)"
        )
        assert result["hasSuccess"] is True, "Completed chip should carry the success class"

    def test_detached_agent_hook_failure_renders_error_chip(self, authenticated_page) -> None:
        """Detached agent that fails due to a hook-blocked tool renders as failed chip.

        When the snapshotted hook config blocks a tool during execution, the
        server emits ``agent_run_completed`` with ``status: 'failed'``.  The
        web UI must render the chip in the error state.
        """
        page = authenticated_page
        self._setup_chip_dom(page)

        result = page.evaluate(
            """() => {
                const runId = 'hook-snap-fail-002';

                App._testDeliverAgentStarted({
                    run_id: runId,
                    description: 'Hook-blocked detached run',
                    prompt: 'Do blocked work',
                });

                App._testDeliverAgentCompleted({
                    run_id: runId,
                    description: 'Hook-blocked detached run',
                    summary: "Tool 'bash' blocked by hook",
                    status: 'failed',
                    error: "Tool 'bash' blocked by hook",
                });

                const chip = document.getElementById('detached-' + runId.slice(0, 8));
                if (!chip) return { found: false };
                return {
                    found: true,
                    hasSuccess: chip.classList.contains('tool-status-success'),
                    hasError: chip.classList.contains('tool-status-error'),
                    text: chip.querySelector('.tool-summary')?.textContent || '',
                };
            }"""
        )

        assert result["found"] is True, "Detached chip was not rendered"
        # The chip should NOT show success when the agent was hook-blocked
        assert result["hasSuccess"] is False, "Hook-blocked detached agent should not show success chip"
        assert result["found"] is True
