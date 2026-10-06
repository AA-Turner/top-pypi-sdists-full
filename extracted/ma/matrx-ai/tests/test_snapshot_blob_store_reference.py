"""Forcing-function: every replaced inline blob stays recoverable (Arman,
2026-10-05: large files are stored by file reference).

An unreferenced 200 KB base64 PDF in the request must be saved through the host
blob store ONCE, the marker must carry the returned file_id, and the stored bytes
must hash to the sha the marker records. A failing store never perturbs the write.
"""

from __future__ import annotations

import base64
import hashlib
import re
from types import SimpleNamespace
from typing import Any
from uuid import uuid4

import pytest

from matrx_ai.orchestrator import executor as executor_mod
from matrx_ai.orchestrator.execution_state import ExecutionState
from matrx_ai.providers import snapshot_redactors as mod
from matrx_ai.providers.snapshot_redactors import MARKER_OPEN

PDF_BYTES = b"%PDF-1.7\n" + bytes(range(256)) * 800  # ~205 KB
PDF_B64 = base64.b64encode(PDF_BYTES).decode("ascii")


class _Store:
    def __init__(self, fail: bool = False) -> None:
        self.saved: dict[str, tuple[bytes, str, dict[str, Any]]] = {}
        self.calls = 0
        self.fail = fail

    async def __call__(self, raw: bytes, mime: str, sha256: str, **kw: Any) -> str:
        self.calls += 1
        if self.fail:
            raise RuntimeError("storage down")
        file_id = f"file-{len(self.saved) + 1}"
        self.saved[file_id] = (raw, mime, kw)
        return file_id


@pytest.fixture(autouse=True)
def _unbind():
    yield
    mod.configure_snapshot_blob_store(None)


async def _write(monkeypatch, request_payload=None, unified_payload=None) -> dict[str, Any]:
    queued: list[dict[str, Any]] = []
    monkeypatch.setattr("matrx_ai.persistence.queue_helpers.get_coordinator", lambda: object())
    monkeypatch.setattr(
        "matrx_ai.persistence.queue_helpers.queue_request_snapshot_create",
        lambda **kwargs: queued.append(kwargs) or "op",
    )
    exec_ctx = SimpleNamespace(
        store=True, conversation_id=str(uuid4()), request_id=str(uuid4()),
        user_id="user-1", organization_id="org-1",
    )
    await executor_mod._write_request_snapshot(
        exec_ctx=exec_ctx, iteration=1, api_response=None,
        request_payload=request_payload or {"messages": []}, unified_payload=unified_payload,
        trigger_position=0, first_assistant_position=1,
        state_snapshot=ExecutionState().snapshot(), provider="google", model="m",
        error_payload={"e": 1},
    )
    assert len(queued) == 1
    return queued[0]


@pytest.mark.asyncio
async def test_unreferenced_pdf_is_stored_and_marker_carries_file_id(monkeypatch) -> None:
    store = _Store()
    mod.configure_snapshot_blob_store(store)
    req = {"contents": [{"parts": [{"inline_data": {"mime_type": "application/pdf", "data": PDF_B64}}]}]}
    out = await _write(monkeypatch, request_payload=req)
    marker = out["request_payload"]["contents"][0]["parts"][0]["inline_data"]["data"]
    assert MARKER_OPEN in marker and len(marker) < 2000
    file_id = re.search(r'ref_file_id="([^"]+)"', marker).group(1)
    raw, mime, kw = store.saved[file_id]
    assert raw == PDF_BYTES and mime == "application/pdf"
    assert hashlib.sha256(raw).hexdigest() in marker
    assert kw == {"user_id": "user-1", "organization_id": "org-1"}


@pytest.mark.asyncio
async def test_same_bytes_in_request_and_unified_are_saved_once_per_tree_and_deduped(monkeypatch) -> None:
    store = _Store()
    mod.configure_snapshot_blob_store(store)
    two = {"a": {"data": PDF_B64}, "b": {"data": PDF_B64}}
    redactors = await mod.redactors_with_stored_blobs(two, user_id="u", organization_id="o")
    assert store.calls == 1
    out = mod.apply_redactors(two, redactors)
    assert 'ref_file_id="file-1"' in out["a"]["data"] and 'ref_file_id="file-1"' in out["b"]["data"]


@pytest.mark.asyncio
async def test_a_block_that_already_names_its_file_is_not_uploaded(monkeypatch) -> None:
    store = _Store()
    mod.configure_snapshot_blob_store(store)
    uni = {"messages": [{"content": [{"type": "document", "base64_data": PDF_B64, "file_id": "existing-id"}]}]}
    out = await _write(monkeypatch, unified_payload=uni)
    assert store.calls == 0
    assert 'ref_file_id="existing-id"' in out["unified_payload"]["messages"][0]["content"][0]["base64_data"]


@pytest.mark.asyncio
async def test_a_failing_store_keeps_the_sha_marker_and_is_reported(monkeypatch) -> None:
    mod.configure_snapshot_blob_store(_Store(fail=True))
    reported: list[Any] = []

    async def _on_error(exc, ctx):
        reported.append((exc, ctx))

    redactors = await mod.redactors_with_stored_blobs({"data": PDF_B64}, on_error=_on_error)
    out = mod.apply_redactors({"data": PDF_B64}, redactors)
    assert 'reference="none_sha256_only"' in out["data"] and "original_sha256" in out["data"]
    assert len(reported) == 1

    # and through the real writer: the snapshot is still queued
    out = await _write(monkeypatch, request_payload={"data": PDF_B64})
    assert MARKER_OPEN in out["request_payload"]["data"]


@pytest.mark.asyncio
async def test_text_is_never_uploaded_or_cut(monkeypatch) -> None:
    store = _Store()
    mod.configure_snapshot_blob_store(store)
    text = "word " * 60_000
    out = await _write(monkeypatch, request_payload={"contents": [{"parts": [{"text": text}]}]})
    assert store.calls == 0
    assert out["request_payload"]["contents"][0]["parts"][0]["text"] == text
