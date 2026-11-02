"""Cube-wide resource utilization — the pure half of the console's Resources tab.

The panel catalog, the window ladder, and the normalization of a Groundcover range
response into plottable points. **Nothing here dials an upstream, touches Apollo, or
authorizes anything** — that is `reads.cube_utilization`'s job, alongside the other two
Groundcover-backed console reads. A sibling of `console/cache.py` and `console/csrf.py`
rather than a second reads module; the moment this file takes an `ApolloClient` or a
registry it belongs in `reads.py` instead.

**Why the module is not called `telemetry`.** In this repo "telemetry" is the tool-call
analytics pipeline (`cube_cloud/telemetry/`), and `main.py` does `from cube_cloud import
telemetry` at module scope, then calls `telemetry.record_tool_call(...)` inside the tool
wrapper's `finally`. A `from cube_cloud.console import telemetry` beside the existing
`from cube_cloud.console import routes` would shadow it and raise an `AttributeError`
*from a finally block*, replacing the result of every MCP tool call. The tab is "Resources".

**Every metric Groundcover exposes is per-host, per-node or per-PVC — there is no
cube-wide series to read.** Cube-wide numbers are produced by server-side aggregation,
and the aggregation available is whatever `groundcover._build_promql` can already emit:
`agg(metric{cluster="<cube>"})`. That builder is the cross-tenant guard, so it is reused
verbatim and never extended. Two consequences are load-bearing:

1. **`avg` of a per-host percentage is a TREND, not a label.** It equals the true
   capacity-weighted figure only when hosts are identically sized, and a cube may carry a
   GPU node with different RAM and core counts. So the series is named "Average across N
   hosts" and never "Cube CPU utilization" — presenting an unweighted mean as *the* cube
   figure is the overclaiming-label bug this repo has already fixed twice (the Lifecycle
   rename, the mandatory "Agent" chip label).
2. **`count` is not decoration.** `avg` silently drops entities that stop reporting, so a
   host dying makes the average *improve*. The entity count is the only thing on screen
   that can contradict that reading, which is what makes the average falsifiable. Its
   corollary is that a metric whose label set multiplies a host into several series makes
   the falsifier itself lie — which is why the disk panel does not read the obvious
   `_fs_` metric; see its entry in `PANELS`.

`VOLUMES` inverts the pair on purpose — see its entry in `PANELS`.

**Verified live against the prod Groundcover backend, 2026-09-11** (`cube-66odzn95`,
`cube-9likqvpd`, `esai-prism-1`, `palantir-sovereign-ai`), which is what the PR that
added this file left open. The envelope is `{"resultType": "matrix", "result": [{"metric":
{...}, "values": [[<seconds>, "<value>"]]}]}` — so timestamps arrive in SECONDS and values
as QUOTED STRINGS, exactly the pair `_sample` is built for; an aggregated query collapses
to exactly one series with an empty `metric` map, so the `len(body) > 1` refusal never
fires on a query this module issues. Values are **0-100** (`max(pvc_usage_percent)` on
`cube-66odzn95` read 45.99, `avg(host_mem_used_percent)` on `cube-9likqvpd` read 24.59),
so `unit: "percent"` is now a checked fact rather than an inference from the name.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

# Outcomes of reading one Groundcover range response. THREE, not two: an empty series
# produced by a parse failure is byte-identical to one produced by `result: []`, and
# collapsing them makes a panel assert a fact about the cube ("does not report CPU") at
# exactly the moment we could not read one. That is the Hardware-tab bug — which rendered
# "no hardware specification is recorded" fleet-wide while the credential was simply
# unset — in a new place. `UNREADABLE` maps to "unavailable", `EMPTY` to "no_data".
OK = "ok"
EMPTY = "empty"
UNREADABLE = "unreadable"

# A single plotted point: epoch milliseconds, and a value that may be None.
# None means "no sample" and the chart BREAKS THE LINE there. It is never zero — a
# flat zero line is a claim about the cube, and it is the claim most likely to be read
# as healthy for CPU and as catastrophic for disk.
Point = tuple[int, float | None]


@dataclass(frozen=True)
class Panel:
    """One graph. `metric` is queried three times: avg, max and count."""

    key: str
    label: str
    metric: str
    #: Which of the two series is the headline (primary colour, and the source of
    #: `latest` / `highest_sampled`).
    headline_role: str
    #: Plural / singular nouns for the entities the aggregation spans.
    noun: str
    noun_one: str
    #: Series names. `{n}` is filled with the entity count when it is known.
    avg_name: str
    max_name: str
    #: A v1 limitation stated in the panel rather than left for the reader to discover.
    note: str = ""


PANELS: tuple[Panel, ...] = (
    # CPU and memory read the HOST layer, not the node layer. It is the physical
    # machine's truth (it includes everything running, not only what kubelet accounts
    # for), and it sidesteps the `_rt_`-vs-rolled-up twin that every `groundcover_node_*`
    # metric carries — picking one of those twins would be an arbitrary choice this file
    # would then have to keep consistent forever.
    Panel(
        key="cpu",
        label="CPU",
        metric="groundcover_host_cpu_usage_percent",
        headline_role="avg",
        noun="hosts",
        noun_one="host",
        avg_name="Average across {n} hosts",
        max_name="Busiest host",
    ),
    Panel(
        key="memory",
        label="Memory",
        metric="groundcover_host_mem_used_percent",
        headline_role="avg",
        noun="hosts",
        noun_one="host",
        avg_name="Average across {n} hosts",
        max_name="Busiest host",
    ),
    # `groundcover_host_disk_space_used_percent`, NOT `groundcover_host_fs_used_percent`,
    # and the difference is a wrong NUMBER on screen rather than a preference. Verified
    # live 2026-09-11: the `_fs_` metric carries `mountpoint`, `device_name` and
    # `file_system` labels, and on `esai-prism-1` the collector emits every host TWICE
    # under them — once as `mountpoint="/boot"` (ext4, nvme0n1p3) and once as
    # `mountpoint="/etc"` (xfs, nvme0n1p4) — with byte-identical values. `count()` there
    # returns 12 against 6 real hosts (CPU and memory both count 6), so this panel would
    # have rendered "Average across 12 hosts" on a six-host cube. That breaks the one
    # thing `count` exists to do: it is the falsifier for the average, so a doubled count
    # makes the check itself lie, and it names the wrong noun as well as the wrong number.
    #
    # `_disk_space_` sits below the mount layer and carries NO mountpoint/device labels,
    # so it is one series per host by construction. On every cube checked the two agree
    # to twelve decimal places (`cube-9likqvpd`: 18.569129869763 from both), so this
    # changes no plotted value today — it removes a hazard that is already live on one
    # cube and would return on any cube whose collector enumerates a third mount.
    Panel(
        key="filesystem",
        label="Host disk",
        metric="groundcover_host_disk_space_used_percent",
        headline_role="avg",
        noun="hosts",
        noun_one="host",
        avg_name="Average across {n} hosts",
        max_name="Fullest host",
        # Stated because neither this panel nor Volume fill can see it: on a TopoLVM
        # cube, a volume that is 10% full still consumes 100% of the logical volume
        # carved for it, so the volume group can be out of room while both graphs
        # look calm.
        note=(
            "Volume-group headroom is not shown here: space allocated to a volume is "
            "consumed whether or not the volume is full."
        ),
    ),
    Panel(
        key="volumes",
        label="Volume fill",
        metric="groundcover_pvc_usage_percent",
        # THE HEADLINE IS `max`, AND THIS INVERSION IS THE POINT. Averaging fill across
        # volumes of wildly different sizes is diluted by construction: one volume at 99%
        # among thirty moves the mean about two points, so an averaged panel renders calm
        # while an app is minutes from crashlooping on a full PV. On a TopoLVM-only cube
        # — local disk, no elasticity — that is the failure mode, and the likeliest
        # reason anyone opens this tab at all.
        headline_role="max",
        noun="volumes",
        noun_one="volume",
        avg_name="Average across {n} volumes",
        max_name="Fullest volume",
        # Naming the fullest volume needs a `by (persistentvolumeclaim)` clause, which
        # `_build_promql` cannot emit and which is not worth widening the cross-tenant
        # guard for. Say so rather than leaving the reader to wonder.
        note="Which volume is fullest is not shown in this view.",
    ),
)

#: `?window=` → (minutes, Groundcover `Step` string, step seconds).
#:
#: All steps are MINUTE granularity, so nothing depends on whether the endpoint accepts
#: sub-minute `Step` strings — unverified, and not worth a runtime surprise.
#:
#: The step is capped at two minutes rather than scaled to a fixed point count. `avg`
#: and `max` are INSTANT aggregations sampled *at* each step timestamp (`_RANGE_AGGS`
#: holds no `*_over_time`, and `_build_promql` cannot nest one inside a collapse), so a
#: spike between samples is invisible. A step that grew with the window would make the
#: 24h chart of a given hour look calmer than the 1h chart of that same hour, which reads
#: as a data bug. Hence also `highest_sampled` rather than "peak".
WINDOWS: dict[str, tuple[int, str, int]] = {
    "1h": (60, "1m", 60),
    "6h": (360, "1m", 60),
    "24h": (1440, "2m", 120),
}

DEFAULT_WINDOW = "1h"


def resolve_window(raw: str) -> tuple[str, int, str, int] | None:
    """`?window=` → (name, minutes, step string, step seconds); None if unrecognized.

    An enumerated allowlist, never a pass-through: the console is an enumerated-args
    surface, and the point cap this yields is also what stops a caller asking for a
    million-point series.
    """
    name = (raw or DEFAULT_WINDOW).strip().lower()
    spec = WINDOWS.get(name)
    if spec is None:
        return None
    return (name, *spec)


def series_name(panel: Panel, role: str, count: int | None) -> str:
    """The label under which a series is presented, with the entity count folded in."""
    if role == "max":
        return panel.max_name
    if count is None:
        # Count unavailable: drop the number rather than print a placeholder. "Average
        # across hosts" is vaguer but stays true.
        return panel.avg_name.replace("{n} ", "")
    noun = panel.noun_one if count == 1 else panel.noun
    return panel.avg_name.replace("{n}", str(count)).replace(panel.noun, noun)


# ---------------------------------------------------------------------------
# Normalizing a Groundcover range response
# ---------------------------------------------------------------------------
#
# The response shape is UNVERIFIED. This repo's own MCP formatter hedges the envelope as
# `resp.get('data', resp)` and the only test fixture that ever existed is an empty
# `{"data": {"result": []}}` — nobody knew. So every rule below is a tolerance, and
# anything not understood is UNREADABLE rather than silently empty.


def _epoch_ms(raw: float) -> int | None:
    """A Prometheus-style timestamp → epoch milliseconds, or None if it is not a time.

    Units are bucketed by magnitude EXPLICITLY. A single `> 1e11` seconds-vs-milliseconds
    test — the obvious implementation — sends microseconds and nanoseconds to roughly the
    year 55000, which renders a chart that is empty with no error raised anywhere and no
    way to tell from the payload that anything went wrong.
    """
    magnitude = abs(raw)
    if magnitude < 1e5:  # 1970 to ~1973: not a real sample time, in any unit
        return None
    if magnitude < 1e11:
        return int(raw * 1_000)  # seconds
    if magnitude < 1e14:
        return int(raw)  # milliseconds
    if magnitude < 1e17:
        return int(raw / 1e3)  # microseconds
    if magnitude < 1e20:
        return int(raw / 1e6)  # nanoseconds
    return None


def _sample(item: object) -> tuple[int, float | None] | None:
    """One sample → a point, or None if the shape is not understood.

    Accepts the Prometheus `[timestamp, "value"]` pair and a `{t, v}`-style mapping,
    because which one this endpoint emits has never been checked.
    """
    stamp: object
    value: object
    if isinstance(item, (list, tuple)):
        if len(item) != 2:
            return None
        stamp, value = item[0], item[1]
    elif isinstance(item, dict):
        stamp = item.get("t", item.get("timestamp", item.get("Timestamp")))
        value = item.get("v", item.get("value", item.get("Value")))
        if stamp is None:
            return None
    else:
        return None

    try:
        # The VALUE arrives as a quoted string and the TIMESTAMP as a float. Gating on
        # `isinstance(v, (int, float))` would drop every point, and — because an empty
        # series is indistinguishable from a missing metric without the outcome flag
        # above — the panel would then claim the cube does not report this metric.
        at = float(stamp)  # type: ignore[arg-type]
        reading = float(str(value))
    except (TypeError, ValueError):
        return None

    ms = _epoch_ms(at)
    if ms is None:
        return None

    # NaN / +Inf / -Inf are legal in Prometheus-shaped JSON — a `_percent` computed 0/0
    # on a host with no matching filesystem is a realistic producer. They must not reach
    # `json.dumps`, which emits a bare `NaN` token: that is invalid JSON, so `JSON.parse`
    # in the browser throws and ALL FOUR panels fail together. Data-dependent, so it
    # passes every test and breaks on exactly one customer's cube.
    if not math.isfinite(reading):
        return (ms, None)
    return (ms, reading)


def read_series(resp: object) -> tuple[str, list[Point]]:
    """A Groundcover metrics response → (outcome, points).

    `OK` with points, `EMPTY` when the envelope was understood and held no series, and
    `UNREADABLE` for anything else. The caller must map `UNREADABLE` to "we could not
    look" and `EMPTY` to "this cube does not report it", never the reverse.
    """
    body: object = resp
    if isinstance(body, dict):
        body = body.get("data", body)

    if isinstance(body, dict):
        # A vector answer carries `value` (one pair) rather than `values`. Classify it
        # rather than reaching into a shape this function does not model.
        kind = body.get("resultType") or body.get("ResultType")
        if isinstance(kind, str) and kind.lower() != "matrix":
            return (UNREADABLE, [])
        if "result" in body or "Result" in body:
            body = body.get("result", body.get("Result"))
        else:
            return (UNREADABLE, [])

    if body is None:
        # The key was present and understood; there is simply nothing in it.
        return (EMPTY, [])
    if not isinstance(body, list):
        return (UNREADABLE, [])
    if not body:
        return (EMPTY, [])
    if len(body) > 1:
        # A bare `avg()`/`max()` collapses to exactly one series, so more than one means
        # the query was not the one this code thinks it issued. NEVER take `body[0]`:
        # presenting one arbitrary host as the cube's average, with nothing on screen to
        # contradict it, is the `agents[0]` mistake — it would also flip as the upstream's
        # ordering changed.
        return (UNREADABLE, [])

    entry = body[0]
    if not isinstance(entry, dict):
        return (UNREADABLE, [])
    raw = entry.get("values", entry.get("Values"))
    if raw is None:
        if "value" in entry or "Value" in entry:
            return (UNREADABLE, [])  # vector shape after all
        return (EMPTY, [])
    if not isinstance(raw, list):
        return (UNREADABLE, [])

    points: list[Point] = []
    for item in raw:
        point = _sample(item)
        if point is None:
            # One unparseable sample means the shape assumption is wrong for the whole
            # series — Prometheus does not emit a partially-malformed array. Failing the
            # series is honest; dropping the sample would quietly thin the graph.
            return (UNREADABLE, [])
        points.append(point)

    if not points:
        return (EMPTY, [])

    # Order is not guaranteed, and a duplicated timestamp would draw a line doubling
    # back on itself. Last write wins.
    merged: dict[int, float | None] = {}
    for at, reading in points:
        merged[at] = reading
    return (OK, sorted(merged.items()))


def read_count(resp: object) -> int | None:
    """`count(...)` → the entity count, or None when it could not be read.

    The LAST finite sample, because entities come and go and the current number is the
    one the series names are describing. A failure here is not a panel failure: the count
    is context for the average, not the data itself.
    """
    outcome, points = read_series(resp)
    if outcome != OK:
        return None
    for _at, reading in reversed(points):
        if reading is not None:
            return int(reading)
    return None


def has_readings(points: list[Point]) -> bool:
    """Does this series carry a single PLOTTABLE number?

    `OK` means the envelope was understood and samples came back; it does not mean any
    of them is a value. `_sample` maps a non-finite reading to `(ms, None)` — a point, so
    it counts toward `OK` — which leaves a real gap between "parsed" and "readable" that
    nothing else in the three-way outcome covers.

    Without this the failure is silent and specifically confusing: a headline series that
    is entirely non-finite yields `state: "ok"` with `latest`/`highest_sampled` both
    `None`, so the panel keeps its title and its entity count, the legend still promises
    "Average across 6 hosts", the figures read "—", the primary line is simply absent, and
    **no sentence anywhere says why**. That is the unexplained blank the three-way outcome
    exists to prevent, arrived at from the one direction it did not guard.

    Deliberately a separate predicate rather than a fourth `read_series` outcome: the
    mixed case is the common one — one series unreadable while the other is fine — and
    collapsing the panel there would discard real data (a working "Busiest host" line)
    to describe the series beside it.

    No evidence the current upstream produces this: probed live 2026-09-11 against the
    plausible `0/0` producers (`groundcover_host_mem_swap_free_percent` on a swapless
    node, `groundcover_container_cpu_request_usage_percent` where a container sets no
    request) and Groundcover's collector guards its own divisions, emitting `0`. That is
    a fact about today's collector, not a property of the wire format, and `_sample`
    already treats non-finite readings as expected enough to map — so handling them here
    and then leaving this case unexplained was an inconsistency in that decision.
    """
    return any(reading is not None for _at, reading in points)


def latest_and_peak(points: list[Point]) -> tuple[float | None, float | None]:
    """(most recent reading, highest sampled reading), ignoring gaps.

    "Highest sampled" rather than "peak" is deliberate — see `WINDOWS`. These are
    computed server-side for the same reason `cube_status.age_seconds` is: the browser
    re-deriving them would let a client-side rounding or clock difference put a different
    number beside the same graph.
    """
    readings = [r for _at, r in points if r is not None]
    if not readings:
        return (None, None)
    return (readings[-1], max(readings))
