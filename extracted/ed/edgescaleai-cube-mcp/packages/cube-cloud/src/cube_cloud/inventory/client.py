"""Reads cube inventory facts and joins them onto Apollo environments.

Background: cube labels, customers, sites, serials and lifecycle status live in the
`edgescale-inventory` service, not in Apollo. The console has only ever had
`cube-o2e87m9a`; this module is what closes **OI-2** in `docs/console-spec.md`.

Four things here are load-bearing.

1. **The authorized cluster set bounds what is REQUESTED, not merely what is
   returned.** A read-capable inventory credential sees the ENTIRE fleet — every
   customer's site labels, locations and serials — and that API has no per-customer
   scoping, so containment is ours, as it is for the Groundcover org key
   (`tools/groundcover.py`). Apollo decides which cubes a caller may see; inventory is
   then asked **only about those cubes**, one `GET /inventory/lookup?q=<cluster>` per
   cube (`_lookup_one`), fanned out concurrently and cached per cluster.

   The earlier design swept the whole fleet into a cached index and filtered on the
   way out. That returned the right thing, but it is a weaker property: every other
   tenant's records crossed the wire and sat in this process's memory, so a logging
   change, a crash dump, or a serializer mistake could expose data this caller was
   never entitled to. Now a scoped tenant's request touches one to three records and
   the process never holds a record for a cube nobody asked about.

   `lookup()` takes the cluster set as its argument precisely so this ordering lives
   in the types rather than in a comment, and both console call sites derive that set
   from `_visible_environments`, which is RBAC-filtered upstream. **The join must
   never be moved above that filter.**

   **The cost is real and was measured, not estimated** (live prod, 2026-08-26):
   `/inventory/lookup` is a server-side scan of the `record_type=cube` partition, not
   a point read, so one cold lookup is **~3.3 s**. Concurrency amortizes it —
   4 cubes 3.4 s, 8 cubes 5.3 s, 16 cubes 7.3 s at `_LOOKUP_CONCURRENCY = 8` — while
   the single fleet sweep is a flat **~6.5 s** for all 91. Break-even is around
   **16 cubes**.

   So the trade is: a scoped tenant (1–3 cubes) pays ~3–4 s on a cold cache and gets
   the strong guarantee; a caller authorized for ~110 cubes would pay roughly **45 s**,
   which is not a page load. `inventory_fleet_sweep_threshold` is the escape hatch —
   above that many authorized cubes, take the single sweep instead. It defaults to
   **0 (never sweep)**, so the per-cube contract holds unless someone deliberately
   opts out.

   Be careful what the threshold actually buys, because it is a proxy and an imperfect
   one. The sweep is only *equivalent in exposure* for a caller whose scope IS the
   fleet; a tenant authorized for 20 cubes is not an admin, and sweeping for them
   would pull records they may not see. A count threshold cannot tell those apart. The
   real fix is to make the scoped fetch cheap rather than to opt out of it — see the
   `?customer=` note in `docs/console-spec.md` §4.13, which would be one GSI-backed
   query instead of N scans.

   `lookup_fleet` is the other way in, and it is the honest form of the same trade:
   the CALLER says its scope is the fleet (the console's fleet map, for an unscoped
   admin profile) instead of a count guessing it. Same cached sweep, same filter on
   the way out; it is never called for a scoped caller, which takes `lookup_each`
   (per cube, threshold ignored) instead.

2. **The join is EXACT match, never substring.** `/inventory/lookup?q=` does
   substring matching across nine fields, which is right for an operator typing a
   fragment and wrong for a machine join: `cube-nvqfm723` is a prefix of
   `cube-nvqfm723-kbsk`, and the console has already been bitten by exactly this
   class of bug — `reads.py::_match_by_resource` exists because
   `esai-data-services-timescaledb` is a prefix of
   `esai-data-services-timescaledb-hv-postgresql`, and first-match attributed one
   database's data to another. Mis-attributing a *customer* is strictly worse than
   mis-attributing a Service, so `build_index` matches exactly and treats any
   ambiguity as a reason to show NOTHING (see rule 3).

   `clustername` is the primary key because `auth/apollo_rbac.py::cluster_name` is
   verified-identity with the Apollo environment name. `apollo_environment_name` is a
   fallback only: the inventory skill's own examples show it holding the
   deploy-suffixed form (`cube-nvqfm723-kbsk`), which will NOT equal the env name, so
   relying on it as primary would silently miss.

3. **Ambiguity resolves to absence, not to a guess.** Two records claiming one
   cluster (a stale record whose `apollo_environment_*` was never scrubbed after a
   teardown — the inventory API has no unassign path, so this is expected, not
   hypothetical) drops BOTH and logs. Showing no label is a cosmetic gap; showing
   another company's name on a customer's cube is a data-integrity incident.

4. **Failure is invisible to the page, and never logged in detail.** `lookup()` does
   not raise: an unreachable backend yields `available=False` and the cube list
   renders exactly as it did before this feature existed. Apollo is the authority for
   whether a cube EXISTS, so inventory being down must never turn a cube list into an
   error page. And failures log `type(e).__name__` only — never the message, never
   `exc_info` — because an inventory HTTP error body can echo record contents, i.e.
   another customer's data, into CloudWatch. That is the same rule, for the same
   reason, as `console/reads.py`'s ban on logging `ApolloError` text.
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
from dataclasses import dataclass, field
from typing import NamedTuple

import boto3
import httpx
from botocore.exceptions import ClientError

from cube_cloud.config import settings
from cube_cloud.inventory.records import InventoryRecord, record_from_raw
from cube_cloud.inventory.simulated import simulated_record

logger = logging.getLogger(__name__)

# Only `record_type == "cube"` rows are cubes; the table holds other record types
# (the inventory skill's own snapshot recipe filters on this). An unfiltered index
# would map non-cube rows onto cube names.
_CUBE_RECORD_TYPE = "cube"

# Placeholder values seen in `apollo_environment_name` on the real prod fleet — a
# workflow writes a status word there before a real environment exists. Observed
# 2026-08-26: `pending` on 2 of 70 populated rows.
#
# These must never become index keys. As it happens the collision guard already
# absorbs the observed case (two rows both claiming `pending` drops both), but that
# is luck rather than design: with only ONE such row the guard stays silent and a
# genuine Apollo environment called `pending` would inherit that cube's customer and
# location. Filtering the value is the actual fix; the guard is the backstop.
#
# EXACT lowercase match, never a substring — the same discipline as
# `tools/modules.py::_NEVER_SECRET_VARIABLES`. A substring rule here would start
# eating real names (a cube legitimately labelled `pending-install`, say).
_NON_NAME_SENTINELS = frozenset({
    "pending", "none", "null", "n/a", "na", "tbd", "unknown", "-", "?",
})

# Response keys that may carry a pagination cursor. The inventory API's paging
# contract is NOT documented in anything we have, so rather than assume there is
# none, every plausible key is followed and an unrecognized-but-cursor-shaped key is
# logged loudly. Silent truncation is the single most repeated failure in this
# codebase (OI-6 / issue 252: `LIST_ENVIRONMENTS`, `CONSOLE_ENVIRONMENT_ENTITIES`),
# and a truncated fleet index here shows as "no label on some cubes" — absence with
# no explanation, the exact symptom those notes warn about.
_CURSOR_KEYS = ("next_token", "nextToken", "last_evaluated_key", "LastEvaluatedKey")

# Hard ceiling on paged requests, so a malformed/looping cursor cannot spin forever
# behind a page load. 25 x 200 = 5,000 cubes, far above the real fleet.
_MAX_PAGES = 25

# The API's own maximum. `backend/cubes.py` does `min(int(qs.get('limit', 50)), 200)`,
# so 200 is the ceiling and the DEFAULT IS 50 — not sending this would quadruple the
# number of round-trips for no reason. Verified against
# EdgescaleAI/edgescale-inventory backend/cubes.py:964.
_PAGE_SIZE = 200

# Sensitive fields the API decrypts into the response for any caller holding
# `view_sensitive` (`backend/shared.py::SENSITIVE_FIELDS`). There is NO query
# parameter that suppresses them: `_redact_sensitive_response` strips them only for a
# caller that LACKS the permission, so whether they cross the wire is decided
# entirely by how our token is scoped.
#
# Named here for ONE purpose — detecting an over-scoped token (see
# `_warn_if_over_scoped`). They are already excluded from `InventoryRecord` by
# construction, so this list is not what keeps them out of the browser; it is what
# makes a bad credential *visible* instead of silently streaming decrypted
# passwords for the whole fleet through this process every cache period.
_SENSITIVE_FIELDS = frozenset({
    "console_password",
    "platform_kubeconfig",
    "ipmi_password",
    "router_wifi_password",
    "router_password",
    "router_esim_1_eid",
    "router_sim_2_eid",
    "motherboard_bmc_default_password",
})

# Logged once per process, not once per page: an over-scoped token is a standing
# condition, and repeating it every 5 minutes for every page would bury it.
_over_scope_warned = False


class InventoryError(Exception):
    """A backend could not be read. Caught by `lookup`; never reaches a route."""


@dataclass(frozen=True)
class InventoryLookup:
    """Result of a lookup — records plus the two facts the UI needs about them.

    `available` distinguishes "could not look" from "nothing there", the distinction
    this codebase preserves everywhere (see `reads.cube_services`'s
    `SERVICES_UNAVAILABLE_MESSAGE`). Without it, an inventory outage would render
    identically to a fleet with no labels assigned, and someone would debug the wrong
    thing.

    `simulated` is propagated all the way to the browser so fictional data can be
    badged. See `simulated.py` for why that is a safety property, not a nicety.

    `unresolved` is the THIRD outcome, and it exists because the other two would both
    lie about it. A cluster lands here when inventory returned more than one record
    claiming it and we refused to guess (rule 3). Reporting that as "no record" is
    wrong — there are records, we just cannot say which is yours — and someone reading
    a blank panel would go add a label that already exists. Reporting it as
    `available=False` is wrong the other way, since the backend answered fine. It is a
    data problem in inventory, and only its own state says so.
    """

    records: dict[str, InventoryRecord] = field(default_factory=dict)
    available: bool = True
    simulated: bool = False
    unresolved: frozenset[str] = frozenset()


class Resolution(NamedTuple):
    """What a join attempt concluded about ONE cluster.

    A bare `InventoryRecord | None` cannot express the difference between "inventory
    has nothing for this cube" and "inventory has two things and we refused to pick",
    and that difference has to survive all the way to the browser — so it is carried
    rather than collapsed at the first return statement.
    """

    record: InventoryRecord | None = None
    ambiguous: bool = False


#: Reused for the common "nothing matched" answer, so the ordinary path allocates
#: nothing and reads as the plain outcome it is.
NO_MATCH = Resolution()


def is_enabled() -> bool:
    """Whether the inventory join runs at all.

    Read per call, never captured at import — the same reason
    `console/reads.py::_platform_prefixes` and `console.is_enabled()` are functions:
    an import-time value cannot be patched in a test and needs a process restart to
    change.
    """
    return bool(settings.inventory_enabled)


def _mode() -> str:
    return (settings.inventory_mode or "").strip().lower()


# --- The join --------------------------------------------------------------


def build_index(records: list[InventoryRecord]) -> dict[str, InventoryRecord]:
    """Index records by cluster name — exact match, ambiguity dropped.

    Thin wrapper over `build_index_detailed` for callers that only want the index.
    """
    return build_index_detailed(records)[0]


def build_index_detailed(
    records: list[InventoryRecord],
) -> tuple[dict[str, InventoryRecord], frozenset[str]]:
    """`(index, ambiguous)` — exact match, ambiguity dropped AND reported.

    Two ordered passes, so a `clustername` match always beats an
    `apollo_environment_name` match rather than depending on record order. See rules
    2 and 3 in the module docstring.

    The ambiguous set is returned rather than only logged because dropping a cluster
    from the index makes it look identical to a cube inventory has no record for, and
    those are different things to tell someone — the same distinction
    `_exact_match` carries on the per-cube path.
    """
    index: dict[str, InventoryRecord] = {}
    ambiguous: set[str] = set()

    def claim(key: str, record: InventoryRecord, *, source: str) -> None:
        if not key or key in ambiguous:
            return
        existing = index.get(key)
        if existing is None:
            index[key] = record
            return
        if existing is record or (
            existing.serial and existing.serial == record.serial
        ):
            return  # the same cube reached by both of its keys
        # NOTE the `existing.serial and` guard: two records that both lack a serial
        # are two unknown cubes, not one. Treating blank == blank as identity would
        # silently merge them and pick whichever landed first — a guess, which is
        # precisely what rule 3 forbids.
        logger.error(
            "inventory: collision on cluster %r via %s (serials %s and %s) — "
            "dropping BOTH records rather than attributing one customer's cube to "
            "another. A stale record whose apollo_environment_* was not scrubbed "
            "after a teardown is the usual cause.",
            key, source, existing.serial or "?", record.serial or "?",
        )
        index.pop(key, None)
        ambiguous.add(key)

    for record in records:
        claim(record.clustername, record, source="clustername")
    for record in records:
        # Fallback only, and only for a cluster no `clustername` already claimed.
        env_name = record.apollo_environment_name
        if env_name.strip().lower() in _NON_NAME_SENTINELS:
            continue  # a status word, not an environment — see _NON_NAME_SENTINELS
        if env_name not in index:
            claim(env_name, record, source="apollo_environment_name")

    return index, frozenset(ambiguous)


# --- Fleet fetch + cache (API mode) ---------------------------------------
#
# The index holds EVERY customer's records in process memory. That is the same
# posture as the Groundcover org key and is safe only because `lookup` filters to the
# caller's authorized clusters on the way out. It is also why the entry is dropped on
# an expired read rather than left resident: `console/cache.py::_live_value`
# documents that exact reasoning for the environments/rolePolicy value, and the whole
# fleet's customer list deserves no less.

# (expires_at_monotonic, index)
_fleet: tuple[float, dict[str, InventoryRecord], frozenset[str]] | None = None
_fleet_lock: asyncio.Lock | None = None
_token: str | None = None

# Per-cluster record cache: cluster -> (expires_at_monotonic, record | None).
#
# Keyed by cluster and NOT by profile, deliberately. A cube's inventory record is a
# property of the cube, not of who asked, so one tenant's read can safely warm
# another's — and the authorization decision happens upstream in Apollo, never here.
# Caching per profile would multiply both the request count and the memory held for
# no security benefit, since the same bytes would be stored N times.
#
# **Negatives are cached too** (the `None`). 23 of 91 cubes on the real prod fleet
# have no `clustername`, so they will never resolve; without negative caching every
# page load would re-scan for every one of them forever.
_records: dict[str, tuple[float, Resolution]] = {}

# Lookups in flight: cluster -> the future its `Resolution` will land in.
#
# The cache above only helps a caller that arrives after a lookup has FINISHED. The
# cube page asks for inventory and GPS in parallel, both need the same record, and
# without this the second request starts its own ~3.3 s scan for a cluster whose
# scan is already running. A caller that finds its cluster here waits on that future
# instead, and shares its outcome — a failure included, so a joined scan that fails
# is "could not look" for every caller rather than a cue to scan again.
_inflight: dict[str, asyncio.Future[Resolution]] = {}

# Bound on concurrent lookups. Each one is a server-side partition scan on the
# inventory Lambda, so an admin's cold load must not arrive as a burst of ~110
# simultaneous scans.
_LOOKUP_CONCURRENCY = 8


def _lock() -> asyncio.Lock:
    """The single-flight lock, replaced if bound to a dead event loop.

    Same hazard and same remedy as `console/cache.py::_lock_for` — an
    `asyncio.Lock` contended under one loop raises if later contended under another,
    which is unreachable on ECS but reachable under `--reload` and in tests. Kept
    minimal here because there is exactly one slot rather than one per profile.
    """
    global _fleet_lock
    lock = _fleet_lock
    if lock is not None:
        try:
            getter = getattr(lock, "_get_loop", None)
            if getter is not None and lock.locked():
                getter()
            return lock
        except RuntimeError:
            logger.warning("inventory fleet lock was bound to a dead loop; replacing")
    lock = asyncio.Lock()
    _fleet_lock = lock
    return lock


def _cached_index() -> tuple[dict[str, InventoryRecord], frozenset[str]] | None:
    global _fleet
    entry = _fleet
    if entry is None:
        return None
    if entry[0] > time.monotonic():
        return entry[1], entry[2]
    _fleet = None  # purge on read — see the note above
    return None


def invalidate() -> None:
    """Drop the cached fleet index and token. For tests and local debugging.

    Not wired to a route, for the reason `console/cache.py::invalidate` gives: a
    cheaply-triggered cache-buster is a way to force an expensive upstream read.
    """
    global _fleet, _token
    _fleet = None
    _token = None
    _records.clear()
    _inflight.clear()


def _load_token() -> str:
    """The inventory API bearer, from Secrets Manager. Cached for the process.

    Secret value JSON: ``{"token": "<bearer>"}``. Follows
    `tools/groundcover.py::_load_key`'s shape rather than inventing a new one.
    """
    global _token
    if _token:
        return _token

    # Local-development override, checked first. Warned about every time it is
    # resolved (once per process, since the result is cached) so a deployed stack
    # running on an env-var credential is visible in its logs rather than silent.
    if settings.inventory_token:
        logger.warning(
            "inventory bearer came from CUBE_CLOUD_INVENTORY_TOKEN, not Secrets "
            "Manager. That is intended for local development only — an ECS task "
            "definition env var is readable via ecs:DescribeTaskDefinition and is "
            "printed by `terraform plan`."
        )
        _token = settings.inventory_token
        return _token

    ref = settings.inventory_token_secret
    if not ref:
        raise InventoryError(
            "inventory_token_secret is unset, so no bearer can be read. Set "
            "CUBE_CLOUD_INVENTORY_TOKEN_SECRET (Terraform sets it on ECS)."
        )
    client = boto3.client("secretsmanager", region_name=settings.aws_region)
    try:
        resp = client.get_secret_value(SecretId=ref)
    except ClientError as e:
        # The secret id is safe to name (it is configuration); the exception is not
        # summarized further than its code, per rule 4.
        raise InventoryError(
            f"Could not read the inventory bearer from {ref}: "
            f"{e.response.get('Error', {}).get('Code', 'ClientError')}"
        ) from e
    try:
        token = (json.loads(resp["SecretString"]) or {}).get("token", "")
    except (ValueError, KeyError) as e:
        raise InventoryError(
            f"The inventory secret {ref} is not JSON of the form "
            '{"token": "..."}.'
        ) from e
    if not token:
        raise InventoryError(f"The inventory secret {ref} is missing 'token'.")
    _token = token
    return token


def _cursor_of(page: dict) -> str | None:
    for key in _CURSOR_KEYS:
        value = page.get(key)
        if value:
            return value if isinstance(value, str) else json.dumps(value)
    # Nothing recognized — but warn if something cursor-SHAPED is present, because
    # the alternative is silently indexing page 1 of N forever.
    _EXPECTED = ("items", "count", "Count")
    unknown = [
        k for k in page
        if k not in _EXPECTED
        and ("token" in k.lower() or "key" in k.lower())
    ]
    if unknown:
        logger.error(
            "inventory: response carries unrecognized cursor-shaped key(s) %s — the "
            "fleet index may be TRUNCATED and some cubes will silently show no "
            "label. Teach _CURSOR_KEYS about it.", sorted(set(unknown)),
        )
    return None


def _warn_if_over_scoped(raw: dict) -> None:
    """Log loudly, ONCE, if the API is handing us decrypted secrets we never asked for.

    A legacy service token resolves to the role `admin`
    (`backend/auth.py:162` maps BOTH legacy tokens to `'admin'`), which carries
    `view_sensitive` — so the fleet list arrives with eight fields decrypted,
    including `ipmi_password` and `platform_kubeconfig`, for every cube, on every
    cache miss. Nothing downstream leaks them (`record_from_raw` copies an allowlist
    of named keys and drops the rest), but "we are not using it" is a weaker property than
    "the server never sent it", and the fix is a credential change rather than a code
    change: a minted read-only token scoped to `view_cubes` WITHOUT `view_sensitive`
    makes the server strip them before they leave.

    So this does not raise or degrade — the join still works, and failing closed on a
    working credential would be the wrong trade. It makes the posture visible.

    **Never log a value, or the field's contents, only its NAME.** The whole point is
    to report a leak without becoming one.
    """
    global _over_scope_warned
    if _over_scope_warned:
        return
    present = sorted(_SENSITIVE_FIELDS & raw.keys())
    if not present:
        return
    _over_scope_warned = True
    logger.warning(
        "inventory token is OVER-SCOPED: the API returned %d decrypted sensitive "
        "field(s) (%s) that this integration never uses and immediately discards. "
        "A legacy service token authenticates as 'admin' and therefore holds "
        "view_sensitive. Replace it with a minted read-only token scoped to "
        "view_cubes only, and the server will strip these before they cross the "
        "wire. See docs/console-spec.md 4.13.",
        len(present), ", ".join(present),
    )


async def _fetch_fleet_index() -> tuple[dict[str, InventoryRecord], frozenset[str]]:
    """Read every cube record from the API and index it. Raises `InventoryError`."""
    base = (settings.inventory_api_base or "").rstrip("/")
    if not base:
        raise InventoryError(
            "inventory_api_base is unset. Set CUBE_CLOUD_INVENTORY_API_BASE to the "
            "stage URL (Terraform sets it on ECS)."
        )
    token = await asyncio.to_thread(_load_token)

    records: list[InventoryRecord] = []
    cursor: str | None = None
    async with httpx.AsyncClient(
        timeout=settings.inventory_timeout_seconds,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        },
    ) as http:
        for page_n in range(_MAX_PAGES):
            # NOT `view=summary`. That projection would be the obvious choice — it
            # is smaller, skips the KMS decrypt pass, and is served from a covering
            # GSI — but `_LIST_VIEW_FIELDS` does NOT include `clustername` or
            # `apollo_environment_name`, i.e. it omits BOTH of this join's keys while
            # happily returning all six original display fields. Using it would yield
            # records that can never be matched to a cube: a silent, total join failure that
            # looks like "inventory has no data". The GSI caps projection at 20
            # non-key attributes and is already full, so adding a key there is a
            # destroy/recreate on the inventory side, not an edit.
            params: dict[str, str] = {"limit": str(_PAGE_SIZE)}
            if cursor:
                params["next_token"] = cursor
            try:
                resp = await http.get(f"{base}/inventory", params=params)
            except httpx.HTTPError as e:
                raise InventoryError(f"inventory request failed: {type(e).__name__}") from e
            if resp.status_code in (401, 403):
                # Drop the cached bearer so the NEXT attempt re-reads Secrets
                # Manager. Without this, a rotated credential needs a
                # `force-new-deployment` to take effect, because `_token` is
                # memoized for the process lifetime.
                #
                # This is not hypothetical: a minted inventory token defaults to a
                # 90-DAY expiry (`token_store.DEFAULT_TOKEN_EXPIRY_DAYS`), unlike the
                # legacy tokens, which never expire. So the credential this
                # integration should be running on is guaranteed to lapse, and the
                # fix — put a new value in the secret — has to be able to take effect
                # without a deploy.
                global _token
                _token = None
                raise InventoryError(
                    f"inventory API rejected the bearer ({resp.status_code}) — it is "
                    "expired, revoked, or lacks `view_cubes`. A minted token expires "
                    "90 days after minting unless expires_in_days was set. The "
                    "cached bearer has been dropped, so updating the secret takes "
                    "effect within one cache period and needs no redeploy."
                )
            if resp.status_code >= 400:
                # Body deliberately NOT included: it can echo record contents.
                raise InventoryError(f"inventory API returned {resp.status_code}")
            try:
                page = resp.json() or {}
            except ValueError as e:
                raise InventoryError("inventory API returned non-JSON") from e

            items = page.get("items") or []
            for raw in items:
                if not isinstance(raw, dict):
                    continue
                if (raw.get("record_type") or _CUBE_RECORD_TYPE) != _CUBE_RECORD_TYPE:
                    continue
                _warn_if_over_scoped(raw)
                records.append(record_from_raw(raw))

            cursor = _cursor_of(page)
            if not cursor:
                break
        else:
            logger.error(
                "inventory: stopped after %d pages with a cursor still present — the "
                "fleet index is TRUNCATED.", _MAX_PAGES,
            )

    logger.info("inventory: indexed %d cube records", len(records))
    return build_index_detailed(records)


# --- Per-cube lookup (the default path) -----------------------------------


def _exact_match(items: list, cluster: str) -> InventoryRecord | None:
    """The record that genuinely IS `cluster`, or None.

    **`/inventory/lookup` will happily return a cube we did not ask for.** Its
    documented behaviour is: exact match against `cube_label_name` /
    `apollo_environment_name` / `clustername` first, and only if there is NO exact
    match does it fall back to a substring sweep across nine fields. So a lookup for
    a cube inventory has never heard of can come back 200 with a *different* cube
    whose serial or notes happen to contain the string — and `cube-nvqfm723` is a
    substring of `cube-nvqfm723-kbsk`.

    Accepting `items[0]` would therefore attribute one customer's site label, location
    and serial to another customer's cube. This function is what makes the API's
    convenience safe: correctness comes from re-checking in Python, the same
    discipline `reads.app_workloads` uses for Groundcover's unverified
    `workload:<name>` matching.

    Case-insensitive because the API matches that way (SCRUM-1618) and Apollo
    environment names are lowercase, so a differently-cased stored value is the same
    cube rather than a different one.

    **Ambiguity resolves to absence here too, and that is not a duplicate of
    `build_index`'s guard — it is the same guard on the path that actually runs.**
    `build_index` has enforced rule 3 since this module was written, but it is only
    reachable through the fleet sweep, which `inventory_fleet_sweep_threshold` gates
    off by default. So for every deployed configuration the guarded code was dead and
    this function was live, and this function took the FIRST match in each tier.

    The reachable failure, using this module's own recorded facts about prod: 23 of 91
    cubes carry no `clustername`, so they fall through to the second tier; and a stale
    record whose `apollo_environment_*` was never scrubbed after a teardown is
    expected rather than hypothetical, because the API has no unassign path. Two
    records can therefore both claim one `apollo_environment_name`, one of them
    another tenant's — and whichever the API happened to list first won, was cached
    process-wide for the TTL, and put that customer's name, site and location on this
    customer's cube page.

    Distinctness is by cube, not by object: a single cube legitimately reached through
    both of its keys is one answer, not a conflict. `_same_cube` carries that test, and
    it is deliberately the same identity rule `build_index.claim` uses.
    """
    target = cluster.strip().lower()
    if not target:
        return NO_MATCH

    candidates = [record_from_raw(raw) for raw in items if isinstance(raw, dict)]

    def resolve(matches: list[InventoryRecord], source: str) -> Resolution | None:
        """One tier's answer, or None to fall through to the next tier."""
        if not matches:
            return None
        first = matches[0]
        conflicting = [r for r in matches[1:] if not _same_cube(first, r)]
        if conflicting:
            logger.error(
                "inventory: %d records claim cluster %r via %s (serials %s) — "
                "resolving to UNRESOLVED rather than attributing one customer's cube "
                "to another. A stale record whose apollo_environment_* was not "
                "scrubbed after a teardown is the usual cause.",
                len(matches), cluster, source,
                ", ".join(sorted(r.serial or "?" for r in matches)),
            )
            return Resolution(record=None, ambiguous=True)
        return Resolution(record=first)

    # `clustername` first, for the same reason it is the primary index key. A conflict
    # in this tier does NOT fall through to the next one: the primary key is
    # contradictory, so a weaker key agreeing would not make the answer safe.
    tier = resolve(
        [r for r in candidates if r.clustername.strip().lower() == target],
        "clustername",
    )
    if tier is not None:
        return tier

    tier = resolve(
        [
            r for r in candidates
            if (env := r.apollo_environment_name.strip().lower()) == target
            and env not in _NON_NAME_SENTINELS
        ],
        "apollo_environment_name",
    )
    return tier if tier is not None else NO_MATCH


def _same_cube(a: InventoryRecord, b: InventoryRecord) -> bool:
    """Whether two records describe one cube, for collision purposes.

    NOTE the `a.serial and` guard, which mirrors `build_index.claim`'s: two records
    that both LACK a serial are two unknown cubes, not one. Treating blank == blank as
    identity would silently merge them and hand back whichever arrived first — which
    is precisely the guess rule 3 forbids.
    """
    return a is b or bool(a.serial and a.serial == b.serial)


async def _lookup_one(http: httpx.AsyncClient, base: str, cluster: str) -> Resolution:
    """One cube's `Resolution` — a record, nothing, or an explicit ambiguity.

    A failed lookup raises, so `_per_cube_records` can fail the whole read rather
    than silently reporting "no record" for a cube whose record exists — "could not
    look" and "nothing there" must stay distinguishable all the way up.
    """
    try:
        resp = await http.get(f"{base}/inventory/lookup", params={"q": cluster})
    except httpx.HTTPError as e:
        raise InventoryError(f"inventory lookup failed: {type(e).__name__}") from e

    if resp.status_code in (401, 403):
        global _token
        _token = None
        raise InventoryError(
            f"inventory API rejected the bearer ({resp.status_code}) — it is expired, "
            "revoked, or lacks `view_cubes`. A minted token expires 90 days after "
            "minting unless expires_in_days was set. The cached bearer has been "
            "dropped, so updating the secret takes effect within one cache period "
            "and needs no redeploy."
        )
    if resp.status_code >= 400:
        # Body withheld: it can echo record contents.
        raise InventoryError(f"inventory API returned {resp.status_code}")

    try:
        payload = resp.json() or {}
    except ValueError as e:
        raise InventoryError("inventory API returned non-JSON") from e

    items = payload.get("items") or []
    for raw in items:
        if isinstance(raw, dict):
            _warn_if_over_scoped(raw)
    return _exact_match(items, cluster)


def _cached_record(cluster: str) -> tuple[bool, Resolution]:
    """(hit, resolution) for `cluster`, purging an expired entry.

    An ambiguous resolution is cached like any other. It is a data problem in
    inventory rather than a transient one, so re-deciding it on every page load would
    buy nothing and cost a ~3.3 s partition scan each time.

    Purge-on-read for the reason `console/cache.py::_live_value` documents: an
    expired entry holding another tenant's customer name should not stay resident for
    the task's lifetime instead of the TTL.
    """
    entry = _records.get(cluster)
    if entry is None:
        return False, NO_MATCH
    if entry[0] > time.monotonic():
        return True, entry[1]
    _records.pop(cluster, None)
    return False, NO_MATCH


async def _per_cube_records(
    clusters: set[str],
) -> tuple[dict[str, InventoryRecord], set[str]]:
    """`(records, unresolved)` for exactly `clusters` — nothing else is requested.

    This is the path that makes the pull scope-limited rather than only the response.

    `unresolved` holds the clusters inventory answered ambiguously, kept separate from
    "not found" all the way out so the page can say which happened. See
    `InventoryLookup`.
    """
    found: dict[str, InventoryRecord] = {}
    unresolved: set[str] = set()

    def take(cluster: str, resolution: Resolution) -> None:
        if resolution.record is not None:
            found[cluster] = resolution.record
        elif resolution.ambiguous:
            unresolved.add(cluster)

    misses: list[str] = []
    for cluster in sorted(clusters):
        hit, resolution = _cached_record(cluster)
        if hit:
            take(cluster, resolution)
        else:
            misses.append(cluster)

    if not misses:
        return found, unresolved

    # Join what is already in flight; claim the rest. No `await` between the check
    # and the claim, so two callers cannot both claim one cluster.
    joined = {c: _inflight[c] for c in misses if c in _inflight}
    loop = asyncio.get_running_loop()
    claims: dict[str, asyncio.Future[Resolution]] = {}
    for cluster in misses:
        if cluster not in joined:
            future: asyncio.Future[Resolution] = loop.create_future()
            # Marks a failure as retrieved even if nobody joined to read it, so an
            # unshared failure is not reported again as "never retrieved".
            future.add_done_callback(lambda f: f.cancelled() or f.exception())
            _inflight[cluster] = future
            claims[cluster] = future

    try:
        if claims:
            results, failure = await _scan(list(claims))
            # Complete every cluster that answered BEFORE the failure is raised, so a
            # caller that joined one of them gets its own answer rather than a
            # batch-mate's failure (the fleet map batches the visible fleet, and a
            # cube page opened meanwhile joins one cluster of that batch).
            for cluster, resolution in results:
                claims[cluster].set_result(resolution)
                take(cluster, resolution)
            if failure is not None:
                raise failure
    except BaseException as e:
        # Every caller waiting on a cluster that did NOT answer gets the failure too.
        # An unauthored upstream exception or a cancellation is re-cast as an
        # `InventoryError` naming its type only (rule 4), so it reaches `lookup`'s
        # safe-to-log branch.
        shared = e if isinstance(e, InventoryError) else InventoryError(
            f"inventory lookup failed: {type(e).__name__}"
        )
        for future in claims.values():
            if not future.done():
                future.set_exception(shared)
        raise
    finally:
        for cluster, future in claims.items():
            if _inflight.get(cluster) is future:
                del _inflight[cluster]

    for cluster, future in joined.items():
        # Shielded: this caller going away (a closed tab) must not cancel a lookup
        # other callers are waiting on.
        take(cluster, await asyncio.shield(future))

    return found, unresolved


async def _scan(
    clusters: list[str],
) -> tuple[list[tuple[str, Resolution]], BaseException | None]:
    """Look up `clusters` against the API and cache each answer.

    Returns `(answered, failure)`: every lookup that answered, and the first failure
    if any did not. A failed lookup is RETURNED rather than raised so the caller can
    complete each answered cluster on its own terms; `_per_cube_records` still fails
    the read when `failure` is set. Raises only what stops the whole batch before it
    starts (no base URL, no token).
    """
    base = (settings.inventory_api_base or "").rstrip("/")
    if not base:
        raise InventoryError(
            "inventory_api_base is unset. Set CUBE_CLOUD_INVENTORY_API_BASE to the "
            "stage URL (Terraform sets it on ECS)."
        )
    token = await asyncio.to_thread(_load_token)
    ttl = settings.inventory_cache_ttl_seconds
    gate = asyncio.Semaphore(_LOOKUP_CONCURRENCY)

    async with httpx.AsyncClient(
        timeout=settings.inventory_timeout_seconds,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
    ) as http:
        async def one(cluster: str) -> tuple[str, Resolution]:
            async with gate:
                return cluster, await _lookup_one(http, base, cluster)

        # One failed lookup still fails the read, which `lookup` degrades to
        # `available=False`. Reporting a partial set as complete would render "this
        # cube has no label" for a cube whose label we simply failed to fetch — the
        # "could not look" vs "nothing there" conflation this codebase refuses
        # everywhere else. But the lookups that DID answer are cached before the
        # failure is raised: a fleet-wide read (the GPS map) otherwise re-scanned the
        # whole visible fleet on every load while one cube kept failing.
        outcomes = await asyncio.gather(
            *(one(c) for c in clusters), return_exceptions=True
        )

    results = [o for o in outcomes if not isinstance(o, BaseException)]
    failure = next((o for o in outcomes if isinstance(o, BaseException)), None)

    if ttl > 0:
        for cluster, resolution in results:
            # Negatives and ambiguities cached too — see the `_records` note.
            _records[cluster] = (time.monotonic() + ttl, resolution)

    logger.info(
        "inventory: looked up %d cube(s), %d resolved, %d unresolved, %d failed",
        len(results),
        sum(r.record is not None for _, r in results),
        sum(r.ambiguous for _, r in results),
        len(outcomes) - len(results),
    )
    return results, failure


async def _api_index() -> tuple[dict[str, InventoryRecord], frozenset[str]]:
    """The cached fleet index plus its ambiguous clusters, fetched at most once per
    TTL across concurrent callers."""
    cached = _cached_index()
    if cached is not None:
        return cached

    ttl = settings.inventory_cache_ttl_seconds
    if ttl <= 0:  # escape hatch for debugging, mirroring console_cache_ttl_seconds
        return await _fetch_fleet_index()

    global _fleet
    lock = _lock()
    async with lock:
        cached = _cached_index()  # another caller may have filled it while we waited
        if cached is not None:
            return cached
        index, ambiguous = await _fetch_fleet_index()
        _fleet = (time.monotonic() + ttl, index, ambiguous)
        return index, ambiguous


# --- Public entry point ----------------------------------------------------


async def lookup(clusters: set[str]) -> InventoryLookup:
    """Inventory records for `clusters` — and ONLY for `clusters`.

    Never raises. See rules 1 and 4 in the module docstring: the caller supplies an
    already-authorized cluster set, and any backend failure degrades to
    `available=False` rather than failing the page.
    """
    # Which path: ask about exactly these cubes (default), or sweep the fleet.
    #
    # The threshold exists because scoping the PULL is only a real narrowing when the
    # caller's scope is narrower than the fleet. For an admin authorized for every
    # environment, N lookups cost N server-side partition scans and pull precisely
    # the same data one sweep would — so the sweep is strictly cheaper at equal
    # exposure. Default 0 means never sweep, i.e. always honour the per-cube
    # contract, and raising it is a deliberate latency decision.
    threshold = settings.inventory_fleet_sweep_threshold
    return await _lookup(clusters, sweep=threshold > 0 and len(clusters) > threshold)


async def lookup_fleet(clusters: set[str]) -> InventoryLookup:
    """`lookup`, answered from ONE whole-fleet read instead of a lookup per cube.

    Only for a caller whose scope IS the fleet (an unscoped admin), and the caller
    decides that, not a cube count: rule 1's "a count threshold cannot tell those
    apart" is why this is its own entry point rather than a lower threshold. For such
    a caller the sweep pulls the same records the per-cube path would, in one ~6.5 s
    read instead of ~110 partition scans, and it is cached for
    `inventory_cache_ttl_seconds` and shared with the threshold sweep.

    It still takes the authorized cluster set and returns only those records, so
    what leaves this module is bounded by Apollo exactly as `lookup`'s is. Never
    raises.
    """
    return await _lookup(clusters, sweep=True)


async def lookup_each(clusters: set[str]) -> InventoryLookup:
    """`lookup`, always one lookup per cube, whatever `inventory_fleet_sweep_threshold`
    says.

    For a caller that must never take the fleet sweep: a scoped viewer of the console's
    fleet map. The threshold is a latency knob for the cube page and a count, which
    cannot tell a large customer from an admin (rule 1), so it must not be able to send
    a customer's map through the whole fleet's records. Never raises.
    """
    return await _lookup(clusters, sweep=False)


async def _lookup(clusters: set[str], *, sweep: bool) -> InventoryLookup:
    if not is_enabled() or not clusters:
        return InventoryLookup(available=True)

    mode = _mode()
    if mode == "simulated":
        # Synthesized per requested cluster, so no fleet read and nothing to cache.
        return InventoryLookup(
            records={c: simulated_record(c) for c in clusters},
            available=True,
            simulated=True,
        )
    if mode != "api":
        logger.error(
            "inventory_mode=%r is not one of 'api' | 'simulated' — the join is being "
            "skipped. Fix CUBE_CLOUD_INVENTORY_MODE.", settings.inventory_mode,
        )
        return InventoryLookup(available=False)

    try:
        if sweep:
            logger.info(
                "inventory: reading the fleet index for %d authorized cubes instead of "
                "%d individual lookups", len(clusters), len(clusters),
            )
            index, ambiguous = await _api_index()
            records = {c: index[c] for c in clusters if c in index}
            # Same three-way answer as the per-cube path. `build_index` has always
            # DROPPED an ambiguous cluster from the index; without this it would then
            # be indistinguishable from a cube inventory has never heard of, which is
            # the conflation `unresolved` exists to prevent.
            unresolved = {c for c in clusters if c in ambiguous}
        else:
            records, unresolved = await _per_cube_records(clusters)
    except InventoryError as e:
        # `InventoryError` messages are authored HERE and carry no record contents,
        # so this one is safe to log in full — unlike the upstream exceptions it
        # wraps, which is why every `raise` above reduces them to a type or a code.
        logger.warning("inventory unavailable: %s", e)
        return InventoryLookup(available=False)
    except Exception as e:
        # Type only. Rule 4.
        logger.warning("inventory lookup errored: %s", type(e).__name__)
        return InventoryLookup(available=False)

    return InventoryLookup(
        records=records,
        available=True,
        simulated=False,
        unresolved=frozenset(unresolved),
    )
