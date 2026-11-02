"""The interrupt presentation contract — SPEC-workflow-ui-contract §4.1/§4.2.

Three things are held down here:

  * **§4.1** the presentation block rides ``ctx.interrupt(payload)`` beside the
    question, and every default reproduces today's behavior — an existing node
    gains keys, never different values;
  * **§4.2** ``preset="approval"`` DERIVES the ``{approved, note}`` schema when
    the author supplied none, and NEVER overrides one they did supply;
  * **§4.3 leg 2** ``build_interrupt_snapshot`` turns the scheduler's interrupt
    into the flat row snapshot — total, including for a payload from a node
    that declares none of the block.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_graph.db.run_store import WAITING_STATUSES, build_interrupt_snapshot
from matrx_graph.errors import GraphInterrupt
from matrx_graph.nodes.control.human_input import (
    APPROVAL_SCHEMA_HINT,
    HumanInputConfig,
    HumanInputExecutor,
    HumanInputInput,
)
from matrx_graph.nodes.output.to_frontend import WORKFLOW_RENDER_SURFACE


class _Ctx:
    """The one method the executor uses. ``ctx.interrupt`` raises, so the
    payload is captured on the exception, exactly as the scheduler sees it."""

    node_id = "ask"

    def interrupt(self, payload: dict[str, Any]) -> None:
        raise GraphInterrupt(node_id=self.node_id, payload=payload)


async def _payload(config: HumanInputConfig, **inputs: Any) -> dict[str, Any]:
    with pytest.raises(GraphInterrupt) as excinfo:
        await HumanInputExecutor().execute(_Ctx(), HumanInputInput(**inputs), config)
    return excinfo.value.payload


async def test_defaults_are_todays_behavior() -> None:
    payload = await _payload(HumanInputConfig())
    # The pre-change keys, byte for byte.
    assert payload["prompt"] == "Please provide input to continue"
    assert payload["schema_hint"] is None
    assert payload["default_answer"] == ""
    assert payload["context"] == {}
    # The block, at its defaults — nothing on screen moves.
    assert payload["preset"] == "free_text"
    assert payload["title"] is None
    assert payload["presentation"] == "panel"
    assert payload["component_ref"] is None
    assert payload["surface"] == WORKFLOW_RENDER_SURFACE


async def test_presentation_block_rides_the_payload() -> None:
    payload = await _payload(
        HumanInputConfig(
            prompt="Ship it?",
            title="Approve the {context.doc}",
            presentation="showcase",
            component_ref="ApprovalCard",
            surface="matrx-user/custom",
        ),
        context={"doc": "draft"},
    )
    assert payload["title"] == "Approve the draft"  # same interpolation as prompt
    assert payload["presentation"] == "showcase"
    assert payload["component_ref"] == "ApprovalCard"
    assert payload["surface"] == "matrx-user/custom"


async def test_approval_preset_derives_the_schema() -> None:
    config = HumanInputConfig(preset="approval", prompt="Approve?")
    assert config.effective_schema_hint() == APPROVAL_SCHEMA_HINT
    payload = await _payload(config)
    assert payload["preset"] == "approval"
    assert payload["schema_hint"] == {
        "type": "object",
        "properties": {"approved": {"type": "boolean"}, "note": {"type": "string"}},
        "required": ["approved"],
    }


async def test_authors_schema_always_wins_over_the_preset() -> None:
    authored = {"type": "object", "properties": {"verdict": {"type": "string"}}}
    payload = await _payload(HumanInputConfig(preset="approval", schema_hint=authored))
    assert payload["schema_hint"] == authored


async def test_non_approval_presets_derive_nothing() -> None:
    assert HumanInputConfig(preset="free_text").effective_schema_hint() is None
    assert HumanInputConfig(preset="form").effective_schema_hint() is None


def test_snapshot_flattens_the_scheduler_interrupt() -> None:
    snapshot = build_interrupt_snapshot(
        {
            "node_id": "approve",
            "checkpoint_id": "66666666-6666-4666-8666-666666666666",
            "payload": {
                "prompt": "Ship it?",
                "title": "Approve the draft",
                "presentation": "showcase",
                "preset": "approval",
                "schema_hint": APPROVAL_SCHEMA_HINT,
                "escalation": {
                    "waiting_since": "2026-08-27T10:00:00+00:00",
                    "deadline_at": "2026-08-28T10:00:00+00:00",
                },
            },
        }
    )
    assert snapshot["node_id"] == "approve"
    assert snapshot["checkpoint_id"] == "66666666-6666-4666-8666-666666666666"
    assert snapshot["title"] == "Approve the draft"
    assert snapshot["prompt"] == "Ship it?"
    assert snapshot["presentation"] == "showcase"
    assert snapshot["preset"] == "approval"
    assert snapshot["schema_hint"] == APPROVAL_SCHEMA_HINT
    assert snapshot["asked_at"] == "2026-08-27T10:00:00+00:00"
    assert snapshot["deadline"] == "2026-08-28T10:00:00+00:00"


def test_snapshot_is_total_for_a_pre_change_interrupt() -> None:
    """A node that declares none of the block still yields a well-formed
    snapshot — this is what makes the projection's fallback work on old runs."""
    snapshot = build_interrupt_snapshot({"node_id": "ask", "payload": {"prompt": "?"}})
    assert snapshot["presentation"] == "panel"
    assert snapshot["preset"] == "free_text"
    assert snapshot["checkpoint_id"] is None
    assert snapshot["deadline"] is None
    assert snapshot["asked_at"]  # the write instant — never absent
    # And a completely empty interrupt does not raise.
    assert build_interrupt_snapshot(None)["preset"] == "free_text"


def test_a_sleep_park_is_not_a_question() -> None:
    """``flow.sleep`` parks the run INTERRUPTED too — but it waits on the CLOCK,
    and Postgres already holds its wake job. Stamped once, here, so no discovery
    surface can put a timer in a person's inbox."""
    from matrx_graph.nodes.flow.sleep import SLEEP_MARKER

    sleeping = build_interrupt_snapshot(
        {
            "node_id": "wait",
            "payload": {SLEEP_MARKER: {"wake_at": "2026-08-29T00:00:00+00:00"}},
        }
    )
    assert sleeping["waits_for_person"] is False

    asking = build_interrupt_snapshot({"node_id": "ask", "payload": {"prompt": "?"}})
    assert asking["waits_for_person"] is True


def test_the_inbox_is_exactly_two_statuses() -> None:
    assert WAITING_STATUSES == ("interrupted", "awaiting_input")
