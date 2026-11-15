"""One central made of every host's central drive (operator 2026-11-14: "each host may have its own central drive,
and they are necessarily to all be considered a single central repo when connected to core to distribute to any
associated wrapper").

  refresh(worker)      intake, every REFRESH_S per worker: its Wrapper's GET /v1/central -> fleet_central_units
  catalog()            the merged catalog: each model once, with every host that holds it
  fetch(dest, ...)     Core arranges a copy onto ``dest``'s central drive from a host that holds the model. Core
                       needs no central drive of its own: the holders are the hosts. First the holder confirms (its
                       Wrapper's POST /v1/central/offer: the files are on its drive whole, and it shares its central),
                       and only then is the destination sent the request, ready: the holder's confirmed files and a
                       token for that one copy bound to the holder's offer (operator 2026-11-15: "send it ready with a
                       confirm from the wrapper who has the model to upload from"). The destination Wrapper pulls
                       32 MiB ranges through Core's relay (web/worker_link.py /fleet-link/relay/<token>/file),
                       verifies each file and hands the model to its Discovery. Core never touches a drive.

A model reaches a worker drive only from its own host's central (Discovery's units are central records), so a copy
from another host lands on the destination's central, then goes to its worker drive the usual way.

Retires the October relay (web/transfer_relay.py, delegate_transfer): those named the fitevict Wrapper's
/v1/transfer routes, which no Wrapper serves since the rewrite.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import secrets
import time

REFRESH_S = 300
TOKEN_TTL_S = 7 * 24 * 3600            # a copy of a large model over a slow link takes days, not minutes
_LAST: dict = {}


def _connect():
    import psycopg
    from psycopg.rows import dict_row
    from hugpy_core.imports.functions import core_dsn
    return psycopg.connect(core_dsn(), row_factory=dict_row, connect_timeout=5)


# ------------------------------------------------------------------------------------------------ intake

def refresh(worker, get, *, force=False) -> bool:
    """Read ``worker``'s central models (GET /v1/central) when REFRESH_S has passed; replace its rows."""
    name = worker["name"]
    if not force and time.time() - _LAST.get(name, 0) < REFRESH_S:
        return False
    _LAST[name] = time.time()
    doc = get(worker, "/v1/central", 120)
    units = doc.get("units") if isinstance(doc, dict) else None
    if not isinstance(units, list):
        return False
    with _connect() as conn:
        conn.execute("DELETE FROM fleet_central_units WHERE holder = %s", (name,))
        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO fleet_central_units(holder, key, variation, bytes, engine, files, content_id, basis, "
                "source_role, locations, task, arch, layers, ctx_train, expert_count, expert_used_count) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (holder, key, variation) DO NOTHING",
                [(name, u["key"], u["variation"], int(u.get("bytes") or 0), u.get("engine"), u.get("files"),
                  u.get("content_id"), u.get("basis"), u.get("source_role") or "central",
                  json.dumps(u.get("locations") or []), u.get("task"), u.get("arch"), _int(u.get("layers")),
                  _int(u.get("ctx_train")), _int(u.get("expert_count")), _int(u.get("expert_used_count")))
                 for u in units if u.get("key") and u.get("variation")])
        # into the model key index the console pages through: every model this host's Discovery has, one row a key
        try:
            from hugpy_core.models import current_catalog
            current_catalog.replace(conn, f"fleet:{name}", _index_rows(units))
        except Exception as exc:  # noqa: BLE001  the fleet table stands; the index catches up next refresh
            import logging
            logging.getLogger(__name__).warning("%s: fleet models not indexed: %s", name, exc)
    return True


FRAMEWORK_OF_ENGINE = {"llama-server": "gguf", "ollama": "gguf", "transformers": "transformers", "vision": "transformers",
                       "videogen": "diffusers", "imagegen": "diffusers", "comfy": "comfyui", "tts": "transformers",
                       "asr": "transformers", "embed": "sentence-transformers", "vllm": "vllm", "sglang": "sglang"}


def framework_of(engine, variation=""):
    if str(variation or "").lower().endswith(".gguf"):
        return "gguf"
    return FRAMEWORK_OF_ENGINE.get(engine or "", engine)


def _index_rows(units) -> list:
    """One index row a model key, from a host's units: its task and framework (Discovery's)."""
    rows = {}
    for u in units:
        if not u.get("key") or not servable(u):
            continue
        r = rows.setdefault(u["key"], {"id": u["key"], "primary_task": None, "framework": None})
        r["primary_task"] = r["primary_task"] or u.get("task")
        r["framework"] = r["framework"] or framework_of(u.get("engine"), u.get("variation"))
    return list(rows.values())


def _int(v):
    try:
        return int(v) if v is not None else None
    except (TypeError, ValueError):
        return None


# ------------------------------------------------------------------------------------------------ catalog

def _connected() -> set:
    """The workers whose central drives are part of the one central now: saved and switched on."""
    from hugpy_core.registry import registrations
    return {c["name"] for c in registrations.all() if registrations.is_connected(c)}


def _all_rows():
    with _connect() as conn:
        return conn.execute("SELECT holder, key, variation, bytes, engine, files, content_id, basis, seen_at, "
                            "source_role, locations, task, arch, layers, ctx_train, expert_count, expert_used_count "
                            "FROM fleet_central_units ORDER BY key, variation, holder").fetchall()


def rows():
    """Every connected host's central models (a disconnected worker's drive is not offered as a holder)."""
    live = _connected()
    return [r for r in _all_rows() if r["holder"] in live]


def servable(row) -> bool:
    """An entry a Wrapper can serve or Discovery recognises as a model: an engine, or at least a task. Entries with
    neither (a pip cache, backups and blobs a drive also holds) stay out of the model lists (2026-11-15, a-brain)."""
    return bool(row.get("engine") or row.get("task"))


def catalog(include_unservable=False) -> list:
    """Each model once: {key, variation, bytes, engine, content_id, basis, holders: [{holder, ...}]}. Copies are one
    model when their content ids agree; without ids, when key, variation and bytes do."""
    merged, by_name = {}, {}
    rs = rows()
    # proved copies first: one model per content id; then a copy not proved yet (a fresh copy its host's discovery
    # has not hashed) joins the proved model of its key, variation and size, as an unverified holder (2026-11-14:
    # a copy fetched from ae stood apart from ae's own until its new host proved it)
    if not include_unservable:
        rs = [r for r in rs if servable(r)]
    for r in sorted(rs, key=lambda r: r["content_id"] is None):
        name = (r["key"], r["variation"], r["bytes"])
        if r["content_id"]:
            ident = ("cid", r["content_id"])
        else:
            ident = by_name.get(name) or ("size",) + name
        m = merged.setdefault(ident, dict(key=r["key"], variation=r["variation"], bytes=r["bytes"], engine=r["engine"],
                                          content_id=r["content_id"], basis=r["basis"], holders=[]))
        by_name.setdefault(name, ident)
        roles = sorted({loc.get("role") for loc in (r.get("locations") or []) if loc.get("role")}
                       or {r.get("source_role") or "central"})
        m["holders"].append(dict(holder=r["holder"], key=r["key"], variation=r["variation"], roles=roles,
                                 source_role=r.get("source_role") or "central",
                                 verified=bool(r["content_id"]) and r["content_id"] == m["content_id"],
                                 seen_at=r["seen_at"].isoformat() if r["seen_at"] else None))
        m["engine"] = m["engine"] or r["engine"]
        for fact in ("task", "arch", "layers", "ctx_train", "expert_count", "expert_used_count"):
            if m.get(fact) is None and r.get(fact) is not None:
                m[fact] = r[fact]
    return sorted(merged.values(), key=lambda m: (m["key"], m["variation"]))


def by_key() -> dict:
    """The fleet models database by model key: {key: {variations: [catalog entries], hosts, roles, task, engine,
    arch, layers, ctx_train, bytes_min}} (one entry per key, for the console's model lists)."""
    out = {}
    for m in catalog():
        k = out.setdefault(m["key"], dict(variations=[], hosts=set(), task=None, engine=None, arch=None, layers=None,
                                          ctx_train=None))
        k["variations"].append(m)
        k["hosts"].update(h["holder"] for h in m["holders"])
        for fact in ("task", "engine", "arch", "layers", "ctx_train"):
            k[fact] = k[fact] or m.get(fact)
    for k in out.values():
        k["hosts"] = sorted(k["hosts"])
    return out


def holders(key, variation) -> list:
    live = _connected()
    with _connect() as conn:
        return [r for r in conn.execute("SELECT * FROM fleet_central_units WHERE key = %s AND variation = %s "
                                        "ORDER BY holder", (key, variation)).fetchall() if r["holder"] in live]


# ------------------------------------------------------------------------------------------------ the relay token

def _secret() -> bytes:
    path = os.path.join(os.environ.get("HUGPY_CORE_STATE_DIR")
                        or os.path.expanduser("~/.local/share/hugpy/core"), "relay.secret")
    try:
        with open(path, "rb") as fh:
            value = fh.read().strip()
        if value:
            return value
    except OSError:
        pass
    os.makedirs(os.path.dirname(path), exist_ok=True)
    value = secrets.token_urlsafe(48).encode()
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as fh:
        fh.write(value)
    return value


def mint(holder, key, variation, dest, ttl=TOKEN_TTL_S, offer=None) -> str:
    claims = dict(h=holder, k=key, v=variation, d=dest, o=offer, e=int(time.time() + ttl))
    body = base64.urlsafe_b64encode(json.dumps(claims, separators=(",", ":")).encode()).decode().rstrip("=")
    sig = hmac.new(_secret(), body.encode(), hashlib.sha256).hexdigest()
    return f"hcr1.{body}.{sig}"


def verify(token: str):
    """The token's claims {h, k, v, d, e} when it is Core's and unexpired; else None."""
    try:
        kind, body, sig = token.split(".")
    except ValueError:
        return None
    if kind != "hcr1" or not hmac.compare_digest(sig, hmac.new(_secret(), body.encode(), hashlib.sha256).hexdigest()):
        return None
    try:
        claims = json.loads(base64.urlsafe_b64decode(body + "=" * (-len(body) % 4)))
    except ValueError:
        return None
    return claims if isinstance(claims, dict) and claims.get("e", 0) > time.time() else None


# ------------------------------------------------------------------------------------------------ suggesting a copy

def _base_for(dest_worker) -> str:
    """Where ``dest`` reaches Core: this process directly when it is the Wrapper on Core's own host, else Core's
    public base (a linked worker, a LAN worker)."""
    from urllib.parse import urlsplit
    from hugpy_core.imports.functions import self_base
    from hugpy_core.web.worker_link import internal_base
    host = urlsplit(dest_worker.get("url") or "").hostname or ""
    if not dest_worker.get("link") and host in ("127.0.0.1", "localhost", "::1"):
        return internal_base()
    return self_base().rstrip("/")


MAX_SOURCES = 3                 # holders a copy pulls from at once (each confirmed, all agreeing on the files)
LIVE = ("sent", "copying")


def _same_files(a, b) -> bool:
    """The same files: one path and size each, and no sha256 that contradicts the other's (a holder whose copy is
    not proved yet has none)."""
    one, two = {f["rel"]: f for f in a}, {f["rel"]: f for f in b}
    if one.keys() != two.keys():
        return False
    for rel, f in one.items():
        g = two[rel]
        if int(f["bytes"]) != int(g["bytes"]) or (f.get("sha256") and g.get("sha256") and f["sha256"] != g["sha256"]):
            return False
    return True


def _live_copy(dest, key, variation):
    with _connect() as conn:
        return conn.execute("SELECT * FROM fleet_central_copies WHERE dest = %s AND key = %s AND variation = %s "
                            "AND finished_at IS NULL ORDER BY id DESC LIMIT 1", (dest, key, variation)).fetchone()


def fetch(dest, key, variation, holder=None, reason="operator") -> dict:
    """Arrange a copy of (key, variation) onto ``dest``'s central drive. The holders confirm first (up to
    MAX_SOURCES, all agreeing on the files); only then is ``dest`` sent the request, ready, with every confirmed
    holder to pull from. -> {state: present | copying (one already is) | sent, copy, holders, ...}."""
    from hugpy_core.registry import registrations, transport
    dest_worker = registrations.get(dest)
    if not dest_worker:
        raise LookupError(f"no worker {dest}")
    held = holders(key, variation)
    if any(h["holder"] == dest for h in held):
        return dict(state="present", message=f"{key}::{variation} is already on {dest}'s central drive")
    live = _live_copy(dest, key, variation)
    if live:
        return dict(state="copying", copy=live["id"], message=f"a copy of {key}::{variation} to {dest} is in flight")
    candidates = [h for h in held if not holder or h["holder"] == holder]
    if not candidates:
        raise LookupError(f"no connected host's central drive holds {key}::{variation}"
                          + (f" (asked: {holder})" if holder else ""))
    # a proved copy before an unproved one, a holder Core reaches directly before one behind a link
    candidates.sort(key=lambda h: (not h.get("content_id"), bool((registrations.get(h["holder"]) or {}).get("link")),
                                   h["holder"]))
    confirmed, declined = [], []
    for h in candidates:
        if len(confirmed) >= MAX_SOURCES:
            break
        holder_worker = registrations.get(h["holder"])
        if not holder_worker:
            continue
        try:                               # each holder confirms before the destination is told anything
            got = transport.request(holder_worker, "/v1/central/offer",
                                    dict(key=key, variation=variation, dest=dest, ttl=TOKEN_TTL_S), timeout=120)
        except (RuntimeError, OSError, ValueError) as exc:
            declined.append(f"{h['holder']}: {exc}")
            continue
        if not (got.get("offer") and got.get("files")):
            declined.append(f"{h['holder']}: no offer in its answer")
            continue
        if confirmed and not _same_files(confirmed[0][1]["files"], got["files"]):
            declined.append(f"{h['holder']}: its files are not the first holder's")
            _close(holder_worker, got["offer"])
            continue
        confirmed.append((holder_worker, got))
    if not confirmed:
        raise LookupError(f"no holder of {key}::{variation} confirmed an upload to {dest}: " + "; ".join(declined))
    base = _base_for(dest_worker)
    sources = []
    for w, got in confirmed:
        token = mint(w["name"], key, variation, dest, offer=got["offer"])
        sources.append(dict(holder=w["name"], offer=got["offer"], url=f"{base}/fleet-link/relay/{token}", token=token))
    files = confirmed[0][1]["files"]
    total = sum(int(f.get("bytes") or 0) for f in files)
    copy_id = _insert_copy(dest, key, variation, [dict(holder=s["holder"], offer=s["offer"]) for s in sources],
                           reason, total)
    job = dict(key=key, variation=variation, files=files, holder=sources[0]["holder"], offer=confirmed[0][1],
               copy=copy_id, sources=sources, source=dict(url=sources[0]["url"], token=sources[0]["token"]))
    try:
        started = transport.request(dest_worker, "/v1/central/fetch", job, timeout=60)
    except (RuntimeError, OSError, ValueError) as exc:
        finish(copy_id, "failed", error=f"{dest} did not take the copy: {exc}")
        raise
    return dict(state="sent", copy=copy_id, holder=sources[0]["holder"], holders=[s["holder"] for s in sources],
                dest=dest, offer=sources[0]["offer"], confirmed_at=confirmed[0][1].get("confirmed_at"),
                files=len(files), bytes=total, declined=declined, fetch=started)


def _insert_copy(dest, key, variation, sources, reason, total) -> int:
    with _connect() as conn:
        return conn.execute("INSERT INTO fleet_central_copies(dest, key, variation, sources, reason, bytes) "
                            "VALUES (%s,%s,%s,%s,%s,%s) RETURNING id",
                            (dest, key, variation, json.dumps(sources), reason, total)).fetchone()["id"]


def _close(holder_worker, offer_id) -> None:
    from hugpy_core.registry import transport
    try:
        transport.request(holder_worker, "/v1/central/offer/close", dict(offer=offer_id), timeout=30)
    except (RuntimeError, OSError, ValueError):
        pass                                # it expires by itself


def finish(copy_id, state, error=None) -> None:
    """A copy over (done, failed, cancelled): recorded, and every holder's offer for it closed."""
    from hugpy_core.registry import registrations
    with _connect() as conn:
        row = conn.execute("UPDATE fleet_central_copies SET state=%s, error=COALESCE(%s, error), finished_at=now(), "
                           "updated_at=now() WHERE id=%s AND finished_at IS NULL RETURNING sources",
                           (state, error, copy_id)).fetchone()
    for src in (row or {}).get("sources") or []:
        w = registrations.get(src.get("holder"))
        if w:
            _close(w, src.get("offer"))


def track(worker, get) -> int:
    """Intake: ``worker``'s copies in flight (its GET /v1/central/fetches) onto Core's rows; a finished one is
    finished here (its holders' offers closed). -> how many rows changed."""
    with _connect() as conn:
        live = conn.execute("SELECT id, key, variation FROM fleet_central_copies WHERE dest = %s AND finished_at IS NULL",
                            (worker["name"],)).fetchall()
    if not live:
        return 0
    doc = get(worker, "/v1/central/fetches", 30)
    seen = {f.get("model"): f for f in (doc.get("fetches") or [])} if isinstance(doc, dict) else {}
    changed = 0
    for row in live:
        f = seen.get(f"{row['key']}::{row['variation']}")
        if f is None:
            continue
        with _connect() as conn:
            conn.execute("UPDATE fleet_central_copies SET state=%s, done_bytes=%s, rate_bytes_per_s=%s, now_file=%s, "
                         "bytes=GREATEST(bytes, %s), error=%s, updated_at=now() WHERE id=%s",
                         ("copying" if f.get("state") == "copying" else f.get("state"), int(f.get("done_bytes") or 0),
                          f.get("rate_bytes_per_s"), f.get("now"), int(f.get("total_bytes") or 0), f.get("error"),
                          row["id"]))
        if f.get("state") in ("done", "failed", "cancelled"):
            finish(row["id"], f["state"], error=f.get("error"))
        changed += 1
    return changed


def copies(limit=200) -> list:
    with _connect() as conn:
        rows = conn.execute("SELECT * FROM fleet_central_copies ORDER BY id DESC LIMIT %s", (int(limit),)).fetchall()
    out = []
    for r in rows:
        d = dict(r)
        for k in ("created_at", "updated_at", "finished_at"):
            d[k] = d[k].isoformat() if d.get(k) else None
        out.append(d)
    return out


def cancel(copy_id) -> dict:
    from hugpy_core.registry import registrations, transport
    with _connect() as conn:
        row = conn.execute("SELECT * FROM fleet_central_copies WHERE id = %s", (int(copy_id),)).fetchone()
    if not row:
        raise LookupError(f"no copy {copy_id}")
    if row["finished_at"]:
        return dict(copy=row["id"], state=row["state"])
    dest = registrations.get(row["dest"])
    if dest:
        try:
            transport.request(dest, "/v1/central/fetch/cancel", dict(model=f"{row['key']}::{row['variation']}"), timeout=30)
        except (RuntimeError, OSError, ValueError):
            pass
    finish(row["id"], "cancelled")
    return dict(copy=row["id"], state="cancelled")


def wait(dest, key, variation, timeout) -> dict:
    """Block until ``dest`` has (key, variation) served (its copy done and its catalog showing it), or ``timeout``.
    -> the copy's last state {state, done_bytes, bytes, error}."""
    from hugpy_core.registry import registrations, transport
    worker = registrations.get(dest)
    name, deadline, last = f"{key}::{variation}", time.time() + timeout, {}
    while time.time() < deadline:
        try:
            doc = transport.request(worker, "/v1/central/fetches", timeout=30)
            last = next((f for f in doc.get("fetches") or [] if f.get("model") == name), last)
        except (RuntimeError, OSError, ValueError):
            pass
        if last.get("state") in ("failed", "cancelled"):
            return last
        if last.get("state") == "done":
            try:                            # served once the destination's catalog has it (discovery's refresh)
                ids = {m.get("id") for m in transport.request(worker, "/v1/models", timeout=30).get("data") or []}
                if name in ids:
                    return dict(last, served=True)
            except (RuntimeError, OSError, ValueError):
                pass
        time.sleep(5)
    return dict(last, state=last.get("state") or "waiting", timed_out=True)


# ------------------------------------------------------------------------------------------------ calls

CALL_COPY_WAIT_S = float(os.environ.get("HUGPY_CALL_COPY_WAIT_S") or 1800)


class CopyPending(Exception):
    """The call's model is being copied to its worker; the copy goes on (a retry is served once it is there)."""
    status = 503


def resolve(model_key):
    """(key, variation) of the one central's model a call names, or None: key::variation as given; a bare key gets
    its proved variation first, then its smallest."""
    key, _, variation = str(model_key or "").partition("::")
    ms = [m for m in catalog() if m["key"].lower() == key.lower() and (not variation or m["variation"] == variation)]
    if not ms:
        return None
    ms.sort(key=lambda m: (not m["content_id"], int(m["bytes"] or 0)))
    return ms[0]["key"], ms[0]["variation"]


def provide(model_key, candidates, rank=None, timeout=None):
    """A call names a model no eligible worker has, but a connected host's central drive does: copy it to the worker
    routing would choose (``candidates`` in ``rank`` order; one refusing, for room or a central drive, passes to the
    next), wait until it is served there, and return that worker. None when no central holds it."""
    found = resolve(model_key)
    if not found:
        return None
    key, variation = found
    from hugpy_core.registry import registrations
    ordered = sorted(candidates, key=rank) if rank else list(candidates)
    refused = []
    for w in ordered:
        name = w.get("name") or w.get("id")
        if not registrations.get(name):
            continue
        try:
            sent = fetch(name, key, variation, reason="call")
        except LookupError:
            raise                            # no holder confirmed: another destination would not change that
        except (RuntimeError, OSError, ValueError) as exc:
            refused.append(f"{name}: {exc}")
            continue
        if sent.get("state") == "present":           # it holds it already: nothing to wait for
            return w
        last = wait(name, key, variation, CALL_COPY_WAIT_S if timeout is None else timeout)
        if last.get("served"):
            return w
        if last.get("state") in ("failed", "cancelled"):
            raise RuntimeError(f"copying {key}::{variation} to {name} {last['state']}: {last.get('error')}")
        done, total = int(last.get("done_bytes") or 0), int(last.get("total_bytes") or sent.get("bytes") or 0)
        raise CopyPending(f"{key}::{variation} is being copied to {name} from another host's central drive "
                          f"({done / 2**30:.1f} of {total / 2**30:.1f} GiB); it is served there once whole: retry")
    if refused:
        raise RuntimeError(f"no worker took a copy of {key}::{variation}: " + "; ".join(refused))
    return None


def relay_range(claims, rel, offset, length):
    """Bytes of a file of the token's model from its holder (direct, or over the holder's link) -> (status, bytes)."""
    import urllib.parse
    import urllib.request
    import urllib.error
    from hugpy_core.registry import registrations, transport
    holder = registrations.get(claims["h"])
    if not holder:
        return 404, json.dumps({"error": f"{claims['h']} is no longer a connected worker"}).encode()
    # the holder serves only within the offer it confirmed for this copy (the token carries it)
    q = urllib.parse.urlencode(dict(offer=claims.get("o") or "", rel=rel, offset=offset, length=length))
    req = urllib.request.Request(holder["url"].rstrip("/") + f"/v1/central/file?{q}", headers=transport.headers(holder))
    try:
        with urllib.request.urlopen(req, timeout=600) as reply:
            return 200, reply.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()
