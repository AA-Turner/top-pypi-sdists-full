"""Datadog collector: sustained per-node CPU utilisation per EKS node group.

Used by the optimizer to decide whether a CPU-throttled type (burstable ``t*`` /
``*-flex``) can carry a node group's real load: if the sustained per-node usage
stays under the candidate's baseline fraction, the throttle never triggers, so
the cheaper type fits.

We read host-level system metrics (one series per node) rather than
``kubernetes.cpu.usage.total``: the latter is emitted at several cardinalities
(container/pod/node), so ``avg by host`` averages the series (huge under-count)
and ``sum by host`` double-counts (can exceed the node's physical vCPU). The
system metrics are unambiguous.

Real workload demand = ``(100 − idle − stolen) / 100``: ``stolen`` (CPU the
hypervisor took away) is **not** workload usage — on a node already throttling
(burstable/flex out of credits) it shows up as steal, and counting it would
inflate the demand and wrongly reject the very throttled types we are sizing
for. We take the **p95 across hosts and time** as the sustained level (a
fraction 0–1, comparable directly to ``baseline_ratio`` since the compared
types share the node's shape).
"""

import re
from dataclasses import dataclass

import httpx

from ..env.resolve import try_auto_resolve
from .timerange import parse_date

DD_SITE = "datadoghq.eu"
# Trailing Terraform-generated id on a managed node group name (e.g. ``dev-bo-2026…``).
# We match Datadog on the stable prefix + wildcard so a recreated node group (new
# suffix) still resolves to its historical metrics within the window.
_NG_SUFFIX_RE = re.compile(r"-\d+$")


@dataclass
class CpuUtil:
    """Sustained per-node CPU utilisation over the window, as fractions 0–1.

    ``p95`` drives the throttled-type head-room decision (sustained level); ``p99``
    is informational only — it shows peak amplitude but does not gate anything,
    since short peaks are exactly what a burstable/flex type's burst absorbs.
    """

    p95: float
    p99: float


def _client() -> httpx.Client | None:
    """Datadog v1 client, or ``None`` when keys are not resolvable (best-effort)."""
    api_key = try_auto_resolve("DD_API_KEY")
    app_key = try_auto_resolve("DD_APP_KEY")
    if not api_key or not app_key:
        return None
    return httpx.Client(
        base_url=f"https://api.{DD_SITE}/api/v1",
        headers={"DD-API-KEY": api_key, "DD-APPLICATION-KEY": app_key},
        timeout=30,
    )


def _percentile(values: list[float], pct: float) -> float:
    """Linear-interpolation percentile of ``values`` (``pct`` in 0–100)."""
    ordered = sorted(values)
    if not ordered:
        return 0.0
    if len(ordered) == 1:
        return ordered[0]
    rank = (pct / 100.0) * (len(ordered) - 1)
    low = int(rank)
    high = min(low + 1, len(ordered) - 1)
    return ordered[low] + (ordered[high] - ordered[low]) * (rank - low)


def _query_points(dd: httpx.Client, query: str, from_ts: int, to_ts: int) -> list[float]:
    resp = dd.get("/query", params={"query": query, "from": from_ts, "to": to_ts})
    resp.raise_for_status()
    series = resp.json().get("series") or []
    return [pt[1] for serie in series for pt in (serie.get("pointlist") or []) if pt[1] is not None]


def nodegroup_cpu_util(ng_names: list[str], start_iso: str, end_iso: str) -> dict[str, CpuUtil]:
    """Map each node group name to its sustained per-node CPU utilisation (p95 + p99).

    Best-effort: returns ``{}`` when Datadog keys are missing, and silently skips a
    node group whose query fails or has no data. The caller treats a missing entry
    as "no signal" and falls back to the static baseline penalty.
    """
    dd = _client()
    if dd is None:
        return {}
    from_ts = int(parse_date(start_iso).timestamp())
    to_ts = int(parse_date(end_iso).timestamp())
    out: dict[str, CpuUtil] = {}
    with dd:
        for name in ng_names:
            prefix = _NG_SUFFIX_RE.sub("", name)
            scope = f"{{eks_nodegroup-name:{prefix}-*}} by {{host}}"
            query = f"100 - avg:system.cpu.idle{scope} - avg:system.cpu.stolen{scope}"
            try:
                usage_pct = _query_points(dd, query, from_ts, to_ts)  # already (100 - idle - stolen)
            except httpx.HTTPError:
                continue
            if usage_pct:
                util = [min(1.0, max(0.0, p / 100.0)) for p in usage_pct]
                out[name] = CpuUtil(p95=_percentile(util, 95), p99=_percentile(util, 99))
    return out
