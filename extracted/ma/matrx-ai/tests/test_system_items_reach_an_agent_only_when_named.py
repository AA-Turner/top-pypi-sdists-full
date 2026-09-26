"""A System (platform) context item reaches an agent ONLY when something names it.

Lane CONTEXT-VALUES-NAMED (Arman, 2026-09-25): "It must be named in context values or
variables or it should not be fed … these will grow to thousands … some of them will also
trigger api calls or other fetching". Both resolvers hand back every deliverable System item;
``agent_context_from_resolved`` — the one body both answers pass through — keeps only the named
ones, and an unnamed computed item is never computed.

The resolver payloads below are the live shape of ``public.resolve_full_context`` /
``custom.resolve_context`` (2026-09-25): the System lane runs first, so a same-key scope item
overwrites the variable entry and carries the System cell in its ``cells``.
"""

from __future__ import annotations

import copy
from typing import Any

import pytest

from matrx_ai import context_engine
from matrx_ai.context_engine import (
    PLATFORM_DEFAULT_SYSTEM_ITEM_KEYS,
    SystemContextNames,
    agent_context_from_resolved,
    naming_system_items,
)

DATE_ID = "11111111-1111-4111-8111-111111111111"
GUIDANCE_ID = "0340dfe8-372c-425d-aed4-08c8a5753088"
COMPANY_ID = "33333333-3333-4333-8333-333333333333"
YEAR_ID = "44444444-4444-4444-8444-444444444444"
SCOPE_COMPANY_ID = "55555555-5555-4555-8555-555555555555"
SCOPE_ID = "66666666-6666-4666-8666-666666666666"


def _system_cell(key: str, item_id: str, value: Any) -> dict[str, Any]:
    return {
        "key": key,
        "value": value,
        "type": "string",
        "context_item_id": item_id,
        "scope_id": None,
        "scope_name": "System",
        "scope_type_id": None,
        "source": "system",
    }


def _resolved() -> dict[str, Any]:
    date = _system_cell("current_date", DATE_ID, "2026-06-15")
    year = _system_cell("current_year", YEAR_ID, "2026")
    guidance = _system_cell("ai_models_guidance", GUIDANCE_ID, ["Use a capable model for tool loops."])
    company_sys = _system_cell("company_name", COMPANY_ID, "AI Matrx")
    company_scope = {
        "key": "company_name",
        "value": "Castellano & Reyes, LLP",
        "type": "string",
        "context_item_id": SCOPE_COMPANY_ID,
        "scope_id": SCOPE_ID,
        "scope_name": "Meridian Risk Services",
        "scope_type_id": "77777777-7777-4777-8777-777777777777",
        "source": "scope:Meridian Risk Services",
    }

    def entry(cell: dict[str, Any], cells: list[dict[str, Any]]) -> dict[str, Any]:
        return {
            "value": cell["value"],
            "type": "string",
            "inject_as": "direct",
            "source": cell["source"],
            "cells": cells,
        }

    return {
        "variables": {
            "current_date": entry(date, [date]),
            "current_year": entry(year, [year]),
            "ai_models_guidance": entry(guidance, [guidance]),
            # the scope lane overwrote the System entry and kept the System cell in `cells`
            "company_name": entry(company_scope, [company_sys, company_scope]),
        },
        "context": {"organization_id": "org-1"},
        "scope_labels": {},
        "cell_values": {
            DATE_ID: [date],
            YEAR_ID: [year],
            GUIDANCE_ID: [guidance],
            COMPANY_ID: [company_sys],
            SCOPE_COMPANY_ID: [company_scope],
        },
    }


@pytest.fixture(autouse=True)
def _no_merge_producer(monkeypatch):
    monkeypatch.setattr(context_engine, "_merge_producer", None)
    # No host knob reader: the registered default list answers (announced).
    monkeypatch.setattr(context_engine, "_defaults_reader", None, raising=False)


@pytest.fixture(autouse=True)
def timezone_reads(monkeypatch):
    """The person's timezone ladder stood in: Los Angeles; reads[] = one entry per read."""
    reads: list[tuple[Any, Any]] = []

    async def person_timezone(user_id, organization_id):
        reads.append((user_id, organization_id))
        return "America/Los_Angeles"

    monkeypatch.setattr(context_engine, "person_timezone", person_timezone, raising=False)
    return reads


@pytest.fixture
def counted_providers(monkeypatch):
    """Every ambient provider replaced by a counting double: calls[key] = how often computed."""
    calls: dict[str, int] = {}

    def providers(user_id: str | None, timezone: str = "UTC") -> dict[str, Any]:
        def make(key: str):
            def compute() -> str:
                calls[key] = calls.get(key, 0) + 1
                return f"computed:{key}"

            return compute

        return {
            k: make(k)
            for k in (
                "current_date",
                "current_datetime",
                "current_timezone",
                "current_time",
                "current_year",
                "current_user_id",
            )
        }

    monkeypatch.setattr(context_engine, "_ambient_providers", providers)
    return calls


async def _build(names: SystemContextNames | None = None, **kw: Any):
    return await agent_context_from_resolved(
        "user-1", copy.deepcopy(_resolved()), entity_type="conversation", entity_id="c-1",
        system_names=names, **kw,
    )


async def test_nothing_named_means_no_system_item_reaches_the_agent():
    agent_ctx = await _build(SystemContextNames.none())

    assert "current_date" not in agent_ctx.direct_variables
    assert "ai_models_guidance" not in agent_ctx.direct_variables
    for cid in (DATE_ID, YEAR_ID, GUIDANCE_ID, COMPANY_ID):
        assert cid not in agent_ctx.cells_by_item_id
    block = agent_ctx.build_system_prompt_block()
    assert "AI Matrx" not in block
    assert "Use a capable model" not in block
    assert sorted(agent_ctx.system_withheld) == sorted(
        ["current_date", "current_year", "ai_models_guidance", "company_name"]
    )


async def test_an_unnamed_computed_item_is_never_computed(counted_providers):
    agent_ctx = await _build(SystemContextNames.none().naming(["current_date"], by="the agent's variable today"))

    assert counted_providers == {"current_date": 1}  # current_year was offered, never computed
    assert agent_ctx.direct_variables["current_date"]["value"] == "computed:current_date"
    assert "current_year" not in agent_ctx.direct_variables


async def test_a_binding_by_id_names_exactly_that_item():
    names = SystemContextNames.none().naming([GUIDANCE_ID], by="the agent's variable model_selection_guidance")
    agent_ctx = await _build(names)

    assert list(agent_ctx.cells_by_item_id[GUIDANCE_ID])[0]["key"] == "ai_models_guidance"
    assert "ai_models_guidance" in agent_ctx.direct_variables
    assert "current_date" not in agent_ctx.direct_variables
    assert agent_ctx.system_delivered == [
        {
            "key": "ai_models_guidance",
            "context_item_id": GUIDANCE_ID,
            "named_by": ["the agent's variable model_selection_guidance"],
        }
    ]


async def test_a_scope_item_sharing_a_system_key_keeps_its_own_value_and_loses_only_the_system_cell():
    agent_ctx = await _build(SystemContextNames.none())

    entry = agent_ctx.direct_variables["company_name"]
    assert entry["value"] == "Castellano & Reyes, LLP"
    assert [c["source"] for c in entry["cells"]] == ["scope:Meridian Risk Services"]
    assert SCOPE_COMPANY_ID in agent_ctx.cells_by_item_id
    assert "AI Matrx" not in agent_ctx.build_system_prompt_block()


async def test_no_naming_in_force_is_the_declared_default_list_never_all(counted_providers):
    agent_ctx = await _build(None)

    offered = {"current_date", "current_year", "ai_models_guidance", "company_name"}
    delivered = {d["key"] for d in agent_ctx.system_delivered}
    assert delivered == offered & set(PLATFORM_DEFAULT_SYSTEM_ITEM_KEYS)
    assert delivered  # the registered default list (the knob's default) is not empty
    assert "ai_models_guidance" not in agent_ctx.direct_variables
    assert "company_name" not in {d["key"] for d in agent_ctx.system_delivered}
    assert set(counted_providers) <= set(PLATFORM_DEFAULT_SYSTEM_ITEM_KEYS)


async def test_the_naming_in_force_applies_when_none_is_passed():
    names = SystemContextNames.none().naming(["company_name"], by="your pick in the inspector")
    with naming_system_items(names):
        agent_ctx = await _build(None)

    assert [d["key"] for d in agent_ctx.system_delivered] == ["company_name"]
    assert agent_ctx.system_delivered[0]["named_by"] == ["your pick in the inspector"]
    # the scope entry still owns the variable; the System cell rides beside it
    sources = [c["source"] for c in agent_ctx.direct_variables["company_name"]["cells"]]
    assert sources == ["system", "scope:Meridian Risk Services"]


# ─────────────────────────────────────── lane CONTEXT-VALUES-NAMED-2: the knob, the clock, the SQL


async def test_the_default_list_is_the_knob_not_a_constant(monkeypatch):
    """Chair ruling (a): an admin who puts company_name on the list changes what every agent gets."""

    async def knob():
        return ["company_name"]

    context_engine.configure_system_item_defaults(knob)
    try:
        agent_ctx = await _build(None)
    finally:
        context_engine.configure_system_item_defaults(None)

    assert [d["key"] for d in agent_ctx.system_delivered] == ["company_name"]
    assert agent_ctx.system_delivered[0]["named_by"] == [context_engine.PLATFORM_DEFAULT_NAMER]
    assert "current_date" not in agent_ctx.direct_variables


async def test_an_unreadable_knob_answers_the_registered_default_and_says_so(caplog):
    async def broken():
        raise RuntimeError("feature_knob unreachable")

    context_engine.configure_system_item_defaults(broken)
    try:
        keys = await context_engine.platform_default_system_item_keys()
    finally:
        context_engine.configure_system_item_defaults(None)

    assert keys == ("current_date", "current_datetime", "current_timezone")
    assert "could not be read" in caplog.text


def test_the_registered_default_is_the_rulings_three_items():
    assert PLATFORM_DEFAULT_SYSTEM_ITEM_KEYS == ("current_date", "current_datetime", "current_timezone")


async def test_the_datetime_is_rendered_in_the_persons_timezone_with_its_offset(timezone_reads):
    """Chair ruling (b): current_datetime in the person's timezone, offset shown; the timezone
    is itself a System item; the date agrees with the date-time."""
    from datetime import datetime
    from zoneinfo import ZoneInfo

    resolved = _resolved()
    for key, item_id in (("current_datetime", "88888888-8888-4888-8888-888888888888"),
                         ("current_timezone", "99999999-9999-4999-8999-999999999999")):
        cell = _system_cell(key, item_id, "(computed at runtime)")
        resolved["variables"][key] = {"value": cell["value"], "type": "string",
                                      "inject_as": "direct", "source": "system", "cells": [cell]}
        resolved["cell_values"][item_id] = [cell]
    agent_ctx = await agent_context_from_resolved(
        "user-1", resolved, entity_type="conversation", entity_id="c-1",
        system_names=SystemContextNames.platform_defaults(),
    )

    got = agent_ctx.direct_variables["current_datetime"]["value"]
    parsed = datetime.fromisoformat(got)
    expected_offset = datetime.now(ZoneInfo("America/Los_Angeles")).utcoffset()
    assert parsed.utcoffset() == expected_offset
    assert got.endswith(("-07:00", "-08:00"))
    assert agent_ctx.direct_variables["current_timezone"]["value"] == "America/Los_Angeles"
    assert agent_ctx.direct_variables["current_date"]["value"] == parsed.date().isoformat()
    assert timezone_reads == [("user-1", "org-1")]


async def test_the_timezone_is_read_only_when_a_clock_item_is_named(timezone_reads):
    await _build(SystemContextNames.none().naming(["company_name"], by="the agent's variable company"))
    assert timezone_reads == []


async def test_both_resolvers_are_handed_the_names_and_read_nothing_else(monkeypatch):
    """Chair ruling (c): the naming reaches the SQL — the old resolver's fifth argument and the
    path chooser's ``system_item_refs`` are the same list, generated from SystemContextNames."""
    from matrx_orm import ArrayArg

    seen: dict[str, Any] = {}

    async def rpc(_db, schema, fn, *args, **_kw):
        seen["rpc"] = (schema, fn, args)
        return copy.deepcopy(_resolved())

    async def chooser(**kw):
        seen["chooser"] = kw
        return None

    monkeypatch.setattr("matrx_orm.call_function", rpc)
    monkeypatch.setattr(context_engine, "_resolve_context_database", lambda: "test")
    monkeypatch.setattr(context_engine, "_path_chooser", chooser)

    names = SystemContextNames.none().naming([GUIDANCE_ID, "current_date"], by="the agent's variable x")
    await context_engine.build_agent_context(
        "user-1", "conversation", "c-1", [], use_cache=False, system_names=names
    )

    schema, fn, args = seen["rpc"]
    assert (schema, fn) == ("public", "resolve_full_context")
    refs = args[4]
    assert isinstance(refs, ArrayArg)
    assert list(refs.value) == sorted([GUIDANCE_ID, "current_date"]) == names.refs()
    assert seen["chooser"]["system_item_refs"] == names.refs()

    seen.clear()
    await context_engine.build_agent_context(
        "user-1", "conversation", "c-1", [], use_cache=False, system_names=SystemContextNames.none()
    )
    # nothing named: an EXPLICIT empty array — NULL would be the knob's default list
    assert seen["rpc"][2][4].value == []
    assert seen["chooser"]["system_item_refs"] == []


async def test_two_namings_never_share_one_cached_answer(monkeypatch):
    calls: list[Any] = []

    async def rpc(_db, _schema, _fn, *args, **_kw):
        calls.append(args[4].value)
        return copy.deepcopy(_resolved())

    monkeypatch.setattr("matrx_orm.call_function", rpc)
    monkeypatch.setattr(context_engine, "_resolve_context_database", lambda: "test")
    monkeypatch.setattr(context_engine, "_path_chooser", None)
    context_engine.invalidate_context_cache()

    a = SystemContextNames.none().naming(["current_date"], by="a")
    b = SystemContextNames.none().naming(["company_name"], by="b")
    await context_engine.build_agent_context("user-9", "conversation", "c-9", [], system_names=a)
    await context_engine.build_agent_context("user-9", "conversation", "c-9", [], system_names=b)
    await context_engine.build_agent_context("user-9", "conversation", "c-9", [], system_names=a)
    context_engine.invalidate_context_cache()

    assert calls == [["current_date"], ["company_name"]]


def test_refs_refuse_an_unread_default_list():
    with pytest.raises(RuntimeError, match="resolved"):
        SystemContextNames.platform_defaults().refs()
