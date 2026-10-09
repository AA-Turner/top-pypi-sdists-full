"""A stored tool id whose tool was deactivated is dropped and announced, never sent.

Agents store tools as ``tool.definition`` ids; the loaded registry holds active
tools only. ``fetch_url_as_markdown`` was deactivated on 2026-10-07 while the
"Director" agent still listed it, so every Repo Analyzer run failed at the
provider boundary with an engineering message shown to visitors (Applet audit
2026-10-09). The edge now removes ids that resolve to no live tool.
"""

from __future__ import annotations

import pytest

from matrx_ai.tools.merge import canonical_tool_names, drop_retired_tool_ids
from matrx_ai.tools.registry import ToolRegistry

LIVE_ID = "55bc14b4-a166-4a33-a0bc-a2b0dcf66de0"
RETIRED_ID = "5654f4ef-ef37-4150-85fb-cb36f3a5389e"


def _registry(monkeypatch: pytest.MonkeyPatch, *, loaded: bool) -> ToolRegistry:
    fresh = ToolRegistry()
    fresh.ensure_registered("web", description="unified web tool", tool_id=LIVE_ID)
    fresh._loaded = loaded
    monkeypatch.setattr(ToolRegistry, "get_instance", classmethod(lambda cls: fresh))
    return fresh


def test_retired_id_is_dropped_and_returned(monkeypatch: pytest.MonkeyPatch) -> None:
    _registry(monkeypatch, loaded=True)
    kept, retired = drop_retired_tool_ids(canonical_tool_names([LIVE_ID, RETIRED_ID]))
    assert kept == ["web"]
    assert retired == [RETIRED_ID]


def test_names_and_live_ids_are_untouched(monkeypatch: pytest.MonkeyPatch) -> None:
    _registry(monkeypatch, loaded=True)
    kept, retired = drop_retired_tool_ids(canonical_tool_names(["web", "custom_tool_1"]))
    assert kept == ["web", "custom_tool_1"]
    assert retired == []


def test_unloaded_registry_drops_nothing(monkeypatch: pytest.MonkeyPatch) -> None:
    # An unloaded registry is a wiring gap the boundary guard must keep reporting.
    fresh = ToolRegistry()
    monkeypatch.setattr(ToolRegistry, "get_instance", classmethod(lambda cls: fresh))
    kept, retired = drop_retired_tool_ids([RETIRED_ID])
    assert kept == [RETIRED_ID]
    assert retired == []
