"""Per-session behavioral policies — agent-control hooks bound to a session.

A :class:`SessionPolicy` is a Pydantic-modelled class with hook methods,
mirroring the :class:`~dreadnode.agents.tools.Toolset` pattern: subclass,
declare config as fields, decorate methods with ``@hook(EventType)``,
and the runtime collects them via :meth:`SessionPolicy.get_hooks` at
turn start.

Two shipped implementations:

- :class:`InteractiveSessionPolicy` — today's TUI behavior. No
  continuation hooks; ``ask_user()`` flows through the runtime's
  per-turn handler which publishes to both transports and awaits.
- :class:`HeadlessSessionPolicy` — autonomous mode. Auto-denies
  ``ask_user()`` (the runtime sees ``is_autonomous=True`` and
  short-circuits the prompt) and attaches a max-step hook that emits
  ``Finish`` once a configurable cap is hit.

Policies are resolved by name via :func:`resolve_policy` so clients can
request a mode with a simple string or ``{"name": ..., **params}`` dict
without importing Python classes across process boundaries.

Class-level metadata fields the runtime and TUI read for status UI:

- ``name`` — registry key. Required.
- ``is_autonomous`` — whether the session has no human in the loop.
  The TUI tags labels and gates background-task notifications by this.
  The runtime auto-denies ``ask_user()`` when true.
- ``display_label`` — short status-bar string when ``is_autonomous`` is
  true (``"auto"``, ``"strict"``, …). Defaults to empty.
"""

import typing as t

from loguru import logger
from pydantic import ConfigDict, Field, PrivateAttr

from dreadnode.agents.events import AgentStart, GenerationStep
from dreadnode.agents.reactions import Finish
from dreadnode.core.hook import Hook, hook
from dreadnode.core.meta.config import Model

if t.TYPE_CHECKING:
    from dreadnode.agents.engines.base import PolicyFacet


class SessionPolicy(Model):
    """Session-scoped agent-event hooks.

    Subclass and decorate methods with ``@hook(EventType)``. The
    runtime calls :meth:`get_hooks` at turn start to collect bound
    ``Hook`` instances, walking the MRO so inherited hooks are
    included and per-class overrides win.

    Class-level metadata fields:

    - ``name`` — registry key.
    - ``is_autonomous`` — runtime auto-denies ``ask_user()`` when true.
    - ``display_label`` — short label rendered by the TUI in autonomous
      sessions.

    Per-policy configuration goes in normal Pydantic fields (e.g.
    ``HeadlessSessionPolicy.max_steps``). ``extra="forbid"`` makes
    typos in ``resolve_policy`` payloads fail loudly. ``Hook`` is in
    ``ignored_types`` so the metaclass leaves ``@hook``-decorated
    methods alone instead of trying to interpret them as fields —
    same trick :class:`~dreadnode.agents.tools.Toolset` uses for
    ``ToolMethod`` (which sidesteps it by inheriting from
    ``property``).
    """

    model_config = ConfigDict(extra="forbid", ignored_types=(Hook,))

    name: t.ClassVar[str]
    is_autonomous: t.ClassVar[bool] = False
    display_label: t.ClassVar[str] = ""

    def required_facets(self) -> "set[PolicyFacet]":
        """Policy facets this policy needs the engine to honor.

        Mirrors an engine's :meth:`describe_enforcement`; the runtime reconciles
        the two (see ``dreadnode.policies.reconciliation`` and CAP-EGOV-*). The
        base requires autonomy handling and — when a human is in the loop —
        tool-approval HITL. Subclasses extend.
        """
        from dreadnode.agents.engines.base import PolicyFacet

        facets = {PolicyFacet.AUTONOMY}
        if not self.is_autonomous:
            facets.add(PolicyFacet.TOOL_APPROVAL)
        return facets

    @property
    def needs_permission_bridge(self) -> bool:
        """Whether the runtime should attach a ``PermissionBridge`` to the agent.

        Defaults to ``True`` for interactive (non-autonomous) policies.
        Subclasses may override to request the bridge even in autonomous
        mode (e.g. guard policies with ASK capabilities).
        """
        return not self.is_autonomous

    @property
    def hooks(self) -> list[Hook]:
        """All hooks declared on this policy, bound to ``self``.

        Walks the MRO and returns every attribute that is a ``Hook``
        descriptor, bound via :meth:`Hook.__get__`. Inherited hooks
        are included; subclass attributes of the same name shadow
        superclass ones (first occurrence in MRO order wins,
        mirroring :meth:`~dreadnode.agents.tools.Toolset.get_tools`).
        """
        hooks: list[Hook] = []
        seen: set[str] = set()
        for cls in type(self).__mro__:
            for attr, value in cls.__dict__.items():
                if attr in seen or not isinstance(value, Hook):
                    continue
                hooks.append(getattr(self, attr))  # descriptor binds via Hook.__get__
                seen.add(attr)
        return hooks


class InteractiveSessionPolicy(SessionPolicy):
    """Default policy — no continuation hooks, no special prompt handling.

    The runtime's per-turn human-prompt handler does the publish/await
    dance directly when ``is_autonomous`` is false. This policy holds
    no state and contributes no hooks; it exists so the
    ``"interactive"`` registry key resolves to a real type.
    """

    name: t.ClassVar[str] = "interactive"


class HeadlessSessionPolicy(SessionPolicy):
    """Autonomous mode with an optional step budget and no human in the loop.

    The runtime reads ``is_autonomous=True`` and resolves
    ``ask_user()`` to ``deny`` instantly without touching any
    transport. When set, ``max_steps`` is enforced by a ``GenerationStep`` hook
    that emits ``Finish(reason="max_steps=N reached")`` once the turn has run
    ``max_steps`` model turns. Tool fan-out and duplicate lifecycle events do
    not consume additional budget. Explicit ``None`` keeps the session autonomous
    without adding a policy step ceiling. The reset on ``AgentStart`` makes the
    counter per-turn rather than per-session, so a long chat with multiple turns
    each gets the full budget.
    """

    name: t.ClassVar[str] = "headless"
    is_autonomous: t.ClassVar[bool] = True
    display_label: t.ClassVar[str] = "auto"

    max_steps: int | None = Field(default=30, gt=0)

    _count: int = PrivateAttr(default=0)

    def required_facets(self) -> "set[PolicyFacet]":
        from dreadnode.agents.engines.base import PolicyFacet

        facets = super().required_facets()
        if self.max_steps is not None:
            facets.add(PolicyFacet.STEP_BUDGET)
        return facets

    @hook(AgentStart)
    async def reset_step_count(self, _event: AgentStart) -> None:
        self._count = 0

    @hook(GenerationStep)
    async def stop_on_max_steps(self, _event: GenerationStep) -> Finish | None:
        if self.max_steps is None:
            return None
        self._count += 1
        if self._count >= self.max_steps:
            return Finish(reason=f"max_steps={self.max_steps} reached")
        return None


_PolicySpec = str | dict[str, t.Any] | None

_REGISTRY: dict[str, type[SessionPolicy]] = {
    "interactive": InteractiveSessionPolicy,
    "headless": HeadlessSessionPolicy,
}


def register_policy(
    cls: type[SessionPolicy],
    *,
    name: str | None = None,
    replace: bool = False,
) -> type[SessionPolicy]:
    """Register a policy class into the global registry.

    The registry key defaults to ``cls.name``; pass ``name`` to
    override. Re-registering an existing name is a no-op unless
    ``replace=True``. Returns the class unchanged so this function
    can be used as a decorator.

    Capabilities ship policies by placing files under ``policies/``;
    the capability loader picks them up and routes them through this
    function.
    """
    key = name or getattr(cls, "name", None)
    if not key:
        raise ValueError(f"policy {cls.__name__} must define ``name`` class attribute")
    existing = _REGISTRY.get(key)
    if existing is not None and existing is not cls and not replace:
        logger.debug("Policy {} already registered, skipping re-register", key)
        return cls
    _REGISTRY[key] = cls
    return cls


def registered_policy_names() -> list[str]:
    """Return sorted list of policy names currently in the registry."""
    return sorted(_REGISTRY)


def get_policy_class(name: str) -> type[SessionPolicy] | None:
    """Look up a registered policy class by name."""
    return _REGISTRY.get(name)


def resolve_policy(spec: _PolicySpec) -> SessionPolicy:
    """Resolve a policy spec from the API into a policy instance.

    ``spec`` may be:
      - ``None`` or ``"interactive"`` → default interactive policy
      - a string matching a registered name → policy with default params
      - a dict ``{"name": ..., **params}`` → policy with keyword params

    Unknown names raise ``ValueError`` so mis-typed policy names in a
    request payload fail loudly at session-create time instead of
    silently falling back to interactive.
    """
    if spec is None:
        return InteractiveSessionPolicy()
    if isinstance(spec, str):
        name, params = spec, {}
    else:
        name = spec.get("name", "interactive")
        params = {k: v for k, v in spec.items() if k != "name"}
    cls = _REGISTRY.get(name)
    if cls is None:
        available = ", ".join(sorted(_REGISTRY))
        raise ValueError(f"unknown session policy {name!r}; known: {available}")
    return cls(**params)


# Bottom-of-file registration so ``guard`` can ``from dreadnode.policies
# import HeadlessSessionPolicy`` — by this point the parent class is already
# bound on the package module.
from dreadnode.policies.guard import GuardSessionPolicy  # noqa: E402

_REGISTRY[GuardSessionPolicy.name] = GuardSessionPolicy


__all__ = [
    "GuardSessionPolicy",
    "HeadlessSessionPolicy",
    "InteractiveSessionPolicy",
    "SessionPolicy",
    "get_policy_class",
    "register_policy",
    "registered_policy_names",
    "resolve_policy",
]
