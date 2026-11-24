"""FORCING TEST — the title/label writer stamps the person, not the system principal.

2026-11-14: chat.conversation e6ecacaf-... was updated 09:29:17 (title set) with updated_by = system, AFTER the
funnel fix in queue_helpers. The label writer (and the tool ledger, and every standalone coordinator) calls
``Coordinator.queue`` directly, never ``queue_helpers._queue_or_drop``. The actor is therefore carried by the
Coordinator itself: its own ``user_id``, with no ambient request at all (the label task is detached).
"""

from __future__ import annotations

import pytest

PERSON = "33333333-3333-4333-8333-333333333333"
CONVERSATION = "55555555-5555-4555-8555-555555555555"


def _spy_session(monkeypatch):
    from matrx_ai.persistence import coordinator as coordinator_mod

    seen: list[dict] = []

    def fake_defer_update(self, model_cls, pk_value, payload):
        seen.append(dict(payload))
        return "op"

    monkeypatch.setattr(coordinator_mod, "_ambient_app_context", lambda: None)
    monkeypatch.setattr(coordinator_mod, "get_model", lambda table: object())
    return seen, fake_defer_update


def _queue(monkeypatch, user_id, fields):
    from matrx_ai.persistence.coordinator import Coordinator

    seen, fake = _spy_session(monkeypatch)
    coord = Coordinator.__new__(Coordinator)
    coord._user_id = user_id
    coord._dropped_ops_count = 0
    from matrx_ai.persistence.coordinator import CoordinatorPhase

    coord._phase = CoordinatorPhase.OPEN
    coord._session = type("S", (), {"defer_update": fake})()
    coord._session.defer_update = lambda model_cls, pk, payload: seen.append(dict(payload)) or "op"
    coord.queue("chat.conversation", fields, op_type="update", primary_key=("id", CONVERSATION))
    return seen


def test_a_label_write_through_the_coordinator_names_its_carried_person(monkeypatch) -> None:
    seen = _queue(monkeypatch, PERSON, {"title": "A title"})
    assert seen[0]["updated_by"] == PERSON


def test_an_updated_by_the_caller_named_is_kept(monkeypatch) -> None:
    other = "44444444-4444-4444-8444-444444444444"
    seen = _queue(monkeypatch, PERSON, {"title": "A title", "updated_by": other})
    assert seen[0]["updated_by"] == other


def test_a_coordinator_with_no_person_and_no_request_stays_the_systems(monkeypatch) -> None:
    seen = _queue(monkeypatch, None, {"title": "A title"})
    assert "updated_by" not in seen[0]


@pytest.mark.parametrize("table", ["chat.message", "chat.tool_call"])
def test_message_rows_keep_their_own_rule(monkeypatch, table) -> None:
    from matrx_ai.persistence.coordinator import with_actor

    assert ("updated_by" in with_actor(table, {"x": 1}, PERSON)) == (table == "chat.tool_call")
