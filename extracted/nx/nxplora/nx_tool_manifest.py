"""nx_tool_manifest.py — AUTO-SYNC the CLI's connector tool surface from the server.

The web app exposes GET /api/personal/manifest (generated from every deployed
app/api/personal/<slug>/route.ts). This module fetches it and builds native
`function` tools + a generic dispatch map from it — so a connector added on the
web needs ZERO CLI hand-wiring: it appears in the manifest and the CLI registers
it automatically on the next turn.

Contract (schemaVersion 2):
  { connectors: [ { provider, route, actions: [ { op, params: [field,...] } ] } ] }

The generic dispatcher forwards { op: <action>, <params...> } to the connector's
route via nx_channel_tools._call_dispatch — the SAME server-side vault + fail-closed
path the hand-wired tools use. Params are passed VERBATIM using the exact field
names the route reads (carried in the manifest), so nothing is silently dropped.

Fail-open by design: if the operator is offline / signed out / the endpoint isn't
deployed, this returns nothing and the hand-wired tools carry the turn unchanged.
"""
import json
import os
import time
import urllib.request

_CACHE = os.path.join(os.path.expanduser("~"), ".nx", "tool-manifest.json")
_TTL_SECONDS = 6 * 3600
_MEM = {"manifest": None, "fetched_at": 0.0}


def _base():
    b = os.environ.get("NX_AUTH_BASE")
    if not b:
        try:
            import nx_message
            b = nx_message._auth_base()
        except Exception:
            b = None
    if not b:
        try:
            import nx_obfuscate as _o
            b = (getattr(_o, "AUTH", {}) or {}).get("base")
        except Exception:
            b = None
    return (b or "https://api.nexplora.ai").rstrip("/")


def _token():
    try:
        import nx_message
        cfg = nx_message._load_config() or {}
    except Exception:
        cfg = {}
    return str(cfg.get("token") or cfg.get("nx_token") or "").strip()


def _fetch(timeout=8):
    """GET the server manifest. Bearer is OPTIONAL (the catalog is public); when present it also
    returns the operator's connected[] set. Returns the parsed dict or None (never raises)."""
    try:
        headers = {"Accept": "application/json"}
        tok = _token()
        if tok:
            headers["Authorization"] = "Bearer " + tok
        req = urllib.request.Request(_base() + "/api/personal/manifest", headers=headers, method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read().decode("utf-8"))
        if isinstance(data, dict) and isinstance(data.get("connectors"), list):
            return data
    except Exception:
        pass
    return None


def _read_cache():
    try:
        with open(_CACHE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict) and isinstance(data.get("connectors"), list):
            return data
    except Exception:
        pass
    return None


def _write_cache(manifest):
    try:
        os.makedirs(os.path.dirname(_CACHE), exist_ok=True)
        with open(_CACHE, "w", encoding="utf-8") as f:
            json.dump(manifest, f)
    except Exception:
        pass


def load_manifest(force=False):
    """Return the connector manifest dict, cached in-memory for the process and on disk (TTL).
    Fetch when stale/forced; fall back to any cache (even stale) then {} — always fail-open."""
    now = time.time()
    if not force and _MEM["manifest"] is not None and (now - _MEM["fetched_at"]) < _TTL_SECONDS:
        return _MEM["manifest"]

    cached = _read_cache()
    cache_fresh = False
    try:
        cache_fresh = cached is not None and (now - os.path.getmtime(_CACHE)) < _TTL_SECONDS
    except Exception:
        cache_fresh = False

    manifest = None
    if force or not cache_fresh:
        fetched = _fetch()
        if fetched is not None:
            manifest = fetched
            _write_cache(manifest)
    if manifest is None:
        manifest = cached if cached is not None else {"connectors": []}

    _MEM["manifest"] = manifest
    _MEM["fetched_at"] = now
    return manifest


def _connectors(manifest=None):
    m = manifest if isinstance(manifest, dict) else load_manifest()
    cx = m.get("connectors")
    return cx if isinstance(cx, list) else []


def connected_providers(manifest=None):
    m = manifest if isinstance(manifest, dict) else load_manifest()
    c = m.get("connected")
    return [str(x) for x in c] if isinstance(c, list) else []


def _describe(provider, actions):
    parts = []
    for a in actions:
        op = str(a.get("op") or "")
        if not op:
            continue
        ps = a.get("params") if isinstance(a.get("params"), list) else []
        parts.append(op + ("(" + ", ".join(str(p) for p in ps) + ")" if ps else ""))
    catalog = "; ".join(parts)
    return (
        "Direct built-in tool for the operator's OWN connected " + provider + " account (BYOK; "
        "fail-closed until they connect " + provider + " on Nexplora or NX). NOT hosted on any "
        "MCP/integration server — call it by the EXACT name `" + provider + "`, never prefix it "
        "with a server name and never route it through zapier/list/discover. One tool — pick "
        "`action`, and pass that action's parameters inside `params` using these EXACT field "
        "names:\n  " + catalog
    )


def _tool_dict(connector):
    provider = str(connector.get("provider") or "")
    actions = connector.get("actions") if isinstance(connector.get("actions"), list) else []
    ops = [str(a.get("op")) for a in actions if a.get("op")]
    return {
        "type": "function",
        "function": {
            "name": provider,
            "description": _describe(provider, actions),
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ops, "description": "the " + provider + " operation to run"},
                    "params": {
                        "type": "object",
                        "description": "the action's parameters, using the exact field names listed in the description",
                    },
                },
                "required": ["action"],
            },
        },
    }


def _make_dispatch(provider, route):
    def _fn(_ga):
        _ga = _ga if isinstance(_ga, dict) else {}
        action = str(_ga.get("action") or "").strip()
        params = _ga.get("params") if isinstance(_ga.get("params"), dict) else {}
        extras = {k: v for k, v in _ga.items() if k not in ("action", "params")}
        payload = {"op": action}
        payload.update(extras)   # model may pass params flat...
        payload.update(params)   # ...or nested; nested wins
        payload = {k: v for k, v in payload.items() if v is not None}
        import nx_channel_tools
        _dr = getattr(nx_channel_tools, "_DISPATCH_ROUTES", None)
        if isinstance(_dr, dict):
            _dr.setdefault(provider + "_crud", route)
        res = nx_channel_tools._call_dispatch(provider, {"name": provider + "_crud"}, payload)
        return (action, res)

    return _fn


def ensure_routes(manifest=None):
    """Register every manifest connector's route into nx_channel_tools._DISPATCH_ROUTES so the
    generic dispatcher (and any caller) can resolve <provider>_crud -> /api/personal/<provider>."""
    try:
        import nx_channel_tools
    except Exception:
        return
    dr = getattr(nx_channel_tools, "_DISPATCH_ROUTES", None)
    if not isinstance(dr, dict):
        return
    for c in _connectors(manifest):
        provider = str(c.get("provider") or "")
        route = str(c.get("route") or ("/api/personal/" + provider))
        if provider:
            dr.setdefault(provider + "_crud", route)


def manifest_tools(exclude_names=frozenset(), manifest=None):
    """Native `function` tool dicts for every manifest connector NOT already registered by name
    (exclude_names = the hand-wired tools, which stay authoritative). Fail-open to []."""
    excl = set(exclude_names or ())
    out = []
    for c in _connectors(manifest):
        provider = str(c.get("provider") or "")
        if not provider or provider in excl:
            continue
        out.append(_tool_dict(c))
    return out


def provider_op_counts(manifest=None):
    """{provider_slug: number-of-personal-connector-ops} from the manifest — the REAL executable-tool count per
    integration, so /integrations can show '15 tools' instead of a hardcoded 0. Fail-open to {}."""
    out = {}
    for c in _connectors(manifest):
        provider = str(c.get("provider") or "")
        acts = c.get("actions")
        if provider and isinstance(acts, list):
            out[provider] = len(acts)
    return out


def manifest_dispatch_map(exclude_names=frozenset(), manifest=None):
    """{provider: dispatch_fn} for every manifest connector NOT already hand-wired. Each fn maps a
    generic tool call to the connector's /api/personal/<provider> route and returns (action, result)."""
    excl = set(exclude_names or ())
    out = {}
    for c in _connectors(manifest):
        provider = str(c.get("provider") or "")
        if not provider or provider in excl:
            continue
        route = str(c.get("route") or ("/api/personal/" + provider))
        out[provider] = _make_dispatch(provider, route)
    return out
