"""Turn-1 storage trusts the server's own loader flag, not client-sendable fields.

Adversarial M6 (2026-10-18): ``first_new_input_position`` treated any message carrying
``id`` + ``position`` as DB-loaded, and ``UnifiedMessage.from_dict`` reads both from client
JSON. A client carrying stored-looking messages into a NEW conversation would have had only
its trigger stored, losing the authored block."""

from __future__ import annotations

from types import SimpleNamespace

from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.orchestrator import executor as executor_mod


def _client_wire() -> list[UnifiedMessage]:
    return [
        UnifiedMessage.from_dict({"role": "user", "content": "q", "id": "m1", "position": 0}),
        UnifiedMessage.from_dict({"role": "assistant", "content": "a", "id": "m2", "position": 1}),
        UnifiedMessage.from_dict({"role": "user", "content": "new"}),
    ]


def test_client_json_with_id_and_position_is_not_stored_history() -> None:
    assert executor_mod.first_new_input_position(_client_wire(), 2) == 0


def test_client_json_cannot_claim_the_server_flag() -> None:
    wire = UnifiedMessage.from_dict(
        {"role": "user", "content": "q", "id": "m1", "position": 0, "from_store": True}
    )
    assert wire.from_store is False


def test_a_message_read_back_from_storage_makes_the_turn_a_continuation() -> None:
    row = SimpleNamespace(
        id="m1", role="user", content=[{"type": "text", "text": "q"}], created_at=None,
        status="active", metadata={}, user_content=None, position=0, agent_id=None,
    )
    stored = UnifiedMessage.from_cx_message(row)
    assert stored.from_store is True
    msgs = [stored, UnifiedMessage.from_dict({"role": "user", "content": "new"})]
    assert executor_mod.first_new_input_position(msgs, 1) == 1
