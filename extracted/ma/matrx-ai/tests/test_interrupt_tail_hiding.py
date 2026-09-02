"""INTERRUPT tail-hiding — the three-send-modes ruling (stop-and-fork).

Pins the executor helper that hides everything produced after the last clean
boundary when a ``mode=interrupt`` cancel fires: assistant/tool messages get
``is_visible_to_user=False`` + ``is_visible_to_model=False`` (metadata keys —
lifted into cx_message columns by the persist layer — AND the in-memory
attribute for the MessageList.sanitize backstop), while USER-role messages
(steered inbox deliveries) stay visible. Costs are untouched — nothing here
drops a message; hiding is the whole point.
"""

from matrx_ai.config import TextContent, UnifiedMessage
from matrx_ai.orchestrator.executor import _hide_interrupted_tail
from matrx_connect.request_controls import RequestControlRegistry


def _msg(role: str, text: str) -> UnifiedMessage:
    return UnifiedMessage(role=role, content=[TextContent(text=text)])


def test_hides_only_past_the_fence():
    messages = [_msg("user", "q"), _msg("assistant", "a1"), _msg("assistant", "a2")]
    hidden = _hide_interrupted_tail(messages, fence=2)
    assert hidden == 1
    # Pre-fence untouched.
    assert messages[1].metadata.get("is_visible_to_user") is None
    # Post-fence hidden both ways.
    assert messages[2].metadata["is_visible_to_user"] is False
    assert messages[2].metadata["is_visible_to_model"] is False
    assert messages[2].is_visible_to_model is False


def test_user_messages_in_tail_stay_visible():
    messages = [
        _msg("assistant", "pre"),
        _msg("assistant", "abandoned"),
        _msg("user", "steered mid-run"),
    ]
    hidden = _hide_interrupted_tail(messages, fence=1)
    assert hidden == 1
    assert messages[2].metadata.get("is_visible_to_user") is None


def test_empty_tail_is_a_noop():
    messages = [_msg("user", "q"), _msg("assistant", "a")]
    assert _hide_interrupted_tail(messages, fence=2) == 0
    assert _hide_interrupted_tail([], fence=0) == 0


def test_registry_interrupt_counts_as_cancel():
    import asyncio

    registry = RequestControlRegistry()
    asyncio.run(registry.interrupt("req-1"))
    assert registry.is_cancelled("req-1") is True
    assert registry.is_interrupted("req-1") is True
    assert registry.is_interrupted("req-2") is False
