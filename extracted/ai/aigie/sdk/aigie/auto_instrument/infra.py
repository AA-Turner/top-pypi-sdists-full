"""
Infrastructure auto-instrumentation for Aigie SDK.

Detects installed Python libraries (databases, HTTP clients, caches)
and instruments them using OTel instrumentor packages.

Usage:
    This module is called automatically by enable_infra() during aigie.init().
    No user action required — just having the library installed triggers instrumentation.

    For DB/HTTP visibility, users install the OTel instrumentor extras:
        pip install aigie[otel-infra]
    Or individual packages:
        pip install opentelemetry-instrumentation-psycopg2
"""

from __future__ import annotations

import importlib
import importlib.util
import logging
import threading
from typing import NamedTuple

logger = logging.getLogger(__name__)

_lock = threading.Lock()


class InstrumentorSpec(NamedTuple):
    """Specification for an OTel instrumentor."""

    lib_name: str  # Python package to check for (e.g., "psycopg2")
    module_path: str  # OTel instrumentor module
    class_name: str  # Instrumentor class name
    alt_lib_names: tuple[str, ...] = ()  # Alternative import names


# Libraries we can instrument, ordered by commonality
INSTRUMENTABLE_LIBRARIES: tuple[InstrumentorSpec, ...] = (
    # Databases
    InstrumentorSpec(
        lib_name="psycopg2",
        module_path="opentelemetry.instrumentation.psycopg2",
        class_name="Psycopg2Instrumentor",
        alt_lib_names=("psycopg2cffi",),
    ),
    InstrumentorSpec(
        lib_name="asyncpg",
        module_path="opentelemetry.instrumentation.asyncpg",
        class_name="AsyncPGInstrumentor",
    ),
    InstrumentorSpec(
        lib_name="sqlalchemy",
        module_path="opentelemetry.instrumentation.sqlalchemy",
        class_name="SQLAlchemyInstrumentor",
    ),
    InstrumentorSpec(
        lib_name="pymongo",
        module_path="opentelemetry.instrumentation.pymongo",
        class_name="PymongoInstrumentor",
    ),
    # Cache
    InstrumentorSpec(
        lib_name="redis",
        module_path="opentelemetry.instrumentation.redis",
        class_name="RedisInstrumentor",
    ),
    # HTTP clients
    InstrumentorSpec(
        lib_name="httpx",
        module_path="opentelemetry.instrumentation.httpx",
        class_name="HTTPXClientInstrumentor",
    ),
    InstrumentorSpec(
        lib_name="requests",
        module_path="opentelemetry.instrumentation.requests",
        class_name="RequestsInstrumentor",
    ),
    InstrumentorSpec(
        lib_name="aiohttp",
        module_path="opentelemetry.instrumentation.aiohttp_client",
        class_name="AioHttpClientInstrumentor",
    ),
)

# Track which libraries we've instrumented (for disable_all)
_instrumented: list[tuple[str, object]] = []


def _is_library_installed(spec: InstrumentorSpec) -> bool:
    """Check if the target library is importable (without executing it)."""
    if importlib.util.find_spec(spec.lib_name) is not None:
        return True
    return any(importlib.util.find_spec(alt) is not None for alt in spec.alt_lib_names)


def detect_and_instrument() -> list[str]:
    """
    Auto-detect installed libraries and instrument them with OTel instrumentors.

    Returns list of library names that were successfully instrumented.
    Only instruments libraries where both the library AND its OTel instrumentor
    package are installed. Thread-safe.
    """
    instrumented_names: list[str] = []

    with _lock:
        already_tracked = {name for name, _ in _instrumented}

        for spec in INSTRUMENTABLE_LIBRARIES:
            if spec.lib_name in already_tracked:
                logger.debug("Skipping %s — already tracked by Aigie", spec.lib_name)
                continue

            if not _is_library_installed(spec):
                continue

            try:
                mod = importlib.import_module(spec.module_path)
                instrumentor_cls = getattr(mod, spec.class_name)
                instrumentor = instrumentor_cls()

                # Skip if already instrumented by another OTel setup
                if hasattr(instrumentor, "is_instrumented") and instrumentor.is_instrumented():
                    logger.debug("Skipping %s — already instrumented by OTel", spec.lib_name)
                    continue

                instrumentor.instrument()
                _instrumented.append((spec.lib_name, instrumentor))
                instrumented_names.append(spec.lib_name)
                logger.debug("Auto-instrumented %s via OTel", spec.lib_name)

            except ImportError:
                logger.debug(
                    "%s is installed but OTel instrumentor (%s) is not — skipping",
                    spec.lib_name,
                    spec.module_path,
                )
            except Exception:
                logger.warning("Failed to instrument %s", spec.lib_name, exc_info=True)

    return instrumented_names


def uninstrument_all() -> None:
    """Remove all OTel instrumentation we added. Thread-safe."""
    with _lock:
        items = list(_instrumented)
        _instrumented.clear()

    for lib_name, instrumentor in items:
        try:
            if hasattr(instrumentor, "uninstrument"):
                instrumentor.uninstrument()
                logger.debug("Uninstrumented %s", lib_name)
        except Exception:
            logger.warning("Failed to uninstrument %s", lib_name, exc_info=True)
