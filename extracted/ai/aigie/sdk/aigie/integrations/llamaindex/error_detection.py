"""
Error Detection and Monitoring for LlamaIndex RAG Workflows.

Provides comprehensive error detection, classification, and monitoring
for query engines, chat engines, retrieval, synthesis, and embeddings.
"""

import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class ErrorType(Enum):
    """Classification of error types for LlamaIndex."""

    # Transient errors (may succeed on retry)
    RATE_LIMIT = "rate_limit"
    TIMEOUT = "timeout"
    NETWORK = "network"
    SERVER_ERROR = "server_error"

    # Query errors
    QUERY_ERROR = "query_error"
    QUERY_PARSE = "query_parse"
    QUERY_TIMEOUT = "query_timeout"
    QUERY_EMPTY = "query_empty"

    # Retrieval errors
    RETRIEVAL_ERROR = "retrieval_error"
    RETRIEVAL_EMPTY = "retrieval_empty"
    RETRIEVAL_TIMEOUT = "retrieval_timeout"
    INDEX_ERROR = "index_error"
    INDEX_NOT_FOUND = "index_not_found"

    # Synthesis errors
    SYNTHESIS_ERROR = "synthesis_error"
    SYNTHESIS_EMPTY = "synthesis_empty"
    SYNTHESIS_TIMEOUT = "synthesis_timeout"

    # Embedding errors
    EMBEDDING_ERROR = "embedding_error"
    EMBEDDING_TIMEOUT = "embedding_timeout"
    EMBEDDING_DIMENSION = "embedding_dimension"

    # Reranking errors
    RERANK_ERROR = "rerank_error"
    RERANK_TIMEOUT = "rerank_timeout"

    # Node/Document errors
    NODE_ERROR = "node_error"
    NODE_NOT_FOUND = "node_not_found"
    DOCUMENT_ERROR = "document_error"
    DOCUMENT_PARSE = "document_parse"

    # Vector store errors
    VECTOR_STORE_ERROR = "vector_store_error"
    VECTOR_STORE_CONNECTION = "vector_store_connection"
    VECTOR_STORE_TIMEOUT = "vector_store_timeout"

    # LLM errors
    MODEL_ERROR = "model_error"
    CONTENT_FILTER = "content_filter"
    CONTEXT_LENGTH = "context_length"
    MAX_RETRIES = "max_retries"

    # Chat engine errors
    CHAT_ERROR = "chat_error"
    CHAT_HISTORY = "chat_history"

    # Authentication
    AUTHENTICATION = "auth"
    PERMISSION = "permission"

    # Unknown
    UNKNOWN = "unknown"


class ErrorSeverity(Enum):
    """Severity levels for errors."""

    LOW = "low"  # Minor issues, no action needed
    MEDIUM = "medium"  # May affect results, worth investigating
    HIGH = "high"  # Significant impact, needs attention
    CRITICAL = "critical"  # Execution failed, immediate action needed


@dataclass
class DetectedError:
    """Represents a detected error with full context."""

    error_type: ErrorType
    severity: ErrorSeverity
    message: str
    source: str  # e.g., "query:engine", "retriever:vector", "embedding:openai"
    is_transient: bool
    raw_error: str | None = None
    query_id: str | None = None
    index_id: str | None = None
    node_count: int | None = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "error_type": self.error_type.value,
            "severity": self.severity.value,
            "message": self.message,
            "source": self.source,
            "is_transient": self.is_transient,
            "raw_error": self.raw_error,
            "query_id": self.query_id,
            "index_id": self.index_id,
            "node_count": self.node_count,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }


@dataclass
class ErrorStats:
    """Statistics for error monitoring."""

    total_errors: int = 0
    errors_by_type: Dict[str, int] = field(default_factory=dict)
    errors_by_source: Dict[str, int] = field(default_factory=dict)
    errors_by_severity: Dict[str, int] = field(default_factory=dict)
    transient_errors: int = 0
    permanent_errors: int = 0
    retrieval_errors: int = 0
    synthesis_errors: int = 0
    embedding_errors: int = 0
    query_errors: int = 0
    recent_errors: List[DetectedError] = field(default_factory=list)

    def record(self, error: DetectedError) -> None:
        """Record an error in statistics."""
        self.total_errors += 1

        # By type
        type_key = error.error_type.value
        self.errors_by_type[type_key] = self.errors_by_type.get(type_key, 0) + 1

        # By source
        self.errors_by_source[error.source] = self.errors_by_source.get(error.source, 0) + 1

        # By severity
        sev_key = error.severity.value
        self.errors_by_severity[sev_key] = self.errors_by_severity.get(sev_key, 0) + 1

        # Transient vs permanent
        if error.is_transient:
            self.transient_errors += 1
        else:
            self.permanent_errors += 1

        # Track specific error categories
        if error.error_type in [
            ErrorType.RETRIEVAL_ERROR,
            ErrorType.RETRIEVAL_EMPTY,
            ErrorType.RETRIEVAL_TIMEOUT,
            ErrorType.INDEX_ERROR,
        ]:
            self.retrieval_errors += 1
        if error.error_type in [
            ErrorType.SYNTHESIS_ERROR,
            ErrorType.SYNTHESIS_EMPTY,
            ErrorType.SYNTHESIS_TIMEOUT,
        ]:
            self.synthesis_errors += 1
        if error.error_type in [
            ErrorType.EMBEDDING_ERROR,
            ErrorType.EMBEDDING_TIMEOUT,
            ErrorType.EMBEDDING_DIMENSION,
        ]:
            self.embedding_errors += 1
        if error.error_type in [
            ErrorType.QUERY_ERROR,
            ErrorType.QUERY_PARSE,
            ErrorType.QUERY_TIMEOUT,
            ErrorType.QUERY_EMPTY,
        ]:
            self.query_errors += 1

        # Keep last 100 errors
        self.recent_errors.append(error)
        if len(self.recent_errors) > 100:
            self.recent_errors = self.recent_errors[-100:]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "total_errors": self.total_errors,
            "errors_by_type": self.errors_by_type,
            "errors_by_source": self.errors_by_source,
            "errors_by_severity": self.errors_by_severity,
            "transient_errors": self.transient_errors,
            "permanent_errors": self.permanent_errors,
            "retrieval_errors": self.retrieval_errors,
            "synthesis_errors": self.synthesis_errors,
            "embedding_errors": self.embedding_errors,
            "query_errors": self.query_errors,
        }


# Error pattern matchers for LlamaIndex
ERROR_PATTERNS = [
    # Query errors
    (r"query\s+(?:error|failed|exception)", ErrorType.QUERY_ERROR, ErrorSeverity.HIGH, True),
    (
        r"query\s+(?:parse|parsing)\s+(?:error|failed)",
        ErrorType.QUERY_PARSE,
        ErrorSeverity.MEDIUM,
        False,
    ),
    (r"query\s+(?:timed?\s*out|timeout)", ErrorType.QUERY_TIMEOUT, ErrorSeverity.MEDIUM, True),
    (
        r"(?:empty|no)\s+query|query\s+(?:is\s+)?empty",
        ErrorType.QUERY_EMPTY,
        ErrorSeverity.MEDIUM,
        False,
    ),
    # Retrieval errors
    (
        r"retriev(?:al|er?)\s+(?:error|failed)",
        ErrorType.RETRIEVAL_ERROR,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"(?:no|empty|zero)\s+(?:results?|nodes?|documents?)\s+(?:found|retrieved)",
        ErrorType.RETRIEVAL_EMPTY,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"retriev(?:al|er?)\s+(?:timed?\s*out|timeout)",
        ErrorType.RETRIEVAL_TIMEOUT,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (r"index\s+(?:error|failed|exception)", ErrorType.INDEX_ERROR, ErrorSeverity.HIGH, True),
    (r"index\s+not\s+(?:found|exist)", ErrorType.INDEX_NOT_FOUND, ErrorSeverity.HIGH, False),
    # Synthesis errors
    (
        r"synthe(?:sis|size)\s+(?:error|failed)",
        ErrorType.SYNTHESIS_ERROR,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"(?:empty|no)\s+(?:response|synthesis)",
        ErrorType.SYNTHESIS_EMPTY,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"synthe(?:sis|size)\s+(?:timed?\s*out|timeout)",
        ErrorType.SYNTHESIS_TIMEOUT,
        ErrorSeverity.MEDIUM,
        True,
    ),
    # Embedding errors
    (r"embed(?:ding)?\s+(?:error|failed)", ErrorType.EMBEDDING_ERROR, ErrorSeverity.MEDIUM, True),
    (
        r"embed(?:ding)?\s+(?:timed?\s*out|timeout)",
        ErrorType.EMBEDDING_TIMEOUT,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"(?:embedding\s+)?dimension\s+(?:error|mismatch)",
        ErrorType.EMBEDDING_DIMENSION,
        ErrorSeverity.HIGH,
        False,
    ),
    # Reranking errors
    (r"rerank\s+(?:error|failed)", ErrorType.RERANK_ERROR, ErrorSeverity.MEDIUM, True),
    (r"rerank\s+(?:timed?\s*out|timeout)", ErrorType.RERANK_TIMEOUT, ErrorSeverity.MEDIUM, True),
    # Node/Document errors
    (r"node\s+(?:error|failed)", ErrorType.NODE_ERROR, ErrorSeverity.MEDIUM, True),
    (r"node\s+not\s+(?:found|exist)", ErrorType.NODE_NOT_FOUND, ErrorSeverity.HIGH, False),
    (r"document\s+(?:error|failed)", ErrorType.DOCUMENT_ERROR, ErrorSeverity.MEDIUM, True),
    (
        r"document\s+(?:parse|parsing)\s+(?:error|failed)",
        ErrorType.DOCUMENT_PARSE,
        ErrorSeverity.MEDIUM,
        False,
    ),
    # Vector store errors
    (r"vector\s*store\s+(?:error|failed)", ErrorType.VECTOR_STORE_ERROR, ErrorSeverity.HIGH, True),
    (
        r"vector\s*store\s+connection\s+(?:error|failed)",
        ErrorType.VECTOR_STORE_CONNECTION,
        ErrorSeverity.HIGH,
        True,
    ),
    (
        r"vector\s*store\s+(?:timed?\s*out|timeout)",
        ErrorType.VECTOR_STORE_TIMEOUT,
        ErrorSeverity.MEDIUM,
        True,
    ),
    # Chat errors
    (r"chat\s+(?:error|failed)", ErrorType.CHAT_ERROR, ErrorSeverity.MEDIUM, True),
    (
        r"chat\s+history\s+(?:error|failed|invalid)",
        ErrorType.CHAT_HISTORY,
        ErrorSeverity.MEDIUM,
        False,
    ),
    # Rate limiting
    (r"rate.?limit|too\s+many\s+requests|429", ErrorType.RATE_LIMIT, ErrorSeverity.MEDIUM, True),
    # Timeout
    (
        r"(?:request|connection|operation)\s+(?:timed?.?out|timeout)",
        ErrorType.TIMEOUT,
        ErrorSeverity.MEDIUM,
        True,
    ),
    # Network
    (
        r"connection\s+(?:refused|reset|failed)|network\s+error",
        ErrorType.NETWORK,
        ErrorSeverity.MEDIUM,
        True,
    ),
    # Server errors
    (
        r"(?:500|502|503|504)(?:\s|:|$)|server\s+error",
        ErrorType.SERVER_ERROR,
        ErrorSeverity.MEDIUM,
        True,
    ),
    # Authentication
    (
        r"(?:401|unauthorized)|invalid\s+(?:api.?key|token)",
        ErrorType.AUTHENTICATION,
        ErrorSeverity.HIGH,
        False,
    ),
    (r"(?:403|forbidden)", ErrorType.PERMISSION, ErrorSeverity.HIGH, False),
    # Content filter
    (
        r"content\s+filter|content\s+policy|moderation",
        ErrorType.CONTENT_FILTER,
        ErrorSeverity.HIGH,
        False,
    ),
    # Context length
    (
        r"context.?length|max.?tokens?\s+exceeded|token\s+limit",
        ErrorType.CONTEXT_LENGTH,
        ErrorSeverity.HIGH,
        False,
    ),
    # Max retries
    (
        r"max(?:imum)?\s+retries?\s+(?:exceeded|reached)",
        ErrorType.MAX_RETRIES,
        ErrorSeverity.HIGH,
        False,
    ),
    # Model errors
    (r"model\s+(?:error|unavailable|not\s+found)", ErrorType.MODEL_ERROR, ErrorSeverity.HIGH, True),
]


class ErrorDetector:
    """
    Detects and classifies errors from LlamaIndex RAG workflows.

    Provides:
    - Pattern-based error detection
    - Error classification (type, severity, transient/permanent)
    - Error statistics and monitoring
    """

    def __init__(self):
        self.stats = ErrorStats()
        self._compiled_patterns = [
            (re.compile(pattern, re.IGNORECASE), error_type, severity, is_transient)
            for pattern, error_type, severity, is_transient in ERROR_PATTERNS
        ]

    def detect_from_text(
        self,
        text: str,
        source: str,
        context: Dict[str, Any] | None = None,
    ) -> DetectedError | None:
        """
        Detect errors from text content.

        Args:
            text: Text to analyze for errors
            source: Source identifier (e.g., "retriever:vector")
            context: Additional context for the error

        Returns:
            DetectedError if an error is found, None otherwise
        """
        if not text:
            return None

        context = context or {}

        # Try to match error patterns
        for pattern, error_type, severity, is_transient in self._compiled_patterns:
            if pattern.search(text):
                error = DetectedError(
                    error_type=error_type,
                    severity=severity,
                    message=self._extract_error_message(text),
                    source=source,
                    is_transient=is_transient,
                    raw_error=text[:500] if len(text) > 500 else text,
                    query_id=context.get("query_id"),
                    index_id=context.get("index_id"),
                    node_count=context.get("node_count"),
                    metadata=context,
                )
                self.stats.record(error)
                logger.warning(
                    f"[AIGIE] LlamaIndex error detected: {error_type.value} from {source}"
                )
                return error

        return None

    def detect_from_query_result(
        self,
        query_id: str,
        query_str: str,
        response: str | None = None,
        source_nodes: List[Any] | None = None,
        error: str | None = None,
    ) -> DetectedError | None:
        """
        Detect errors from query execution.

        Args:
            query_id: Query identifier
            query_str: The query string
            response: Query response
            source_nodes: Source nodes used
            error: Error message if failed

        Returns:
            DetectedError if an error is found, None otherwise
        """
        source = "query"
        context = {
            "query_id": query_id,
            "query_preview": query_str[:100] if query_str else None,
            "node_count": len(source_nodes) if source_nodes else 0,
        }

        if error:
            detected = self.detect_from_text(error, source, context)
            if detected:
                return detected

            # Create generic query error
            detected = DetectedError(
                error_type=ErrorType.QUERY_ERROR,
                severity=ErrorSeverity.HIGH,
                message=f"Query failed: {error[:200]}",
                source=source,
                is_transient=True,
                raw_error=error[:500],
                query_id=query_id,
                metadata=context,
            )
            self.stats.record(detected)
            return detected

        # Check for empty response
        if response is not None and len(response.strip()) < 5:
            detected = DetectedError(
                error_type=ErrorType.QUERY_EMPTY,
                severity=ErrorSeverity.MEDIUM,
                message="Query returned empty or minimal response",
                source=source,
                is_transient=True,
                query_id=query_id,
                metadata=context,
            )
            self.stats.record(detected)
            return detected

        return None

    def detect_from_retrieval(
        self,
        retrieve_id: str,
        retriever_type: str,
        nodes: List[Any] | None = None,
        scores: List[float] | None = None,
        error: str | None = None,
    ) -> DetectedError | None:
        """
        Detect errors from retrieval operations.

        Args:
            retrieve_id: Retrieval identifier
            retriever_type: Type of retriever (vector, keyword, hybrid)
            nodes: Retrieved nodes
            scores: Similarity scores
            error: Error message if failed

        Returns:
            DetectedError if an error is found, None otherwise
        """
        source = f"retriever:{retriever_type}"
        context = {
            "retrieve_id": retrieve_id,
            "retriever_type": retriever_type,
            "node_count": len(nodes) if nodes else 0,
        }

        if error:
            detected = self.detect_from_text(error, source, context)
            if detected:
                return detected

            # Create generic retrieval error
            detected = DetectedError(
                error_type=ErrorType.RETRIEVAL_ERROR,
                severity=ErrorSeverity.MEDIUM,
                message=f"Retrieval failed ({retriever_type}): {error[:150]}",
                source=source,
                is_transient=True,
                raw_error=error[:500],
                node_count=0,
                metadata=context,
            )
            self.stats.record(detected)
            return detected

        # Check for empty results
        if nodes is not None and len(nodes) == 0:
            detected = DetectedError(
                error_type=ErrorType.RETRIEVAL_EMPTY,
                severity=ErrorSeverity.MEDIUM,
                message=f"Retrieval ({retriever_type}) returned no results",
                source=source,
                is_transient=True,
                node_count=0,
                metadata=context,
            )
            self.stats.record(detected)
            return detected

        return None

    def detect_from_synthesis(
        self,
        synth_id: str,
        response: str | None = None,
        error: str | None = None,
    ) -> DetectedError | None:
        """
        Detect errors from synthesis operations.

        Args:
            synth_id: Synthesis identifier
            response: Synthesized response
            error: Error message if failed

        Returns:
            DetectedError if an error is found, None otherwise
        """
        source = "synthesis"
        context = {"synth_id": synth_id}

        if error:
            detected = self.detect_from_text(error, source, context)
            if detected:
                return detected

            # Create generic synthesis error
            detected = DetectedError(
                error_type=ErrorType.SYNTHESIS_ERROR,
                severity=ErrorSeverity.MEDIUM,
                message=f"Synthesis failed: {error[:150]}",
                source=source,
                is_transient=True,
                raw_error=error[:500],
                metadata=context,
            )
            self.stats.record(detected)
            return detected

        # Check for empty synthesis
        if response is not None and len(response.strip()) < 5:
            detected = DetectedError(
                error_type=ErrorType.SYNTHESIS_EMPTY,
                severity=ErrorSeverity.MEDIUM,
                message="Synthesis produced empty or minimal response",
                source=source,
                is_transient=True,
                metadata=context,
            )
            self.stats.record(detected)
            return detected

        return None

    def detect_from_embedding(
        self,
        embed_id: str,
        model: str,
        num_texts: int,
        error: str | None = None,
    ) -> DetectedError | None:
        """
        Detect errors from embedding operations.

        Args:
            embed_id: Embedding identifier
            model: Embedding model name
            num_texts: Number of texts embedded
            error: Error message if failed

        Returns:
            DetectedError if an error is found, None otherwise
        """
        source = f"embedding:{model}"
        context = {
            "embed_id": embed_id,
            "model": model,
            "num_texts": num_texts,
        }

        if error:
            detected = self.detect_from_text(error, source, context)
            if detected:
                return detected

            # Create generic embedding error
            detected = DetectedError(
                error_type=ErrorType.EMBEDDING_ERROR,
                severity=ErrorSeverity.MEDIUM,
                message=f"Embedding failed ({model}): {error[:150]}",
                source=source,
                is_transient=True,
                raw_error=error[:500],
                metadata=context,
            )
            self.stats.record(detected)
            return detected

        return None

    def detect_from_llm_error(
        self,
        error: str,
        model: str | None = None,
    ) -> DetectedError:
        """
        Detect errors from LLM calls.

        Args:
            error: Error message
            model: Model name

        Returns:
            DetectedError for the LLM error
        """
        source = f"llm:{model}" if model else "llm"
        context = {"model": model}

        detected = self.detect_from_text(error, source, context)
        if detected:
            return detected

        # Default LLM error
        return DetectedError(
            error_type=ErrorType.MODEL_ERROR,
            severity=ErrorSeverity.HIGH,
            message=f"LLM error: {error[:200]}",
            source=source,
            is_transient=True,
            raw_error=error[:500],
            metadata=context,
        )

    def detect_from_exception(
        self,
        exception: Exception,
        source: str,
        context: Dict[str, Any] | None = None,
    ) -> DetectedError:
        """
        Create DetectedError from a Python exception.

        Args:
            exception: The exception that occurred
            source: Source identifier
            context: Additional context

        Returns:
            DetectedError for the exception
        """
        exc_type = type(exception).__name__
        exc_message = str(exception)
        context = context or {}

        # Try to classify the exception
        error = self.detect_from_text(exc_message, source, context)
        if error:
            error.metadata["exception_type"] = exc_type
            return error

        # Default classification based on exception type
        error_type = ErrorType.UNKNOWN
        severity = ErrorSeverity.HIGH
        is_transient = False

        exc_type_lower = exc_type.lower()
        if "timeout" in exc_type_lower:
            error_type = ErrorType.TIMEOUT
            is_transient = True
        elif "connection" in exc_type_lower or "network" in exc_type_lower:
            error_type = ErrorType.NETWORK
            is_transient = True
        elif "index" in exc_type_lower:
            error_type = ErrorType.INDEX_ERROR

        error = DetectedError(
            error_type=error_type,
            severity=severity,
            message=f"{exc_type}: {exc_message[:200]}",
            source=source,
            is_transient=is_transient,
            raw_error=f"{exc_type}: {exc_message}",
            query_id=context.get("query_id"),
            index_id=context.get("index_id"),
            metadata={**context, "exception_type": exc_type},
        )
        self.stats.record(error)
        return error

    def _extract_error_message(self, text: str) -> str:
        """Extract a clean error message from text."""
        patterns = [
            r"error[:\s]+(.+?)(?:\.|$)",
            r"failed[:\s]+(.+?)(?:\.|$)",
            r"exception[:\s]+(.+?)(?:\.|$)",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                msg = match.group(1).strip()
                if len(msg) > 10:
                    return msg[:200]

        first_line = text.split("\n")[0].strip()
        return first_line[:200] if first_line else text[:200]

    def get_stats(self) -> Dict[str, Any]:
        """Get current error statistics."""
        return self.stats.to_dict()

    def get_recent_errors(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent errors as dictionaries."""
        return [e.to_dict() for e in self.stats.recent_errors[-limit:]]

    def get_error_summary(self) -> str:
        """Get a human-readable error summary."""
        if self.stats.total_errors == 0:
            return "No errors detected"

        summary = f"Total errors: {self.stats.total_errors}"
        summary += f" (query: {self.stats.query_errors}, retrieval: {self.stats.retrieval_errors}, synthesis: {self.stats.synthesis_errors}, embedding: {self.stats.embedding_errors})"

        if self.stats.errors_by_type:
            top_types = sorted(self.stats.errors_by_type.items(), key=lambda x: x[1], reverse=True)[
                :3
            ]
            summary += f"\nTop error types: {', '.join(f'{t}({c})' for t, c in top_types)}"

        return summary


# Global error detector instance
_global_detector: ErrorDetector | None = None


def get_error_detector() -> ErrorDetector:
    """Get or create the global error detector instance."""
    global _global_detector
    if _global_detector is None:
        _global_detector = ErrorDetector()
    return _global_detector


def reset_error_detector() -> None:
    """Reset the global error detector (for testing)."""
    global _global_detector
    _global_detector = None
