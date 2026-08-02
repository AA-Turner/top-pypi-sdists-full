"""NX → Nexplora cloud-gate dispatch. NX runs the WHOLE business OS — marketing, sales,
leads, campaigns, finance, hr, growth, product, support, seo, strategy, … (32 packs) —
autonomously, behind the backend's approval + cost-ceiling gates.

Flow per action: evaluate (get the gate + projected cost) → operator approves → execute.
Auth = the device-logged-in nx_token (bearer); workspace_id comes from /api/cli/credentials.
Everything FAILS OPEN with a clear reason (signed out / endpoint absent / not approved), so
this is safe even before the backend dispatch endpoints are deployed.
"""
import json
import os
import urllib.error
import urllib.request

_CONFIG = os.path.join(os.path.expanduser("~"), ".nx", "config.json")

# The business-OS packs NX can dispatch into (each has evaluate/approve/execute on the
# backend). NX picks the pack + action from the operator's request.
PACKS = (
    "nx-marketing", "nx-sales", "nx-leads", "nx-growth", "nx-finance", "nx-hr", "nx-legal",
    "nx-product", "nx-operations", "nx-support", "nx-seo", "nx-strategy", "nx-research",
    "nx-brand", "nx-analytics", "nx-communication", "nx-automation", "nx-designs",
    "nx-documents", "nx-procurement", "nx-productivity", "nx-customer-success", "nx-devops",
    "nx-security", "nx-onboarding", "nx-knowledge-management", "nx-visuals", "nx-education",
    "nx-agents", "nx-admin", "nx-study", "nx-foundry",
)


def _cfg():
    try:
        with open(_CONFIG, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_cfg(c):
    try:
        with open(_CONFIG, "w", encoding="utf-8") as f:
            json.dump(c, f)
        return True
    except Exception:
        return False


def _token():
    # Canonical device-flow token is cfg['token']; 'nx_token' is the RETIRED (tiyon) key kept only as a fallback.
    c = _cfg()
    return str((c.get("token") or c.get("nx_token") or "")).strip()


def _base():
    b = os.environ.get("NX_AUTH_BASE")
    if not b:
        try:
            import nx_obfuscate as _o
            b = (getattr(_o, "AUTH", {}) or {}).get("base")
        except Exception:
            b = None
    return (b or "").rstrip("/")


def _req(method, url, tok, body=None, timeout=20):
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": f"Bearer {tok}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", "replace")
            return resp.status, (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace") if e.fp else ""
        try:
            return e.code, json.loads(raw) if raw else {}
        except Exception:
            return e.code, {"error": raw[:200]}


def workspace_id():
    """The operator's workspace — cached in config, else fetched from the vault endpoint
    (which resolves it server-side). '' if unavailable (signed out / not deployed)."""
    c = _cfg()
    wid = (c.get("workspace_id") or "").strip()
    if wid:
        return wid
    tok, base = _token(), _base()
    if not tok or not base:
        return ""
    try:
        st, d = _req("GET", f"{base}/api/cli/credentials", tok, timeout=10)
        wid = (d.get("workspace_id") or "").strip() if st == 200 and isinstance(d, dict) else ""
    except Exception:
        wid = ""
    if wid:
        c["workspace_id"] = wid
        _save_cfg(c)
    return wid


def available():
    """True only when signed in + we know the base (else dispatch can't reach the gates)."""
    return bool(_token() and _base())


def _action_url(pack, action):
    return f"{_base()}/api/{pack}/actions/{action}"


def evaluate(pack, action_id, requested_action, run_id=None):
    """Step 1 — evaluate the action through its gate. Returns
    {ok, request_id, gate:{display_tag, action_label, ...projected cost...}} or {ok:False,error}."""
    tok = _token()
    if not tok or not _base():
        return {"ok": False, "error": "not_signed_in — run /login to dispatch business actions"}
    wid = workspace_id()
    if not wid:
        return {"ok": False, "error": "no_workspace — could not resolve your Nexplora workspace"}
    body = {"workspace_id": wid, "action_id": action_id,
            "requested_action": requested_action, "run_id": run_id}
    try:
        st, d = _req("POST", _action_url(pack, "evaluate"), tok, body)
        if st == 200 and isinstance(d, dict) and d.get("ok"):
            return d
        return {"ok": False, "error": (d or {}).get("error") or f"evaluate_failed:{st}"}
    except Exception as e:
        return {"ok": False, "error": f"request_failed:{type(e).__name__}"}


def execute(pack, action_id, requested_action, run_id, seed_approval=False):
    """Step 3 — approve (if needed) then execute. Returns the execution result."""
    tok = _token()
    if not tok or not _base():
        return {"ok": False, "error": "not_signed_in"}
    wid = workspace_id()
    if not wid:
        return {"ok": False, "error": "no_workspace"}
    # approve, then execute (both bearer-authed; the gate re-checks cost/approval at execute)
    try:
        _req("POST", _action_url(pack, "approve"), tok,
             {"workspace_id": wid, "action_id": action_id, "run_id": run_id})
    except Exception:
        pass
    body = {"workspace_id": wid, "action_id": action_id, "requested_action": requested_action,
            "run_id": run_id, "seed_approval": bool(seed_approval)}
    try:
        st, d = _req("POST", _action_url(pack, "execute"), tok, body)
        if isinstance(d, dict):
            d.setdefault("ok", st == 200)
            return d
        return {"ok": st == 200}
    except Exception as e:
        return {"ok": False, "error": f"request_failed:{type(e).__name__}"}
