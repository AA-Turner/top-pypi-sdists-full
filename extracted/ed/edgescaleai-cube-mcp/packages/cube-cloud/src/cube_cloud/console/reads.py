"""Structured reads behind the console's JSON API (docs/console-spec.md §4.4).

This module queries Apollo through the **shared** query constants
(`cube_common.apollo_queries`) and the **shared** RBAC helpers
(`auth.apollo_rbac`) and returns plain dicts. It deliberately does NOT call the
MCP tool functions and parse their output: those formatters exist for agents, and
scraping them is what made the previous `edgeport` implementation carry five
hand-written text parsers that broke whenever a tool's wording changed.

Sharing the *query* layer rather than the *presentation* layer means one source of
truth for the GraphQL and two renderers over it — text for agents, JSON here. It
is also the seam the eventual unified API grows from: MCP tool handlers can be
moved onto these functions one at a time rather than in a single refactor.

**Two rules govern every function here.**

1. **Serialize through an explicit field allowlist, never by passing an Apollo
   object through.** Apollo entity payloads carry `declaredState.config`, which
   holds **cleartext deployment secrets** (verified live: a litellm `masterKey` on
   `cube-66odzn95`). The console does not redact those — it never selects them and
   never emits a config field, so a future Apollo field that starts carrying a
   secret cannot leak through a serializer that only copies named keys. Tests
   assert the response shape *is* the allowlist.

2. **RBAC is `auth.apollo_rbac`'s, never re-implemented.** The caller's profile
   already resolved to per-tenant Apollo credentials in the middleware; visibility
   is decided by `has_environment_access`, the same function the MCP environment
   tools use.
"""

from __future__ import annotations

import asyncio
import ipaddress
import logging
import re
from datetime import datetime, timedelta, timezone
from typing import NamedTuple
from urllib.parse import urlsplit

from cube_common import apollo_queries as Q
from cube_common.apollo_client import ApolloClient
from cube_common.apollo_pagination import fetch_all_environments
from cube_cloud.auth.apollo_rbac import get_user_team_names, has_environment_access
from cube_cloud.auth.app_companies import (
    AppCompanies,
    app_companies,
    is_unscoped,
    label_companies,
    reads_stored_sets,
)
from cube_cloud.browser_proxy.resolver import browser_app_url, is_http_app
from cube_cloud.config import settings
from cube_cloud.console import cache
from cube_cloud import ic2, inventory, places
from cube_cloud.tools.environments import TELEPORT_APP_SERVICE_PRODUCTS

logger = logging.getLogger(__name__)


async def _visible_environments(
    client: ApolloClient, profile: str
) -> tuple[list[dict], bool]:
    """Every Apollo environment the caller's teams have a role on.

    Both queries are cached per profile (see `console/cache.py`) because
    `_resolve_environment` in the MCP tools reissues them on *every* call — a cube
    detail view is otherwise three Apollo round-trips, two of them repeating what
    the list page just fetched.
    """
    envs, truncated, teams = await _environments_and_teams(client, profile)
    return [e for e in envs if has_environment_access(e, teams)], truncated


async def _environments_and_teams(
    client: ApolloClient, profile: str
) -> tuple[list[dict], bool, set[str]]:
    """`(every environment the read returned, truncated, the caller's teams)`, cached.

    The UNFILTERED list, for a caller that has to reason about names across the fleet
    before narrowing to what this profile may open (`fleet_apps`' placement). Anything
    that returns environments to the browser goes through `_visible_environments`.
    """
    envs, truncated = await cache.get_or_set(
        profile, "environments",
        lambda: _fetch_environments(client),
    )
    teams = await cache.get_or_set(
        profile, "teams",
        lambda: get_user_team_names(client),
    )
    return envs, truncated, teams


async def _fetch_environments(client: ApolloClient) -> tuple[list[dict], bool]:
    """Every environment the query returns, plus whether the read fell short.

    The drain lives in `cube_common.apollo_pagination` so this path, the MCP
    `list_environments` tool and `allowed_cubes` all share one loop — fixing issue
    252 in the shared module is what fixed all four call sites at once.

    **`truncated` has changed meaning, and the old meaning must not come back.**
    Before pagination it meant "the page came back full", because a saturated page
    was the only truncation signal that did not depend on unverified Apollo
    behaviour. Now every page but the last is full by construction, so saturation
    says nothing at all; `truncated` means the drain STOPPED EARLY — the page cap
    was hit, or the next-page token stopped advancing. Re-adding a
    `len(envs) >= ENVIRONMENTS_PAGE_SIZE` check here would put a permanent banner
    on any fleet larger than one page.

    It still reports upward rather than raising, for the reason it always did: a
    partial list the UI can label beats an error page, because a cube missing with
    no explanation reads as "deleted" or "I lost access".
    """
    result = await fetch_all_environments(client, Q.CONSOLE_LIST_ENVIRONMENTS)
    if result.truncated:
        # The drain logs the specific cause (cap or stalled token); this adds the
        # console-facing consequence, which is what someone greps for after a user
        # says a cube is missing from the list.
        logger.error(
            "console cube list is INCOMPLETE: the environment drain stopped early "
            "with %d environments read. See OI-6 in docs/console-spec.md.",
            len(result.items),
        )
    return result.items, result.truncated


# Apollo agent connection statuses, lowercased. Observed on the live fleet:
# CONNECTED | STALE | NEVER_REPORTED.
_AGENT_STATUSES = frozenset({"connected", "stale", "never_reported"})


def _display_name(env: dict) -> str:
    """Apollo's human label for an environment, or "" — never a key.

    `displayMetadataV2` is nullable and populated on only ~50 of 166 environments,
    and **several of those are just an echo of the environment id or name**, which
    carries no information a viewer does not already have on screen. Those are dropped
    by exact case-insensitive match against both.

    Exact match, not substring: a legitimate label can contain the cube name
    (`cube-9likqvpd-spare`), and eating it would be worse than showing an echo.
    """
    meta = env.get("displayMetadataV2") or {}
    label = str(meta.get("displayName") or "").strip()
    if not label:
        return ""
    for identifier in (env.get("name"), env.get("id")):
        if label.casefold() == str(identifier or "").strip().casefold():
            return ""
    return label


def _agent_status(env: dict) -> str:
    """One status for the cube, rolled up from its agents.

    Returns `connected` | `stale` | `never_reported` | `mixed` | `unknown` | `none`.

    **`mixed` is a real state, not a rounding error.** On the live fleet today: 61
    cubes all-CONNECTED, 92 all-STALE, 7 NEVER_REPORTED and **6 mixed**. Reading
    `agents[0]` would report one of those 6 as whatever its first agent happened to
    be, silently, and the answer would flip as Apollo reordered the list. So the roll
    up is deliberate and disagreement is surfaced rather than resolved.

    A status Apollo adds later lands as `unknown` rather than being folded into a
    state we recognize — the same fail-visible rule the health and lifecycle dots
    follow.
    """
    agents = env.get("agents") or []
    seen = {
        str((a or {}).get("connectionStatus") or "").strip().casefold()
        for a in agents
        if isinstance(a, dict)
    }
    seen.discard("")
    if not seen:
        return "none"
    if len(seen) > 1:
        return "mixed"
    only = next(iter(seen))
    return only if only in _AGENT_STATUSES else "unknown"


def _agent_last_updated(env: dict) -> str:
    """The newest `lastUpdated` across the cube's agents, or "".

    Comes free with the `agents` selection — `ApolloAgent_Reporting.lastUpdated`
    carries the same information as `ApolloEnvironment.latestAgentUpdateTime`, which
    must NOT be selected here (it takes the list query from ~0.5s to ~4.5s across 166
    environments). Only `ApolloAgent_Reporting` has the field; a
    `ApolloAgent_NeverReported` member simply has none.

    Max, not first: `mixed` cubes have agents in different states, and the most recent
    contact is the useful one for "stale since when".
    """
    stamps = []
    for agent in env.get("agents") or []:
        if not isinstance(agent, dict):
            continue
        parsed = parse_rfc3339(str(agent.get("lastUpdated") or ""))
        if parsed is not None:
            stamps.append(parsed)
    if not stamps:
        return ""
    return max(stamps).astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _cube_summary(env: dict) -> dict:
    """Serialize ONE environment for the browser — allowlist, not passthrough.

    Only these eight fields ever reach a client. `rolePolicy` is deliberately
    dropped: it is how visibility was *decided*, and echoing another team's role
    statements would leak the tenancy graph to anyone who can see the cube. `agents`
    is dropped too — the per-agent `agentId`s are internal plumbing, and only the
    rolled-up status and newest timestamp are published.
    """
    return {
        "name": env.get("name") or "",
        "rid": env.get("rid") or "",
        "namespace": env.get("namespaceId") or "",
        "space_id": env.get("spaceId") or "",
        # Kept explicit so the UI never has to re-derive it: an Apollo environment
        # name IS the Teleport/Groundcover cluster name (auth/apollo_rbac.py
        # documents this as verified against ri.apollo.main).
        "cluster": env.get("name") or "",
        # A label only. Empty when Apollo has none, or when the one it has merely
        # echoes the id — see `_display_name`.
        "display_name": _display_name(env),
        "agent_status": _agent_status(env),
        "agent_last_updated": _agent_last_updated(env),
    }


CUBE_SUMMARY_FIELDS = frozenset({
    "name", "rid", "namespace", "space_id", "cluster",
    "display_name", "agent_status", "agent_last_updated",
})

# --- Inventory, per cube, on its own endpoint (OI-2) -----------------------
#
# Customer, site label, environment, serial, lifecycle status, location and the
# router's MAC live in `edgescale-inventory`, not Apollo. Three decisions shape this
# seam.
#
# 1. **The CUBE LIST does not join inventory, and that is a latency decision made
#    from measurement.** `/inventory/lookup` is a server-side partition scan, not a
#    point read: ~3.3s cold for ONE cube (measured against prod, 2026-08-26). Joining
#    the list meant one lookup per visible cube, so an admin seeing ~110 environments
#    waited ~45s for a page that used to be instant. The list therefore stays exactly
#    what it was before this feature — five Apollo fields, no inventory key at all —
#    and inventory is read only for the cube someone actually opens: one lookup
#    instead of N.
#
#    The cost of that choice is real and worth naming: the list is no longer
#    searchable by label, customer or serial, which was the most useful part of
#    closing OI-2 (`cube-o2e87m9a` is unmemorable; a serial off the chassis is not).
#    Getting it back cheaply needs the GSI-backed `?customer=` filter — one query for
#    a whole tenant instead of N scans. See `docs/console-spec.md` §4.13.
#
# 2. **It is a SEPARATE endpoint rather than a field on the cube-detail payload.**
#    Folding a ~3.3s read into `cube_apps` would have delayed the apps list — the
#    page's primary content — behind a secondary panel. Same reasoning, and the same
#    shape, as `cube_services`: a slow read the page fetches alongside rather than
#    inside the main one.
#
# 3. **Authorization is inherent, not re-checked.** `cube_inventory` resolves the
#    cube out of `_visible_environments`, which is RBAC-filtered upstream, and
#    returns None when it is not there — so a caller can only ever cause a lookup for
#    a cube they can already see. That ordering is the whole tenancy boundary for this
#    feature, since a read-capable inventory credential sees the entire fleet.


INVENTORY_SUMMARY_FIELDS = inventory.SUMMARY_FIELDS


async def cube_inventory(client: ApolloClient, profile: str, cube: str) -> dict | None:
    """Inventory facts for ONE cube, or None if the caller cannot see it.

    Returns `{"cube": name, "inventory": {...} | None, "inventory_source": {...}}`.

    `inventory` is `None` both when the join is disabled and when inventory simply
    has no record for the cube — an ordinary state, since a cube can exist in Apollo
    before anyone files its label. `inventory_source` is what tells those apart, plus
    the third case of "the backend could not be reached": collapsing any two would
    send someone debugging the wrong thing, the same reason `cube_services` keeps
    "could not look" distinct from "nothing there".

    Never raises on the inventory side — `inventory.lookup` degrades an unreachable
    backend to `available=False`, because Apollo is the authority for whether a cube
    exists and an inventory outage must not turn this into an error.
    """
    envs, envs_truncated = await _visible_environments(client, profile)
    match = next((e for e in envs if (e.get("name") or "") == cube), None)
    if match is None:
        # Same non-enumerable 404 contract as `cube_apps`: "not yours" and "does not
        # exist" are indistinguishable, and the truncation flag is a property of the
        # caller's own list rather than of any cube.
        if envs_truncated:
            return {"not_found": True, "environments_truncated": True}
        return None

    if not inventory.is_enabled():
        return {
            "cube": cube,
            "inventory": None,
            "resolved": True,
            "inventory_source": {
                "enabled": False, "available": True, "simulated": False,
            },
        }

    cluster = _cube_summary(match)["cluster"]
    result = await inventory.lookup({cluster} if cluster else set())
    record = result.records.get(cluster)
    return {
        "cube": cube,
        # THREE outcomes, not two. `inventory: null` with `available: true` has always
        # meant "inventory has no record", which is ordinary — a cube can exist in
        # Apollo before anyone files its label. `resolved: false` is the third: records
        # exist and more than one claims this cube, so the join refused to pick
        # (`inventory/client.py::_exact_match`). Folding that into "no record" would
        # send someone to create a label that already exists, and folding it into
        # `available: false` would blame the backend for answering correctly.
        "resolved": cluster not in result.unresolved,
        # `record.summary()` — the seven identity fields and nothing else. See
        # `inventory/records.py` for why that object is already minimal here.
        "inventory": record.summary() if record is not None else None,
        # The hardware specification, from the SAME record — so the Hardware tab
        # costs no extra request. `None` when there is no record at all; a populated
        # object with every field blank is possible and distinct, meaning "we have a
        # record but nobody filled in the specs" (about half the fleet).
        "hardware": (
            record.hardware.summary()
            if record is not None and record.hardware.any_known()
            else None
        ),
        "inventory_source": {
            "enabled": True,
            "available": result.available,
            "simulated": result.simulated,
        },
    }


# --- GPS location, per cube, on its own endpoint ---------------------------
#
# Where the cube's router last reported its GPS position, from Peplink InControl2
# (`cube_cloud/ic2/`). A LIVE reading, kept apart from inventory's typed-in Location,
# which is a declared fact: its own endpoint, its own source state, and an IC2 outage
# never touches the inventory panel. Join path: cube -> cluster -> inventory record ->
# router serial -> IC2 index. Authorization is the inventory endpoint's: the cube must
# be in `_visible_environments` before inventory or IC2 is asked anything.
#
# The router serial is used here and dropped. No key or value in this payload may
# contain it or the word "router" (the inventory payload's containment test checks
# both, and the state names are chosen to pass it).
#
# `place` is the nearest town to the position ("Denver, CO"), named offline from the
# GeoNames extract in `cube_cloud/places`. None when there is no position, no town
# within reach, or the extract can't be read: the row then shows coordinates.

#: Reports older than this read as stale. A constant, not config.
GPS_STALE_AFTER = timedelta(days=7)
#: How far in the future a report may be before its time is distrusted. Clocks drift a
#: little; more than this means the time is wrong, and a wrong time must never make a
#: report look fresh.
_GPS_FUTURE_TOLERANCE = timedelta(minutes=2)
#: Inventory's placeholder for "no router serial filed yet" (9 cubes on 2026-10-08).
_PLACEHOLDER_ROUTER_SERIAL = re.compile(r"^F{4}-F{4}-F{3}", re.IGNORECASE)


def _gps(state: str, position=None, now: datetime | None = None) -> dict:
    """The `gps` object. Coordinates and the nearest town for any state that has a
    position; time and age only when the time can be trusted.

    Callers holding a position await `places.ready()` first, so the extract's first
    load happens off the event loop rather than in here.
    """
    place = lat = lng = reported_at = age = None
    if position is not None:
        lat, lng = position.lat, position.lng
        place = places.nearest_place(lat, lng)
        if state in ("reported", "stale"):
            reported_at = position.reported_at.isoformat()
            age = max(0, int((now - position.reported_at).total_seconds()))
    return {
        "state": state, "place": place, "lat": lat, "lng": lng,
        "reported_at": reported_at, "age_seconds": age,
    }


def _gps_state(position, now: datetime) -> str:
    when = position.reported_at
    if when is None or when > now + _GPS_FUTURE_TOLERANCE:
        return "time_unknown"
    return "stale" if now - when > GPS_STALE_AFTER else "reported"


def _usable_router_serial(record) -> str | None:
    """The record's router serial in IC2's form, or None if there is none to look up
    (no record, a blank, or inventory's placeholder)."""
    serial = ic2.normalize_serial(record.router_serial_number if record else "")
    if not serial or _PLACEHOLDER_ROUTER_SERIAL.match(serial):
        return None
    return serial


def _gps_from_index(serial: str, index: dict, now: datetime) -> dict:
    """The `gps` object for a usable serial, from an IC2 index that was read.

    The per-cube read and the fleet read both decide a cube's state here, so the map
    and the cube page cannot disagree about one cube.
    """
    if serial not in index:
        return _gps("not_found")
    position = index[serial]
    if position is None:
        return _gps("no_position")
    return _gps(_gps_state(position, now), position, now)


async def cube_gps(client: ApolloClient, profile: str, cube: str) -> dict | None:
    """The cube router's latest GPS position, or None if the caller cannot see the cube.

    Returns `{"cube", "gps": {state, place, lat, lng, reported_at, age_seconds} | None,
    "gps_source": {enabled, available}}`. `state` is one of `reported`, `stale`,
    `time_unknown`, `no_position` (never reported one), `unmatched` (inventory has no
    usable router serial), `not_found` (IC2 doesn't know that serial) or `unavailable`
    (inventory or IC2 couldn't be read, so we couldn't look). Never raises on the
    inventory or IC2 side.
    """
    envs, envs_truncated = await _visible_environments(client, profile)
    match = next((e for e in envs if (e.get("name") or "") == cube), None)
    if match is None:
        # Same non-enumerable 404 contract as `cube_inventory`.
        if envs_truncated:
            return {"not_found": True, "environments_truncated": True}
        return None

    def answer(gps: dict | None, *, enabled: bool = True, available: bool = True) -> dict:
        return {
            "cube": cube, "gps": gps,
            "gps_source": {"enabled": enabled, "available": available},
        }

    if not ic2.is_enabled():
        return answer(None, enabled=False)
    if not inventory.is_enabled():
        # Without inventory there is no way to find the cube's router. That is
        # "couldn't look", not "no router on record".
        return answer(_gps("unavailable"), available=False)

    cluster = _cube_summary(match)["cluster"]
    found = await inventory.lookup({cluster} if cluster else set())
    if not found.available or cluster in found.unresolved:
        return answer(_gps("unavailable"), available=False)
    serial = _usable_router_serial(found.records.get(cluster))
    if serial is None:
        return answer(_gps("unmatched"))

    index = await ic2.positions()
    if index is None:
        return answer(_gps("unavailable"), available=False)
    if index.get(serial) is not None:
        await places.ready()
    return answer(_gps_from_index(serial, index, datetime.now(timezone.utc)))


# --- GPS positions, fleet-wide, for the landing page's map ------------------
#
# Every cube the viewer can see that has a position, plus counts of the ones that
# don't, so a sparse map is not read as a small fleet. Fetched only when someone opens
# the map; the cube LIST stays untouched (see the inventory note above).
#
# Authorization first, as everywhere: the viewer's Apollo-visible set is resolved
# before inventory or IC2 is asked anything, and only those cubes are looked up,
# listed or counted.
#
# Which inventory read depends on WHO is asking, never on how many cubes they see:
#   * an unscoped admin profile (`auth/app_companies.is_unscoped`, the same test that
#     gives it every app on the fleet Apps page and the break-glass module tools)
#     takes ONE cached whole-fleet read (`inventory.lookup_fleet`). Its Apollo team has
#     a role on every cube, so the sweep pulls nothing it could not already ask about
#     one cube at a time, at ~6.5 s instead of ~45 s;
#   * everyone else takes the per-cube lookups for exactly their cubes
#     (`inventory.lookup_each`, which ignores the cube page's sweep threshold), so
#     another customer's record never crosses the wire to answer them
#     (docs/console-spec.md §4.13).
# A visibility test such as "sees every environment Apollo listed" was rejected: the
# console spec records the admin seeing ~110 rows of a ~200-environment read (§4.6,
# §4.9), so it can be false for the admin, and it would be TRUE for any credential
# whose listing holds only its own cubes, which is the dangerous direction.
#
# No extra cache: each upstream already bounds its own cost (Apollo per profile for
# the console TTL, the fleet sweep and per-cube records for
# `inventory_cache_ttl_seconds`, IC2 for `ic2_cache_ttl_seconds`), and the join on top
# is in-memory work over at most a few hundred cubes.

GPS_FLEET_CUBE_FIELDS = frozenset({
    "name", "display_name", "state", "lat", "lng", "reported_at", "age_seconds",
    "place",
})
GPS_FLEET_COUNTS = (
    "shown", "no_position", "stale", "unmatched", "not_found", "time_unknown",
    "unresolved",
)
#: States that carry a position, i.e. the cubes the map can draw.
_GPS_POSITIONED = frozenset({"reported", "stale", "time_unknown"})


async def fleet_gps(client: ApolloClient, profile: str) -> dict:
    """GPS positions -> `{cubes, counts, gps_source, environments_truncated}`.

    `cubes` lists only cubes with a position (`reported`, `stale`, `time_unknown`),
    sorted by name, each with `place` (its nearest town, or None). `counts` covers
    every visible cube: `shown` is `len(cubes)`; `stale` and `time_unknown` count
    among the shown; `no_position`, `unmatched` and `not_found` are the cubes that
    could not be drawn, and `unresolved` the ones whose inventory record is ambiguous
    (more than one claims the cube, so we could not look). Every visible cube with a
    cluster is in exactly one of `shown` and those four.

    `gps_source` is the per-cube read's: `enabled: false` when the feature is off
    (nothing read), `available: false` when inventory or IC2 could not be read (no
    cubes, zero counts, never a 5xx). Raises only what the Apollo read raises.

    `environments_truncated` is the environment drain's own signal, as `list_cubes`
    carries it: when Apollo's list stopped short, "every visible cube" above is every
    cube we READ, so the counts line must not claim to cover the whole fleet. In Map
    mode the cube list's banner is not on screen to say so.
    """
    envs, truncated = await _visible_environments(client, profile)

    def answer(cubes: list[dict], counts: dict | None = None, *,
               enabled: bool = True, available: bool = True) -> dict:
        return {
            "cubes": cubes,
            "counts": counts or dict.fromkeys(GPS_FLEET_COUNTS, 0),
            "gps_source": {"enabled": enabled, "available": available},
            "environments_truncated": truncated,
        }

    if not ic2.is_enabled():
        return answer([], enabled=False)
    if not inventory.is_enabled():
        return answer([], available=False)

    visible = {
        cluster: env for env in envs
        if (cluster := _cube_summary(env)["cluster"])
    }
    if not visible:
        return answer([])

    if is_unscoped(profile):
        found = await inventory.lookup_fleet(set(visible))
    else:
        found = await inventory.lookup_each(set(visible))
    if not found.available:
        return answer([], available=False)
    index = await ic2.positions()
    if index is None:
        return answer([], available=False)
    await places.ready()

    now = datetime.now(timezone.utc)
    cubes: list[dict] = []
    counts = dict.fromkeys(GPS_FLEET_COUNTS, 0)
    # Driven by the VISIBLE set, never by what inventory returned, so a record for any
    # other cube cannot reach the payload even if a lower layer hands one back.
    for cluster in sorted(visible):
        if cluster in found.unresolved:
            counts["unresolved"] += 1
            continue
        serial = _usable_router_serial(found.records.get(cluster))
        gps = _gps("unmatched") if serial is None else _gps_from_index(serial, index, now)
        state = gps["state"]
        if state not in _GPS_POSITIONED:
            counts[state] += 1
            continue
        if state in ("stale", "time_unknown"):
            counts[state] += 1
        env = visible[cluster]
        cubes.append({
            "name": env.get("name") or "",
            "display_name": _display_name(env),
            **gps,
        })
    counts["shown"] = len(cubes)
    return answer(cubes, counts)


async def list_cubes(client: ApolloClient, profile: str) -> dict:
    """The caller's RBAC-scoped cube list, as a JSON-ready object.

    An **object**, not a bare list, per the read contract (spec §4.2 item 4) — a
    top-level array is historically readable cross-origin via `<script src>`.

    Every environment the profile can see is returned, with no name heuristics
    (spec §4.9). There is no "is a cube" flag in the Apollo payload, and any
    name-based filter would eventually hide a real customer cube — so an admin
    legitimately sees ~110 rows including personal test environments, and the UI
    makes that usable with search rather than by guessing.
    """
    envs, truncated = await _visible_environments(client, profile)
    cubes = sorted((_cube_summary(e) for e in envs), key=lambda c: c["name"])
    # NO inventory join here, deliberately — see the note above `_inventory_lookup`.
    # `truncated` is surfaced rather than swallowed: a short list with no
    # explanation is the worst outcome here, because a user would read it as
    # "that cube doesn't exist" or "I lost access to it".
    return {"cubes": cubes, "count": len(cubes), "truncated": truncated}

# ---------------------------------------------------------------------------
# Per-cube apps (Phase 3)
# ---------------------------------------------------------------------------

# Two lists classify an entity as PLATFORM rather than a customer/ESAI app. Of 18
# entities on a real cube, most are platform: the helm-chart operator,
# cert-manager, the Apollo auth broker, expected-state-k8s, the Teleport agents,
# Groundcover and its prereqs. EXACT product ids are the default way to name one;
# whole GROUPS are for a vendor whose entire group is platform. Neither list may
# hold a group that also publishes apps, and anything in neither is an app.
#
# Config, not literals (docs/console-spec.md §4.9), so a change needs an env var
# rather than a deploy of new code. Interim: products are to carry a platform label
# in Apollo, which replaces both lists.
def _platform_prefixes() -> tuple[str, ...]:
    """Platform product GROUPS, read per call.

    NOT captured at import: an import-time tuple cannot be patched in a test and
    would need a process restart to change, which is the same trap `is_enabled()`
    and `_apex_cookie_prefixes()` avoid for the same reason.
    """
    raw = settings.console_platform_product_prefixes or ""
    return tuple(p.strip().lower() for p in raw.split(",") if p.strip())


def _platform_product_ids() -> frozenset[str]:
    """Exact platform product ids, read per call for the same reason as the groups.

    The default way to mark a product as platform, and the only way for one that
    shares a product GROUP with customer apps, which no group entry can separate.
    Exact match only: a prefix here would turn
    `com.edgescaleai-cube:esai-groundcover` into a rule that also hides a customer
    product named `esai-groundcover-dashboard`.
    """
    raw = settings.console_platform_product_ids or ""
    return frozenset(p.strip().lower() for p in raw.split(",") if p.strip())


# Group delimiters an Apollo product id uses after the group segment. Matching must
# require one, or a bare "com.palantir" prefix also swallows
# `com.palantirventures:customer-app` and `com.teleportation-inc:their-app` —
# hiding a real customer app, which is the failure this classifier's fail-visible
# default exists to avoid.
_GROUP_DELIMITERS = (".", ":")


def classify_entity(product_id: str) -> str:
    """"app" or "platform" for an Apollo product id.

    Deterministic matching on an exact product id or a whole platform group —
    `edgeport` used a Claude call for this, which is not needed and is dropped
    (spec §4.9 non-goals).

    **An unrecognized product classifies as "app" — fail-VISIBLE.** A new
    customer-facing product should appear in the list the moment it exists, even
    before anyone teaches this function about it. The opposite default would make a
    real app silently invisible, which is the same class of failure as the
    truncation banner: absence with no explanation reads as "it is not deployed".
    """
    pid = (product_id or "").strip().lower()
    if pid and pid in _platform_product_ids():
        return "platform"
    for prefix in _platform_prefixes():
        # Exact group match, or the prefix followed by a delimiter — never a bare
        # string prefix (see _GROUP_DELIMITERS).
        if pid == prefix or pid.startswith(tuple(prefix + d for d in _GROUP_DELIMITERS)):
            return "platform"
    return "app"


APP_SUMMARY_FIELDS = frozenset({
    "id", "name", "entity_name", "product_id", "kind", "lifecycle",
    "version", "health", "rollout", "config_status", "blockers", "plan_state",
    "exposed",
})


def _app_summary(entity: dict) -> dict:
    """Serialize ONE entity — allowlist, not passthrough.

    Same discipline as `_cube_summary`, and it matters more here: entity payloads
    are where `declaredState.config` lives. That field is not even *fetched* (see
    `CONSOLE_ENVIRONMENT_ENTITIES`), so this is the second of two independent
    barriers rather than the only one.
    """
    reported = entity.get("reportedStatus") or {}
    plan = entity.get("planStatus") or {}
    locator = entity.get("entityLocator") or {}
    product_id = ((entity.get("product") or {}).get("productId")) or ""

    plan_state = (plan.get("__typename") or "").replace("ApolloEntityPlanStatus_", "")

    return {
        "id": entity.get("id") or "",
        "name": entity.get("displayName") or locator.get("entityName") or "",
        "entity_name": locator.get("entityName") or "",
        "product_id": product_id,
        "kind": classify_entity(product_id),
        "lifecycle": entity.get("lifecycleStatus") or "",
        "version": reported.get("version") or "",
        "health": reported.get("healthStatus") or "",
        "rollout": reported.get("rolloutStatus") or "",
        "config_status": reported.get("configStatus") or "",
        "blockers": list(reported.get("upgradeBlockerTypes") or []),
        "plan_state": plan_state,
        # Filled in by `_attach_exposed`. Always a list — an entity can expose more
        # than one service (minio publishes an S3 API *and* a console).
        "exposed": [],
    }


# --- Exposed apps: the public URL on an app card ----------------------------
#
# An exposed app has TWO addresses and the console must show the second one:
#
#   1. `public_addr` as `expose` stores it -> `<qualified>.edgescaleai.teleport.sh`
#      Teleport's own address. Reaching it requires a Teleport account, so it is
#      useless to the console's audience.
#   2. `<qualified>.<apex>` -> the browser app proxy (docs/browser-app-proxy-spec.md),
#      which authenticates with the same session cookie the console already has.
#      This is the account-less URL, and the one rendered on the card.
#
# The leftmost label must be the **qualified** name (`<app>-<env>`), not the bare
# app name: `browser_proxy/resolver.py` strips the apex and uses what is left *as
# the Teleport app name*, so a bare label would fail to resolve at dial time.

# `companies` is the app's audience; `reachable` says whether THIS caller holds one of
# them. An app the caller cannot reach is listed (on a "stored" stack) with its name,
# audience and `target` only: `url` and `uri` are "" so nothing about reaching it
# crosses to the browser.
#
# `target` is the `{namespace, service, port}` the app points at (`_target_from_uri`), so
# the cube page can draw it on the line for that Service port (docs/console-spec.md
# §4.4f). It is sent for an unreachable app TOO, and that is a deliberate widening: it
# tells a viewer already authorized for this cube which in-cluster Service and port
# another company's app targets. Usually one `/services` lists for that viewer anyway —
# but not always: not when `/services` failed for them, and not for a Service in an
# infra namespace `fetch_services` filters out. Accepted, since the viewer is authorized
# for the cube; the narrowing that WOULD matter is enforced: only a cluster-local host
# form yields a target (`_target_from_uri`), so an app pointed at an arbitrary external
# hostname reveals nothing of it. It never carries the scheme, the host, the URL,
# rewrite headers or the Teleport address.
EXPOSED_SUMMARY_FIELDS = frozenset(
    {"name", "url", "uri", "companies", "unreadable_companies", "reachable", "target"}
)

# What the console says when the Service enumeration failed. Fixed text, composed
# here: `fetch_services`' own `error` is written for an MCP operator and carries
# ApolloError or kubectl detail that must not reach a browser. See `cube_services`.
SERVICES_UNAVAILABLE_MESSAGE = (
    "Could not read this cube's services just now. Try again in a moment."
)


def _proxy_url(qualified_name: str) -> str:
    """Browser-app-proxy URL for an exposed app, or "" if it has none.

    Delegates to `browser_proxy.resolver.browser_app_url` — the same module that
    parses the host back at dial time, so the console cannot publish a URL the
    proxy would refuse to route, and the `expose`/`list_exposed` tools cannot
    drift from what the card shows. `settings.domain` is per-env
    (`cube.edgescaleai-cube.com` in prod, `cube-dev.…` in dev), so the dev/prod
    split needs no branch here; "" rather than a half-built URL keeps a
    misconfigured stack from rendering a link to nowhere.
    """
    return browser_app_url(qualified_name)


def _service_from_uri(uri: str) -> tuple[str, str]:
    """`(service, namespace)` from a cluster-local URI, or `("", "")`.

    `http://litellm.esai-sovereign-ai.svc.cluster.local:4000` -> `("litellm",
    "esai-sovereign-ai")`. `expose` accepts an arbitrary `app_uri`, so anything
    that is not `<service>.<namespace>…` — a bare hostname, a raw IP — yields
    `("", "")` and simply does not participate in the join.
    """
    if "//" not in uri:
        uri = f"//{uri}"
    try:
        host = urlsplit(uri).hostname or ""
    except ValueError:
        return "", ""
    if not host:
        return "", ""
    try:
        # A raw IP has no service/namespace to read; `10.0.0.5` would otherwise
        # yield service "10", namespace "0".
        ipaddress.ip_address(host)
        return "", ""
    except ValueError:
        pass
    labels = host.split(".")
    if len(labels) < 2 or not labels[0] or not labels[1]:
        return "", ""
    return labels[0], labels[1]


# The port a URI implies when it names none. Only the schemes `expose` accepts over
# HTTP; a `tcp://` target has no default, so a port-less one has no line to land on.
_DEFAULT_PORTS = {"http": 80, "https": 443}


def _target_from_uri(uri: str) -> dict | None:
    """`{namespace, service, port}` for a cluster-local URI, or None.

    The key the cube page joins an exposed app to a Service PORT on — equality on these
    three fields, so the browser never parses a URI. Built on `_service_from_uri`, so an
    app lands on the same Service here that `_match_entity` attributes it to. A missing
    port defaults by scheme; anything without a readable service, namespace and port (a
    raw IP, a bare hostname, a port-less `tcp://`) is None and renders in the page's
    "Also exposed" section instead of on a line.

    **Only a Kubernetes Service host form counts**: `<svc>.<ns>`, `<svc>.<ns>.svc` or
    `<svc>.<ns>.svc.cluster.local`. `_service_from_uri` reads the first two labels of
    ANY host, which is fine for a best-effort entity join but wrong here twice over:
    `https://api.acme-internal.example.com:8443` would draw a line for a Service that
    does not exist, and — since `target` is sent for apps the caller cannot reach — would
    hand that caller two labels and the port of another company's private hostname.
    """
    service, namespace = _service_from_uri(uri)
    if not service:
        return None
    try:
        parts = urlsplit(uri if "//" in uri else f"//{uri}")
        port = parts.port
        labels = (parts.hostname or "").split(".")
    except ValueError:
        return None
    if not (len(labels) == 2
            or labels[2:] == ["svc"]
            or labels[2:] == ["svc", "cluster", "local"]):
        return None
    if port is None:
        port = _DEFAULT_PORTS.get((parts.scheme or "").lower())
    if port is None:
        return None
    return {"namespace": namespace, "service": service, "port": port}


def _match_entity(uri: str, entity_names: set[str]) -> str:
    """Which entity does an exposed app belong to? Match on the URI, not the name.

    The app *name* is free text a human typed at `expose` time; the *URI* points
    at the Kubernetes Service the Helm release actually created, and Helm names
    resources after the release. Verified against `cube-66odzn95`, where matching
    on the app name gets 4 of 5 right and matching on the URI gets 5 of 5:

        app name        uri service.namespace                    entity
        litellm         litellm.esai-sovereign-ai                esai-sovereign-ai-litellm   rule 2
        rtsp-camera     esai-data-services-rtsp-camera.default   (same)                      rule 1
        minio-console   esai-data-services-minio-console.default esai-data-services-minio    rule 3
        mov-sqlpad      sqlpad.mov-core                          sqlpad                      rule 1
        mov-dashboard   esai-ludvika-mov-dashboard.mov-apps      (same)                      rule 1

    `minio-console` is why name matching cannot work — the label shares no suffix
    with `esai-data-services-minio` — and `mov-sqlpad` is why it would need to
    match in both directions even to reach 4/5.

    Returns "" when no rule fires. An unmatched app is surfaced separately rather
    than dropped, so its URL is never lost to a heuristic that missed.
    """
    service, namespace = _service_from_uri(uri)
    if not service:
        return ""
    return _match_by_resource(service, namespace, entity_names)


def _match_by_resource(name: str, namespace: str, entity_names: set[str]) -> str:
    """Attribute one Kubernetes resource to the entity whose Helm release made it.

    Shared by BOTH joins — exposed Services (via `_match_entity`) and Groundcover
    workloads (via `cube_logs`) — because Helm names every resource off the release
    the same way, and the two joins were converging on identical rules. One rule set
    with two callers means the mutation coverage on these three rules covers both.

    Verified against `cube-66odzn95` in both directions. Services:

        litellm        in esai-sovereign-ai  -> esai-sovereign-ai-litellm    rule 2
        …-minio-console in default           -> esai-data-services-minio     rule 3

    Workloads:

        esai-ludvika-mov-dashboard in mov-apps          -> (same name)       rule 1
        litellm                    in esai-sovereign-ai -> esai-sovereign-ai-litellm  rule 2
        …-timescaledb-hv-postgresql in mov-hv           -> …-timescaledb-hv  rule 3

    Returns "" when no rule fires.
    """
    if not name:
        return ""
    # 1. The resource is named for the release: `sqlpad` -> entity `sqlpad`.
    if name in entity_names:
        return name
    # 2. The release lives in its own namespace and the resource drops the prefix:
    #    `litellm` in ns `esai-sovereign-ai` -> `esai-sovereign-ai-litellm`.
    composed = f"{namespace}-{name}"
    if composed in entity_names:
        return composed
    # 3. A component of a release: `…-minio-console` -> `…-minio`. Require the `-`
    #    boundary so `minio` cannot claim a `minioproxy` resource, and take the
    #    LONGEST match so `…-timescaledb-hv-postgresql` resolves to
    #    `…-timescaledb-hv` and not to `…-timescaledb`, which is also a prefix.
    #    Both timescaledb entities are real and coexist on cube-66odzn95.
    candidates = [e for e in entity_names if e and name.startswith(e + "-")]
    if candidates:
        return max(candidates, key=len)
    return ""


def _exposed_summary(app: dict, companies: AppCompanies) -> dict:
    """Serialize ONE exposed app — allowlist, same rule as `_app_summary`.

    `labels` is reduced to the app's audience (`companies`): it is an
    operator-controlled free-form map on the Teleport app, and passing it through would
    put whatever a future label carries into an HTTP response.

    An app ``companies`` cannot see keeps its name, audience and `target` and loses its
    `url` and `uri`: the cube's users may know it is exposed, to whom, and which of the
    cube's Service ports it covers — never how to reach it. See `EXPOSED_SUMMARY_FIELDS`
    for why `target` is sent regardless.

    A `tcp://` app gets NO url. The proxy behind that URL speaks HTTP/WebSocket
    only, so a link would 502 rather than reach anything — the card renders a
    non-clickable name instead. Console-created exposes are always `http://`
    (`reads._service_candidate` builds them), so this only bites an app exposed
    through the MCP tool.

    `unreadable_companies` carries the label's tokens that are not app company names
    (a live `Groundcover`): a role matching one can reach the app, so dropping them made
    it read as visible to nobody -- the same contract `list_exposed` keeps. They are
    shown, and never offered as something the console can add or remove.
    """
    from cube_cloud.tools.expose import _unreadable_tokens  # local: tools imports console-free

    name = app.get("name") or ""
    uri = app.get("uri") or ""
    label = (app.get("labels") or {}).get("company")
    reachable = companies.can_see(label)
    return {
        "name": name,
        "url": _proxy_url(name) if reachable and is_http_app(uri) else "",
        "uri": uri if reachable else "",
        "companies": sorted(label_companies(label)),
        "unreadable_companies": _unreadable_tokens(label),
        "reachable": reachable,
        "target": _target_from_uri(uri),
    }


# The entity that actually serves exposed apps. Removing an app from the module's
# `apps` variable is a DECLARED-state change; this Helm release is what has to roll
# out before the app stops answering, so its plan/rollout status is the real signal.
#
# **Do not use the module installation's `state` for this.** `LIST_MODULES` reports
# `Installed` — the installation state — and never moves during a rollout. The
# `UpdateRequested` that looks like a rollout signal comes from the *mutation
# response* (`updateModuleInstallationV2`), which acknowledges the request and is not
# queryable afterward. An earlier revision keyed off it and was therefore inert: the
# UI reported every removal as complete immediately.
#
# **Measured on `cube-66odzn95`:** the legacy release rolled out in 1m 12s – 1m 23s;
# the module's took 2m 10s – 3m 1s to return to NoWork (2026-10-20), and the app kept
# answering for ~2m 27s after an unexpose. So the window in which a "removed" app is
# still answering is minutes, not a moment, which is why this is worth reporting and
# why the poll budget is minutes rather than seconds.
#
# **A settled read is only an answer once the poll has seen the plan in flight.**
# Apollo starts the plan 28–55s after the module write, and until then this entity
# reads NoWork/UP_TO_DATE — the state from BEFORE the change. `rollout_of` cannot tell
# the two apart (it has no write time), so the client does: `CubePage.awaitRollout`
# accepts settled only after an unsettled read. `rolloutStatus`/`configStatus` stayed
# UP_TO_DATE through every rollout measured, and `healthStatus` read ACTIVE_PLAN at
# rest, so none of them closes that window.
#
# **Two products, and the console's own path only ever meets the second.** A legacy,
# hand-managed cube runs `com.teleport:teleport-app-service`; a cube on
# `teleport-multi-app-service-module` (the only kind the console can expose on) runs
# `com.edgescaleai-cube:esai-teleport-app-service`. Matching the legacy id alone found no
# row on any module-managed cube, so every console unexpose ended in "has not confirmed
# the rollout" (verified 2026-10-20 on `cube-66odzn95` and `cube-9likqvpd`, both
# `NoWork`/`UP_TO_DATE` at the time). The pair is `tools/environments.py`'s
# `TELEPORT_APP_SERVICE_PRODUCTS`, imported above, so the config-withholding rule and
# this one cannot disagree about which entity serves exposed apps.

# `planStatus` NoWork + `rolloutStatus` UP_TO_DATE together mean "nothing in flight".
# Anything else — an active plan, a recall, a grace period, a value we have not seen —
# is reported UNSETTLED, because claiming an app is unreachable on an unrecognized
# status asserts the one thing this check exists to avoid.
_PLAN_SETTLED = "NoWork"
_ROLLOUT_SETTLED_STATUS = "UP_TO_DATE"


# What one read of the app-service entity says, and the only thing the client may
# branch on. Four values because `settled: false` alone was two different facts, and
# the client's "seen in flight" guard armed on both: a read that could not see the
# entity (a null `environmentById`, a partial-error payload, a truncated page, an
# entity whose status fields are empty) is not evidence that a rollout STARTED, and
# treating it as such let a following stale settled read print "Rollout complete".
#
#   in_flight  the row was read and a plan is running or the rollout is not up to date
#   settled    the row was read at NoWork + UP_TO_DATE
#   unknown    we could not tell: the read was incomplete, or a status field was empty
#   absent     the entity page was read COMPLETELY and carries no app-service row,
#              which is what a teardown (the last app on a cube) leaves once Apollo
#              drops the uninstalled entity. Whether Apollo drops it before or after the
#              uninstall finishes is not verified, so `absent` is never a completion
#              signal; the client says the cube's app-exposure service is being removed.
ROLLOUT_IN_FLIGHT = "in_flight"
ROLLOUT_SETTLED = "settled"
ROLLOUT_UNKNOWN = "unknown"
ROLLOUT_ABSENT = "absent"


class RolloutRead(NamedTuple):
    label: str
    settled: bool
    phase: str


def rollout_of(entities: list[dict], *, complete: bool = True) -> RolloutRead:
    """What the Teleport app-service entity's status says about a rollout.

    `entities` are `_app_summary` rows; `complete` says whether they are the whole
    entity page (the environment resolved, the page was present and not truncated).
    `settled` is True only for the `settled` phase, so unknown is never reported as
    settled. A cube carrying both products (not observed, but not ruled out
    mid-migration) is settled only when every one of them is, and the label is the first one still in flight: which of the two
    serves the removed app is not something this read can tell. Any row we cannot read
    makes the whole read `unknown`, never `in_flight`.
    """
    rows = [e for e in entities if e.get("product_id") in TELEPORT_APP_SERVICE_PRODUCTS]
    if not rows:
        return RolloutRead("", False, ROLLOUT_ABSENT if complete else ROLLOUT_UNKNOWN)
    states = []
    for row in rows:
        plan = row.get("plan_state") or ""
        rollout = row.get("rollout") or ""
        if not plan or not rollout:
            return RolloutRead(plan or rollout, False, ROLLOUT_UNKNOWN)
        settled = plan == _PLAN_SETTLED and rollout == _ROLLOUT_SETTLED_STATUS
        states.append((plan if plan != _PLAN_SETTLED else rollout, settled))
    label, settled = next((s for s in states if not s[1]), states[0])
    return RolloutRead(label, settled, ROLLOUT_SETTLED if settled else ROLLOUT_IN_FLIGHT)


async def _exposed_apps(client: ApolloClient, profile: str, env_id: str) -> list[dict]:
    """Exposed apps, with a failed read flattened to `[]`.

    Only for callers that DEGRADE on failure — `cube_apps` drops the URLs off the
    cards and renders the page anyway. Any caller that draws a *conclusion* from
    absence must use `_exposed_apps_read` instead, because `[]` here conflates
    "nothing is exposed" with "the read failed". Confirming an unexpose off this
    function reported success for writes that never happened.
    """
    apps, _ok = await _exposed_apps_read(client, profile, env_id)
    return apps


async def _exposed_apps_read(
    client: ApolloClient, profile: str, env_id: str
) -> tuple[list[dict], bool]:
    """Exposed apps on one cube -> `(summaries, read_succeeded)`. See `_exposed_records`."""
    records, ok = await _exposed_records(client, profile, env_id)
    return [summary for summary, _uri in records], ok


async def _exposed_records(
    client: ApolloClient, profile: str, env_id: str
) -> tuple[list[tuple[dict, str]], bool]:
    """Exposed apps on one cube -> `([(summary, join_uri)], read_succeeded)`.

    ``join_uri`` is the app's in-cluster target, kept ONLY so `_attach_exposed` can put
    an app the caller cannot reach on its entity row; it never leaves the server (the
    summary already blanks `uri` for such an app). On a "map" stack only apps the caller
    can reach are returned, as before; on a "stored" stack every app is, with its
    audience.

    The caller-VISIBLE view. Anything deciding whether a NAME is free must use
    `_exposed_names_read` instead — see the warning on that function.

    **The boolean is the whole point.** Three outcomes have to stay distinguishable:

      * `([...], True)`  — apps are exposed
      * `([], True)`     — the read worked and NOTHING is exposed. Legitimate and
                           common: the Teleport module is absent until something is
                           exposed, and the last `unexpose` tears it back down.
      * `([], False)`    — the read FAILED. A corrupt `apps` variable (which really
                           happened on `cube-66odzn95`), an unresolvable company, or
                           any Apollo error.

    Collapsing the last two is how a confirmation could report an unexposed app as
    gone when no mutation had been issued at all.

    Reads the same Teleport multi-app module variable `expose`/`unexpose`/
    `list_exposed` manage, via the tools' Apollo helpers — one extra GraphQL
    query, no Teleport or kubectl on this path.

    **Never raises.** This decorates a card; a cube with no Teleport module
    installed (entirely normal — nothing has been exposed there) and an Apollo
    hiccup both have to leave the app list intact rather than fail the page.

    **Never logs the Apollo error text, only its class.** `LIST_MODULES` selects
    *every* module's variable values, and a module variable can hold a secret
    (`update_module_variables` writes them). Rule 3 in AGENTS.md — exclude
    structurally, don't redact — cannot be satisfied by a leaner query here:
    `moduleInstallations`/`variables` take no filter args, so narrowing to the one
    module and the one `apps` variable is not expressible. The containment is
    therefore at both exits instead:

      * to the client — `_exposed_summary` copies seven named keys, so no other
        module's variables reach the response;
      * to the logs — `ApolloError` embeds the raw GraphQL response body in its
        message, so `exc_info`/`%s` on the exception would put another module's
        secret in CloudWatch. Only `type(e).__name__` is recorded. Diagnose a real
        failure through the `list_modules` MCP tool, which is allowed to show it.
    """
    from cube_cloud.tools import expose as expose_tool
    from cube_cloud.tools import modules as modules_tool

    try:
        installations = await modules_tool._fetch_module_installations(client, env_id)
        module = modules_tool._find_module_by_coordinate(
            installations, expose_tool.TELEPORT_MULTI_APP_SERVICE_MODULE
        )
        if module is None:
            # A successful read of "nothing is exposed here" — not a failure. The
            # module only exists once something has been exposed.
            return [], True
        apps, load_err = expose_tool._load_apps(module)
        if load_err or apps is None:
            # `load_err` may quote the raw variable, and that is fine *here* where
            # the exception text is not: it is the Teleport module's `apps` variable
            # specifically — names, URIs, addresses, which `list_exposed` already
            # prints — not an arbitrary module's variables.
            logger.warning(
                "console could not read exposed apps for env %s: %s", env_id, load_err
            )
            return [], False

        # Same tenancy rule as `list_exposed`: on a "map" stack a scoped caller never
        # sees another company's app at all; on a "stored" stack it sees the name and
        # audience only (`_exposed_summary`).
        companies = app_companies(profile)
        if companies is None:
            logger.warning("console skipping exposed apps for profile=%s: app companies unresolvable", profile)
            return [], False
        if not reads_stored_sets():
            apps = [a for a in apps if companies.can_see((a.get("labels") or {}).get("company"))]
        return [(_exposed_summary(a, companies), a.get("uri") or "") for a in apps], True
    except Exception as e:
        # Class name ONLY — never the message, never exc_info. See the docstring:
        # an ApolloError's text is the raw response body for a query that selected
        # every module's variables.
        logger.warning(
            "console exposed-apps read failed for env %s (%s) — app cards will "
            "omit URLs; use the list_modules tool to see the underlying error.",
            env_id, type(e).__name__,
        )
        return [], False


async def _same_target(
    client: ApolloClient, env_id: str, name: str, uri: str,
) -> tuple[bool, bool]:
    """Does the existing app ``name`` point at ``uri``? -> `(same, read_succeeded)`.

    Crosses the company boundary like `_exposed_names_read`, and for the same kind of
    reason: whether a console expose may JOIN an app it cannot see depends on the
    target, and only this boolean leaves the server -- never the other app's URI.
    """
    from cube_cloud.tools import expose as expose_tool
    from cube_cloud.tools import modules as modules_tool

    try:
        installations = await modules_tool._fetch_module_installations(client, env_id)
        module = modules_tool._find_module_by_coordinate(
            installations, expose_tool.TELEPORT_MULTI_APP_SERVICE_MODULE
        )
        if module is None:
            return False, True
        apps, load_err = expose_tool._load_apps(module)
        if load_err or apps is None:
            return False, False
        entry = next((a for a in apps if (a.get("name") or "") == name), None)
        return entry is not None and (entry.get("uri") or "") == uri, True
    except Exception as e:
        logger.warning("console same-target read failed for env %s (%s)", env_id, type(e).__name__)
        return False, False


async def _exposed_names_read(
    client: ApolloClient, env_id: str
) -> tuple[set[str], bool]:
    """EVERY exposed app name on the cube -> `(names, read_succeeded)`. Unfiltered.

    **This is the one read that deliberately crosses the company boundary, and its
    result must never be returned to a caller.** It answers exactly one question —
    "is this name already taken on this cube" — and only a boolean derived from it
    may leave the server.

    Why it has to exist. `expose`'s `_merge_app` upserts by `name` alone, with no
    regard for `labels.company`, so publishing under a name another tenant already
    uses REPLACES their entry: their public hostname starts serving the new URI,
    their app vanishes from their `list_exposed`, and the label merge hands the new
    caller control of it. The `expose` tool refuses a SCOPED caller that would do that
    to an app it cannot see; on a `stored` stack it lets any company on an app
    reconfigure it, and it never refuses an unscoped admin or a caller re-exposing its
    own name -- which is why this guard still stands in front of it.

    That guard originally read `_exposed_apps_read`, which is company-FILTERED. For a
    scoped caller another tenant's app is invisible, so the guard saw an empty set and
    waved the write through — the guard was blind in precisely the case that motivates
    it. Filtering is right for *display* and wrong for *collision*, so the two reads
    are now separate functions with the difference stated in both names.

    Names only. Not URIs, addresses, or labels — a collision check needs nothing else,
    and the narrower return is what keeps a future caller from casually rendering it.
    """
    from cube_cloud.tools import expose as expose_tool
    from cube_cloud.tools import modules as modules_tool

    try:
        installations = await modules_tool._fetch_module_installations(client, env_id)
        module = modules_tool._find_module_by_coordinate(
            installations, expose_tool.TELEPORT_MULTI_APP_SERVICE_MODULE
        )
        if module is None:
            return set(), True
        apps, load_err = expose_tool._load_apps(module)
        if load_err or apps is None:
            logger.warning(
                "console could not read exposed names for env %s: %s", env_id, load_err
            )
            return set(), False
        return {a.get("name") or "" for a in apps}, True
    except Exception as e:
        # Class name only, same reason as `_exposed_apps_read`.
        logger.warning(
            "console exposed-names read failed for env %s (%s)", env_id, type(e).__name__
        )
        return set(), False


def _exposed_list_is_complete(profile: str) -> bool:
    """Does `_exposed_records` return every app on a cube for this caller?

    Yes on a `stored` stack (it lists every app, with audience only for the ones the
    caller cannot reach) and for an unscoped admin anywhere; no for a scoped caller on
    a `map` stack, where another company's app is dropped rather than listed. Only
    decides what the page may CLAIM — it hides nothing and authorizes nothing.
    """
    if reads_stored_sets():
        return True
    companies = app_companies(profile)
    return companies is not None and companies.unscoped


def _attach_exposed(entities: list[dict], exposed: list[tuple[dict, str]]) -> list[dict]:
    """Join exposed apps onto entity rows; return the apps that matched nothing.

    Joins on the SERVER-SIDE target (`_exposed_records`' ``join_uri``), so an app the
    caller cannot reach still lands on the row of the service it exposes without its
    target ever being serialized.
    """
    by_entity: dict[str, list[dict]] = {}
    unmatched: list[dict] = []
    names = {e["entity_name"] for e in entities if e["entity_name"]}
    for app, join_uri in exposed:
        owner = _match_entity(join_uri, names)
        if owner:
            by_entity.setdefault(owner, []).append(app)
        else:
            unmatched.append(app)
    for entity in entities:
        entity["exposed"] = sorted(
            by_entity.get(entity["entity_name"], []), key=lambda a: a["name"]
        )
    return sorted(unmatched, key=lambda a: a["name"])


async def cube_apps(client: ApolloClient, profile: str, cube: str) -> dict | None:
    """Apps + platform components on one cube, or None if the caller cannot see it.

    **Authorization is inherent, not a separate check.** The environment is resolved
    out of `_visible_environments` — already RBAC-filtered — so a cube the caller has
    no role on simply is not found, and returns None for the route to 404. There is
    no `has_access(...)` call here that a future edit could forget or reorder.

    That also avoids the MCP tools' `_resolve_environment`, which reissues
    LIST_ENVIRONMENTS + MY_TEAMS on every call; both come from the Phase 2 per-profile
    cache instead, so this view costs ONE uncached Apollo query rather than three.
    """
    envs, envs_truncated = await _visible_environments(client, profile)
    match = next((e for e in envs if (e.get("name") or "") == cube), None)
    if match is None:
        # A cube that IS the caller's but was not reached by the environment drain
        # is indistinguishable here from one they have no role on — and the page's
        # copy would blame their Apollo team roles, which is exactly the
        # misdiagnosis the cube list's truncation banner exists to prevent (OI-6,
        # issue 252). Pagination made this rarer, not impossible: `truncated` now
        # means the drain stopped early rather than "the fleet is past page 1".
        #
        # `envs_truncated` is reported so the page can say "your environment list is
        # truncated" INSTEAD of blaming RBAC. Note it is a property of the caller's
        # own list, not of any particular cube, so surfacing it does not reveal
        # whether `cube` exists — the non-enumerable 404 is preserved.
        if envs_truncated:
            logger.error(
                "cube %r not found for profile=%s, but that profile's environment "
                "list is TRUNCATED — the cube may exist on a page that is not being "
                "fetched. See OI-6 / issue 252.", cube, profile,
            )
            return {"not_found": True, "environments_truncated": True}
        return None

    # Two independent Apollo queries against the same environment — issued together
    # so the exposed-apps read costs no extra wall-clock. `_exposed_apps` never
    # raises, so `gather` needs no `return_exceptions` for it; the entities query is
    # still allowed to fail the request, since without it there is no page at all.
    #
    # Inventory is NOT read here. It is its own endpoint, fetched by the page in
    # parallel — see `cube_inventory` for why.
    cube_summary = _cube_summary(match)
    data, (exposed, exposed_ok) = await asyncio.gather(
        client.graphql(Q.CONSOLE_ENVIRONMENT_ENTITIES, {"id": match.get("id")}),
        _exposed_records(client, profile, match.get("id") or ""),
    )
    env = ((data or {}).get("apollo") or {}).get("environmentById") or {}
    page = env.get("entities") or {}
    raw = page.get("entities") or []

    saturated = len(raw) >= Q.CONSOLE_ENTITIES_PAGE_SIZE
    truncated = saturated or bool(page.get("nextPageToken"))
    if truncated:
        logger.error(
            "CONSOLE_ENVIRONMENT_ENTITIES looks truncated for %s (%d entities; page "
            "size %d): the app list is INCOMPLETE. Same class as OI-6.",
            cube, len(raw), Q.CONSOLE_ENTITIES_PAGE_SIZE,
        )

    entities = sorted((_app_summary(e) for e in raw), key=lambda a: a["name"].lower())
    exposed_unmatched = _attach_exposed(entities, exposed)
    if exposed_unmatched:
        logger.info(
            "console: %d of %d exposed apps on %s did not match an entity by URI "
            "(%s) — shown separately rather than dropped.",
            len(exposed_unmatched), len(exposed), cube,
            ", ".join(a["name"] for a in exposed_unmatched),
        )
    apps = [e for e in entities if e["kind"] == "app"]
    platform = [e for e in entities if e["kind"] == "platform"]
    # Every entity must land in exactly one bucket. A third `classify_entity` return
    # value would otherwise drop entities from both lists silently — an app vanishing
    # with no explanation, the same failure class as a truncated list.
    if len(apps) + len(platform) != len(entities):
        logger.error(
            "console classified %d entities on %s into %d apps + %d platform — some "
            "were dropped, which means classify_entity returned an unexpected kind.",
            len(entities), cube, len(apps), len(platform),
        )

    return {
        "cube": cube_summary,
        "apps": apps,
        "platform": platform,
        "exposed_unmatched": exposed_unmatched,
        "counts": {
            "apps": len(apps),
            "platform": len(platform),
            "exposed": len(exposed),
        },
        "truncated": truncated,
        # The cube page draws "Not exposed" from the ABSENCE of an app on a port, so it
        # must know whether that absence means anything (docs/console-spec.md §4.4f).
        # `exposed_available`: the exposed-apps read succeeded — `_exposed_records`'
        # `([], False)` is otherwise byte-identical to "nothing is exposed here", and a
        # corrupt `apps` variable or an unreadable app-company secret would mark every
        # live port "Not exposed" with an Expose button beside it.
        # `exposed_complete`: the list holds EVERY app on the cube. False on a `map`
        # stack for a scoped caller, where another company's app is filtered out
        # entirely, so a port it covers is not exposed only as far as this caller knows.
        "exposed_available": exposed_ok,
        "exposed_complete": exposed_ok and _exposed_list_is_complete(profile),
    }


# --- Logs for one app ------------------------------------------------------
#
# Three facts about Groundcover drove this shape, all read off the live API on
# `cube-66odzn95` rather than assumed:
#
# 1. **One entity owns several workloads.** `esai-data-services-minio` runs both
#    `esai-data-services-minio` and `esai-data-services-minio-console`;
#    `esai-ludvika-mov-dbt` runs three CronJobs. So a single `workload:<name>`
#    filter cannot cover an app, and the view issues ONE QUERY PER WORKLOAD in
#    parallel and merges by timestamp. Groundcover's syntax for OR-ing workloads
#    into one query is not documented in anything we have, and guessing a query
#    that silently matches the wrong set is worse than N small correct ones.
#
# 2. **A log row carries far more than a log line.** `container.image` (the private
#    registry path), `host.id`, `host.name`, `node_name`, `pod_uid`, `instance_uid`,
#    `series_id`, and an `is_pii` flag Groundcover sets itself. The serializer is an
#    allowlist for the same reason as everywhere else in this module — none of that
#    infrastructure fingerprinting needs to reach a browser to read a log line.
#
# 3. **`workload:<name>` matching semantics are unverified** (exact? prefix?). It is
#    used as a *narrowing* hint only; correctness comes from re-checking
#    `row["workload"]` in Python, so the result is right either way. Same discipline
#    as verifying an unexpose by re-reading rather than parsing the tool's message.

LOG_ROW_FIELDS = frozenset({
    "timestamp", "level", "message", "workload", "namespace", "container", "pod",
})

# An incremental poll passes the newest timestamp it has seen as `since`. It is
# clamped to this lookback so a stale or hand-edited value cannot turn a poll into a
# full-retention scan of the cube's logs.
LOG_MAX_LOOKBACK_MINUTES = 24 * 60

# Groundcover stamps NANOSECONDS (`…56.932044783Z`), and the client echoes that value
# back verbatim as its poll cursor. `datetime.fromisoformat` accepts only 3 or 6
# fractional digits before Python 3.11, and rejects a bare `Z` before 3.11 too — so
# the fraction is truncated to microseconds and the `Z` normalized by hand.
#
# This is not defensive future-proofing: the Docker image runs 3.12 (where the stdlib
# would cope), but `requires-python` is >=3.10 and the project venv **is** 3.10, so
# the naive parse fails in the test suite itself. Verified both ways:
#   3.10: fromisoformat("…56.932044783+00:00") -> ValueError
#   3.10: fromisoformat("…56.932044+00:00")    -> ok
_RFC3339_RE = re.compile(
    r"^(\d{4}-\d{2}-\d{2}[Tt]\d{2}:\d{2}:\d{2})(\.\d+)?([Zz]|[+-]\d{2}:\d{2})$"
)


def parse_rfc3339(raw: str) -> datetime | None:
    """An aware UTC datetime for an RFC3339 string, or None if it is not one.

    Extracted from `parse_since` so the log-timestamp readers share it rather than
    reimplementing the fraction handling, which is subtler than it looks:
    `fromisoformat` accepts only 3 or 6 fractional digits before 3.11, and
    Groundcover stamps NANOSECONDS (9). Truncating alone was not enough — 1, 2, 4 and
    5 digits still failed — so the fraction is padded to exactly 6. The container runs
    3.12 (which copes with any length) while `requires-python` is >=3.10 and the
    project venv IS 3.10, so without this dev and prod disagree on identical input.
    """
    raw = (raw or "").strip()
    m = _RFC3339_RE.match(raw)
    if not m:
        return None
    head, frac, offset = m.group(1), m.group(2) or "", m.group(3)
    if frac:
        frac = "." + (frac[1:7].ljust(6, "0"))
    offset = "+00:00" if offset in ("Z", "z") else offset
    try:
        parsed = datetime.fromisoformat(f"{head}{frac}{offset}")
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def parse_since(raw: str) -> tuple[datetime | None, str]:
    """Validate a caller-supplied `since` -> `(clamped datetime, error)`.

    Returns `(None, "")` for an absent value, meaning "use the default window".
    """
    raw = (raw or "").strip()
    if not raw:
        return None, ""
    parsed = parse_rfc3339(raw)
    if parsed is None:
        return None, "'since' must be an RFC3339 timestamp."

    now = datetime.now(timezone.utc)
    floor = now - timedelta(minutes=LOG_MAX_LOOKBACK_MINUTES)
    if parsed < floor:
        logger.info(
            "console logs: clamping 'since' from %s to the %d-minute lookback floor",
            raw, LOG_MAX_LOOKBACK_MINUTES,
        )
        return floor, ""
    # A clock-skewed client could send a future timestamp, which would make
    # Groundcover's window start after it ends and return nothing forever.
    if parsed > now:
        return now, ""
    return parsed, ""

# Groundcover streams unboundedly without a limit, and a browser cannot render an
# unbounded list either. Per-workload, so an app with 3 workloads can return 3x.
LOG_LIMIT_DEFAULT = 200
LOG_LIMIT_MAX = 1000
LOG_WINDOW_MINUTES = 60

# Ceiling on the per-workload fan-out. One browser request issues ONE Groundcover
# query per workload, and nothing bounds how many workloads an entity owns —
# `workloads_list` returns up to 1000, and rule 3 of the join attributes every
# `<entity>-` prefixed workload to it. An entity with a short name could turn a single
# poll into hundreds of concurrent POSTs, on a page that re-polls every 10s. The spec
# said "N is 1-3 in practice"; this enforces it rather than asserting it.
LOG_MAX_WORKLOADS = 12


def _log_row(row: dict) -> dict:
    """Serialize ONE log row — allowlist, not passthrough. See note 2 above.

    **`is_pii` is dropped, not honoured, and that is a deliberate choice.**
    Groundcover sets the flag itself, and the allowlist keeps the field name out of
    the response — but `message` (the row `body`) is emitted regardless, so a row
    Groundcover marked as containing PII renders with no marker. Suppressing those
    rows would silently hide log lines from an operator reading their own app's logs,
    which is worse for this audience; surfacing the flag would need UI that does not
    exist yet. Recorded here so it is a decision rather than an omission — if the
    console's audience widens beyond operators with an Apollo role on the cube, this
    is the line to revisit.

    `body` and `content` were identical on every row observed live; `body` is
    preferred and `content` is the fallback rather than emitting both.
    """
    return {
        "timestamp": row.get("timestamp") or "",
        "level": (row.get("level") or "").lower(),
        "message": row.get("body") or row.get("content") or "",
        "workload": row.get("workload") or "",
        "namespace": row.get("namespace") or "",
        "container": row.get("container_name") or "",
        "pod": row.get("pod_name") or "",
    }


async def app_workloads(gc, cube: str, entity_names: set[str]) -> dict[str, list[dict]]:
    """Map entity name -> its Groundcover workloads, via the shared join rules.

    Returns `{}` on any failure — a cube not reporting to Groundcover, or an API
    hiccup, must leave the cube page intact.
    """
    from cube_cloud.tools import groundcover as gc_tool

    try:
        resp = await gc.workloads_list(cube, LOG_LIMIT_MAX, None)
    except Exception as e:
        logger.warning(
            "console workload list failed for %s (%s) — no log links will be offered",
            cube, type(e).__name__,
        )
        return {}

    out: dict[str, list[dict]] = {}
    for w in (resp or {}).get("workloads") or []:
        name = w.get("workload") or ""
        namespace = w.get("namespace") or ""
        if not name:
            # Real rows on cube-66odzn95 have an empty workload (namespace-level Job
            # aggregates, e.g. `assisted-installer/`). They belong to no entity.
            continue
        owner = _match_by_resource(name, namespace, entity_names)
        if owner:
            out.setdefault(owner, []).append({
                "workload": name,
                "namespace": namespace,
                "kind": w.get("kind") or "",
            })
    for rows in out.values():
        rows.sort(key=lambda r: r["workload"])
    return out


async def cube_exposed(client: ApolloClient, profile: str, cube: str) -> dict | None:
    """Just the exposed apps for one cube, or None if the caller cannot see it.

    Two Apollo queries, gathered — the module read alone cannot say whether the cube has
    stopped serving a removed app, which is the whole reason this is polled.

    `rollout_settled` is used by the UNEXPOSE flow only. It says Apollo finished applying
    the Helm release — deliberately not "the app is reachable", which the console no
    longer claims for expose (spec §4.4d).
    """
    envs, _truncated = await _visible_environments(client, profile)
    match = next((e for e in envs if (e.get("name") or "") == cube), None)
    if match is None:
        return None
    env_id = match.get("id") or ""
    # Two queries, deliberately. The exposed list alone cannot say whether the cube
    # has stopped serving a removed app, and that is the whole reason this endpoint
    # is polled. Still cheaper than `cube_apps`'s consumer, which also serializes and
    # classifies every entity.
    # `_exposed_apps_read`, not the degrading `_exposed_apps`: the client concludes
    # "nothing is exposed here" from an empty list when it explains an `absent`
    # app-service entity as a teardown, so a failed module read must not look empty.
    (exposed, exposed_ok), data = await asyncio.gather(
        _exposed_apps_read(client, profile, env_id),
        client.graphql(Q.CONSOLE_ENVIRONMENT_ENTITIES, {"id": env_id}),
    )
    env = ((data or {}).get("apollo") or {}).get("environmentById")
    page = (env or {}).get("entities")
    raw = (page or {}).get("entities")
    # A null `environmentById` or entity page (both nullable, and a GraphQL partial-error
    # payload is returned as data rather than raised) is not "no app service here", and
    # neither is a truncated page. Only a complete page may report `absent`.
    truncated = raw is not None and (
        len(raw) >= Q.CONSOLE_ENTITIES_PAGE_SIZE or bool(page.get("nextPageToken"))
    )
    complete = raw is not None and not truncated
    if truncated:
        logger.error(
            "console exposed read: entity page for %s looks truncated (%d; page size "
            "%d) — the rollout signal may be unreadable. Same class as OI-6.",
            cube, len(raw), Q.CONSOLE_ENTITIES_PAGE_SIZE,
        )
    read = rollout_of([_app_summary(e) for e in raw or []], complete=complete)
    if read.phase == ROLLOUT_UNKNOWN:
        # It used to be invisible. Names only what was missing, never Apollo's text.
        logger.warning(
            "console exposed read: rollout unreadable on %s (environment %s, entity "
            "page %s, truncated %s)", cube,
            "present" if env is not None else "null",
            "present" if raw is not None else "null", truncated,
        )
    rollout_state, settled = read.label, read.settled
    return {
        "cube": cube,
        "exposed": exposed,
        "count": len(exposed),
        # The load-bearing field: the UI must not claim an app is unreachable until
        # the Teleport app-service release has finished rolling out.
        "rollout_state": rollout_state,
        "rollout_settled": settled,
        # What the client branches on. `rollout_settled` is kept, and is true only when
        # this is `settled`.
        "rollout_phase": read.phase,
        # Whether `exposed` is an answer. False when the module read failed, which
        # `_exposed_records` returns as `[]`, byte-identical to "nothing is exposed".
        # Same field, same meaning, as `cube_apps` publishes (§4.4f).
        "exposed_available": exposed_ok,
    }


# --- Fleet Apps page (docs/console-spec.md §4.22) ------------------------------
#
# Every app the caller can OPEN, across every cube. The source is the admin Teleport
# listing the browser proxy authorizes against (`tbot.list_apps`), not a per-cube
# `LIST_MODULES` fan-out: 36 of 86 live apps (every Lear and Conagra app, 2026-09-29) sit
# on legacy app services outside any multi-app module, so the module read — the cube
# page's — lists none of them.

FLEET_APP_FIELDS = frozenset({
    "name", "url", "uri", "companies", "unreadable_companies", "cube", "cube_display",
})


class _CubeIndex:
    """What placement needs from the environment read: every name, and which are visible.

    ``by_suffix`` maps a SANITIZED environment name (the form `expose._qualified_app_name`
    appends) to the raw names that sanitize to it; it is empty when the read was
    truncated, because a name missing from the list could make another one look unique.
    """

    def __init__(self, envs: list[dict], truncated: bool, teams: set[str]) -> None:
        from cube_cloud.tools.expose import _sanitize_label  # local: tools imports console-free

        self.names = {e.get("name") or "" for e in envs} - {""}
        self.visible = {
            e["name"]: e for e in envs if e.get("name") and has_environment_access(e, teams)
        }
        self.by_suffix: dict[str, set[str]] = {}
        if not truncated:
            for name in self.names:
                key = _sanitize_label(name)
                if key:
                    self.by_suffix.setdefault(key, set()).add(name)

    def place(self, app_name: str, cube_label: object) -> str:
        """The environment ``app_name`` runs on, or "" when that cannot be decided.

        The server-stamped `cube` label wins when it names a known environment. A label
        naming an UNKNOWN one places nothing, rather than falling back to the name: a
        weaker key agreeing does not repair a contradictory strong one (the inventory
        join's rule). With no label, the app is placed on the one environment whose
        sanitized name is a `-`-delimited suffix of the app name; two candidates, or
        two environments sanitizing to one name, are ambiguous and place nothing.
        """
        if cube_label:
            return cube_label if isinstance(cube_label, str) and cube_label in self.names else ""
        parts = app_name.split("-")
        hits: set[str] = set()
        for i in range(1, len(parts)):
            hits |= self.by_suffix.get("-".join(parts[i:]), set())
        return next(iter(hits)) if len(hits) == 1 else ""


def _fleet_app(app: dict, index: _CubeIndex | None, companies: AppCompanies) -> dict:
    """Serialize ONE reachable app — an allowlist, like `_exposed_summary`.

    Only ever called on an app the caller can open, so `url` and `uri` are always
    filled (`url` is "" for `tcp://`, which the browser proxy does not serve). The
    Teleport label map never passes through: `company` becomes the audience, `cube`
    becomes a placement, and every other label (`app-type`, `teleport.dev/origin`, and
    whatever an operator adds next) stays on the server. `cube` and `cube_display` are
    "" unless the app is placed on a cube the caller can see, so a reachable app on a
    cube outside the caller's Apollo scope does not name that cube.

    **A scoped caller is told only about the companies it holds** (decided 2026-09-29):
    `companies` is the app's audience intersected with the caller's set, and
    `unreadable_companies` is empty, since a token that is not an app company name is
    never one the caller holds. The page groups by company, so this is what keeps a
    group for another company off a customer's screen; the cube page remains the one
    place a cube's users see an app's whole audience. An unscoped admin gets it all.
    """
    from cube_cloud.tools.expose import _unreadable_tokens  # local: tools imports console-free

    name = app.get("name") or ""
    uri = app.get("uri") or ""
    labels = app.get("labels") or {}
    label = labels.get("company")
    audience = label_companies(label)
    placed = index.place(name, labels.get("cube")) if index is not None else ""
    env = index.visible.get(placed) if (index is not None and placed) else None
    return {
        "name": name,
        "url": _proxy_url(name) if is_http_app(uri) else "",
        "uri": uri,
        "companies": sorted(audience if companies.unscoped else audience & companies.held),
        "unreadable_companies": _unreadable_tokens(label) if companies.unscoped else [],
        "cube": placed if env is not None else "",
        "cube_display": _display_name(env) if env is not None else "",
    }


async def fleet_apps(client: ApolloClient, profile: str) -> dict:
    """Every app the caller can open, fleet-wide -> `{available, cubes_available, apps}`.

    **Authorization comes first and is the one predicate.** The caller's app companies
    are resolved before Teleport is asked anything, and an unresolvable set (`None`)
    answers `available: false` without dialing it. The listing is then filtered with
    `can_see` before a single app is serialized — never by the caller's Teleport
    identity (which falls back to the shared, unscoped one when a profile has no
    per-role output) and never by Apollo cube visibility, because reachability does not
    depend on it (`browser_proxy/authz.py` checks the company alone).

    **Reachable apps only** (decided 2026-09-29): other companies' apps on the caller's
    cubes stay on the cube page and never appear in a fleet-wide list.

    Three outcomes stay distinct: `available: false` (could not look — never shown as
    "no apps"), an empty `apps` (looked; nothing the caller can open), and apps. Apollo
    only PLACES apps, so a failed environment read degrades to apps with no cube
    (`cubes_available: false`) rather than failing a page whose links work without it;
    it logs the error class only.
    """
    from cube_cloud.teleport.tbot_manager import tbot

    companies = app_companies(profile)
    if companies is None:
        logger.warning(
            "console fleet apps: app companies unresolvable for profile=%s; listing nothing",
            profile,
        )
        return {"available": False, "cubes_available": False, "apps": []}

    listing = await tbot.list_apps()
    if listing is None:
        return {"available": False, "cubes_available": False, "apps": []}
    reachable = [a for a in listing if companies.can_see((a.get("labels") or {}).get("company"))]
    if not reachable:
        return {"available": True, "cubes_available": True, "apps": []}

    index: _CubeIndex | None
    try:
        envs, truncated, teams = await _environments_and_teams(client, profile)
        index = _CubeIndex(envs, truncated, teams)
    except Exception as e:
        # Class only, the rule every console read follows for an Apollo error.
        logger.warning(
            "console fleet apps: environment read failed for profile=%s (%s); apps are "
            "listed without their cubes", profile, type(e).__name__,
        )
        index = None

    apps = [_fleet_app(a, index, companies) for a in reachable]
    apps.sort(key=lambda a: (a["cube"] == "", a["cube"], a["name"]))
    return {"available": True, "cubes_available": index is not None, "apps": apps}


# --- Candidate Services for expose -----------------------------------------
#
# `expose` needs an `app_uri` (`http://<svc>.<ns>.svc.cluster.local:<port>`), and an
# Apollo entity does not have one: an entity is a Helm release, the Service is a
# separate Kubernetes object. That gap is why inline expose was deferred. The answer
# is `clusters.fetch_services`, whose per-port `app_uri` is exactly what `expose`
# takes — the SAME construction the MCP tool suggests, so the two cannot drift.
#
# **This read is kubectl-backed via tbot, not Apollo.** Every other console read is
# Apollo-only and cheap; this one is not. It used to be LAZY (fetched only when the
# expose picker opened); since the cube page draws one line per Service port beneath
# each app (docs/console-spec.md §4.4f) it runs on page load instead, as its OWN
# request so it can never hold the apps list back, and it is bounded three ways to
# keep that affordable:
#
#   * cached per (profile, cube) for `console_services_cache_ttl_seconds`, BELOW the
#     visibility check, so a cache hit never answers a caller this request did not
#     authorize;
#   * a failed read is held for `SERVICES_FAILURE_TTL_SECONDS` only — long enough to
#     stop a burst of page loads on a disconnected cube each spawning kubectl, short
#     enough that a recovered cube shows its services on the next load;
#   * kubectl gets `SERVICES_KUBECTL_TIMEOUT_SECONDS` rather than its 60s default.
#
# It still degrades rather than failing the page, and "could not look" stays distinct
# from "no services". The expose WRITE path does not use this function or its cache:
# `writes.expose_app` enumerates fresh through `fetch_services`, because its URI
# allowlist is a security check and must not be answered from a 30s-old list.

SERVICES_FAILURE_TTL_SECONDS = 10.0
SERVICES_KUBECTL_TIMEOUT_SECONDS = 20.0

SERVICE_CANDIDATE_FIELDS = frozenset({"service", "namespace", "type", "ports"})


def _service_candidate(svc: dict) -> dict:
    """Serialize ONE Service — allowlist, same rule as every other read here."""
    return {
        "service": svc.get("name") or "",
        "namespace": svc.get("namespace") or "",
        "type": svc.get("type") or "",
        "ports": [
            {
                "port": p.get("port"),
                "protocol": p.get("protocol") or "",
                # Built by `fetch_services`, passed through untouched. Rebuilding it
                # here would be a second place for the port to be got wrong.
                "app_uri": p.get("app_uri") or "",
                # The tcp:// form of the same target. Without it the console can
                # only ever publish http://, so exposing an MQTT or Postgres port
                # from the browser produced an HTTP Teleport app pointed at a
                # non-HTTP service — accepted silently (http:// IS a valid
                # scheme) and surfacing much later as a dial timeout.
                "app_uri_tcp": p.get("app_uri_tcp") or "",
            }
            for p in (svc.get("ports") or [])
            # A port with no number cannot form a URI, so it is not a candidate.
            if p.get("port") is not None and p.get("app_uri")
        ],
    }


async def cube_services(
    client: ApolloClient, profile: str, cube: str
) -> dict | None:
    """Services on one cube that could be exposed, grouped by owning entity.

    `None` when the caller cannot see the cube — same non-enumerable 404 as every
    other per-cube read.

    Grouping reuses `_match_by_resource`, the same three rules that attribute an
    exposed Service and a Groundcover workload to their entity. That is deliberate:
    a Service is exactly the resource kind those rules were derived from, and the
    `…-timescaledb` / `…-timescaledb-hv` longest-prefix trap applies here too — both
    are real on `cube-66odzn95` and both own `-postgresql` Services.

    Services the join cannot attribute are returned under `unattributed` rather than
    dropped: the join is a Helm-naming convention, and an operator may well want to
    expose something it did not recognize.
    """
    envs, _truncated = await _visible_environments(client, profile)
    match = next((e for e in envs if (e.get("name") or "") == cube), None)
    if match is None:
        return None

    # CACHED FROM HERE, AND NOT ONE LINE EARLIER: the visibility check above runs on
    # every request, cache hit or not. Same structure as `cube_utilization`.
    env_id = match.get("id") or ""
    return await cache.get_or_set(
        profile,
        f"services:{cube}:{env_id}",
        lambda: _services_payload(client, profile, cube, env_id),
        ttl=settings.console_services_cache_ttl_seconds,
        ttl_for=lambda p: SERVICES_FAILURE_TTL_SECONDS if p.get("error") else float("inf"),
    )


async def _services_payload(
    client: ApolloClient, profile: str, cube: str, env_id: str
) -> dict:
    """The kubectl enumeration and entity join behind `cube_services`. Authorizes
    NOTHING — its caller has already resolved `env_id` out of the visible set."""
    from cube_cloud.tools import clusters as clusters_tool

    # The entity list comes from Apollo (cheap, cached visibility); the Service list
    # from kubectl. Gathered so the kubectl round-trip is not serialized behind it.
    data, svc_result = await asyncio.gather(
        client.graphql(Q.CONSOLE_ENVIRONMENT_ENTITIES, {"id": env_id}),
        # `resolved_name`: the caller resolved and authorized `cube` out of
        # `_visible_environments` above, so the tool's own uncached re-resolution —
        # LIST_ENVIRONMENTS drained plus MY_TEAMS, on every cache miss — is skipped.
        clusters_tool.fetch_services(
            client, cube, None, profile, timeout=SERVICES_KUBECTL_TIMEOUT_SECONDS,
            resolved_name=cube,
        ),
    )
    services, _env_name, hidden, svc_err = svc_result

    env = ((data or {}).get("apollo") or {}).get("environmentById") or {}
    raw = (env.get("entities") or {}).get("entities") or []
    entity_names = {
        (e.get("entityLocator") or {}).get("entityName") or ""
        for e in raw
    }
    entity_names.discard("")

    by_entity: dict[str, list[dict]] = {}
    unattributed: list[dict] = []
    for svc in services:
        candidate = _service_candidate(svc)
        if not candidate["ports"]:
            # Nothing addressable — a headless or port-less Service is not a
            # candidate, and offering it would produce a Teleport dial that hangs.
            continue
        owner = _match_by_resource(
            candidate["service"], candidate["namespace"], entity_names
        )
        if owner:
            by_entity.setdefault(owner, []).append(candidate)
        else:
            unattributed.append(candidate)

    for rows in by_entity.values():
        rows.sort(key=lambda c: (c["namespace"], c["service"]))
    unattributed.sort(key=lambda c: (c["namespace"], c["service"]))

    if svc_err:
        # `fetch_services` composes `error` for an MCP OPERATOR — it embeds the
        # ApolloError text (whose message is the raw GraphQL response body for a query
        # that selected every module's variable values) or raw kubectl stderr. The
        # `list_services` tool is allowed to show that, the same way `list_modules` is;
        # a browser is not, and neither is CloudWatch. So the console substitutes its
        # own message at this boundary rather than at the source, which keeps the
        # tool's output byte-identical.
        #
        # The DISTINCTION survives — "could not look" stays different from "nothing to
        # expose", which is the property the picker depends on. Only the detail is
        # dropped.
        logger.warning(
            "console services read failed for cube=%s — detail withheld; reproduce "
            "with the list_services tool to see it.", cube,
        )

    return {
        "cube": cube,
        "by_entity": by_entity,
        "unattributed": unattributed,
        # Non-empty when kubectl/tbot failed. The UI shows this instead of an empty
        # picker, because "no services" and "could not look" are different answers
        # and conflating them is the mistake that made a failed read look like a
        # successful unexpose.
        "error": SERVICES_UNAVAILABLE_MESSAGE if svc_err else "",
        "infra_hidden": hidden,
    }


def result_unknown_unavailable(cube: str, threshold: int) -> dict:
    """The "we could not look" outcome, shared by both failure exits so they agree."""
    return {
        "cube": cube, "state": "unknown", "last_seen": None, "age_seconds": None,
        "reason": "unavailable", "threshold_seconds": threshold,
        "window_minutes": None,
    }


# --- Teleport connectivity, per cube (§4.17) --------------------------------
#
# The COMPUTATION lives in `tools/teleport_status.py`, not here. Everything this file
# keeps is the console's own half: resolve the cube out of the caller's Apollo-visible
# set, then serialize an allowlist for the browser.
#
# That split is the `fetch_services` precedent (AGENTS.md), and it is what lets a
# future `teleport_status` MCP tool share the join rather than reimplement it — the
# dependency runs `console/ -> tools/` and never back, so platform knowledge left in
# this file would be unreachable from `tools/` except by inverting the layering.
#
# Authorization deliberately does NOT move: `_visible_environments` is cached per
# profile and matches exactly and case-sensitively, which is right for a browser and
# wrong for an agent (`_resolve_environment` takes RIDs and fuzzy names and is
# uncached). Sharing it would hand an MCP tool a cached authorization decision.


async def cube_teleport(
    client: ApolloClient, profile: str, cube: str
) -> dict | None:
    """Teleport connectivity for one cube, or None if the caller cannot see it.

    Returns `{cube, state, cluster, reason, heartbeat_ttl_seconds}` — see
    `tools/teleport_status.py` for what each state means and why the join key is the
    agent module's `kubeClusterName` rather than the environment name.

    **Never raises for a Teleport or module failure** — those become
    `state: "unknown"`, so the chip reports "could not look" rather than the route
    5xx'ing on decoration. An `ApolloError` from resolving the caller's visible set
    DOES propagate, because that is the authorization step rather than the signal, and
    the route answers 502 for it exactly as every other console read does.
    """
    from cube_cloud.tools import teleport_status as teleport_tool

    envs, envs_truncated = await _visible_environments(client, profile)
    match = next((e for e in envs if (e.get("name") or "") == cube), None)
    if match is None:
        if envs_truncated:
            logger.error(
                "console teleport: cube %r not found for profile=%s, but that "
                "profile's environment list is TRUNCATED (OI-6 / issue 252).",
                cube, profile,
            )
        return None

    status = await teleport_tool.fetch_teleport_status(
        client, match.get("id") or "", cube
    )

    # An explicit dict literal, NOT `dataclasses.asdict` — console rule 3's allowlist
    # discipline. A field added to `TeleportStatus` for an MCP consumer must not reach
    # the browser without an edit here, and `test_the_payload_is_an_allowlist...`
    # pins the key set.
    return {
        "cube": status.cube,
        "state": status.state,
        "cluster": status.cluster,
        "reason": status.reason,
        "heartbeat_ttl_seconds": status.heartbeat_ttl_seconds,
    }


# --- Why an app is unhealthy: its health checks (§4.21) ----------------------

APP_HEALTH_FIELDS = frozenset({
    "cube", "app", "health", "state", "checks", "containers", "passing_checks",
    "pods", "reported_at", "reported_age_seconds", "omitted", "truncated",
})
APP_HEALTH_CHECK_FIELDS = frozenset({
    "state", "check", "message", "pod", "container", "updated_age_seconds",
})
APP_HEALTH_CONTAINER_FIELDS = frozenset({
    "pod", "container", "live", "ready", "updated_age_seconds",
})


def _age_seconds(raw: str, now: datetime) -> int | None:
    """Server-computed, like `cube_status`'s: the browser's clock may be skewed."""
    from cube_cloud.tools.health_checks import parse_timestamp

    parsed = parse_timestamp(raw)
    return None if parsed is None else max(0, int((now - parsed).total_seconds()))


async def app_health(
    client: ApolloClient, profile: str, cube: str, app: str
) -> dict | None:
    """The health checks behind ONE app's status, or None if the caller cannot see it.

    Fetched when a user opens an app's status, never with the page: one Apollo read
    per app, and the list already carries the status itself.

    **Authorization is the pair every per-app read uses**, and the order matters:
    the cube comes out of `_visible_environments`, and the entity id out of THAT
    cube's entity list by exact entity name. The id is never taken from the request —
    `entityById` is fleet-wide — and `fetch_entity_health_checks` additionally
    refuses an entity whose environment is not the one resolved here. An app that is
    not on the cube is the same 404 as a cube that is not the caller's.
    """
    from cube_cloud.tools import health_checks as checks_tool

    envs, envs_truncated = await _visible_environments(client, profile)
    match = next((e for e in envs if (e.get("name") or "") == cube), None)
    if match is None:
        if envs_truncated:
            logger.error(
                "console app health: cube %r not found for profile=%s, but that "
                "profile's environment list is TRUNCATED (OI-6 / issue 252).",
                cube, profile,
            )
        return None

    env_id = match.get("id") or ""
    data = await client.graphql(Q.CONSOLE_ENVIRONMENT_ENTITIES, {"id": env_id})
    env = ((data or {}).get("apollo") or {}).get("environmentById") or {}
    raw = (env.get("entities") or {}).get("entities") or []
    matches = [
        e for e in raw
        if ((e.get("entityLocator") or {}).get("entityName") or "") == app
    ]
    if len(matches) != 1:
        if len(matches) > 1:
            logger.error(
                "console app health: %d entities on %s share entity name %r; "
                "refusing rather than picking one", len(matches), cube, app,
            )
        return None
    entity = matches[0]

    result = await checks_tool.fetch_entity_health_checks(
        client, env_id, entity.get("id") or ""
    )
    now = datetime.now(timezone.utc)

    # Explicit literals, never `dataclasses.asdict` — console rule 3. A field added
    # to the dataclass for the MCP renderer must not reach the browser without an
    # edit here; the `*_FIELDS` sets above are what the tests pin.
    return {
        "cube": cube,
        "app": app,
        "health": ((entity.get("reportedStatus") or {}).get("healthStatus")) or "",
        "state": result.state,
        "checks": [
            {
                "state": c.state, "check": c.check, "message": c.message,
                "pod": c.pod, "container": c.container,
                "updated_age_seconds": _age_seconds(c.updated, now),
            }
            for c in result.checks
        ],
        "containers": [
            {
                "pod": c.pod, "container": c.container, "live": c.live,
                "ready": c.ready, "updated_age_seconds": _age_seconds(c.updated, now),
            }
            for c in result.containers
        ],
        "passing_checks": result.passing_checks,
        "pods": result.pods,
        "reported_at": result.reported_at,
        "reported_age_seconds": _age_seconds(result.reported_at, now),
        "omitted": result.omitted,
        "truncated": result.truncated,
    }


# --- "Last changed" per app, from Apollo plan history (§4.15) ---------------
#
# The most recent SUCCESSFUL plan's `endTime`. "Last changed" is a claim about change,
# so a failed deploy does not qualify — otherwise a retrying, failing entity would
# read "changed 2 minutes ago" while nothing about it had changed.
#
# Two things about the upstream data are NOT documented anywhere and are handled
# rather than assumed.
#
# **1. Plan ordering is unknown.** Nothing in Apollo's docs states it, and this repo
# has only ever assumed newest-first — `format_plan_details` indexes `plans[0]`, and
# `cancel_active_plan` takes the first status match in array order. Those tolerate
# being wrong (one active plan; an operator-facing view with an index argument). A
# "Last changed" column does not: with oldest-first ordering every app would show its
# FIRST-EVER deploy date, and nobody would notice because there is nothing on screen
# to compare it against.
#
# Taking `max(endTime)` over the page does not fix that on its own — with oldest-first
# a full page holds the OLDEST plans, so its max is still not the newest. So the
# direction is inferred from the page (`_page_direction`) and a full page in the
# unfavourable direction reports `unknown` instead of a date. A blank cell is a much
# cheaper error than a confidently wrong one.
#
# **2. The success enum is unverified.** `apollo_models.PLAN_STATUS_ICONS` hedges
# `SUCCESSFUL` *and* `SUCCESS` (and `UNSUCCESSFUL` *and* `FAILURE`), which is a
# recorded admission that nobody knew which Apollo emits. Both spellings are accepted;
# and if NO plan matches while plans exist, the newest plan of any status is reported
# with `state="unsuccessful"` so the UI can say the last deploy did not succeed —
# rather than showing "never changed" for an entity that has been deploying all week.

# Plan status values counted as a completed, successful change. Both spellings, per
# the hedge above — guessing one would show "never changed" for the whole fleet.
PLAN_SUCCESS_TYPES = frozenset({"SUCCESSFUL", "SUCCESS", "SUCCEEDED"})


def _plan_end(plan: dict) -> datetime | None:
    """When a plan finished, or None if it has not.

    `endTime` only — a plan still running has not changed anything yet, so its
    `startTime` must not be mistaken for a completed change.
    """
    return parse_rfc3339(str(plan.get("endTime") or ""))


def _page_direction(plans: list[dict]) -> str:
    """`"newest_first"` | `"oldest_first"` | `"unknown"`, inferred from the page.

    Compares the first and last plan that carry a usable timestamp. `unknown` when
    the page is too small or too uniform to tell — which, combined with saturation,
    is what makes the caller fail safe rather than guess.
    """
    stamped = [(i, _plan_end(p)) for i, p in enumerate(plans)]
    stamped = [(i, t) for i, t in stamped if t is not None]
    if len(stamped) < 2:
        return "unknown"
    first, last = stamped[0][1], stamped[-1][1]
    if first > last:
        return "newest_first"
    if first < last:
        return "oldest_first"
    return "unknown"


def _last_change_for(plans: list[dict]) -> dict:
    """`{last_changed, age_seconds, state}` for one entity's plan page.

    `state` is one of:
      * `changed`      — a successful plan; `last_changed` is its end time
      * `unsuccessful` — plans exist, none succeeded; the newest end time is reported
      * `none`         — no completed plans at all (a freshly installed entity)
      * `unknown`      — the page may not contain the newest plan (see note 1)
    """
    def out(state: str, when: datetime | None = None) -> dict:
        if when is None:
            return {"last_changed": None, "age_seconds": None, "state": state}
        age = max(0, int((datetime.now(timezone.utc) - when).total_seconds()))
        return {
            "last_changed": when.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "age_seconds": age,
            "state": state,
        }

    if not plans:
        return out("none")

    saturated = len(plans) >= Q.CONSOLE_PLANS_PAGE_SIZE
    direction = _page_direction(plans)
    if saturated and direction != "newest_first":
        # A full page that is not demonstrably newest-first may be hiding newer
        # plans. Report nothing rather than a date we cannot stand behind.
        logger.info(
            "console changes: a full plan page (%d) with direction=%s — reporting "
            "unknown rather than a possibly-stale date.",
            len(plans), direction,
        )
        return out("unknown")

    finished = [(p, t) for p in plans if (t := _plan_end(p)) is not None]
    if not finished:
        return out("none")

    successful = [
        t for p, t in finished
        if str((p.get("status") or {}).get("type") or "").upper() in PLAN_SUCCESS_TYPES
    ]
    if successful:
        return out("changed", max(successful))

    # Plans ran and none succeeded. Reporting `none` here would read as "never
    # deployed" for an entity that has been failing to deploy repeatedly.
    return out("unsuccessful", max(t for _p, t in finished))


async def cube_changes(
    client: ApolloClient, profile: str, cube: str
) -> dict | None:
    """`{cube, changes: {entity_name: {...}}, truncated}` or None if not visible.

    Its own read rather than a field on `cube_apps`, so the plan query cannot delay
    the apps list — the same reasoning as the inventory and status endpoints, and it
    additionally leaves `CONSOLE_ENVIRONMENT_ENTITIES`'s deliberate omission of
    `nonGenericPlans` intact.

    Authorization is inherent: the environment is resolved out of the already
    RBAC-filtered `_visible_environments`, so a caller can only ever cause a plan read
    for a cube they can already see.
    """
    envs, envs_truncated = await _visible_environments(client, profile)
    match = next((e for e in envs if (e.get("name") or "") == cube), None)
    if match is None:
        if envs_truncated:
            return {"not_found": True, "environments_truncated": True}
        return None

    data = await client.graphql(Q.CONSOLE_ENTITY_PLANS, {"id": match.get("id")})
    env = ((data or {}).get("apollo") or {}).get("environmentById") or {}
    page = env.get("entities") or {}
    raw = page.get("entities") or []

    # Same saturation signal as the apps list, for the same reason: a short entity
    # list with no explanation reads as "this app has no history" rather than "we did
    # not fetch it".
    truncated = len(raw) >= Q.CONSOLE_ENTITIES_PAGE_SIZE or bool(page.get("nextPageToken"))
    if truncated:
        logger.error(
            "console changes: entity list looks truncated for %s (%d entities) — "
            "some apps will have no Last changed value. Same class as OI-6.",
            cube, len(raw),
        )

    changes: dict[str, dict] = {}
    for entity in raw:
        name = ((entity.get("entityLocator") or {}).get("entityName") or "").strip()
        if not name:
            continue
        plans = ((entity.get("nonGenericPlans") or {}).get("plans")) or []
        changes[name] = _last_change_for(plans)

    return {"cube": cube, "changes": changes, "truncated": truncated}


# --- Cube online/offline status (from Groundcover log freshness) -----------
#
# The signal is **the timestamp of the most recent log Groundcover holds for the
# cube**. Chosen over the alternatives after tracing each one:
#
#   * Apollo `reportedStatus.healthStatus` carries NO timestamp, so a cube whose
#     agent died an hour ago still reads `HEALTHY` — it reports the last KNOWN state,
#     not contact. docs/console-spec.md already records a live case where an entity
#     read `HEALTHY` while nothing answered, and warns that it "is not evidence of
#     readiness". A badge built on it would be confidently wrong.
#   * Apollo plan/task timestamps are real, but only advance when there is a plan to
#     run — so a stable cube with nothing to deploy would age into "offline"
#     precisely because it is healthy.
#   * Groundcover's `clusters/list` presence is binary, and whether a silent cluster
#     ever ages out of that list is unverified, so its time constant is unknown.
#
# **What this measures, stated plainly so the UI copy can be honest:** that the
# cube's Groundcover agent had network egress to Groundcover recently enough to ship
# a log line. That is a strong "the cube is alive" signal and NOT a statement that
# Apollo can deploy to it, nor that any particular app is serving.
#
# **The known weakness** is a cube that is up but silent: nothing guarantees a
# workload logs on any schedule, so a genuinely-idle cube could read offline. In
# practice Groundcover's own agent pods log, so a cube reporting at all rarely goes
# fully quiet — but this is why the threshold is generous and configurable rather
# than a tight liveness probe, and why "offline" copy says what was observed rather
# than asserting the cube is down.

# Windows searched, narrowest first, stopping at the first one with any rows. A
# ladder rather than one wide window because the reported age can only be as precise
# as the window that produced it: finding a row in the 5-minute window bounds the age
# at 5 minutes, whereas one 48-hour query could report a cube that logged 20 seconds
# ago as "last seen 40 hours ago" if the API returned an arbitrary subset.
STATUS_WINDOWS_MINUTES = (5, 30, 120, 720, 2880)

# Rows fetched per window. Only the MAX timestamp is used, so this is about the
# chance of catching the true newest row within a window, not about volume.
STATUS_LOG_LIMIT = 50


async def cube_status(
    client: ApolloClient, registry, profile: str, cube: str
) -> dict | None:
    """Online/offline/unknown for one cube, or None if the caller cannot see it.

    Returns `{cube, state, last_seen, age_seconds, reason, threshold_seconds,
    window_minutes}`.

    `state` is `online` | `offline` | `unknown`, and **`unknown` is a first-class
    outcome, never folded into `offline`**. A false "offline" on a working cube is
    worse than no badge: it is a confident claim the customer can disprove by using
    their app, and it costs the badge its credibility everywhere else. So a cube that
    Groundcover has never heard of, or a failed query, reports unknown.

    Authorization mirrors `cube_logs` exactly — Apollo visibility AND
    `groundcover._authorize` — because the Groundcover key is workspace-scoped and
    sees the whole fleet, so that second check is the tenancy boundary for
    Groundcover and must not be forked.
    """
    from cube_cloud.tools import groundcover as gc_tool

    envs, envs_truncated = await _visible_environments(client, profile)
    match = next((e for e in envs if (e.get("name") or "") == cube), None)
    if match is None:
        if envs_truncated:
            logger.error(
                "console status: cube %r not found for profile=%s, but that "
                "profile's environment list is TRUNCATED (OI-6 / issue 252).",
                cube, profile,
            )
        return None

    ok, _msg = await gc_tool._authorize(client, cube)
    if not ok:
        logger.warning(
            "console status: groundcover authorization refused cube=%s profile=%s "
            "even though Apollo visibility allowed it", cube, profile,
        )
        return None

    threshold = max(1, int(settings.console_cube_online_threshold_seconds))

    # `registry is None` means the stack has no Groundcover credentials — a supported
    # deployment. It is handled HERE, after both authorization checks, rather than by
    # the route returning early: a cube the caller cannot see must 404 whether or not
    # Groundcover is configured, so the resolve has to happen either way.
    if registry is None:
        return result_unknown_unavailable(cube, threshold)

    # The registry's cached cube -> backend index is what distinguishes a cube
    # Groundcover has never heard of from one that reports and has simply gone quiet.
    # `resolve_backend` returns None for a cube absent from every backend's cluster
    # list, and routing is also why it is needed: our fleet spans two backends and a
    # per-cube query must go to the one that actually holds that cube.
    try:
        backend_id = await registry.resolve_backend(cube)
    except Exception as e:
        logger.warning(
            "console status: could not resolve a Groundcover backend for %s (%s)",
            cube, type(e).__name__,
        )
        return result_unknown_unavailable(cube, threshold)

    if not backend_id:
        # Not in any backend's cluster list. Judging this cube is not possible, and
        # guessing "offline" would be a claim about a cube we have no telemetry for.
        return {
            "cube": cube, "state": "unknown", "last_seen": None, "age_seconds": None,
            "reason": "not_reporting", "threshold_seconds": threshold,
            "window_minutes": None,
        }

    gc = registry.clients[backend_id]

    def result(state: str, last_seen=None, age=None, reason="", window=None) -> dict:
        return {
            "cube": cube,
            "state": state,
            "last_seen": last_seen,
            "age_seconds": age,
            "reason": reason,
            "threshold_seconds": threshold,
            # Which window produced `last_seen`, so the client can say how tightly
            # the age is bounded instead of implying second-level precision.
            "window_minutes": window,
        }

    now = datetime.now(timezone.utc)
    newest: datetime | None = None
    found_window: int | None = None

    for minutes in STATUS_WINDOWS_MINUTES:
        start = gc_tool._rfc3339(now - timedelta(minutes=minutes))
        end = gc_tool._rfc3339(now)
        # The limit is appended HERE rather than through `_bounded_query`, which
        # skips it whenever the substring "limit" appears anywhere in the query. That
        # is fine for a hand-written query and wrong for a generated one — see the
        # same note in `cube_logs`. An unbounded Groundcover search hangs the
        # connection.
        query = f"* | limit {STATUS_LOG_LIMIT}"
        try:
            resp = await gc.logs_search(cube, start, end, query)
        except Exception as e:
            # Type only: a Groundcover error body can carry log content, which is
            # another tenant's data on a shared-workspace key.
            logger.warning(
                "console status: log query failed for %s (%s)", cube, type(e).__name__
            )
            return result_unknown_unavailable(cube, threshold)

        rows = resp if isinstance(resp, list) else (resp or {}).get("logs") or []
        stamps = [
            parsed
            for parsed in (parse_rfc3339(str(r.get("timestamp") or "")) for r in rows
                           if isinstance(r, dict))
            if parsed is not None
        ]
        if stamps:
            newest = max(stamps)
            found_window = minutes
            break

    if newest is None:
        # The cube IS in Groundcover's cluster list (checked above) but has shipped
        # no log line in the widest window. That is a real observation, so it is
        # reported as offline rather than unknown — but with no `last_seen`, because
        # we have no timestamp to show and inventing one would be worse than the gap.
        return result("offline", reason="no_recent_logs",
                     window=STATUS_WINDOWS_MINUTES[-1])

    # A clock difference between Groundcover and this process can put the newest log
    # marginally in the future; clamp rather than render a negative age.
    age = max(0, int((now - newest).total_seconds()))
    state = "online" if age <= threshold else "offline"
    return result(
        state,
        last_seen=gc_tool._rfc3339(newest),
        age=age,
        reason="" if state == "online" else "stale_logs",
        window=found_window,
    )


async def cube_logs(
    client: ApolloClient,
    gc,
    profile: str,
    cube: str,
    app: str,
    limit: int = LOG_LIMIT_DEFAULT,
    since: datetime | None = None,
) -> dict | None:
    """Recent logs for one app on one cube, or None if the caller cannot see it.

    **Two independent authorization checks, deliberately.** The cube must be in the
    caller's Apollo-visible set (as everywhere else in this module) AND
    `groundcover._authorize` must pass. The second is not redundant: the Groundcover
    API key is workspace-scoped and sees the whole fleet, so that check is the
    tenancy boundary for Groundcover specifically, and reusing it means the boundary
    is not forked. Both resolve from `auth/apollo_rbac.py`.
    """
    from cube_cloud.tools import groundcover as gc_tool

    envs, envs_truncated = await _visible_environments(client, profile)
    match = next((e for e in envs if (e.get("name") or "") == cube), None)
    if match is None:
        if envs_truncated:
            logger.error(
                "console logs: cube %r not found for profile=%s, but that profile's "
                "environment list is TRUNCATED (OI-6 / issue 252).", cube, profile,
            )
        return None

    ok, _msg = await gc_tool._authorize(client, cube)
    if not ok:
        # Same 404 as an invisible cube — the message is dropped rather than
        # returned, because it enumerates the caller's authorized cubes.
        logger.warning(
            "console logs: groundcover authorization refused cube=%s profile=%s "
            "even though Apollo visibility allowed it", cube, profile,
        )
        return None

    data = await client.graphql(
        Q.CONSOLE_ENVIRONMENT_ENTITIES, {"id": match.get("id")}
    )
    env = ((data or {}).get("apollo") or {}).get("environmentById") or {}
    raw = (env.get("entities") or {}).get("entities") or []
    entities = [_app_summary(e) for e in raw]
    names = {e["entity_name"] for e in entities if e["entity_name"]}
    if app not in names:
        # An app that is not on this cube is the same 404 as a cube that is not
        # the caller's — nothing here confirms what exists.
        return None

    by_entity = await app_workloads(gc, cube, names)
    workloads = by_entity.get(app, [])
    if not workloads:
        return {
            "cube": cube, "app": app, "workloads": [], "rows": [],
            "truncated": False, "no_workloads": True,
            "incremental": since is not None,
        }

    queried = workloads[:LOG_MAX_WORKLOADS]
    workloads_dropped = len(workloads) - len(queried)
    if workloads_dropped:
        logger.warning(
            "console logs: %s on %s owns %d workloads; querying the first %d only",
            app, cube, len(workloads), LOG_MAX_WORKLOADS,
        )

    bounded = max(1, min(int(limit), LOG_LIMIT_MAX))
    # An incremental poll asks only for what is newer than what it already has, so
    # a 10s tick transfers a handful of rows instead of re-sending the whole window.
    start, end = gc_tool._time_window(
        gc_tool._rfc3339(since) if since else None, None, LOG_WINDOW_MINUTES
    )

    # Each entry is (kept rows, whether Groundcover's own page looked full).
    async def one(workload: str) -> tuple[list[dict], bool]:
        # The limit is appended HERE, not via `_bounded_query`. That helper skips the
        # limit whenever the substring "limit" already appears anywhere in the query —
        # a reasonable guard for a caller-written query, and wrong for a generated
        # one: a Kubernetes workload legitimately named `rate-limiter` or `api-limits`
        # matches it, so the query went to Groundcover UNBOUNDED. Per that module,
        # an unbounded search "streams unboundedly and hangs the connection", and this
        # page re-issues it every 10s.
        q = f"workload:{workload} | limit {bounded}"
        try:
            resp = await gc.logs_search(cube, start, end, q)
        except Exception as e:
            logger.warning(
                "console logs: query failed for %s/%s (%s)",
                cube, workload, type(e).__name__,
            )
            return [], False
        rows = resp if isinstance(resp, list) else (resp or {}).get("logs") or []
        # Saturation is measured on what GROUNDCOVER returned, before the equality
        # filter below. Measuring the filtered group instead meant a genuinely full
        # page read as not-truncated as soon as one foreign row was discarded — and
        # that filter exists precisely because `workload:` may prefix-match, so the
        # expected behaviour was the thing defeating the flag.
        page_full = len(rows) >= bounded
        # See note 3: the query is a hint, this equality check is the guarantee.
        kept = [_log_row(r) for r in rows if (r.get("workload") or "") == workload]
        return kept, page_full

    results = await asyncio.gather(*(one(w["workload"]) for w in queried))
    rows = [r for group, _full in results for r in group]
    # Newest first. Groundcover timestamps are RFC3339 with nanoseconds, which sorts
    # correctly as a string only while the offset is uniform — every observed row is
    # `Z`, and a row without one sorts last rather than crashing the page.
    rows.sort(key=lambda r: r["timestamp"] or "", reverse=True)
    saturated = any(full for _group, full in results)

    # Three independent ways rows can be missing, and all three must set the flag or
    # the page silently under-reports: Groundcover's page was full, the merged buffer
    # overflowed, or the app owns more workloads than the fan-out cap allows.
    overflowed = len(rows) > LOG_LIMIT_MAX
    truncated = saturated or overflowed or bool(workloads_dropped)
    if overflowed:
        logger.warning(
            "console logs: %s on %s merged %d rows, returning %d",
            app, cube, len(rows), LOG_LIMIT_MAX,
        )

    return {
        "cube": cube,
        "app": app,
        "workloads": workloads,
        "workloads_queried": len(queried),
        "rows": rows[:LOG_LIMIT_MAX],
        "window_minutes": LOG_WINDOW_MINUTES,
        "truncated": truncated,
        # Echoed so the client polls from the window it actually got, not the one it
        # asked for — the two differ whenever `since` was clamped.
        "start": start,
        "end": end,
        "incremental": since is not None,
    }


# ---------------------------------------------------------------------------
# Cube-wide resource utilization (docs/console-spec.md §4.18)
# ---------------------------------------------------------------------------

#: Aggregations issued per panel. `count` rides along because it is what makes the
#: average falsifiable — see the module docstring in `console/utilization.py`.
UTILIZATION_AGGREGATIONS = ("avg", "max", "count")


async def _utilization_query(
    gc, cube: str, metric: str, aggregation: str, start: str, end: str, step: str
):
    """One cluster-pinned aggregated range query, or None if it could not be read.

    The PromQL goes through `groundcover._build_promql`, never a local f-string: that
    builder pins `cluster="<cube>"` and refuses a caller-supplied `cluster` label, and it
    is the cross-tenant guard for every metrics query in this codebase. Forking it here
    to save an import would fork the guard.
    """
    from cube_cloud.tools import groundcover as gc_tool

    try:
        promql = gc_tool._build_promql(metric, cube, None, aggregation, None)
        return await gc.metrics_query(promql, start, end, step)
    except Exception as e:
        # Type only, and never the exception itself: `GroundcoverError` embeds
        # `resp.text[:300]` of the upstream body in its message. The metric name and
        # aggregation are ours, so they are safe to name; the cube is already in scope.
        logger.warning(
            "console utilization: %s(%s) failed for %s (%s)",
            aggregation, metric, cube, type(e).__name__,
        )
        return None


def _utilization_panel(panel, responses: list) -> dict:
    """Three raw responses (avg, max, count) -> one panel payload."""
    from cube_cloud.console import utilization as util

    avg_raw, max_raw, count_raw = responses
    count = util.read_count(count_raw) if count_raw is not None else None

    def outcome(raw):
        # A failed request is "we could not look", exactly like an unreadable envelope.
        return (util.UNREADABLE, []) if raw is None else util.read_series(raw)

    avg_state, avg_points = outcome(avg_raw)
    max_state, max_points = outcome(max_raw)

    if util.UNREADABLE in (avg_state, max_state):
        # Both series come from one metric through one endpoint, so if either is
        # unreadable the panel cannot be trusted. "Unavailable" is the honest word and
        # it must never be rendered as "this cube does not report it".
        state = "unavailable"
    elif avg_state == util.EMPTY and max_state == util.EMPTY:
        state = "no_data"
    elif not util.has_readings(avg_points) and not util.has_readings(max_points):
        # Parsed, and samples came back, but not one of them is a number we can plot —
        # every reading was non-finite. A FOURTH state, because it is neither of its
        # neighbours: `no_data` would assert the cube does not report this metric, which
        # is exactly wrong when it reported a sample at every step; `unavailable` would
        # blame our side of a query that succeeded. Rendering it as `ok` is what leaves a
        # titled panel with an empty chart and no sentence explaining it.
        state = "no_readings"
    else:
        state = "ok"

    series: list[dict] = []
    latest = peak = None
    if state == "ok":
        for role, points in (("avg", avg_points), ("max", max_points)):
            series.append({
                "role": role,
                "name": util.series_name(panel, role, count),
                "points": [[at, value] for at, value in points],
                # The MIXED case, and the reason this is per-series rather than only a
                # panel state: one series can be entirely non-finite while the other is
                # fine (PromQL `avg` propagates a non-finite operand where `max` skips
                # it). Collapsing the panel would throw away a working "Busiest host"
                # line; saying nothing would leave the reader guessing why the line the
                # legend names is missing. The client must be TOLD, never left to infer
                # it from an empty array — same rule as every other state here.
                "has_readings": util.has_readings(points),
            })
        # Headline first, so the client renders `series[0]` as primary without having to
        # re-derive which of avg/max leads for this panel.
        series.sort(key=lambda s: 0 if s["role"] == panel.headline_role else 1)
        latest, peak = util.latest_and_peak(
            avg_points if panel.headline_role == "avg" else max_points
        )

    return {
        "key": panel.key,
        "label": panel.label,
        # 0-100, not 0-1 — verified live 2026-09-11 against all four metrics rather than
        # inferred from the `_percent` suffix (see `utilization.py`'s docstring). A metric
        # that did arrive 0-1 would render as a flat line on the axis floor and read as
        # healthy, which is why this was worth checking rather than assuming.
        "unit": "percent",
        "state": state,
        "entity_count": count,
        "entity_noun": panel.noun_one if count == 1 else panel.noun,
        "latest": latest,
        "highest_sampled": peak,
        "note": panel.note,
        "series": series,
    }


async def cube_utilization(
    client: ApolloClient, registry, profile: str, cube: str, window: str
) -> dict | None:
    """Cube-wide CPU / memory / filesystem / volume utilization, or None if unseeable.

    Authorization is the same PAIR `cube_status` and `cube_logs` use — Apollo visibility
    AND `groundcover._authorize` — because the Groundcover key is workspace-scoped and
    sees the whole fleet, so that second check is the tenancy boundary and must not be
    forked. `None` means "no such cube, as far as this caller is concerned"; the route
    turns it into the same non-enumerable 404 `cube_detail` gives.

    Never raises on a Groundcover failure: individual panels degrade to `unavailable`
    and the tab still renders.
    """
    from cube_cloud.console import utilization as util
    from cube_cloud.tools import groundcover as gc_tool

    envs, envs_truncated = await _visible_environments(client, profile)
    match = next((e for e in envs if (e.get("name") or "") == cube), None)
    if match is None:
        if envs_truncated:
            logger.error(
                "console utilization: cube %r not found for profile=%s, but that "
                "profile's environment list is TRUNCATED (OI-6 / issue 252).",
                cube, profile,
            )
        return None

    ok, _msg = await gc_tool._authorize(client, cube)
    if not ok:
        # `_msg` is dropped on purpose: it enumerates the caller's authorized cubes.
        logger.warning(
            "console utilization: groundcover authorization refused cube=%s profile=%s "
            "even though Apollo visibility allowed it", cube, profile,
        )
        return None

    resolved = util.resolve_window(window)
    if resolved is None:  # the route validates first; belt and braces
        resolved = util.resolve_window(util.DEFAULT_WINDOW)
    name, minutes, step, step_seconds = resolved  # type: ignore[misc]

    # CACHED FROM HERE, AND NOT ONE LINE EARLIER. Both authorization checks above have
    # already run and neither is inside `_produce`, so a cache hit can never answer a
    # caller who was not independently cleared for this cube on this request — the entry
    # is a rendering of data the caller has just been authorized to see, never a substitute
    # for the check. Keyed by profile as well as cube and window, which is redundant given
    # that ordering and kept anyway: it matches the rest of this cache's tenancy story,
    # and redundancy is the right side to err on for the one boundary here.
    return await cache.get_or_set(
        profile,
        f"utilization:{cube}:{name}",
        lambda: _utilization_payload(
            registry, cube, name, minutes, step, step_seconds
        ),
        ttl=settings.console_utilization_cache_ttl_seconds,
    )


async def _utilization_payload(
    registry, cube: str, name: str, minutes: int, step: str, step_seconds: int
) -> dict:
    """Resolve the backend and fan out the 12 range queries. Authorizes NOTHING.

    Split out so the caching wrapper in `cube_utilization` cannot accidentally enclose
    an authorization check — the check is in the caller, above the cache, and this
    function has no `profile` and no `ApolloClient` to perform one with even if a later
    edit wanted to.

    **Why it is cached at all.** This is the console's largest single-request
    amplification: 12 concurrent `POST /api/metrics/query` calls, where `/status` is a
    ≤5-query ladder that stops at its first hit. The one Groundcover org key carries
    150 req/s and 1000 req/min across every backend, every `groundcover_*` MCP tool, the
    online badge and the logs view's 10s poll — so roughly 83 uncached tab loads a minute
    exhausts the per-minute budget, and `GroundcoverClient._request` raises on any
    non-200. The damage then lands on OTHER tenants: every cube's online badge degrades to
    `unknown` and every `groundcover_*` tool answers `Error: …`, with nothing in the
    system attributing it to whoever was reloading graphs.

    The browser's own `utilCache` does not bound this — it is a `useRef`, so it dies on
    page reload, which is exactly when a `?tab=resources` link is opened.
    """
    from cube_cloud.console import utilization as util
    from cube_cloud.tools import groundcover as gc_tool

    now = datetime.now(timezone.utc)
    start = gc_tool._rfc3339(now - timedelta(minutes=minutes))
    end = gc_tool._rfc3339(now)

    envelope = {
        "cube": cube,
        "window": name,
        "window_minutes": minutes,
        "step_seconds": step_seconds,
        "start": start,
        "end": end,
    }

    try:
        backend_id = await registry.resolve_backend(cube)
    except Exception as e:
        logger.warning(
            "console utilization: could not resolve a Groundcover backend for %s (%s)",
            cube, type(e).__name__,
        )
        return {**envelope, "available": False, "reason": "unavailable", "panels": []}

    if not backend_id:
        # In no backend's cluster list. Reported ONCE at the root rather than letting
        # four panels each claim "this cube does not report CPU" — four wrong sentences
        # instead of one right one. Mirrors `cube_status`'s `not_reporting`.
        return {**envelope, "available": False, "reason": "not_reporting", "panels": []}

    gc = registry.clients[backend_id]

    # One flat fan-out rather than per-panel batches: 12 queries, all independent.
    # There is deliberately NO polling anywhere above this — the single Groundcover key
    # carries a 150 req/s, 1000 req/min budget shared across the entire fleet and every
    # other consumer (docs/groundcover-integration-spec.md).
    jobs = [
        _utilization_query(gc, cube, panel.metric, aggregation, start, end, step)
        for panel in util.PANELS
        for aggregation in UTILIZATION_AGGREGATIONS
    ]
    flat = await asyncio.gather(*jobs)

    width = len(UTILIZATION_AGGREGATIONS)
    panels = [
        _utilization_panel(panel, list(flat[i * width:(i + 1) * width]))
        for i, panel in enumerate(util.PANELS)
    ]
    return {**envelope, "available": True, "reason": "", "panels": panels}


# ---------------------------------------------------------------------------
# AI tab (docs/ai-reactor-deploy-spec.md)
# ---------------------------------------------------------------------------

# What one catalog model contributes to the AI tab payload. Explicit, like every other
# console serializer: the gateway's override (which `reactor.service` reads under the
# console-rule-3 exception) and each model's `apiBase` never reach the browser.
AI_MODEL_FIELDS = frozenset({
    "id", "display_name", "description", "task", "platform", "gpu_count", "min_vram_gb",
    "storage_gb", "status", "owner", "wired", "lifecycle", "health", "entity_name", "actions",
    "fits", "memory_reserved_gb",
})
AI_GPU_FIELDS = frozenset({
    "available", "total", "free", "product", "memory_gb", "users", "waiting",
    "memory_used_gb", "memory_free_gb",
})
AI_GATEWAY_FIELDS = frozenset({
    "status", "reason", "mode", "lifecycle", "health", "release_channel", "console_installed",
    "ready",
})


def ai_can_write(profile: str) -> bool:
    """Whether `profile` may deploy or remove models (`console_ai_write_profiles`)."""
    allowed = {p.strip() for p in (settings.console_ai_write_profiles or "").split(",") if p.strip()}
    return "*" in allowed or profile in allowed


def ai_payload(state, cube: str) -> dict:
    """Serialize a `reactor.state.ReactorState` for the browser. Explicit literals only."""
    gw = state.gateway
    return {
        "cube": cube,
        "can_write": state.can_write,
        "saturated": state.saturated,
        "gpu_likely_taken": state.gpu_likely_taken,
        "gpu": {
            "available": state.gpu.available,
            "total": state.gpu.total,
            "free": state.gpu.free,
            "product": state.gpu.product,
            "memory_gb": state.gpu.memory_gb,
            # On the GPU with the most room; null when the DCGM exporter did not answer.
            "memory_used_gb": state.gpu.memory_used_gb,
            "memory_free_gb": state.gpu.memory_free_gb,
            "users": list(state.gpu.users),
            "waiting": list(state.gpu.waiting),
        },
        "gateway": {
            "status": gw.status,
            "reason": gw.reason,
            "mode": gw.mode,
            "lifecycle": gw.lifecycle,
            "health": gw.health,
            "release_channel": gw.release_channel,
            "console_installed": gw.console_installed,
            "ready": gw.ready,
        },
        "models": [
            {
                "id": m.spec.id,
                "display_name": m.spec.display_name,
                "description": m.spec.description,
                "task": m.spec.task,
                "platform": m.spec.platform,
                "gpu_count": m.spec.gpu_count,
                "min_vram_gb": m.spec.min_vram_gb,
                "storage_gb": m.spec.storage_gb,
                "status": m.status,
                "owner": m.owner,
                "wired": m.wired,
                "lifecycle": m.lifecycle,
                "health": m.health,
                "entity_name": ((m.entity or {}).get("entityLocator") or {}).get("entityName"),
                "actions": list(m.actions),
                "fits": m.fits,
                # What this model's own vLLM reserves of its GPU, from its pod's
                # --gpu-memory-utilization; null when unknown. The DCGM figure is the
                # whole card's, so a shared card needs this to say who holds what.
                "memory_reserved_gb": state.gpu.reserved_gb(
                    ((m.entity or {}).get("entityLocator") or {}).get("entityName")),
            }
            for m in state.models
        ],
    }


async def _ai_environment(client: ApolloClient, profile: str, cube: str) -> dict | None:
    """The authorized environment row for `cube`, or None (the route 404s)."""
    envs, envs_truncated = await _visible_environments(client, profile)
    match = next((e for e in envs if (e.get("name") or "") == cube), None)
    if match is None and envs_truncated:
        logger.error(
            "console ai: cube %r not found for profile=%s, but that profile's environment "
            "list is TRUNCATED (OI-6 / issue 252).", cube, profile,
        )
    return match


async def cube_ai(client: ApolloClient, profile: str, cube: str) -> dict | None:
    """`GET /console/api/cubes/{name}/ai` — the catalog and this cube's AI Reactor state.

    Read-only: it never repairs anything it finds out of sync (console rule 1a). Returns
    None for a cube the caller cannot see.
    """
    from cube_cloud.reactor import service as reactor

    env = await _ai_environment(client, profile, cube)
    if env is None:
        return None
    state = await reactor.read_state(
        client, env, can_write=ai_can_write(profile), profile=profile,
        gpu_wait=reactor.GPU_WAIT_ON_READ_SECONDS,
    )
    return ai_payload(state, cube)
