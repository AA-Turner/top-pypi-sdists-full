"""Regression test for role-gated fence swaps in build_wire_config (2026-07-02).

Pins the echo-bypass defect: the wire-swap substitution used to be role-blind —
when the same reference fence appeared in BOTH a user/system text (where it is
legitimately staged) and an assistant echo, the global substring replace
expanded the full referenced value into the assistant turn on every send,
re-inflating exactly the content pass-by-reference exists to keep out.

Fence-shaped swap keys (```matrx prefix) must apply to system/user/tool text
only; server-minted picklist tokens keep swapping everywhere.
"""
from __future__ import annotations

from matrx_ai.config.picklist_runtime import build_wire_config, set_wire_swaps
from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.config.unified_content import TextContent

FENCE = '```matrx\n{"matrx_version": 1, "kind": "reference", "type": "conversation_value", "items": [{"key": "big-doc"}]}\n```'


def _msg(role: str, text: str) -> UnifiedMessage:
    return UnifiedMessage(role=role, content=[TextContent(text=text)])


def _texts(config) -> list[tuple[str, str]]:
    out = []
    for m in config.messages:
        role = getattr(m.role, "value", m.role)
        out.append((str(role), m.content[0].text))
    return out


def test_fence_swap_skips_assistant_echo_but_applies_elsewhere():
    set_wire_swaps({FENCE: "THE-FULL-2MB-VALUE"})
    try:
        cfg = UnifiedConfig(
            model="test-model",
            messages=[
                _msg("user", f"please use {FENCE} for the synthesis"),
                _msg("assistant", f"I will pass {FENCE} to the tool now"),
            ],
        )
        wire = build_wire_config(cfg)
        assert wire is not None
        texts = dict(_texts(wire))
        assert "THE-FULL-2MB-VALUE" in texts["user"]
        assert FENCE not in texts["user"]
        # The assistant echo is NEVER expanded — the fence stays verbatim.
        assert texts["assistant"] == f"I will pass {FENCE} to the tool now"
    finally:
        set_wire_swaps({})


def test_picklist_tokens_still_swap_in_assistant_text():
    token = "⁣matrx:picklist:abc⁣"
    set_wire_swaps({token: "the real description"})
    try:
        cfg = UnifiedConfig(
            model="test-model",
            messages=[_msg("assistant", f"context: {token}")],
        )
        wire = build_wire_config(cfg)
        assert wire is not None
        assert wire.messages[0].content[0].text == "context: the real description"
    finally:
        set_wire_swaps({})
