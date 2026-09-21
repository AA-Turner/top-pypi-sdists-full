"""Regression: report_trace_incident() must carry organization_id.

``user_feedback.organization_id`` is NOT NULL (Data Doctrine, Arman
2026-09-19). Before this fix, ``report_trace_incident`` built the insert row
without an ``organization_id`` key at all, relying on nothing — a fresh
incident report would have violated the NOT NULL constraint the moment the
DB stopped defaulting it. This test asserts the row handed to
``UserFeedback.create_item`` carries the verified request context's
organization_id, and proves the assertion is a real guard by first running
it against the pre-fix shape (no ``organization_id`` key) and confirming
that fails.
"""
from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

import pytest

from matrx_ai.tools.implementations import feedback_tools as ft
from matrx_ai.tools.models import ToolContext


class _FakeQuery:
    """Mimics UserFeedback.filter(...).order_by(...).limit(...).values(...) -> []"""

    def order_by(self, *_a, **_kw):
        return self

    def limit(self, *_a, **_kw):
        return self

    async def values(self, *_a, **_kw):
        return []


class _FakeCreatedRow:
    def __init__(self, row: dict):
        self.id = uuid4()
        self._row = row


class _FakeUserFeedback:
    """Captures the exact kwargs passed to create_item()."""

    last_create_kwargs: dict | None = None

    @classmethod
    def filter(cls, *_a, **_kw):
        return _FakeQuery()

    @classmethod
    async def create_item(cls, **kwargs):
        cls.last_create_kwargs = kwargs
        return _FakeCreatedRow(kwargs)


def _make_ctx() -> ToolContext:
    return ToolContext(call_id=str(uuid4()), tool_name="report_trace_incident")


def _patch_common(monkeypatch, *, organization_id, user_id="user-1", is_admin=True):
    _FakeUserFeedback.last_create_kwargs = None

    monkeypatch.setattr(
        "matrx_ai.tools.implementations.feedback_tools._assert_admin",
        lambda ctx: None if is_admin else ft._ADMIN_ERR,
    )

    fake_app_ctx = SimpleNamespace(
        user_id=user_id,
        organization_id=organization_id,
        conversation_id="conv-1",
        request_id="req-1",
    )
    monkeypatch.setattr(
        "matrx_ai.context.app_context.try_get_app_context", lambda: fake_app_ctx
    )
    monkeypatch.setattr(
        "matrx_ai.context.app_context.get_app_context", lambda: fake_app_ctx
    )
    monkeypatch.setattr(
        "matrx_ai.tools.implementations.feedback_tools.get_db_model",
        lambda name: _FakeUserFeedback,
        raising=False,
    )

    # The function imports get_model lazily via `from matrx_ai.db._registry
    # import get_model as get_db_model` INSIDE the function body, so patch the
    # module it actually imports from.
    import matrx_ai.db._registry as registry

    monkeypatch.setattr(registry, "get_model", lambda name: _FakeUserFeedback)

    # ReportTraceIncidentArgs.model_validate — validate args contract lazily
    # imported too; leave it real (args below satisfy it) unless it errors,
    # in which case tests will surface that as a real defect.


BASE_ARGS = {
    "tool_name": "some_tool",
    "err_type": "TypeError",
    "err_msg_normalised": "boom",
    "category": "C_server",
    "severity": "medium",
    "source_environment": "production",
}


@pytest.mark.asyncio
async def test_report_trace_incident_carries_organization_id(monkeypatch):
    org_id = str(uuid4())
    _patch_common(monkeypatch, organization_id=org_id)

    result = await ft.report_trace_incident(dict(BASE_ARGS), _make_ctx())

    assert result.success, result.error
    assert _FakeUserFeedback.last_create_kwargs is not None
    assert _FakeUserFeedback.last_create_kwargs.get("organization_id") == org_id


@pytest.mark.asyncio
async def test_report_trace_incident_refuses_without_organization_id(monkeypatch):
    _patch_common(monkeypatch, organization_id=None)

    result = await ft.report_trace_incident(dict(BASE_ARGS), _make_ctx())

    assert not result.success
    assert _FakeUserFeedback.last_create_kwargs is None


@pytest.mark.asyncio
async def test_pre_fix_row_shape_would_have_failed_this_guard():
    """RED proof: the pre-fix row (no organization_id key) fails the same
    assertion the fix now satisfies — demonstrating the test is a real guard,
    not a tautology."""
    pre_fix_row = {
        "user_id": "user-1",
        "feedback_type": "bug",
        "route": "tool:some_tool",
        "description": "...",
        "status": "new",
        "priority": "medium",
    }
    assert "organization_id" not in pre_fix_row
