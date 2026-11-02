"""data.map_template + text.render_list — the generic list-shaping pair.

These two nodes exist because the data.transform sandbox deliberately has no
loops/calls: reshaping a list (for fan-out or agent variables) and rendering
a list into an LLM-ready text block were impossible without custom nodes.

Verifies:
    1. map_template: $item projection, $in enrichment from other inputs,
       require_path filtering, limit as a mappable input, miss → parks.
    2. render_list: {path} interpolation, header/separator/empty_text,
       max_items + max_chars_per_item bounding, missing path renders ''.
    3. control.map payload_template '$in.' refs (shared mini-language).
"""

from __future__ import annotations

from typing import Any

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.nodes.data.map_template import (
    MapTemplateConfig,
    MapTemplateExecutor,
    MapTemplateInput,
)
from matrx_graph.nodes.text.render_list import (
    RenderListConfig,
    RenderListExecutor,
    RenderListInput,
)

from tests._fixtures import FakeEmitter, make_app_context


async def _exec_map_template(inputs: dict[str, Any], config: dict[str, Any]) -> Any:
    result = await MapTemplateExecutor().execute(
        None,  # ctx unused
        MapTemplateInput.model_validate(inputs),
        MapTemplateConfig.model_validate(config),
    )
    assert result.status == "success", result
    return result.result


async def _exec_render_list(inputs: dict[str, Any], config: dict[str, Any]) -> Any:
    result = await RenderListExecutor().execute(
        None,
        RenderListInput.model_validate(inputs),
        RenderListConfig.model_validate(config),
    )
    assert result.status == "success", result
    return result.result


async def test_map_template_projects_items():
    out = await _exec_map_template(
        {"items": [{"url": "u1", "t": "a"}, {"url": "u2", "t": "b"}]},
        {"template": "$item.url"},
    )
    assert out.values == ["u1", "u2"]
    assert out.count == 2
    assert out.dropped == 0


async def test_map_template_enriches_from_in_namespace():
    out = await _exec_map_template(
        {
            "items": [{"title": "T1", "text": "body1"}],
            "topic": "quantum computing",
        },
        {
            "template": {
                "page_title": "$item.title",
                "page_content": "$item.text",
                "topic": "$in.topic",
            }
        },
    )
    assert out.values == [
        {"page_title": "T1", "page_content": "body1", "topic": "quantum computing"}
    ]


async def test_map_template_require_path_and_limit():
    pages = [
        {"url": "u1", "text": "good"},
        {"url": "u2", "text": ""},
        {"url": "u3", "text": "also good"},
        {"url": "u4", "text": "third good"},
    ]
    out = await _exec_map_template(
        {"items": pages, "limit": 2},
        {"template": "$item.url", "require_path": "text"},
    )
    assert out.values == ["u1", "u3"]
    assert out.dropped == 2


async def test_render_list_formats_and_bounds():
    out = await _exec_render_list(
        {
            "items": [
                {"title": "A", "url": "ua", "description": "x" * 50},
                {"title": "B", "url": "ub", "description": "short"},
                {"title": "C", "url": "uc", "description": "dropped by max_items"},
            ]
        },
        {
            "item_template": "- {title} ({url}): {description}",
            "separator": "\n",
            "header": "Sources:\n",
            "max_items": 2,
            "max_chars_per_item": 10,
        },
    )
    assert out.text.startswith("Sources:\n- A (ua): xxxxxxxxxx…")
    assert "- B (ub): short" in out.text
    assert "C (uc)" not in out.text
    assert out.rendered == 2
    assert out.truncated is True


async def test_render_list_missing_path_and_empty():
    out = await _exec_render_list(
        {"items": [{"a": 1}]},
        {"item_template": "{a}|{missing.path}|{item}"},
    )
    assert out.text == '1||{"a": 1}'

    empty = await _exec_render_list({"items": []}, {"item_template": "{a}", "empty_text": "(none)"})
    assert empty.text == "(none)"
    assert empty.rendered == 0


async def test_control_map_template_in_refs_flow_through_graph():
    received: list[dict[str, Any]] = []

    from typing import ClassVar

    from matrx_graph.types.context import NodeExecutionContext
    from matrx_graph.types.handle import HandleDirection, HandleSpec
    from matrx_graph.types.node_spec import NodeSpec
    from matrx_graph.types.primitives import ActionTier, NodeCategory
    from matrx_graph.types.result import NodeResult, success
    from pydantic import BaseModel, ConfigDict

    class _SinkInput(BaseModel):
        model_config = ConfigDict(extra="allow")

    class _SinkOutput(BaseModel):
        model_config = ConfigDict(extra="forbid")
        ok: bool = True

    class _SinkConfig(BaseModel):
        model_config = ConfigDict(extra="forbid")

    class _SinkExecutor:
        spec: ClassVar[NodeSpec] = NodeSpec(
            type="test.in_ref_sink",
            category=NodeCategory.DATA,
            display_name="Sink",
            description="Records payloads.",
            input_schema=_SinkInput,
            output_schema=_SinkOutput,
            config_schema=_SinkConfig,
            handles=(
                HandleSpec(id="in", direction=HandleDirection.INPUT),
                HandleSpec(id="out", direction=HandleDirection.OUTPUT),
            ),
            determinism=ActionTier.PURE,
        )

        async def execute(
            self,
            _ctx: NodeExecutionContext,
            inputs: _SinkInput,
            _config: _SinkConfig,
        ) -> NodeResult[_SinkOutput]:
            received.append(inputs.model_dump())
            return success(_SinkOutput())

    definition = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "fanout",
                    "type": "control.map",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "config": {
                            "target_node_id": "sink",
                            "payload_template": {
                                "keyword": "$item",
                                "topic": "$in.topic",
                            },
                        },
                        "input": {"items": ["k1", "k2"], "topic": "AI safety"},
                    },
                },
                {
                    "id": "sink",
                    "type": "test.in_ref_sink",
                    "position": {"x": 200, "y": 0},
                    "data": {"config": {}},
                },
            ],
            "edges": [],
            "entry_nodes": ["fanout"],
        }
    )
    registry = NodeRegistry()
    register_builtin_nodes(registry)
    registry.register(_SinkExecutor(), overwrite=True)
    graph = compile_graph(definition, registry=registry)
    scheduler = Scheduler(
        graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry
    )
    result = await scheduler.run(run_id="tmpl-in-refs")
    assert result.status is RunStatus.COMPLETED
    assert sorted((p["keyword"], p["topic"]) for p in received) == [
        ("k1", "AI safety"),
        ("k2", "AI safety"),
    ]
