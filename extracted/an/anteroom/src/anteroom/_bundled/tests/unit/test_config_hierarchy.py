"""Tests for config hierarchy visualization service."""

from __future__ import annotations

from dataclasses import dataclass, field

from anteroom.services.config_explanation import ConfigExplanationContext
from anteroom.services.config_hierarchy import build_config_hierarchy, hierarchy_to_dict


@dataclass
class _References:
    instructions: list[str] = field(default_factory=lambda: ["ANTEROOM.md"])
    rules: list[str] = field(default_factory=lambda: ["rules/security.md"])
    skills: list[str] = field(default_factory=lambda: ["skills/review"])


@dataclass
class _Cli:
    builtin_tools: bool = True


@dataclass
class _McpServer:
    name: str = "filesystem"
    transport: str = "stdio"
    enabled: bool = True


@dataclass
class _Config:
    ai: dict[str, str] = field(default_factory=lambda: {"model": "gpt-4o"})
    references: _References = field(default_factory=_References)
    cli: _Cli = field(default_factory=_Cli)
    mcp_servers: list[_McpServer] = field(default_factory=lambda: [_McpServer()])


def test_build_config_hierarchy_counts_layers_and_related_inputs() -> None:
    context = ConfigExplanationContext(
        config=_Config(),
        layer_raws={
            "team": {"ai": {"model": "gpt-4o-mini"}, "required": [{"path": "ai.api_key"}]},
            "personal": {"ai": {"model": "gpt-4o"}},
        },
        source_map={"ai.model": "personal"},
        enforced_fields=["ai.api_key"],
        working_dir="/tmp/project",
    )
    hierarchy = build_config_hierarchy(
        context=context,
    )

    by_layer = {layer.name: layer for layer in hierarchy.layers}
    assert by_layer["team"].active is True
    assert by_layer["personal"].winning_key_count == 1
    assert hierarchy.required_fields[0].name == "ai.api_key"
    assert hierarchy.required_fields[0].detail.startswith("missing")
    assert any(item.name == "ai.model" and item.source == "personal" for item in hierarchy.key_settings)
    assert hierarchy.references[0].kind == "instruction"
    assert hierarchy.skills
    assert hierarchy.mcp_servers[0].name == "filesystem"
    assert hierarchy.tools[0].name == "builtin_tools"
    assert any(item.name == "approval_mode" for item in hierarchy.tools)


def test_hierarchy_json_is_serializable_shape() -> None:
    context = ConfigExplanationContext(
        config=_Config(),
        layer_raws={},
        source_map={},
        enforced_fields=[],
    )
    hierarchy = build_config_hierarchy(
        context=context,
    )
    payload = hierarchy_to_dict(hierarchy)
    assert "layers" in payload
    assert "key_settings" in payload
    assert "skills" in payload
    assert payload["final_key_count"] > 0
