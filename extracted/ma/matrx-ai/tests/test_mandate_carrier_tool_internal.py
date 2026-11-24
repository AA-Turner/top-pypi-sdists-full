"""A tool's own provider call (tool-upkeep image/TTS probe) is lawful tool-internal spend, not a bypass.

Live 2026-11-16: tool_upkeep probes of grok-imagine-image and gpt-4o-mini-tts filed ``no_mandate_carrier``.
An app-code AI call with no Holder and no tool-internal reason stays a bypass.
"""

from __future__ import annotations

from typing import Any

import pytest
from matrx_connect import AppContext
from matrx_connect.emitters.console_emitter import ConsoleEmitter

from matrx_ai import _ext
from matrx_ai.orchestrator import mandate_carrier
from matrx_ai.orchestrator.mandate_carrier import (
    MANDATE_BYPASS_KIND,
    TOOL_INTERNAL_CARRIER,
    TOOL_INTERNAL_METADATA_KEY,
    carrier_for,
    note_mandate_carrier,
)


class _Config:
    model = "grok-imagine-image"


@pytest.fixture
def recorded(monkeypatch) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    monkeypatch.setitem(_ext._registry, "record_error", lambda exc, **kw: rows.append({"exc": exc, **kw}))
    ctx = AppContext(emitter=ConsoleEmitter("test", accumulate=False), source_feature="tool_upkeep")
    monkeypatch.setattr(mandate_carrier, "_context", lambda: ctx)
    mandate_carrier.reset_reported_signatures()
    yield rows
    mandate_carrier.reset_reported_signatures()


def test_tool_upkeep_probe_is_lawful_with_its_reason(recorded) -> None:
    md = {TOOL_INTERNAL_METADATA_KEY: "tools.upkeep"}
    assert carrier_for(md) == (TOOL_INTERNAL_CARRIER, "tools.upkeep")
    assert note_mandate_carrier(_Config(), md) is None
    assert recorded == []


def test_app_code_agent_run_without_mandate_is_still_a_bypass(recorded) -> None:
    assert carrier_for({"feature": "tool_call_generation"}) is None
    assert note_mandate_carrier(_Config(), {"feature": "x"}) is not None
    assert [r["kind"] for r in recorded] == [MANDATE_BYPASS_KIND]
    assert note_mandate_carrier(_Config(), {TOOL_INTERNAL_METADATA_KEY: "  "}) is not None
