"""Agent-designed mini workflows.

A simplified, LLM-authorable scheme (``AgentPlan``) for ad-hoc multi-agent
workflows, plus a deterministic converter (``compile_plan``) that turns a
plan into a bona-fide ``matrx_graph.Definition``. Once converted, the
workflow is identical to any other — the engine doesn't know or care that
an agent designed it.
"""

from matrx_ai.plans.compiler import compile_plan
from matrx_ai.plans.errors import AgentPlanValidationError, PlanIssue
from matrx_ai.plans.types import (
    FOR_EACH_MAX_ITEMS,
    MAX_PLAN_STEPS,
    AgentPlan,
    PlanStep,
    plan_json_schema,
)
from matrx_ai.plans.validate import validate_plan, validate_plan_agents

__all__ = [
    "FOR_EACH_MAX_ITEMS",
    "MAX_PLAN_STEPS",
    "AgentPlan",
    "AgentPlanValidationError",
    "PlanIssue",
    "PlanStep",
    "compile_plan",
    "plan_json_schema",
    "validate_plan",
    "validate_plan_agents",
]
