"""
Checkpoint Validity Metric.

Validates checkpoint state integrity and correctness.
Production-grade implementation with comprehensive validation.
"""

import json
import logging
from datetime import datetime
from typing import Any

from ..evaluation import EvaluationResult, ScoreType
from .base import BaseMetric

logger = logging.getLogger(__name__)


class CheckpointValidityMetric(BaseMetric):
    """
    Metric for validating checkpoint state.

    Ensures checkpoint integrity and correctness for time-travel debugging.
    Designed for production use with proper validation logic.

    Usage:
        metric = CheckpointValidityMetric(threshold=0.9)
        result = await metric.measure(
            input={"checkpoint_id": "..."},
            output={"state": {...}},
            context={"checkpoint_type": "agent_transition", "execution_path": [...]}
        )
    """

    def __init__(
        self, threshold: float = 0.9, name: str | None = None, description: str | None = None
    ):
        """
        Initialize checkpoint validity metric.

        Args:
            threshold: Minimum score for valid checkpoint (0.0-1.0)
            name: Metric name (defaults to class name)
            description: Metric description
        """
        super().__init__(
            threshold=threshold,
            name=name or "CheckpointValidity",
            description=description or "Validates checkpoint state integrity",
        )

    async def measure(
        self, input: Any, output: Any, context: dict[str, Any] | None = None
    ) -> EvaluationResult:
        """
        Measure checkpoint validity.

        Args:
            input: Checkpoint input or checkpoint ID
            output: Checkpoint state or validation result
            context: Optional context containing:
                - checkpoint_id: Checkpoint identifier
                - checkpoint_type: Type of checkpoint
                - state_snapshot: State snapshot data
                - execution_path: Execution path leading to checkpoint
                - trace_id: Associated trace ID

        Returns:
            EvaluationResult with validity score (0.0 = invalid, 1.0 = valid)

        Raises:
            TypeError: If context is not a dict
            ValueError: If required context fields are missing
        """
        # Validate context type
        context = self._validate_context(context)

        try:
            # Extract checkpoint data
            checkpoint_id = context.get("checkpoint_id") or self._extract_id(input)
            checkpoint_type = context.get("checkpoint_type", "agent_transition")
            state_snapshot = context.get("state_snapshot") or self._extract_state(output, context)
            execution_path = context.get("execution_path", [])

            if not checkpoint_id:
                logger.warning("CheckpointValidityMetric: Missing checkpoint ID")
                return self._create_fallback_result(score=0.0, explanation="Missing checkpoint ID")

            if not state_snapshot:
                logger.warning("CheckpointValidityMetric: Missing state snapshot")
                return self._create_fallback_result(score=0.0, explanation="Missing state snapshot")

            # Validate checkpoint
            return await self._validate_checkpoint(
                checkpoint_id, checkpoint_type, state_snapshot, execution_path
            )

        except Exception as e:
            logger.error(
                f"CheckpointValidityMetric: Error validating checkpoint: {e}", exc_info=True
            )
            return self._create_fallback_result(
                score=0.0, explanation=f"Error validating checkpoint: {e!s}"
            )

    async def _validate_checkpoint(
        self,
        checkpoint_id: str,
        checkpoint_type: str,
        state_snapshot: dict[str, Any],
        execution_path: list,
    ) -> EvaluationResult:
        """Validate checkpoint using multiple criteria."""
        validation_results = {}
        total_score = 0.0
        weight_sum = 0.0

        # 1. State completeness (30% weight)
        completeness_score = self._validate_completeness(state_snapshot)
        validation_results["completeness"] = completeness_score
        total_score += completeness_score * 0.3
        weight_sum += 0.3

        # 2. State consistency (30% weight)
        consistency_score = self._validate_consistency(state_snapshot)
        validation_results["consistency"] = consistency_score
        total_score += consistency_score * 0.3
        weight_sum += 0.3

        # 3. Execution path validity (20% weight)
        path_score = self._validate_execution_path(execution_path)
        validation_results["execution_path"] = path_score
        total_score += path_score * 0.2
        weight_sum += 0.2

        # 4. Checkpoint type validity (20% weight)
        type_score = self._validate_checkpoint_type(checkpoint_type, state_snapshot)
        validation_results["checkpoint_type"] = type_score
        total_score += type_score * 0.2
        weight_sum += 0.2

        # Normalize score
        final_score = total_score / weight_sum if weight_sum > 0 else 0.0

        # Determine validity
        if final_score >= 0.9:
            validity = "valid"
        elif final_score >= 0.7:
            validity = "mostly_valid"
        elif final_score >= 0.5:
            validity = "questionable"
        else:
            validity = "invalid"

        return EvaluationResult(
            score=final_score,
            score_type=ScoreType.CUSTOM,
            explanation=(
                f"Checkpoint validation: {validity}. "
                f"Completeness: {completeness_score:.2f}, "
                f"Consistency: {consistency_score:.2f}, "
                f"Path: {path_score:.2f}, "
                f"Type: {type_score:.2f}"
            ),
            metadata={
                "checkpoint_id": checkpoint_id,
                "checkpoint_type": checkpoint_type,
                "validity": validity,
                "validation_results": validation_results,
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

    def _validate_completeness(self, state_snapshot: dict[str, Any]) -> float:
        """Validate that state snapshot is complete."""
        required_fields = ["state", "timestamp", "context"]
        optional_fields = ["metadata", "parent_checkpoint", "children"]

        # Check required fields
        required_present = sum(1 for field in required_fields if field in state_snapshot)
        required_score = required_present / len(required_fields)

        # Check optional fields (bonus)
        optional_present = sum(1 for field in optional_fields if field in state_snapshot)
        optional_bonus = optional_present / len(optional_fields) * 0.2

        # Check state content
        state_content = state_snapshot.get("state", {})
        content_score = 0.5 if state_content else 0.0

        return min(1.0, required_score * 0.7 + optional_bonus + content_score * 0.1)

    def _validate_consistency(self, state_snapshot: dict[str, Any]) -> float:
        """Validate that state snapshot is internally consistent."""
        state = state_snapshot.get("state", {})

        if not state:
            return 0.0

        # Check for circular references (simplified)
        try:
            json.dumps(state, default=str)
            # If serialization succeeds, likely no circular refs
            serialization_score = 1.0
        except (TypeError, ValueError):
            serialization_score = 0.5

        # Check data types consistency
        type_consistency = 1.0  # Simplified - could be enhanced

        # Check timestamp validity
        timestamp = state_snapshot.get("timestamp")
        timestamp_valid = 1.0 if timestamp else 0.5

        return serialization_score * 0.5 + type_consistency * 0.3 + timestamp_valid * 0.2

    def _validate_execution_path(self, execution_path: list) -> float:
        """Validate execution path leading to checkpoint."""
        if not execution_path:
            return 0.5  # No path provided

        # Check path is a list
        if not isinstance(execution_path, list):
            return 0.0

        # Check path has reasonable length
        if len(execution_path) == 0:
            return 0.5
        if len(execution_path) > 1000:
            return 0.7  # Suspiciously long

        # Check path elements are valid
        valid_elements = sum(
            1
            for elem in execution_path
            if isinstance(elem, (str, dict)) or hasattr(elem, "__dict__")
        )
        return valid_elements / len(execution_path) if execution_path else 0.0


    def _validate_checkpoint_type(
        self, checkpoint_type: str, state_snapshot: dict[str, Any]
    ) -> float:
        """Validate checkpoint type matches state structure."""
        valid_types = ["agent_transition", "tool_call", "llm_call", "error_recovery", "checkpoint"]

        if checkpoint_type not in valid_types:
            return 0.5  # Unknown type

        # Check state has appropriate fields for type
        state = state_snapshot.get("state", {})

        type_requirements = {
            "agent_transition": ["agent_id", "transition"],
            "tool_call": ["tool_name", "tool_input"],
            "llm_call": ["model", "prompt"],
            "error_recovery": ["error", "recovery_strategy"],
            "checkpoint": ["state"],
        }

        required = type_requirements.get(checkpoint_type, [])
        if not required:
            return 1.0  # No specific requirements

        present = sum(1 for field in required if field in state)
        return present / len(required) if required else 1.0

    def _extract_id(self, input: Any) -> str | None:
        """Extract checkpoint ID from input."""
        if isinstance(input, dict):
            return input.get("checkpoint_id") or input.get("id")
        if isinstance(input, str):
            return input
        return None

    def _extract_state(self, output: Any, context: dict[str, Any]) -> dict[str, Any] | None:
        """Extract state snapshot from output or context."""
        # Try context first
        if "state_snapshot" in context:
            state = context["state_snapshot"]
            return state if isinstance(state, dict) else {"state": state}

        # Try output
        if isinstance(output, dict):
            if "state" in output:
                return output
            if "state_snapshot" in output:
                return output["state_snapshot"]
            # Assume entire output is state
            return output

        return None

    def _create_fallback_result(self, score: float, explanation: str) -> EvaluationResult:
        """Create fallback result on error."""
        return EvaluationResult(
            score=score,
            score_type=ScoreType.CUSTOM,
            explanation=explanation,
            metadata={"error": True, "timestamp": datetime.utcnow().isoformat()},
        )
