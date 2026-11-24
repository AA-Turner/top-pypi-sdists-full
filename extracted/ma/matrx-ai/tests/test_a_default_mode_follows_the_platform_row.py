"""A default mode the maker has not edited follows the platform row (Understanding v2, D14).

The agent stores ``{key, source}``; when a conversation's configuration is fixed (the first turn, with the declared
prompt blocks), the row's label / description / content become the mode's name / description / instructions, read
through the prompt-block host seam. The conversation keeps them (D12). A missing row leaves the mode out and is
captured, never replaced by text in code.

Fails when: a sourced mode is not filled from its row; an edited mode (no source) is touched; a missing row is
silent or gets fallback text; a continued conversation re-reads the row.
"""

from __future__ import annotations

import pytest

from matrx_ai.config import UnifiedConfig
from matrx_ai.config.agent_modes import modes_need_resolving, render_block, resolve_agent_modes
from matrx_ai.prompt_blocks import resolve_declared_blocks
from matrx_ai.prompt_blocks.models import BlockRow


class _Source:
    def __init__(self, rows: list[BlockRow]) -> None:
        self.rows = rows
        self.asked: list[list[str]] = []

    async def candidates(self, names, *, organization_id, personal_user_id):
        self.asked.append(list(names))
        return [r for r in self.rows if r.name in names]

    async def skill(self, skill_id):
        return None

    async def model_facts(self, model):
        return None

    async def personal_rung_enabled(self, organization_id):
        return False


DISCOVERY_ROW = BlockRow(
    id="b1", name="agent_mode_discovery", level="system", content="Keep asking until everything is known.",
    label="Discovery", description="Learn from the person first.",
)


def _config(modes: list[dict]) -> UnifiedConfig:
    config = UnifiedConfig.from_dict({"model": "m", "messages": [], "agent_modes": modes})
    return config


@pytest.fixture
def captured(monkeypatch: pytest.MonkeyPatch) -> list[dict]:
    rows: list[dict] = []

    async def record_error(exc, **kwargs):
        rows.append(kwargs)

    monkeypatch.setattr("matrx_ai._ext.get_ext", lambda name: record_error)
    return rows


@pytest.mark.asyncio
async def test_a_sourced_mode_takes_the_rows_text_and_an_edited_one_is_untouched(captured) -> None:
    mine = {"key": "answer", "name": "Answer", "description": "mine", "instructions": "My words."}
    config = _config([{"key": "discovery", "source": "agent_mode_discovery"}, mine])
    assert modes_need_resolving(config)
    await resolve_declared_blocks(config, runner_id=None, organization_id="org-1", source=_Source([DISCOVERY_ROW]))
    discovery, answer = config.agent_modes
    assert (discovery["name"], discovery["description"], discovery["instructions"]) == (
        "Discovery", "Learn from the person first.", "Keep asking until everything is known.",
    )
    assert discovery["source"] == "agent_mode_discovery"
    assert {k: answer[k] for k in mine} == mine and "source" not in answer
    block = render_block(config.agent_modes, None) or ""
    assert "- Discovery — Learn from the person first." in block and "Keep asking until everything is known." in block
    assert not modes_need_resolving(config) and captured == []


@pytest.mark.asyncio
async def test_a_continued_conversation_keeps_the_text_it_started_with(captured) -> None:
    config = _config([{"key": "discovery", "source": "agent_mode_discovery"}])
    await resolve_agent_modes(config, organization_id=None, source=_Source([DISCOVERY_ROW]))
    stored = config.to_storage_dict()["config"]
    restored = UnifiedConfig.from_dict({"model": "m", "messages": [], **stored})
    later = _Source([BlockRow(id="b1", name="agent_mode_discovery", level="system", content="EDITED", label="X")])
    await resolve_agent_modes(restored, organization_id=None, source=later)
    assert later.asked == [] and restored.agent_modes[0]["instructions"] == "Keep asking until everything is known."


@pytest.mark.asyncio
async def test_a_missing_row_leaves_the_mode_out_and_is_captured(captured) -> None:
    config = _config([{"key": "planning", "source": "agent_mode_planning"}, {"key": "x", "name": "X"}])
    missing = await resolve_agent_modes(config, organization_id=None, source=_Source([]))
    assert missing == ["agent_mode_planning"]
    assert [m["key"] for m in config.agent_modes] == ["x"]
    assert [r["kind"] for r in captured] == ["agent_mode_default_missing"]
