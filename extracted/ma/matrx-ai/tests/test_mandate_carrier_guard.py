"""THE RUNTIME MANDATE-CARRIER GATE, proven.

What is being proven: an AI call that reaches ``execute_ai_request`` with no
Holder of any kind produces a ``mandate_bypass_runtime`` record through the
host's own ``record_error`` door — and one that DOES carry a Holder produces
nothing.

Why it is a forcing test: the assertions are about the real gate's real
behavior against the real ``_ext`` seam (only the host's record_error is a
sink we can read). Planting the bug — deleting the carrier check at the top of
``note_mandate_carrier`` — turns ``test_bypass_is_recorded`` RED.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai import _ext
from matrx_ai.orchestrator import mandate_carrier
from matrx_ai.orchestrator.mandate_carrier import (
    MANDATE_BYPASS_KIND,
    MANDATE_CARRIED_UNRESOLVED_KIND,
    MANDATE_HOLDER_METADATA_KEY,
    MANDATE_SCAN_SOURCE_APP,
    HOLDER_CARRIER_MARKER,
    HolderCarrier,
    carrier_for,
    note_mandate_carrier,
)


class _Config:
    """The one thing the gate reads off a config."""

    def __init__(self, model: str) -> None:
        self.model = model


class _Ctx:
    def __init__(self, **kwargs: Any) -> None:
        self.metadata = kwargs.pop("metadata", {})
        self.source_feature = kwargs.pop("source_feature", "")
        self.agent_id = kwargs.pop("agent_id", None)
        self.agent_version_id = kwargs.pop("agent_version_id", None)
        self.user_id = kwargs.pop("user_id", None)
        self.organization_id = kwargs.pop("organization_id", None)
        self.conversation_id = kwargs.pop("conversation_id", None)
        self.request_id = kwargs.pop("request_id", None)
        self.source_app = kwargs.pop("source_app", None)


@pytest.fixture
def recorded(monkeypatch) -> list[dict[str, Any]]:
    """Capture what the gate files, and make every test start with a clean dedupe."""
    rows: list[dict[str, Any]] = []

    def _record_error(exc: BaseException, **kwargs: Any) -> None:
        rows.append({"exc": exc, **kwargs})

    monkeypatch.setitem(_ext._registry, "record_error", _record_error)
    monkeypatch.setattr(mandate_carrier, "_context", lambda: None)
    mandate_carrier.reset_reported_signatures()
    yield rows
    mandate_carrier.reset_reported_signatures()


def test_bypass_is_recorded(recorded: list[dict[str, Any]]) -> None:
    """No carrier anywhere → a mandate_bypass_runtime row naming caller + model."""
    bypass = note_mandate_carrier(_Config("gpt-4o-mini"))

    assert bypass is not None, "a call with no Holder must return a bypass record"
    assert bypass["reason"] == "no_mandate_carrier"
    assert bypass["model"] == "gpt-4o-mini"
    assert "test_mandate_carrier_guard.py" in bypass["caller"]

    assert len(recorded) == 1, "exactly one system_error row"
    row = recorded[0]
    assert row["kind"] == MANDATE_BYPASS_KIND
    assert row["source_app"] == MANDATE_SCAN_SOURCE_APP
    assert row["payload"]["model"] == "gpt-4o-mini"
    assert "test_mandate_carrier_guard.py" in row["route"]


def test_explicit_mandate_key_with_a_resolved_holder_records_nothing(
    recorded: list[dict[str, Any]],
) -> None:
    """The workflow-step shape: the key AND the Holder that resolved it."""
    stamped = {MANDATE_HOLDER_METADATA_KEY: {"agent_id": "a1", "holder_type": "agent"}}
    assert (
        note_mandate_carrier(
            _Config("gpt-4o-mini"), stamped, mandate_key="workflow.step_intelligence"
        )
        is None
    )
    assert recorded == []


def test_explicit_mandate_key_without_a_resolved_holder_is_a_label(
    recorded: list[dict[str, Any]],
) -> None:
    """THE SECOND HALF OF THE GATE (2026-09-12). A key named at the executor
    with nothing resolved is a label: the Holder an admin bound never ran.
    Recorded as its own kind, stamped on the request, never raised.

    Proven failing: deleting the `carrier[0] == "mandate_key"` branch in
    ``note_mandate_carrier`` turns this red."""
    record = note_mandate_carrier(_Config("gpt-4o-mini"), mandate_key="workflow.step_intelligence")

    assert record is not None
    assert record["reason"] == MANDATE_CARRIED_UNRESOLVED_KIND
    assert record["mandate_key"] == "workflow.step_intelligence"
    assert len(recorded) == 1
    row = recorded[0]
    assert row["kind"] == MANDATE_CARRIED_UNRESOLVED_KIND
    assert row["source_app"] == MANDATE_SCAN_SOURCE_APP
    assert row["payload"]["mandate_key"] == "workflow.step_intelligence"
    assert "test_mandate_carrier_guard.py" in row["route"]

    # One row per code path, like the bypass.
    note_mandate_carrier(_Config("gpt-4o-mini"), mandate_key="workflow.step_intelligence")
    assert len(recorded) == 1


def test_explicit_mandate_key_with_a_context_agent_is_held(monkeypatch, recorded) -> None:
    """A loaded Holder executing under run_agent stamps agent_id on the context."""
    monkeypatch.setattr(mandate_carrier, "_context", lambda: _Ctx(agent_id="a1"))
    assert note_mandate_carrier(_Config("x"), mandate_key="workflow.step_intelligence") is None
    assert recorded == []


def test_metadata_mandate_key_records_nothing(recorded: list[dict[str, Any]]) -> None:
    assert note_mandate_carrier(_Config("x"), {"mandate_key": "chat.cx_default"}) is None
    assert recorded == []


def test_blank_mandate_key_is_not_a_carrier(recorded: list[dict[str, Any]]) -> None:
    """An empty string is the shape a broken upstream produces; it must not pass."""
    assert note_mandate_carrier(_Config("x"), mandate_key="   ") is not None
    assert len(recorded) == 1


def test_one_row_per_code_path(recorded: list[dict[str, Any]]) -> None:
    """Ten thousand extract steps are one fact, not ten thousand rows — and every one is COUNTED.

    Each sighting reaches the host door as a GROUPED capture keyed on the code path (``route``): the door
    keeps ONE open row per path and bumps its ``context.occurrences`` (matrx-orm ``record_error(group_open=)``,
    proven in ``packages/matrx-orm/tests/test_record_error_group_open.py``). A per-process set alone re-filed
    the same path once per process and deploy: 56 rows for 2 lines in 12 hours (2026-10-22)."""
    for model in ("gpt-4o-mini",) * 5 + ("claude-opus-5",):
        note_mandate_carrier(_Config(model))
    assert len(recorded) == 6, "every sighting is counted"
    assert all(r.get("group_open") is True for r in recorded), "one open row per code path, at the door"
    # A different model on the same line is the same code path: counted on the same row.
    assert len({r["route"] for r in recorded}) == 1


def test_a_door_without_grouping_still_records(monkeypatch) -> None:
    """A client host's record_error that takes no ``group_open`` still gets the row (never a lost alarm)."""
    rows: list[dict[str, Any]] = []

    def _plain(exc: BaseException, *, kind: str, error_type: str, error_text: str, source_app: str,
               source_feature: str, route: str, user_id: Any, organization_id: Any, conversation_id: Any,
               request_id: Any, payload: dict[str, Any]) -> None:
        rows.append({"kind": kind, "route": route})

    monkeypatch.setitem(_ext._registry, "record_error", _plain)
    monkeypatch.setattr(mandate_carrier, "_context", lambda: None)
    mandate_carrier.reset_reported_signatures()
    note_mandate_carrier(_Config("gpt-4o-mini"))
    mandate_carrier.reset_reported_signatures()
    assert [r["kind"] for r in rows] == [MANDATE_BYPASS_KIND]


def test_context_carriers(monkeypatch) -> None:
    """The three context-borne carriers the platform already writes."""
    monkeypatch.setattr(mandate_carrier, "_context", lambda: None)

    assert carrier_for(None, _Ctx(metadata={"mandate_key": "seo.page_analyzer"})) == (
        "context.metadata.mandate_key",
        "seo.page_analyzer",
    )
    assert carrier_for(None, _Ctx(source_feature="mandate:crm.save_contact")) == (
        "context.source_feature",
        "crm.save_contact",
    )
    assert carrier_for(None, _Ctx(agent_id="1234"))[0] == "context.agent_id"
    assert carrier_for(None, _Ctx(source_feature="agent")) is None


def test_gate_never_raises(recorded: list[dict[str, Any]]) -> None:
    """A broken record_error, a config with no model — the run still proceeds."""

    def _boom(*_args: Any, **_kwargs: Any) -> None:
        raise RuntimeError("the alarm itself is broken")

    _ext._registry["record_error"] = _boom
    assert note_mandate_carrier(object()) is not None  # no .model attribute at all


def test_the_holder_carrier_types_the_value_and_changes_nothing() -> None:
    """The retired function-wide decorator is gone; the value that carries the
    Holder is typed instead, and the type is an inert ``Annotated``."""
    from typing import Annotated, get_args, get_origin

    assert not hasattr(mandate_carrier, "mandate_carrier_passthrough")
    carried = HolderCarrier[dict[str, Any] | None]
    assert get_origin(carried) is Annotated
    assert get_args(carried) == (dict[str, Any] | None, HOLDER_CARRIER_MARKER)
