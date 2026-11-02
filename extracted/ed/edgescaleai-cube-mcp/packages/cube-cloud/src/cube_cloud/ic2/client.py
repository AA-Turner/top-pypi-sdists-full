"""Reads each cube router's latest GPS position from Peplink InControl2 (IC2).

One login, one `GET /rest/o` to find the orgs, then per org one `last_loc` call (every
router's latest position in a single response) and one `g` call (the groups, for their
timezones). The result is an index from router serial to position. The console joins
a cube to its router through inventory's `router_serial_number`; nothing here knows
about cubes.

How the index is kept, per process. IC2 allows one live token per API client and a
new login cancels the last, so logins are kept few and never concurrent:

- one refresh at a time; callers that arrive during it share it;
- each index lives `ic2_cache_ttl_seconds`, give or take a minute so tasks drift apart;
- once there is an index, an expired one is served while the refresh runs, and kept
  if the refresh fails; only a process that has never read IC2 waits, or sees None;
- a refresh has `ic2_refresh_deadline_seconds` in all;
- after a failed refresh, IC2 is left alone for 45 to 75 s;
- a `401 invalid_accessor` (another login cancelled our token) gets one fresh login
  and retry per refresh; any other 401 is final.

Four things here are load-bearing.

1. **`ts` is local time in the router's GROUP timezone, not UTC.** It carries no zone.
   Confirmed live on 2026-10-13: the newest reports read as America/Denver were under a
   minute old, and read as UTC all of them were exactly six hours old. So each row's
   `group_id` is looked up in the org's groups to convert it. An error here must never
   make a report look FRESHER than it is, so a missing timezone, an unknown one, or a
   wall time that is ambiguous or skipped by a DST change gives `reported_at = None`
   ("time unknown"), never a UTC guess.

2. **Only a `last_loc` point with `la`, `lo` and `ts` is a GPS position.** A point with
   no `la`/`lo` means the router never reported one. IC2's device detail also carries
   coordinates for routers with no GPS, but those are IC2's own cell-tower estimate (the
   org has `opencell` on) and are never read here. IC2's `address` field is ignored: it is
   one static address on every router.

3. **A router present with no position is not a router that is absent.** The index maps
   a serial to `None` for the first ("no GPS position reported") and lacks the key for
   the second ("router not found"). The console shows them differently.

4. **Failure is "unavailable", never an exception and never "no GPS".** `positions()`
   returns `None` when anything went wrong, and the console shows the row as unavailable.
   A partial answer is a failure too: one org's call failing fails the whole refresh,
   and zero orgs or zero routers is never read as an empty fleet, since either would
   show real routers as "not found".
   Failures log the exception type and IC2's `resp_code` only, never a response body,
   the client secret or a token.
"""

from __future__ import annotations

import asyncio
import json
import logging
import random
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import boto3
import httpx
from botocore.exceptions import ClientError

from cube_cloud.config import settings

logger = logging.getLogger(__name__)

_TOKEN_PATH = "/api/oauth2/token"
_REST_PATH = "/rest"


class Ic2Error(Exception):
    """IC2 could not be read. Caught by `positions`; never reaches a route.

    Messages are authored here and carry no response body, so they are safe to log.
    """


@dataclass(frozen=True)
class Position:
    """A router's latest GPS position. `reported_at` is UTC, or None if the time
    can't be trusted (see rule 1)."""

    lat: float
    lng: float
    reported_at: datetime | None


#: Router serial (normalized) -> its position, or None if it never reported one.
Ic2Index = dict[str, "Position | None"]

# (expires_at on the `_now()` clock, index). Kept past expiry: it is the last good
# index, served while a refresh runs and when one fails.
_index: tuple[float, Ic2Index] | None = None

# The refresh in flight, shared by every caller that arrives while it runs. IC2 allows
# one live token per client and a new login cancels the last, so concurrent page views
# on a cold cache must not each log in: the later ones would cancel the earlier ones'
# tokens mid-read. Same pattern as `inventory/client.py::_inflight`.
_refresh: asyncio.Task[Ic2Index | None] | None = None

# After a failed refresh, IC2 is left alone until this time (`_now()` clock). A down
# or rate-limiting IC2 should see one try a minute per task, not one per page view.
# Randomised so that tasks which failed together do not retry together.
_retry_at: float = 0.0
_BACKOFF_SECONDS = (45.0, 75.0)

# Each index lives `ic2_cache_ttl_seconds` give or take up to this much, so tasks
# started together (a rolling deploy) drift apart instead of logging in together.
_TTL_SPREAD_SECONDS = 60.0

# See `stats`. cube-cloud has no metrics pipeline (its OTLP export is spans per tool
# call), so these are in-process counts, and each log line that reports an event
# carries the running count, which is where an operator will see it.
_counts = {"invalid_accessor_relogins": 0, "refresh_failures": 0}

# Every random draw comes from here, so tests can pin it.
_rng = random.Random()


def _now() -> float:
    """The clock the cache and back-off run on. A seam for tests: patching
    `time.monotonic` itself would also move the event loop's clock."""
    return time.monotonic()


def stats() -> dict[str, int]:
    """This process's counts since it started (or since `invalidate`).

    `invalid_accessor_relogins`: logins forced because another login to this client
    cancelled our token. A steady rate means the client is being shared.
    `refresh_failures`: refreshes that ended with no new index (back-off skips are
    not refreshes). A run of them means IC2 is down or the credentials are bad.
    """
    return dict(_counts)


def is_enabled() -> bool:
    """Read per call, never at import, so tests and a restart-free config change work."""
    return bool(settings.ic2_enabled)


def normalize_serial(serial: str) -> str:
    """The form serials are compared in. Inventory and IC2 both write upper case today;
    this keeps a stray space or lower-case entry from reading as "router not found"."""
    return (serial or "").strip().upper()


def invalidate() -> None:
    """Back to a fresh process: no index, no back-off, counts at zero. For tests and
    local debugging; not wired to a route, since a cheap cache-buster is a way to
    force logins against IC2."""
    global _index, _refresh, _retry_at
    _index = None
    _refresh = None
    _retry_at = 0.0
    for name in _counts:
        _counts[name] = 0


def _load_credentials() -> tuple[str, str]:
    """`(client_id, client_secret)` for this stack's IC2 client."""
    if settings.ic2_client_id or settings.ic2_client_secret:
        logger.warning(
            "IC2 client came from CUBE_CLOUD_IC2_CLIENT_ID/_SECRET, not Secrets "
            "Manager. That is for local development only, with your own IC2 client."
        )
        if not (settings.ic2_client_id and settings.ic2_client_secret):
            raise Ic2Error("Set both CUBE_CLOUD_IC2_CLIENT_ID and CUBE_CLOUD_IC2_CLIENT_SECRET.")
        return settings.ic2_client_id, settings.ic2_client_secret

    ref = settings.ic2_credentials_secret
    if not ref:
        raise Ic2Error(
            "ic2_credentials_secret is unset, so no IC2 client can be read. Set "
            "CUBE_CLOUD_IC2_CREDENTIALS_SECRET (Terraform sets it on ECS)."
        )
    sm = boto3.client("secretsmanager", region_name=settings.aws_region)
    try:
        resp = sm.get_secret_value(SecretId=ref)
    except ClientError as e:
        raise Ic2Error(
            f"Could not read the IC2 client from {ref}: "
            f"{e.response.get('Error', {}).get('Code', 'ClientError')}"
        ) from e
    try:
        doc = json.loads(resp["SecretString"]) or {}
    except (ValueError, KeyError) as e:
        raise Ic2Error(
            f"The IC2 secret {ref} is not JSON of the form "
            '{"client_id": "...", "client_secret": "..."}.'
        ) from e
    client_id, client_secret = doc.get("client_id", ""), doc.get("client_secret", "")
    if not (client_id and client_secret):
        raise Ic2Error(f"The IC2 secret {ref} is missing client_id or client_secret.")
    return client_id, client_secret


async def _login(http: httpx.AsyncClient, base: str, client_id: str, client_secret: str) -> str:
    resp = await http.post(
        base + _TOKEN_PATH,
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        },
    )
    if resp.status_code != 200:
        raise Ic2Error(f"IC2 login answered HTTP {resp.status_code}")
    token = (resp.json() or {}).get("access_token")
    if not token:
        raise Ic2Error("IC2 login returned no access_token")
    return token


class _Session:
    """One refresh's conversation with IC2: a login, then GETs with its token.

    IC2 allows one live token per client, and a new login cancels the last. A GET
    answered `401 invalid_accessor` means someone else logged in with this client
    (a second task, or a local run borrowing it) and cancelled ours. That one is
    worth a fresh login and a retry, once per refresh: two holders fighting over
    one client would otherwise trade logins forever. Any other 401 is bad or
    revoked credentials, which logging in again cannot fix.
    """

    def __init__(self, http: httpx.AsyncClient, base: str, client_id: str, client_secret: str):
        self._http, self._base = http, base
        self._client_id, self._client_secret = client_id, client_secret
        self._token = ""
        self._relogged_in = False

    async def login(self) -> None:
        self._token = await _login(self._http, self._base, self._client_id, self._client_secret)

    async def get(self, path: str):
        resp = await self._send(path)
        if _is_invalid_accessor(resp) and not self._relogged_in:
            self._relogged_in = True
            _counts["invalid_accessor_relogins"] += 1
            logger.warning(
                "ic2 token was cancelled by another login to this client "
                "(invalid_accessor); logging in again (%d such re-logins in this process)",
                _counts["invalid_accessor_relogins"],
            )
            await self.login()
            resp = await self._send(path)
        if resp.status_code != 200:
            raise Ic2Error(f"IC2 {_path_shape(path)} answered HTTP {resp.status_code}")
        doc = resp.json() or {}
        # IC2 reports most errors as HTTP 200 with a non-SUCCESS resp_code.
        if doc.get("resp_code") != "SUCCESS":
            raise Ic2Error(
                f"IC2 {_path_shape(path)} answered resp_code {doc.get('resp_code')!r}"
            )
        return doc.get("data")

    async def _send(self, path: str):
        return await self._http.get(
            self._base + _REST_PATH + path,
            headers={"Authorization": f"Bearer {self._token}"},
        )


def _is_invalid_accessor(resp) -> bool:
    """A 401 whose body names `invalid_accessor`.

    IC2's API documentation gives the body as `{"error": "invalid_accessor", ...}`;
    no real one has been captured, so any mention in the body counts, as
    shared-workflow-lib's tested rule does. Never raises.
    """
    if resp.status_code != 401:
        return False
    try:
        doc = resp.json()
    except ValueError:
        doc = None
    if isinstance(doc, dict) and doc.get("error") == "invalid_accessor":
        return True
    try:
        return "invalid_accessor" in (resp.text or "").lower()
    except Exception:
        return False


def _device_count(group: dict) -> int:
    """A group's online plus offline devices, as `GET /rest/o/{org}/g` reports them."""
    total = 0
    for key in ("online_device_count", "offline_device_count"):
        value = group.get(key)
        if isinstance(value, int) and not isinstance(value, bool):
            total += value
    return total


def _path_shape(path: str) -> str:
    """The endpoint without the org id, for log lines."""
    parts = path.strip("/").split("/")
    if len(parts) >= 2 and parts[0] == "o":
        parts[1] = "{org}"
    return "/" + "/".join(parts)


def _to_utc(ts: str, tz_name: str) -> datetime | None:
    """A zone-less group-local `ts` as UTC, or None if it can't be trusted (rule 1)."""
    if not ts or not tz_name:
        return None
    try:
        local = datetime.fromisoformat(ts)
        zone = ZoneInfo(tz_name)
    except (ValueError, ZoneInfoNotFoundError):
        return None
    if local.tzinfo is not None:
        return local.astimezone(timezone.utc)
    early = local.replace(tzinfo=zone, fold=0)
    late = local.replace(tzinfo=zone, fold=1)
    if early.utcoffset() != late.utcoffset():
        # The wall time happens twice (the fall-back hour) or never (the spring-forward
        # hour): either reading could be an hour off.
        return None
    return early.astimezone(timezone.utc)


def _position(row: dict, zones: dict) -> Position | None:
    points = row.get("points") or []
    point = points[0] if points and isinstance(points[0], dict) else {}
    lat, lng = point.get("la"), point.get("lo")
    if lat is None or lng is None:
        return None
    try:
        lat, lng = float(lat), float(lng)
    except (TypeError, ValueError):
        return None
    return Position(lat, lng, _to_utc(point.get("ts") or "", zones.get(row.get("group_id"), "")))


async def _fetch_index() -> Ic2Index:
    # boto3 blocks, with timeouts of its own far longer than the refresh deadline: off
    # the event loop, the deadline can stop waiting for it.
    client_id, client_secret = await asyncio.to_thread(_load_credentials)
    base = (settings.ic2_api_base or "").rstrip("/")
    async with httpx.AsyncClient(timeout=settings.ic2_timeout_seconds) as http:
        ic2 = _Session(http, base, client_id, client_secret)
        await ic2.login()
        index: Ic2Index = {}
        orgs = await ic2.get("/o") or []
        if not orgs:
            # Read as an empty fleet, every router would show as "not found".
            raise Ic2Error("IC2 listed no organisations for this client")
        for org in orgs:
            org_id = org.get("id")
            rows = await ic2.get(f"/o/{org_id}/last_loc") or []
            groups = await ic2.get(f"/o/{org_id}/g") or []
            zones = {g.get("id"): g.get("timezone") or "" for g in groups}
            devices = sum(_device_count(g) for g in groups)
            if len(rows) < devices:
                # `last_loc` has no paging today (146 rows for 146 devices, checked
                # 2026-10-13). If it starts paging, the missing routers would read as
                # "not found"; this line is how anyone would know. What came is served.
                logger.warning(
                    "ic2: last_loc returned %d rows for an org whose groups hold %d "
                    "devices; IC2 may be paging",
                    len(rows), devices,
                )
            for row in rows:
                serial = normalize_serial(row.get("sn") or "")
                if serial:
                    index[serial] = _position(row, zones)
    if not index:
        raise Ic2Error("IC2 returned no routers in any organisation's last_loc")
    logger.info(
        "ic2: indexed %d routers, %d with a GPS position",
        len(index), sum(p is not None for p in index.values()),
    )
    return index


async def _refresh_index() -> Ic2Index | None:
    """One refresh: the new index, or None if IC2 could not be read. Never raises."""
    global _index
    deadline = settings.ic2_refresh_deadline_seconds
    try:
        index = await asyncio.wait_for(_fetch_index(), deadline)
    except asyncio.TimeoutError:
        _failed(f"the refresh missed its {deadline}s deadline")
        return None
    except Ic2Error as e:
        _failed(str(e))
        return None
    except Exception as e:
        # Type only: an upstream exception's text can carry a response body.
        _failed(f"read errored: {type(e).__name__}")
        return None
    ttl = settings.ic2_cache_ttl_seconds
    if ttl > 0:
        # At most half the setting either way, so a short one is never spread to zero.
        spread = min(_TTL_SPREAD_SECONDS, ttl / 2)
        _index = (_now() + _rng.uniform(ttl - spread, ttl + spread), index)
    return index


def _failed(reason: str) -> None:
    """Record a failed refresh and back off. `reason` must be safe to log (rule 4)."""
    global _retry_at
    _counts["refresh_failures"] += 1
    backoff = _rng.uniform(*_BACKOFF_SECONDS)
    _retry_at = _now() + backoff
    logger.warning(
        "ic2 unavailable: %s; next try in %.0fs (%d failed refreshes in this process)",
        reason, backoff, _counts["refresh_failures"],
    )


def _running_refresh() -> asyncio.Task[Ic2Index | None] | None:
    """The refresh in flight on this event loop, if any.

    A task left behind by a dead loop is dropped rather than awaited, which would
    raise. Unreachable on ECS (one loop for the process's life) but reachable under
    `--reload` and in tests; the same hazard `inventory/client.py::_lock` handles.
    """
    global _refresh
    task = _refresh
    if task is None:
        return None
    if task.get_loop() is not asyncio.get_running_loop():
        logger.warning("ic2 refresh was bound to a dead loop; replacing")
        _refresh = None
        return None
    return task


def _start_refresh() -> asyncio.Task[Ic2Index | None]:
    global _refresh
    task = asyncio.get_running_loop().create_task(_refresh_index())
    _refresh = task

    def _done(t: asyncio.Task) -> None:
        global _refresh
        if _refresh is t:
            _refresh = None

    task.add_done_callback(_done)
    return task


async def positions() -> Ic2Index | None:
    """Every visible router's latest position, by normalized serial; None if IC2 is
    off or could not be read. Never raises.

    Once an index has been read, an expired one is still served (refreshed behind
    the caller) rather than None. Only a process that has never read IC2 waits.
    """
    if not is_enabled():
        return None
    entry = _index
    if entry is not None and entry[0] > _now():
        return entry[1]
    if _now() < _retry_at:
        return entry[1] if entry is not None else None
    # No `await` between looking for a refresh and starting one, so two callers
    # cannot both start one.
    task = _running_refresh() or _start_refresh()
    if entry is not None:
        # The last good index, served at once while the refresh runs, and kept if it
        # fails: a position a few minutes old is more use than "unavailable", and
        # every row already says how old its report is.
        return entry[1]
    # Shielded: this caller going away (a closed tab) must not cancel a refresh other
    # callers are waiting on.
    return await asyncio.shield(task)
