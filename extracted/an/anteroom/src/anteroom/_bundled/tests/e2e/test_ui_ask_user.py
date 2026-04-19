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


class TestAskUserEmptyVsCancel:
    """Empty submission and timeout must render distinctly from Cancelled."""

    def test_empty_submission_posts_approved_true_and_shows_empty_marker(self, authenticated_page) -> None:
        """Clicking Submit with an empty input sends a real empty answer.

        Verifies: the request body has ``approved: true, answer: ""`` and
        the resolved card renders the ``(empty answer)`` marker without
        the ``ask-user-cancelled`` class.
        """
        page = authenticated_page

        page.evaluate(
            """() => {
                window.__capturedRequests = [];
                const origFetch = window.fetch;
                window.fetch = async function(url, opts) {
                    if (typeof url === 'string' && url.includes('/approvals/') && url.includes('/respond')) {
                        window.__capturedRequests.push({ url, body: opts && opts.body });
                        // Stub a 200 response so the JS success path runs
                        // (the synthetic prompt has no backend entry to
                        // consume — the real endpoint would 404).
                        return new Response(
                            JSON.stringify({ status: 'ok', approved: true, scope: 'once' }),
                            { status: 200, headers: { 'Content-Type': 'application/json' } }
                        );
                    }
                    return origFetch.apply(window, arguments);
                };
            }"""
        )

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

        input_box = card.locator(".ask-user-input")
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

        captured = page.evaluate("() => window.__capturedRequests")
        empty_submissions = [req for req in captured if "test-empty-1" in req.get("url", "")]
        assert len(empty_submissions) == 1
        body = empty_submissions[0]["body"]
        import json as _json

        parsed = _json.loads(body)
        assert parsed.get("approved") is True
        assert parsed.get("answer") == "", f"Empty submission must post answer='', got: {parsed}"

    def test_cancel_button_posts_approved_false(self, authenticated_page) -> None:
        """Clicking Cancel posts ``approved: false`` and marks the card cancelled."""
        page = authenticated_page

        page.evaluate(
            """() => {
                window.__capturedRequests = [];
                const origFetch = window.fetch;
                window.fetch = async function(url, opts) {
                    if (typeof url === 'string' && url.includes('/approvals/') && url.includes('/respond')) {
                        window.__capturedRequests.push({ url, body: opts && opts.body });
                        // Stub a 200 response so the JS success path runs
                        // (the synthetic prompt has no backend entry to
                        // consume — the real endpoint would 404).
                        return new Response(
                            JSON.stringify({ status: 'ok', approved: true, scope: 'once' }),
                            { status: 200, headers: { 'Content-Type': 'application/json' } }
                        );
                    }
                    return origFetch.apply(window, arguments);
                };
            }"""
        )

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

        captured = page.evaluate("() => window.__capturedRequests")
        cancel_posts = [req for req in captured if "test-cancel-1" in req.get("url", "")]
        assert len(cancel_posts) == 1
        import json as _json

        parsed = _json.loads(cancel_posts[0]["body"])
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
