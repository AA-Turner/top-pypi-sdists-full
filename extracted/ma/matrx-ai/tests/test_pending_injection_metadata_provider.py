"""A host can stamp every new inbox row's metadata (aidream: the requester's test stamp); the row's own keys win."""
from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.db import _cx_managers_impl as impl


@pytest.mark.asyncio
async def test_provider_is_merged_under_the_rows_own_metadata(monkeypatch: pytest.MonkeyPatch) -> None:
    seen: dict[str, Any] = {}

    async def _create_item(self: Any, **kw: Any) -> Any:
        seen.update(kw)
        return SimpleNamespace(**kw)

    monkeypatch.setattr(impl.CxPendingInjectionManager, "create_item", _create_item)
    kw = dict(injection_id="i", conversation_id="c", created_by="u", kind="system_message", content={"text": "x"},
              source="deferred_tool", is_visible_to_user=False, is_visible_to_model=True, organization_id="o")
    mgr = impl.CxPendingInjectionManager()
    impl.set_pending_injection_metadata_provider(lambda: {"test_run_id": "R", "a": 0})
    try:
        await mgr.enqueue(**kw, metadata={"a": 1})
        assert seen["metadata"] == {"test_run_id": "R", "a": 1}
    finally:
        impl.set_pending_injection_metadata_provider(None)
    await mgr.enqueue(**kw, metadata={"a": 1})
    assert seen["metadata"] == {"a": 1}
