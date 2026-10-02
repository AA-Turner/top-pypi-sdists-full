"""The few Probe reads the daemon's plain code makes itself (not through the CLI).

Facts for an approval question come from Probe, never from the model: what a
delete would trash, and who made it (`DELETE ...?dry_run=true`, S13).

A dry-run DELETE is still a DELETE: a server that does not know `dry_run`
ignores it and deletes. So the preview is sent only to a server that declares
the trash (`GET /v1/server/features` lists "trash", which S13 ships with), and
the daemon deletes nothing anywhere else (`precheck.NO_TRASH`).

A 401, or a 403 that names a gone team or membership (`sdk/key_refusal.py`),
on any of these calls raises `KeyRefused`: Probe refused the daemon's KEY, and
the tools stop the bite and hand the session back, as they do when the CLI
prints `KEY_REFUSED_LINE`. A 403 for a missing scope is not that.
"""

from __future__ import annotations

import re
import time
from urllib.parse import quote

import httpx

from probe.sdk.config import DEFAULT_BASE_URL
from probe.sdk.key_refusal import credential_refused
from probe.sdk.tls import ssl_context

TIMEOUT_S = 30.0
#: The feature a server declares when a delete goes to its trash and
#: `?dry_run=true` previews one (S13).
TRASH = "trash"
#: What a ref the model hands to a delete may look like: a slug, a uuid, either
#: behind `id:`. No `/ ? # %`, no `..`, no whitespace: the ref becomes one path
#: segment, and anything else could reach another route.
_REF_RE = re.compile(r"^(id:)?[A-Za-z0-9][A-Za-z0-9_.:-]{0,199}$")

#: The last answer to `GET /v1/server/features`, and until when it holds.
_features: frozenset[str] | None = None
_features_until = 0.0
#: How long a server's "I declare nothing" (a 404) is believed before it is asked
#: again: a server upgraded while the daemon runs is noticed within this.
NO_FEATURES_RECHECK_S = 300.0
_clock = time.monotonic


class BadRef(ValueError):
    """A ref that is not a slug or an id."""


class Unreachable(RuntimeError):
    """Probe could not be asked (no answer, or an error): try again later."""


class KeyRefused(RuntimeError):
    """Probe refused the daemon's key itself (a 401, or a 403 naming the credential)."""


def _refuse_key(resp: httpx.Response) -> None:
    """Raise `KeyRefused` when this answer refuses the credential (not a scope)."""
    try:
        detail = resp.json().get("detail")
    except (ValueError, AttributeError):
        detail = None
    message = detail.get("message") if isinstance(detail, dict) else detail
    if credential_refused(resp.status_code, message if isinstance(message, str) else resp.text):
        raise KeyRefused(f"{resp.request.method} {resp.request.url.path}: HTTP {resp.status_code}")


def valid_ref(ref: str) -> str:
    """`ref` when it is a slug, a uuid or `id:<uuid>`; else BadRef. Checked before any request."""
    if not isinstance(ref, str) or not _REF_RE.fullmatch(ref) or ".." in ref:
        raise BadRef(f"{ref!r} is not a slug or an id")
    return ref


async def _client(env: dict[str, str]) -> httpx.AsyncClient:
    base = env.get("PROBE_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
    return httpx.AsyncClient(base_url=base, timeout=TIMEOUT_S, verify=ssl_context(),
                             headers={"Authorization": f"Bearer {env.get('PROBE_TOKEN', '')}"})


async def whoami(env: dict[str, str]) -> dict:
    async with await _client(env) as client:
        resp = await client.get("/v1/me")
        _refuse_key(resp)
        resp.raise_for_status()
        return resp.json()


async def server_features(env: dict[str, str]) -> frozenset[str] | None:
    """What the server declares it can do (`GET /v1/server/features`). A listing is
    kept for the process's life; a server without the route (404) declares
    nothing, re-asked after `NO_FEATURES_RECHECK_S`. None when Probe could not be
    asked (no answer, an error, a body that is not a listing): NOT cached, and
    never read as "no trash". `KeyRefused` when Probe refused the key."""
    global _features, _features_until
    if _features is not None and _clock() < _features_until:
        return _features
    try:
        async with await _client(env) as client:
            resp = await client.get("/v1/server/features")
    except httpx.HTTPError:
        return None
    _refuse_key(resp)
    if resp.status_code == 404:
        _features, _features_until = frozenset(), _clock() + NO_FEATURES_RECHECK_S
        return _features
    if resp.status_code != 200:
        return None
    try:
        listed = resp.json().get("features")
    except (ValueError, AttributeError):
        return None
    if not isinstance(listed, list):
        return None
    _features, _features_until = frozenset(f for f in listed if isinstance(f, str)), float("inf")
    return _features


async def has_trash(env: dict[str, str]) -> bool | None:
    """Does the server declare the trash? None: Probe could not be asked."""
    features = await server_features(env)
    return None if features is None else TRASH in features


async def deletion_preview(env: dict[str, str], kind: str, ref: str, *, recursive: bool = False) -> dict | None:
    """`{"id", "name", "what", "count", "others": {"<user>|<kind>": n}, "updated_at",
    "restorable_until"}`. When the server cannot say, the delete is treated as
    reaching others' data, and the daemon asks.

    Sent ONLY to a server that declares the trash: anywhere else a dry-run DELETE
    may be a real one, so this raises instead of sending it. `recursive` only when
    the command itself asked for it."""
    ref = valid_ref(ref).removeprefix("id:")
    if await has_trash(env) is not True:
        raise RuntimeError("the server declares no trash (or could not be asked): a dry-run delete is not sent")
    segment = quote(ref, safe="")
    async with await _client(env) as client:
        params = {"dry_run": "true"}
        if recursive and kind in ("project", "experiment"):
            params["recursive"] = "true"
        # Literal f-strings, one per route: tests/test_parity.py reads the path
        # at the call site. An experiment IS a project row (same uuid).
        if kind == "run":
            resp = await client.delete(f"/v1/runs/{segment}", params=params)
        elif kind in ("project", "experiment"):
            resp = await client.delete(f"/v1/projects/{segment}", params=params)
        else:
            raise KeyError(kind)
        _refuse_key(resp)
        if resp.status_code != 200:
            return {"id": ref, "name": ref, "what": kind, "others": {"unknown owner|items": 1},
                    "count": None, "updated_at": None}
        data = resp.json()
        me = _who((await whoami(env)).get("user_id")) if data.get("created_by") else None
        return {"id": data.get("id", ref), "name": data.get("name") or ref, "what": kind,
                "others": others_from(data.get("created_by"), me),
                "count": data.get("count"), "updated_at": data.get("updated_at"),
                "restorable_until": data.get("restorable_until")}


async def edge(env: dict[str, str], edge_id: str) -> dict:
    """One lineage edge (`GET /v1/edges/{id}`), with its `meta`. Raises on any
    answer but a 200 carrying an object -- a server without the route answers
    404, like a missing edge -- and `KeyRefused` when Probe refused the key."""
    segment = quote(valid_ref(edge_id).removeprefix("id:"), safe="")
    async with await _client(env) as client:
        resp = await client.get(f"/v1/edges/{segment}")
        _refuse_key(resp)
        resp.raise_for_status()
        data = resp.json()
    if not isinstance(data, dict):
        raise ValueError("the edge is not an object")
    return data


async def edge_is_this_daemons(env: dict[str, str], edge_id: str) -> bool:
    """Did THIS researcher's daemon make the edge? True only when Probe says so:
    the server stamps a daemon key's link `provenance = "inferred"`, `meta.via =
    "daemon"` and `meta.by` = the key's user (lineage plan L1), and `meta.by`
    must be the user this key answers to now (`GET /v1/me`). Another
    researcher's daemon's link is not (R9). Raises when either read fails: the
    caller then asks (fail closed).

    This trusts the STAMP, so it is only as good as the server's rule that no
    caller can write it: the server strips `meta.via` / `meta.by` from every
    other key's edge and overwrites them on a daemon key's (lineage2-server
    `app/lineage/service.py`). The provenance check is a second belt: the same
    stamp sets it, and a person's link is never `inferred` by that door."""
    row = await edge(env, edge_id)
    meta = row.get("meta")
    if row.get("provenance") != "inferred" or not isinstance(meta, dict) or meta.get("via") != "daemon":
        return False
    by, me = _who(meta.get("by")), _who((await whoami(env)).get("user_id"))
    return bool(by) and by == me


#: What `others_from` answers when it cannot read the tally: someone else's data.
UNKNOWN_OTHERS = {"unknown owner|items": 1}


def others_from(created_by: object, me: str | None) -> dict[str, int]:
    """`{"<who>|<kind>": n}` for everything another researcher made. A kind with
    nothing in it is no one's data (only n > 0 counts); an unknown creator is
    someone else. A tally in a shape this code does not know (not a dict of
    dicts of counts) FAILS CLOSED: it is someone else's data, and the delete asks."""
    if not isinstance(created_by, dict):
        return dict(UNKNOWN_OTHERS)
    others: dict[str, int] = {}
    for who, kinds in created_by.items():
        if not isinstance(kinds, dict):
            return dict(UNKNOWN_OTHERS)
        mine = me is not None and _who(who) == me
        for what, n in kinds.items():
            if isinstance(n, bool):
                return dict(UNKNOWN_OTHERS)
            try:
                count = int(n)
            except (TypeError, ValueError):
                return dict(UNKNOWN_OTHERS)
            if count > 0 and not mine:
                others[f"{who}|{what}"] = count
    return others


def _who(value: object) -> str:
    """`user:<uuid>` and `<uuid>` name the same person."""
    return str(value or "").removeprefix("user:").strip().lower()
