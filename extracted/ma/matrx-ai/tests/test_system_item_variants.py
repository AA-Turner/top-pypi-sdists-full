"""One System item, several renderings (Arman, 2026-11-01).

A computed item declares variants in ``feed_config``; a binding names one; the item's cell
carries the default as its value and every named variant beside it, so one item named twice
with two variants delivers both. A zero-argument provider and an item with no variants work
exactly as before.
"""

from __future__ import annotations

import logging
from typing import Any

import pytest

from matrx_ai.context_engine import (
    SystemContextNames,
    SystemItemVariants,
    agent_context_from_resolved,
    configure_ambient_provider,
    configure_system_item_variants,
    system_cell_for_variant,
)

GUIDE_ID = "f371b79f-c82f-4158-9f50-a0e149f227f1"
FEED_CONFIG = {
    "kind": "reserved",
    "reserved_key": "workflow_step_guide",
    "variants": [
        {"key": "wide", "label": "Wide first cut"},
        {"key": "lean", "label": "Leanest", "description": "The smallest guide."},
    ],
    "default_variant": "wide",
}


def _resolved() -> dict[str, Any]:
    cell = {
        "key": "workflow_step_guide", "value": "(computed at runtime)", "type": "string",
        "context_item_id": GUIDE_ID, "scope_id": None, "scope_name": "System",
        "scope_type_id": None, "source": "system",
    }
    return {
        "variables": {
            "workflow_step_guide": {
                "value": cell["value"], "type": "string", "inject_as": "direct",
                "source": "system", "cells": [dict(cell)],
            }
        },
        "context": {"organization_id": "org-1"},
        "scope_labels": {},
        "cell_values": {GUIDE_ID: [dict(cell)]},
    }


@pytest.fixture
def guide_provider():
    calls: list[str | None] = []

    def guide(variant: str | None) -> str:
        calls.append(variant)
        return f"GUIDE[{variant}]"

    async def reader(key: str) -> Any:
        return FEED_CONFIG if key == "workflow_step_guide" else {}

    configure_ambient_provider("workflow_step_guide", guide)
    configure_system_item_variants(reader)
    try:
        yield calls
    finally:
        configure_ambient_provider("workflow_step_guide", None)
        configure_system_item_variants(None)


async def _cell_for(names: SystemContextNames) -> dict[str, Any]:
    ctx = await agent_context_from_resolved(
        "user-1", _resolved(), entity_type="conversation", entity_id="c-1",
        system_names=names, organization_id="org-1",
    )
    return ctx.cells_by_item_id[GUIDE_ID][0]


async def test_one_item_named_with_two_variants_delivers_both(guide_provider) -> None:
    names = (
        SystemContextNames()
        .naming([GUIDE_ID], by="the agent's variable guide", variant="lean")
        .naming([GUIDE_ID], by="the agent's context policy wide_guide")
    )
    cell = await _cell_for(names)
    assert cell["value"] == "GUIDE[wide]"  # the declared default
    assert cell["variant"] == "wide"
    assert cell["variants"] == {"lean": "GUIDE[lean]"}
    assert system_cell_for_variant(cell, "lean")["value"] == "GUIDE[lean]"
    assert system_cell_for_variant(cell, None)["value"] == "GUIDE[wide]"
    # each variant computed once, however many cells carry it
    assert sorted(guide_provider, key=str) == ["lean", "wide"]


async def test_the_declared_default_is_what_an_unvarianted_naming_reads(guide_provider) -> None:
    FEED_CONFIG["default_variant"] = "lean"
    try:
        cell = await _cell_for(SystemContextNames().naming([GUIDE_ID], by="x"))
    finally:
        FEED_CONFIG["default_variant"] = "wide"
    assert cell["value"] == "GUIDE[lean]"
    assert "variants" not in cell


async def test_an_undeclared_variant_is_announced_and_reads_the_default(guide_provider, caplog) -> None:
    caplog.set_level(logging.ERROR)
    cell = await _cell_for(SystemContextNames().naming([GUIDE_ID], by="x", variant="nope"))
    assert "variants" not in cell
    assert "does not declare" in caplog.text
    assert system_cell_for_variant(cell, "nope")["value"] == "GUIDE[wide]"
    assert "did not produce" in caplog.text
    assert "nope" not in guide_provider


async def test_a_zero_argument_provider_still_answers_every_naming() -> None:
    configure_ambient_provider("workflow_step_guide", lambda: "ONE GUIDE")
    try:
        cell = await _cell_for(SystemContextNames().naming([GUIDE_ID], by="x", variant="lean"))
    finally:
        configure_ambient_provider("workflow_step_guide", None)
    # no variants reader bound: the item declares none, and its one value is delivered
    assert cell["value"] == "ONE GUIDE"
    assert "variant" not in cell


def test_two_namings_that_differ_only_by_variant_are_both_kept() -> None:
    names = SystemContextNames().naming(["k"], by="a", variant="lean").naming(["k"], by="a")
    assert len(names.items) == 2
    assert names.refs() == ["k"]
    assert names.variants_named(key="k", context_item_id=None) == ["lean"]


def test_feed_config_is_read_tolerantly() -> None:
    assert SystemItemVariants.from_feed_config({}) == SystemItemVariants()
    assert SystemItemVariants.from_feed_config(None).variants == ()
    v = SystemItemVariants.from_feed_config(
        {"variants": [{"key": "a"}, {"key": "a"}, {"label": "no key"}, "x", {"key": "b"}],
         "default_variant": "missing"}
    )
    assert [x.key for x in v.variants] == ["a", "b"]
    assert v.default_variant == "a"  # an undeclared default falls back to the first


async def test_a_declared_variant_the_provider_cannot_render_never_breaks_the_turn(caplog) -> None:
    def guide(variant: str | None) -> str:
        if variant not in (None, "wide"):
            raise ValueError(f"unknown {variant}")
        return "WIDE"

    async def reader(_key: str) -> Any:
        return {"variants": [{"key": "lean"}, {"key": "wide"}], "default_variant": "lean"}

    configure_ambient_provider("workflow_step_guide", guide)
    configure_system_item_variants(reader)
    caplog.set_level(logging.ERROR)
    try:
        cell = await _cell_for(SystemContextNames().naming([GUIDE_ID], by="x", variant="lean"))
    finally:
        configure_ambient_provider("workflow_step_guide", None)
        configure_system_item_variants(None)
    assert cell["value"] == "WIDE"
    assert "cannot render" in caplog.text


async def test_a_provider_that_fails_outright_leaves_the_stored_value_and_the_turn_runs(caplog) -> None:
    def broken(_variant: str | None) -> str:
        raise KeyError("boom")

    configure_ambient_provider("workflow_step_guide", broken)
    caplog.set_level(logging.ERROR)
    try:
        cell = await _cell_for(SystemContextNames().naming([GUIDE_ID], by="x", variant="lean"))
    finally:
        configure_ambient_provider("workflow_step_guide", None)
    assert cell["value"] == "(computed at runtime)"
    assert "provider failed" in caplog.text
