"""Kind-filtered edges, fan-out modes, and kind-triggered nodes — end to end.

Every test here runs the REAL scheduler over a REAL compiled graph. The
behaviors pinned are Arman's rulings (plan of record §7.3/§7.4/§7.7c):

* an edge declares "carry `web_result` instances" and the engine draws them out
  of whatever the source produced, however nested;
* an edge whose kind never appears simply does not fire — a conditional
  downstream path with zero custom code;
* fan-out is `all` by DEFAULT (the whole list to one invocation) and `each` is
  a deliberate, visible authoring choice — never implicit parallelism;
* a node connected to NOTHING fires when its kind appears anywhere in the run,
  at any depth, and it does not fire at step 1 on nothing (the entry-node trap).
"""

from __future__ import annotations

from typing import Any, ClassVar

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.content_ir.model import KindModel
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from matrx_graph.validation import validate_definition
from pydantic import BaseModel, ConfigDict, JsonValue

from tests._fixtures import FakeEmitter, make_app_context


class Rating(KindModel, kind="rating"):
    value: float


class WebResult(KindModel, kind="web_result"):
    url: str
    rating: Rating | None = None


class NewsResult(KindModel, kind="news_result"):
    headline: str


# ---------------------------------------------------------------------------
# Two spy nodes: one produces a sectioned payload, one records what it received
# ---------------------------------------------------------------------------


class _SourceInput(BaseModel):
    model_config = ConfigDict(extra="allow")


class _SourceOutput(BaseModel):
    model_config = ConfigDict(extra="allow")

    query: str = ""
    web: list[JsonValue] = []
    news: list[JsonValue] = []


class _EmptyConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")


class _Source:
    """Emits a sectioned search payload — the real pilot shape, not a flat list."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.kind_source",
        category=NodeCategory.DATA,
        display_name="Kind source",
        description="Emits a sectioned kind payload.",
        input_schema=_SourceInput,
        output_schema=_SourceOutput,
        config_schema=_EmptyConfig,
        handles=(HandleSpec(id="out", direction=HandleDirection.OUTPUT),),
        determinism=ActionTier.PURE,
    )

    def __init__(self, web: int = 2, news: int = 1) -> None:
        self._web, self._news = web, news

    async def execute(
        self, _ctx: NodeExecutionContext, _inputs: _SourceInput, _config: _EmptyConfig
    ) -> NodeResult[_SourceOutput]:
        return success(
            _SourceOutput(
                query="pizza",
                web=[
                    WebResult(url=f"w{i}", rating=Rating(value=float(i))).model_dump()
                    for i in range(self._web)
                ],
                news=[NewsResult(headline=f"n{i}").model_dump() for i in range(self._news)],
            )
        )


class _SinkInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    value: JsonValue = None


class _SinkOutput(BaseModel):
    model_config = ConfigDict(extra="allow")

    seen: JsonValue = None


class _Sink:
    """Records every invocation — how many, and with what."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.kind_sink",
        category=NodeCategory.DATA,
        display_name="Kind sink",
        description="Records what it was handed.",
        input_schema=_SinkInput,
        output_schema=_SinkOutput,
        config_schema=_EmptyConfig,
        handles=(HandleSpec(id="in", direction=HandleDirection.INPUT),),
        determinism=ActionTier.PURE,
    )

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def execute(
        self, _ctx: NodeExecutionContext, inputs: _SinkInput, _config: _EmptyConfig
    ) -> NodeResult[_SinkOutput]:
        self.calls.append(inputs.model_dump())
        return success(_SinkOutput(seen=inputs.value))


def _registry(web: int = 2, news: int = 1) -> tuple[NodeRegistry, _Source, _Sink]:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    source, sink = _Source(web=web, news=news), _Sink()
    reg.register(source, overwrite=True)
    reg.register(sink, overwrite=True)
    return reg, source, sink


def _definition(
    edge_data: dict[str, Any], *, sink_data: dict[str, Any] | None = None
) -> Definition:
    return Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "source",
                    "type": "test.kind_source",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {}},
                },
                {
                    "id": "sink",
                    "type": "test.kind_sink",
                    "position": {"x": 200, "y": 0},
                    "data": {"config": {}, **(sink_data or {})},
                },
            ],
            "edges": [
                {
                    "id": "e1",
                    "source": "source",
                    "target": "sink",
                    "data": edge_data,
                }
            ],
        }
    )


# ---------------------------------------------------------------------------
# A source whose output is ONE list — the unambiguous `each`-without-a-filter
# case. Kept separate from _Source (which is deliberately multi-sectioned).
# ---------------------------------------------------------------------------


class _ListOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: list[JsonValue] = []


class _ListSource:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="test.list_source",
        category=NodeCategory.DATA,
        display_name="List source",
        description="Emits one list.",
        input_schema=_SourceInput,
        output_schema=_ListOutput,
        config_schema=_EmptyConfig,
        handles=(HandleSpec(id="out", direction=HandleDirection.OUTPUT),),
        determinism=ActionTier.PURE,
    )

    async def execute(
        self, _ctx: NodeExecutionContext, _inputs: _SourceInput, _config: _EmptyConfig
    ) -> NodeResult[_ListOutput]:
        return success(_ListOutput(items=["x", "y", "z"]))


def _list_registry() -> tuple[NodeRegistry, _Sink]:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    sink = _Sink()
    reg.register(_ListSource(), overwrite=True)
    reg.register(sink, overwrite=True)
    return reg, sink


def _list_definition(edge_data: dict[str, Any]) -> Definition:
    return Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "source",
                    "type": "test.list_source",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {}},
                },
                {
                    "id": "sink",
                    "type": "test.kind_sink",
                    "position": {"x": 200, "y": 0},
                    "data": {"config": {}},
                },
            ],
            "edges": [{"id": "e1", "source": "source", "target": "sink", "data": edge_data}],
        }
    )


async def _run(definition: Definition, registry: NodeRegistry, run_id: str):
    graph = compile_graph(definition, registry=registry)
    scheduler = Scheduler(
        graph, MemoryCheckpointer(), make_app_context(FakeEmitter()), registry=registry
    )
    return await scheduler.run(run_id=run_id)


# ---------------------------------------------------------------------------
# Kind-filtered edges (§7.3)
# ---------------------------------------------------------------------------


async def test_kind_filter_carries_only_that_kind_and_finds_it_nested():
    registry, _source, sink = _registry(web=2, news=1)
    result = await _run(_definition({"kind_filter": "web_result"}), registry, "filter-1")

    assert result.status is RunStatus.COMPLETED
    # ONE invocation (the `all` default), carrying both web results and no news.
    assert len(sink.calls) == 1
    carried = sink.calls[0]["value"]
    assert [v["url"] for v in carried] == ["w0", "w1"]
    assert all(v["__kind"] == "web_result" for v in carried)


async def test_a_filter_reaches_a_kind_nested_inside_another_kind():
    # `rating` is never a top-level field of the source's output — it lives
    # inside each web result. Routing is by what the payload IS, at any depth.
    registry, _source, sink = _registry(web=2)
    result = await _run(_definition({"kind_filter": "rating"}), registry, "filter-nested")
    assert result.status is RunStatus.COMPLETED
    assert [v["value"] for v in sink.calls[0]["value"]] == [0.0, 1.0]


async def test_an_edge_whose_kind_never_appears_does_not_fire():
    # THE conditional-path feature: zero custom code, and the target's join
    # releases instead of blocking forever.
    registry, _source, sink = _registry(web=0, news=0)
    result = await _run(_definition({"kind_filter": "web_result"}), registry, "filter-empty")
    assert result.status is RunStatus.COMPLETED
    assert sink.calls == []


# ---------------------------------------------------------------------------
# Fan-out modes (§7.4) — `all` is the ratified default
# ---------------------------------------------------------------------------


async def test_all_is_the_default_the_whole_list_to_one_invocation():
    registry, _source, sink = _registry(web=3)
    await _run(_definition({"kind_filter": "web_result"}), registry, "mode-default")
    assert len(sink.calls) == 1
    assert len(sink.calls[0]["value"]) == 3


async def test_each_is_opt_in_and_produces_one_invocation_per_instance():
    registry, _source, sink = _registry(web=3)
    result = await _run(
        _definition({"kind_filter": "web_result", "fan_out": "each"}), registry, "mode-each"
    )
    assert result.status is RunStatus.COMPLETED
    assert len(sink.calls) == 3
    assert sorted(c["value"]["url"] for c in sink.calls) == ["w0", "w1", "w2"]


async def test_each_delivers_under_the_authored_item_key():
    registry, _source, sink = _registry(web=2)
    await _run(
        _definition({"kind_filter": "web_result", "fan_out": "each", "item_key": "record"}),
        registry,
        "mode-each-key",
    )
    assert all("record" in call for call in sink.calls)


async def test_each_over_a_plain_list_needs_no_kind_filter():
    # §7.4's "a list[K] payload maps with an explicit edge mode": one list in
    # the payload, so `each` is unambiguous and needs no kind at all.
    registry, sink = _list_registry()
    result = await _run(_list_definition({"fan_out": "each"}), registry, "mode-each-list")
    assert result.status is RunStatus.COMPLETED
    assert sorted(c["value"] for c in sink.calls) == ["x", "y", "z"]


async def test_each_refuses_to_guess_when_the_payload_is_ambiguous():
    # The source emits TWO lists (web and news). Picking the first would be a
    # coin flip that silently fans a paid step over the wrong data, and
    # delivering the whole payload once would contradict what the author asked
    # for. So the edge REFUSES, by name, and says how to fix it.
    registry, _source, sink = _registry(web=2, news=1)
    result = await _run(_definition({"fan_out": "each"}), registry, "mode-each-ambiguous")
    assert result.status is RunStatus.ERRORED
    assert "fans out per item" in (result.error or "")
    assert sink.calls == []


async def test_malformed_fan_out_dies_at_compile_never_mid_run():
    registry, _source, _sink = _registry()
    definition = _definition({"kind_filter": "web_result", "fan_out": "eachh"})
    try:
        compile_graph(definition, registry=registry)
    except Exception as exc:  # CompilationError
        assert "fan_out" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("a typo in fan_out must not compile")


# ---------------------------------------------------------------------------
# Kind-triggered nodes (§7.7c)
# ---------------------------------------------------------------------------


def _trigger_definition(trigger_data: dict[str, Any]) -> Definition:
    """A source wired to a passthrough, plus a node wired to NOTHING."""
    return Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "source",
                    "type": "test.kind_source",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {}},
                },
                {
                    "id": "saver",
                    "type": "test.kind_sink",
                    "position": {"x": 200, "y": 200},
                    "data": {"config": {}, **trigger_data},
                },
            ],
            "edges": [],
        }
    )


async def test_a_node_wired_to_nothing_fires_when_its_kind_appears():
    # Arman's motivating case: streams generate kinds that must be persisted;
    # the trigger node saves them wherever they surfaced, with no wiring.
    registry, _source, sink = _registry(web=2)
    result = await _run(_trigger_definition({"trigger_kind": "web_result"}), registry, "trigger-1")
    assert result.status is RunStatus.COMPLETED
    assert len(sink.calls) == 1
    assert len(sink.calls[0]["value"]) == 2
    # A node connected to nothing must still answer "where did this come from?"
    assert sink.calls[0]["trigger_source_node_ids"] == ["source", "source"]
    assert sink.calls[0]["trigger_paths"] == ["web[0]", "web[1]"]


async def test_a_trigger_fires_on_a_deeply_nested_kind():
    registry, _source, sink = _registry(web=2)
    result = await _run(_trigger_definition({"trigger_kind": "rating"}), registry, "trigger-nested")
    assert result.status is RunStatus.COMPLETED
    assert [v["value"] for v in sink.calls[0]["value"]] == [0.0, 1.0]


async def test_each_mode_fires_once_per_instance():
    registry, _source, sink = _registry(web=3)
    await _run(
        _trigger_definition({"trigger_kind": "web_result", "trigger_mode": "each"}),
        registry,
        "trigger-each",
    )
    assert len(sink.calls) == 3


async def test_fire_once_fires_exactly_once():
    registry, _source, sink = _registry(web=3)
    await _run(
        _trigger_definition(
            {
                "trigger_kind": "web_result",
                "trigger_mode": "each",
                "trigger_fire_once": True,
            }
        ),
        registry,
        "trigger-once",
    )
    assert len(sink.calls) == 1


async def test_a_trigger_node_never_fires_on_nothing_at_step_one():
    # THE trap: a node with no incoming edges looks exactly like an entry node.
    registry, _source, sink = _registry(web=0, news=0)
    result = await _run(
        _trigger_definition({"trigger_kind": "web_result"}), registry, "trigger-entry"
    )
    assert result.status is RunStatus.COMPLETED
    assert sink.calls == []


def test_a_trigger_node_is_excluded_from_derived_entry_nodes():
    registry, _source, _sink = _registry()
    graph = compile_graph(_trigger_definition({"trigger_kind": "web_result"}), registry=registry)
    assert graph.entry_node_ids == ("source",)


def test_a_trigger_node_with_an_inbound_edge_is_a_validation_error():
    # A contradiction: two mechanisms would each try to open its firing.
    definition = _definition({}, sink_data={"trigger_kind": "web_result"})
    result = validate_definition(definition, registry=_registry()[0])
    assert result.valid is False
    assert any("trigger" in issue.message.lower() for issue in result.issues)


def test_a_malformed_trigger_declaration_is_a_validation_error():
    definition = _trigger_definition({"trigger_kind": "web_result", "trigger_mode": "sometimes"})
    result = validate_definition(definition, registry=_registry()[0])
    assert result.valid is False
