import os
import re

import structlog
from langgraph.version import __version__

logger = structlog.stdlib.get_logger(__name__)

# Only gate features on the major.minor version; Lets you ignore the rc/alpha/etc. releases anyway
LANGGRAPH_PY_MINOR = tuple(map(int, __version__.split(".")[:2]))

OMIT_PENDING_SENDS = LANGGRAPH_PY_MINOR >= (0, 5)
USE_RUNTIME_CONTEXT_API = LANGGRAPH_PY_MINOR >= (0, 6)
USE_NEW_INTERRUPTS = LANGGRAPH_PY_MINOR >= (0, 6)
USE_DURABILITY = LANGGRAPH_PY_MINOR >= (0, 6)


# Runtime edition detection
# Not in public docs: LANGGRAPH_RUNTIME_EDITION is internal, set by packaging/entrypoint
_RUNTIME_EDITION = os.getenv("LANGGRAPH_RUNTIME_EDITION", "inmem")
IS_POSTGRES_BACKEND = _RUNTIME_EDITION == "postgres"
IS_POSTGRES_OR_GRPC_BACKEND = IS_POSTGRES_BACKEND
# Server-side kill switch for the Protocol v2 event-streaming surface
# (#3296). When false, the v2 routes are not registered (clients hit a
# 404), and ``_create_or_resume_run`` rejects any direct call with a
# clear ``unsupported`` envelope so a misbehaving v2 hot path can be
# disabled without a redeploy. Defaults on — v2 is the protocol the SDK
# targets — operators flip to false to roll back.
FF_V2_EVENT_STREAMING = os.getenv("FF_V2_EVENT_STREAMING", "true").lower() in (
    "true",
    "1",
    "yes",
)


def _resolve_prefer_grpc_checkpointer(
    env_value: str | None, *, langgraph_supported: bool, is_postgres: bool
) -> bool:
    enabled = ("true" if env_value is None else env_value).lower() in (
        "true",
        "1",
        "yes",
    )
    if langgraph_supported:
        return enabled
    if is_postgres:
        ignored = (
            "Ignoring PREFER_GRPC_CHECKPOINTER=true. " if env_value and enabled else ""
        )
        logger.warning(
            f"{ignored}Using the Python checkpointer because the Go checkpointer "
            "requires langgraph>=0.5. Please upgrade langgraph: support for "
            "langgraph<0.5 will be removed in a future release.",
            langgraph_version=__version__,
        )
    return False


# When true on the postgres runtime, use ``GrpcCheckpointer``.
# Inmem edition is unaffected (``IS_POSTGRES_BACKEND`` is false there).
# Custom checkpointer (``backend=custom`` in ``LANGGRAPH_CHECKPOINTER``) and
# Mongo (``backend=mongo``) is also unaffected.
# langgraph < 0.5 keeps Send() packets in checkpoint["pending_sends"], which only
# the Python checkpointer rebuilds on load; the Go checkpointer drops them. Keep
# < 0.5 on the Python checkpointer. Before removing it, raise the minimum
# langgraph to >= 0.5.
PREFER_GRPC_CHECKPOINTER = _resolve_prefer_grpc_checkpointer(
    os.getenv("PREFER_GRPC_CHECKPOINTER"),
    langgraph_supported=OMIT_PENDING_SENDS,
    is_postgres=IS_POSTGRES_BACKEND,
)

# In langgraph <= 1.0.3, we automatically subscribed to updates stream events to surface interrupts. In langgraph 1.0.4 we include interrupts in values events (which we are automatically subscribed to), so we no longer need to implicitly subscribe to updates stream events
# Strip prerelease suffixes (e.g. "0a5" -> 0) so versions like 1.2.0a5 still
# parse correctly; fall back to (0, 0, 0) only if no leading digits at all.
_LEADING_DIGITS = re.compile(r"^\d+")
try:
    LANGGRAPH_PY_PATCH = tuple(
        int(_LEADING_DIGITS.match(p).group()) for p in __version__.split(".")[:3]
    )
except (AttributeError, ValueError):
    LANGGRAPH_PY_PATCH = (0, 0, 0)
UPDATES_NEEDED_FOR_INTERRUPTS = LANGGRAPH_PY_PATCH <= (1, 0, 3)

# DeltaChannel checkpointer fast-path (two-stage SQL) requires langgraph >= 1.2.
DELTA_CHANNEL_SUPPORT = LANGGRAPH_PY_MINOR >= (1, 2)

# Resuming drained runs requires langgraph >= 1.2.15, which checks a step's
# interrupt_before breakpoints before a drain request
# (langchain-ai/langgraph#9281). Earlier versions drain in front of a
# breakpoint, and the resume then runs past it.
DRAIN_RESUME_SUPPORT = LANGGRAPH_PY_PATCH >= (1, 2, 15)
