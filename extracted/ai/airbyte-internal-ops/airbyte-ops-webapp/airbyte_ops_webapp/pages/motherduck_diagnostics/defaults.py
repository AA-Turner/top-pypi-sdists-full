"""MotherDuck Diagnostics route defaults and page constants."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

MOTHERDUCK_DIAGNOSTICS_TOOL_NAME = "motherduck_diagnostics"
MOTHERDUCK_DIAGNOSTICS_PATH = "/motherduck_diagnostics"
MOTHERDUCK_DIAGNOSTICS_EMOJI = "🐤"
"""Hero emoji for the MotherDuck Diagnostics page (duckling)."""


@dataclass(frozen=True)
class SummaryOption:
    """A paired Recent-Activity-Summary lookback window and aggregation grain.

    The period and grain are intentionally coupled so a longer window always
    rolls up at a coarser grain (7d/14d aggregate by day, 24h/48h by hour). The
    `key` is the only value the browser round-trips; `period_hours` and `grain`
    are resolved server-side from a closed mapping, so arbitrary window or grain
    text is never interpolated into SQL.
    """

    key: str
    label: str
    period_hours: int
    grain: Literal["hour", "day"]
    window_label: str


# The four Recent Activity Summary period/grain options, rendered as a compact
# selection control (not a dropdown). `24h` is the default.
SUMMARY_OPTIONS: tuple[SummaryOption, ...] = (
    SummaryOption("24h", "24h · hourly", 24, "hour", "last 24 hours"),
    SummaryOption("48h", "48h · hourly", 48, "hour", "last 48 hours"),
    SummaryOption("7d", "7d · daily", 24 * 7, "day", "last 7 days"),
    SummaryOption("14d", "14d · daily", 24 * 14, "day", "last 14 days"),
)
"""The selectable Summary period/grain options, in display order."""

SUMMARY_OPTIONS_BY_KEY: dict[str, SummaryOption] = {
    option.key: option for option in SUMMARY_OPTIONS
}
"""`SUMMARY_OPTIONS` indexed by their safe `key`."""

DEFAULT_SUMMARY_OPTION = "24h"
"""Default Summary period/grain option key."""

WIDEST_SUMMARY_OPTION = "14d"
"""Widest selectable Summary window, probed at build time to decide which
`ERROR_TYPE` stack series to render. Being a superset of every selectable
period, it guarantees a series exists for any type any period could surface."""


# MotherDuck's native `QUERY_TYPE` categories rendered as fixed compute-usage
# stack series. Null/empty query types are normalized to `UNKNOWN` server-side
# (in the aggregate SQL), so only native values outside this set fold into
# `OTHER_QUERY_TYPE`, keeping the stacked chart's series set known and finite.
KNOWN_QUERY_TYPES: tuple[str, ...] = ("QUERY", "DML", "DDL", "UNKNOWN")
"""Native `QUERY_TYPE` values with a dedicated compute-usage stack series."""

OTHER_QUERY_TYPE = "OTHER"
"""Catch-all stack-series key for native query types outside `KNOWN_QUERY_TYPES`."""


# MotherDuck's native `ERROR_TYPE` classifications rendered as fixed stack series
# on the Summary "Failed queries" chart. Failures whose native `ERROR_TYPE` is
# null/empty fold under `UNKNOWN` server-side; native values outside this set
# fold into `OTHER_ERROR_TYPE`, keeping the stacked chart's series set finite.
# Confirm the live distinct `ERROR_TYPE` values against preview before promoting
# a new classification into this list.
KNOWN_ERROR_TYPES: tuple[str, ...] = (
    "OutOfMemory",
    "QueryTimeout",
    "PermissionDenied",
    "Connection",
    "UNKNOWN",
)
"""Native `ERROR_TYPE` values with a dedicated failed-queries stack series."""

OTHER_ERROR_TYPE = "OTHER"
"""Catch-all stack-series key for error types outside `KNOWN_ERROR_TYPES`."""

# Recent Queries defaults.
DEFAULT_LOOKBACK_HOURS = 8
"""Default Recent Queries lookback window, in hours."""

# Selectable lookback windows (hours) offered in the Recent Queries tab.
LOOKBACK_OPTIONS_HOURS: tuple[int, ...] = (1, 4, 8, 24, 72)

# Total-elapsed-seconds threshold at or above which a query is "slow".
SLOW_QUERY_THRESHOLD_SECONDS = 10.0

# Total-elapsed-seconds threshold at or above which a query is "very slow".
VERY_SLOW_QUERY_THRESHOLD_SECONDS = 120.0


@dataclass(frozen=True)
class QueryMode:
    """A top-level Recent Queries modality: what the server-side fetch returns.

    Unlike the in-memory `query_type` / `query_subtype` chips, changing the mode
    re-runs the query against MotherDuck, because the relevant rows (errors,
    slow queries) are rare and would otherwise be sampled out of the newest
    `_RECENT_QUERY_LIMIT` rows. `error_only` and `min_total_elapsed_seconds` map
    directly onto `MotherDuckQueryFilters`; `Slow` is inclusive of `Very slow`
    (both threshold on `TOTAL_ELAPSED_TIME`, so `Slow` \u2265 10s also matches the
    \u2265 2m `Very slow` rows).
    """

    key: str
    label: str
    error_only: bool
    min_total_elapsed_seconds: float | None


QUERY_MODE_ALL = "all"
QUERY_MODE_FAILED = "failed"
QUERY_MODE_SLOW = "slow"
QUERY_MODE_VERY_SLOW = "very_slow"

# The top-level Recent Queries modality toggle, in display order. Each option
# drives a server-side fetch (no counts on the buttons). `All queries` is the
# default.
QUERY_MODES: tuple[QueryMode, ...] = (
    QueryMode(QUERY_MODE_ALL, "All queries", False, None),
    QueryMode(QUERY_MODE_FAILED, "Failed only", True, None),
    QueryMode(
        QUERY_MODE_SLOW,
        f"Slow \u2265{SLOW_QUERY_THRESHOLD_SECONDS:.0f}s",
        False,
        SLOW_QUERY_THRESHOLD_SECONDS,
    ),
    QueryMode(
        QUERY_MODE_VERY_SLOW,
        f"Very slow \u2265{VERY_SLOW_QUERY_THRESHOLD_SECONDS / 60:.0f}m",
        False,
        VERY_SLOW_QUERY_THRESHOLD_SECONDS,
    ),
)
"""The selectable Recent Queries modality options, in display order."""

QUERY_MODES_BY_KEY: dict[str, QueryMode] = {mode.key: mode for mode in QUERY_MODES}
"""`QUERY_MODES` indexed by their safe `key`."""

DEFAULT_QUERY_MODE = QUERY_MODE_ALL
"""Default Recent Queries modality (server-side fetch of all queries)."""
