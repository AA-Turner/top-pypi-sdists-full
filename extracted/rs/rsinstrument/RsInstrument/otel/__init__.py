"""OpenTelemetry instrumentation for RsInstrument SCPI commands.

Import ``setup_otel`` and ``teardown_otel`` from this submodule::

    from RsInstrument.otel import setup_otel, teardown_otel

Call ``setup_otel()`` once at process start to monkey-patch
``RsInstrument`` with OTEL span and histogram instrumentation.
Call ``teardown_otel()`` to restore the original methods.
"""

from .patcher import (
    _OTEL_ENV_MAP as _OTEL_ENV_MAP,
    _ORIGINALS as _ORIGINALS,
    _apply_env_kwargs as _apply_env_kwargs,
    _patch_method as _patch_method,
    setup_otel,
    teardown_otel,
)

__all__ = [
    "setup_otel",
    "teardown_otel",
]
