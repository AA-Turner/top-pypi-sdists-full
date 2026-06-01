"""
Drift Detection for LlamaIndex RAG Workflows.

Tracks query execution expectations vs actual behavior to detect drifts.
Useful for monitoring retrieval quality, response generation, and RAG pipeline health.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class DriftType(Enum):
    """Types of behavioral drift in LlamaIndex workflows."""

    # Retrieval drifts
    EMPTY_RETRIEVAL = "empty_retrieval"  # No nodes retrieved
    LOW_RELEVANCE = "low_relevance"  # Poor similarity scores
    RETRIEVAL_COUNT = "retrieval_count"  # Unexpected retrieval count
    RETRIEVAL_TIMEOUT = "retrieval_timeout"  # Retrieval took too long

    # Response drifts
    EMPTY_RESPONSE = "empty_response"  # Empty or minimal response
    RESPONSE_TRUNCATED = "response_truncated"  # Response appears cut off
    NO_SOURCE_NODES = "no_source_nodes"  # Response without sources
    HALLUCINATION = "hallucination"  # Possible hallucinated content

    # Query drifts
    QUERY_MODIFICATION = "query_modification"  # Query was transformed
    QUERY_EXPANSION = "query_expansion"  # Query was expanded
    QUERY_FAILURE = "query_failure"  # Query execution failed

    # Synthesis drifts
    SYNTHESIS_FAILURE = "synthesis_failure"  # Synthesis step failed
    SYNTHESIS_EMPTY = "synthesis_empty"  # Empty synthesis result

    # Embedding drifts
    EMBEDDING_FAILURE = "embedding_failure"  # Embedding failed
    EMBEDDING_DIMENSION = "embedding_dimension"  # Dimension mismatch

    # Reranking drifts
    RERANK_FAILURE = "rerank_failure"  # Reranking failed
    RERANK_SCORE_ANOMALY = "rerank_score_anomaly"  # Unusual reranking scores

    # Performance drifts
    DURATION_ANOMALY = "duration_anomaly"  # Query took too long
    TOKEN_ANOMALY = "token_anomaly"  # Unusual token usage
    COST_ANOMALY = "cost_anomaly"  # Unusual cost

    # Quality drifts
    LOW_QUALITY_RESPONSE = "low_quality_response"  # Response quality concerns
    INCOMPLETE_RESPONSE = "incomplete_response"  # Response seems incomplete


class DriftSeverity(Enum):
    """Severity of detected drift."""

    INFO = "info"  # Expected variation, informational
    WARNING = "warning"  # Notable deviation, worth monitoring
    ALERT = "alert"  # Significant drift, may need intervention


@dataclass
class DetectedDrift:
    """Represents a detected drift with full context."""

    drift_type: DriftType
    severity: DriftSeverity
    description: str
    expected: str | None = None
    actual: str | None = None
    query_id: str | None = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "drift_type": self.drift_type.value,
            "severity": self.severity.value,
            "description": self.description,
            "expected": self.expected,
            "actual": self.actual,
            "query_id": self.query_id,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }


@dataclass
class QueryPlan:
    """Captures expected query execution behavior."""

    # Query info
    query_id: str | None = None
    query_str: str | None = None
    query_type: str = "query"  # query, chat

    # Index info
    index_id: str | None = None
    index_type: str = "vector"  # vector, keyword, hybrid

    # Retrieval settings
    retriever_type: str = "vector"
    top_k: int = 5
    similarity_threshold: float | None = None

    # Expected behavior
    expect_source_nodes: bool = True
    expect_reranking: bool = False
    max_response_length: int | None = None

    # Metadata
    timestamp: datetime = field(default_factory=datetime.now)
    llm_model: str | None = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "query_id": self.query_id,
            "query_preview": self.query_str[:100] if self.query_str else None,
            "query_type": self.query_type,
            "index_id": self.index_id,
            "index_type": self.index_type,
            "retriever_type": self.retriever_type,
            "top_k": self.top_k,
            "similarity_threshold": self.similarity_threshold,
            "expect_source_nodes": self.expect_source_nodes,
            "expect_reranking": self.expect_reranking,
            "timestamp": self.timestamp.isoformat(),
            "llm_model": self.llm_model,
        }


@dataclass
class ExecutionTrace:
    """Tracks actual query execution for comparison against plan."""

    # Retrieval tracking
    retrievals: List[Dict[str, Any]] = field(default_factory=list)
    total_nodes_retrieved: int = 0
    avg_similarity_score: float = 0.0
    max_similarity_score: float = 0.0
    empty_retrievals: int = 0

    # Synthesis tracking
    synthesis_calls: List[Dict[str, Any]] = field(default_factory=list)
    empty_syntheses: int = 0

    # LLM tracking
    llm_calls: List[Dict[str, Any]] = field(default_factory=list)

    # Embedding tracking
    embedding_calls: List[Dict[str, Any]] = field(default_factory=list)
    total_texts_embedded: int = 0

    # Reranking tracking
    rerank_calls: List[Dict[str, Any]] = field(default_factory=list)

    # Response tracking
    final_response: str | None = None
    response_length: int = 0
    source_node_count: int = 0

    # Metrics
    total_duration_ms: float = 0
    total_tokens: int = 0
    total_cost: float = 0

    # Result
    success: bool = False

    def add_retrieval(
        self,
        retriever_type: str,
        num_nodes: int,
        scores: List[float] | None = None,
        duration_ms: float = 0,
    ) -> None:
        """Record a retrieval operation."""
        avg_score = sum(scores) / len(scores) if scores else 0.0
        max_score = max(scores) if scores else 0.0
        self.retrievals.append(
            {
                "retriever_type": retriever_type,
                "num_nodes": num_nodes,
                "avg_score": avg_score,
                "max_score": max_score,
                "duration_ms": duration_ms,
                "timestamp": datetime.now().isoformat(),
            }
        )
        self.total_nodes_retrieved += num_nodes
        if scores:
            # Update running average
            total = len(self.retrievals)
            self.avg_similarity_score = (
                self.avg_similarity_score * (total - 1) + avg_score
            ) / total
            if max_score > self.max_similarity_score:
                self.max_similarity_score = max_score
        if num_nodes == 0:
            self.empty_retrievals += 1

    def add_synthesis(
        self,
        num_nodes: int,
        response_length: int,
        success: bool = True,
    ) -> None:
        """Record a synthesis operation."""
        self.synthesis_calls.append(
            {
                "num_nodes": num_nodes,
                "response_length": response_length,
                "success": success,
                "timestamp": datetime.now().isoformat(),
            }
        )
        if response_length < 10:
            self.empty_syntheses += 1

    def add_llm_call(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
        cost: float = 0,
    ) -> None:
        """Record an LLM call."""
        self.llm_calls.append(
            {
                "model": model,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost": cost,
                "timestamp": datetime.now().isoformat(),
            }
        )
        self.total_tokens += input_tokens + output_tokens
        self.total_cost += cost

    def add_embedding(
        self,
        model: str,
        num_texts: int,
        tokens: int = 0,
    ) -> None:
        """Record an embedding operation."""
        self.embedding_calls.append(
            {
                "model": model,
                "num_texts": num_texts,
                "tokens": tokens,
                "timestamp": datetime.now().isoformat(),
            }
        )
        self.total_texts_embedded += num_texts

    def add_rerank(
        self,
        model: str,
        num_input: int,
        num_output: int,
        scores: List[float] | None = None,
    ) -> None:
        """Record a reranking operation."""
        self.rerank_calls.append(
            {
                "model": model,
                "num_input": num_input,
                "num_output": num_output,
                "top_scores": scores[:3] if scores else None,
                "timestamp": datetime.now().isoformat(),
            }
        )

    def set_response(
        self,
        response: str,
        source_node_count: int = 0,
    ) -> None:
        """Set the final response."""
        self.final_response = response
        self.response_length = len(response) if response else 0
        self.source_node_count = source_node_count
        self.success = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "retrieval_count": len(self.retrievals),
            "total_nodes_retrieved": self.total_nodes_retrieved,
            "avg_similarity_score": self.avg_similarity_score,
            "max_similarity_score": self.max_similarity_score,
            "empty_retrievals": self.empty_retrievals,
            "synthesis_count": len(self.synthesis_calls),
            "empty_syntheses": self.empty_syntheses,
            "llm_call_count": len(self.llm_calls),
            "embedding_count": len(self.embedding_calls),
            "rerank_count": len(self.rerank_calls),
            "response_length": self.response_length,
            "source_node_count": self.source_node_count,
            "total_duration_ms": self.total_duration_ms,
            "total_tokens": self.total_tokens,
            "total_cost": self.total_cost,
            "success": self.success,
        }


class DriftDetector:
    """
    Detects drift between expected and actual query execution.

    Captures:
    - Query and index configuration
    - Actual retrieval and synthesis execution
    - Compares and reports deviations
    """

    def __init__(self):
        self.plan = QueryPlan()
        self.execution = ExecutionTrace()
        self.detected_drifts: List[DetectedDrift] = []

    def capture_query_start(
        self,
        query_id: str,
        query_str: str,
        query_type: str = "query",
        index_id: str | None = None,
    ) -> None:
        """
        Capture query initiation details.

        Args:
            query_id: Query identifier
            query_str: The query string
            query_type: Type of query (query, chat)
            index_id: Index identifier
        """
        self.plan.query_id = query_id
        self.plan.query_str = query_str
        self.plan.query_type = query_type
        self.plan.index_id = index_id

    def capture_retriever_config(
        self,
        retriever_type: str,
        top_k: int = 5,
        similarity_threshold: float | None = None,
    ) -> None:
        """Capture retriever configuration."""
        self.plan.retriever_type = retriever_type
        self.plan.top_k = top_k
        self.plan.similarity_threshold = similarity_threshold

    def capture_llm_model(self, model: str) -> None:
        """Capture the LLM model being used."""
        self.plan.llm_model = model

    def record_retrieval(
        self,
        retriever_type: str,
        nodes: List[Any] | None = None,
        scores: List[float] | None = None,
        duration_ms: float = 0,
    ) -> DetectedDrift | None:
        """
        Record a retrieval operation and check for drift.

        Returns DetectedDrift if drift is detected.
        """
        num_nodes = len(nodes) if nodes else 0
        self.execution.add_retrieval(retriever_type, num_nodes, scores, duration_ms)

        # Check for empty retrieval
        if num_nodes == 0:
            drift = DetectedDrift(
                drift_type=DriftType.EMPTY_RETRIEVAL,
                severity=DriftSeverity.WARNING,
                description=f"Retrieval ({retriever_type}) returned no results",
                expected=f"At least 1 node (top_k={self.plan.top_k})",
                actual="0 nodes",
                query_id=self.plan.query_id,
            )
            self.detected_drifts.append(drift)
            return drift

        # Check for low relevance
        if scores and self.plan.similarity_threshold:
            if max(scores) < self.plan.similarity_threshold:
                drift = DetectedDrift(
                    drift_type=DriftType.LOW_RELEVANCE,
                    severity=DriftSeverity.WARNING,
                    description="Best match below similarity threshold",
                    expected=f">= {self.plan.similarity_threshold}",
                    actual=f"{max(scores):.3f}",
                    query_id=self.plan.query_id,
                )
                self.detected_drifts.append(drift)
                return drift

        # Check for unexpectedly few results
        if self.plan.top_k and num_nodes < self.plan.top_k * 0.5:
            drift = DetectedDrift(
                drift_type=DriftType.RETRIEVAL_COUNT,
                severity=DriftSeverity.INFO,
                description="Retrieved fewer nodes than expected",
                expected=f"~{self.plan.top_k} nodes",
                actual=f"{num_nodes} nodes",
                query_id=self.plan.query_id,
            )
            self.detected_drifts.append(drift)
            return drift

        return None

    def record_synthesis(
        self,
        response: str | None = None,
        num_nodes: int = 0,
    ) -> DetectedDrift | None:
        """Record a synthesis operation and check for drift."""
        response_length = len(response) if response else 0
        self.execution.add_synthesis(num_nodes, response_length)

        # Check for empty synthesis
        if response_length < 10:
            drift = DetectedDrift(
                drift_type=DriftType.SYNTHESIS_EMPTY,
                severity=DriftSeverity.WARNING,
                description="Synthesis produced empty or minimal response",
                expected="Substantive response",
                actual=f"{response_length} characters",
                query_id=self.plan.query_id,
            )
            self.detected_drifts.append(drift)
            return drift

        return None

    def record_llm_call(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
        cost: float = 0,
    ) -> None:
        """Record an LLM call."""
        self.execution.add_llm_call(model, input_tokens, output_tokens, cost)

    def record_embedding(
        self,
        model: str,
        num_texts: int,
        tokens: int = 0,
    ) -> None:
        """Record an embedding operation."""
        self.execution.add_embedding(model, num_texts, tokens)

    def record_rerank(
        self,
        model: str,
        num_input: int,
        num_output: int,
        scores: List[float] | None = None,
    ) -> DetectedDrift | None:
        """Record a reranking operation and check for drift."""
        self.execution.add_rerank(model, num_input, num_output, scores)

        # Check for all filtered out
        if num_output == 0 and num_input > 0:
            drift = DetectedDrift(
                drift_type=DriftType.RERANK_FAILURE,
                severity=DriftSeverity.WARNING,
                description=f"Reranking filtered out all {num_input} nodes",
                expected="At least 1 node surviving reranking",
                actual="0 nodes after reranking",
                query_id=self.plan.query_id,
            )
            self.detected_drifts.append(drift)
            return drift

        return None

    def finalize(
        self,
        response: str | None = None,
        source_nodes: List[Any] | None = None,
        success: bool = True,
        total_duration_ms: float = 0,
    ) -> List[DetectedDrift]:
        """
        Finalize query tracking and perform final drift analysis.

        Returns all detected drifts.
        """
        source_node_count = len(source_nodes) if source_nodes else 0
        if response:
            self.execution.set_response(response, source_node_count)
        self.execution.success = success
        self.execution.total_duration_ms = total_duration_ms

        # Check for empty response
        if not response or len(response.strip()) < 10:
            drift = DetectedDrift(
                drift_type=DriftType.EMPTY_RESPONSE,
                severity=DriftSeverity.WARNING,
                description="Query returned empty or minimal response",
                expected="Substantive response",
                actual=f"{len(response) if response else 0} characters",
                query_id=self.plan.query_id,
            )
            self.detected_drifts.append(drift)

        # Check for missing source nodes
        if self.plan.expect_source_nodes and source_node_count == 0:
            drift = DetectedDrift(
                drift_type=DriftType.NO_SOURCE_NODES,
                severity=DriftSeverity.WARNING,
                description="Response generated without source nodes",
                expected="At least 1 source node",
                actual="0 source nodes",
                query_id=self.plan.query_id,
            )
            self.detected_drifts.append(drift)

        # Check for high empty retrieval rate
        if len(self.execution.retrievals) > 0:
            empty_rate = self.execution.empty_retrievals / len(self.execution.retrievals)
            if empty_rate > 0.5:
                drift = DetectedDrift(
                    drift_type=DriftType.EMPTY_RETRIEVAL,
                    severity=DriftSeverity.WARNING,
                    description=f"High empty retrieval rate: {empty_rate:.1%}",
                    expected="< 50% empty",
                    actual=f"{empty_rate:.1%}",
                    query_id=self.plan.query_id,
                )
                self.detected_drifts.append(drift)

        # Check overall success
        if not success:
            drift = DetectedDrift(
                drift_type=DriftType.QUERY_FAILURE,
                severity=DriftSeverity.ALERT,
                description="Query execution failed",
                expected="Successful completion",
                actual="Failed",
                query_id=self.plan.query_id,
            )
            self.detected_drifts.append(drift)

        return self.detected_drifts

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of expected vs actual execution."""
        return {
            "plan": self.plan.to_dict(),
            "execution": self.execution.to_dict(),
            "drifts": [d.to_dict() for d in self.detected_drifts],
            "drift_count": len(self.detected_drifts),
            "has_warnings": any(
                d.severity in [DriftSeverity.WARNING, DriftSeverity.ALERT]
                for d in self.detected_drifts
            ),
        }

    def get_drift_report(self) -> str:
        """Get a human-readable drift report."""
        if not self.detected_drifts:
            return "No drifts detected - query execution matched expectations"

        report = f"Detected {len(self.detected_drifts)} drift(s):\n"
        for i, drift in enumerate(self.detected_drifts, 1):
            report += f"\n{i}. [{drift.severity.value.upper()}] {drift.drift_type.value}"
            if drift.query_id:
                report += f" (query: {drift.query_id})"
            report += f"\n   {drift.description}\n"
            if drift.expected:
                report += f"   Expected: {drift.expected}\n"
            if drift.actual:
                report += f"   Actual: {drift.actual}\n"

        return report
