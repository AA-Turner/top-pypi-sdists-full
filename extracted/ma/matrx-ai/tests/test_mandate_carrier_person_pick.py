"""A PERSON'S OWN PICK runs directly (mandates STATE.md §9, D51): the carrier gate must not file it as a bypass.

Live 2026-11-04: every Android chat turn (a person picks a model, no agent) filed
``mandate_bypass_runtime`` at ``ai_task.py in _run_ai_task_body`` (42 occurrences). The person's pick is
read from the provenance WITNESS (``reconcile_origin``), so a caller cannot declare its way past the gate:
an undeclared HTTP caller (``api``) on a non-chat route, a platform helper (``child_agent``) and background work
stay bypasses.

Live 2026-11-07..15: ~195 unattested ``/ai/chat`` turns from test and agent accounts (which test as a user
would) still filed bypasses, because billing's person predicate refuses those accounts. The host now installs a
carrier-only predicate (``set_caller_pick_resolver``) that answers for a witnessed ``api`` chat-door turn; it
never upgrades a machine class.
"""

from __future__ import annotations

from typing import Any

import pytest
from matrx_connect import AppContext
from matrx_connect.context import provenance
from matrx_connect.emitters.console_emitter import ConsoleEmitter

from matrx_ai import _ext
from matrx_ai.orchestrator import mandate_carrier
from matrx_ai.orchestrator.mandate_carrier import (
    MANDATE_BYPASS_KIND,
    PERSON_PICK_CARRIER,
    carrier_for,
    note_mandate_carrier,
)


class _Config:
    def __init__(self, model: str) -> None:
        self.model = model


def _http_ctx(*, person: bool, auth_type: str = "token", **overrides: Any) -> AppContext:
    """A chat request as the server sees it; the class is DERIVED by the provenance module, never stamped.

    ``person`` sets the host's person-request resolver (the seam ``set_person_request_resolver`` the
    host installs), so ``reconcile_origin`` reads a real person's own request as ``human``."""
    provenance.set_person_request_resolver((lambda _ctx: True) if person else None)
    return AppContext(
        emitter=ConsoleEmitter("test", accumulate=False),
        route=overrides.pop("route", "/ai/chat"),
        auth_type=auth_type,
        source_app="matrx-android",
        source_feature="chat",
        **overrides,
    )


@pytest.fixture
def recorded(monkeypatch) -> list[dict[str, Any]]:
    # Whatever resolver the host installed comes back after the test.
    monkeypatch.setattr(provenance, "_person_request_resolver", provenance._person_request_resolver)
    monkeypatch.setattr(mandate_carrier, "_CALLER_PICK_RESOLVER", None)
    rows: list[dict[str, Any]] = []
    monkeypatch.setitem(_ext._registry, "record_error", lambda exc, **kw: rows.append({"exc": exc, **kw}))
    mandate_carrier.reset_reported_signatures()
    yield rows
    mandate_carrier.reset_reported_signatures()


def test_a_person_picking_a_model_in_chat_is_held(monkeypatch, recorded) -> None:
    ctx = _http_ctx(person=True)
    monkeypatch.setattr(mandate_carrier, "_context", lambda: ctx)

    assert carrier_for(None, ctx) == (PERSON_PICK_CARRIER, "person")
    assert note_mandate_carrier(_Config("model-the-person-picked")) is None
    assert recorded == []


@pytest.mark.parametrize(
    ("label", "ctx_factory"),
    [
        # An HTTP caller that did not attest a person, on a route that is not a chat door, with the
        # host's caller-pick predicate installed: code picking.
        ("api", lambda: _http_ctx(person=False, route="/research/topics/t1/run")),
        # The same unattested chat turn when the host installed no caller-pick predicate.
        ("api-unconfigured", lambda: _http_ctx(person=False)),
        # A helper the platform launched inside the person's turn is not their pick.
        (
            "child_agent",
            lambda: _http_ctx(
                person=True, conversation_type="subagent", parent_conversation_id="p1"
            ),
        ),
        # Background work with no HTTP witness.
        ("system", lambda: AppContext(emitter=ConsoleEmitter("test", accumulate=False))),
    ],
)
def test_code_picking_a_model_is_still_a_bypass(monkeypatch, recorded, label, ctx_factory) -> None:
    if label != "api-unconfigured":
        mandate_carrier.set_caller_pick_resolver(_chat_door_only)
    ctx = ctx_factory()
    monkeypatch.setattr(mandate_carrier, "_context", lambda: ctx)

    assert carrier_for(None, ctx) is None, label
    assert note_mandate_carrier(_Config(f"model-{label}")) is not None
    assert [row["kind"] for row in recorded] == [MANDATE_BYPASS_KIND]


def _chat_door_only(ctx: Any) -> bool:
    """A stand-in for the host's predicate: the chat doors only (the host's real one is tested in aidream)."""
    return ctx.route in ("/ai/chat", "/ai/manual")


def test_a_test_accounts_unattested_chat_turn_is_held_by_the_host_predicate(monkeypatch, recorded) -> None:
    """Before the seam: a test account's own ``/ai/chat`` pick (witness ``api``) filed a bypass."""
    mandate_carrier.set_caller_pick_resolver(_chat_door_only)
    ctx = _http_ctx(person=False)
    monkeypatch.setattr(mandate_carrier, "_context", lambda: ctx)

    assert carrier_for(None, ctx) == (PERSON_PICK_CARRIER, "person")
    assert note_mandate_carrier(_Config("model-the-test-account-picked")) is None
    assert recorded == []


@pytest.mark.parametrize(
    ("label", "ctx_factory"),
    [
        ("child_agent", lambda: _http_ctx(person=True, conversation_type="subagent", parent_conversation_id="p1")),
        ("system", lambda: AppContext(emitter=ConsoleEmitter("test", accumulate=False))),
        ("client_auto", lambda: _http_ctx(person=False, origin_class="client_auto")),
    ],
)
def test_the_caller_pick_predicate_never_upgrades_a_machine_class(monkeypatch, recorded, label, ctx_factory) -> None:
    """The host predicate answers only for a witnessed ``api`` turn, even when it would say yes."""
    mandate_carrier.set_caller_pick_resolver(lambda _ctx: True)
    ctx = ctx_factory()
    monkeypatch.setattr(mandate_carrier, "_context", lambda: ctx)

    assert carrier_for(None, ctx) is None, label
    assert note_mandate_carrier(_Config(f"model-{label}")) is not None
    assert [row["kind"] for row in recorded] == [MANDATE_BYPASS_KIND]
