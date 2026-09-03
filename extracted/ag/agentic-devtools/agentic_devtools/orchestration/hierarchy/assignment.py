"""Hierarchy assignment and team composition (FR-001–FR-004, FR-014, FR-015).

Combines the resolved ``HierarchyChain`` (see ``runtime_inputs.py``) with
file-classification results (see ``file_classification.py``) to compose the
smallest valid team of ``ScopeAgent`` declarations for one orchestration
run:

- Epic + Feature + Subtask agents for a complete hierarchy (FR-002).
- Feature + Subtask agents when no epic exists (FR-003).
- Epic + Subtask agents for a leaf task directly beneath an epic with no
  intermediate feature issue (FR-003, SC-008).
- The existing single-agent path for standalone issues (FR-004).
- A reduced or no-edit workflow when scope cannot be safely established
  (FR-014, FR-015).
"""

from __future__ import annotations

from dataclasses import dataclass

from .runtime_inputs import HierarchyChain
from .scopes import (
    AgentScopeLevel,
    ArtifactReference,
    ScopeAgent,
    make_review_only_scope,
)


class AssignmentOutcome:
    """The composed-team outcome classification for one hierarchy assignment."""

    COMPLETE = "complete"  # Epic + Feature + Subtask
    FEATURE_ONLY = "feature_only"  # Feature + Subtask, no Epic
    EPIC_SUBTASK = "epic_subtask"  # Epic + Subtask, no intermediate Feature
    STANDALONE = "standalone"  # existing single-agent behavior
    SAFE_STOPPED = "safe_stopped"  # invalid/ambiguous hierarchy; no agents spawned


@dataclass(frozen=True)
class DegradationRecord:
    """Describes a graceful-degradation decision (FR-015) for the trace."""

    reason: str
    missing_level: str | None
    resulting_topology: tuple[str, ...]


@dataclass(frozen=True)
class HierarchyAssignment:
    """The composed team and degradation status for one orchestration run.

    Attributes:
        outcome: One of ``AssignmentOutcome``.
        chain: The underlying hierarchy chain (``None`` only for
            ``SAFE_STOPPED`` when discovery itself failed upstream).
        epic_agent: The Epic scope agent, if any.
        feature_agent: The Feature scope agent, if any.
        subtask_agents: The classified Subtask scope agents, if any.
        degradation: A degradation record when the topology is reduced,
            else ``None``.
    """

    outcome: str
    chain: HierarchyChain | None
    epic_agent: ScopeAgent | None = None
    feature_agent: ScopeAgent | None = None
    subtask_agents: tuple[ScopeAgent, ...] = ()
    degradation: DegradationRecord | None = None

    @property
    def requires_epic(self) -> bool:
        return self.epic_agent is not None

    @property
    def requires_feature(self) -> bool:
        return self.feature_agent is not None

    @property
    def all_agents(self) -> tuple[ScopeAgent, ...]:
        """Return all spawned agents in creation order, higher scopes first."""
        return (
            tuple(agent for agent in (self.epic_agent, self.feature_agent) if agent is not None) + self.subtask_agents
        )

    @property
    def review_order(self) -> tuple[ScopeAgent, ...]:
        """Return the higher-level review order: Feature before Epic (FR-009)."""
        order: list[ScopeAgent] = []
        if self.feature_agent is not None:
            order.append(self.feature_agent)
        if self.epic_agent is not None:
            order.append(self.epic_agent)
        return tuple(order)


def _epic_scope(epic_key: str, artifacts: tuple[ArtifactReference, ...]) -> ScopeAgent:
    return make_review_only_scope(
        agent_id=f"epic-{epic_key}",
        scope_level=AgentScopeLevel.EPIC,
        issue_key=epic_key,
        artifacts=artifacts,
        can_resolve_conflicts=True,
    )


def _feature_scope(feature_key: str, artifacts: tuple[ArtifactReference, ...]) -> ScopeAgent:
    return make_review_only_scope(
        agent_id=f"feature-{feature_key}",
        scope_level=AgentScopeLevel.FEATURE,
        issue_key=feature_key,
        artifacts=artifacts,
        can_resolve_conflicts=True,
    )


def compose_assignment(
    chain: HierarchyChain,
    *,
    epic_artifacts: tuple[ArtifactReference, ...] = (),
    feature_artifacts: tuple[ArtifactReference, ...] = (),
    subtask_agents: tuple[ScopeAgent, ...] = (),
) -> HierarchyAssignment:
    """Compose the smallest valid team for an already-discovered hierarchy chain.

    This function performs *composition only*; it does not perform hierarchy
    discovery (see ``runtime_inputs.discover_hierarchy_chain``) and does not
    build the Subtask agent(s), which additionally require file
    classification (see ``file_classification.py``).

    Args:
        chain: The resolved (and already-validated) hierarchy chain.
        epic_artifacts: Verified epic artifact references, if any were found.
        feature_artifacts: Verified feature artifact references, if any were found.
        subtask_agents: Classified Subtask scope agents. Classification is
            intentionally performed by ``file_classification.py`` and supplied
            here so composition remains independent of file discovery.
    """
    if chain.is_standalone:
        return HierarchyAssignment(outcome=AssignmentOutcome.STANDALONE, chain=chain, subtask_agents=subtask_agents)

    if not subtask_agents:
        raise ValueError("Non-standalone hierarchy assignments require at least one Subtask Agent")

    for agent in subtask_agents:
        if agent.scope_level is not AgentScopeLevel.SUBTASK:
            msg = (
                f"compose_assignment received a non-Subtask agent '{agent.agent_id}' "
                f"(scope_level={agent.scope_level.value!r}); "
                "only AgentScopeLevel.SUBTASK agents may be supplied as subtask_agents"
            )
            raise ValueError(msg)
        if agent.issue_key != chain.subtask_key:
            msg = (
                f"Subtask agent '{agent.agent_id}' has issue_key={agent.issue_key!r} "
                f"but the resolved chain subtask_key is {chain.subtask_key!r}; "
                "each subtask agent must be scoped to the resolved subtask key"
            )
            raise ValueError(msg)

    if chain.epic_key is not None and chain.feature_key is not None:
        return HierarchyAssignment(
            outcome=AssignmentOutcome.COMPLETE,
            chain=chain,
            epic_agent=_epic_scope(chain.epic_key, epic_artifacts),
            feature_agent=_feature_scope(chain.feature_key, feature_artifacts),
            subtask_agents=subtask_agents,
        )

    if chain.feature_key is not None and chain.epic_key is None:
        return HierarchyAssignment(
            outcome=AssignmentOutcome.FEATURE_ONLY,
            chain=chain,
            feature_agent=_feature_scope(chain.feature_key, feature_artifacts),
            subtask_agents=subtask_agents,
            degradation=DegradationRecord(
                reason="epic_not_found",
                missing_level="epic",
                resulting_topology=("feature", "subtask"),
            ),
        )

    # epic present, feature absent: leaf task directly beneath an epic
    # (FR-003, SC-008) — the absent feature-review level is recorded.
    return HierarchyAssignment(
        outcome=AssignmentOutcome.EPIC_SUBTASK,
        chain=chain,
        epic_agent=_epic_scope(chain.epic_key, epic_artifacts),  # type: ignore[arg-type]
        subtask_agents=subtask_agents,
        degradation=DegradationRecord(
            reason="feature_not_found",
            missing_level="feature",
            resulting_topology=("epic", "subtask"),
        ),
    )


def safe_stop(reason: str) -> HierarchyAssignment:
    """Return a ``SAFE_STOPPED`` assignment recording a discovery failure (FR-014).

    No agents are spawned; the caller is expected to record a
    ``hierarchy_discovery`` trace event with ``outcome: "failed"`` and this
    ``reason`` before halting.
    """
    return HierarchyAssignment(outcome=AssignmentOutcome.SAFE_STOPPED, chain=None)
