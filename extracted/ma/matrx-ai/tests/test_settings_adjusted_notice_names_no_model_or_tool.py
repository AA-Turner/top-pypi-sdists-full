"""The settings_adjusted notice never names a model or a tool (feedback d94804c3)."""

from __future__ import annotations

from typing import Any

from matrx_ai.catalog.models import Adjustment
from matrx_ai.providers import outbound_params


def _adj() -> list[Adjustment]:
    return [
        Adjustment(
            key="top_k",
            action="dropped",
            canonical_value=5,
            sent_value=None,
            reason="not supported",
            expected=False,
        )
    ]


def test_notice_text_names_neither_model_nor_tool(monkeypatch) -> None:
    shown: list[Any] = []
    monkeypatch.setattr(outbound_params, "send_client_info", lambda p, **kw: shown.append(p))
    outbound_params.publish_settings_adjustments(_adj(), model="claude-sonnet-5-5", seam="chat")
    for p in shown:
        assert "claude-sonnet-5-5" not in p.user_message


def test_tool_seam_text_names_no_tool(monkeypatch) -> None:
    shown: list[Any] = []
    monkeypatch.setattr(outbound_params, "send_client_info", lambda p, **kw: shown.append(p))
    outbound_params.publish_settings_adjustments(
        _adj(), model="tool ask_person", seam="tool_schema", announce=True
    )
    assert shown and all("ask_person" not in p.user_message for p in shown)
