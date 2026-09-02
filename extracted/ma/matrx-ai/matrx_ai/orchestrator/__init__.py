"""matrx_ai.orchestrator — execution engine, requests, resolvers.

LAZY FACADE (PEP 562). This package's public names used to be imported
EAGERLY here — which meant that importing ANY orchestrator submodule (e.g.
``matrx_ai.orchestrator.requests``, pulled at module scope by
``providers/unified_client.py`` and ``providers/snapshot.py``) first executed
this __init__ and dragged in ``executor`` + ``concurrent_engine`` +
``parallel_executor`` — a huge closure that itself reaches back into
``matrx_ai.providers`` and ``matrx_ai.tools``. That structural edge is what
made ``import matrx_ai.providers`` fragile in client hosts: one innocent
module-scope ``from matrx_ai.providers import X`` anywhere in the executor's
closure turned a cold providers import into a circular-import crash
(matrx-local shipped an "import matrx_ai.orchestrator first" workaround for
exactly this).

Every public name now resolves on FIRST ATTRIBUTE ACCESS. Importing an
orchestrator submodule no longer imports the executor, and
``from matrx_ai.orchestrator import execute_until_complete`` keeps working
exactly as before in every host.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # static analysis only — never imported at runtime
    from matrx_ai.orchestrator.concurrent_engine import (
        BatchResult,
        ConcurrentEngine,
        EngineConfig,
        ItemOutcome,
        WarmupStrategy,
        WorkerResultError,
    )
    from matrx_ai.orchestrator.executor import execute_ai_request, execute_until_complete
    from matrx_ai.orchestrator.parallel_executor import ParallelResult, parallel_execute
    from matrx_ai.orchestrator.requests import AIMatrixRequest, CompletedRequest
    from matrx_ai.orchestrator.tracking import TimingUsage, ToolCallUsage

# public name -> submodule that defines it
_LAZY_EXPORTS: dict[str, str] = {
    "BatchResult": "concurrent_engine",
    "ConcurrentEngine": "concurrent_engine",
    "EngineConfig": "concurrent_engine",
    "ItemOutcome": "concurrent_engine",
    "WarmupStrategy": "concurrent_engine",
    "WorkerResultError": "concurrent_engine",
    "execute_ai_request": "executor",
    "execute_until_complete": "executor",
    "ParallelResult": "parallel_executor",
    "parallel_execute": "parallel_executor",
    "AIMatrixRequest": "requests",
    "CompletedRequest": "requests",
    "TimingUsage": "tracking",
    "ToolCallUsage": "tracking",
}

__all__ = sorted(_LAZY_EXPORTS)


def __getattr__(name: str) -> Any:
    module_name = _LAZY_EXPORTS.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    import importlib

    module = importlib.import_module(f".{module_name}", __name__)
    value = getattr(module, name)
    globals()[name] = value  # cache: __getattr__ fires once per name
    return value


def __dir__() -> list[str]:
    return sorted(__all__)
