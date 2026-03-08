"""Tests for Chronos session analysis."""

from __future__ import annotations

import json

import httpx

from plato.chronos.analysis import (
    SpanNode,
    analyze_session,
    build_span_tree,
    fetch_all_spans,
)
from plato.chronos.models import OTelSpan


def _span(
    span_id: str,
    name: str = "test",
    parent_span_id: str | None = None,
    start_ns: int = 0,
    end_ns: int | None = 1_000_000,
    attributes: dict | None = None,
    trace_id: str = "trace-1",
) -> OTelSpan:
    return OTelSpan(
        trace_id=trace_id,
        span_id=span_id,
        parent_span_id=parent_span_id,
        name=name,
        start_time_unix_nano=start_ns,
        end_time_unix_nano=end_ns,
        attributes=attributes or {},
    )


class TestBuildSpanTree:
    def test_parent_child(self):
        spans = [
            _span("root", "root_span"),
            _span("child1", "child", parent_span_id="root"),
            _span("child2", "child", parent_span_id="root"),
        ]
        tree = build_span_tree(spans)
        assert len(tree.roots) == 1
        assert len(tree.orphan_roots) == 0
        assert len(tree.roots[0].children) == 2
        assert tree.by_id["child1"].parent_span_id == "root"

    def test_orphans(self):
        spans = [
            _span("a", "a_span"),
            _span("b", "b_span", parent_span_id="missing"),
            _span("c", "c_span", parent_span_id="missing"),
        ]
        tree = build_span_tree(spans)
        assert len(tree.roots) == 1
        assert len(tree.orphan_roots) == 2

    def test_empty(self):
        tree = build_span_tree([])
        assert tree.roots == []
        assert tree.orphan_roots == []


class TestSpanNode:
    def test_duration_ms(self):
        node = SpanNode(span=_span("x", start_ns=0, end_ns=5_000_000))
        assert node.duration_ms == 5.0

    def test_duration_none(self):
        node = SpanNode(span=_span("x", end_ns=None))
        assert node.duration_ms is None

    def test_get_attr(self):
        node = SpanNode(span=_span("x", attributes={"foo": "bar"}))
        assert node.get_attr("foo") == "bar"
        assert node.get_attr("missing", 42) == 42


class TestAgentExecutionGrouping:
    def test_agent_execution_output_spans(self):
        spans = [
            _span(
                "agent1",
                "agent.execution.output",
                start_ns=0,
                end_ns=100_000_000,
                attributes={
                    "atif.agent.name": "test-agent",
                    "atif.agent.prompt_tokens": 100,
                    "atif.agent.completion_tokens": 50,
                    "atif.agent.cost_usd": 0.01,
                },
            ),
            _span(
                "step1",
                "atif.step.1",
                parent_span_id="agent1",
                start_ns=1_000_000,
                end_ns=10_000_000,
                attributes={
                    "atif.step.id": 1,
                    "atif.step.source": "agent",
                    "atif.step.prompt_tokens": 100,
                    "atif.step.completion_tokens": 50,
                },
            ),
            _span(
                "step2",
                "atif.step.2",
                parent_span_id="agent1",
                start_ns=10_000_000,
                end_ns=20_000_000,
                attributes={
                    "atif.step.id": 2,
                    "atif.step.source": "agent",
                    "atif.step.prompt_tokens": 100,
                    "atif.step.completion_tokens": 50,
                },
            ),
        ]
        result = analyze_session(spans, "test-session")
        assert len(result.agent_executions) == 1
        ex = result.agent_executions[0]
        assert ex.agent_name == "test-agent"
        assert ex.step_count == 2
        assert not ex.is_orphaned
        assert ex.token_summary.prompt_tokens == 100  # from root node attrs
        assert ex.token_summary.cost_usd == 0.01

    def test_orphan_steps_grouped(self):
        spans = [
            _span(
                "s1",
                "atif.step.1",
                parent_span_id="missing_parent",
                start_ns=0,
                end_ns=5_000_000,
                attributes={"atif.step.id": 1, "atif.step.source": "agent", "atif.step.prompt_tokens": 50},
            ),
            _span(
                "s2",
                "atif.step.2",
                parent_span_id="missing_parent",
                start_ns=5_000_000,
                end_ns=10_000_000,
                attributes={"atif.step.id": 2, "atif.step.source": "agent", "atif.step.prompt_tokens": 60},
            ),
        ]
        result = analyze_session(spans, "test-session")
        assert len(result.agent_executions) == 1
        ex = result.agent_executions[0]
        assert ex.is_orphaned
        assert ex.step_count == 2
        assert ex.token_summary.prompt_tokens == 110


class TestAnalyzeSession:
    def test_full_analysis(self):
        spans = [
            _span("reset1", "reset", start_ns=0, end_ns=50_000_000),
            _span("loop1", "ad_loop", start_ns=50_000_000, end_ns=200_000_000),
            _span(
                "agent1",
                "agent.execution.output",
                parent_span_id="loop1",
                start_ns=60_000_000,
                end_ns=190_000_000,
                attributes={"atif.agent.name": "my-agent", "atif.agent.cost_usd": 0.05},
            ),
            _span(
                "step1",
                "atif.step.1",
                parent_span_id="agent1",
                start_ns=70_000_000,
                end_ns=80_000_000,
                attributes={
                    "atif.step.id": 1,
                    "atif.step.source": "agent",
                    "atif.step.model_name": "gpt-4",
                    "atif.step.prompt_tokens": 500,
                    "atif.step.completion_tokens": 100,
                    "atif.step.tool_calls": json.dumps([{"name": "Read"}, {"name": "Bash"}]),
                },
            ),
            _span(
                "step2",
                "atif.step.2",
                parent_span_id="agent1",
                start_ns=80_000_000,
                end_ns=90_000_000,
                attributes={
                    "atif.step.id": 2,
                    "atif.step.source": "agent",
                    "atif.step.model_name": "gpt-4",
                    "atif.step.prompt_tokens": 600,
                    "atif.step.completion_tokens": 150,
                    "atif.step.tool_calls": json.dumps([{"name": "Edit"}]),
                },
            ),
        ]
        result = analyze_session(spans, "sess-1")

        assert result.session_id == "sess-1"
        assert result.total_spans == 5
        assert result.total_duration_ms == 200.0

        # Phases
        assert len(result.phases) == 2
        assert result.phases[0].name == "reset"
        assert result.phases[1].name == "ad_loop"

        # Agent
        assert len(result.agent_executions) == 1
        ex = result.agent_executions[0]
        assert ex.agent_name == "my-agent"
        assert ex.step_count == 2
        assert ex.models_used == ["gpt-4"]
        assert ex.tool_usage == {"Read": 1, "Bash": 1, "Edit": 1}
        assert ex.token_summary.cost_usd == 0.05

        # Global tools
        assert result.tool_usage == {"Read": 1, "Bash": 1, "Edit": 1}

    def test_empty_session(self):
        result = analyze_session([], "empty")
        assert result.total_spans == 0
        assert result.agent_executions == []


class TestPhaseDetection:
    def test_structural_spans_detected(self):
        spans = [
            _span("r", "reset", start_ns=0, end_ns=10_000_000),
            _span("a", "ad_loop.iter.0.improve", start_ns=10_000_000, end_ns=50_000_000),
            _span("t", "transition_analysis", start_ns=50_000_000, end_ns=60_000_000),
            _span("log1", "log.info", start_ns=5_000_000, end_ns=5_000_000),  # should be excluded
        ]
        result = analyze_session(spans, "s")
        names = [p.name for p in result.phases]
        assert "reset" in names
        assert "ad_loop.iter.0.improve" in names
        assert "transition_analysis" in names
        assert "log.info" not in names


class TestFetchAllSpansPagination:
    def test_two_pages(self):
        call_count = 0

        def handler(request: httpx.Request):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return httpx.Response(
                    200,
                    json={
                        "session_id": "s1",
                        "spans": [{"trace_id": "t", "span_id": "a", "name": "x", "start_time_unix_nano": 0}],
                        "total_count": 2,
                        "has_more": True,
                        "cursor": "page2",
                    },
                )
            else:
                return httpx.Response(
                    200,
                    json={
                        "session_id": "s1",
                        "spans": [{"trace_id": "t", "span_id": "b", "name": "y", "start_time_unix_nano": 1}],
                        "total_count": 2,
                        "has_more": False,
                        "cursor": None,
                    },
                )

        client = httpx.Client(base_url="https://test.example", transport=httpx.MockTransport(handler))
        spans = fetch_all_spans(client, "s1")
        assert len(spans) == 2
        assert spans[0].span_id == "a"
        assert spans[1].span_id == "b"
        assert call_count == 2
