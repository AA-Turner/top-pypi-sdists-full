"""Playwright E2E coverage for detached agent chip description label (#1461).

Tests the ``agent_run_started`` / ``agent_run_completed`` SSE handler logic
in app.js that selects the ``description`` field over ``prompt``/``summary``
when rendering the detached-agent chip label.

Coverage:
- description label is shown on start
- description label is preserved through started → completed (not overwritten by summary)
- fallback: when no description is present on completed, summary is used
- fallback: when no description is present on started, prompt is used
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


def _setup_chip_dom(page) -> None:
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


@requires_playwright
@requires_app_deps
class TestDetachedAgentDescriptionLabel:
    """Verify the description label preference fix in app.js agent_run_* handlers."""

    def test_started_event_shows_description_over_prompt(self, authenticated_page) -> None:
        """agent_run_started with description should render description, not prompt."""
        page = authenticated_page
        _setup_chip_dom(page)

        result = page.evaluate(
            """() => {
                App._testDeliverAgentStarted({
                    run_id: 'desc-start-001',
                    description: 'my custom label',
                    prompt: 'fallback prompt',
                });
                const chip = document.getElementById('detached-desc-sta');
                if (!chip) return { found: false };
                return {
                    found: true,
                    text: chip.querySelector('.tool-summary')?.textContent || '',
                };
            }"""
        )

        assert result["found"] is True, "Detached chip was not rendered"
        assert "my custom label" in result["text"], f"Expected 'my custom label' in {result['text']!r}"
        assert "fallback prompt" not in result["text"], "prompt should not appear when description is set"

    def test_started_event_falls_back_to_prompt_when_no_description(self, authenticated_page) -> None:
        """agent_run_started without description should fall back to prompt."""
        page = authenticated_page
        _setup_chip_dom(page)

        result = page.evaluate(
            """() => {
                App._testDeliverAgentStarted({
                    run_id: 'prompt-start-002',
                    prompt: 'the prompt text',
                });
                const chip = document.getElementById('detached-prompt-s');
                if (!chip) return { found: false };
                return {
                    found: true,
                    text: chip.querySelector('.tool-summary')?.textContent || '',
                };
            }"""
        )

        assert result["found"] is True, "Detached chip was not rendered"
        assert "the prompt text" in result["text"], f"Expected prompt fallback in {result['text']!r}"

    def test_completed_event_preserves_description_label(self, authenticated_page) -> None:
        """Description label set on start must persist through agent_run_completed.

        This is the core fix in #1461: previously completed overwrote the label
        with summary; now description takes precedence.
        """
        page = authenticated_page
        _setup_chip_dom(page)

        result = page.evaluate(
            """() => {
                const runId = 'persist-label-003';

                // Simulate started with a description
                App._testDeliverAgentStarted({
                    run_id: runId,
                    description: 'my custom label',
                    prompt: 'fallback prompt',
                });

                // Simulate completed — description is echoed back, summary is different
                App._testDeliverAgentCompleted({
                    run_id: runId,
                    description: 'my custom label',
                    summary: 'agent finished doing work',
                    status: 'completed',
                });

                const chipId = 'detached-' + runId.slice(0, 8);
                const chip = document.getElementById(chipId);
                if (!chip) return { found: false };
                return {
                    found: true,
                    text: chip.querySelector('.tool-summary')?.textContent || '',
                    hasSuccess: chip.classList.contains('tool-status-success'),
                };
            }"""
        )

        assert result["found"] is True, "Detached chip was not rendered"
        assert "my custom label" in result["text"], (
            f"Description label should be preserved on completion; got {result['text']!r}"
        )
        assert "agent finished doing work" not in result["text"], "Summary should not replace the description label"
        assert result["hasSuccess"] is True, "Completed chip should have tool-status-success class"

    def test_completed_event_falls_back_to_summary_when_no_description(self, authenticated_page) -> None:
        """When agent_run_completed has no description, summary is used as the label."""
        page = authenticated_page
        _setup_chip_dom(page)

        result = page.evaluate(
            """() => {
                App._testDeliverAgentCompleted({
                    run_id: 'summary-fall-004',
                    summary: 'processed 42 files',
                    status: 'completed',
                });

                const chip = document.getElementById('detached-summary-');
                if (!chip) return { found: false };
                return {
                    found: true,
                    text: chip.querySelector('.tool-summary')?.textContent || '',
                    hasSuccess: chip.classList.contains('tool-status-success'),
                };
            }"""
        )

        assert result["found"] is True, "Detached chip was not rendered"
        assert "processed 42 files" in result["text"], f"Expected summary fallback in chip text; got {result['text']!r}"
        assert result["hasSuccess"] is True

    def test_completed_dedup_does_not_re_render_on_second_delivery(self, authenticated_page) -> None:
        """A duplicate agent_run_completed (SSE reconnect) must not re-render the chip."""
        page = authenticated_page
        _setup_chip_dom(page)

        result = page.evaluate(
            """() => {
                const runId = 'dedup-agent-005';
                const data = {
                    run_id: runId,
                    description: 'dedup label',
                    summary: 'should not overwrite',
                    status: 'completed',
                };

                App._testDeliverAgentCompleted(data);
                const textAfterFirst = document.getElementById('detached-' + runId.slice(0, 8))
                    ?.querySelector('.tool-summary')?.textContent || '';

                // Deliver again (reconnect duplicate)
                App._testDeliverAgentCompleted({ ...data, summary: 'overwrite attempt' });

                const textAfterSecond = document.getElementById('detached-' + runId.slice(0, 8))
                    ?.querySelector('.tool-summary')?.textContent || '';

                return { textAfterFirst, textAfterSecond };
            }"""
        )

        assert "dedup label" in result["textAfterFirst"]
        assert result["textAfterFirst"] == result["textAfterSecond"], (
            "Second delivery should not modify the chip (dedup guard)"
        )
