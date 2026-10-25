"""A request a person's OWN model file served is written: ai_model_id NULL, served_via, cost 0.

There is no ai.model_definition for an own file, so the persist path used to SKIP the
chat.request INSERT ("ai_model_id unresolvable") and the run left no request row (L5 rerun
walk, 2026-10-24). chat.request.ai_model_id is nullable since 20261024160000; the row now
carries ai_model_id None, metadata.served_via (provider, app_instance_id, local_model_id,
model_key) and device_served, and cost 0.0. A cloud row with no resolvable model still files
its skip (tests/persistence/test_every_skipped_write_is_filed.py).
"""

from __future__ import annotations

from typing import Any

import pytest
from test_provider_id_never_message_pk import (  # noqa: F401
    CONVERSATION_ID,
    _build_tool_loop_completed,
    persist_harness,
)

SERVED_VIA = {
    "provider": "device",
    "app_instance_id": "6f1c2a7e-3b9d-4c1e-8f0a-2d4b6c8e0a13",
    "local_model_id": "9d2e4f60-1a3b-4c5d-8e7f-0a1b2c3d4e5f",
    "model_key": "own-my-finetune-1a2b3c4d",
    "model_name": "my-finetune",
}


class _NoModel:
    async def load_model_get_string_uuid(self, name):
        return None


@pytest.mark.asyncio
@pytest.mark.parametrize("device", [True, False])
async def test_an_own_file_request_row_is_written_with_no_model(persist_harness, monkeypatch, device) -> None:  # noqa: F811
    persistence_mod, _creates, _updates = persist_harness
    completed = _build_tool_loop_completed()
    rows: list[dict[str, Any]] = []
    skipped: list[str] = []
    monkeypatch.setattr(persistence_mod, "ai_model_manager_instance", _NoModel())
    monkeypatch.setattr(persistence_mod, "_queue_request_create", lambda **kw: rows.append(kw) or "")

    async def _skip(stage, detail, **kw):
        skipped.append(stage)

    monkeypatch.setattr(persistence_mod, "surface_skipped_write", _skip)
    original = completed.to_storage_dict

    def _storage() -> dict[str, Any]:
        storage = original()
        for req in storage["requests"]:
            req["ai_model"] = None
            req["cost"] = None
            if device:
                req.setdefault("metadata", {})["served_via"] = dict(SERVED_VIA)
        return storage

    monkeypatch.setattr(completed, "to_storage_dict", _storage)
    await persistence_mod.persist_completed_request(completed, conversation_id=CONVERSATION_ID)

    if device:
        assert rows, "the device-served request row was skipped"
        assert skipped == []
        for row in rows:
            data = row.get("data", row)
            assert data["ai_model_id"] is None
            assert data["cost"] == 0.0
            assert data["metadata"]["served_via"] == SERVED_VIA
            assert data["metadata"]["device_served"] is True
    else:
        assert rows == [] and skipped and set(skipped) == {"cx_request_model_unresolvable"}
