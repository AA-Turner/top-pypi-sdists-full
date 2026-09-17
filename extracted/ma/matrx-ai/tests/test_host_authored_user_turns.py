"""A user-role turn the HOST wrote is never mistaken for the person's own.

THE DEFECT THIS EXISTS FOR (matrx-frontend D327, 2026-09-16). Three different
things land in the `user` tier of `chat.message`: what the person typed, the
agent definition's own seeded opening turn merged with resolved launch variables
(so provider replay stays lossless), and turns the orchestrator injects mid-loop
— the "⚠️ SYSTEM NOTICE (not from the user)" gates. The first two are separated
by the `user_content` column. The third was not: it persisted with `user_content`
NULL, and NULL is defined by the contract as "a row predating this contract", so
every reader doing it RIGHT fell back to `content` and quoted the machine's own
notice back at the person as her words (live row `chat.message`
363252d8-08d4-444e-9795-b139a607d3ad).

Authorship can only be stamped by the WRITER — no reader can infer it. So the
guard has two halves:

  1. the primitive really stamps it, all the way to the storage dict the DB
     write consumes, and the platform's one projection really reads it;
  2. no orchestrator gate builds such a turn by hand any more — a census over
     the real source, because a new gate added next month is exactly how this
     class comes back.

PROVEN FAILING: with `user_content=[]` dropped from `host_authored_user_turn`,
half 1 fails on the projection (the notice comes back as the human's words) and
on the storage dict; restoring a bare `UnifiedMessage(role="user", ...)` at any
executor gate fails half 2.
"""

from __future__ import annotations

import re
from pathlib import Path

from matrx_ai.config import (
    HOST_AUTHORED_BY,
    host_authored_user_turn,
    human_authored_text,
)

NOTICE = (
    "⚠️ SYSTEM NOTICE (not from the user): 3 of your last 5 tool calls have FAILED."
)


def test_a_host_injected_turn_projects_to_nothing_a_person_said():
    message = host_authored_user_turn(NOTICE, reason="loop_guard_approaching")
    stored = message.to_storage_dict()

    # The model still receives the notice — that is the whole point of injecting it.
    assert stored["content"] == [{"type": "text", "text": NOTICE}]
    # 🚨 And the authorship record says, explicitly, that the human said nothing.
    # EMPTY, never absent: absent is NULL, and NULL means "we don't know".
    assert stored["user_content"] == []
    assert stored["metadata"]["authored_by"] == HOST_AUTHORED_BY
    assert stored["metadata"]["authored_reason"] == "loop_guard_approaching"

    assert (
        human_authored_text("user", stored["content"], stored["user_content"]) == ""
    ), "the orchestrator's own notice was read back as the person's words"


def test_a_row_predating_the_contract_still_falls_back_to_content():
    """NULL is not empty. A historical row must keep reading as it always did."""
    assert (
        human_authored_text("user", [{"type": "text", "text": "her words"}], None)
        == "her words"
    )


def test_the_humans_words_win_over_the_merged_payload():
    merged = [
        {"type": "text", "text": "Let's get started. Follow the mode you were given."},
        {"type": "text", "text": "The call I keep having to make is whether a pallet…"},
    ]
    hers = [{"type": "text", "text": "The call I keep having to make is whether a pallet…"}]
    assert (
        human_authored_text("user", merged, hers)
        == "The call I keep having to make is whether a pallet…"
    )


def test_no_orchestrator_gate_builds_a_user_turn_by_hand():
    """The census half: every mid-loop user injection goes through the primitive.

    A bare `UnifiedMessage(role="user", ...)` in the orchestrator is the exact
    shape that left `user_content` NULL. Nothing forbids the class itself — the
    drain path builds one deliberately WITH `user_content` — so the census reads
    the constructions and requires each to carry authorship.
    """
    root = Path(__file__).resolve().parents[1] / "matrx_ai"
    offenders: list[str] = []
    for path in (root / "orchestrator").rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        for match in re.finditer(r"UnifiedMessage\(\s*role=\"user\"", source):
            line = source.count("\n", 0, match.start()) + 1
            offenders.append(f"{path.relative_to(root)}:{line}")
    assert offenders == [], (
        "an orchestrator gate builds a user-role turn by hand — it will persist "
        "with user_content NULL and be read as something the person said. Use "
        f"host_authored_user_turn(): {offenders}"
    )


def test_the_drain_path_stamps_authorship_on_both_halves():
    """`dynamic_drain` delivers BOTH a queued human message and a host steer.

    Only that code knows which is which, so it is the one place allowed to build
    a user turn directly — and it must stamp `user_content` on both branches.
    """
    source = (
        Path(__file__).resolve().parents[1]
        / "matrx_ai"
        / "tools"
        / "dynamic_drain.py"
    ).read_text(encoding="utf-8")
    assert "user_content=[TextContent(text=text)]" in source, (
        "the queued HUMAN message lost its authorship stamp — it will read as a "
        "row predating the contract"
    )
    assert "host_authored_user_turn(text, reason=f\"injection:{kind}\")" in source, (
        "a host steer delivered as a user turn is no longer stamped host-authored"
    )
