"""Reasoning is neither visible reply text nor decision material (sweep after run 57db7ef9).

A ``thinking`` block keeps the model's reasoning under ``text``.
* A handoff hides the textless assistant rows of its turn from the person; a reasoning-plus-tool-call
  row counted as "has text" and stayed visible. Red when ``_hide_handoff_plumbing`` reads any ``text``.
* A decision call's state is built from earlier messages; earlier assistant reasoning entered it as
  conversation. Red when ``_text_of`` reads a thinking block's ``text``.
"""

from __future__ import annotations

from types import SimpleNamespace

from matrx_ai.config.unified_content import TextContent, ThinkingContent
from matrx_ai.decisions.translate import _message_text, _text_of
from matrx_ai.orchestrator.executor import _hide_handoff_plumbing


def _msg(role, *content):
    return SimpleNamespace(role=role, content=list(content), metadata={})


def test_a_reasoning_only_assistant_row_is_hidden_from_the_person():
    reasoning = _msg("assistant", ThinkingContent(text="private plan", provider="anthropic"))
    tool = _msg("tool")
    _hide_handoff_plumbing([reasoning, tool])
    assert reasoning.metadata["is_visible_to_user"] is False
    assert tool.metadata["is_visible_to_user"] is False


def test_the_preamble_with_reply_text_stays_visible():
    preamble = _msg("assistant", ThinkingContent(text="private plan", provider="anthropic"), TextContent(text="On it."))
    tool = _msg("tool")
    _hide_handoff_plumbing([preamble, tool])
    assert "is_visible_to_user" not in preamble.metadata


def test_a_decision_state_leaves_out_reasoning():
    message = _msg("assistant", ThinkingContent(text="private plan", provider="anthropic"), TextContent(text="Said."))
    assert _text_of(message.content[0]) == ""
    assert _message_text(message) == "Said."
