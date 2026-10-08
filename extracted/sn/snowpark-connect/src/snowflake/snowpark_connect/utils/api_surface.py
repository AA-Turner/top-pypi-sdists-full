#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
"""Request-scoped tracking of which client API surface issued the current request.

Iceberg telemetry cannot tell a SQL call from a DataFrame call by looking at the
code path it fires from: ``spark.sql("INSERT ...")`` is parsed into a logical plan
that re-enters the very same relation/write mappers a real DataFrame call uses
(``map_sql.py`` -> ``map_relation`` / the shared write helpers). A sink firing
inside those shared paths therefore records SQL and DataFrame traffic
identically.

The fix is to record the surface at the *entry point*, where it is still known,
and let the sinks read it back out. Mirrors the shape of
``utils/cld_context.py``'s CLD hint: a single ``ContextVar``, set by the handler
that owns the request, read by everything downstream without threading an
argument through every call site.

Lifecycle:
  1. Reset to ``dataframe_v1`` at every RPC entry via ``clear_context_data`` ->
     :func:`reset_request_api_surface` (``utils/context.py``). The sync gRPC
     server reuses worker threads across RPCs, so without this a value set
     during request A would still be visible at the start of request B.
  2. Set by the entry point that knows the surface:
     ``sql`` at both ``spark.sql()`` entries (``map_sql`` for the relation path,
     ``map_sql_to_pandas_df`` for the SQL-command path), and ``dataframe_v2`` on
     the ``df.writeTo(...)`` branch (``map_write_v2``). ``dataframe_v1`` is the
     default and is also set explicitly by the classic ``df.write`` path
     (``map_write``).

Both write paths set their surface *after* mapping the input relation, not
before. A writer's input can itself be a SQL relation
(``spark.sql(...).writeTo(t).append()``), which sets ``sql`` while it is mapped;
setting the writer's surface afterwards means read events emitted during input
mapping keep ``sql`` (the read really was SQL) while the write event gets the
writer API the customer actually called.

``map_sql`` is not only a request entry point: ``map_relation`` also calls it
whenever a plan has a nested SQL child (e.g. ``spark.table(...).join(spark.sql(...))``).
So that a nested SQL child's claim on the surface does not leak into sibling or
parent events mapped afterwards, ``set_api_surface`` returns a token capturing
the surface that was current before the call; ``map_sql`` restores it via
``reset_api_surface`` once it is done mapping that child, the same
save/restore-scope pattern as a ``ContextVar`` used for a lexically-scoped
override.
"""

from contextvars import ContextVar, Token

API_SURFACE_SQL = "sql"
API_SURFACE_DATAFRAME_V1 = "dataframe_v1"
API_SURFACE_DATAFRAME_V2 = "dataframe_v2"

#: The complete vocabulary. Telemetry consumers can rely on every Iceberg event
#: carrying exactly one of these values.
API_SURFACES = frozenset(
    {API_SURFACE_SQL, API_SURFACE_DATAFRAME_V1, API_SURFACE_DATAFRAME_V2}
)

# `dataframe_v1` is the default rather than an "unknown" sentinel: the classic
# DataFrame API is the surface a request is on unless a more specific entry point
# claims it, so an un-instrumented read path reports the truth instead of a hole
# the dashboards would have to special-case.
DEFAULT_API_SURFACE = API_SURFACE_DATAFRAME_V1

_current_api_surface: ContextVar[str] = ContextVar(
    "current_api_surface", default=DEFAULT_API_SURFACE
)


def set_api_surface(surface: str) -> Token:
    """Record the API surface that issued the current request.

    Returns the ``ContextVar`` token for the previous value. A caller whose
    claim on the surface should be scoped to its own call (e.g. ``map_sql``
    mapping a nested SQL child) should pass this token to
    :func:`reset_api_surface` once it is done, so the surface reverts to
    whatever the enclosing context had claimed.
    """
    if surface not in API_SURFACES:
        raise ValueError(
            f"unknown api_surface {surface!r}; expected one of {sorted(API_SURFACES)}"
        )
    return _current_api_surface.set(surface)


def reset_api_surface(token: Token) -> None:
    """Restore the API surface to what it was before the matching call to
    ``set_api_surface``."""
    _current_api_surface.reset(token)


def get_api_surface() -> str:
    """Return the API surface for the current request."""
    return _current_api_surface.get()


def reset_request_api_surface() -> None:
    """Reset the API surface to the default at the start of an RPC."""
    _current_api_surface.set(DEFAULT_API_SURFACE)
