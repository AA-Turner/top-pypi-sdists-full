"""Planning tool for exploration strategy."""

from typing import Optional

from .base import BaseTool, ToolResult, ToolCategory
from ...utils.logger import log


# Exploration strategies
STRATEGIES = {
    "understand_feature": {
        "description": "Understand how a feature works",
        "steps": [
            {"tool": "semantic_search", "purpose": "Find entry points"},
            {"tool": "expand_node", "purpose": "Understand main components"},
            {"tool": "get_callers", "purpose": "See usage patterns"},
            {"tool": "get_file_dependencies", "purpose": "Map module structure"},
        ],
    },
    "debug_issue": {
        "description": "Debug a bug or issue",
        "steps": [
            {"tool": "grep", "purpose": "Find error messages or symptoms"},
            {"tool": "semantic_search", "purpose": "Find related code"},
            {"tool": "get_callees", "purpose": "Trace execution path"},
            {"tool": "expand_node", "purpose": "Examine suspicious code"},
        ],
    },
    "assess_change_impact": {
        "description": "Assess impact of a proposed change",
        "steps": [
            {"tool": "get_callers", "purpose": "Find all usages"},
            {"tool": "get_impact_analysis", "purpose": "Assess blast radius"},
            {"tool": "get_file_dependencies", "purpose": "Find affected modules"},
            {"tool": "get_class_hierarchy", "purpose": "Check inheritance impact"},
        ],
    },
    "onboard_codebase": {
        "description": "Get oriented in a new codebase",
        "steps": [
            {"tool": "get_communities", "purpose": "Understand major areas"},
            {"tool": "get_top_pagerank", "purpose": "Find key components"},
            {"tool": "get_area_importance", "purpose": "Map directory structure"},
            {"tool": "semantic_search", "purpose": "Explore specific topics"},
        ],
    },
    "find_similar_code": {
        "description": "Find code similar to a reference",
        "steps": [
            {"tool": "expand_node", "purpose": "Understand the reference"},
            {"tool": "semantic_search", "purpose": "Find similar patterns"},
            {"tool": "get_neighbors", "purpose": "Explore related code"},
        ],
    },
}


class PlanExplorationTool(BaseTool):
    """Create an exploration plan for a goal."""

    name = "plan_exploration"
    description = """Create a structured exploration plan for understanding code.

Available strategies:
- understand_feature: Learn how a feature works
- debug_issue: Track down a bug
- assess_change_impact: Evaluate change risk
- onboard_codebase: Get oriented in new code
- find_similar_code: Find similar patterns

Or provide a custom goal and get a tailored plan."""
    category = ToolCategory.PLANNING

    def execute(
        self,
        goal: str,
        strategy: Optional[str] = None,
        context: Optional[str] = None,
        constraints: Optional[list[str]] = None,
        use_case: Optional[str] = None,
    ) -> ToolResult:
        """Create an exploration plan.

        Args:
            goal: What you want to understand or accomplish
            strategy: Optional predefined strategy to use
            context: Additional context about the goal
            constraints: Constraints to consider
            use_case: Optional use case hint (e.g., "spec", "debug", "review")

        Returns:
            ToolResult with exploration plan
        """
        # Map use_case to strategy if strategy not provided
        if use_case and not strategy:
            use_case_mapping = {
                "spec": "understand_feature",
                "debug": "debug_issue",
                "review": "assess_change_impact",
                "onboard": "onboard_codebase",
            }
            strategy = use_case_mapping.get(use_case)
        try:
            # Use predefined strategy if specified
            if strategy and strategy in STRATEGIES:
                strat = STRATEGIES[strategy]
                return ToolResult.success_result(
                    data={
                        "goal": goal,
                        "strategy": strategy,
                        "description": strat["description"],
                        "steps": strat["steps"],
                        "context": context,
                        "constraints": constraints,
                    },
                )

            # Infer strategy from goal
            inferred = self._infer_strategy(goal)

            if inferred and inferred in STRATEGIES:
                strat = STRATEGIES[inferred]
                return ToolResult.success_result(
                    data={
                        "goal": goal,
                        "strategy": inferred,
                        "description": strat["description"],
                        "steps": strat["steps"],
                        "context": context,
                        "constraints": constraints,
                        "inferred": True,
                    },
                )

            # Generic exploration plan
            return ToolResult.success_result(
                data={
                    "goal": goal,
                    "strategy": "custom",
                    "description": "Custom exploration plan",
                    "steps": [
                        {"tool": "semantic_search", "purpose": f"Search for '{goal}'"},
                        {"tool": "expand_node", "purpose": "Examine top results"},
                        {"tool": "get_neighbors", "purpose": "Explore connections"},
                    ],
                    "context": context,
                    "constraints": constraints,
                    "available_strategies": list(STRATEGIES.keys()),
                },
            )

        except Exception as e:
            log.exception("Plan exploration failed")
            return ToolResult.error_result(f"Planning failed: {str(e)}")

    def _infer_strategy(self, goal: str) -> Optional[str]:
        """Infer strategy from goal text."""
        goal_lower = goal.lower()

        if any(word in goal_lower for word in ["bug", "error", "issue", "fix", "debug"]):
            return "debug_issue"

        if any(word in goal_lower for word in ["how", "understand", "learn", "feature"]):
            return "understand_feature"

        if any(word in goal_lower for word in ["change", "modify", "refactor", "impact"]):
            return "assess_change_impact"

        if any(word in goal_lower for word in ["new", "onboard", "overview", "structure"]):
            return "onboard_codebase"

        if any(word in goal_lower for word in ["similar", "like", "pattern", "example"]):
            return "find_similar_code"

        return None

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "goal": {
                    "type": "string",
                    "description": "What you want to understand or accomplish",
                },
                "strategy": {
                    "type": "string",
                    "enum": list(STRATEGIES.keys()),
                    "description": "Optional predefined strategy to use",
                },
                "context": {
                    "type": "string",
                    "description": "Additional context about the goal",
                },
                "constraints": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Constraints to consider",
                },
                "use_case": {
                    "type": "string",
                    "enum": ["spec", "debug", "review", "onboard"],
                    "description": "Use case hint to guide strategy selection",
                },
            },
            required=["goal"],
        )
