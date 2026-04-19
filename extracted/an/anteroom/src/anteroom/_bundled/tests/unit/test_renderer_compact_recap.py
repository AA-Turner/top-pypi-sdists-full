"""Renderer tests for the compacted conversation shape (#1413).

Verifies that ``render_conversation_recap()`` skips the system-role
compact summary and system-role boundary marker, showing only the real
last user/assistant exchange from the preserved tail.
"""

from __future__ import annotations

from io import StringIO

from rich.console import Console


def _capture_recap(messages: list[dict]) -> str:
    """Capture output from both consoles used by ``render_conversation_recap``.

    The recap routes the "You:" line through ``renderer.console`` and the
    assistant markdown through ``renderer._stdout_console`` (Padding support).
    We patch both and return the merged output.
    """
    from anteroom.cli import renderer

    buf = StringIO()
    test_console = Console(file=buf, width=120, force_terminal=False, no_color=True)
    original = renderer.console
    original_stdout = renderer._stdout_console
    renderer.console = test_console
    renderer._stdout_console = test_console
    try:
        renderer.render_conversation_recap(messages)
    finally:
        renderer.console = original
        renderer._stdout_console = original_stdout
    return buf.getvalue()


class TestRecapSkipsCompactedSummary:
    def test_skips_system_compact_summary(self) -> None:
        """Recap does not show the system-role compact summary."""
        msgs = [
            {"role": "system", "content": "[Previous conversation summary] Older history..."},
            {"role": "system", "content": "[Context compacted...]"},  # boundary
            {"role": "user", "content": "real user message"},
            {"role": "assistant", "content": "real assistant reply"},
        ]
        out = _capture_recap(msgs)
        assert "real user message" in out
        assert "real assistant reply" in out
        assert "Older history" not in out
        assert "[Context compacted" not in out

    def test_finds_real_last_user_after_compact(self) -> None:
        """The 'You:' line shows the actual last user message, not the summary."""
        msgs = [
            {"role": "system", "content": "SUMMARY_CONTENT_DO_NOT_SHOW"},
            {"role": "system", "content": "[Context compacted...]"},
            {"role": "user", "content": "TAIL_USER_MESSAGE"},
            {"role": "assistant", "content": "TAIL_ASSISTANT_REPLY"},
        ]
        out = _capture_recap(msgs)
        assert "TAIL_USER_MESSAGE" in out
        assert "SUMMARY_CONTENT_DO_NOT_SHOW" not in out

    def test_empty_tail_produces_no_output(self) -> None:
        """Conversation with only system messages (no tail) renders nothing."""
        msgs = [
            {"role": "system", "content": "summary"},
            {"role": "system", "content": "boundary"},
        ]
        out = _capture_recap(msgs)
        assert out == ""

    def test_no_compact_shape_still_works(self) -> None:
        """Regular (non-compacted) conversations render normally."""
        msgs = [
            {"role": "user", "content": "hello"},
            {"role": "assistant", "content": "hi"},
        ]
        out = _capture_recap(msgs)
        assert "hello" in out
        assert "hi" in out
