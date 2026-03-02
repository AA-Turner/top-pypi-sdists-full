"""Tool macros for reproducible research workflows.

This module provides predefined tool sequences (macros) that can be
executed to gather specific types of evidence.
"""

from dataclasses import dataclass, field
from typing import Any, Optional

from .state import EvidenceItem
from ...utils.logger import log


@dataclass
class MacroStep:
    """A single step in a tool macro.

    Attributes:
        tool: Tool name to execute
        params: Parameters for the tool
        depends_on: Previous step whose output is needed
        param_mappings: Map output fields to this step's params
    """
    tool: str
    params: dict = field(default_factory=dict)
    depends_on: Optional[str] = None
    param_mappings: dict = field(default_factory=dict)


@dataclass
class ToolMacro:
    """A sequence of tool calls for gathering evidence.

    Attributes:
        name: Macro identifier
        description: What this macro investigates
        steps: Ordered list of steps
        output_schema: Expected output fields
    """
    name: str
    description: str
    steps: list[MacroStep]
    output_schema: dict = field(default_factory=dict)


# Predefined macros for common research patterns
TOOL_MACROS = {
    "deep_feature_analysis": ToolMacro(
        name="deep_feature_analysis",
        description="Understand feature behavior and impact",
        steps=[
            MacroStep(
                tool="semantic_search",
                params={"query": "{topic}", "limit": 10},
            ),
            MacroStep(
                tool="expand_node",
                params={"node_type": "Function", "identifier": "{identifier}"},
                depends_on="semantic_search",
                param_mappings={"identifier": "results[0].qualified_name"},
            ),
            MacroStep(
                tool="get_callers",
                params={"qualified_name": "{identifier}"},
                depends_on="expand_node",
            ),
            MacroStep(
                tool="get_callees",
                params={"qualified_name": "{identifier}"},
                depends_on="expand_node",
            ),
        ],
    ),

    "team_activity_analysis": ToolMacro(
        name="team_activity_analysis",
        description="Find owners, expertise, and velocity risks",
        steps=[
            MacroStep(
                tool="semantic_search",
                params={"query": "{topic}", "limit": 5},
            ),
            MacroStep(
                tool="get_file_dependencies",
                params={"file_path": "{file_path}"},
                depends_on="semantic_search",
                param_mappings={"file_path": "results[0].file_path"},
            ),
        ],
    ),

    "architectural_deep_dive": ToolMacro(
        name="architectural_deep_dive",
        description="Map architecture and key modules",
        steps=[
            MacroStep(
                tool="get_communities",
                params={"limit": 10, "include_members": True},
            ),
            MacroStep(
                tool="get_top_pagerank",
                params={"limit": 15},
            ),
            MacroStep(
                tool="get_area_importance",
                params={"area_type": "directory", "limit": 10},
            ),
        ],
    ),

    "implementation_trace": ToolMacro(
        name="implementation_trace",
        description="Trace specific implementation paths",
        steps=[
            MacroStep(
                tool="semantic_search",
                params={"query": "{topic}", "limit": 10},
            ),
            MacroStep(
                tool="expand_node",
                params={"node_type": "Function", "identifier": "{identifier}"},
                depends_on="semantic_search",
                param_mappings={"identifier": "results[0].qualified_name"},
            ),
            MacroStep(
                tool="get_callees",
                params={"qualified_name": "{identifier}", "limit": 20},
                depends_on="expand_node",
            ),
        ],
    ),

    "risk_assessment": ToolMacro(
        name="risk_assessment",
        description="Assess risks of modifications",
        steps=[
            MacroStep(
                tool="semantic_search",
                params={"query": "{topic}", "limit": 5},
            ),
            MacroStep(
                tool="get_impact_analysis",
                params={
                    "entity_type": "Function",
                    "identifier": "{identifier}",
                    "depth": 2,
                },
                depends_on="semantic_search",
                param_mappings={"identifier": "results[0].qualified_name"},
            ),
            MacroStep(
                tool="get_callers",
                params={"qualified_name": "{identifier}", "limit": 30},
                depends_on="semantic_search",
                param_mappings={"qualified_name": "results[0].qualified_name"},
            ),
        ],
    ),

    "pr_context": ToolMacro(
        name="pr_context",
        description="Understand PR and change context",
        steps=[
            MacroStep(
                tool="github_list_prs",
                params={"owner": "{owner}", "repo": "{repo}", "state": "all", "per_page": 10},
            ),
        ],
    ),
}


class MacroExecutor:
    """Executes tool macros and collects evidence.

    The executor handles:
    - Step sequencing and dependencies
    - Parameter resolution from prior outputs
    - Evidence collection with unique IDs
    - Budget tracking
    """

    def __init__(self, toolkit: Any):
        """Initialize the executor.

        Args:
            toolkit: AgentToolkit instance for executing tools
        """
        self.toolkit = toolkit
        self.evidence_counter = 0

    def execute_macro(
        self,
        macro_name: str,
        params: dict,
        budget_remaining: int = 50,
        prior_context: Optional[dict] = None,
    ) -> tuple[list[EvidenceItem], dict]:
        """Execute a macro and return evidence.

        Args:
            macro_name: Name of the macro to execute
            params: Initial parameters
            budget_remaining: Maximum tool calls allowed
            prior_context: Context from previous iterations

        Returns:
            Tuple of (evidence_items, updated_context)
        """
        if macro_name not in TOOL_MACROS:
            log.warning(f"Unknown macro: {macro_name}")
            return [], {}

        macro = TOOL_MACROS[macro_name]
        evidence: list[EvidenceItem] = []
        context = dict(prior_context or {})
        step_outputs: dict[str, Any] = {}

        for step in macro.steps:
            if len(evidence) >= budget_remaining:
                break

            # Resolve parameters
            resolved_params = self._resolve_params(
                step.params,
                params,
                step_outputs,
                step.param_mappings,
                context,
            )

            # Skip if required params are missing
            if None in resolved_params.values():
                log.debug(f"Skipping step {step.tool}: missing params")
                continue

            try:
                result = self.toolkit.execute(step.tool, **resolved_params)

                if result.success:
                    # Store output for dependent steps
                    step_outputs[step.tool] = result.data

                    # Create evidence
                    self.evidence_counter += 1
                    # Only extract summary/entities if data is a dict
                    data = result.data if isinstance(result.data, dict) else {}
                    ev = EvidenceItem(
                        id=f"E{self.evidence_counter}",
                        tool=step.tool,
                        input=resolved_params,
                        output_ref=f"result_{self.evidence_counter}",
                        summary=self._summarize_result(step.tool, data),
                        entities=self._extract_entities(data),
                    )
                    evidence.append(ev)

                    # Update context
                    if isinstance(result.data, dict) and "results" in result.data and result.data["results"]:
                        context["last_search_results"] = result.data["results"]
                        context["last_search_top"] = result.data["results"][0]

            except Exception as e:
                log.warning(f"Macro step {step.tool} failed: {e}")

        return evidence, context

    def _resolve_params(
        self,
        step_params: dict,
        initial_params: dict,
        step_outputs: dict,
        mappings: dict,
        context: dict,
    ) -> dict:
        """Resolve parameter placeholders.

        Args:
            step_params: Parameters with {placeholders}
            initial_params: Initial params from caller
            step_outputs: Outputs from previous steps
            mappings: Output field to param mappings
            context: Prior context

        Returns:
            Resolved parameters
        """
        resolved = {}

        for key, value in step_params.items():
            if isinstance(value, str) and value.startswith("{") and value.endswith("}"):
                placeholder = value[1:-1]

                # Check mappings first
                if key in mappings:
                    resolved[key] = self._resolve_mapping(mappings[key], step_outputs, context)
                # Then initial params
                elif placeholder in initial_params:
                    resolved[key] = initial_params[placeholder]
                # Then context
                elif placeholder in context:
                    resolved[key] = context[placeholder]
                # Try to get from last search results
                elif placeholder == "identifier" and "last_search_top" in context:
                    top = context["last_search_top"]
                    resolved[key] = top.get("qualified_name") or top.get("file_path")
                else:
                    resolved[key] = None
            else:
                resolved[key] = value

        return resolved

    def _resolve_mapping(
        self,
        mapping: str,
        step_outputs: dict,
        context: dict,
    ) -> Optional[str]:
        """Resolve an output mapping like 'results[0].qualified_name'.

        Args:
            mapping: Mapping string
            step_outputs: Previous step outputs
            context: Prior context

        Returns:
            Resolved value or None
        """
        try:
            parts = mapping.split(".")

            # Get base value
            base = parts[0]
            if "[" in base:
                # Array access: results[0]
                array_name = base[:base.index("[")]
                index = int(base[base.index("[") + 1:base.index("]")])

                # Look in step outputs first, then context
                if array_name in step_outputs:
                    value = step_outputs[array_name][index]
                elif array_name in context:
                    value = context[array_name][index]
                else:
                    return None
            else:
                value = step_outputs.get(base) or context.get(base)

            # Navigate to nested value
            for part in parts[1:]:
                if isinstance(value, dict):
                    value = value.get(part)
                else:
                    return None

            return value

        except (IndexError, KeyError, TypeError):
            return None

    def _summarize_result(self, tool: str, data: dict) -> str:
        """Create a brief summary of a tool result."""
        if "results" in data:
            return f"Found {len(data['results'])} results"
        elif "root_node" in data:
            node = data["root_node"]
            return f"Expanded {node.get('qualified_name', 'node')}"
        elif "callers" in data:
            return f"Found {len(data['callers'])} callers"
        elif "callees" in data:
            return f"Found {len(data['callees'])} callees"
        elif "communities" in data:
            return f"Found {len(data['communities'])} communities"
        else:
            return f"{tool} completed"

    def _extract_entities(self, data: dict) -> list[str]:
        """Extract entity identifiers from result data."""
        entities = []

        if "results" in data:
            for item in data["results"][:10]:
                if isinstance(item, dict):
                    for key in ["qualified_name", "file_path", "identifier"]:
                        if key in item and item[key]:
                            entities.append(str(item[key]))
                            break

        if "root_node" in data:
            root = data["root_node"]
            for key in ["qualified_name", "file_path"]:
                if key in root and root[key]:
                    entities.append(str(root[key]))

        if "callers" in data:
            for caller in data["callers"][:5]:
                if isinstance(caller, dict) and "qualified_name" in caller:
                    entities.append(caller["qualified_name"])

        if "callees" in data:
            for callee in data["callees"][:5]:
                if isinstance(callee, dict) and "qualified_name" in callee:
                    entities.append(callee["qualified_name"])

        return list(set(entities))[:20]


def get_macro(name: str) -> Optional[ToolMacro]:
    """Get a macro by name.

    Args:
        name: Macro name

    Returns:
        ToolMacro or None
    """
    return TOOL_MACROS.get(name)


def list_macros() -> list[str]:
    """List all available macro names.

    Returns:
        List of macro names
    """
    return list(TOOL_MACROS.keys())


def suggest_macros(
    goal: str,
    include_github: bool = False,
) -> list[str]:
    """Suggest macros based on a goal.

    Args:
        goal: Research goal
        include_github: Whether to include GitHub macros

    Returns:
        List of suggested macro names
    """
    goal_lower = goal.lower()
    suggestions = []

    # Feature/implementation questions
    if any(word in goal_lower for word in ["how", "what", "feature", "work", "implement"]):
        suggestions.append("deep_feature_analysis")
        suggestions.append("implementation_trace")

    # Architecture questions
    if any(word in goal_lower for word in ["architecture", "structure", "module", "component"]):
        suggestions.append("architectural_deep_dive")

    # Risk/impact questions
    if any(word in goal_lower for word in ["risk", "impact", "change", "modify", "refactor"]):
        suggestions.append("risk_assessment")

    # Team/ownership questions
    if any(word in goal_lower for word in ["who", "owner", "team", "expertise"]):
        suggestions.append("team_activity_analysis")

    # PR/history questions
    if include_github and any(word in goal_lower for word in ["pr", "pull", "change", "history"]):
        suggestions.append("pr_context")

    # Default if nothing matched
    if not suggestions:
        suggestions = ["deep_feature_analysis", "architectural_deep_dive"]

    return suggestions[:3]  # Return top 3
