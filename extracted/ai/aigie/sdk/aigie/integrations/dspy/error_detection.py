"""
Error Detection and Monitoring for DSPy Workflows.

Provides comprehensive error detection, classification, and monitoring
for DSPy modules, predictions, retrievers, and optimizers.
"""

import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class ErrorType(Enum):
    """Classification of error types for DSPy."""

    # Transient errors (may succeed on retry)
    RATE_LIMIT = "rate_limit"
    TIMEOUT = "timeout"
    NETWORK = "network"
    SERVER_ERROR = "server_error"

    # Module errors
    MODULE_ERROR = "module_error"
    MODULE_NOT_FOUND = "module_not_found"
    MODULE_CONFIGURATION = "module_config"
    MODULE_FORWARD = "module_forward"

    # Signature errors
    SIGNATURE_ERROR = "signature_error"
    SIGNATURE_INVALID = "signature_invalid"
    SIGNATURE_MISMATCH = "signature_mismatch"
    INPUT_FIELD_MISSING = "input_field_missing"
    OUTPUT_FIELD_MISSING = "output_field_missing"

    # Prediction errors
    PREDICTION_ERROR = "prediction_error"
    PREDICTION_EMPTY = "prediction_empty"
    PREDICTION_PARSE = "prediction_parse"
    PREDICTION_VALIDATION = "prediction_validation"

    # Retriever errors
    RETRIEVER_ERROR = "retriever_error"
    RETRIEVER_EMPTY = "retriever_empty"
    RETRIEVER_TIMEOUT = "retriever_timeout"
    INDEX_ERROR = "index_error"

    # Optimization errors
    OPTIMIZATION_ERROR = "optimization_error"
    METRIC_ERROR = "metric_error"
    COMPILATION_ERROR = "compilation_error"
    BOOTSTRAP_ERROR = "bootstrap_error"

    # Reasoning errors (CoT, ReAct)
    REASONING_ERROR = "reasoning_error"
    COT_ERROR = "cot_error"
    REACT_ERROR = "react_error"
    TOOL_ERROR = "tool_error"

    # LLM errors
    MODEL_ERROR = "model_error"
    CONTENT_FILTER = "content_filter"
    CONTEXT_LENGTH = "context_length"
    MAX_RETRIES = "max_retries"

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
    source: str  # e.g., "module:ChainOfThought", "retriever:ColBERT"
    is_transient: bool
    raw_error: str | None = None
    module_name: str | None = None
    module_type: str | None = None
    signature: str | None = None
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
            "module_name": self.module_name,
            "module_type": self.module_type,
            "signature": self.signature,
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
    errors_by_module: Dict[str, int] = field(default_factory=dict)
    transient_errors: int = 0
    permanent_errors: int = 0
    prediction_errors: int = 0
    retriever_errors: int = 0
    optimization_errors: int = 0
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

        # By module
        if error.module_name:
            self.errors_by_module[error.module_name] = (
                self.errors_by_module.get(error.module_name, 0) + 1
            )

        # Transient vs permanent
        if error.is_transient:
            self.transient_errors += 1
        else:
            self.permanent_errors += 1

        # Track specific error categories
        if error.error_type in [
            ErrorType.PREDICTION_ERROR,
            ErrorType.PREDICTION_EMPTY,
            ErrorType.PREDICTION_PARSE,
            ErrorType.PREDICTION_VALIDATION,
        ]:
            self.prediction_errors += 1
        if error.error_type in [
            ErrorType.RETRIEVER_ERROR,
            ErrorType.RETRIEVER_EMPTY,
            ErrorType.RETRIEVER_TIMEOUT,
            ErrorType.INDEX_ERROR,
        ]:
            self.retriever_errors += 1
        if error.error_type in [
            ErrorType.OPTIMIZATION_ERROR,
            ErrorType.METRIC_ERROR,
            ErrorType.COMPILATION_ERROR,
            ErrorType.BOOTSTRAP_ERROR,
        ]:
            self.optimization_errors += 1

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
            "errors_by_module": self.errors_by_module,
            "transient_errors": self.transient_errors,
            "permanent_errors": self.permanent_errors,
            "prediction_errors": self.prediction_errors,
            "retriever_errors": self.retriever_errors,
            "optimization_errors": self.optimization_errors,
        }


# Error pattern matchers for DSPy
ERROR_PATTERNS = [
    # Module errors
    (r"module\s+(?:error|failed|exception)", ErrorType.MODULE_ERROR, ErrorSeverity.HIGH, True),
    (r"module\s+not\s+(?:found|defined)", ErrorType.MODULE_NOT_FOUND, ErrorSeverity.HIGH, False),
    (
        r"(?:invalid|bad)\s+module\s+(?:configuration|config)",
        ErrorType.MODULE_CONFIGURATION,
        ErrorSeverity.HIGH,
        False,
    ),
    (
        r"forward\s+(?:error|failed)|__call__\s+(?:error|failed)",
        ErrorType.MODULE_FORWARD,
        ErrorSeverity.HIGH,
        True,
    ),
    # Signature errors
    (
        r"signature\s+(?:error|invalid|mismatch)",
        ErrorType.SIGNATURE_ERROR,
        ErrorSeverity.HIGH,
        False,
    ),
    (
        r"(?:input|field)\s+(?:missing|required|not\s+found)",
        ErrorType.INPUT_FIELD_MISSING,
        ErrorSeverity.MEDIUM,
        False,
    ),
    (
        r"output\s+(?:field\s+)?(?:missing|not\s+found)",
        ErrorType.OUTPUT_FIELD_MISSING,
        ErrorSeverity.MEDIUM,
        True,
    ),
    # Prediction errors
    (r"prediction\s+(?:error|failed)", ErrorType.PREDICTION_ERROR, ErrorSeverity.MEDIUM, True),
    (r"(?:empty|no)\s+prediction", ErrorType.PREDICTION_EMPTY, ErrorSeverity.MEDIUM, True),
    (
        r"(?:parse|parsing)\s+(?:error|failed)|could\s+not\s+parse",
        ErrorType.PREDICTION_PARSE,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"(?:validation|validate)\s+(?:error|failed)",
        ErrorType.PREDICTION_VALIDATION,
        ErrorSeverity.MEDIUM,
        True,
    ),
    # Retriever errors
    (r"retriever?\s+(?:error|failed)", ErrorType.RETRIEVER_ERROR, ErrorSeverity.MEDIUM, True),
    (
        r"(?:no|empty)\s+(?:results?|passages?|documents?)\s+(?:found|retrieved)",
        ErrorType.RETRIEVER_EMPTY,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (
        r"retriever?\s+(?:timed?\s*out|timeout)",
        ErrorType.RETRIEVER_TIMEOUT,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (r"index\s+(?:error|not\s+found|missing)", ErrorType.INDEX_ERROR, ErrorSeverity.HIGH, False),
    # Optimization errors
    (
        r"optim(?:ization|izer)?\s+(?:error|failed)",
        ErrorType.OPTIMIZATION_ERROR,
        ErrorSeverity.HIGH,
        True,
    ),
    (r"metric\s+(?:error|failed|invalid)", ErrorType.METRIC_ERROR, ErrorSeverity.HIGH, False),
    (
        r"compil(?:ation|e)\s+(?:error|failed)",
        ErrorType.COMPILATION_ERROR,
        ErrorSeverity.HIGH,
        True,
    ),
    (r"bootstrap\s+(?:error|failed)", ErrorType.BOOTSTRAP_ERROR, ErrorSeverity.HIGH, True),
    # Reasoning errors
    (
        r"(?:reasoning|thought)\s+(?:error|failed)",
        ErrorType.REASONING_ERROR,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (r"chain.?of.?thought\s+(?:error|failed)", ErrorType.COT_ERROR, ErrorSeverity.MEDIUM, True),
    (
        r"react\s+(?:error|failed)|action\s+(?:error|failed)",
        ErrorType.REACT_ERROR,
        ErrorSeverity.MEDIUM,
        True,
    ),
    (r"tool\s+(?:error|failed|not\s+found)", ErrorType.TOOL_ERROR, ErrorSeverity.MEDIUM, True),
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
    Detects and classifies errors from DSPy workflows.

    Provides:
    - Pattern-based error detection
    - Error classification (type, severity, transient/permanent)
    - Per-module error tracking
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
            source: Source identifier (e.g., "module:ChainOfThought")
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
                    module_name=context.get("module_name"),
                    module_type=context.get("module_type"),
                    signature=context.get("signature"),
                    metadata=context,
                )
                self.stats.record(error)
                logger.warning(f"[AIGIE] DSPy error detected: {error_type.value} from {source}")
                return error

        return None

    def detect_from_module_result(
        self,
        module_name: str,
        module_type: str,
        signature: str | None = None,
        output: Any = None,
        error: str | None = None,
    ) -> DetectedError | None:
        """
        Detect errors from module execution.

        Args:
            module_name: Name of the module
            module_type: Type of module (predict, cot, react, etc.)
            signature: Module signature
            output: Module output (Prediction object)
            error: Error message if failed

        Returns:
            DetectedError if an error is found, None otherwise
        """
        source = f"module:{module_name}"
        context = {
            "module_name": module_name,
            "module_type": module_type,
            "signature": signature,
        }

        if error:
            detected = self.detect_from_text(error, source, context)
            if detected:
                return detected

            # Create generic module error
            detected = DetectedError(
                error_type=ErrorType.MODULE_ERROR,
                severity=ErrorSeverity.HIGH,
                message=f"Module '{module_name}' ({module_type}) failed: {error[:150]}",
                source=source,
                is_transient=True,
                raw_error=error[:500],
                module_name=module_name,
                module_type=module_type,
                signature=signature,
                metadata=context,
            )
            self.stats.record(detected)
            return detected

        return None

    def detect_from_prediction(
        self,
        module_name: str,
        model: str | None = None,
        output_fields: Dict[str, Any] | None = None,
        error: str | None = None,
    ) -> DetectedError | None:
        """
        Detect errors from LLM prediction.

        Args:
            module_name: Name of the calling module
            model: LLM model name
            output_fields: Predicted output fields
            error: Error message if failed

        Returns:
            DetectedError if an error is found, None otherwise
        """
        source = f"prediction:{model}" if model else f"prediction:{module_name}"
        context = {
            "module_name": module_name,
            "model": model,
        }

        if error:
            detected = self.detect_from_text(error, source, context)
            if detected:
                return detected

            # Create generic prediction error
            detected = DetectedError(
                error_type=ErrorType.PREDICTION_ERROR,
                severity=ErrorSeverity.MEDIUM,
                message=f"Prediction failed for '{module_name}': {error[:150]}",
                source=source,
                is_transient=True,
                raw_error=error[:500],
                module_name=module_name,
                metadata=context,
            )
            self.stats.record(detected)
            return detected

        # Check for empty prediction
        if output_fields is not None and not output_fields:
            detected = DetectedError(
                error_type=ErrorType.PREDICTION_EMPTY,
                severity=ErrorSeverity.MEDIUM,
                message=f"Empty prediction from '{module_name}'",
                source=source,
                is_transient=True,
                module_name=module_name,
                metadata=context,
            )
            self.stats.record(detected)
            return detected

        return None

    def detect_from_retrieval(
        self,
        retriever_name: str,
        query: str | None = None,
        passages: List[Any] | None = None,
        error: str | None = None,
    ) -> DetectedError | None:
        """
        Detect errors from retrieval operations.

        Args:
            retriever_name: Name of the retriever
            query: Query string
            passages: Retrieved passages
            error: Error message if failed

        Returns:
            DetectedError if an error is found, None otherwise
        """
        source = f"retriever:{retriever_name}"
        context = {
            "retriever_name": retriever_name,
            "query_preview": query[:100] if query else None,
        }

        if error:
            detected = self.detect_from_text(error, source, context)
            if detected:
                return detected

            # Create generic retriever error
            detected = DetectedError(
                error_type=ErrorType.RETRIEVER_ERROR,
                severity=ErrorSeverity.MEDIUM,
                message=f"Retriever '{retriever_name}' failed: {error[:150]}",
                source=source,
                is_transient=True,
                raw_error=error[:500],
                module_name=retriever_name,
                module_type="retriever",
                metadata=context,
            )
            self.stats.record(detected)
            return detected

        # Check for empty results
        if passages is not None and len(passages) == 0:
            detected = DetectedError(
                error_type=ErrorType.RETRIEVER_EMPTY,
                severity=ErrorSeverity.MEDIUM,
                message=f"Retriever '{retriever_name}' returned no results",
                source=source,
                is_transient=True,
                module_name=retriever_name,
                module_type="retriever",
                metadata=context,
            )
            self.stats.record(detected)
            return detected

        return None

    def detect_from_optimization(
        self,
        optimizer_name: str,
        metric_name: str | None = None,
        best_score: float | None = None,
        error: str | None = None,
    ) -> DetectedError | None:
        """
        Detect errors from optimization/compilation.

        Args:
            optimizer_name: Name of the optimizer
            metric_name: Metric being optimized
            best_score: Best score achieved
            error: Error message if failed

        Returns:
            DetectedError if an error is found, None otherwise
        """
        source = f"optimizer:{optimizer_name}"
        context = {
            "optimizer_name": optimizer_name,
            "metric_name": metric_name,
            "best_score": best_score,
        }

        if error:
            detected = self.detect_from_text(error, source, context)
            if detected:
                return detected

            # Create generic optimization error
            detected = DetectedError(
                error_type=ErrorType.OPTIMIZATION_ERROR,
                severity=ErrorSeverity.HIGH,
                message=f"Optimizer '{optimizer_name}' failed: {error[:150]}",
                source=source,
                is_transient=True,
                raw_error=error[:500],
                module_name=optimizer_name,
                module_type="optimizer",
                metadata=context,
            )
            self.stats.record(detected)
            return detected

        return None

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
        elif "validation" in exc_type_lower:
            error_type = ErrorType.PREDICTION_VALIDATION
            is_transient = True
        elif "signature" in exc_type_lower:
            error_type = ErrorType.SIGNATURE_ERROR

        error = DetectedError(
            error_type=error_type,
            severity=severity,
            message=f"{exc_type}: {exc_message[:200]}",
            source=source,
            is_transient=is_transient,
            raw_error=f"{exc_type}: {exc_message}",
            module_name=context.get("module_name"),
            module_type=context.get("module_type"),
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

    def get_errors_by_module(self) -> Dict[str, int]:
        """Get error counts by module."""
        return self.stats.errors_by_module.copy()

    def get_error_summary(self) -> str:
        """Get a human-readable error summary."""
        if self.stats.total_errors == 0:
            return "No errors detected"

        summary = f"Total errors: {self.stats.total_errors}"
        summary += f" (prediction: {self.stats.prediction_errors}, retriever: {self.stats.retriever_errors}, optimization: {self.stats.optimization_errors})"

        if self.stats.errors_by_type:
            top_types = sorted(self.stats.errors_by_type.items(), key=lambda x: x[1], reverse=True)[
                :3
            ]
            summary += f"\nTop error types: {', '.join(f'{t}({c})' for t, c in top_types)}"

        if self.stats.errors_by_module:
            top_modules = sorted(
                self.stats.errors_by_module.items(), key=lambda x: x[1], reverse=True
            )[:3]
            summary += (
                f"\nTop modules with errors: {', '.join(f'{m}({c})' for m, c in top_modules)}"
            )

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
