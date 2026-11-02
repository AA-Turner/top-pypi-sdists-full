"""Action registry — a second registry alongside NodeRegistry.

Every `@action` function registers in two places:

- ``node_registry`` (from matrx_graph.executor.registry) — so the scheduler
  can dispatch the registered node directly by its bare dotted name.
- ``action_registry`` (here) — so UIs can enumerate actions by name, filter
  by determinism tier or category, and hand ``tool.call`` a resolver.

Keeping the action metadata separate from NodeSpec lets us add things like
cost estimates, ownership, call-budgets, and search indexes later without
polluting the core engine type.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from matrx_graph.actions.spec import ActionSpec
from matrx_graph.errors import NodeRegistryError

#: ``async (name, app) -> ActionSpec | None`` — a host source of GENERATED Actions whose
#: declarations are rows, not code (every saved workflow, every typed agent). Resolved by
#: name at call time, never loaded at boot: the registry stays one registry, the rows stay
#: in the database.
ActionSource = Callable[[str, Any], Awaitable[ActionSpec | None]]


class ActionRegistry:
    """Holds ActionSpec by action name."""

    def __init__(self) -> None:
        self._actions: dict[str, ActionSpec] = {}
        self._sources: dict[str, ActionSource] = {}

    def register(self, action: ActionSpec, *, overwrite: bool = False) -> None:
        if not overwrite and action.name in self._actions:
            raise NodeRegistryError(
                f"Action '{action.name}' is already registered. Pass overwrite=True to replace."
            )
        self._actions[action.name] = action

    def unregister(self, name: str) -> None:
        self._actions.pop(name, None)

    def get(self, name: str) -> ActionSpec:
        try:
            return self._actions[name]
        except KeyError as e:
            known = sorted(self._actions)
            raise NodeRegistryError(
                f"No action registered with name '{name}'. Known: {known!r}."
            ) from e

    def add_source(self, prefix: str, source: ActionSource) -> None:
        """A host plugs in a lazy source of generated Actions named ``<prefix>.<…>``
        (e.g. ``workflow``, ``agent``). Re-adding the same source is a no-op."""
        existing = self._sources.get(prefix)
        if existing is not None and existing is not source:
            raise NodeRegistryError(f"Action source '{prefix}' is already registered by {existing!r}.")
        self._sources[prefix] = source

    def sources(self) -> list[str]:
        return sorted(self._sources)

    async def resolve(self, name: str, *, app: Any = None) -> ActionSpec:
        """THE lookup every door uses: a declared Action, else a generated one from the
        source its prefix names (as the caller ``app`` — a row the caller cannot see is
        not found). Unknown names raise ``NodeRegistryError``, never None."""
        if name in self._actions:
            return self._actions[name]
        source = self._sources.get(name.split(".", 1)[0])
        if source is not None:
            spec = await source(name, app)
            if spec is not None:
                return spec
            raise NodeRegistryError(f"No action named '{name}' exists that this caller can run.")
        return self.get(name)

    def has(self, name: str) -> bool:
        return name in self._actions

    def all(self) -> list[ActionSpec]:
        return list(self._actions.values())

    def names(self) -> list[str]:
        return list(self._actions)

    def catalog(self) -> list[dict[str, object]]:
        return [a.to_descriptor() for a in self.all()]

    def clear(self) -> None:
        self._actions.clear()


_default_action_registry = ActionRegistry()


def default_action_registry() -> ActionRegistry:
    return _default_action_registry
