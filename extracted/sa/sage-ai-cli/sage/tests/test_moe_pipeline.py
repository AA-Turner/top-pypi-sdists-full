"""Unit and integration tests for moe_pipeline.py."""

from __future__ import annotations

import pytest
from typing import Any

from sage.core.moe_pipeline import MoEPipeline, Specialist, SpecialistOutput, MoEResult


# ==========================================
# UNIT TESTS
# ==========================================

def test_moe_pipeline_init():
    """Verify initialization values."""
    planner = Specialist("p", "m-p", "sys-p")
    specs = {"s1": Specialist("s1", "m-s1", "sys-s1")}
    pipeline = MoEPipeline(
        send_fn=lambda *a, **kw: "s1",
        planner=planner,
        specialists=specs,
        max_specialists=2
    )
    assert pipeline.planner == planner
    assert pipeline.specialists == specs
    assert pipeline.max_specialists == 2


def test_moe_pipeline_ask_planner_capping():
    """Verify planner selection is sliced to max_specialists."""
    planner = Specialist("p", "m-p", "sys-p")
    specs = {
        "s1": Specialist("s1", "m-s1", "sys-s1", "desc1"),
        "s2": Specialist("s2", "m-s2", "sys-s2", "desc2"),
        "s3": Specialist("s3", "m-s3", "sys-s3", "desc3"),
    }
    
    # Planner returns 3, but max_specialists is 2
    pipeline = MoEPipeline(
        send_fn=lambda *a, **kw: "s1, s2, s3",
        planner=planner,
        specialists=specs,
        max_specialists=2
    )
    
    plan, reasoning = pipeline._ask_planner("test prompt")
    assert plan == ["s1", "s2"]
    assert reasoning == "s1, s2, s3"


def test_moe_pipeline_ask_planner_filtering_invalid():
    """Verify planner output only keeps valid specialists."""
    planner = Specialist("p", "m-p", "sys-p")
    specs = {
        "s1": Specialist("s1", "m-s1", "sys-s1", "desc1"),
    }
    
    pipeline = MoEPipeline(
        send_fn=lambda *a, **kw: "s1, invalid_spec, s2",
        planner=planner,
        specialists=specs
    )
    
    plan, reasoning = pipeline._ask_planner("test prompt")
    assert plan == ["s1"]


def test_moe_pipeline_ask_planner_exception():
    """Verify planner error handling."""
    planner = Specialist("p", "m-p", "sys-p")
    
    def failing_send(prompt, *, model, system):
        raise ValueError("LLM unavailable")
        
    pipeline = MoEPipeline(
        send_fn=failing_send,
        planner=planner,
        specialists={}
    )
    
    plan, reasoning = pipeline._ask_planner("test prompt")
    assert plan == []
    assert "planner error: LLM unavailable" in reasoning


def test_moe_pipeline_consult_prior_context():
    """Verify prior specialist outputs are properly formatted and included, ignoring errors."""
    specs = {"s1": Specialist("s1", "m-s1", "sys-s1")}
    received_prompts = []
    
    def mock_send(prompt, *, model, system):
        received_prompts.append(prompt)
        return "response"

    pipeline = MoEPipeline(
        send_fn=mock_send,
        planner=Specialist("p", "m-p", "sys-p"),
        specialists=specs
    )
    
    prior_outputs = [
        SpecialistOutput("specA", "modelA", "outputA", 0.5),
        SpecialistOutput("specB", "modelB", "", 0.1, error="failed output"),
        SpecialistOutput("specC", "modelC", "outputC", 0.3),
    ]
    
    output = pipeline._consult(specs["s1"], "user request", prior_outputs)
    assert output.specialist == "s1"
    assert output.output == "response"
    assert output.error is None
    
    # Assert prior context contains A and C but not B (due to error)
    last_prompt = received_prompts[-1]
    assert "## PRIOR SPECIALISTS" in last_prompt
    assert "## specA\noutputA" in last_prompt
    assert "## specC\noutputC" in last_prompt
    assert "specB" not in last_prompt


def test_moe_pipeline_consult_exception():
    """Verify specialist failure yields SpecialistOutput with error and doesn't crash."""
    specs = {"s1": Specialist("s1", "m-s1", "sys-s1")}
    
    def failing_send(*a, **kw):
        raise RuntimeError("Specialist model crashed")

    pipeline = MoEPipeline(
        send_fn=failing_send,
        planner=Specialist("p", "m-p", "sys-p"),
        specialists=specs
    )
    
    output = pipeline._consult(specs["s1"], "request", [])
    assert output.specialist == "s1"
    assert output.output == ""
    assert output.error == "Specialist model crashed"
    assert output.duration_s >= 0.0


def test_moe_pipeline_synthesize_filters_errors():
    """Verify synthesis prompt aggregates only successful outputs and handles errors."""
    received_prompts = []
    
    def mock_send(prompt, *, model, system):
        received_prompts.append(prompt)
        return "synthesis response"

    pipeline = MoEPipeline(
        send_fn=mock_send,
        planner=Specialist("p", "m-p", "sys-p"),
        specialists={}
    )
    
    outputs = [
        SpecialistOutput("coder", "model1", "code text", 0.1),
        SpecialistOutput("tester", "model2", "", 0.2, error="no tests generated"),
    ]
    
    res = pipeline._synthesize("request", outputs)
    assert res == "synthesis response"
    
    last_prompt = received_prompts[-1]
    assert "code text" in last_prompt
    assert "tester" not in last_prompt


def test_moe_pipeline_synthesize_exception():
    """Verify synthesis failure handles exception gracefully."""
    def failing_send(*a, **kw):
        raise Exception("Synthesis timeout")

    pipeline = MoEPipeline(
        send_fn=failing_send,
        planner=Specialist("p", "m-p", "sys-p"),
        specialists={}
    )
    
    res = pipeline._synthesize("request", [])
    assert "[synthesis failed: Synthesis timeout]" in res


def test_moe_pipeline_run_all_failed():
    """Verify run failure state when all specialists fail."""
    planner = Specialist("p", "m-p", "sys-p")
    specs = {"coder": Specialist("coder", "m-c", "sys-c")}
    
    def mock_send(prompt, *, model, system):
        if "AVAILABLE SPECIALISTS" in prompt:
            return "coder"
        raise ValueError("Coder model error")
        
    pipeline = MoEPipeline(
        send_fn=mock_send,
        planner=planner,
        specialists=specs
    )
    
    result = pipeline.run("run code")
    assert result.success is False
    assert result.plan == ["coder"]
    assert len(result.outputs) == 1
    assert result.outputs[0].error == "Coder model error"
    assert "[synthesis failed:" in result.final


# ==========================================
# INTEGRATION TESTS
# ==========================================

class MockAIOchestrationEngine:
    """Simulated Orchestration Engine integrating MoEPipeline routing."""
    def __init__(self):
        self.models_invoked: list[str] = []
        self.specialists = {
            "web_search": Specialist("web_search", "search-3b", "Search System", "searches the web for context"),
            "coder": Specialist("coder", "coder-7b", "Code System", "writes Python and TypeScript code"),
            "reviewer": Specialist("reviewer", "reviewer-3b", "Reviewer System", "reviews changes for correctness"),
        }
        self.planner = Specialist("planner", "planner-3b", "Planner System", "routes requests to specialists")

    def llm_send_fn(self, prompt: str, *, model: str, system: str) -> str:
        self.models_invoked.append(model)
        # Mock answers based on model routing
        if model == "planner-3b":
            if "AVAILABLE SPECIALISTS" in prompt:
                # Decide which specialists to call based on the user request
                req_section = prompt.split("AVAILABLE SPECIALISTS")[0].lower()
                if "bug" in req_section or "code" in req_section:
                    return "coder, reviewer"
                elif "search" in req_section or "weather" in req_section:
                    return "web_search"
                return "coder"
            elif "SPECIALIST OUTPUTS" in prompt:
                return f"Final unified answer integrating: {prompt}"
        elif model == "coder-7b":
            return "def some_code(): pass"
        elif model == "reviewer-3b":
            return "Review: Code looks functional and correct."
        elif model == "search-3b":
            return "Search Result: Today's weather is sunny."
        return "Default response"

    def process_request(self, user_request: str) -> MoEResult:
        pipeline = MoEPipeline(
            send_fn=self.llm_send_fn,
            planner=self.planner,
            specialists=self.specialists,
            max_specialists=3
        )
        return pipeline.run(user_request)


def test_integration_moe_routing_coding_task():
    """Verify integration routing for coding task consulting coder and reviewer."""
    engine = MockAIOchestrationEngine()
    result = engine.process_request("Write code to fix a bug in context management")
    
    assert result.success is True
    assert result.plan == ["coder", "reviewer"]
    assert len(result.outputs) == 2
    assert result.outputs[0].specialist == "coder"
    assert result.outputs[0].output == "def some_code(): pass"
    assert result.outputs[1].specialist == "reviewer"
    assert result.outputs[1].output == "Review: Code looks functional and correct."
    
    assert "Final unified answer" in result.final
    assert "def some_code(): pass" in result.final
    assert "Review: Code looks functional and correct." in result.final
    
    # Check that planner was called for routing and synthesis, and both specialists were called
    assert engine.models_invoked == ["planner-3b", "coder-7b", "reviewer-3b", "planner-3b"]


def test_integration_moe_routing_search_task():
    """Verify integration routing for search task consulting only web_search."""
    engine = MockAIOchestrationEngine()
    result = engine.process_request("Search weather forecast")
    
    assert result.success is True
    assert result.plan == ["web_search"]
    assert len(result.outputs) == 1
    assert result.outputs[0].specialist == "web_search"
    assert result.outputs[0].output == "Search Result: Today's weather is sunny."
    
    assert "Final unified answer" in result.final
    assert "Today's weather is sunny." in result.final
    
    assert engine.models_invoked == ["planner-3b", "search-3b", "planner-3b"]


def test_moe_pipeline_run_empty_plan():
    """Verify run output when planner returns no valid specialists."""
    planner = Specialist("p", "m-p", "sys-p")
    pipeline = MoEPipeline(
        send_fn=lambda *a, **kw: "",
        planner=planner,
        specialists={}
    )
    result = pipeline.run("hi")
    assert result.success is False
    assert result.plan == []
    assert result.routing_reason == "no specialists selected"

