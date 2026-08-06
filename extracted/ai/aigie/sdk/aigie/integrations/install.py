"""Single install loop for FrameworkAdapter-backed integrations.

One pass installs the tracing surface for every adapter registered via
``@register_adapter``. Called once from :meth:`Aigie.initialize`.

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
    "aigie.integrations.strands",
    "aigie.integrations.openai_agents",
)


def _register_source_enricher(emitter: Any, aigie: Any) -> None:
    """Register the SDK-source enricher that stamps the root span."""
    from aigie import __version__
    from aigie.tracing.source_enricher import SdkSourceEnricher

    emitter.register_span_complete_hook(
        SdkSourceEnricher(
            sdk_version=__version__,
            agent_name=getattr(aigie, "_agent_name", None),
        )
    )


def install_adapter(framework: str, *, aigie: Any = None, coordinator: Any = None) -> bool:
    """Install one registered adapter's tracing surface.

    Returns True when the adapter was found and installed without raising.
    Shared by the bulk :func:`install_framework_adapters` pass and the
    per-framework registry entry points (``aigie.patch("<framework>")``), so
    both routes wire the emitter identically.
    """
    from aigie.integrations import _base as _registry
    from aigie.tracing.emitter import TraceEmitter

    adapter = _registry.get(framework)
    if adapter is None:
        return False
    emitter = TraceEmitter(aigie) if aigie is not None else None
    if emitter is not None:
        _register_source_enricher(emitter, aigie)
    try:
        adapter.install(emitter=emitter, coordinator=coordinator)
    except Exception as exc:  # noqa: BLE001
        logger.warning("FrameworkAdapter.install failed for %s: %s", framework, exc)
        return False
    return True


def install_framework_adapters(*, aigie: Any = None) -> None:
    """Install every registered FrameworkAdapter's tracing surface.

    ``aigie`` enables the tracing surface (an emitter is built and passed).
    When ``None`` the adapter receives no emitter and installs nothing.
    """
    for pkg in _ADAPTER_PACKAGES:
        try:
            importlib.import_module(pkg)
        except Exception as exc:  # noqa: BLE001
            logger.debug("adapter import skipped (%s): %s", pkg, exc)

    from aigie.integrations import _base as _registry

    coordinator = getattr(aigie, "_rewind_coordinator", None)

    for framework in sorted(_registry.registered_frameworks()):
        install_adapter(framework, aigie=aigie, coordinator=coordinator)
