"""A cx_user_request INSERT that failed is never remembered as ensured.

Live 2026-11-03 (write_failure 127702ef / fd3d2f78 / 1ce12194): refused
``rag.pdf_page_cleaner`` runs settled their row with an UPDATE that "matched no
row", and their cx_request child died on ``cx_request_user_request_id_fkey``.
The parent INSERT had failed and been swallowed (fire-and-forget), yet
``ensure_user_request_exists`` memoized the id as durably ensured anyway, so
``_request_rows_have_a_parent`` trusted the memo and queued writes against a row
that never existed. The memo may only say what actually landed.
"""

from contextlib import asynccontextmanager, contextmanager
from types import SimpleNamespace
from uuid import uuid4

import matrx_orm
import pytest

from matrx_ai.db import conversation_gate as gate


def _wire(monkeypatch):
    import matrx_ai.context.app_context as contexts

    ctx = SimpleNamespace(
        metadata={},
        user_id=str(uuid4()),
        source_app="aidream",
        source_feature="mandate:rag.pdf_page_cleaner",
        organization_id=str(uuid4()),
    )
    monkeypatch.setattr(contexts, "try_get_app_context", lambda: ctx)

    async def _not_a_store(*a, **k):
        return False

    async def _no_lineage(*a, **k):
        return None

    monkeypatch.setattr(gate, "_store_pending_user_request", _not_a_store)
    monkeypatch.setattr(gate, "_stamp_origin", lambda *a, **k: None)
    monkeypatch.setattr(gate, "_stamp_attribution", lambda *a, **k: None)
    monkeypatch.setattr(gate, "_stamp_agent_refs", lambda *a, **k: None)
    monkeypatch.setattr(gate, "_stamp_launch_binding", lambda *a, **k: None)
    monkeypatch.setattr(gate, "_stamp_lineage", _no_lineage)
    monkeypatch.setattr(gate, "_refuse_person_request_in_platform_tenant", lambda *a, **k: None)
    monkeypatch.setattr(gate, "try_get_tracker", lambda: None)
    monkeypatch.setattr(gate, "_get_active_lane_coordinator", lambda: None)
    monkeypatch.setattr(gate, "_require_persistence_actor", lambda user_id, _where: user_id)

    import matrx_ai.providers.usage_gate as usage_gate

    monkeypatch.setattr(usage_gate, "precheck_usage", lambda config=None: None)

    class Requests:
        model = object()

        async def filter_user_requests(self, **kwargs):
            return []  # the row never landed

        async def create_user_request(self, **kwargs):
            raise RuntimeError("insert refused (FK user_request_parent_request_id_fkey)")

    @asynccontextmanager
    async def session():
        yield

    @contextmanager
    def allow_direct(*args, **kwargs):
        yield

    monkeypatch.setattr(gate, "_cxm", lambda: SimpleNamespace(user_request=Requests()))
    monkeypatch.setattr(matrx_orm, "Session", session)
    monkeypatch.setattr(matrx_orm, "allow_direct_coordinator_write", allow_direct)
    return ctx


@pytest.mark.asyncio
async def test_a_swallowed_insert_failure_leaves_the_request_unrecorded(monkeypatch):
    ctx = _wire(monkeypatch)
    request_id = str(uuid4())

    await gate.ensure_user_request_exists(request_id, ctx.user_id)

    assert request_id not in gate._ensured_request_ids
    assert not gate.request_has_record(request_id)
    assert await gate._user_request_was_recorded(request_id) is False


@pytest.mark.asyncio
async def test_recording_a_refused_run_reports_a_failed_insert(monkeypatch):
    _wire(monkeypatch)
    request_id = str(uuid4())

    assert await gate.record_failed_user_request(request_id, "run_approval_required") is False
    assert request_id not in gate._ensured_request_ids
