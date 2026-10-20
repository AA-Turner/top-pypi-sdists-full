"""A deliberate, recorded tools-array break excuses ONLY the tools it names.

Adversarial M5 (2026-10-18): the wire guard consumed a single yes/no "the ledger made a
break" flag, so ANY other change made in the same request was excused with it. A tool
removed or reordered alongside one recorded definition update rode through silently."""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.providers import cache_guard
from matrx_ai.tools import declaration_ledger

CONV = "conv-m5-scope"


def _decl(name: str, description: str = "d") -> dict[str, Any]:
    return {"name": name, "description": description, "input_schema": {}}


def _payload(*decls: dict[str, Any]) -> dict[str, Any]:
    return {"tools": list(decls)}


@pytest.fixture(autouse=True)
def _clean():
    declaration_ledger.reset_for_tests()
    cache_guard._CONVERSATION_TOOLS.clear()
    yield
    declaration_ledger.reset_for_tests()
    cache_guard._CONVERSATION_TOOLS.clear()


def _ledger_turn(*decls: dict[str, Any]) -> None:
    declaration_ledger.stabilize_declarations(
        "anthropic", list(decls), name_of=lambda d: d.get("name"),
        conversation_id=CONV, identities={},
    )


def _observe(*decls: dict[str, Any]) -> str | None:
    return cache_guard.observe_tool_declarations(
        provider="anthropic", conversation_id=CONV, payload=_payload(*decls)
    )


def test_the_recorded_change_alone_is_excused() -> None:
    _ledger_turn(_decl("a"), _decl("b"))
    assert _observe(_decl("a"), _decl("b")) is None
    _ledger_turn(_decl("a", "new words"), _decl("b"))  # recorded definition update of a
    assert _observe(_decl("a", "new words"), _decl("b")) is None


def test_an_unrecorded_removal_riding_with_a_recorded_update_still_screams() -> None:
    _ledger_turn(_decl("a"), _decl("b"), _decl("c"))
    assert _observe(_decl("a"), _decl("b"), _decl("c")) is None
    _ledger_turn(_decl("a", "new words"), _decl("b"), _decl("c"))  # records "a" only
    # The wire loses "c" as well: nobody recorded that.
    assert _observe(_decl("a", "new words"), _decl("b")) == "tool_removed_mid_conversation"


def test_a_reorder_riding_with_a_recorded_update_still_screams() -> None:
    _ledger_turn(_decl("a"), _decl("b"), _decl("c"))
    assert _observe(_decl("a"), _decl("b"), _decl("c")) is None
    _ledger_turn(_decl("a", "new words"), _decl("b"), _decl("c"))
    assert _observe(_decl("a", "new words"), _decl("c"), _decl("b")) is not None


def test_a_whole_belt_swap_is_still_excused_when_the_ledger_recorded_it() -> None:
    _ledger_turn(_decl("a"), _decl("b"))
    assert _observe(_decl("a"), _decl("b")) is None
    _ledger_turn(_decl("x"), _decl("y"))
    assert _observe(_decl("x"), _decl("y")) is None
