"""Single install loop for FrameworkAdapter-backed integrations.

One pass installs both surfaces — tracing and autonomous — for every
adapter registered via ``@register_adapter``. Called once from
:meth:`Aigie.initialize` after the autonomous runtime is constructed.

Legacy frameworks that have not migrated to the FrameworkAdapter ABC
keep their per-framework ``enable_*()`` path in
:mod:`aigie.auto_instrument`. They have no entry in the adapter
registry, so this loop skips them naturally.

To migrate a framework onto the ABC:
1. Implement its ``FrameworkAdapter`` subclass with ``@register_adapter``.
2. Add its package import to :data:`_ADAPTER_PACKAGES` below.
3. Delete its ``enable_*()`` function from ``aigie/auto_instrument/__init__.py``.
"""

from __future__ import annotations

import importlib
import logging
from typing import Any

logger = logging.getLogger(__name__)


_ADAPTER_PACKAGES: tuple[str, ...] = (
    "aigie.integrations.langgraph",
    "aigie.integrations.langchain",
    "aigie.integrations.claude_agent_sdk",
)


def install_framework_adapters(*, aigie: Any = None, runtime: Any = None) -> None:
    """Install every registered FrameworkAdapter on both surfaces.

    ``aigie`` enables the tracing surface (an emitter is built and passed).
    ``runtime`` enables the autonomous surface. Either or both may be
    ``None`` — the adapter only installs the surfaces it received.
    """
    for pkg in _ADAPTER_PACKAGES:
        try:
            importlib.import_module(pkg)
        except Exception as exc:  # noqa: BLE001
            logger.debug("adapter import skipped (%s): %s", pkg, exc)

    from aigie.autonomous import adapters as _registry
    from aigie.tracing.emitter import TraceEmitter

    for framework in sorted(_registry.registered_frameworks()):
        adapter = _registry.get(framework)
        if adapter is None:
            continue
        # Each adapter gets its OWN emitter. Span-complete hooks (the error
        # enricher) are registered per emitter, so a per-adapter emitter keeps
        # one framework's enricher from running on another framework's spans —
        # each framework's spans flow through its own emitter. They share
        # aigie._buffer, so wire output is unchanged.
        emitter = TraceEmitter(aigie) if aigie is not None else None
        try:
            adapter.install(runtime=runtime, emitter=emitter)
        except Exception as exc:  # noqa: BLE001
            logger.warning("FrameworkAdapter.install failed for %s: %s", framework, exc)
