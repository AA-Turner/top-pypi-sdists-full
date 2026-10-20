"""An organization's own value for a System item wins over the platform default (defect 5).

PB-01 check S12 (common-docs operations/real-tests/core-chain): an agent variable bound to the
System item ``company_name`` must render the RUN's organization's own value ("Tidewater Compass
Movers") instead of the platform value ("AI Matrx"); a second organization with no value of its
own still gets "AI Matrx". The override lives in ``context.system_context_item_org_value``
(written through ``custom.context_value_write`` with ``organization_id`` and no ``scope_id``) and
is applied in ``agent_context_from_resolved`` — the one body every resolver answer passes through
(run, dry run, preview, compare) — with the organization the run is admitted for.

Order of supply: a scope item sharing the key still beats System (ruling 13 of the scopes STATE),
an ambient (computed) item is always computed, and otherwise organization value → System default.
"""

from __future__ import annotations

import copy
from typing import Any

import pytest

from matrx_ai import context_engine
from matrx_ai.context_engine import SystemContextNames, agent_context_from_resolved

COMPANY_ID = "11b7b942-d604-4d7a-9566-571865f121ed"
DATE_ID = "11111111-1111-4111-8111-111111111111"
SCOPE_COMPANY_ID = "55555555-5555-4555-8555-555555555555"
TIDEWATER_ORG = "226be635-194d-42dd-87c8-7a9562f70939"
WORKSPACE_ORG = "884d1ce8-7b49-4fba-a2f3-0f7dd7c83d4f"
ENTITY_ORG = "99999999-9999-4999-8999-999999999999"

OVERRIDES: dict[str, dict[str, Any]] = {
    TIDEWATER_ORG: {COMPANY_ID: "Tidewater Compass Movers", DATE_ID: "1999-01-01"},
}


def _system_cell(key: str, item_id: str, value: Any) -> dict[str, Any]:
    return {
        "key": key, "value": value, "type": "string", "context_item_id": item_id,
        "scope_id": None, "scope_name": "System", "scope_type_id": None, "source": "system",
    }


def _entry(cell: dict[str, Any], cells: list[dict[str, Any]]) -> dict[str, Any]:
    return {"value": cell["value"], "type": "string", "inject_as": "direct",
            "source": cell["source"], "cells": cells}


def _resolved(*, scope_company: bool = False, entity_org: str | None = None) -> dict[str, Any]:
    company = _system_cell("company_name", COMPANY_ID, "AI Matrx")
    date = _system_cell("current_date", DATE_ID, "placeholder")
    variables = {"company_name": _entry(company, [company]), "current_date": _entry(date, [date])}
    cell_values: dict[str, Any] = {COMPANY_ID: [company], DATE_ID: [date]}
    if scope_company:
        scope_cell = {
            "key": "company_name", "value": "Castellano & Reyes, LLP", "type": "string",
            "context_item_id": SCOPE_COMPANY_ID, "scope_id": "66666666-6666-4666-8666-666666666666",
            "scope_name": "Meridian", "scope_type_id": "77777777-7777-4777-8777-777777777777",
            "source": "scope:Meridian",
        }
        variables["company_name"] = _entry(scope_cell, [company, scope_cell])
        cell_values[SCOPE_COMPANY_ID] = [scope_cell]
    return {
        "variables": variables,
        "context": {"organization_id": entity_org} if entity_org else {},
        "scope_labels": {},
        "cell_values": cell_values,
    }


@pytest.fixture(autouse=True)
def _isolated(monkeypatch):
    monkeypatch.setattr(context_engine, "_merge_producer", None)
    monkeypatch.setattr(context_engine, "_defaults_reader", None, raising=False)

    async def person_timezone(user_id, organization_id):
        return "UTC"

    monkeypatch.setattr(context_engine, "person_timezone", person_timezone, raising=False)
    monkeypatch.setattr(
        context_engine, "_ambient_providers",
        lambda user_id, timezone="UTC": {"current_date": lambda: "computed:current_date"},
    )


@pytest.fixture
def reads(monkeypatch):
    """The organization-value reader stood in; reads[] = the organizations it was asked for."""
    asked: list[Any] = []

    async def organization_system_values(organization_id):
        asked.append(organization_id)
        return dict(OVERRIDES.get(str(organization_id), {}))

    monkeypatch.setattr(context_engine, "organization_system_values", organization_system_values, raising=False)
    return asked


NAMED = SystemContextNames.none().naming([COMPANY_ID, DATE_ID], by="the agent's variable company_name")


async def _build(org: str | None, **kw: Any):
    return await agent_context_from_resolved(
        "user-1", copy.deepcopy(_resolved(**kw)), entity_type="conversation", entity_id="c-1",
        system_names=NAMED, organization_id=org,
    )


async def test_the_runs_organization_value_wins_over_the_platform_default(reads):
    ctx = await _build(TIDEWATER_ORG)

    assert ctx.direct_variables["company_name"]["value"] == "Tidewater Compass Movers"
    assert ctx.cells_by_item_id[COMPANY_ID][0]["value"] == "Tidewater Compass Movers"
    block = ctx.build_system_prompt_block()
    assert "Tidewater Compass Movers" in block
    assert "AI Matrx" not in block
    assert reads == [TIDEWATER_ORG]


async def test_an_organization_without_its_own_value_gets_the_platform_default(reads):
    ctx = await _build(WORKSPACE_ORG)

    assert ctx.direct_variables["company_name"]["value"] == "AI Matrx"
    assert ctx.cells_by_item_id[COMPANY_ID][0]["value"] == "AI Matrx"


async def test_the_run_organization_is_asked_before_the_entitys(reads):
    await _build(TIDEWATER_ORG, entity_org=ENTITY_ORG)
    assert reads == [TIDEWATER_ORG]


async def test_with_no_run_organization_the_entitys_organization_is_asked(reads):
    ctx = await _build(None, entity_org=TIDEWATER_ORG)
    assert reads == [TIDEWATER_ORG]
    assert ctx.direct_variables["company_name"]["value"] == "Tidewater Compass Movers"


async def test_a_scope_item_sharing_the_key_still_beats_the_organization_value(reads):
    ctx = await _build(TIDEWATER_ORG, scope_company=True)

    assert ctx.direct_variables["company_name"]["value"] == "Castellano & Reyes, LLP"
    # the System cell itself carries the organization's value
    assert ctx.cells_by_item_id[COMPANY_ID][0]["value"] == "Tidewater Compass Movers"


async def test_an_ambient_item_is_always_computed(reads):
    ctx = await _build(TIDEWATER_ORG)
    assert ctx.direct_variables["current_date"]["value"] == "computed:current_date"


async def test_the_host_reader_is_what_answers_and_an_unbound_reader_means_platform_values():
    asked: list[str] = []

    async def reader(organization_id: str) -> dict[str, Any]:
        asked.append(organization_id)
        return dict(OVERRIDES.get(organization_id, {}))

    context_engine.configure_organization_system_values(reader)
    try:
        ctx = await _build(TIDEWATER_ORG)
        assert ctx.direct_variables["company_name"]["value"] == "Tidewater Compass Movers"
        await _build(TIDEWATER_ORG)  # the second turn inside the TTL reads nothing
        assert asked == [TIDEWATER_ORG]
    finally:
        context_engine.configure_organization_system_values(None)
    ctx = await _build(TIDEWATER_ORG)
    assert ctx.direct_variables["company_name"]["value"] == "AI Matrx"
