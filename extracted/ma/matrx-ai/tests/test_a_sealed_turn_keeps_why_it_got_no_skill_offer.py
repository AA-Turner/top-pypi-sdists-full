"""A confidential (sealed) turn's request row keeps the platform's reason it got no skill offer (and its chat mode),
and never the offered list's text. chat-agent-skills finding 8: the refusal was recorded but the sealed row's
keep-spec dropped it, so an admin saw nothing."""

from __future__ import annotations

from matrx_ai.persistence.sealed import keep_by_spec, sealed_metadata_spec


def test_the_refusal_reason_survives_sealing_and_the_offered_text_does_not():
    meta = {
        "skill_offer": {"state": "not_started", "reason": "confidential turn", "text": "the person's words", "listed": True},
        "chat_mode": {"mode": None, "reason": "not a chat interface", "provider": None, "core_block": True, "small_model": False},
    }
    kept = keep_by_spec(meta, sealed_metadata_spec("chat.user_request"))
    assert kept["skill_offer"] == {"state": "not_started", "reason": "confidential turn"}
    assert kept["chat_mode"]["reason"] == "not a chat interface"
