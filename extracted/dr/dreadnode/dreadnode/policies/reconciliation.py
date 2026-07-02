"""Reconcile a session policy against an engine's enforcement surface.

Offloading the agent loop to a foreign engine must not silently defeat policy.
Each policy declares its ``required_facets``; each engine declares an
``EnforcementSurface``. The runtime diffs them (CAP-EGOV-*) and either accepts,
warns (degraded-but-bounded), or refuses (would silently lose enforcement).

Refusal raises :class:`PolicyEngineMismatch` on the programmatic path; CLI call
sites render the same diff and hard-fail.
"""

import typing as t
from dataclasses import dataclass, field

from dreadnode.agents.engines.base import AgentEngine, CapabilityComponent, PolicyFacet

if t.TYPE_CHECKING:
    from dreadnode.agents.agent import Agent
    from dreadnode.policies import SessionPolicy

# Facets with no native harness mechanism but a degraded-but-bounded fallback
# (kill the run via the inference gateway). Required → warning, not refusal.
_DEGRADED_BOUNDED: frozenset[PolicyFacet] = frozenset(
    {PolicyFacet.TOKEN_BUDGET, PolicyFacet.COST_BUDGET, PolicyFacet.TIME_BUDGET}
)


class PolicyEngineMismatch(Exception):  # noqa: N818  (named for the diagnostic, not "Error")
    """Raised when an engine cannot enforce a facet the session policy requires."""

    def __init__(self, engine_name: str, refusals: list[str]) -> None:
        self.engine_name = engine_name
        self.refusals = refusals
        detail = "; ".join(refusals)
        super().__init__(f"Engine '{engine_name}' cannot enforce the session policy: {detail}")


@dataclass
class ReconciliationResult:
    """Outcome of reconciling a policy against an engine surface."""

    engine_name: str
    ok: bool
    refusals: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def raise_if_refused(self) -> None:
        if not self.ok:
            raise PolicyEngineMismatch(self.engine_name, self.refusals)


def reconcile(policy: "SessionPolicy", engine: AgentEngine) -> ReconciliationResult:
    """Diff a policy's required facets against an engine's enforcement surface."""
    surface = engine.describe_enforcement(policy)
    required = policy.required_facets()

    refusals: list[str] = []
    warnings: list[str] = []
    for facet in sorted(required, key=lambda f: f.value):
        if facet in surface.enforces or facet in surface.bridges:
            continue
        if facet in surface.no_equivalent and facet in _DEGRADED_BOUNDED:
            warnings.append(
                f"facet '{facet.value}': no native enforcement in engine "
                f"'{engine.name}'; bounded only by killing the run via the gateway"
            )
            continue
        # observes_only, absent (treated observe-only), or no_equivalent with no
        # bounded fallback — enforcement would be silently lost.
        refusals.append(
            f"facet '{facet.value}': engine '{engine.name}' can only observe it, not enforce it"
        )

    return ReconciliationResult(
        engine_name=engine.name,
        ok=not refusals,
        refusals=refusals,
        warnings=warnings,
    )


# Loop-shaping Agent fields a foreign engine may ignore. We only warn when the
# user *explicitly set* one (tracked via Pydantic's ``model_fields_set``), so
# defaults never produce noise. ``hooks`` is deliberately excluded — observational
# hooks still fire via ``ctx.dispatch`` regardless of engine.
_LOOP_SHAPING_FIELDS: frozenset[str] = frozenset(
    {
        "cache",
        "stop_conditions",
        "judge",
        "generation_timeout",
        "tool_mode",
        "generate_params_extra",
        "backoff_max_tries",
        "backoff_max_time",
    }
)


def describe_config_gaps(agent: "Agent", engine: AgentEngine) -> list[str]:
    """Return warnings for explicitly-set ``Agent`` fields the engine ignores (CAP-EGOV-006)."""
    honored = engine.honored_config()
    if honored is None:  # native — honors everything
        return []

    set_fields = getattr(agent, "model_fields_set", set())
    gaps: list[str] = []
    for field_name in sorted(_LOOP_SHAPING_FIELDS - honored):
        if field_name in set_fields:
            gaps.append(
                f"engine '{engine.name}' does not honor Agent.{field_name}; it will be ignored"
            )
    return gaps


def describe_component_gaps(
    engine: AgentEngine, *, tool_count: int = 0, skill_count: int = 0
) -> list[str]:
    """Warn when a capability declares components a foreign engine won't use (CAP-ENG-022).

    Only fires for components that are actually present, so capabilities without
    tools/skills produce no noise. Tool *approval* still applies to every tool the
    engine runs via the permission bridge (CAP-ENG-024) — this is about which
    capability-defined tools/skills are *injected*, not about governance.
    """
    consumed = engine.consumed_components()
    gaps: list[str] = []
    if tool_count and CapabilityComponent.PYTHON_TOOLS not in consumed:
        gaps.append(
            f"engine '{engine.name}' uses its own tools; {tool_count} capability "
            f"tool(s) are not available to it"
        )
    if skill_count and CapabilityComponent.SKILLS not in consumed:
        gaps.append(
            f"engine '{engine.name}' does not surface capability skills; "
            f"{skill_count} skill(s) are not provided to it"
        )
    return gaps
