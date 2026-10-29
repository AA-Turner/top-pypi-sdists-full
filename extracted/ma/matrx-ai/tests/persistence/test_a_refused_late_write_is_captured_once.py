"""A late one-shot write the database refuses is captured ONCE, not twice.

Since matrx-orm a682d7ad a Session block that lost a write raises FlushError
after its own flush already preserved the op in system_write_failure. The
Coordinator's late one-shot path used to capture it again — a second
replayable row for the same op — and log "FAILED outside Session".
"""

from __future__ import annotations

import asyncio
import contextlib

import pytest

from matrx_ai.persistence.coordinator import Coordinator
from matrx_ai.persistence.registry import register_table


class _Meta:
    primary_keys = ["id"]
    foreign_keys: dict = {}
    table_name = "cx_refused_late"
    db_schema = "public"


class _Model:
    _meta = _Meta()

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


register_table("public.cx_refused_late", _Model)


class _CheckViolation(Exception):
    pass


@contextlib.asynccontextmanager
async def _fake_transaction(*args, **kwargs):
    yield


@pytest.mark.asyncio
async def test_a_refused_late_one_shot_reaches_system_write_failure_exactly_once(
    monkeypatch, capture_sink
):
    import matrx_orm.core.transaction as txn_mod

    monkeypatch.setattr(txn_mod, "transaction", _fake_transaction)
    monkeypatch.setattr(
        "matrx_connect.streaming.error_capture.capture_error",
        lambda *a, **k: asyncio.sleep(0),
    )
    coord = Coordinator(request_id="r-refused", conversation_id="c-refused")
    await coord.flush(reason="stream_end")  # sealed: later writes one-shot

    async def refuse(tiers):
        raise _CheckViolation('violates check constraint "cx_message_role_check"')

    monkeypatch.setattr("matrx_orm.session.flush.execute_tiers", refuse)
    monkeypatch.setattr("matrx_orm.session.session.execute_tiers", refuse)

    coord.queue("public.cx_refused_late", {"id": "m-late", "role": "system"})
    late = [t for t in coord._late_one_shots if not t.done()]
    assert late, "the late write was not scheduled as a one-shot"
    await asyncio.wait(set(late), timeout=5.0)

    failures, _ = capture_sink
    captured = [op.pk_value for f in failures for op in f["ops"]]
    assert captured == ["m-late"], f"captured {len(captured)} time(s): {captured}"
