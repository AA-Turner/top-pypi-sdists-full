import json

from abstra_internals.entities.agents.action_tracker import ActionTracker


class TestActionTracker:
    def test_initial_state(self):
        tracker = ActionTracker()
        assert len(tracker.action_history) == 0
        assert tracker.consecutive_repeats == 0
        assert tracker.last_action_sig is None

    def test_record_action(self):
        tracker = ActionTracker()
        tracker.record_action("click", "5", "Clicked element 5")
        assert len(tracker.action_history) == 1
        assert tracker.action_history[0]["action"] == "click"

    def test_consecutive_repeats(self):
        tracker = ActionTracker()
        tracker.record_action("click", "5", "ok")
        assert tracker.consecutive_repeats == 1
        tracker.record_action("click", "5", "ok")
        assert tracker.consecutive_repeats == 2
        tracker.record_action("click", "5", "ok")
        assert tracker.consecutive_repeats == 3

    def test_consecutive_repeats_reset(self):
        tracker = ActionTracker()
        tracker.record_action("click", "5", "ok")
        tracker.record_action("click", "5", "ok")
        tracker.record_action("navigate", "url", "ok")
        assert tracker.consecutive_repeats == 1

    def test_window_size(self):
        tracker = ActionTracker(window_size=5)
        for i in range(10):
            tracker.record_action("click", str(i), "ok")
        assert len(tracker.action_history) == 5


class TestDetectLoop:
    def test_no_loop_with_few_actions(self):
        tracker = ActionTracker()
        tracker.record_action("click", "5", "ok")
        is_loop, reason = tracker.detect_loop()
        assert not is_loop

    def test_consecutive_repeat_loop(self):
        tracker = ActionTracker()
        tracker.record_action("click", "5", "ok")
        tracker.record_action("click", "5", "ok")
        tracker.record_action("click", "5", "ok")
        is_loop, reason = tracker.detect_loop()
        assert is_loop
        assert "repeated" in reason.lower()

    def test_cyclic_pattern_loop(self):
        tracker = ActionTracker()
        for _ in range(3):
            tracker.record_action("click", "5", "ok")
            tracker.record_action("navigate", "url", "ok")
        is_loop, reason = tracker.detect_loop()
        assert is_loop
        assert "cyclic" in reason.lower() or "Cyclic" in reason

    def test_repeated_wait_for_download_loop(self):
        tracker = ActionTracker()
        for _ in range(3):
            tracker.record_action("wait_for_download", "{}", "no download")
        tracker.record_action("wait_for_download", "{}", "no download")
        is_loop, reason = tracker.detect_loop()
        assert is_loop

    def test_repeated_request_url_loop(self):
        tracker = ActionTracker()
        url_input = json.dumps({"url": "https://api.example.com/data"})
        for _ in range(3):
            tracker.record_action("make_request", url_input, "ok")
        is_loop, reason = tracker.detect_loop()
        assert is_loop
        assert "api.example.com" in reason

    def test_consecutive_failures_loop(self):
        tracker = ActionTracker()
        tracker.record_action("click", "1", "Error: element not found")
        tracker.record_action("click", "2", "Failed to click")
        tracker.record_action("click", "3", "Error: timeout")
        is_loop, reason = tracker.detect_loop()
        assert is_loop
        assert "failed" in reason.lower()

    def test_no_loop_with_mixed_successes(self):
        tracker = ActionTracker()
        tracker.record_action("click", "1", "ok")
        tracker.record_action("navigate", "url", "ok")
        tracker.record_action("type_text", "hello", "typed")
        is_loop, reason = tracker.detect_loop()
        assert not is_loop


class TestShouldTryDifferentAction:
    def test_no_suggestion_when_no_loop(self):
        tracker = ActionTracker()
        tracker.record_action("click", "5", "ok")
        should_change, suggestion = tracker.should_try_different_action()
        assert not should_change

    def test_suggestion_for_click_loop(self):
        tracker = ActionTracker()
        for _ in range(3):
            tracker.record_action("click", "5", "ok")
        should_change, suggestion = tracker.should_try_different_action()
        assert should_change
        assert "javascript" in suggestion.lower() or "JS" in suggestion

    def test_suggestion_for_navigate_loop(self):
        tracker = ActionTracker()
        for _ in range(3):
            tracker.record_action("navigate", "url", "ok")
        should_change, suggestion = tracker.should_try_different_action()
        assert should_change
        assert "re-navigating" in suggestion.lower() or "interact" in suggestion.lower()


class TestShouldForceWaitForDownload:
    def test_no_force_when_empty(self):
        tracker = ActionTracker()
        should_force, reason = tracker.should_force_wait_for_download()
        assert not should_force

    def test_force_after_download_click_without_wait(self):
        tracker = ActionTracker()
        tracker.record_action("click", "10", "clicked", element_text="Download Report")
        should_force, reason = tracker.should_force_wait_for_download()
        assert should_force
        assert "wait_for_download" in reason

    def test_no_force_after_regular_click(self):
        tracker = ActionTracker()
        tracker.record_action("click", "10", "clicked", element_text="Submit Form")
        should_force, reason = tracker.should_force_wait_for_download()
        assert not should_force


class TestGetContextForPrompt:
    def test_empty_context(self):
        tracker = ActionTracker()
        assert tracker.get_context_for_prompt() == ""

    def test_context_includes_action_history(self):
        tracker = ActionTracker()
        tracker.record_action("navigate", "https://example.com", "ok")
        tracker.record_action("click", "5", "clicked")
        context = tracker.get_context_for_prompt()
        assert "Action History" in context
        assert "navigate" in context
        assert "click" in context

    def test_context_includes_loop_warning(self):
        tracker = ActionTracker()
        for _ in range(3):
            tracker.record_action("click", "5", "ok")
        context = tracker.get_context_for_prompt()
        assert "LOOP DETECTED" in context

    def test_context_includes_repeat_warning(self):
        tracker = ActionTracker()
        tracker.record_action("click", "5", "ok")
        tracker.record_action("click", "5", "ok")
        context = tracker.get_context_for_prompt()
        assert "WARNING" in context
        assert "repeated" in context.lower()

    def test_context_includes_failed_actions(self):
        tracker = ActionTracker()
        tracker.record_action("click", "5", "Error: not found")
        tracker.record_action("click", "6", "Error: timeout")
        tracker.record_action("click", "7", "Error: blocked")
        context = tracker.get_context_for_prompt()
        assert "FAILED ACTIONS" in context

    def test_context_includes_repeated_urls(self):
        tracker = ActionTracker()
        url_input = json.dumps({"url": "https://api.example.com/data"})
        tracker.record_action("make_request", url_input, "ok")
        tracker.record_action("make_request", url_input, "ok")
        context = tracker.get_context_for_prompt()
        assert "REPEATED REQUEST URLs" in context
        assert "api.example.com" in context
