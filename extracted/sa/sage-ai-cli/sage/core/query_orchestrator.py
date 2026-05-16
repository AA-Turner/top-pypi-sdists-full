"""Perplexity-style multi-model Q&A pipeline.

For ONE user query, runs a pipeline that uses DIFFERENT models per stage:

    [CLASSIFY]     small model decides query type + whether search needed
    [RETRIEVE]     search backend pulls candidate sources (skipped if not needed)
    [SYNTHESIZE]   bigger model picked by query type composes the answer
    [CITE]         small model extracts + formats citations

This is the routing logic Perplexity AI uses to pick "the right model for
each step" — different from sage's existing ``core/swarm.py`` which
decomposes a CODING task into typed subtasks.

Both modules coexist:
  - QueryOrchestrator: one Q&A → multiple models per stage
  - SwarmOrchestrator: one big task → multiple typed subtasks each on one model

Model picks here are data-driven from the available_models list, so adding
new cloud:* models just expands the routing options automatically.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable

logger = logging.getLogger("sage.query_orchestrator")


# ── Query types + stages ─────────────────────────────────────────────────────


class QueryType(Enum):
    """Categories the classifier outputs. Picked to cover ~95% of real
    Q&A traffic without over-fitting; we can split further later if
    telemetry shows a category dominating."""
    FACTUAL = "factual"             # "what's the capital of France"
    CODE = "code"                   # "how do I parse JSON in Python"
    REASONING = "reasoning"         # "why does X behavior happen"
    CREATIVE = "creative"           # "write a poem about", "design a UI for"
    CONVERSATIONAL = "conversational"  # "hi", "thanks", "how are you"


class QueryStage(Enum):
    CLASSIFY = "classify"
    RETRIEVE = "retrieve"
    SYNTHESIZE = "synthesize"
    CITE = "cite"


# ── Result types ─────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class QueryClassification:
    """Output of the classify stage. ``requires_search`` lets us short-
    circuit the retrieval stage for queries that don't need external
    info (reasoning, creative, conversational)."""
    query_type: QueryType
    confidence: float
    requires_search: bool


@dataclass(frozen=True)
class QueryResult:
    """Final output of the pipeline. Includes per-stage model attribution
    for cost auditing and debugging."""
    query: str
    answer: str
    sources: list[dict]
    models_used: dict[str, str]  # stage_name → model_id
    total_tokens: int = 0


# ── Model preference table ───────────────────────────────────────────────────
#
# For each (stage, query_type) pair we keep an ORDERED list of preferred
# model substrings. The orchestrator picks the first available model that
# matches any preference. If none match, falls back to the first available
# model — never returns None.

# Preferences are substrings (case-insensitive) of model_id.
# Order = priority. ("phi-4" before "gemma" means we prefer Phi-4 when
# both are available, but fall back to Gemma if not.)
_PREFERENCES: dict[QueryStage, dict[QueryType, list[str]]] = {
    QueryStage.CLASSIFY: {
        # Classification is cheap typing work — small fast models excel.
        QueryType.FACTUAL: ["phi-4", "gemma-2", "llama-3-1"],
        QueryType.CODE: ["phi-4", "gemma-2", "llama-3-1"],
        QueryType.REASONING: ["phi-4", "gemma-2", "llama-3-1"],
        QueryType.CREATIVE: ["phi-4", "gemma-2", "llama-3-1"],
        QueryType.CONVERSATIONAL: ["phi-4", "gemma-2", "llama-3-1"],
    },
    QueryStage.SYNTHESIZE: {
        # Synthesis benefits from the strongest model for that domain.
        QueryType.CODE: ["qwen-coder", "deepseek", "llama"],
        QueryType.REASONING: ["deepseek-r1", "yi-1-5", "llama"],
        QueryType.FACTUAL: ["llama-3-1", "gemma-2", "mistral"],
        QueryType.CREATIVE: ["llama-3-1", "mistral", "gemma-2"],
        QueryType.CONVERSATIONAL: ["llama-3-1", "gemma-2", "mistral"],
    },
    QueryStage.CITE: {
        # Citation extraction is structural pattern matching — same
        # small-model preference as classification.
        QueryType.FACTUAL: ["phi-4", "gemma-2", "llama-3-1"],
        QueryType.CODE: ["phi-4", "gemma-2", "llama-3-1"],
        QueryType.REASONING: ["phi-4", "gemma-2", "llama-3-1"],
        QueryType.CREATIVE: ["phi-4", "gemma-2", "llama-3-1"],
        QueryType.CONVERSATIONAL: ["phi-4", "gemma-2", "llama-3-1"],
    },
    # RETRIEVE stage uses a search backend (no model picking needed)
}


# ── Orchestrator ─────────────────────────────────────────────────────────────


class QueryOrchestrator:
    """Multi-stage, multi-model Q&A pipeline.

    Construct with the list of available model_ids (typically the deployed
    cloud:* models for paid users). Call ``run(query)`` to execute the
    full pipeline.

    Stage implementations are pluggable via the ``_classify_stage``,
    ``_retrieve_stage``, ``_synthesize_stage``, ``_cite_stage`` attributes.
    The defaults are simple stubs; production wires them to the actual
    model-call + search-API helpers.
    """

    def __init__(
        self,
        available_models: list[str],
        classifier_fn: Callable | None = None,
        retriever_fn: Callable | None = None,
        synthesizer_fn: Callable | None = None,
        citation_fn: Callable | None = None,
    ):
        self._available = list(available_models)

        # Inject stage handlers or use no-op defaults. The full real
        # impls live in the CLI command that wires this with sage's
        # providers + grounded_web_search.
        self._classify_stage = classifier_fn or self._default_classify
        self._retrieve_stage = retriever_fn or self._default_retrieve
        self._synthesize_stage = synthesizer_fn or self._default_synthesize
        self._cite_stage = citation_fn or self._default_cite

    # ── Model picking ────────────────────────────────────────────────────────

    def pick_model(self, stage: QueryStage, query_type: QueryType) -> str:
        """Return the best available model for this (stage, query_type)
        based on the preference table.

        Raises RuntimeError if no models are configured at all.
        """
        if not self._available:
            raise RuntimeError(
                "QueryOrchestrator has no available models — pass at least "
                "one to the constructor."
            )

        prefs = _PREFERENCES.get(stage, {}).get(query_type, [])
        for pref in prefs:
            for model in self._available:
                if pref.lower() in model.lower():
                    return model
        # Fallback: first available model. Better than None — guarantees
        # the pipeline always runs end-to-end.
        return self._available[0]

    # ── Pipeline ────────────────────────────────────────────────────────────

    def run(self, query: str) -> QueryResult:
        """Execute the full pipeline for a single query."""
        if not query or not query.strip():
            raise ValueError("Cannot orchestrate empty query.")

        models_used: dict[str, str] = {}
        total_tokens = 0

        # Stage 1: classify
        classify_model = self.pick_model(QueryStage.CLASSIFY, QueryType.FACTUAL)
        models_used["CLASSIFY"] = classify_model
        classification: QueryClassification = self._classify_stage(query)

        # Stage 2: retrieve (skipped if classifier says no search needed)
        sources: list[dict] = []
        if classification.requires_search:
            sources = self._retrieve_stage(query)
            models_used["RETRIEVE"] = "search_api"

        # Stage 3: synthesize — model picked by query type
        synth_model = self.pick_model(QueryStage.SYNTHESIZE, classification.query_type)
        models_used["SYNTHESIZE"] = synth_model
        answer, synth_tokens = self._synthesize_stage(query, classification, sources)
        total_tokens += int(synth_tokens or 0)

        # Stage 4: cite — only if we had sources
        formatted_sources: list[dict] = sources
        if sources:
            cite_model = self.pick_model(QueryStage.CITE, classification.query_type)
            models_used["CITE"] = cite_model
            formatted_sources = self._cite_stage(answer, sources) or sources

        return QueryResult(
            query=query,
            answer=answer,
            sources=formatted_sources,
            models_used=models_used,
            total_tokens=total_tokens,
        )

    # ── Default stage stubs ─────────────────────────────────────────────────
    #
    # These let the orchestrator run end-to-end without network calls —
    # useful for tests and for "dry-run" CLI mode. Production wires real
    # implementations via the constructor's *_fn args.

    def _default_classify(self, query: str) -> QueryClassification:
        # Cheap heuristic. Real classifier would call a model.
        q_lower = query.lower()
        if any(w in q_lower for w in ("def ", "import ", "class ", "function", "python", "javascript", "code")):
            return QueryClassification(QueryType.CODE, 0.6, requires_search=True)
        if any(w in q_lower for w in ("why", "how does", "explain", "reason")):
            return QueryClassification(QueryType.REASONING, 0.6, requires_search=False)
        if any(w in q_lower for w in ("write", "poem", "story", "design")):
            return QueryClassification(QueryType.CREATIVE, 0.6, requires_search=False)
        if any(w in q_lower for w in ("hi", "hello", "thanks", "how are you")):
            return QueryClassification(QueryType.CONVERSATIONAL, 0.6, requires_search=False)
        return QueryClassification(QueryType.FACTUAL, 0.6, requires_search=True)

    def _default_retrieve(self, query: str) -> list[dict]:
        return []  # Real retriever pulls from a search API

    def _default_synthesize(
        self,
        query: str,
        classification: QueryClassification,
        sources: list[dict],
    ) -> tuple[str, int]:
        return (f"(no synthesis backend wired) classified={classification.query_type.value}", 0)

    def _default_cite(self, answer: str, sources: list[dict]) -> list[dict]:
        return sources


__all__ = [
    "QueryType",
    "QueryStage",
    "QueryClassification",
    "QueryResult",
    "QueryOrchestrator",
]
