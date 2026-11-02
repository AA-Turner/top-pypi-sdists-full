"""Groundcover observability tools (read-only), scoped per cube.

Authorization model — read this before touching the query builders.

A Groundcover API key is workspace/tenant-scoped, and our whole cube fleet lives
in one Groundcover workspace (each cube is a `cluster`). So the key can see ALL
cubes — it gives us no per-cube isolation. *We* enforce tenancy at the edge.

The authority is Apollo (see ``auth/apollo_rbac.allowed_cubes``): every cube is an
Apollo environment, and the caller's Apollo creds determine which environments —
hence which cubes — they may read. Admins see all; a tenant sees only their
cube(s).

Two defenses, both applied to every tool here:

1. ``cube`` is a required argument and must be in the caller's ``allowed_cubes``
   set, else we reject before touching Groundcover.
2. We never forward a raw user query untouched. Metrics queries are *built*
   server-side from structured args with ``cluster="<cube>"`` pinned into the
   PromQL selector (``_build_promql``). Every other query (logs, traces, k8s
   events, workloads, metric discovery) carries a ``cluster == <cube>`` Condition
   that we add — placed in both ``sources`` (the scope selector) and
   ``conditions`` where the endpoint has both, which is fail-closed: both are
   AND-narrowing, so at worst a query returns nothing, never another cube's data.

READ-ONLY GUARANTEE. ``GroundcoverClient`` exposes only query/search/list/get
calls, and ``_request`` refuses any (method, path) not on ``_READ_ENDPOINTS`` and
any verb other than GET/POST. There is no create/update/delete code path. The
Groundcover monitors API (which has POST/PUT/DELETE write verbs) is intentionally
not wired up here.

Endpoint paths, request field names, the Condition shape, and the ``cluster``
label key were all taken from Groundcover's official Go SDK
(github.com/groundcover-com/groundcover-sdk-go), not guessed. Response formatting
is best-effort and may need tuning against the live API; the authz logic does
not depend on response shape.

MULTI-BACKEND ROUTING. Our fleet's telemetry is not all in one Groundcover
backend — confirmed live (2026-08-11) that dev cubes (e.g. ``cube-9px8lv5i``)
report into a *different* backend (``edgescaleai-dev``) than prod
(``groundcover``), and that the org API key works against both via the
``X-Backend-Id`` header alone (one key, not two accounts). ``GroundcoverRegistry``
holds one ``GroundcoverClient`` per configured backend id and a cached
``cube -> backend_id`` index (built by fanning ``clusters_list`` out across every
backend), so a per-cube call is routed to whichever backend actually reports
that cube instead of assuming a single global backend. See
docs/groundcover-integration-spec.md, "Multi-backend routing", for the full
design rationale (a hand-maintained cube->backend map was rejected as the
primary mechanism — it silently drifts).
"""

from __future__ import annotations

import asyncio
import json
import re
from datetime import datetime, timedelta, timezone
from functools import lru_cache

import boto3
import httpx
from botocore.exceptions import ClientError

from cube_cloud.auth.apollo_rbac import allowed_cubes
from cube_cloud.config import settings
from cube_common.apollo_client import ApolloClient

# Groundcover read-only endpoints (method, path). _request refuses anything else.
_READ_ENDPOINTS: set[tuple[str, str]] = {
    ("POST", "/api/k8s/v3/clusters/list"),
    ("POST", "/api/k8s/v3/workloads/list"),
    ("POST", "/api/k8s/v2/events/search"),
    ("POST", "/api/metrics/query"),
    ("POST", "/api/metrics/names"),
    ("POST", "/api/logs/v2/search"),
    ("POST", "/api/traces/v2/search"),
}

_METRIC_RE = re.compile(r"^[a-zA-Z_:][a-zA-Z0-9_:]*$")
_LABEL_KEY_RE = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")
_WINDOW_RE = re.compile(r"^[0-9]+(ms|s|m|h|d|w|y)$")

_RANGE_AGGS = {"rate", "irate", "increase", "delta", "idelta", "deriv"}
_INSTANT_AGGS = {"sum", "avg", "min", "max", "count", "stddev", "stdvar"}


class GroundcoverError(Exception):
    """Raised for Groundcover API or validation errors."""


# ---------------------------------------------------------------------------
# Condition / time helpers (shapes from the groundcover Go SDK)
# ---------------------------------------------------------------------------

def _cluster_condition(cube: str) -> dict:
    """A `cluster == cube` Condition, matching the SDK's ConditionSet output."""
    return {
        "key": "cluster",
        "origin": "root",
        "type": "string",
        "filters": [{"op": "eq", "value": cube}],
    }


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _rfc3339(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _time_window(start: str | None, end: str | None, default_minutes: int = 60) -> tuple[str, str]:
    """Resolve a (start, end) window, defaulting to the last `default_minutes`."""
    end_s = end or _rfc3339(_now())
    start_s = start or _rfc3339(_now() - timedelta(minutes=default_minutes))
    return start_s, end_s


# ---------------------------------------------------------------------------
# Safe PromQL builder (metrics half of the cross-cube guard)
# ---------------------------------------------------------------------------

def _escape_label_value(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "")


def _build_selector(metric: str, cube: str, match: dict | None) -> str:
    if not _METRIC_RE.match(metric):
        raise GroundcoverError(f"Invalid metric name: {metric!r}")
    matchers = [f'cluster="{_escape_label_value(cube)}"']
    for key, value in (match or {}).items():
        if key == "cluster":
            raise GroundcoverError("'cluster' may not be set in match; it is pinned to your cube.")
        if not _LABEL_KEY_RE.match(key):
            raise GroundcoverError(f"Invalid label key: {key!r}")
        matchers.append(f'{key}="{_escape_label_value(str(value))}"')
    return f"{metric}{{{','.join(matchers)}}}"


def _build_promql(metric: str, cube: str, match: dict | None,
                  aggregation: str | None, window: str | None) -> str:
    selector = _build_selector(metric, cube, match)
    if aggregation is None:
        if window is not None:
            raise GroundcoverError("window requires an aggregation (e.g. rate).")
        return selector
    if aggregation in _RANGE_AGGS:
        win = window or "5m"
        if not _WINDOW_RE.match(win):
            raise GroundcoverError(f"Invalid window: {win!r}")
        return f"{aggregation}({selector}[{win}])"
    if aggregation in _INSTANT_AGGS:
        if window is not None:
            raise GroundcoverError(f"{aggregation} does not take a window.")
        return f"{aggregation}({selector})"
    raise GroundcoverError(
        f"Unsupported aggregation {aggregation!r}. "
        f"Allowed: {sorted(_RANGE_AGGS | _INSTANT_AGGS)}"
    )


# ---------------------------------------------------------------------------
# Groundcover HTTP client (read-only by construction)
# ---------------------------------------------------------------------------

def _parse_backend_ids(value: str) -> list[str]:
    return [b.strip() for b in value.split(",") if b.strip()]


@lru_cache(maxsize=1)
def _get_credentials() -> tuple[str, tuple[str, ...]]:
    """Read the Groundcover (api_key, backend_ids) from Secrets Manager (cached).

    One org-wide key is confirmed (live) to span every backend in `backend_ids`
    — see the MULTI-BACKEND ROUTING note at the top of this module. Each id is
    sent as the required `X-Backend-Id` header on its own client; without it
    the Groundcover data endpoints return 500/400.

    Resolution order: the secret's `backend_ids` (list or comma-separated
    string) wins; else its legacy singular `backend_id`; else
    `settings.groundcover_backend_ids`.
    """
    client = boto3.client("secretsmanager", region_name=settings.aws_region)
    try:
        resp = client.get_secret_value(SecretId=settings.groundcover_api_key_secret)
    except ClientError as e:
        raise GroundcoverError(
            f"Could not read Groundcover API key from "
            f"{settings.groundcover_api_key_secret}: {e}"
        ) from e
    secret = json.loads(resp["SecretString"])
    key = secret.get("api_key", "")
    if not key:
        raise GroundcoverError("Groundcover secret is missing 'api_key'.")

    if "backend_ids" in secret:
        raw = secret["backend_ids"]
        ids = _parse_backend_ids(raw) if isinstance(raw, str) else [str(b) for b in raw]
    elif "backend_id" in secret:  # legacy single-backend secret shape
        ids = [secret["backend_id"]]
    else:
        ids = _parse_backend_ids(settings.groundcover_backend_ids)

    if not ids:
        raise GroundcoverError("No Groundcover backend_ids configured.")
    return key, tuple(ids)


class GroundcoverClient:
    """Thin async client over the Groundcover *read* APIs.

    Every call goes through `_request`, which refuses any endpoint not on the
    read-only allowlist and any verb other than GET/POST — so this client is
    structurally incapable of mutating Groundcover.
    """

    def __init__(self, api_key: str, base_url: str | None = None,
                 backend_id: str = "") -> None:
        self._base = (base_url or settings.groundcover_api_base).rstrip("/")
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if backend_id:  # required by the Groundcover data endpoints
            headers["X-Backend-Id"] = backend_id
        self._http = httpx.AsyncClient(timeout=60, headers=headers)

    async def __aenter__(self) -> "GroundcoverClient":
        return self

    async def __aexit__(self, *exc) -> None:
        await self._http.aclose()

    async def _request(self, method: str, path: str, body: dict | None = None) -> dict:
        if method not in ("GET", "POST") or (method, path) not in _READ_ENDPOINTS:
            # Defense in depth: never issue a non-read call.
            raise GroundcoverError(f"Refusing non-read Groundcover call: {method} {path}")
        resp = await self._http.request(method, f"{self._base}{path}", json=body)
        if resp.status_code != 200:
            raise GroundcoverError(f"Groundcover {method} {path} failed ({resp.status_code}): {resp.text[:300]}")
        try:
            return resp.json()
        except ValueError as e:
            raise GroundcoverError(f"Groundcover {method} {path} returned non-JSON: {e}") from e

    # -- read calls --------------------------------------------------------

    async def clusters_list(self, sources: list[dict] | None = None) -> dict:
        return await self._request("POST", "/api/k8s/v3/clusters/list", {"sources": sources or []})

    async def workloads_list(self, cube: str, limit: int, namespace: str | None,
                             sort_by: str = "workload", order: str = "asc") -> dict:
        # Live API validated: workloads/list requires sortBy + order, else 400.
        cond = [_cluster_condition(cube)]
        if namespace:
            cond.append({"key": "namespace", "origin": "root", "type": "string",
                         "filters": [{"op": "eq", "value": namespace}]})
        return await self._request("POST", "/api/k8s/v3/workloads/list", {
            "sources": [_cluster_condition(cube)],
            "conditions": cond,
            "limit": limit, "sortBy": sort_by, "order": order,
        })

    async def metrics_query(self, promql: str, start: str, end: str, step: str) -> dict:
        # Live API validated: only QueryType "range" is accepted here ("instant"
        # returns 400). A short range with a small step covers point-in-time use.
        return await self._request("POST", "/api/metrics/query", {
            "Promql": promql, "QueryType": "range",
            "Start": start, "End": end, "Step": step, "Conditions": [],
        })

    async def metrics_names(self, cube: str, start: str, end: str, limit: int,
                            filter: str | None = None) -> dict:
        body: dict = {
            "sources": [_cluster_condition(cube)],
            "required": [],
            "start": start, "end": end, "limit": limit,
        }
        if filter:  # server-side substring filter on metric names
            body["filter"] = filter
        return await self._request("POST", "/api/metrics/names", body)

    async def logs_search(self, cube: str, start: str, end: str, query: str) -> dict:
        # Live API validated: `query` is required and MUST be bounded — a bare
        # `*` streams unboundedly and hangs the connection. Callers pass a query
        # that already includes `| limit N` (see search_logs handler).
        return await self._request("POST", "/api/logs/v2/search", {
            "sources": [_cluster_condition(cube)], "start": start, "end": end, "query": query,
        })

    async def traces_search(self, cube: str, start: str, end: str, query: str) -> dict:
        return await self._request("POST", "/api/traces/v2/search", {
            "sources": [_cluster_condition(cube)], "start": start, "end": end, "query": query,
        })

    async def k8s_events_search(self, cube: str, start: str, end: str, query: str = "*") -> dict:
        return await self._request("POST", "/api/k8s/v2/events/search", {
            "sources": [_cluster_condition(cube)], "start": start, "end": end, "query": query,
        })


class GroundcoverRegistry:
    """One `GroundcoverClient` per configured backend id, all sharing the same
    org API key, plus a cached `cube -> backend_id` index used to route
    per-cube calls.

    The index is built by fanning `clusters_list()` out across every backend
    (`clusters_by_backend`) — the same call `list_clusters` needs anyway to
    answer "which cubes across both backends" — and cached with a short TTL.
    A backend that errors during a refresh keeps its *previous* entries rather
    than being treated as "now has zero clusters", so one backend's hiccup
    doesn't blank out what we already knew about the others.

    This is a process-lifetime singleton (see `groundcover_registry()`) so the
    cache — and the underlying httpx connections — actually amortize across
    calls instead of being rebuilt on every tool invocation.
    """

    _INDEX_TTL_SECONDS = 300

    def __init__(self, clients: dict[str, GroundcoverClient]) -> None:
        self.clients = clients
        self._index: dict[str, str] = {}
        self._index_at: float = 0.0
        self._refresh_lock = asyncio.Lock()

    async def __aenter__(self) -> "GroundcoverRegistry":
        return self

    async def __aexit__(self, *exc) -> None:
        await asyncio.gather(*(c.__aexit__(*exc) for c in self.clients.values()))

    async def clusters_by_backend(self) -> dict[str, "list[str] | Exception"]:
        """Fan `clusters_list()` out to every backend. Returns
        `{backend_id: [cluster names] | the exception that backend raised}` —
        callers decide how to surface a partial failure rather than one down
        backend taking out the whole call."""
        async def _one(backend_id: str, client: GroundcoverClient):
            try:
                resp = await client.clusters_list()
                names = sorted({c.get("name") for c in resp.get("clusters", []) if c.get("name")})
                return backend_id, names
            except Exception as e:  # noqa: BLE001 - surfaced to the caller, not swallowed
                return backend_id, e

        pairs = await asyncio.gather(*(_one(bid, c) for bid, c in self.clients.items()))
        return dict(pairs)

    async def _refresh_index(self) -> None:
        by_backend = await self.clusters_by_backend()
        failed = {bid for bid, v in by_backend.items() if isinstance(v, Exception)}
        index = {cube: bid for cube, bid in self._index.items() if bid in failed}
        for backend_id, names in by_backend.items():
            if backend_id in failed:
                continue
            for name in names:
                index[name] = backend_id  # last-writer-wins on a genuine cross-backend name collision
        self._index = index
        self._index_at = _now().timestamp()

    async def resolve_backend(self, cube: str) -> str | None:
        """Which backend `cube` is reporting to, or None if it's in none of
        them. Refreshes the index when it's past its TTL (single-flighted via
        `_refresh_lock` so concurrent misses share one fan-out); a hit within
        the TTL — including a cached "not found" — is trusted without
        re-probing on every call."""
        if (_now().timestamp() - self._index_at) > self._INDEX_TTL_SECONDS:
            async with self._refresh_lock:
                if (_now().timestamp() - self._index_at) > self._INDEX_TTL_SECONDS:
                    await self._refresh_index()
        return self._index.get(cube)


_registry: GroundcoverRegistry | None = None


def groundcover_registry() -> GroundcoverRegistry:
    """Factory used by the dispatcher; reads creds from Secrets Manager once
    and returns the same process-lifetime registry on every call (needed for
    the cube->backend cache to actually amortize — see `GroundcoverRegistry`)."""
    global _registry
    if _registry is None:
        api_key, backend_ids = _get_credentials()
        _registry = GroundcoverRegistry(
            {bid: GroundcoverClient(api_key, backend_id=bid) for bid in backend_ids}
        )
    return _registry


# ---------------------------------------------------------------------------
# Authorization
# ---------------------------------------------------------------------------

async def _authorize(apollo: ApolloClient, cube: str) -> tuple[bool, str]:
    allowed = await allowed_cubes(apollo)
    if cube not in allowed:
        return False, (
            f"Access denied: cube '{cube}' is not in your authorized set.\n"
            f"Authorized cubes: {', '.join(sorted(allowed)) or '(none)'}"
        )
    return True, ""


async def _authorize_and_route(
    apollo: ApolloClient, registry: GroundcoverRegistry, cube: str
) -> tuple[GroundcoverClient | None, str]:
    """Authorize `cube` against Apollo, then resolve which registered backend
    it's actually reporting to. Returns `(None, message)` on either failure —
    an unauthorized cube and a cube absent from every configured backend are
    both "can't help you", just for different reasons, so callers can treat
    them identically: return `msg` when `gc` is None."""
    ok, msg = await _authorize(apollo, cube)
    if not ok:
        return None, msg
    backend_id = await registry.resolve_backend(cube)
    if backend_id is None:
        return None, f"Cube '{cube}' is not reporting to Groundcover on any configured backend."
    return registry.clients[backend_id], ""


def _dump(obj, limit: int = 6000) -> str:
    return json.dumps(obj, indent=2, default=str)[:limit]


# ---------------------------------------------------------------------------
# Tool handlers
# ---------------------------------------------------------------------------

async def list_clusters(apollo: ApolloClient, registry: GroundcoverRegistry) -> str:
    """List the caller's authorized cubes that are reporting to Groundcover,
    across every configured backend."""
    allowed = await allowed_cubes(apollo)
    if not allowed:
        return "You have no authorized cubes."

    by_backend = await registry.clusters_by_backend()
    gc_clusters: set[str] = set()
    failed = []
    for backend_id, names in by_backend.items():
        if isinstance(names, Exception):
            failed.append(f"{backend_id} ({names})")
        else:
            gc_clusters.update(names)

    reporting = sorted(allowed & gc_clusters)
    not_reporting = sorted(allowed - gc_clusters)

    lines = [f"Groundcover clusters you can read ({len(reporting)}):", "=" * 50]
    lines += [f"  {c}" for c in reporting] or ["  (none reporting to Groundcover)"]
    if not_reporting:
        lines += ["", "Authorized cubes NOT reporting to Groundcover:"]
        lines += [f"  {c}" for c in not_reporting]
    if failed:
        lines += ["", "Some Groundcover backends could not be reached (results may be incomplete):"]
        lines += [f"  {b}" for b in failed]
    return "\n".join(lines)


async def list_workloads(apollo: ApolloClient, registry: GroundcoverRegistry, cube: str,
                         namespace: str | None = None, limit: int = 100) -> str:
    """List workloads (deployments/pods) and their health for one cube."""
    gc, msg = await _authorize_and_route(apollo, registry, cube)
    if gc is None:
        return msg
    try:
        resp = await gc.workloads_list(cube, max(1, min(int(limit), 1000)), namespace)
    except GroundcoverError as e:
        return f"Error: {e}"

    workloads = resp.get("workloads", [])
    lines = [f"Workloads for cube '{cube}' ({len(workloads)})", "=" * 60]
    for w in workloads:
        lines.append(
            f"  {w.get('namespace','?')}/{w.get('workload','?')} "
            f"[{w.get('kind','?')}] pods={w.get('podsCount','?')} "
            f"ready={w.get('ready','?')} cpu={w.get('cpuUsage','?')} "
            f"mem={w.get('memoryUsage','?')} rps={w.get('rps','?')} "
            f"errRate={w.get('errorRate','?')} issues={w.get('issueCount','?')}"
        )
    return "\n".join(lines) if workloads else f"No workloads found for cube '{cube}'."


async def query_metrics(
    apollo: ApolloClient, registry: GroundcoverRegistry, cube: str, metric: str,
    match: dict | None = None, aggregation: str | None = None, window: str | None = None,
    start: str | None = None, end: str | None = None, step: str | None = None,
) -> str:
    """Run a cluster-pinned PromQL query built from structured args."""
    gc, msg = await _authorize_and_route(apollo, registry, cube)
    if gc is None:
        return msg
    try:
        promql = _build_promql(metric, cube, match, aggregation, window)
    except GroundcoverError as e:
        return f"Error: {e}"

    # The endpoint only accepts range queries; default to the last 15 minutes at
    # a 1m step when no window is given (covers point-in-time use).
    start_s, end_s = _time_window(start, end, default_minutes=15)
    try:
        resp = await gc.metrics_query(promql, start_s, end_s, step or "1m")
    except GroundcoverError as e:
        return f"Error: {e}"

    return (
        f"Groundcover metrics (range {start_s} → {end_s}) for cube '{cube}'\n"
        f"PromQL: {promql}\n{'=' * 50}\n{_dump(resp.get('data', resp))}"
    )


def _metric_families(names: list[str]) -> list[tuple[str, int, list[str]]]:
    """Group metric names by their first two underscore-tokens.

    Returns (family_prefix, count, up-to-3 example names) sorted alphabetically.
    Groundcover metric names are NOT standard Prometheus names, so this vocabulary
    map is how a caller discovers what to `filter` for (e.g. the `groundcover_pvc_*`
    family for PVC fill — there is no `kube_persistentvolumeclaim_*`).
    """
    groups: dict[str, list[str]] = {}
    for n in names:
        parts = n.split("_")
        prefix = "_".join(parts[:2]) if len(parts) >= 2 else n
        groups.setdefault(prefix, []).append(n)
    # Sort by size (biggest, most substantive families first), then name — the
    # catalog has a long tail of ~1-metric internal agent families.
    out = []
    for prefix in sorted(groups, key=lambda p: (-len(groups[p]), p)):
        members = sorted(groups[prefix])
        out.append((prefix, len(members), members[:3]))
    return out


# Common concepts → filter hooks, so the caller has hooks without scanning.
# `host` first: the whole-machine families (host_cpu/host_mem/host_fs) are what a
# caller asking "how loaded is this cube" actually wants, and they are easy to miss
# behind the per-container and per-node families.
_FILTER_HINTS = "host, pvc, disk, fs, cpu, memory, network, http, restart, latency, node"
_MAX_FAMILIES_SHOWN = 40


async def list_metrics(apollo: ApolloClient, registry: GroundcoverRegistry, cube: str,
                       start: str | None = None, end: str | None = None,
                       limit: int = 1000, filter: str | None = None) -> str:
    """Discover metrics for one cube.

    Without `filter`: returns a families/vocabulary map (prefix + count + examples)
    so the caller can see what to filter for. With `filter`: returns the matching
    metric names (feed one to groundcover_query_metrics).
    """
    gc, msg = await _authorize_and_route(apollo, registry, cube)
    if gc is None:
        return msg
    start_s, end_s = _time_window(start, end)
    try:
        resp = await gc.metrics_names(cube, start_s, end_s, max(1, min(int(limit), 5000)), filter)
    except GroundcoverError as e:
        return f"Error: {e}"

    names = sorted(m.get("name", "") for m in resp.get("metrics", []) if m.get("name"))

    if filter:
        header = f"{len(names)} metric(s) for cube '{cube}' matching '{filter}':"
        body = "\n".join(f"  {n}" for n in names) or "  (none — try a different filter)"
        return f"{header}\n{'=' * 50}\n{body}"

    families = _metric_families(names)
    shown = families[:_MAX_FAMILIES_SHOWN]
    lines = [
        f"{len(names)} metrics for cube '{cube}' in {len(families)} families.",
        "Metric names are Groundcover-specific (NOT standard Prometheus/k8s names). "
        "Call again with filter=<word> to get matching names, then pass one to "
        f"groundcover_query_metrics. Common filters: {_FILTER_HINTS}.",
        "=" * 50,
    ]
    for prefix, count, examples in shown:
        lines.append(f"  {prefix}_* ({count})  e.g. {', '.join(examples)}")
    if len(families) > len(shown):
        lines.append(f"  … +{len(families) - len(shown)} smaller families — use filter to search.")
    return "\n".join(lines)


def _bounded_query(query: str | None, limit: int) -> str:
    """Build a Groundcover search query that is always bounded by a limit.

    A bare `*` (or any query without a limit) streams unboundedly and hangs the
    connection, so we append `| limit N` when the caller hasn't set one.
    """
    q = (query or "*").strip()
    if "limit" not in q.lower():
        q = f"{q} | limit {limit}"
    return q


async def search_logs(apollo: ApolloClient, registry: GroundcoverRegistry, cube: str,
                      start: str | None = None, end: str | None = None,
                      query: str | None = None, limit: int = 100) -> str:
    """Search logs for one cube. Pinned to the authorized cube."""
    gc, msg = await _authorize_and_route(apollo, registry, cube)
    if gc is None:
        return msg
    start_s, end_s = _time_window(start, end)
    q = _bounded_query(query, max(1, min(int(limit), 1000)))
    try:
        resp = await gc.logs_search(cube, start_s, end_s, q)
    except GroundcoverError as e:
        return f"Error: {e}"
    return f"Logs for cube '{cube}' ({start_s} → {end_s}, query: {q})\n{'=' * 50}\n{_dump(resp)}"


async def search_traces(apollo: ApolloClient, registry: GroundcoverRegistry, cube: str,
                        start: str | None = None, end: str | None = None,
                        query: str | None = None, limit: int = 100) -> str:
    """Search traces for one cube. Pinned to the authorized cube."""
    gc, msg = await _authorize_and_route(apollo, registry, cube)
    if gc is None:
        return msg
    start_s, end_s = _time_window(start, end)
    q = _bounded_query(query, max(1, min(int(limit), 1000)))
    try:
        resp = await gc.traces_search(cube, start_s, end_s, q)
    except GroundcoverError as e:
        return f"Error: {e}"
    return f"Traces for cube '{cube}' ({start_s} → {end_s}, query: {q})\n{'=' * 50}\n{_dump(resp)}"


async def k8s_events(apollo: ApolloClient, registry: GroundcoverRegistry, cube: str,
                     start: str | None = None, end: str | None = None) -> str:
    """Search Kubernetes events for one cube. Pinned to the authorized cube."""
    gc, msg = await _authorize_and_route(apollo, registry, cube)
    if gc is None:
        return msg
    start_s, end_s = _time_window(start, end)
    try:
        resp = await gc.k8s_events_search(cube, start_s, end_s)
    except GroundcoverError as e:
        return f"Error: {e}"
    return f"K8s events for cube '{cube}' ({start_s} → {end_s})\n{'=' * 50}\n{_dump(resp)}"
