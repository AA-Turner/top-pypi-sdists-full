"""The xAI request snapshot keeps the messages, so the system text is auditable.

Adversarial M7 (2026-10-18): xAI snapshots held only ``message_count``, so the cache-law
audits and the judge's fed check could not read what xAI was sent."""

from __future__ import annotations

import json

from xai_sdk.proto import chat_pb2

from matrx_ai.providers.xai.translator import XAITranslator


def _msg(role: int, text: str) -> chat_pb2.Message:
    return chat_pb2.Message(role=role, content=[chat_pb2.Content(text=text)])


def test_debug_summary_carries_the_system_and_user_text() -> None:
    kwargs = {
        "model": "grok-4",
        "messages": [
            _msg(chat_pb2.ROLE_SYSTEM, "SYSTEM-TEXT-M7"),
            _msg(chat_pb2.ROLE_USER, "USER-TEXT-M7"),
        ],
    }
    summary = XAITranslator.debug_summary(kwargs)
    blob = json.dumps(summary)
    assert "SYSTEM-TEXT-M7" in blob and "USER-TEXT-M7" in blob
    assert summary["message_count"] == 2
