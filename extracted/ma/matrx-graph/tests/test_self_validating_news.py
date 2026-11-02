"""Structural + mocked-execution tests for the self-validating news example.

No real API calls or LLM calls here — those require env secrets and
aidream's full app context (the ``judge`` tier covers them). This file
verifies:

- The definition is well-formed (Pydantic validates the ReactFlow JSON).
- The map → worker → channel → gather fan-in is wired per engine
  semantics: the worker owns the channel write (``output_channel``) and
  gather is edge-triggered by the worker, never by the map node.
- The graph compiles given the expected actions are registered.
- A fully mocked scheduler run executes the whole chain and gather
  receives one entry per fanned-out URL.
"""

from __future__ import annotations

import pytest
from matrx_graph import (
    ActionRegistry,
    ActionTier,
    Definition,
    MemoryCheckpointer,
    NodeCategory,
    NodeRegistry,
    RunStatus,
    Scheduler,
    register_node,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.examples import build_self_validating_news_definition
from matrx_graph.types.result import NodeResult, success
from pydantic import BaseModel, ConfigDict

from tests._fixtures import FakeEmitter, make_app_context

# Every non-builtin action the definition references, with its category.
_EXTERNAL_ACTIONS: tuple[tuple[str, NodeCategory], ...] = (
    ("news.search", NodeCategory.DATA),
    ("text.extract_field", NodeCategory.DATA),
    ("web.brave.search", NodeCategory.IO),
    ("ai.llm.chat", NodeCategory.LLM),
    ("scraper.scrape", NodeCategory.IO),
    ("ai.util.format_scraped_content", NodeCategory.DATA),
)


def _registry_with_fakes() -> NodeRegistry:
    """Builtins + a permissive fake executor per external action."""
    nreg = NodeRegistry()
    areg = ActionRegistry()

    class _Inputs(BaseModel):
        model_config = ConfigDict(extra="allow")

    class _Outputs(BaseModel):
        model_config = ConfigDict(extra="allow")

    for name, category in _EXTERNAL_ACTIONS:

        @register_node(
            name=name,
            category=category,
            determinism=ActionTier.NON_DETERMINISTIC,
            input_schema=_Inputs,
            output_schema=_Outputs,
            node_registry=nreg,
            action_registry=areg,
        )
        async def _stub(_ctx, _inputs: _Inputs) -> NodeResult[_Outputs]:  # noqa: B023
            return success(_Outputs())

    register_builtin_nodes(nreg)
    return nreg


def test_definition_is_well_formed():
    definition = build_self_validating_news_definition()
    # Full 13-node chain
    assert len(definition.nodes) == 13
    node_ids = {n.id for n in definition.nodes}
    expected = {
        "headlines",
        "top_title",
        "web_search",
        "search_text",
        "rank_urls",
        "parse_urls",
        "fanout",
        "scrape_page",
        "gather_scrapes",
        "combine_pages",
        "summarize",
        "mix_decoys",
        "final_answer",
    }
    assert node_ids == expected

    # 11 edges, mix of data + control
    assert len(definition.edges) == 11
    kinds = {e.kind.value for e in definition.edges}
    assert "data" in kinds and "control" in kinds

    # One declared channel (scrapes)
    names = {c.name for c in definition.channels}
    assert names == {"scrapes"}

    # Entry node locked
    assert definition.entry_nodes == ["headlines"]


def test_fan_in_topology_matches_engine_semantics():
    """The map → gather fan-in must follow the two engine invariants.

    1. The WORKER owns the channel write: scrape_page carries
       data.output_channel="scrapes" (control.map only dispatches Sends —
       nothing else ever writes the channel).
    2. Gather is edge-triggered BY the worker, one super-step after the
       workers run, when their writes are committed. An edge from the map
       node would run gather in the same super-step as the workers, where
       it reads the pre-step channel snapshot — always empty. This exact
       miswiring shipped once; it must never come back.
    """
    definition = build_self_validating_news_definition()
    nodes = {n.id: n for n in definition.nodes}

    # Invariant 1 — worker writes the declared channel.
    declared = {c.name for c in definition.channels}
    assert nodes["scrape_page"].data.get("output_channel") == "scrapes"
    assert "scrapes" in declared

    # Invariant 2 — gather triggered by the worker, and ONLY the worker.
    gather_sources = [e.source for e in definition.edges if e.target == "gather_scrapes"]
    assert gather_sources == ["scrape_page"]
    assert "fanout" not in gather_sources

    # Strict-schema seams are bridged with edge mappings: the LLM's
    # final_text feeds regex_extract's sole "text" field, and the extracted
    # "matches" list feeds control.map's required "items" input.
    (e4,) = [e for e in definition.edges if e.source == "rank_urls" and e.target == "parse_urls"]
    assert e4.mappings == {"text": "final_text"}
    (e5,) = [e for e in definition.edges if e.source == "parse_urls" and e.target == "fanout"]
    assert e5.mappings == {"items": "matches"}

    # ai.llm.chat sends `prompt` and nothing else, so every LLM stage must be
    # fed real upstream text THROUGH an explicit prompt mapping. Without these
    # three the chain still "runs" and every model answers from a static
    # string — the exact rot that made the judge tier meaningless.
    prompt_sources = {
        (e.source, e.target): e.mappings
        for e in definition.edges
        if (e.mappings or {}).get("prompt")
    }
    assert prompt_sources == {
        ("search_text", "rank_urls"): {"prompt": "text"},
        ("combine_pages", "summarize"): {"prompt": "formatted_text"},
        ("mix_decoys", "final_answer"): {"prompt": "context_text"},
    }

    # A worker that parks the whole run on one unreachable news site cannot
    # fan out over the open web; gather(only_successful) exists for exactly
    # this and needs the worker to punch holes.
    nodes = {n.id: n for n in definition.nodes}
    assert nodes["scrape_page"].data.get("on_item_failure") == "hole"


def test_definition_missing_actions_fails_compile_cleanly():
    """Compiling without any of the required actions registered must fail
    with a clear NodeRegistryError — not a silent pass or a hard crash."""
    empty_registry = NodeRegistry()
    definition = build_self_validating_news_definition()

    with pytest.raises(Exception) as exc:
        compile_graph(definition, registry=empty_registry)
    # Either CompilationError wrapping NodeRegistryError, or NodeRegistryError
    msg = str(exc.value)
    assert "action." in msg or "node type" in msg.lower()


def test_definition_compiles_with_fakes():
    """Register fake executors for every action the definition references,
    then confirm the graph compiles end-to-end with the fan-in surfaced."""
    registry = _registry_with_fakes()
    definition = build_self_validating_news_definition()
    graph = compile_graph(definition, registry=registry)
    # Full 13-node chain compiles
    assert len(graph.nodes) == 13
    # Entry comes straight from the definition
    assert graph.entry_node_ids == ("headlines",)
    # The output_channel binding survives compilation.
    scrape = graph.nodes["scrape_page"]
    assert scrape.output_channel == "scrapes"
    assert "scrapes" in scrape.writes_channels
    assert graph.channels["scrapes"].reducer == "append"


def test_definition_roundtrips_as_reactflow_json():
    """The Studio POSTs ReactFlow JSON directly. Verify the definition
    serializes losslessly so Studio can render it without re-keying."""
    definition = build_self_validating_news_definition()
    dumped = definition.model_dump(mode="json")
    assert dumped["version"] == "1"
    assert len(dumped["nodes"]) == 13
    # User-authored payload under data.input survives round-trip
    first = dumped["nodes"][0]
    assert first["data"]["input"] == {"query": "top US news", "limit": 10}


_MOCK_URLS = [
    "http://one.example/story",
    "http://two.example/story",
    "http://three.example/story",
]

# Per-node mock outputs for every external (IO/LLM) node. The builtin
# nodes (text.regex_extract, control.map, control.gather, data.transform)
# run for real, so the parse → map → worker → channel → gather chain is
# actually executed, edge mappings included.
_MOCKS: dict[str, dict] = {
    "headlines": {"hits": [{"title": "Big Story"}]},
    "top_title": {"value": "Big Story"},
    "web_search": {"results": [{"url": u} for u in _MOCK_URLS]},
    "rank_urls": {"final_text": "\n".join(_MOCK_URLS)},
    "scrape_page": {"url": "mocked", "content": "mocked page body"},
    "combine_pages": {
        "formatted_text": "mocked page body\n---\nmocked page body",
        "sources": _MOCK_URLS,
        "page_count": len(_MOCK_URLS),
        "failed_pages": 0,
    },
    "summarize": {"final_text": "Real summary of Big Story."},
    "final_answer": {"final_text": "Big Story happened; key facts follow."},
}


def _mocked_definition() -> Definition:
    definition = build_self_validating_news_definition()
    for node in definition.nodes:
        if node.id in _MOCKS:
            node.data["mock_response"] = {"enabled": True, "output": _MOCKS[node.id]}
    return definition


async def test_mocked_run_executes_full_fan_in_chain():
    """Execute the ACTUAL example definition with every IO/LLM node mocked.

    This is the drift guard the structural checks can't provide: the run
    only completes — and gather only sees N items — if the map dispatches
    one Send per URL, each scrape invocation's output lands in the
    "scrapes" channel, and gather fires after the commit. The original
    miswiring (fanout → gather, no channel writer) dies here with count=0.
    """
    registry = _registry_with_fakes()
    graph = compile_graph(_mocked_definition(), registry=registry)
    emitter = FakeEmitter()
    scheduler = Scheduler(
        graph,
        MemoryCheckpointer(),
        make_app_context(emitter),
        registry=registry,
    )
    result = await scheduler.run(run_id="svn-mocked-e2e")
    assert result.status is RunStatus.COMPLETED

    # The regex node parsed every URL out of the LLM's ranked list, and the
    # map dispatched one worker per URL.
    assert result.last_outputs["parse_urls"]["matches"] == _MOCK_URLS
    assert result.last_outputs["fanout"]["dispatched"] == len(_MOCK_URLS)

    # Every worker's output reached the channel and gather drained all N.
    gathered = result.last_outputs["gather_scrapes"]
    assert gathered["count"] == len(_MOCK_URLS)
    assert all(v == _MOCKS["scrape_page"] for v in gathered["values"])
    assert result.channel_values["scrapes"] == [_MOCKS["scrape_page"]] * len(_MOCK_URLS)

    # Gather fired exactly once — N worker→gather edge firings in one
    # super-step collapse to a single invocation (per-target aggregation).
    gather_completions = [
        e
        for k, e in emitter.events
        if k == "data"
        and isinstance(e, dict)
        and e.get("event") == "node_completed"
        and e.get("node_id") == "gather_scrapes"
    ]
    assert len(gather_completions) == 1

    # Downstream kept flowing: mix_decoys built ONE prompt string carrying the
    # real summary plus all five decoys, and it reached the final node.
    context_text = result.last_outputs["mix_decoys"]["context_text"]
    assert _MOCKS["summarize"]["final_text"] in context_text
    assert "monarch butterflies" in context_text
    assert context_text.count("\n") >= 5
    assert result.last_outputs["final_answer"]["final_text"] == _MOCKS["final_answer"]["final_text"]
