"""Engine contract for the agent loop.

An :class:`AgentEngine` owns the *interior* of an agent — the loop that turns a
goal into generation/tool events. The native engine is the default; foreign
engines (e.g. ``claude-code``) delegate the loop to an external harness while the
rest of the stack (sessions, eval, optimization, policy, telemetry, TUI) keeps
working because the foreign agent is still an :class:`~dreadnode.agents.agent.Agent`.

See ``specs/capabilities/engines.md`` (ENG-*) for the canonical contract.
"""

import typing as t
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import StrEnum

if t.TYPE_CHECKING:
    from dreadnode.agents.agent import Agent
    from dreadnode.agents.events import AgentEvent
    from dreadnode.agents.trajectory import Trajectory


class PolicyFacet(StrEnum):
    """A single governable dimension of a session policy.

    An engine declares, per facet, whether it *enforces* it, *bridges* it via a
    harness callback, can only *observe* it, or has *no equivalent* mechanism.
    The runtime reconciles the session policy against that declaration (ENG-REC-*).
    """

    AUTONOMY = "autonomy"
    """Block-vs-auto-allow (native ``is_autonomous`` / harness ``permission_mode``)."""
    TOOL_APPROVAL = "tool_approval"
    """Human-in-the-loop tool approval (``ask_user`` → ``prompt.required``)."""
    STEP_BUDGET = "step_budget"
    """Step/turn ceiling (``max_steps`` / harness ``max_turns``)."""
    TOKEN_BUDGET = "token_budget"  # noqa: S105  (facet name, not a secret)
    """Token ceiling (no harness equivalent — enforced by killing the run)."""
    COST_BUDGET = "cost_budget"
    """Cost ceiling (no harness equivalent — enforced by killing the run)."""
    TIME_BUDGET = "time_budget"
    """Wall-clock ceiling (no harness equivalent — enforced by killing the run)."""
    GUARD_STEERING = "guard_steering"
    """Mid-loop prevention/steering via hook ``Reaction`` (in-loop only)."""
    SCORERS = "scorers"
    """Observational scorers/detectors/metrics (attach to events after the fact)."""


class CapabilityComponent(StrEnum):
    """A kind of capability-declared resource an engine may or may not consume.

    The native engine consumes all kinds (it executes our tools in-loop and
    surfaces our skills). A foreign engine that brings its own tools declares a
    subset; the runtime informs the author which declared components are inert
    under that engine (CAP-ENG-022). See ``specs/capabilities/engines.md``.
    """

    PYTHON_TOOLS = "python_tools"
    """Capability ``@tool`` / MCP tools from our registry, executed in-loop."""
    MCP_SERVERS = "mcp_servers"
    """MCP servers the capability declares (folded with python_tools today)."""
    SKILLS = "skills"
    """``SKILL.md`` directories (the shared Agent Skills standard)."""


@dataclass(frozen=True)
class EnforcementSurface:
    """What an engine can actually do about each policy facet.

    A facet absent from all four sets is treated as ``observes_only`` by the
    reconciler (the conservative default).
    """

    enforces: frozenset[PolicyFacet] = field(default_factory=frozenset)
    """Enforced natively or by translatable config (e.g. ``permission_mode``)."""
    bridges: frozenset[PolicyFacet] = field(default_factory=frozenset)
    """Enforced by wiring a harness callback back into our control plane."""
    observes_only: frozenset[PolicyFacet] = field(default_factory=frozenset)
    """Visible after the harness acted — can record, cannot prevent."""
    no_equivalent: frozenset[PolicyFacet] = field(default_factory=frozenset)
    """No mechanism in the harness — enforceable only by killing the run."""

    @classmethod
    def all_enforced(cls) -> "EnforcementSurface":
        """The native engine's surface: it owns the loop, so it enforces everything."""
        return cls(enforces=frozenset(PolicyFacet))


@t.runtime_checkable
class PermissionBridge(t.Protocol):
    """Bridges a harness tool-approval callback into the native HITL path.

    Implemented by the runtime over ``_human_prompt_handler`` so a foreign
    engine's ``can_use_tool`` reuses the existing ``prompt.required`` /
    ``prompt.respond`` protocol (TUI widget, eval-worker auto-deny). Wired in M1.
    """

    async def request_tool_approval(
        self, *, tool_name: str, tool_input: dict[str, t.Any]
    ) -> bool: ...


@dataclass
class EngineContext:
    """Everything an engine needs to run one turn.

    The native engine uses only ``agent`` + ``trajectory`` (it reaches the rest
    through ``agent``). Foreign engines additionally use ``goal``, ``dispatch``
    (to run observational hooks on translated events), and ``permission``.
    """

    agent: "Agent"
    trajectory: "Trajectory"
    goal: str
    dispatch: "t.Callable[[AgentEvent], t.AsyncIterator[AgentEvent]]"
    """Run an event through the agent's hooks (metrics + reactions). Foreign
    engines call this per translated event; the native engine dispatches inline."""
    permission: "PermissionBridge | None" = None


class AgentEngine(ABC):
    """Pluggable owner of the agent loop.

    Implementations live in this package (built-ins) or are supplied by a
    customer via a ``mod:attr`` reference. Built-ins register via
    :func:`~dreadnode.agents.engines.register_engine`.
    """

    name: t.ClassVar[str]
    """Stable identifier used in ``engine:`` declarations and the registry."""

    dispatches_internally: t.ClassVar[bool] = False
    """True when ``run_loop`` already routes its events through ``ctx.dispatch``
    (the native engine does, inline). Foreign engines leave this False and call
    ``ctx.dispatch`` themselves on translated events."""

    @abstractmethod
    def run_loop(self, ctx: EngineContext) -> "t.AsyncIterator[AgentEvent]":
        """Drive one turn, yielding native ``AgentEvent``s as it progresses."""
        ...

    def describe_enforcement(self, policy: t.Any) -> EnforcementSurface:  # noqa: ARG002
        """Declare which policy facets this engine can enforce for ``policy``.

        Defaults to fully-enforced (correct for any engine that owns a native
        loop). Foreign engines override with an honest, partial surface.
        """
        return EnforcementSurface.all_enforced()

    def honored_config(self) -> set[str] | None:
        """Which ``Agent`` config fields this engine respects.

        ``None`` means "all" (the native engine). A foreign engine returns the
        explicit set it honors so the runtime can warn about ignored config.
        """
        return None

    def consumed_components(self) -> set[CapabilityComponent]:
        """Which capability component kinds this engine consumes.

        Defaults to all (the native engine executes our tools in-loop and
        surfaces our skills). A foreign engine that uses its own tools returns a
        subset; the runtime informs the author about the unconsumed components
        a capability declares (CAP-ENG-022).
        """
        return set(CapabilityComponent)
