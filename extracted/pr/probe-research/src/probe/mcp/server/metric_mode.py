"""each `metrics` mode's arguments, required set and route (_METRIC_ROUTES), and the arguments checked against them."""

from __future__ import annotations
from collections.abc import Callable
from typing import Any
from mcp.server.fastmcp.exceptions import ToolError
from ...shared.reads.search_contract import MetricMode
from ..tools.tools import ResearchReadService
from probe.mcp.server.metric_modes.coordinates import _metric_route_coordinates
from probe.mcp.server.metric_modes.grouped import _metric_route_grouped
from probe.mcp.server.metric_modes.points import _metric_route_points
from probe.mcp.server.metric_modes.series import _metric_route_series


# -- read_metrics: one concept, three grains ---------------------------------
#
# `get_metrics_grouped`, `get_run_coordinates` and `export_metric_points` were
# one question about GRAIN asked three ways, so the question is now the tool and
# the grain is an argument.
#
# THE HAZARD THIS BLOCK EXISTS TO STOP. A merged tool declares the UNION of its
# branches: `read_metrics` offers `by`, `agg`, `where`, `step_bucket`, `after_id`,
# `limit` and `max_rows` together though no single grain reads more than seven of
# them. Validating a call against that union is not validation -- it is a check
# that the argument exists SOMEWHERE in the tool. An argument meant for another
# mode then passes, reaches the service, and is dropped without a word (FastAPI
# ignores an undeclared query parameter; pydantic's default `extra="ignore"`
# drops an undeclared body field), and the call returns a 200 that answered a
# question nobody asked. The backend's own collapse shipped seven of these and
# not one raised: `mode=points, by=["rank"]` came back as ungrouped raw points,
# confidently, with no error.
#
# So the union is only half the schema and these tables are the other half.
# Three rules, each earned:
#
#   REFUSE, NEVER DROP. An argument this mode does not read is an error, because
#   the alternative is a wrong answer wearing the shape of a right one.
#
#   CHECK BEFORE TRANSLATION. The names below are the CALLER'S, and nothing has
#   been rewritten when they are checked, so the refusal quotes what the agent
#   wrote instead of what this layer rewrote it into.
#
#   DERIVE FROM WHAT THE MODE RETURNS, NOT FROM WHAT ITS ROUTE TOLERATES. Those
#   differ, and the difference is exactly where the silent bug lives.
#   `coordinates` is the sharp case: `GET /v1/runs/{ref}/coordinates` takes no
#   query parameters at all, so `key` and a step window are not "ignored
#   filters" -- they are a request to narrow an enumeration that cannot be
#   narrowed, and every one of them would have come back as the whole catalog.
_METRIC_MODE_ARGS: dict[MetricMode, frozenset[str]] = {
    MetricMode.GROUPED: frozenset(
        {
            "run_id",
            "key",
            "kind",
            "agg",
            "by",
            "where",
            "step_bucket",
            "step_from",
            "step_to",
            "max_rows",
        }
    ),
    MetricMode.COORDINATES: frozenset({"run_id"}),
    MetricMode.POINTS: frozenset(
        {"run_id", "key", "kind", "step_from", "step_to", "after_id", "limit"}
    ),
    # PLURAL where the other three are singular, because it is the one grain
    # that is not one run: `run_ids` + `keys`, never `run_id` + `key`. No `kind`
    # either -- the series route has no top-level kind filter and would DROP it
    # (its body model ignores unknown fields); each row says its kind instead.
    MetricMode.SERIES: frozenset(
        {"run_ids", "keys", "step_from", "step_to", "smoothing", "max_points"}
    ),
}

#: What each mode cannot run without. `key` is the one that varies, and it varies
#: in all three directions: REQUIRED by `grouped` (a reduction needs something to
#: reduce), OPTIONAL for `points` (omitted exports every key), and REFUSED by
#: `coordinates`. Passing `key=None` into the grouped reduction would have sent
#: `key=None` to the route rather than failing here.
_METRIC_MODE_REQUIRED: dict[MetricMode, frozenset[str]] = {
    MetricMode.GROUPED: frozenset({"run_id", "key"}),
    MetricMode.COORDINATES: frozenset({"run_id"}),
    MetricMode.POINTS: frozenset({"run_id"}),
    MetricMode.SERIES: frozenset({"run_ids", "keys"}),
}

#: Arguments whose TYPE a naive arity check cannot police. A `str` is a
#: `Sequence`, so `by="rank"` satisfies "is it iterable?" and then splits into
#: one axis per CHARACTER -- the backend collapse shipped exactly this as
#: `keys="loss"` reaching the route as `"l"`.
#:
#: ON EVERY MCP PATH THE ANNOTATION IS WHAT STOPS THIS, aliases included: they
#: are `@mcp.tool()`-decorated with the same `list[str]` / `dict` types, so
#: pydantic rejects a bare string before any body runs. These checks are NOT
#: load-bearing there and the comment here used to claim otherwise. They are
#: kept to make `_metric_args_for_mode` TOTAL -- it is a module-level validator
#: and a caller reaching it directly (its own unit tests today, any in-process
#: caller later) gets the same refusal as the wire does, rather than a str
#: silently reaching the route. Tested directly for that reason; a test that
#: drove it through the tool would be scoring pydantic, not this.
_METRIC_SEQUENCE_ARGS = frozenset({"by", "run_ids", "keys"})
_METRIC_MAPPING_ARGS = frozenset({"where"})

#: The series route's own list bounds (`MAX_RUN_IDS_PER_QUERY`,
#: `MAX_SERIES_PER_QUERY`), checked here so the refusal names the argument the
#: caller wrote instead of relaying a body 422.
_METRIC_SEQUENCE_MAX = {"run_ids": 50, "keys": 200}


#: Mode -> the read it actually performs. These are REAL service methods, not a
#: synthesised `read(mode)` seam, so swapping two entries changes which data
#: comes back and a behavioural test has to notice -- verified by mutation, not
#: assumed. Tests that only assert the modes EXIST would pass a swapped table.
_METRIC_ROUTES: dict[MetricMode, Callable[[ResearchReadService, dict[str, Any]], dict]] = {
    MetricMode.GROUPED: _metric_route_grouped,
    MetricMode.COORDINATES: _metric_route_coordinates,
    MetricMode.POINTS: _metric_route_points,
    MetricMode.SERIES: _metric_route_series,
}


def _metric_args_for_mode(mode: MetricMode, args: dict[str, Any]) -> dict[str, Any]:
    """Validate one `read_metrics` call against THE MODE IT CHOSE, and return the
    arguments that were actually supplied.

    Raises ``ToolError`` -- an argument the mode does not read is refused, never
    dropped. Absent-vs-null is not a distinction the wire preserves (every
    optional parameter defaults to ``None``), so "supplied" means "not None";
    that is why `where={}` and `max_rows=0` still count as supplied.
    """
    # A mode with no table entry would otherwise be a KeyError deep in dispatch,
    # which surfaces as an opaque 500 rather than "you named a mode that does not
    # exist". test_read_metrics_tables_cover_every_mode makes it unreachable; this
    # keeps it honest if someone adds a member and not a row.
    if (
        mode not in _METRIC_ROUTES
        or mode not in _METRIC_MODE_ARGS
        or mode not in _METRIC_MODE_REQUIRED
    ):
        complete = sorted(
            m.value for m in _METRIC_ROUTES if m in _METRIC_MODE_ARGS and m in _METRIC_MODE_REQUIRED
        )
        raise ToolError(
            f"read_metrics: mode={mode.value!r} is not fully registered — it is "
            f"missing a row in one of the three mode tables. Usable modes: "
            f"{', '.join(complete)}"
        )

    allowed = _METRIC_MODE_ARGS[mode]
    supplied = {name: value for name, value in args.items() if value is not None}

    unsupported = sorted(set(supplied) - allowed)
    if unsupported:
        # Names the mode that DID want each argument, because the usual cause is
        # a right question asked at the wrong grain and the fix is the other mode.
        elsewhere = {
            name: sorted(
                m.value for m, ok in _METRIC_MODE_ARGS.items() if name in ok and m is not mode
            )
            for name in unsupported
        }
        detail = "; ".join(
            f"{name} (read by mode={' or '.join(modes)})" if modes else f"{name} (read by no mode)"
            for name, modes in elsewhere.items()
        )
        raise ToolError(
            f"read_metrics: mode={mode.value} does not read {', '.join(unsupported)} — "
            f"{detail}. It reads {', '.join(sorted(allowed))}. "
            "Re-issue the call in the mode that answers your question; passing it here "
            "would return a result that ignored the argument."
        )

    missing = sorted(_METRIC_MODE_REQUIRED[mode] - set(supplied))
    if missing:
        raise ToolError(f"read_metrics: mode={mode.value} requires {', '.join(missing)}")

    for name in sorted(_METRIC_SEQUENCE_ARGS & set(supplied)):
        value = supplied[name]
        if isinstance(value, str) or not isinstance(value, (list, tuple)):
            noun = "coordinate axes" if name == "by" else "strings"
            raise ToolError(
                f"read_metrics: {name} must be a list of {noun}, not "
                f"{type(value).__name__} — {name}=[{value!r}] for a single one. "
                "A bare string is a sequence of CHARACTERS and would be read as "
                "one entry per letter."
            )
        if not all(isinstance(item, str) for item in value):
            raise ToolError(f"read_metrics: every entry in {name} must be a string")
        bound = _METRIC_SEQUENCE_MAX.get(name)
        if bound is not None and not 1 <= len(value) <= bound:
            raise ToolError(
                f"read_metrics: {name} takes 1 to {bound} entries, got {len(value)} -- "
                "split a larger comparison into several reads"
            )

    for name in sorted(_METRIC_MAPPING_ARGS & set(supplied)):
        if not isinstance(supplied[name], dict):
            raise ToolError(
                f"read_metrics: {name} must be an object mapping a coordinate axis "
                f"to the value to match, not {type(supplied[name]).__name__}"
            )

    return supplied
