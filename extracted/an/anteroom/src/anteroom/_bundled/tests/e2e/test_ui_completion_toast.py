"""E2E tests for completion notification toasts (#1315).

Tests the showCompletionToast() function from chat.js and the SSE dedup
logic in app.js via the _testDeliver* hooks, exercising the real handler
code path including _deliveredNotificationIds state.
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


def _setup_toast_dom(page) -> None:
    """Create the minimal DOM elements that showCompletionToast() needs.

    The function reads from #chat-messages (scrollHeight) and appends to
    .chat-area or #chat-column.  We create both and set scroll state so
    the toast is NOT suppressed by the "at bottom" check.
    """
    page.evaluate(
        """() => {
            // Create chat-messages with a tall scrollHeight so isAtBottom is false
            let cm = document.getElementById('chat-messages');
            if (!cm) {
                cm = document.createElement('div');
                cm.id = 'chat-messages';
                cm.style.height = '200px';
                cm.style.overflow = 'auto';
                document.body.appendChild(cm);
            }
            // Fill with enough content to make scrollHeight > clientHeight
            cm.innerHTML = '<div style="height:2000px">spacer</div>';

            // Create .chat-area container where the toast is appended
            let ca = document.querySelector('.chat-area');
            if (!ca) {
                ca = document.createElement('div');
                ca.className = 'chat-area';
                document.body.appendChild(ca);
            }
        }"""
    )


class TestShowCompletionToast:
    """Verify the Chat.showCompletionToast() rendering behaviour."""

    def test_toast_renders_with_correct_content(self, authenticated_page) -> None:
        page = authenticated_page
        _setup_toast_dom(page)

        page.evaluate("""() => Chat.showCompletionToast('Task abc12345: completed')""")

        toast = page.locator(".completion-toast")
        assert toast.count() == 1
        assert "Task abc12345: completed" in toast.text_content()

    def test_toast_has_dismiss_button(self, authenticated_page) -> None:
        page = authenticated_page
        _setup_toast_dom(page)

        page.evaluate("""() => Chat.showCompletionToast('Agent xyz: done')""")

        dismiss = page.locator(".completion-toast-dismiss")
        assert dismiss.count() >= 1
        assert dismiss.first.get_attribute("aria-label") == "Dismiss"

    def test_dismiss_button_removes_toast(self, authenticated_page) -> None:
        page = authenticated_page
        _setup_toast_dom(page)

        page.evaluate("""() => Chat.showCompletionToast('Task to dismiss')""")

        toast = page.locator(".completion-toast")
        assert toast.count() >= 1

        page.locator(".completion-toast-dismiss").first.click()
        page.wait_for_timeout(200)

        assert page.locator(".completion-toast").count() == 0

    def test_toast_has_accessibility_attributes(self, authenticated_page) -> None:
        page = authenticated_page
        _setup_toast_dom(page)

        page.evaluate("""() => Chat.showCompletionToast('Accessible toast')""")

        toast = page.locator(".completion-toast")
        assert toast.get_attribute("role") == "alert"
        assert toast.get_attribute("aria-live") == "polite"

    def test_toast_not_shown_when_scrolled_to_bottom(self, authenticated_page) -> None:
        """When the user is at the bottom of the chat, no toast should appear."""
        page = authenticated_page

        page.evaluate(
            """() => {
                let cm = document.getElementById('chat-messages');
                if (!cm) {
                    cm = document.createElement('div');
                    cm.id = 'chat-messages';
                    cm.style.height = '200px';
                    cm.style.overflow = 'auto';
                    document.body.appendChild(cm);
                }
                // Short content so scrollHeight ~= clientHeight (isAtBottom = true)
                cm.innerHTML = '<div style="height:10px">short</div>';

                let ca = document.querySelector('.chat-area');
                if (!ca) {
                    ca = document.createElement('div');
                    ca.className = 'chat-area';
                    document.body.appendChild(ca);
                }
            }"""
        )

        page.evaluate("""() => Chat.showCompletionToast('should not appear')""")

        assert page.locator(".completion-toast").count() == 0

    def test_toast_auto_dismisses(self, authenticated_page) -> None:
        """Toast auto-removes after 6 seconds. We use a fast clock to avoid waiting."""
        page = authenticated_page
        _setup_toast_dom(page)

        # Override setTimeout to fire immediately for the auto-dismiss
        page.evaluate(
            """() => {
                const origSetTimeout = window.setTimeout;
                window.setTimeout = (fn, ms) => origSetTimeout(fn, 50);
                Chat.showCompletionToast('auto dismiss test');
                // Restore original
                window.setTimeout = origSetTimeout;
            }"""
        )

        page.wait_for_timeout(200)
        assert page.locator(".completion-toast").count() == 0

    def test_multiple_toasts_stack(self, authenticated_page) -> None:
        page = authenticated_page
        _setup_toast_dom(page)

        page.evaluate(
            """() => {
                Chat.showCompletionToast('Toast 1');
                Chat.showCompletionToast('Toast 2');
            }"""
        )

        toasts = page.locator(".completion-toast")
        assert toasts.count() == 2


class TestDeliveredNotificationDedup:
    """Verify _deliveredNotificationIds prevents duplicate toasts via real SSE handler hooks."""

    def test_task_completed_dedup(self, authenticated_page) -> None:
        """Delivering the same task_completed twice via the real handler only renders one toast."""
        page = authenticated_page
        _setup_toast_dom(page)

        count = page.evaluate(
            """() => {
                const data = { task_id: 'dedup-task-001', command: 'echo hello', status: 'completed', exit_code: 0 };

                // First delivery via the real SSE handler logic
                App._testDeliverTaskCompleted(data);
                // Second delivery (reconnect duplicate)
                App._testDeliverTaskCompleted(data);

                return document.querySelectorAll('.completion-toast').length;
            }"""
        )

        assert count == 1

    def test_agent_completed_dedup(self, authenticated_page) -> None:
        """Delivering the same agent_run_completed twice via the real handler only renders one toast."""
        page = authenticated_page
        _setup_toast_dom(page)

        count = page.evaluate(
            """() => {
                const data = { run_id: 'dedup-agent-001', summary: 'Done', status: 'completed' };

                App._testDeliverAgentCompleted(data);
                App._testDeliverAgentCompleted(data);

                return document.querySelectorAll('.completion-toast').length;
            }"""
        )

        assert count == 1

    def test_dedup_clears_on_reconnect(self, authenticated_page) -> None:
        """After clearing the dedup set (simulating reconnect), the same ID renders again."""
        page = authenticated_page
        _setup_toast_dom(page)

        result = page.evaluate(
            """() => {
                const data = { task_id: 'reconnect-task', command: 'ls', status: 'completed', exit_code: 0 };

                // First delivery
                App._testDeliverTaskCompleted(data);
                const before = document.querySelectorAll('.completion-toast').length;

                // Remove existing toasts to isolate the count
                document.querySelectorAll('.completion-toast').forEach(t => t.remove());

                // Simulate reconnect clearing the dedup set
                App._testClearDeliveredIds();

                // Re-deliver same event — should render again after clear
                App._testDeliverTaskCompleted(data);
                const after = document.querySelectorAll('.completion-toast').length;

                return { before, after };
            }"""
        )

        assert result["before"] == 1
        assert result["after"] == 1
