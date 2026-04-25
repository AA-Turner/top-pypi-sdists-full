"""E2E tests for ask_user cancel-vs-empty semantics in the web UI (#1437).

Scenarios locked in by the contract change:

1. **Real empty-string submission** — clicking Submit (or pressing Enter)
   with an empty input posts ``approved: true, answer: ""``. The UI shows
   ``(empty answer)`` in the resolved card, NOT ``Cancelled``.

2. **Timeout cancel** — ``Chat.resolveAskUserCard(id, "timed_out")``
   transitions the card to the expired state with ``Expired`` status
   text, so the backend timeout path (which now returns ``None`` →
   ``{"cancelled": true}``) has a matching UI signal and does not look
   like a real empty submission.
"""

from __future__ import annotations

import pytest

try:
    import playwright  # noqa: F401

    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

requires_playwright = pytest.mark.skipif(not HAS_PLAYWRIGHT, reason="playwright not installed")

pytestmark = [pytest.mark.e2e, requires_playwright]


def _install_ask_user_fetch_capture(page) -> None:
    page.evaluate(
        """() => {
            window.__capturedRequests = [];
            const origFetch = window.fetch;
            window.fetch = async function(url, opts) {
                if (typeof url === 'string' && url.includes('/approvals/') && url.includes('/respond')) {
                    window.__capturedRequests.push({ url, body: opts && opts.body });
                    // Stub a 200 response so the JS success path runs
                    // (the synthetic prompt has no backend entry to consume).
                    return new Response(
                        JSON.stringify({ status: 'ok', approved: true, scope: 'once' }),
                        { status: 200, headers: { 'Content-Type': 'application/json' } }
                    );
                }
                return origFetch.apply(window, arguments);
            };
        }"""
    )


def _captured_answer_for(page, ask_id: str):
    import json as _json

    page.wait_for_function(
        """askId => (window.__capturedRequests || []).some(req => (req.url || '').includes(askId))""",
        ask_id,
        timeout=5000,
    )
    captured = page.evaluate("() => window.__capturedRequests")
    matches = [req for req in captured if ask_id in req.get("url", "")]
    assert len(matches) == 1
    return _json.loads(matches[0]["body"])


class TestAskUserEmptyVsCancel:
    """Empty submission and timeout must render distinctly from Cancelled."""

    def test_empty_submission_posts_approved_true_and_shows_empty_marker(self, authenticated_page) -> None:
        """Clicking Submit with an empty input sends a real empty answer.

        Verifies: the request body has ``approved: true, answer: ""`` and
        the resolved card renders the ``(empty answer)`` marker without
        the ``ask-user-cancelled`` class.
        """
        page = authenticated_page
        _install_ask_user_fetch_capture(page)

        page.evaluate(
            """() => {
                Chat.showAskUserPrompt({
                    ask_id: 'test-empty-1',
                    question: 'Anything to add?',
                });
            }"""
        )

        card = page.locator('.ask-user-prompt[data-ask-id="test-empty-1"]')
        assert card.count() == 1

        input_box = card.locator("textarea.ask-user-input")
        assert input_box.count() == 1

        submit_btn = card.locator(".ask-user-submit")
        assert submit_btn.count() == 1

        # Click Submit without typing anything.
        submit_btn.click()

        # Wait for the card to transition out of the "pending" state by
        # waiting for the .ask-user-status element to appear.
        page.wait_for_selector('.ask-user-prompt[data-ask-id="test-empty-1"] .ask-user-status', timeout=5000)

        card_class = card.get_attribute("class") or ""
        assert "ask-user-cancelled" not in card_class, (
            f"Empty submission must NOT apply ask-user-cancelled class, got: {card_class}"
        )

        status_text = card.locator(".ask-user-status").text_content() or ""
        assert "empty" in status_text.lower(), f"Expected '(empty answer)' marker, got: {status_text!r}"

        parsed = _captured_answer_for(page, "test-empty-1")
        assert parsed.get("approved") is True
        assert parsed.get("answer") == "", f"Empty submission must post answer='', got: {parsed}"

    def test_cancel_button_posts_approved_false(self, authenticated_page) -> None:
        """Clicking Cancel posts ``approved: false`` and marks the card cancelled."""
        page = authenticated_page
        _install_ask_user_fetch_capture(page)

        page.evaluate(
            """() => {
                Chat.showAskUserPrompt({
                    ask_id: 'test-cancel-1',
                    question: 'Proceed?',
                });
            }"""
        )

        card = page.locator('.ask-user-prompt[data-ask-id="test-cancel-1"]')
        cancel_btn = card.locator(".ask-user-cancel")
        assert cancel_btn.count() == 1
        cancel_btn.click()

        page.wait_for_selector(
            '.ask-user-prompt[data-ask-id="test-cancel-1"].ask-user-cancelled',
            timeout=5000,
        )

        parsed = _captured_answer_for(page, "test-cancel-1")
        assert parsed.get("approved") is False, f"Cancel button must post approved:false, got: {parsed}"

    def test_timeout_resolution_shows_expired_marker(self, authenticated_page) -> None:
        """Timeout flow resolves the card with the expired state and marker.

        After the contract change, the backend timeout path returns
        ``None`` which the tool layer maps to ``{"cancelled": true}`` —
        the UI signal for that is the ``timed_out`` resolution reason,
        which must render distinctly from ``Cancelled`` and
        ``(empty answer)``.
        """
        page = authenticated_page
        page.evaluate(
            """() => {
                Chat.showAskUserPrompt({
                    ask_id: 'test-timeout-1',
                    question: 'Waiting too long?',
                });
                Chat.resolveAskUserCard('test-timeout-1', 'timed_out');
            }"""
        )

        card = page.locator('.ask-user-prompt[data-ask-id="test-timeout-1"]')
        assert card.count() == 1

        classes = card.get_attribute("class") or ""
        assert "ask-user-expired" in classes
        # Expired must NOT be conflated with "cancelled" (cancel button)
        # or "answered" (real submission).
        assert "ask-user-cancelled" not in classes
        assert "ask-user-answered" not in classes

        status = card.locator(".ask-user-status")
        assert status.count() == 1
        status_text = status.text_content() or ""
        assert "Expired" in status_text, f"Timeout must show 'Expired' status, got: {status_text!r}"


class TestAskUserMultilineTextarea:
    """Multiline ask_user answers and option-plus-custom-answer behavior."""

    def test_shift_enter_inserts_newline_and_submit_posts_full_answer(self, authenticated_page) -> None:
        page = authenticated_page
        _install_ask_user_fetch_capture(page)
        page.evaluate(
            """() => {
                Chat.showAskUserPrompt({
                    ask_id: 'test-multiline-1',
                    question: 'Explain the choice?',
                });
            }"""
        )

        card = page.locator('.ask-user-prompt[data-ask-id="test-multiline-1"]')
        input_box = card.locator("textarea.ask-user-input")
        input_box.fill("first line")
        input_box.press("Shift+Enter")
        assert page.evaluate("() => window.__capturedRequests.length") == 0
        input_box.type("second line")
        card.locator(".ask-user-submit").click()

        parsed = _captured_answer_for(page, "test-multiline-1")
        assert parsed.get("approved") is True
        assert parsed.get("answer") == "first line\nsecond line"

    def test_enter_and_ctrl_or_cmd_enter_submit_textarea_answer(self, authenticated_page) -> None:
        page = authenticated_page
        _install_ask_user_fetch_capture(page)
        page.evaluate(
            """() => {
                Chat.showAskUserPrompt({ ask_id: 'test-enter-submit', question: 'Enter submit?' });
                Chat.showAskUserPrompt({ ask_id: 'test-ctrl-submit', question: 'Ctrl submit?' });
                Chat.showAskUserPrompt({ ask_id: 'test-cmd-submit', question: 'Cmd submit?' });
            }"""
        )

        enter_card = page.locator('.ask-user-prompt[data-ask-id="test-enter-submit"]')
        enter_card.locator("textarea.ask-user-input").fill("plain enter")
        enter_card.locator("textarea.ask-user-input").press("Enter")

        ctrl_card = page.locator('.ask-user-prompt[data-ask-id="test-ctrl-submit"]')
        ctrl_card.locator("textarea.ask-user-input").fill("ctrl enter")
        ctrl_card.locator("textarea.ask-user-input").press("Control+Enter")

        cmd_card = page.locator('.ask-user-prompt[data-ask-id="test-cmd-submit"]')
        cmd_card.locator("textarea.ask-user-input").fill("cmd enter")
        cmd_card.locator("textarea.ask-user-input").press("Meta+Enter")

        assert _captured_answer_for(page, "test-enter-submit").get("answer") == "plain enter"
        assert _captured_answer_for(page, "test-ctrl-submit").get("answer") == "ctrl enter"
        assert _captured_answer_for(page, "test-cmd-submit").get("answer") == "cmd enter"

    def test_options_prompt_supports_buttons_and_custom_multiline_answer(self, authenticated_page) -> None:
        page = authenticated_page
        _install_ask_user_fetch_capture(page)
        page.evaluate(
            """() => {
                Chat.showAskUserPrompt({
                    ask_id: 'test-options-custom',
                    question: 'Which option?',
                    options: ['A. Alpha', 'B. Beta'],
                });
            }"""
        )

        card = page.locator('.ask-user-prompt[data-ask-id="test-options-custom"]')
        assert card.locator(".ask-user-option").count() == 2
        assert card.locator("textarea.ask-user-input").count() == 1
        help_text = card.locator(".ask-user-help").text_content() or ""
        assert "Choose an option" in help_text
        assert "Shift+Enter adds a newline" in help_text

        input_box = card.locator("textarea.ask-user-input")
        input_box.fill("  custom answer")
        input_box.press("Shift+Enter")
        input_box.type("with context  ")
        card.locator(".ask-user-submit").click()

        parsed = _captured_answer_for(page, "test-options-custom")
        assert parsed.get("approved") is True
        assert parsed.get("answer") == "custom answer\nwith context"

    def test_option_button_still_submits_original_option_value(self, authenticated_page) -> None:
        page = authenticated_page
        _install_ask_user_fetch_capture(page)
        page.evaluate(
            """() => {
                Chat.showAskUserPrompt({
                    ask_id: 'test-options-button',
                    question: 'Which option?',
                    options: ['A. Alpha', 'B. Beta'],
                });
            }"""
        )

        card = page.locator('.ask-user-prompt[data-ask-id="test-options-button"]')
        card.locator(".ask-user-option").first.click()

        parsed = _captured_answer_for(page, "test-options-button")
        assert parsed.get("approved") is True
        assert parsed.get("answer") == "A. Alpha"
