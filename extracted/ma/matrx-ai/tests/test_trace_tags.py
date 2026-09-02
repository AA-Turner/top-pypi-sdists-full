"""Ambient trace tags — a scope labels every `chat.tool_trace` row it produces.

Why this exists: a Hindsight replay executes REAL tool calls, and its dispatches
land in the same durable audit channel as a user's own. Without a label, "what
did this replay actually DO?" cannot be answered from the DB, which is the
evidence a replay verdict has to be trusted against.

The tool layer must never learn what a replay is — it carries whatever label the
scope declared, on the context, under one reserved key.
"""

from __future__ import annotations

import pytest


@pytest.fixture
def _queued(monkeypatch):
    from matrx_ai.persistence import queue_helpers as qh
    from matrx_ai.tools import _db_log

    rows: list[dict] = []
    monkeypatch.setattr(qh, "get_coordinator", lambda: object())
    monkeypatch.setattr(qh, "queue_tool_trace_create", lambda **row: rows.append(row))
    # Both sinks are stage-disabled under pytest so deliberate failure fixtures
    # never pollute the real table — re-enable for these assertions.
    monkeypatch.setattr(_db_log, "sinks_disabled_by_stage", lambda: False)
    return rows


def _install_context(metadata: dict | None):
    from matrx_connect.context.app_context import AppContext, set_app_context
    from matrx_connect.emitters.console_emitter import ConsoleEmitter

    ctx = AppContext(
        emitter=ConsoleEmitter("test", accumulate=False),
        user_id="u1",
        auth_type="token",
        is_authenticated=True,
        request_id="r1",
        store=True,
        metadata=metadata or {},
    )
    return set_app_context(ctx)


def _dispatch(**kwargs):
    from matrx_ai.tools._db_log import _queue_db_log_event

    _queue_db_log_event(
        "OK", tool_name="probe_tool", conversation_id="conv-1", call_id="c1", **kwargs
    )


def test_ambient_tags_land_on_the_trace_row(_queued):
    from matrx_connect.context.app_context import clear_app_context

    from matrx_ai.tools import TRACE_TAGS_CONTEXT_KEY

    token = _install_context(
        {TRACE_TAGS_CONTEXT_KEY: {"kind": "hindsight_replay", "database": "mirror"}}
    )
    try:
        _dispatch()
    finally:
        clear_app_context(token)

    assert len(_queued) == 1
    assert _queued[0]["metadata"][TRACE_TAGS_CONTEXT_KEY] == {
        "kind": "hindsight_replay",
        "database": "mirror",
    }


def test_tags_never_displace_the_rows_own_metadata(_queued):
    """A traceback (the FAIL path's payload) must survive a tagged scope."""
    from matrx_connect.context.app_context import clear_app_context

    from matrx_ai.tools import TRACE_TAGS_CONTEXT_KEY

    token = _install_context({TRACE_TAGS_CONTEXT_KEY: {"kind": "hindsight_replay"}})
    try:
        _dispatch(metadata={"traceback": "Traceback (most recent call last): ..."})
    finally:
        clear_app_context(token)

    meta = _queued[0]["metadata"]
    assert meta["traceback"].startswith("Traceback")
    assert meta[TRACE_TAGS_CONTEXT_KEY] == {"kind": "hindsight_replay"}


def test_an_untagged_scope_adds_nothing(_queued):
    """The default path must be byte-identical to before — no empty key."""
    from matrx_connect.context.app_context import clear_app_context

    from matrx_ai.tools import TRACE_TAGS_CONTEXT_KEY

    token = _install_context(None)
    try:
        _dispatch()
    finally:
        clear_app_context(token)

    assert TRACE_TAGS_CONTEXT_KEY not in _queued[0]["metadata"]
