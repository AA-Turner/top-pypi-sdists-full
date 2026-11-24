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


def test_every_column_the_follow_trigger_watches_is_followed_at_run_time() -> None:
    from matrx_ai.agents.follow_source import FOLLOWED_FIELDS, TRIGGER_WATCHED_FIELDS

    assert set(TRIGGER_WATCHED_FIELDS) <= set(FOLLOWED_FIELDS)


@pytest.mark.asyncio
async def test_a_following_copy_runs_the_sources_prompt_blocks_and_output_schema(manager) -> None:
    mgr, rows = manager
    schema = {"name": "brand_basics", "strict": True, "schema": {"type": "object", "properties": {}}}
    rows[SOURCE_ID] = _row(output_schema=schema, prompt_blocks=["source_block"])
    copy = _copy(follows=True)
    copy.output_schema = None
    copy.prompt_blocks = ["stale_block"]
    rows[COPY_ID] = copy

    config = await mgr.to_config(COPY_ID)

    assert config.config.prompt_blocks == ["source_block"]
    assert config.config.response_format == {"type": "json_schema", "json_schema": schema}


def test_a_following_copy_keeps_the_tools_it_was_born_with_beside_its_sources() -> None:
    """A template's assistant is born with ``records`` (``agent.duplicate_agent(..., p_add_tools)``, U7 follow-up): it
    stays following, and its run must still have the tool — the source's CURRENT tools, then the kept ones."""
    from matrx_ai.agents.follow_source import followed_row

    records, search, gone = "30cf4ddd-d9e6-4f43-af3a-595f467bd661", "tool-search", "tool-removed-from-source"
    source = _row(tools=[search])
    copy = _copy(follows=True)
    copy.tools = [gone, records]
    copy.metadata = {"follows_source_keeps_tools": [records]}

    assert followed_row(copy, source).tools == [search, records]  # a tool the source dropped does not come back

    plain = _copy(follows=True)
    plain.metadata = {}
    assert followed_row(plain, source).tools == [search]


# ── An archived agent named by id still runs (2026-11-08) ─────────────────────────────────────────
# One Archive (archived-items law item 5, Arman 2026-11-05) keeps ``is_archived`` and ``deleted_at``
# as ONE state: the ``zz_archive_states_agree_*`` triggers on ``agent.definition`` stamp
# ``deleted_at`` on every archived agent, at birth too. ``to_config`` refused any row with
# ``deleted_at`` set, so every agent saved archived (a build's draft until it passes, a proof
# scaffold, a version kept for history) answered ``agent_not_found`` the moment a step ran it by id
# (workflow runs 99515d5b / 6d966d09). Archived stays out of lists, pickers and default resolution;
# a reference that names it resolves. Only an id with no row is "not found".


def _archived(row: SimpleNamespace) -> SimpleNamespace:
    row.is_archived = True
    row.deleted_at = datetime(2026, 11, 8, 20, 40, tzinfo=UTC)
    return row


@pytest.mark.asyncio
async def test_an_archived_agent_run_by_id_loads(manager) -> None:
    mgr, rows = manager
    rows[SOURCE_ID] = _archived(_row())

    config = await mgr.to_config(SOURCE_ID)

    assert "Source instructions v5." in _system_text(config)


@pytest.mark.asyncio
async def test_a_copy_following_an_archived_source_still_follows_it(manager) -> None:
    mgr, rows = manager
    rows[SOURCE_ID] = _archived(_row())
    rows[COPY_ID] = _copy(follows=True)

    config = await mgr.to_config(COPY_ID)

    assert "Source instructions v5." in _system_text(config)


@pytest.mark.asyncio
async def test_an_agent_with_no_row_is_still_not_found(manager) -> None:
    from matrx_orm.exceptions import DoesNotExist

    mgr, _rows = manager
    with pytest.raises(DoesNotExist):
        await mgr.to_config("09f0e23c-d9f0-445f-a589-172d44ecd435")
