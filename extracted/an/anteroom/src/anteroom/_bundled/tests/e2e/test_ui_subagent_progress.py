"""Playwright coverage for live sub-agent progress rendering (#1460)."""

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


@requires_playwright
@requires_app_deps
class TestUiSubagentProgress:
    def test_subagent_card_renders_before_parent_tool_call_end(self, page_with_conversation) -> None:
        """Live subagent cards should appear before the parent tool_call_end frame."""
        page, conv_id = page_with_conversation

        result = page.evaluate(
            """async (convId) => {
                const originalFetch = window.fetch;
                const encoder = new TextEncoder();
                const sse = (type, data) => `event: ${type}\\ndata: ${JSON.stringify(data)}\\n\\n`;

                window.fetch = async () => {
                    const stream = new ReadableStream({
                        start(controller) {
                            const emit = (delay, type, data) => {
                                setTimeout(() => controller.enqueue(encoder.encode(sse(type, data))), delay);
                            };

                            emit(0, 'tool_call_start', {
                                id: 'run-agent-1',
                                tool_name: 'run_agent',
                                input: { prompt: 'Inspect the renderer flow' },
                            });
                            emit(40, 'subagent_event', {
                                kind: 'subagent_start',
                                agent_id: 'agent-1',
                                parent_tool_call_id: 'run-agent-1',
                                prompt: 'Inspect the renderer flow',
                                model: 'gpt-test',
                            });
                            emit(80, 'subagent_event', {
                                kind: 'tool_call_start',
                                agent_id: 'agent-1',
                                parent_tool_call_id: 'run-agent-1',
                                tool_name: 'read_file',
                            });
                            emit(120, 'subagent_event', {
                                kind: 'subagent_end',
                                agent_id: 'agent-1',
                                parent_tool_call_id: 'run-agent-1',
                                status: 'succeeded',
                                elapsed_seconds: 1.2,
                                tool_calls: ['read_file'],
                            });
                            emit(200, 'tool_call_end', {
                                id: 'run-agent-1',
                                status: 'success',
                                output: { ok: true },
                            });
                            emit(240, 'done', {});
                            setTimeout(() => controller.close(), 260);
                        },
                    });

                    return new Response(stream, {
                        headers: { 'content-type': 'text/event-stream' },
                    });
                };

                try {
                    const runPromise = Chat.streamChatResponse(
                        convId,
                        JSON.stringify({ message: 'run live progress test' }),
                        {
                            'Content-Type': 'application/json',
                            'X-CSRF-Token': App._getCsrfToken(),
                        }
                    );

                    await new Promise(resolve => setTimeout(resolve, 110));
                    const midCard = document.querySelector('#subagent-agent-1');
                    const midParent = document.querySelector('#tool-run-agent-1');
                    const mid = {
                        hasCard: !!midCard,
                        cardRunning: !!midCard && midCard.classList.contains('subagent-running'),
                        toolCount: midCard?.querySelector('.subagent-tool-count')?.textContent || '',
                        loadingPromptHidden:
                            document.querySelector('.subagent-loading-prompt')?.style.display === 'none',
                        parentRunning:
                            !!midParent && midParent.classList.contains('subagent-running'),
                        parentSummary: midParent?.querySelector('summary')?.textContent || '',
                    };

                    await runPromise;

                    const finalCard = document.querySelector('#subagent-agent-1');
                    const finalParent = document.querySelector('#tool-run-agent-1');
                    return {
                        mid,
                        final: {
                            completed:
                                !!finalCard && finalCard.classList.contains('subagent-completed'),
                            running:
                                !!finalCard && finalCard.classList.contains('subagent-running'),
                            footer: finalCard?.querySelector('.subagent-footer')?.textContent || '',
                            parentRunning:
                                !!finalParent && finalParent.classList.contains('subagent-running'),
                            parentSummary: finalParent?.querySelector('summary')?.textContent || '',
                        },
                    };
                } finally {
                    window.fetch = originalFetch;
                }
            }""",
            conv_id,
        )

        assert result["mid"]["hasCard"] is True
        assert result["mid"]["cardRunning"] is True
        assert result["mid"]["toolCount"] == "1 tool"
        assert result["mid"]["loadingPromptHidden"] is True
        assert result["mid"]["parentRunning"] is True
        assert "Sub-agent complete" not in result["mid"]["parentSummary"]

        assert result["final"]["completed"] is True
        assert result["final"]["running"] is False
        assert "Done in 1.2s" in result["final"]["footer"]
        assert "1 tool call" in result["final"]["footer"]
        assert result["final"]["parentRunning"] is False
        assert result["final"]["parentSummary"] == "Sub-agent complete"

    def test_failure_terminal_frame_uses_semantic_failure_class(self, page_with_conversation) -> None:
        """Failure state should render distinct semantic + backward-compatible classes."""
        page, conv_id = page_with_conversation

        result = page.evaluate(
            """(convId) => {
                if (typeof App !== 'undefined' && App.loadConversation) {
                    App.loadConversation(convId);
                }
                Chat._handleSSEEvent('tool_call_start', {
                    id: 'run-agent-fail',
                    tool_name: 'run_agent',
                    input: { prompt: 'Investigate failing path' },
                });
                Chat._handleSSEEvent('subagent_event', {
                    kind: 'subagent_start',
                    agent_id: 'agent-fail',
                    parent_tool_call_id: 'run-agent-fail',
                    prompt: 'Investigate failing path',
                    model: 'gpt-test',
                });
                Chat._handleSSEEvent('subagent_event', {
                    kind: 'subagent_end',
                    agent_id: 'agent-fail',
                    parent_tool_call_id: 'run-agent-fail',
                    status: 'failed',
                    elapsed_seconds: 0.4,
                    tool_calls: [],
                    error: 'boom on first line\\nstack trace',
                });

                const card = document.querySelector('#subagent-agent-fail');
                return {
                    failed: !!card && card.classList.contains('subagent-failed'),
                    legacyError: !!card && card.classList.contains('subagent-error'),
                    completed: !!card && card.classList.contains('subagent-completed'),
                    footer: card?.querySelector('.subagent-footer')?.textContent || '',
                };
            }""",
            conv_id,
        )

        assert result["failed"] is True
        assert result["legacyError"] is True
        assert result["completed"] is False
        assert "Failed: boom on first line" in result["footer"]

    def test_parallel_parent_run_agent_wrappers_keep_cards_separate(self, page_with_conversation) -> None:
        """Concurrent run_agent wrappers should not steal each other's subagent cards."""
        page, conv_id = page_with_conversation

        result = page.evaluate(
            """(convId) => {
                if (typeof App !== 'undefined' && App.loadConversation) {
                    App.loadConversation(convId);
                }
                Chat._handleSSEEvent('tool_call_start', {
                    id: 'run-agent-a',
                    tool_name: 'run_agent',
                    input: { prompt: 'First task' },
                });
                Chat._handleSSEEvent('tool_call_start', {
                    id: 'run-agent-b',
                    tool_name: 'run_agent',
                    input: { prompt: 'Second task' },
                });
                Chat._handleSSEEvent('subagent_event', {
                    kind: 'subagent_start',
                    agent_id: 'agent-a',
                    parent_tool_call_id: 'run-agent-a',
                    prompt: 'First task',
                    model: 'gpt-test',
                });
                Chat._handleSSEEvent('subagent_event', {
                    kind: 'subagent_start',
                    agent_id: 'agent-b',
                    parent_tool_call_id: 'run-agent-b',
                    prompt: 'Second task',
                    model: 'gpt-test',
                });

                const wrapperA = document.querySelector('#tool-run-agent-a .subagent-cards-container');
                const wrapperB = document.querySelector('#tool-run-agent-b .subagent-cards-container');
                return {
                    aHasA: !!wrapperA?.querySelector('#subagent-agent-a'),
                    aHasB: !!wrapperA?.querySelector('#subagent-agent-b'),
                    bHasA: !!wrapperB?.querySelector('#subagent-agent-a'),
                    bHasB: !!wrapperB?.querySelector('#subagent-agent-b'),
                };
            }""",
            conv_id,
        )

        assert result["aHasA"] is True
        assert result["aHasB"] is False
        assert result["bHasA"] is False
        assert result["bHasB"] is True
