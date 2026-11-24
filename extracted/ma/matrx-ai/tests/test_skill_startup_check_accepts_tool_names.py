"""Feedback 2c3a1b35: a skill naming an ACTIVE tool by name (SKILL.md frontmatter
``allowed_tools: [kindcomp_preview]``) is valid — the runtime resolves names — so
the startup check must not file it as an invalid UUID on every boot. An unknown
name is still reported."""

from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

import pytest

from matrx_ai.skills import startup_check


class _Mgr:
    def __init__(self, rows):
        self._rows = rows

    async def filter_items(self, **_kw):
        return self._rows


@pytest.mark.asyncio
async def test_active_tool_name_is_valid_and_unknown_name_is_not(monkeypatch):
    tool = SimpleNamespace(id=uuid4(), name="kindcomp_preview")
    skills = [
        SimpleNamespace(id=uuid4(), skill_id="shape-authoring", allowed_tools=["kindcomp_preview"]),
        SimpleNamespace(id=uuid4(), skill_id="broken", allowed_tools=["no_such_tool"]),
    ]
    import matrx_ai.db._registry as reg
    import matrx_ai.tools.tool_def_db as tdd

    monkeypatch.setattr(reg, "get_instance", lambda _name: _Mgr(skills))
    monkeypatch.setattr(tdd, "get_tool_def_manager", lambda: _Mgr([tool]))

    report = await startup_check.validate_allowed_tools_on_startup(strict=False)

    assert report["invalid_uuid"] == [{"skill_id": "broken", "value": "no_such_tool"}]
    assert report["missing"] == []
