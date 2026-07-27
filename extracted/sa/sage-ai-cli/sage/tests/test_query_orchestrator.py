"""Tests for QueryOrchestrator — Perplexity-style multi-model Q&A.

Perplexity's signature pattern: one user query gets handled by MULTIPLE
models, each picked for its strength at a particular stage:

  1. CLASSIFY   — small/fast model decides query type (factual, code, math, reasoning)
  2. RETRIEVE   — search backend gets candidate sources
  3. SYNTHESIZE — bigger model picks the right model based on type + composes the answer
  4. CITE       — fast model extracts citations + formats them

This is different from `core/swarm.py`'s task-decomposition (which splits
ONE coding task into typed subtasks). QueryOrchestrator handles ONE Q&A.

TDD: tests describe the stage contract and routing decisions.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from sage.core.query_orchestrator import (
    QueryClassification,
    QueryOrchestrator,
    QueryResult,
    QueryStage,
    QueryType,
)

# Real cloud API calls — integration only.
pytestmark = [
    pytest.mark.timeout(900),
    pytest.mark.integration,
]


# ── QueryClassification ──────────────────────────────────────────────────────


class TestQueryClassification:
    def test_classification_has_type_and_confidence(self):
        c = QueryClassification(
            query_type=QueryType.FACTUAL,
            confidence=0.95,
            requires_search=True,
        )
        assert c.query_type == QueryType.FACTUAL
        assert c.confidence == 0.95
        assert c.requires_search

    def test_classification_types_cover_main_categories(self):
        """Five categories cover ~95% of real Q&A: factual, code,
        reasoning, creative, conversational."""
        for t in [
            QueryType.FACTUAL,
            QueryType.CODE,
            QueryType.REASONING,
            QueryType.CREATIVE,
            QueryType.CONVERSATIONAL,
        ]:
            QueryClassification(query_type=t, confidence=1.0, requires_search=False)


# ── QueryOrchestrator stage routing ──────────────────────────────────────────


class TestStageRouting:
    """Each stage picks a model based on the query type. Tests verify the
    routing decisions, not the actual model output."""

    @pytest.fixture
    def orch(self):
        return QueryOrchestrator(
            available_models=[
                "cloud:qwen-coder-7b",
                "cloud:llama-3-1-8b",
                "cloud:deepseek-r1-7b",
                "cloud:gemma-2-9b",
                "cloud:phi-4-14b",
            ],
        )

    def test_picks_small_fast_model_for_classification(self, orch):
        """Classification is a quick binary/typing decision — should use
        the smallest available model so we don't burn budget on metadata."""
        model = orch.pick_model(QueryStage.CLASSIFY, QueryType.FACTUAL)
        # Phi-4 14B is fast at small tasks; Gemma 2 9B also acceptable
        assert model in ("cloud:phi-4-14b", "cloud:gemma-2-9b", "cloud:llama-3-1-8b")

    def test_picks_coder_for_synthesis_when_code_query(self, orch):
        model = orch.pick_model(QueryStage.SYNTHESIZE, QueryType.CODE)
        assert model == "cloud:qwen-coder-7b"

    def test_picks_reasoner_for_synthesis_when_reasoning_query(self, orch):
        model = orch.pick_model(QueryStage.SYNTHESIZE, QueryType.REASONING)
        assert model == "cloud:deepseek-r1-7b"

    def test_picks_general_for_synthesis_when_factual_query(self, orch):
        """Factual lookups don't need the reasoning specialist — the
        cheaper general-purpose model is appropriate."""
        model = orch.pick_model(QueryStage.SYNTHESIZE, QueryType.FACTUAL)
        assert model in ("cloud:llama-3-1-8b", "cloud:gemma-2-9b")

    def test_picks_small_model_for_citation_extraction(self, orch):
        """Citation extraction is structural pattern-matching — cheap
        models handle it fine."""
        model = orch.pick_model(QueryStage.CITE, QueryType.FACTUAL)
        assert "phi-4" in model or "gemma-2" in model or "llama-3-1" in model

    def test_unknown_query_type_picks_general_model(self, orch):
        """Defensive: never returns None. Falls back to whatever
        general-purpose model is available."""
        # Build with NONE of the specialty models
        orch_min = QueryOrchestrator(available_models=["cloud:llama-3-1-8b"])
        # Should still pick something
        m = orch_min.pick_model(QueryStage.SYNTHESIZE, QueryType.CODE)
        assert m == "cloud:llama-3-1-8b"

    def test_empty_model_list_raises(self):
        orch = QueryOrchestrator(available_models=[])
        with pytest.raises(RuntimeError, match="no.*models"):
            orch.pick_model(QueryStage.SYNTHESIZE, QueryType.FACTUAL)


# ── Full pipeline ────────────────────────────────────────────────────────────


class TestFullPipeline:
    """End-to-end test of the four-stage pipeline. Stages are mocked;
    we verify the orchestration logic, not model outputs."""

    def test_pipeline_runs_all_four_stages_in_order(self):
        orch = _orch_with_stage_recorders()
        result = orch.run("What is the capital of France?")

        # All four stages fired, in order
        assert orch._stages_fired == ["CLASSIFY", "RETRIEVE", "SYNTHESIZE", "CITE"]
        assert isinstance(result, QueryResult)

    def test_skips_retrieval_when_classifier_says_no_search_needed(self):
        """Some queries are pure reasoning/creative — no search benefits.
        Classifier signals this and we skip the retrieval stage to save
        a search-API call."""
        orch = _orch_with_stage_recorders(
            classification=QueryClassification(
                query_type=QueryType.REASONING,
                confidence=0.9,
                requires_search=False,
            ),
        )
        orch.run("Why might a refactor improve test reliability?")
        assert "RETRIEVE" not in orch._stages_fired
        assert "SYNTHESIZE" in orch._stages_fired

    def test_records_model_used_per_stage(self):
        """For debugging + cost analysis, every model invocation is logged
        on the QueryResult."""
        orch = _orch_with_stage_recorders()
        result = orch.run("test")
        # Result captures which model handled each stage
        assert "CLASSIFY" in result.models_used
        assert "SYNTHESIZE" in result.models_used

    def test_returns_result_with_answer_and_sources(self):
        orch = _orch_with_stage_recorders()
        result = orch.run("Tell me about Mars")
        assert result.answer  # non-empty synthesized text
        assert isinstance(result.sources, list)

    def test_records_total_tokens_across_stages(self):
        """Cost reporting needs to know how many tokens the pipeline used.
        Even when individual stages don't report tokens, the orchestrator
        defaults to 0 (not None) so the field is always numeric."""
        orch = _orch_with_stage_recorders()
        result = orch.run("anything")
        assert isinstance(result.total_tokens, int)
        assert result.total_tokens >= 0


# ── Test helpers ─────────────────────────────────────────────────────────────


def _orch_with_stage_recorders(classification=None):
    """Build an orchestrator with fake stage handlers that record their
    invocation. Lets us assert on flow control without real model calls."""
    classification = classification or QueryClassification(
        query_type=QueryType.FACTUAL, confidence=0.9, requires_search=True,
    )

    orch = QueryOrchestrator(
        available_models=[
            "cloud:phi-4-14b",
            "cloud:llama-3-1-8b",
            "cloud:qwen-coder-7b",
            "cloud:deepseek-r1-7b",
        ],
    )
    orch._stages_fired = []  # type: ignore[attr-defined]

    # Patch each stage to record invocation
    orch._classify_stage = lambda q: (orch._stages_fired.append("CLASSIFY") or classification)  # type: ignore[attr-defined]
    orch._retrieve_stage = lambda q: (orch._stages_fired.append("RETRIEVE") or [{"uri": "x", "snippet": "y"}])  # type: ignore[attr-defined]
    orch._synthesize_stage = lambda q, c, srcs: (  # type: ignore[attr-defined]
        orch._stages_fired.append("SYNTHESIZE") or ("Paris is the capital.", 50)
    )
    orch._cite_stage = lambda answer, srcs: (orch._stages_fired.append("CITE") or [])  # type: ignore[attr-defined]
    return orch
