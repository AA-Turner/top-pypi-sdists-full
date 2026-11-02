"""The console SETTINGS surface + the box relay (secrets architecture, step 2).

Operator ruling 2026-10-03: the toolserver is the engine room (vault, box
enrollment, per-box Postgres roles, artifacts, audit); hugpy_core's Settings page
is the client face; boxes talk only to hugpy_core, which relays to the toolserver.

Two surfaces live here:

  OPERATOR (/settings/*, operator-only — see operator_only):
    GET  /settings/boxes                    toolserver /boxes/list
    POST /settings/boxes/enroll-token       toolserver /boxes/enroll_token (+ install_cmd)
    POST /settings/boxes/revoke             toolserver /boxes/revoke
    GET  /settings/secrets                  toolserver /vault/list (metadata only)
    POST /settings/secrets/set              toolserver /vault/set     (write-only, no echo)
    POST /settings/secrets/rotate           toolserver /vault/rotate  (write-only, no echo)
    POST /settings/secrets/grant            toolserver /vault/grant
    POST /settings/secrets/revoke           toolserver /vault/revoke
    POST /settings/secrets/delete           toolserver /vault/delete
    GET  /settings/audit                    toolserver /vault/audit
    GET  /settings/artifacts                operator artifacts (toolserver offers
                                            these only inside a box bundle, so empty)
    GET  /settings/policies                 core DB policies + read-only env display
    POST /settings/policies                 write core DB policies

  BOX RELAY (open / box-token — a box talks only to core, never the toolserver):
    POST /boxes/enroll            (open)       -> toolserver /boxes/enroll
    POST /boxes/bundle            (box-token)  -> toolserver /boxes/bundle
    POST /boxes/bundle_version    (box-token)  -> toolserver /boxes/bundle_version

The toolserver operator token lives server-side only (env
HUGPY_CORE_TOOLSERVER_TOKEN); the browser never sees it. Set/rotate responses
never echo secret values. Every error is JSON, never HTML.
"""
from __future__ import annotations

import functools
import json
import logging
import os
import urllib.error
import urllib.request

from hugpy_core.imports.functions import self_base
from hugpy_core.models.modeldb import _conn

logger = logging.getLogger("hugpy_core")

TOOLSERVER_URL = os.environ.get("HUGPY_CORE_TOOLSERVER_URL", "http://127.0.0.1:7004")
TOOLSERVER_TOKEN = os.environ.get("HUGPY_CORE_TOOLSERVER_TOKEN", "")


# ── toolserver client ────────────────────────────────────────────────────────
def _ts(path: str, payload: dict, operator: bool = False,
        timeout: float = 20.0) -> "tuple[int, dict]":
    """POST one JSON body to the toolserver; return (status, parsed_body).

    Operator routes carry X-Operator-Token (held server-side). The toolserver
    wraps success as {"result": ...} and errors as {"error": ...}; both are
    returned verbatim so the caller can pass the real message through."""
    url = TOOLSERVER_URL.rstrip("/") + path
    headers = {"Content-Type": "application/json"}
    if operator:
        headers["X-Operator-Token"] = TOOLSERVER_TOKEN
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"),
                                 headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, (json.loads(r.read().decode("utf-8") or "{}") or {})
    except urllib.error.HTTPError as exc:
        try:
            return exc.code, (json.loads(exc.read().decode("utf-8") or "{}") or {})
        except Exception:  # noqa: BLE001 — a bodyless error is still that status
            return exc.code, {"error": f"toolserver HTTP {exc.code}"}
    except urllib.error.URLError as exc:
        return 502, {"error": f"toolserver unreachable at {url}: {exc.reason}"}
    except Exception as exc:  # noqa: BLE001
        return 502, {"error": f"toolserver call to {url} failed: {type(exc).__name__}: {exc}"}


def _relay(path: str, payload: dict, operator: bool = False):
    """Call the toolserver and return its reply as JSON-able data.

    On success the {"result": ...} payload is unwrapped and returned; a
    toolserver error passes its real message through as {"error": ...}. Operator
    routes with no token configured fail loudly rather than hitting the
    toolserver. The registrar wraps/serialises the returned data; the toolserver
    client (_ts) and its {"result": ...}/{"error": ...} contract are unchanged."""
    if operator and not TOOLSERVER_TOKEN:
        return {"error": "hugpy_core has no toolserver operator token configured "
                         "(env HUGPY_CORE_TOOLSERVER_TOKEN); operator settings are unavailable"}
    status, body = _ts(path, payload, operator=operator)
    if status == 200 and isinstance(body, dict) and "result" in body:
        return body["result"]
    if isinstance(body, dict) and body.get("error"):
        return {"error": body["error"]}
    return {"error": f"toolserver {path} returned HTTP {status} with an unexpected body"}


def box_bundle_version(client_id: "str | None", token: "str | None") -> "str | None":
    """The box's current bundle version from the toolserver, or None when it
    cannot be read (no creds, toolserver down). Used to stamp register/heartbeat
    replies so a box refetches its env only when the version changes."""
    if not client_id or not token:
        return None
    status, body = _ts("/boxes/bundle_version", {"client_id": client_id, "token": token})
    if status == 200 and isinstance(body, dict):
        return (body.get("result") or {}).get("version")
    return None


# ── operator gate (single hook; central auth plugs in here later) ─────────────
def _operator_gate():
    """The one operator-auth hook for every /settings/* route. The console auth
    mode is 'open' today (see routes.auth_config), so this allows all callers;
    when central auth lands it decides here. LAN/WG-only enforcement stays at
    nginx (deny non-LAN for /api/settings/). Returns an {"error": ...} dict to
    deny (the registrar wraps it), or None to allow."""
    return None


def operator_only(fn):
    @functools.wraps(fn)
    def wrapper(*a, **k):
        denied = _operator_gate()
        if denied is not None:
            return denied
        return fn(*a, **k)
    return wrapper


# ── policies (core DB; the toolserver owns boxes/secrets/audit) ───────────────
# Allowed policy keys and their validators. storage.default_root is NOT here —
# it is a read-only display of the router's DEFAULT_ROOT env at GET time.
def _is_exclusions(v) -> bool:
    if not isinstance(v, list):
        return False
    for e in v:
        if not isinstance(e, dict) or not isinstance(e.get("model_key"), str):
            return False
        ex = e.get("exclude")
        if not isinstance(ex, list) or not all(isinstance(x, str) for x in ex):
            return False
    return True


def _is_bindings(v) -> bool:
    return isinstance(v, dict) and all(isinstance(k, str) and isinstance(m, str) and m
                                       for k, m in v.items())


def _is_model_preferences(value):
    from .model_preferences import valid
    return valid(value)


_POLICY_KEYS = {
    "model_preferences": _is_model_preferences,
    # task -> the model a task-only call (execute_prompt(task=...), /ml/<task>) is sent to
    "task_bindings": _is_bindings,
    "grading.judge_model": lambda v: v is None or isinstance(v, str),
    "updates.auto": lambda v: isinstance(v, bool),
    "exclusions": _is_exclusions,
    # THE BRAIN (operator 2026-10-06): its model (a hugpy-brain group member or any
    # model; None = automatic from the group), whether failures are auto-evaluated,
    # whether fixes are auto-IMPLEMENTED (the tick box), and the grade threshold a
    # model-inferred fix's brain must meet ({grader category: tiers passed}, default
    # coding 3/3 + logic 3/3) — below it a fix waits for operator approval
    "brain.model": lambda v: v is None or isinstance(v, str),
    "brain.auto": lambda v: isinstance(v, bool),
    "brain.auto_fix": lambda v: isinstance(v, bool),
    "brain.threshold": lambda v: _is_threshold(v),
}


def _is_threshold(v) -> bool:
    """{grader category: tiers that must pass, 0..tiers} over the grader's own categories."""
    if not isinstance(v, dict) or not v:
        return False
    try:
        from hugpy_core.grading import grader
        cats = {c for c, _t, _p, _k in grader.curriculum(grader.SUITE)}
        tiers = len(grader.TIER_ORDER)
    except Exception:  # noqa: BLE001
        return False
    return all(k in cats and isinstance(n, int) and not isinstance(n, bool) and 0 <= n <= tiers
               for k, n in v.items())


def read_policies() -> dict:
    """Every stored policy plus the read-only env displays, in the shape the
    Settings page binds to. Missing keys render as explicit defaults."""
    stored: dict = {}
    try:
        with _conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT key, value, updated_at, updated_by FROM settings_policies")
            for r in cur.fetchall():
                stored[r["key"]] = {"value": r["value"], "updated_at": r["updated_at"],
                                    "updated_by": r["updated_by"]}
    except Exception as exc:  # noqa: BLE001
        logger.warning("settings_policies read failed: %s", exc)
    from .model_preferences import read as read_model_preferences
    return {
        "model_preferences": read_model_preferences((stored.get("model_preferences") or {}).get("value")),
        "grading": {"judge_model": (stored.get("grading.judge_model") or {}).get("value")},
        "updates": {"auto": bool((stored.get("updates.auto") or {}).get("value") or False)},
        "brain": {"model": (stored.get("brain.model") or {}).get("value"),
                  "auto": (stored.get("brain.auto") or {}).get("value", True) is not False,
                  "auto_fix": (stored.get("brain.auto_fix") or {}).get("value", True) is not False,
                  "threshold": (stored.get("brain.threshold") or {}).get("value") or {"coding": 3, "logic": 3}},
        "exclusions": (stored.get("exclusions") or {}).get("value") or [],
        "task_bindings": (stored.get("task_bindings") or {}).get("value") or {},
        "storage": {"default_root": os.environ.get("DEFAULT_ROOT"), "editable": False},
        "updated": {k: v.get("updated_at") for k, v in stored.items()},
    }


def write_policies(doc: dict) -> "tuple[dict, list, int]":
    """Write the recognised keys present in ``doc``; return
    (result, rejected, accepted_count).

    Accepts either the nested read shape ({"grading":{"judge_model":...}}) or
    flat keys ({"grading.judge_model":...}). storage.default_root is read-only
    and is rejected. Returns the full re-read policy set."""
    from psycopg.types.json import Jsonb
    flat: dict = {}
    # nested -> flat for the keys we recognise
    if isinstance(doc.get("grading"), dict) and "judge_model" in doc["grading"]:
        flat["grading.judge_model"] = doc["grading"]["judge_model"]
    if isinstance(doc.get("updates"), dict) and "auto" in doc["updates"]:
        flat["updates.auto"] = doc["updates"]["auto"]
    if isinstance(doc.get("brain"), dict):
        for bk in ("model", "auto", "auto_fix", "threshold"):
            if bk in doc["brain"]:
                flat["brain." + bk] = doc["brain"][bk]
    if "exclusions" in doc:
        flat["exclusions"] = doc["exclusions"]
    if "task_bindings" in doc:
        flat["task_bindings"] = doc["task_bindings"]
    if "model_preferences" in doc:
        flat["model_preferences"] = doc["model_preferences"]
    for k in ("grading.judge_model", "updates.auto", "exclusions"):
        if k in doc:
            flat[k] = doc[k]
    rejected = []
    # storage.default_root is a read-only display of the router's env — a write
    # attempt is rejected explicitly rather than silently ignored.
    if ("storage.default_root" in doc
            or (isinstance(doc.get("storage"), dict) and "default_root" in doc["storage"])):
        rejected.append({"key": "storage.default_root",
                         "reason": "read-only (the router's DEFAULT_ROOT environment)"})
    accepted = {}
    for k, v in flat.items():
        chk = _POLICY_KEYS.get(k)
        if chk is None:
            rejected.append({"key": k, "reason": "unknown policy key"})
        elif not chk(v):
            rejected.append({"key": k, "reason": "value failed validation"})
        else:
            accepted[k] = v
    if accepted:
        with _conn() as conn, conn.cursor() as cur:
            for k, v in accepted.items():
                if k == "model_preferences":
                    # Merge only edited tasks; a Media change must preserve Video
                    # preferences and defaults for tasks the operator did not edit.
                    cur.execute("INSERT INTO settings_policies (key,value,updated_by) VALUES (%s,%s,%s) "
                                "ON CONFLICT (key) DO NOTHING", (k, Jsonb({}), "operator"))
                    cur.execute("SELECT value FROM settings_policies WHERE key=%s FOR UPDATE", (k,))
                    existing = dict(cur.fetchone()["value"] or {})
                    for surface, tasks in v.items():
                        existing[surface] = {**existing.get(surface, {}), **tasks}
                    v = existing
                cur.execute(
                    "INSERT INTO settings_policies (key, value, updated_by) VALUES (%s,%s,%s)"
                    " ON CONFLICT (key) DO UPDATE SET value=EXCLUDED.value,"
                    " updated_at=now(), updated_by=EXCLUDED.updated_by",
                    (k, Jsonb(v), "operator"))
            conn.commit()
    return read_policies(), rejected, len(accepted)


def task_bindings(surface="media") -> dict:
    """{task: model_key} — the operator's bindings (settings_policies 'task_bindings')."""
    try:
        with _conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT key,value FROM settings_policies WHERE key IN ('task_bindings','model_preferences')")
            stored = {row["key"]: row["value"] for row in cur.fetchall()}
        result = dict(stored.get("task_bindings") or {})
        if "model_preferences" in stored:
            from .model_preferences import read
            preferences = read(stored["model_preferences"])
            for task in stored["model_preferences"].get(surface, {}):
                rule = preferences[surface][task]
                if rule["preferred"]:
                    result[task] = rule["preferred"][0]
                else:
                    result.pop(task, None)
        return result
    except Exception as exc:  # noqa: BLE001
        logger.warning("task_bindings read failed: %s", exc)
        return {}


# ── handlers (abstract_flask convention: kwargs in, JSON-able out) ────────────
# The registrar merges query + form + JSON body + path params into kwargs (URL
# identity wins) and wraps the returned data as {"result": ...}; these views
# never read ``flask.request`` and never ``jsonify``. Custom HTTP statuses
# (400/403/502/503) collapse to 200 (accepted). The operator gate stays a plain
# function check (operator_only / _operator_gate) returning {"error": ...} data.


# --- boxes (operator) --------------------------------------------------------
@operator_only
def settings_boxes():
    return _relay("/boxes/list", {}, operator=True)


@operator_only
def settings_boxes_enroll_token(name=None, ttl_s=None):
    name = str(name or "").strip()
    if not name:
        return {"error": "name is required"}
    payload = {"name": name}
    if ttl_s is not None:
        payload["ttl_s"] = ttl_s
    if not TOOLSERVER_TOKEN:
        return {"error": "hugpy_core has no toolserver operator token configured "
                         "(env HUGPY_CORE_TOOLSERVER_TOKEN); operator settings are unavailable"}
    status, tbody = _ts("/boxes/enroll_token", payload, operator=True)
    if status != 200 or "result" not in tbody:
        msg = tbody.get("error") if isinstance(tbody, dict) else None
        return {"error": msg or f"toolserver /boxes/enroll_token returned HTTP {status}"}
    res = dict(tbody["result"])
    # The one-line install command the operator runs on the new box. Built from
    # the configured core self base (HUGPY_SELF_BASE) rather than the live
    # request origin (the convention's views do not read ``request``).
    tok = res.get("enroll_token")
    if tok:
        res["install_cmd"] = (f"curl -fsSL {self_base()}/api/fleet/workers/install.sh | "
                              f"bash -s -- --name {name} --token {tok}")
    return res


@operator_only
def settings_boxes_revoke(client_id=None):
    if not client_id:
        return {"error": "client_id is required"}
    return _relay("/boxes/revoke", {"client_id": client_id}, operator=True)


# --- secrets (operator; write-only, values never echoed) ---------------------
@operator_only
def settings_secrets():
    return _relay("/vault/list", {}, operator=True)


@operator_only
def settings_secrets_set(name=None, value=None, scope=None, description=None):
    if not name or value is None:
        return {"error": "name and value are required"}
    payload = {"name": name, "value": value}
    if scope is not None:
        payload["scope"] = scope
    if description is not None:
        payload["description"] = description
    # The toolserver reply carries name/scope/version/updated/rotated — no value.
    return _relay("/vault/set", payload, operator=True)


@operator_only
def settings_secrets_rotate(name=None, value=None):
    if not name or value is None:
        return {"error": "name and value are required"}
    return _relay("/vault/rotate", {"name": name, "value": value}, operator=True)


@operator_only
def settings_secrets_grant(name=None, grantee=None):
    if not name or not grantee:
        return {"error": "name and grantee are required"}
    return _relay("/vault/grant", {"name": name, "grantee": grantee}, operator=True)


@operator_only
def settings_secrets_revoke(name=None, grantee=None):
    if not name or not grantee:
        return {"error": "name and grantee are required"}
    return _relay("/vault/revoke", {"name": name, "grantee": grantee}, operator=True)


@operator_only
def settings_secrets_delete(name=None):
    if not name:
        return {"error": "name is required"}
    return _relay("/vault/delete", {"name": name}, operator=True)


# --- audit (operator) --------------------------------------------------------
@operator_only
def settings_audit(limit=None):
    payload = {}
    if limit is not None:
        try:
            payload["limit"] = int(limit)
        except (TypeError, ValueError):
            return {"error": "limit must be an integer"}
    return _relay("/vault/audit", payload, operator=True)


# --- artifacts (operator) ----------------------------------------------------
@operator_only
def settings_artifacts():
    # The toolserver exposes artifacts only inside a box bundle (/boxes/bundle),
    # keyed to a box credential — there is no operator-wide artifacts list. State
    # that explicitly rather than inventing one.
    return {"artifacts": [], "available": False,
            "reason": "the toolserver serves artifacts only in a box "
                      "bundle (/boxes/bundle); there is no operator artifacts list"}


# --- policies (core DB) ------------------------------------------------------
@operator_only
def settings_policies_get():
    return read_policies()


@operator_only
def settings_policies_post(**doc):
    if not isinstance(doc, dict):
        return {"error": "body must be a JSON object"}
    try:
        result, rejected, _accepted = write_policies(doc)
    except Exception as exc:  # noqa: BLE001
        return {"error": f"policy write failed: {type(exc).__name__}: {exc}"}
    return {**result, "rejected": rejected}


# ── box relay (open / box-token) ──────────────────────────────────────────────
def boxes_enroll(enroll_token=None, name=None, info=None):
    if not enroll_token or not name:
        return {"error": "enroll_token and name are required"}
    payload = {"enroll_token": enroll_token, "name": name}
    if info is not None:
        payload["info"] = info
    return _relay("/boxes/enroll", payload)


def boxes_bundle(client_id=None, token=None):
    if not client_id or not token:
        return {"error": "client_id and token are required"}
    return _relay("/boxes/bundle", {"client_id": client_id, "token": token})


def boxes_bundle_version(client_id=None, token=None):
    if not client_id or not token:
        return {"error": "client_id and token are required"}
    return _relay("/boxes/bundle_version", {"client_id": client_id, "token": token})
