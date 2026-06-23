"""
Aigie Agent Observability Module.

This module provides production-grade observability features for AI agents,
addressing the key challenges that prevent 95% of agents from reaching production:

1. Loop Detection - Detect and prevent infinite loops (from AutoGPT patterns)
2. Goal Tracking - Track plan adherence and reliability (from SuperAGI patterns)
3. Execution Cycles - Think-Act-Observe pattern for structured execution

These features support Aigie's core mission:
- Context drift detection
- Auto-error correction
- Production guardrails
- Self-healing workflows
- Reliability scoring
- Predictive prevention

Usage:
    from aigie.agents import LoopDetector, GoalTracker, ExecutionCycle

    # Loop detection
    detector = LoopDetector(
        max_similar_states=3,
        similarity_threshold=0.85,
        action="warn"
    )

    # Goal tracking
    tracker = GoalTracker(
        goal="Complete user task",
        expected_steps=["step1", "step2", "step3"]
    )

    # Execution cycle
    async with aigie.trace("agent_run") as trace:
        cycle = ExecutionCycle(trace)

        async with cycle.think() as thought:
            thought.set_output(plan)

        async with cycle.act() as action:
            action.set_output(result)

        async with cycle.observe() as observation:
            observation.set_output(evaluation)
"""

from aigie.agents.execution_cycle import (
    CycleMetrics,
    CyclePhase,
    ExecutionCycle,
    MultiCycleExecutor,
    PhaseContext,
    PhaseResult,
)
from aigie.agents.goal_tracking import (
    Deviation,
    DeviationType,
    Goal,
    GoalTracker,
    PlanMetrics,
    Step,
    StepStatus,
    TracingGoalTracker,
)
from aigie.agents.loop_detection import (
    LoopAction,
    LoopDetectionResult,
    LoopDetector,
    LoopState,
    TracingLoopDetector,
)

__all__ = [
    # Loop Detection
    "LoopDetector",
    "TracingLoopDetector",
    "LoopAction",
    "LoopState",
    "LoopDetectionResult",
    # Goal Tracking
    "GoalTracker",
    "TracingGoalTracker",
    "Goal",
    "Step",
    "StepStatus",
    "Deviation",
    "DeviationType",
    "PlanMetrics",
    # Execution Cycle
    "ExecutionCycle",
    "CyclePhase",
    "PhaseContext",
    "PhaseResult",
    "CycleMetrics",
    "MultiCycleExecutor",
]
