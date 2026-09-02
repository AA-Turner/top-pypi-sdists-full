"""Agent-definition (agx_) managers and row->config mapping.

LAZY FACADE (PEP 562). The real module body lives in ``_agx_manager_impl.py`` and
constructs classes/singletons from HOST-INJECTED ORM bases at module scope,
which requires ``matrx_ai.configure()``. Importing THIS module is therefore
always safe in an unconfigured environment — the impl is imported (and the
managers built, memoized by normal module caching) on FIRST ATTRIBUTE ACCESS,
so config errors surface at call time, never import time. Every public name of
the impl is re-exported unchanged; ``from matrx_ai.db.agx_manager import ...``
keeps working exactly as before in a configured host.

``agx`` is a transparent proxy over the real ``AgxManagers`` singleton. Its
``load_for_execution`` checks the client-host ``ExecutionAgentSource`` seam
BEFORE importing the ORM-backed impl (client hosts have no bases). Every
other attribute (``agx_agent``, ``agx_version``, …) is delegated to the real
managers on first access.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # static analysis only — never imported at runtime
    from ._agx_manager_impl import *  # noqa: F403


class _AgxFacade:
    async def load_for_execution(self, resolved_id: str, is_version: bool = False) -> Any:
        from matrx_ai.client_host.agent_source import try_load_from_execution_source

        loaded = await try_load_from_execution_source(resolved_id, is_version=is_version)
        if loaded is not None:
            return loaded

        from . import _agx_manager_impl as _impl

        return await _impl.agx.load_for_execution(resolved_id, is_version=is_version)

    def __getattr__(self, name: str) -> Any:
        from . import _agx_manager_impl as _impl

        return getattr(_impl.agx, name)


agx = _AgxFacade()


def __getattr__(name: str) -> Any:
    if name.startswith("__"):
        raise AttributeError(name)
    from . import _agx_manager_impl as _impl

    try:
        value = getattr(_impl, name)
    except AttributeError:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from None
    globals()[name] = value  # cache: __getattr__ fires once per name
    return value


def __dir__() -> list[str]:
    from . import _agx_manager_impl as _impl

    return sorted(n for n in dir(_impl) if not n.startswith("_"))
