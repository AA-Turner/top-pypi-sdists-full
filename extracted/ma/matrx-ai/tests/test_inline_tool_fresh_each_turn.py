"""A client-delegated inline tool is read fresh every turn.

Incident (2026-10-04, Board side chat): turn 1 injected ``apply_surface_write``
with its per-turn "Available targets right now" description; the post-merge
config stayed in the process AgentCache; turn 2's fresh (different) definition
then raised ToolMergeError before the model ran. The request's definition must
REPLACE the remembered one; a real same-request clash must still raise.
"""

from __future__ import annotations

import pytest
from matrx_connect.context.app_context import AppContext

from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.tools.merge import ToolMergeError, merge_request_tools
from matrx_ai.tools.models import CustomTool
from matrx_ai.tools.specs import InlineToolSpec

SCHEMA = {"type": "object", "properties": {"target": {"type": "string"}}}


def _spec(description: str, name: str = "apply_surface_write") -> InlineToolSpec:
    return InlineToolSpec(name=name, description=description, input_schema=SCHEMA)


def _merge(config, specs):
    return merge_request_tools(
        config,
        AppContext(emitter=None, client_tools=[]),
        specs,
        active_executors=frozenset(),
    )


def _config(custom=None, authored=None) -> UnifiedConfig:
    cfg = UnifiedConfig(model="gpt-4.1-mini", messages=[], tools=[], custom_tools=custom or [])
    if authored is not None:
        cfg.authored_custom_tools = authored
    return cfg


def test_fresh_definition_replaces_remembered_one_from_prior_turn() -> None:
    cfg = _config()
    _merge(cfg, [_spec("Available targets right now: cell A1")])
    # turn 2 reuses the cached post-merge config
    _merge(cfg, [_spec("Available targets right now: nothing on the board")])
    mine = [t for t in cfg.custom_tools if t.name == "apply_surface_write"]
    assert len(mine) == 1
    assert "nothing on the board" in mine[0].description


def test_two_different_declarations_in_one_request_still_clash() -> None:
    with pytest.raises(ToolMergeError):
        _merge(_config(), [_spec("one"), _spec("two")])


def test_clash_with_agent_authored_inline_tool_still_raises() -> None:
    authored = [CustomTool(name="apply_surface_write", description="agent's own", input_schema=SCHEMA)]
    cfg = _config(custom=list(authored), authored=list(authored))
    with pytest.raises(ToolMergeError):
        _merge(cfg, [_spec("client's different one")])
