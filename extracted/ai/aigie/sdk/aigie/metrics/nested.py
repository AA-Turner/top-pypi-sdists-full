"""
Nested Agent Health Metric.

Measures health of nested agent hierarchies.
Production-grade implementation with comprehensive validation.
"""

import json
import logging
from datetime import datetime
from typing import Any

from ..evaluation import EvaluationResult, ScoreType
from .base import BaseMetric

logger = logging.getLogger(__name__)


class NestedAgentHealthMetric(BaseMetric):
    """
    Metric for measuring nested agent hierarchy health.

    Evaluates the health and performance of nested agent systems.
    Designed for production use with comprehensive health checks.

    Usage:
        metric = NestedAgentHealthMetric(threshold=0.7)
        result = await metric.measure(
            input={"agent_type": "parent"},
            output={"nested_agents": [...]},
            context={"nested_depth": 2, "agent_hierarchy": {...}}
        )
    """

    def __init__(
        self, threshold: float = 0.7, name: str | None = None, description: str | None = None
    ):
        """
        Initialize nested agent health metric.

        Args:
            threshold: Minimum score for healthy nested agents (0.0-1.0)
            name: Metric name (defaults to class name)
            description: Metric description
        """
        super().__init__(
            threshold=threshold,
            name=name or "NestedAgentHealth",
            description=description or "Measures nested agent hierarchy health",
        )

    async def measure(
        self, input: Any, output: Any, context: dict[str, Any] | None = None
    ) -> EvaluationResult:
        """
        Measure nested agent health.

        Args:
            input: Agent input or parent agent data
            output: Agent output or nested agent results
            context: Optional context containing:
                - nested_depth: Depth of nesting
                - agent_hierarchy: Agent hierarchy structure
                - nested_agents: List of nested agents
                - parent_agent_id: Parent agent identifier
                - trace_id: Associated trace ID

        Returns:
            EvaluationResult with health score (0.0 = unhealthy, 1.0 = healthy)

        Raises:
            TypeError: If context is not a dict
            ValueError: If required context fields are missing
        """
        # Validate context type
        context = self._validate_context(context)

        try:
            # Extract nested agent data
            nested_depth = context.get("nested_depth", 0)
            agent_hierarchy = context.get("agent_hierarchy", {})
            nested_agents = context.get("nested_agents", [])
            parent_agent_id = context.get("parent_agent_id")

            # Extract from output if not in context
            if not nested_agents and isinstance(output, dict):
                nested_agents = output.get("nested_agents", output.get("children", []))

            if nested_depth == 0 and not nested_agents:
                # Not a nested agent scenario
                return self._create_fallback_result(
                    score=1.0, explanation="No nested agents detected - health check not applicable"
                )

            # Evaluate nested agent health
            return await self._evaluate_nested_health(
                nested_depth, agent_hierarchy, nested_agents, parent_agent_id, context
            )

        except Exception as e:
            logger.error(f"NestedAgentHealthMetric: Error measuring health: {e}", exc_info=True)
            return self._create_fallback_result(
                score=0.5, explanation=f"Error evaluating nested agent health: {e!s}"
            )

    async def _evaluate_nested_health(
        self,
        nested_depth: int,
        agent_hierarchy: dict[str, Any],
        nested_agents: list[dict[str, Any]],
        parent_agent_id: str | None,
        context: dict[str, Any],
    ) -> EvaluationResult:
        """Evaluate nested agent health using multiple criteria."""
        health_scores = {}
        total_score = 0.0
        weight_sum = 0.0

        # 1. Hierarchy structure validity (25% weight)
        structure_score = self._validate_hierarchy_structure(agent_hierarchy, nested_agents)
        health_scores["structure"] = structure_score
        total_score += structure_score * 0.25
        weight_sum += 0.25

        # 2. Nested agent success rate (30% weight)
        success_score = self._calculate_success_rate(nested_agents)
        health_scores["success_rate"] = success_score
        total_score += success_score * 0.30
        weight_sum += 0.30

        # 3. Depth management (20% weight)
        depth_score = self._evaluate_depth_management(nested_depth)
        health_scores["depth_management"] = depth_score
        total_score += depth_score * 0.20
        weight_sum += 0.20

        # 4. Communication efficiency (25% weight)
        communication_score = self._evaluate_communication(nested_agents, context)
        health_scores["communication"] = communication_score
        total_score += communication_score * 0.25
        weight_sum += 0.25

        # Normalize score
        final_score = total_score / weight_sum if weight_sum > 0 else 0.0

        # Determine health status
        if final_score >= 0.8:
            health_status = "healthy"
        elif final_score >= 0.6:
            health_status = "mostly_healthy"
        elif final_score >= 0.4:
            health_status = "degraded"
        else:
            health_status = "unhealthy"

        return EvaluationResult(
            score=final_score,
            score_type=ScoreType.CUSTOM,
            explanation=(
                f"Nested agent health: {health_status}. "
                f"Structure: {structure_score:.2f}, "
                f"Success: {success_score:.2f}, "
                f"Depth: {depth_score:.2f}, "
                f"Communication: {communication_score:.2f}"
            ),
            metadata={
                "health_status": health_status,
                "nested_depth": nested_depth,
                "nested_agent_count": len(nested_agents),
                "parent_agent_id": parent_agent_id,
                "health_scores": health_scores,
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

    def _validate_hierarchy_structure(
        self, agent_hierarchy: dict[str, Any], nested_agents: list[dict[str, Any]]
    ) -> float:
        """Validate hierarchy structure is well-formed."""
        if not agent_hierarchy and not nested_agents:
            return 0.5  # No hierarchy data

        # Check for circular references (simplified)
        try:
            json.dumps(agent_hierarchy, default=str)
            structure_valid = 1.0
        except (TypeError, ValueError):
            structure_valid = 0.5

        # Check nested agents have required fields
        if nested_agents:
            valid_agents = sum(
                1
                for agent in nested_agents
                if isinstance(agent, dict) and ("id" in agent or "agent_id" in agent)
            )
            agent_validity = valid_agents / len(nested_agents) if nested_agents else 0.0
        else:
            agent_validity = 0.5

        return structure_valid * 0.6 + agent_validity * 0.4

    def _calculate_success_rate(self, nested_agents: list[dict[str, Any]]) -> float:
        """Calculate success rate of nested agents."""
        if not nested_agents:
            return 0.5  # No agents to evaluate

        successful = 0
        total = 0

        for agent in nested_agents:
            if isinstance(agent, dict):
                status = agent.get("status", agent.get("state", "unknown"))
                if status in ["success", "completed", "successful"]:
                    successful += 1
                elif status in ["failure", "failed", "error"]:
                    pass  # Count as failed
                total += 1

        if total == 0:
            return 0.5

        return successful / total

    def _evaluate_depth_management(self, nested_depth: int) -> float:
        """Evaluate if nesting depth is manageable."""
        # Optimal depth: 2-4 levels
        if nested_depth == 0:
            return 1.0  # No nesting
        if 1 <= nested_depth <= 3:
            return 1.0  # Optimal
        if nested_depth == 4:
            return 0.8  # Acceptable
        if nested_depth == 5:
            return 0.6  # Getting deep
        if nested_depth <= 7:
            return 0.4  # Too deep
        return 0.2  # Excessive depth

    def _evaluate_communication(
        self, nested_agents: list[dict[str, Any]], context: dict[str, Any]
    ) -> float:
        """Evaluate communication efficiency between nested agents."""
        if not nested_agents:
            return 0.5

        # Check for communication metadata
        has_communication = sum(
            1
            for agent in nested_agents
            if isinstance(agent, dict)
            and ("communication" in agent or "handoff" in agent or "parent_communication" in agent)
        )

        communication_score = has_communication / len(nested_agents) if nested_agents else 0.0

        # Check for handoff efficiency
        handoffs = context.get("agent_handoffs", [])
        if handoffs:
            # More handoffs might indicate inefficiency
            handoff_efficiency = max(0.0, 1.0 - (len(handoffs) / 10.0))
            communication_score = communication_score * 0.7 + handoff_efficiency * 0.3

        return communication_score

    def _create_fallback_result(self, score: float, explanation: str) -> EvaluationResult:
        """Create fallback result on error."""
        return EvaluationResult(
            score=score,
            score_type=ScoreType.CUSTOM,
            explanation=explanation,
            metadata={"error": True, "timestamp": datetime.utcnow().isoformat()},
        )
