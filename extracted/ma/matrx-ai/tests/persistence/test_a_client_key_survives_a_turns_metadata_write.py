"""A client's conversation-metadata key written mid-turn survives the turn (CGU-M3 W4, lead's ruling 2026-11-04).

The server patched a conversation's metadata by laying its keys over a copy read earlier in the turn and writing
the WHOLE object back, so a key a client wrote in between (W2's dismissed proposals, a run setting) vanished
when the turn's write landed; W2 worked around it by re-writing 5 s after every first turn. A row on disk is now
patched by key at write time: whatever the queued value is, applying it to what is stored NOW keeps the
client's key.
"""

from __future__ import annotations

from typing import Any

import pytest

import matrx_ai.persistence.queue_helpers as qh

CONV = "6b7d1d36-6d0b-4c6e-9a5e-2f4c8f0d1a11"


@pytest.fixture
def queued(monkeypatch) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    monkeypatch.setattr(qh, "queue_conversation_update", lambda id, **fields: out.append(fields) or id)
    monkeypatch.setattr(qh, "conversation_insert_is_queued", lambda cid: False)
    monkeypatch.setattr(qh, "_pending_conversation_metadata", lambda cid: None)
    return out


def _written(value: Any, stored_now: dict[str, Any]) -> dict[str, Any]:
    """What the row holds after the queued value lands on ``stored_now``."""
    from matrx_orm import JsonbPatch

    return value.apply(stored_now) if isinstance(value, JsonbPatch) else dict(value)


def test_a_client_key_written_after_the_turns_read_survives(queued):
    read_at_turn_start = {"run_configuration": {"tools": ["web"]}}
    # The client writes its key while the turn runs.
    stored_now = {**read_at_turn_start, "dismissed_proposals": {"p-9": "2026-11-04T08:18:22Z"}}

    qh.queue_conversation_metadata_patch(
        CONV, {"last_request_context": {"organization_id": "o-1"}}, db_metadata=read_at_turn_start
    )

    (fields,) = queued
    after = _written(fields["metadata"], stored_now)
    assert after["dismissed_proposals"] == {"p-9": "2026-11-04T08:18:22Z"}, (
        "the turn's metadata write dropped a key the client wrote mid-turn"
    )
    assert after["last_request_context"] == {"organization_id": "o-1"}
    assert after["run_configuration"] == {"tools": ["web"]}


def test_a_nested_key_still_merges_one_level_down(queued):
    stored_now = {"run_configuration": {"tools": ["web"], "outputKinds": ["table"]}}
    qh.queue_conversation_metadata_patch(CONV, {"run_configuration": {"removed_tools": ["memory"]}}, db_metadata={})
    (fields,) = queued
    assert _written(fields["metadata"], stored_now)["run_configuration"] == {
        "tools": ["web"],
        "outputKinds": ["table"],
        "removed_tools": ["memory"],
    }
