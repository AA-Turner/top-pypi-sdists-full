from __future__ import annotations

import logging
import os
import warnings

# The ONE source of truth for quieting the framework's log flood for LOCAL SDK use. It lives
# outside `mistralai.workflows.*` on purpose: importing anything under that namespace fires the
# framework's import-time banners (workflows/__init__ -> exports), so the SDK entry point
# (mistralai/agents/__init__.py) must raise the noisy loggers BEFORE that import resolves. Only
# logging/os/warnings/structlog and Authlib's small deprecate module are imported here, so this
# module is safe to import first. The runtime message filter (for records structlog writes
# straight to a handler) is applied later by sdk/quiet.py, which imports the name lists from here.
# AGENTS_SDK_DEBUG=1 disables all of it.

DEBUG_ENV = "AGENTS_SDK_DEBUG"


def debug_enabled() -> bool:
    return bool(os.environ.get(DEBUG_ENV))


# The [Workflow]/telemetry INFO chatter an SDK caller never wants. Named individually (verified by
# capturing one local run) rather than by parent namespace, so any unlisted logger's warnings/errors
# still surface.
QUIET_WARNING = (
    "mistralai.workflows.core.config.config",
    "mistralai.workflows.core.workflow",
    "kazekit.feature_flags.feature_flag_service",
    "kazekit.feature_flags.feature_flag_service_factory",
)
# Fully silenced: the WARNING/ERROR a non-Temporal (local) run unavoidably emits because there is
# no activity context to publish events into, plus the benign OTel context-detach race.
QUIET_CRITICAL = (
    "mistralai.workflows.core._events.event_context",
    "mistralai.workflows.core._events.event_utils",
    "opentelemetry.context",
)
# Records structlog writes straight to a handler at runtime, which a per-logger level cannot catch;
# dropped by message. The import banners are gated by presilence() raising their loggers before
# import; they are listed here too as a backstop for any unusual import order.
DROP_MESSAGES = (
    "Failed to detach context",
    "Configuration loaded",
    "Workflow registered WITHOUT versioning behavior",
    # SDK agents always run enforce_determinism=False (their loop is nondeterministic by design), so
    # this warning fires on every serve/deploy and is expected noise, not a signal.
    "Workflow registered with determinism enforcement disabled",
)

# The loggers that emit DROP_MESSAGES. The message filter is attached to each of them, not only to
# the root handlers, which the worker replaces when it sets up its logging at startup.
NOISY_LOGGERS = (
    "mistralai.workflows.core.config.config",
    "mistralai.workflows.core.workflow",
    "opentelemetry.context",
)

# Loggers whose import-time banners fire while structlog is still in its DEFAULT config
# (printing straight to stderr, ignoring stdlib levels). They are raised during the import window,
# then restored after the workflows import so real runtime warnings still surface.
_BANNER_LOGGERS = (
    "mistralai.workflows.core.config.config",
    "mistralai.workflows.core.workflow",
)

_presilenced = False
_banner_logger_levels: dict[str, int] = {}


def presilence() -> None:
    # Raise the noisy loggers to WARNING/CRITICAL by NAME only (touches no framework module, so it
    # runs BEFORE `mistralai.workflows` is imported) and point structlog at the stdlib factory with
    # level filtering so the import-time banners honor those levels during the import window. The
    # framework calls its own structlog.configure() later at app/worker startup, fully replacing
    # this (cache_logger_on_first_use=False so nothing caches the transient config). Idempotent;
    # no-op under AGENTS_SDK_DEBUG=1.
    global _presilenced, _banner_logger_levels
    if _presilenced or debug_enabled():
        return
    _presilenced = True
    _banner_logger_levels = {name: logging.getLogger(name).level for name in _BANNER_LOGGERS}
    for name in QUIET_WARNING:
        logging.getLogger(name).setLevel(logging.WARNING)
    for name in _BANNER_LOGGERS:
        logging.getLogger(name).setLevel(logging.ERROR)
    for name in QUIET_CRITICAL:
        logging.getLogger(name).setLevel(logging.CRITICAL)
    _ignore_authlib_httpx_deprecation()
    import structlog  # noqa: PLC0415

    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=False,
    )


def _ignore_authlib_httpx_deprecation() -> None:
    # Authlib >= 1.8 warns when its httpx integration is imported without `httpx2` installed
    # (authlib/integrations/httpx_client/_compat.py), and `mistralai.extra.mcp.auth` imports it on
    # every SDK load. The user cannot act on it. Authlib installs an "always" filter for its warning
    # class when authlib.deprecate is first imported (authlib/deprecate.py), so import it first:
    # a filter added after it takes precedence. Only this message is ignored; other Authlib
    # deprecations still surface.
    from authlib.deprecate import AuthlibDeprecationWarning  # type: ignore[import-untyped]  # noqa: PLC0415

    warnings.filterwarnings("ignore", message="The httpx module is deprecated", category=AuthlibDeprecationWarning)


def restore_runtime_warning_levels() -> None:
    if debug_enabled():
        return
    for name, level in _banner_logger_levels.items():
        logging.getLogger(name).setLevel(level)
