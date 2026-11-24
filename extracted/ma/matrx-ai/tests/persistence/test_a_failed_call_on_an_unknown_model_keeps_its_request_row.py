"""A FAILED call on a model the catalog does not know still writes its request row.

system_error 814ab934 (2026-11-12): /ai/chat asked for the bare alias ``gpt-4.1-nano``; the
catalog refused it (CatalogRoutingError, d2645d63) and persist_completed_request then SKIPPED the
chat.request INSERT as ``cx_request_model_unresolvable`` — the failed run lost its only request
row. ``chat.request.ai_model_id`` is nullable since 20261024160000, so the failure is written:
ai_model_id NULL, status failed, the error, and ``metadata.requested_model`` naming what the caller
asked for. A COMPLETED cloud call with no resolvable model still files its skip (a catalog gap).
"""

from __future__ import annotations

from typing import Any

import pytest
from test_provider_id_never_message_pk import (  # noqa: F401
    CONVERSATION_ID,
    _build_tool_loop_completed,
    persist_harness,
)


class _NoModel:
    async def load_model_get_string_uuid(self, name):
        return None


@pytest.mark.asyncio
async def test_failed_unknown_model_call_writes_a_failed_row(persist_harness, monkeypatch) -> None:  # noqa: F811
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
        storage["conversation"]["ai_model"] = "gpt-4.1-nano"
        storage["user_request"]["status"] = "failed"
        storage["user_request"]["error"] = (
            '{"error_type":"matrx_catalog_error","message":"resolve_call_profile: unknown model"}'
        )
        storage["requests"] = storage["requests"][:1]
        for req in storage["requests"]:
            req["ai_model"] = None
            req["cost"] = None
        return storage

    monkeypatch.setattr(completed, "to_storage_dict", _storage)
    await persistence_mod.persist_completed_request(completed, conversation_id=CONVERSATION_ID)

    assert "cx_request_model_unresolvable" not in skipped, skipped
    assert rows, "the failed call's request row was dropped"
    for row in rows:
        data = row.get("data", row)
        assert data["ai_model_id"] is None
        assert data["status"] == "failed"
        assert data["error"]
        assert data["metadata"]["model_unresolved"] is True
        assert data["metadata"]["requested_model"] == "gpt-4.1-nano"
