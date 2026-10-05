"""A template copy with follows_source runs its SOURCE's current content (templates7_b).

Drives the real ``AgxDefinitionManager.to_config`` — the one door every run's
``agx.load_for_execution`` reaches for a definition row — with the row loads stubbed.
"""

from __future__ import annotations

from datetime import UTC, datetime
from types import SimpleNamespace
from typing import Any

import pytest

SOURCE_ID = "4cd676c6-f55d-4426-b7eb-a9d0273566ec"
COPY_ID = "1b7a9c1e-0000-4000-8000-000000000001"
MODEL_SOURCE = "617abdcd-79e2-4a4b-be76-4a9960cdffa1"
MODEL_COPY = "00000000-0000-4000-8000-0000000000aa"


def _row(**over: Any) -> SimpleNamespace:
    base: dict[str, Any] = dict(
        id=SOURCE_ID,
        name="Answers From Your Tables",
        description="",
        version=5,
        updated_at=datetime(2026, 10, 4, tzinfo=UTC),
        model_id=MODEL_SOURCE,
        messages=[{"role": "system", "content": [{"type": "text", "text": "Source instructions v5."}]}],
        settings={},
        tools=[],
        custom_tools=[],
        mcp_servers=[],
        variable_definitions=[
            {"name": "primary_table", "defaultValue": None, "required": True},
            {"name": "related_tables", "defaultValue": None},
        ],
        context_policies=[],
        auto_context_disabled=False,
        tool_config={},
        output_schema=None,
        matrx_actions={},
        skill_config={},
        model_tiers=None,
        source_agent_id=None,
        follows_source=False,
        deleted_at=None,
    )
    base.update(over)
    return SimpleNamespace(**base)


def _copy(follows: bool) -> SimpleNamespace:
    return _row(
        id=COPY_ID,
        name="Salon bookings answers",
        version=1,
        model_id=MODEL_COPY,
        messages=[{"role": "system", "content": [{"type": "text", "text": "Stale copied instructions."}]}],
        variable_definitions=[
            {"name": "primary_table", "defaultValue": "tbl-bookings", "required": True},
            {"name": "related_tables", "defaultValue": ["tbl-clients"]},
        ],
        source_agent_id=SOURCE_ID,
        follows_source=follows,
    )


def _system_text(config: Any) -> str:
    return str(config.config.system_instruction.base_instruction)


@pytest.fixture
def manager(monkeypatch: pytest.MonkeyPatch):
    from matrx_ai.db._agx_manager_impl import AgxDefinitionManager

    rows: dict[str, Any] = {}
    mgr = AgxDefinitionManager()

    async def load_by_id(item_id: Any) -> Any:
        return rows[str(item_id)]

    async def load_by_id_or_none(item_id: Any) -> Any:
        return rows.get(str(item_id))

    monkeypatch.setattr(mgr, "load_by_id", load_by_id)
    monkeypatch.setattr(mgr, "load_by_id_or_none", load_by_id_or_none)
    return mgr, rows


@pytest.mark.asyncio
async def test_a_following_copy_runs_the_sources_instructions_and_model_with_its_own_tables(manager) -> None:
    mgr, rows = manager
    rows[SOURCE_ID] = _row()
    rows[COPY_ID] = _copy(follows=True)

    config = await mgr.to_config(COPY_ID)

    assert "Source instructions v5." in _system_text(config)
    assert "Stale copied instructions." not in _system_text(config)
    assert config.config.model == MODEL_SOURCE
    assert config.variable_defaults["primary_table"].default_value == "tbl-bookings"
    assert config.variable_defaults["related_tables"].default_value == ["tbl-clients"]


@pytest.mark.asyncio
async def test_a_customized_copy_runs_its_own_content(manager) -> None:
    mgr, rows = manager
    rows[SOURCE_ID] = _row()
    rows[COPY_ID] = _copy(follows=False)

    config = await mgr.to_config(COPY_ID)

    assert "Stale copied instructions." in _system_text(config)
    assert config.config.model == MODEL_COPY


@pytest.mark.asyncio
async def test_a_copy_whose_source_is_gone_runs_its_own_content(manager) -> None:
    mgr, rows = manager
    rows[COPY_ID] = _copy(follows=True)

    config = await mgr.to_config(COPY_ID)

    assert "Stale copied instructions." in _system_text(config)


def test_a_source_variable_the_copy_lacks_arrives_and_its_own_bindings_win() -> None:
    from matrx_ai.agents.follow_source import merge_variable_definitions

    merged = merge_variable_definitions(
        [{"name": "primary_table", "defaultValue": None, "label": "Table"}, {"name": "tone", "defaultValue": "plain"}],
        [{"name": "primary_table", "defaultValue": "tbl-1", "binding": {"kind": "merge_field"}}],
    )
    assert merged == [
        {"name": "primary_table", "defaultValue": "tbl-1", "label": "Table", "binding": {"kind": "merge_field"}},
        {"name": "tone", "defaultValue": "plain"},
    ]
