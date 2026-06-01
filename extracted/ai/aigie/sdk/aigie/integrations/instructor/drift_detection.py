"""
Drift Detection for Instructor Structured Output Workflows.

Tracks schema expectations vs actual extraction results to detect drifts.
Useful for monitoring extraction reliability and output quality.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Set

logger = logging.getLogger(__name__)


class DriftType(Enum):
    """Types of behavioral drift in structured output extraction."""

    # Schema drifts
    MISSING_FIELD = "missing_field"  # Expected field not in output
    EXTRA_FIELD = "extra_field"  # Unexpected field in output
    TYPE_MISMATCH = "type_mismatch"  # Field type differs from schema

    # Value drifts
    NULL_VALUE = "null_value"  # Expected value is null
    EMPTY_VALUE = "empty_value"  # Expected value is empty
    VALUE_TRUNCATED = "value_truncated"  # Value appears truncated
    VALUE_RANGE = "value_range"  # Value outside expected range

    # Retry drifts
    RETRY_REQUIRED = "retry_required"  # Needed retry to get valid output
    MAX_RETRIES = "max_retries"  # Hit max retry limit

    # Quality drifts
    LOW_CONFIDENCE = "low_confidence"  # Model expressed low confidence
    INCOMPLETE_EXTRACTION = "incomplete"  # Extraction appears incomplete
    HALLUCINATION = "hallucination"  # Possible hallucinated content

    # Performance drifts
    DURATION_ANOMALY = "duration_anomaly"  # Extraction took unusually long
    TOKEN_ANOMALY = "token_anomaly"  # Unusual token usage


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
    field_name: str | None = None
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
            "field_name": self.field_name,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }


@dataclass
class ExtractionPlan:
    """Captures the expected extraction schema and behavior."""

    # Schema info
    model_name: str | None = None
    schema: Dict[str, Any] | None = None
    required_fields: Set[str] = field(default_factory=set)
    optional_fields: Set[str] = field(default_factory=set)
    field_types: Dict[str, str] = field(default_factory=dict)

    # Extraction settings
    max_retries: int = 1
    validation_context: str | None = None

    # Metadata
    timestamp: datetime = field(default_factory=datetime.now)
    llm_model: str | None = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "model_name": self.model_name,
            "schema_preview": str(self.schema)[:500] if self.schema else None,
            "required_fields": list(self.required_fields),
            "optional_fields": list(self.optional_fields),
            "field_types": self.field_types,
            "max_retries": self.max_retries,
            "timestamp": self.timestamp.isoformat(),
            "llm_model": self.llm_model,
        }


@dataclass
class ExtractionTrace:
    """Tracks actual extraction for comparison against plan."""

    # Extraction events
    attempts: List[Dict[str, Any]] = field(default_factory=list)
    validation_errors: List[Dict[str, Any]] = field(default_factory=list)

    # Metrics
    total_duration_ms: float = 0
    total_tokens: int = 0
    total_cost: float = 0
    retry_count: int = 0
    success: bool = False

    # Results
    final_result: Dict[str, Any] | None = None
    extracted_fields: Set[str] = field(default_factory=set)
    null_fields: Set[str] = field(default_factory=set)
    empty_fields: Set[str] = field(default_factory=set)

    def add_attempt(
        self,
        attempt_number: int,
        success: bool,
        duration_ms: float = 0,
        validation_error: str | None = None,
    ) -> None:
        """Record an extraction attempt."""
        self.attempts.append(
            {
                "attempt": attempt_number,
                "success": success,
                "duration_ms": duration_ms,
                "validation_error": validation_error[:200] if validation_error else None,
                "timestamp": datetime.now().isoformat(),
            }
        )
        if not success and attempt_number > 0:
            self.retry_count += 1
        if validation_error:
            self.validation_errors.append(
                {
                    "attempt": attempt_number,
                    "error": validation_error[:500],
                }
            )

    def set_result(self, result: Any) -> None:
        """Set the final extraction result."""
        self.success = True

        if hasattr(result, "model_dump"):
            self.final_result = result.model_dump()
        elif hasattr(result, "dict"):
            self.final_result = result.dict()
        elif isinstance(result, dict):
            self.final_result = result
        else:
            self.final_result = {"value": str(result)}

        # Analyze result fields
        if isinstance(self.final_result, dict):
            for key, value in self.final_result.items():
                self.extracted_fields.add(key)
                if value is None:
                    self.null_fields.add(key)
                elif value == "" or value == [] or value == {}:
                    self.empty_fields.add(key)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "attempts": self.attempts,
            "attempt_count": len(self.attempts),
            "validation_error_count": len(self.validation_errors),
            "total_duration_ms": self.total_duration_ms,
            "total_tokens": self.total_tokens,
            "total_cost": self.total_cost,
            "retry_count": self.retry_count,
            "success": self.success,
            "extracted_fields": list(self.extracted_fields),
            "null_fields": list(self.null_fields),
            "empty_fields": list(self.empty_fields),
        }


class DriftDetector:
    """
    Detects drift between expected schema and actual extraction results.

    Captures:
    - Schema expectations from Pydantic models
    - Actual extraction results and validation errors
    - Compares and reports deviations
    """

    def __init__(self):
        self.plan = ExtractionPlan()
        self.execution = ExtractionTrace()
        self.detected_drifts: List[DetectedDrift] = []

    def capture_schema(
        self,
        model_class: Any,
        max_retries: int = 1,
        llm_model: str | None = None,
    ) -> None:
        """
        Capture schema from a Pydantic model.

        Args:
            model_class: Pydantic model class
            max_retries: Maximum retries configured
            llm_model: LLM model being used
        """
        self.plan.model_name = getattr(model_class, "__name__", str(model_class))
        self.plan.max_retries = max_retries
        self.plan.llm_model = llm_model

        # Extract schema
        if hasattr(model_class, "model_json_schema"):
            try:
                self.plan.schema = model_class.model_json_schema()
            except Exception:
                pass

        # Extract field info
        if hasattr(model_class, "model_fields"):
            try:
                for name, field_info in model_class.model_fields.items():
                    # Check if required
                    if field_info.is_required():
                        self.plan.required_fields.add(name)
                    else:
                        self.plan.optional_fields.add(name)

                    # Get type
                    annotation = field_info.annotation
                    if annotation:
                        self.plan.field_types[name] = str(annotation)
            except Exception:
                pass

    def record_attempt(
        self,
        attempt_number: int,
        success: bool,
        duration_ms: float = 0,
        validation_error: str | None = None,
    ) -> DetectedDrift | None:
        """Record an extraction attempt and check for drift."""
        self.execution.add_attempt(attempt_number, success, duration_ms, validation_error)

        # Check for retry drift
        if not success and attempt_number > 0:
            drift = DetectedDrift(
                drift_type=DriftType.RETRY_REQUIRED,
                severity=DriftSeverity.WARNING,
                description=f"Retry {attempt_number} required due to: {validation_error[:100] if validation_error else 'unknown'}",
                expected="First attempt success",
                actual=f"Retry #{attempt_number}",
                metadata={"validation_error": validation_error[:200] if validation_error else None},
            )
            self.detected_drifts.append(drift)
            return drift

        # Check for max retries
        if attempt_number >= self.plan.max_retries and not success:
            drift = DetectedDrift(
                drift_type=DriftType.MAX_RETRIES,
                severity=DriftSeverity.ALERT,
                description=f"Max retries ({self.plan.max_retries}) exceeded without success",
                expected=f"Success within {self.plan.max_retries} retries",
                actual=f"Failed after {attempt_number + 1} attempts",
            )
            self.detected_drifts.append(drift)
            return drift

        return None

    def record_result(self, result: Any) -> List[DetectedDrift]:
        """
        Record the final result and check for drifts.

        Returns list of detected drifts.
        """
        self.execution.set_result(result)

        drifts = []

        # Check for missing required fields
        if self.plan.required_fields:
            missing = self.plan.required_fields - self.execution.extracted_fields
            for field_name in missing:
                drift = DetectedDrift(
                    drift_type=DriftType.MISSING_FIELD,
                    severity=DriftSeverity.WARNING,
                    description=f"Required field '{field_name}' missing from extraction",
                    expected="Field present",
                    actual="Field missing",
                    field_name=field_name,
                )
                drifts.append(drift)
                self.detected_drifts.append(drift)

        # Check for null values in required fields
        null_required = self.plan.required_fields & self.execution.null_fields
        for field_name in null_required:
            drift = DetectedDrift(
                drift_type=DriftType.NULL_VALUE,
                severity=DriftSeverity.WARNING,
                description=f"Required field '{field_name}' has null value",
                expected="Non-null value",
                actual="null",
                field_name=field_name,
            )
            drifts.append(drift)
            self.detected_drifts.append(drift)

        # Check for empty values
        for field_name in self.execution.empty_fields:
            drift = DetectedDrift(
                drift_type=DriftType.EMPTY_VALUE,
                severity=DriftSeverity.INFO,
                description=f"Field '{field_name}' has empty value",
                field_name=field_name,
            )
            drifts.append(drift)
            self.detected_drifts.append(drift)

        return drifts

    def finalize(
        self,
        total_duration_ms: float,
        total_tokens: int,
        total_cost: float,
    ) -> List[DetectedDrift]:
        """
        Finalize extraction tracking and perform final drift analysis.

        Returns all detected drifts.
        """
        self.execution.total_duration_ms = total_duration_ms
        self.execution.total_tokens = total_tokens
        self.execution.total_cost = total_cost

        return self.detected_drifts

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of expected vs actual extraction."""
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
            return "No drifts detected - extraction matched expectations"

        report = f"Detected {len(self.detected_drifts)} drift(s):\n"
        for i, drift in enumerate(self.detected_drifts, 1):
            report += f"\n{i}. [{drift.severity.value.upper()}] {drift.drift_type.value}"
            if drift.field_name:
                report += f" (field: {drift.field_name})"
            report += f"\n   {drift.description}\n"
            if drift.expected:
                report += f"   Expected: {drift.expected}\n"
            if drift.actual:
                report += f"   Actual: {drift.actual}\n"

        return report
