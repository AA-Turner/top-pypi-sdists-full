"""Every httpx-API flavor a provider SDK can raise from — the ONE place that knows them.

``anthropic>=1.0`` and ``openai>=3.0`` (and every OpenAI-built SDK after it) run on
``httpx2``; supabase, MCP, Google and our own clients still run on ``httpx``. The two
share an API and NOTHING else: ``httpx2.ReadTimeout`` is not an ``httpx.ReadTimeout``,
nor a subclass of one. An ``isinstance(exc, httpx.TimeoutException)`` check therefore
misses every timeout an httpx2 SDK raises, and the failure falls through to string
guessing — a dropped Claude stream classified as an ``unknown_error`` instead of a
retryable transport failure.

So no classifier names ``httpx.<Error>`` directly. It asks ``transport_classes(...)``
for the class from EVERY installed flavor. A flavor that is installed but no longer
exports one of the names asked for is drift; ``tests/providers/test_every_transport_and_sdk_error_we_classify_exists.py``
fails on it, so a rename breaks the build instead of silently shrinking a tuple.
"""

from __future__ import annotations

from types import ModuleType

import httpx

try:
    import httpx2
except ImportError:  # optional: present whenever an httpx2-built SDK is installed
    httpx2 = None

HTTPX_FLAVORS: tuple[ModuleType, ...] = tuple(m for m in (httpx, httpx2) if m is not None)


def transport_classes(*names: str) -> tuple[type[BaseException], ...]:
    """The named exception class from every installed httpx flavor, for ``isinstance``."""
    found: list[type[BaseException]] = []
    for module in HTTPX_FLAVORS:
        for name in names:
            cls = getattr(module, name, None)
            if isinstance(cls, type) and issubclass(cls, BaseException):
                found.append(cls)
    return tuple(found)


def missing_transport_names(*names: str) -> list[str]:
    """``flavor.Name`` for every asked-for name an installed flavor does not export."""
    return [
        f"{module.__name__}.{name}"
        for module in HTTPX_FLAVORS
        for name in names
        if not isinstance(getattr(module, name, None), type)
    ]
