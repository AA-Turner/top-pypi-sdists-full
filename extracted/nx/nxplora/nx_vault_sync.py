"""NX ⇄ Nexplora credential-vault sync — one business, one account.

A connection made in the CLI is PUSHED to the Nexplora server vault (so it shows on the
web), and on login the vault is PULLED into the local Keychain cache. The vault is the
source of truth; the Keychain is a per-user cache.

EVERY operation is best-effort and FAILS OPEN (graceful no-op) when signed out, offline,
or the backend endpoint isn't deployed yet — so this is safe to ship before the endpoint
is live; deploying the endpoint alone activates the bridge. Reads nx_token from
~/.nx/config.json and the API base from nx_obfuscate (mirrors nx_cli AUTH_BASE).
"""
import json
import os
import urllib.error
import urllib.request

_CONFIG = os.path.join(os.path.expanduser("~"), ".nx", "config.json")


def _cfg():
    try:
        with open(_CONFIG, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _token():
    # The web routes (/api/cli/credentials -> getRequestActor) validate the Supabase
    # SESSION token via supabase.auth.getUser. The platform `nx_token` is a DIFFERENT
    # project's JWT that getUser REJECTS (401) — so pushing it silently failed and no
    # connection ever reached the vault. Prefer `token`, matching nx_tool_manifest /
    # nx_channels; keep nx_token only as a last-resort fallback.
    c = _cfg()
    return str((c.get("token") or c.get("nx_session_token") or c.get("nx_token") or "")).strip()


def _base():
    b = os.environ.get("NX_AUTH_BASE")
    if not b:
        try:
            import nx_obfuscate as _o
            b = (getattr(_o, "AUTH", {}) or {}).get("base")
        except Exception:
            b = None
    return (b or "").rstrip("/")


def _endpoint():
    b = _base()
    return f"{b}/api/cli/credentials" if b else ""


def _req(method, url, tok, body=None, timeout=8):
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": f"Bearer {tok}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    })
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8", "replace")
        return resp.status, (json.loads(raw) if raw else {})


def enabled():
    """True only when signed in AND we know the endpoint — else everything no-ops."""
    return bool(_token() and _endpoint())


def push(slug, rec):
    """Push a just-made connection to the vault. No-op (returns False) when signed out,
    when the record has no usable token (public/no-auth servers aren't vaulted), or when
    the endpoint is absent/unreachable (e.g. not deployed yet) — always fail-open."""
    tok, url = _token(), _endpoint()
    if not tok or not url or not isinstance(rec, dict):
        return False
    val = rec.get("access_token")
    if not val or rec.get("public"):
        return False
    scope_str = rec.get("scope") or ""
    # Forward the refresh token + real expiry so the server can keep the connection alive
    # past the short access-token lifetime (server-side refresh-on-read). Without these the
    # vault copy silently rots ~1h after the push while the Keychain copy stays fresh.
    import time as _time
    exp_at = rec.get("expires_at")
    expires_in = None
    if isinstance(exp_at, (int, float)) and exp_at > 0:
        expires_in = max(0, int(exp_at - _time.time()))
    body = {
        "provider": str(slug).strip().lower(),
        "value": val,
        "refreshToken": rec.get("refresh_token"),
        "credentialType": "oauth_access_token",
        "scopes": scope_str.split() if scope_str else [],
        "scope": "default",
        "expiresInSeconds": expires_in,
        "expiresAt": None,
    }
    try:
        st, _ = _req("POST", url, tok, body)
        return st == 200
    except Exception:
        return False


def pull_into_keychain():
    """Pull the vault's connection set into the local Keychain cache (on login). Returns
    the count synced. Fail-open: 0 on any error (signed out / offline / not deployed)."""
    tok, url = _token(), _endpoint()
    if not tok or not url:
        return 0
    try:
        st, data = _req("GET", url, tok)
        if st != 200 or not isinstance(data, dict) or not data.get("ok"):
            return 0
        conns = data.get("connections") or []
    except Exception:
        return 0
    try:
        import nx_mcp_oauth as _O
    except Exception:
        return 0
    provs = [p for p in ((c or {}).get("provider") for c in conns) if p]
    if not provs:
        return 0

    # Fetch each connection's token in PARALLEL. This used to be N SEQUENTIAL vault round-trips run
    # synchronously in the login path — with ~105 connections that made `nx login` take MINUTES. A
    # bounded pool cuts it to a few seconds. Keychain writes stay serial (each _kc_set spawns a
    # `security` subprocess; concurrent writes are not worth the thread-safety risk).
    def _fetch(prov):
        try:
            st, d = _req("GET", f"{url}?provider={prov}&scope=default", tok)
            if st == 200 and isinstance(d, dict) and d.get("value"):
                return (prov, d["value"])
        except Exception:
            return None
        return None

    import concurrent.futures
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=16) as _ex:
            fetched = list(_ex.map(_fetch, provs))
    except Exception:
        return 0

    n = 0
    for item in fetched:
        if not item:
            continue
        prov, val = item
        try:
            _O._kc_set(_O._tok_key(prov),
                       json.dumps({"access_token": val, "expires_in": 10 ** 9}))
            n += 1
        except Exception:
            continue
    return n


def web_oauth_connect(slug, open_browser=True, poll_seconds=180):
    """Connect a provider via its WEB OAuth flow — which grants a REST-usable token the
    /api/personal/* tools ACCEPT — instead of the MCP-server OAuth (whose token those
    REST APIs reject). POST the connect endpoint, open the returned authorize URL in the
    browser, then poll until the server-side callback has stored the token in the vault.

    Returns True on success, False if the provider has no configured web OAuth (the caller
    then falls back to MCP / api-key). Fail-open: never raises.
    """
    tok, base = _token(), _base()
    if not tok or not base:
        return "signed_out"
    try:
        st, d = _req("POST", f"{base}/api/integrations/connect", tok, {"providerSlug": slug})
    except urllib.error.HTTPError as he:
        # 401/403 = the session token expired (the ~2h decay) → tell the operator to re-login.
        return "signed_out" if he.code in (401, 403) else "error"
    except Exception:
        return "error"
    # kind=="redirect" ⇒ a configured web OAuth adapter. Anything else (api_key required,
    # mcp, plaid_link, 503 not-configured) means "no web OAuth here" → caller falls back.
    if st != 200 or not isinstance(d, dict) or d.get("kind") != "redirect" or not d.get("redirectUrl"):
        return "unconfigured"
    url = d["redirectUrl"]
    import time as _t
    # Capture a FRESH-connect watermark BEFORE opening the browser: a provider may already
    # show status=="connected" (e.g. from a prior connect/bridge), so we must wait for the
    # NEW authorization (lastSyncAt newer than now), not a stale "connected" flag. Otherwise
    # we'd return success without the fresh OAuth token ever landing.
    start_ms = int(_t.time() * 1000) - 3000  # small skew tolerance
    if open_browser:
        try:
            import webbrowser
            webbrowser.open(url)
            print(f"  Opening browser to authorize {slug}… (waiting for you to finish)")
        except Exception:
            print(f"  Authorize {slug} in your browser: {url}")
    else:
        print(f"  Authorize {slug}: {url}")
    deadline = _t.time() + poll_seconds
    conn_url = f"{base}/api/integrations/connections"
    while _t.time() < deadline:
        try:
            s2, d2 = _req("GET", conn_url, tok)
            if s2 == 200 and isinstance(d2, dict):
                for c in (d2.get("connections") or []):
                    if str(c.get("providerSlug", "")).lower() == str(slug).lower() and c.get("status") == "connected":
                        ls = c.get("lastSyncAt")
                        # only count a connect that happened AFTER we opened the browser
                        if isinstance(ls, (int, float)) and ls >= start_ms:
                            return "connected"
        except Exception:
            pass
        _t.sleep(3)
    return "timeout"


def paste_api_key(slug, key):
    """Store an operator-pasted API key / service-account token for a provider in the
    server vault (for providers whose REST API is key-auth, not OAuth — Stripe secret
    keys, Grafana glsa_ service-account tokens, Amplitude/Klaviyo/etc.). Stamps the
    personal_read/write tags server-side so the /api/personal tools resolve it.
    Returns True on success. Fail-open.
    """
    tok, base = _token(), _base()
    if not tok or not base or not key:
        return False
    body = {
        "provider": str(slug).strip().lower(),
        "value": str(key).strip(),
        "credentialType": "api_key",
        "scopes": [],
        "scope": "default",
        "expiresAt": None,
    }
    try:
        st, _ = _req("POST", f"{base}/api/cli/credentials", tok, body)
        return st == 200
    except Exception:
        return False
