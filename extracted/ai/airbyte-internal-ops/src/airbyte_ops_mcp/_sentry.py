# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Sentry error tracking integration for airbyte-ops-mcp.

This module provides automatic error tracking via Sentry for the airbyte-ops-mcp
package. Errors during server startup, tool execution, and API interactions are
automatically captured and reported.

The Sentry DSN is embedded in the package since it only allows write access
(sending errors), not read access. This is standard practice for client-side
error tracking.

Sentry only initializes when `SENTRY_ENVIRONMENT` is set; unset means "not a
deployed environment" (laptops, CI test runs) and no events are sent. It is
set to `production`/`preview` on the ops-webapp and ops-mcp Cloud Run services
via Pulumi (`infra/`), and to `production` in
`.github/workflows/rollout-autopilot.yml` (the autopilot cron acts on prod;
its runs are distinguishable by `server_name` and `cli.command` names).

Performance tracing is enabled so DB and HTTP work shows up as spans. The
`SqlalchemyIntegration` and `StarletteIntegration` are both auto-enabling, so
merely having those packages installed instruments every Prod DB Replica query
and every webapp request without an explicit integration list.

Modes:

- `"mcp"` — MCP server processes (`airbyte-ops-mcp-http`, the webapp's
  FastMCP backend in `app.py`): the Starlette integration is disabled so
  the trace root is the `mcp.server tools/call …` transaction rather than
  the `/mcp` HTTP request.
- `"webapp"` — the `serve.py` host process: page routes keep `http.server`
  transactions; the `/mcp` proxy route (browser→backend transport,
  including the 300s SSE listen stream and `DELETE` session teardown) is
  never sampled.

Bind parameter values are deliberately *not* recorded. `record_sql_queries`
drops them unless `_experiments={"record_sql_params": True}`, which is
all-or-nothing and would ship operator search strings (`name_contains`,
`email_domain`) to Sentry. Selected, redacted parameters are attached instead by
`prod_db_access.queries`, which can make the per-parameter call.

To change the trace sample rate (default: 1.0 — query volume is low enough that
sampling would only cost fidelity), set:
    SENTRY_TRACES_SAMPLE_RATE=0.25
"""

import contextlib
import logging
import os
from collections.abc import Iterator
from typing import Any, Literal

import sentry_sdk
from sentry_sdk.integrations.starlette import StarletteIntegration

# Valid Sentry severity levels
SentryLevel = Literal["fatal", "error", "warning", "info", "debug"]

# Process role for `init_sentry_tracking` — see module docstring.
SentryMode = Literal["mcp", "webapp"]

logger = logging.getLogger(__name__)

# Environment variable to override the performance trace sample rate
TRACES_SAMPLE_RATE_ENV_VAR = "SENTRY_TRACES_SAMPLE_RATE"

# Environment variable declaring the deployment environment; Sentry only
# initializes when this is set.
SENTRY_ENVIRONMENT_ENV_VAR = "SENTRY_ENVIRONMENT"

DEFAULT_TRACES_SAMPLE_RATE = 1.0
"""Sample every trace; this is ops tooling, not user-facing traffic."""

# Sentry DSN for the airbyte-ops-mcp project
# This DSN only allows sending errors to Sentry, not reading data.
# It is safe to embed in client-side code per Sentry's documentation.
# Project: https://airbytehq.sentry.io/projects/internal-ops-app/
_SENTRY_DSN = "https://292842cbf7f632f34c68cff23f2deee3@o1009025.ingest.us.sentry.io/4510746336559104"

_sentry_initialized = False


def _get_package_version() -> str:
    """Get the package version for Sentry release tracking."""
    try:
        from importlib.metadata import version

        return version("airbyte-internal-ops")
    except Exception as exc:
        logger.debug("Failed to get package version for Sentry release", exc_info=exc)
        return "unknown"


def _get_traces_sample_rate() -> float:
    """Resolve the trace sample rate from env, clamped to [0.0, 1.0]."""
    raw = os.getenv(TRACES_SAMPLE_RATE_ENV_VAR)
    if raw is None or not raw.strip():
        return DEFAULT_TRACES_SAMPLE_RATE

    try:
        rate = float(raw.strip())
    except ValueError:
        logger.warning(
            "Ignoring non-numeric %s=%r; falling back to %s",
            TRACES_SAMPLE_RATE_ENV_VAR,
            raw,
            DEFAULT_TRACES_SAMPLE_RATE,
        )
        return DEFAULT_TRACES_SAMPLE_RATE

    return min(max(rate, 0.0), 1.0)


def get_sentry_environment() -> str | None:
    """Return the deployment environment Sentry should report under, or `None`.

    Unset (or blank) means "not a deployed environment" — laptops, CI test
    runs — and no Sentry client is initialized at all. Deployments set this
    (`production`, `preview`) via infra / workflow env.
    """
    raw = os.getenv(SENTRY_ENVIRONMENT_ENV_VAR)
    if raw is None or not raw.strip():
        return None
    return raw.strip()


def _webapp_traces_sampler(sampling_context: dict[str, Any]) -> float:
    """Webapp-side sampler: `mcp.server` roots on the backend sample
    independently, so here we only need to drop the `/mcp` proxy route
    (browser→backend transport — listen stream, session teardown, and the
    tool-call hop itself) and otherwise honor the parent decision."""
    scope = sampling_context.get("asgi_scope")
    if (
        isinstance(scope, dict)
        and scope.get("type") == "http"
        and (scope.get("root_path", "") + scope.get("path", ""))
        .rstrip("/")
        .endswith("/mcp")
    ):
        return 0.0

    parent_sampled = sampling_context.get("parent_sampled")
    if parent_sampled is not None:
        return 1.0 if parent_sampled else 0.0

    return _get_traces_sample_rate()


def init_sentry_tracking(mode: SentryMode | None = None) -> bool:
    """Initialize Sentry error tracking if not already initialized.

    Args:
        mode: Process role. `"mcp"` disables the Starlette integration so
            `mcp.server` spans become trace roots; `"webapp"` installs a
            sampler that drops `/mcp` proxy-route transactions; `None`
            (CLI / lazy `capture_*` init) uses the flat sample rate.

    Returns:
        True if Sentry is initialized; False if `SENTRY_ENVIRONMENT` is
        unset or init failed.
    """
    global _sentry_initialized

    if _sentry_initialized:
        return True

    environment = get_sentry_environment()
    if environment is None:
        logger.debug("%s not set; Sentry disabled", SENTRY_ENVIRONMENT_ENV_VAR)
        return False

    kwargs: dict[str, Any] = {}
    if mode == "mcp":
        kwargs["disabled_integrations"] = [StarletteIntegration()]
        kwargs["traces_sample_rate"] = _get_traces_sample_rate()
    elif mode == "webapp":
        kwargs["traces_sampler"] = _webapp_traces_sampler
    else:
        kwargs["traces_sample_rate"] = _get_traces_sample_rate()

    try:
        sentry_sdk.init(
            dsn=_SENTRY_DSN,
            release=f"airbyte-ops-mcp@{_get_package_version()}",
            environment=environment,
            # Attach request data for better debugging
            send_default_pii=False,
            # Set server name to help identify the source
            server_name=os.getenv("HOSTNAME", "unknown"),
            **kwargs,
        )
        _sentry_initialized = True
        logger.debug("Sentry initialized successfully")
        return True
    except Exception as e:
        logger.warning(f"Failed to initialize Sentry: {e}")
        return False


def capture_exception(exception: BaseException) -> None:
    """Capture an exception and send it to Sentry.

    This is a convenience wrapper that ensures Sentry is initialized
    before capturing the exception.
    """
    if init_sentry_tracking():
        sentry_sdk.capture_exception(exception)


def capture_message(message: str, level: SentryLevel = "info") -> None:
    """Capture a message and send it to Sentry.

    This is useful for logging important events that aren't exceptions.
    """
    if init_sentry_tracking():
        sentry_sdk.capture_message(message, level=level)


@contextlib.contextmanager
def entrypoint_transaction(name: str, *, op: str) -> Iterator[None]:
    """Root a Sentry trace around an entrypoint no framework instruments.

    Sentry drops spans recorded with no active transaction, so DB spans from a
    CLI or cron process are lost unless something opens a root. Web processes
    get one from `StarletteIntegration`; this is the equivalent for processes
    that do not serve HTTP.

    Only use this for entrypoints whose lifetime *is* one logical operation. A
    long-lived server would produce one enormous transaction; those need
    per-request or per-tool-call roots instead.

    Does not initialize Sentry. `fastmcp_extensions.cli.cli_app` already does
    that at import with `traces_sample_rate=0.0`, so this forces the sampling
    decision for the entrypoint rather than installing a competing client.
    Yields control unchanged when nothing has initialized Sentry.

    Args:
        name: Transaction name. Keep it low-cardinality — a command path, not
            a command line with argument values in it.
        op: Sentry operation category, e.g. `"cli.command"`.
    """
    if not sentry_sdk.is_initialized():
        yield
        return

    with sentry_sdk.start_transaction(op=op, name=name, sampled=True):
        yield


@contextlib.contextmanager
def operation_span(
    name: str,
    *,
    op: str,
    attributes: dict[str, object] | None = None,
) -> Iterator[None]:
    """Record a child span, but only when Sentry is already initialized.

    Never initializes Sentry: this runs on hot paths reached from library code,
    where importing a module should not start error reporting as a side effect.
    Checks the SDK rather than this module's flag, since the CLI is initialized
    by `fastmcp_extensions` rather than by `init_sentry_tracking`.

    Args:
        name: Span name. Keep it low-cardinality.
        op: Sentry operation category, e.g. `"db.prod_replica.query"`.
        attributes: Span data. Callers are responsible for redacting values
            before they get here.
    """
    if not sentry_sdk.is_initialized():
        yield
        return

    with sentry_sdk.start_span(op=op, name=name) as span:
        for key, value in (attributes or {}).items():
            span.set_data(key, value)
        yield
