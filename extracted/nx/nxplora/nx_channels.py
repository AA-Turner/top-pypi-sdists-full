"""
nx_channels.py — NX "Publish": OAuth connectors for the platforms operators
actually publish to (Meta/FB/IG first). This is the execution half of an
operations AI — NX plans the campaign AND can push it to the channel.

The surface is `/publish`. It was called `/channels` until the web and the CLI
were reconciled: the web has always used Channels for the OPPOSITE direction —
the ways to reach Nexplora — so the one word meant reach-me on one surface and
publish-out on the other. The MODULE keeps its name (renaming it would touch ~14
importers and risk the py_modules wheel list for no operator-visible gain); only
the command moved.

SECURITY CONTRACT (non-negotiable):
  - App credentials (App ID / App Secret) and user OAuth tokens live ONLY in the
    macOS Keychain. Never in code, never in a file, never printed to screen/chat.
  - All Keychain service names are validated before they touch the `security`
    subprocess (no shell-metacharacter / argument injection).
  - Every capability FAILS CLOSED and HONEST: if a channel isn't configured or
    isn't connected, the method says exactly that and tells the operator what to
    do — it NEVER fakes a success. A post is "ok" only when the platform's API
    returns success. (This is the same honesty spine as the agent loop.)

Public platform endpoints (graph.facebook.com etc.) are documented public APIs,
not secrets, so they're readable constants. The SECRETS are Keychain-only.
"""

import json
import os
import re
import sys
import time
import subprocess

# macOS uses the native `security`/Keychain path below (proven, never migrated). Every
# other platform (Windows / Linux) routes the SAME (account, service) contract through
# keyring in nx_keystore. Branch is per-call so tests can flip it.
_IS_MAC = sys.platform == "darwin"

try:
    import requests
except Exception:  # pragma: no cover
    requests = None

# Keychain service-name allowlist (mirrors nx_key_pool) — validated before the
# name is ever handed to the `security` subprocess.
_KC_NAME_RE = re.compile(r"^[A-Za-z0-9._-]{1,64}$")
_KC_ACCOUNT = "nx-channels"


def _safe_kc_name(name: str) -> bool:
    return bool(name) and bool(_KC_NAME_RE.match(name))


# Indirection so tests can patch Keychain without touching the real one, and so
# every `security` call goes through one validated path.
def _security(args, input_text=None):
    return subprocess.run(
        ["security", *args],
        capture_output=True, text=True, input=input_text, timeout=10,
    )


def kc_get(service: str):
    """Read a secret from the store. Returns None if absent/invalid."""
    if not _safe_kc_name(service):
        return None
    if not _IS_MAC:
        from nx_keystore import kr_get
        return kr_get(_KC_ACCOUNT, service)
    try:
        r = _security(["find-generic-password", "-a", _KC_ACCOUNT, "-s", service, "-w"])
        if r.returncode == 0:
            return (r.stdout or "").strip() or None
    except Exception:
        pass
    return None


def kc_set(service: str, value: str) -> bool:
    """Store a secret (update if present). Never logs the value."""
    if not _safe_kc_name(service) or value is None:
        return False
    if not _IS_MAC:
        from nx_keystore import kr_set
        return kr_set(_KC_ACCOUNT, service, value)
    try:
        r = _security([
            "add-generic-password", "-a", _KC_ACCOUNT, "-s", service,
            "-w", value, "-U",
        ])
        return r.returncode == 0
    except Exception:
        return False


def kc_delete(service: str) -> bool:
    if not _safe_kc_name(service):
        return False
    if not _IS_MAC:
        from nx_keystore import kr_delete
        return kr_delete(_KC_ACCOUNT, service)
    try:
        r = _security(["delete-generic-password", "-a", _KC_ACCOUNT, "-s", service])
        return r.returncode == 0
    except Exception:
        return False


class ChannelError(Exception):
    pass


def push_token_to_cloud(slug: str = "x") -> dict:
    """Bridge a locally-connected channel token into the Nexplora server vault so the CLOUD/Telegram poster can use
    it — reuses the proven CLI connection instead of the web OAuth. Reads the operator's OWN device token from
    ~/.nx/config.json and POSTs the channel's access token (from Keychain nx-channel-<slug>-token) to
    /api/nexplora/credential-import. The token is read from the local Keychain and sent over TLS to the operator's
    OWN account; it is never printed or logged. Returns the server JSON; raises on failure.

    X access tokens expire ~2h — re-run to refresh the cloud copy (durable server-side refresh is a follow-on)."""
    import json as _json
    import requests
    cfg_path = os.path.join(os.path.expanduser("~"), ".nx", "config.json")
    try:
        cfg = _json.load(open(cfg_path))
    except Exception:
        cfg = {}
    # The device access token is short-lived (~1h) — refresh it via the stored refresh_token before we auth,
    # otherwise a stale token 401s. refresh_token_if_needed persists + returns the refreshed cfg.
    try:
        import nx_cli as _nc
        cfg = _nc.refresh_token_if_needed(cfg) or cfg
    except Exception:
        pass
    dtoken = str(cfg.get("token") or cfg.get("nx_token") or "").strip()
    if not dtoken:
        raise ChannelError("sign in first (run nx) — the bridge needs your account")
    # The provider access token is short-lived (X ~2h). Refresh it via its stored refresh_token BEFORE reading +
    # pushing, so the cloud always gets a LIVE token (a stale one 401s at POST /2/tweets). Best-effort: if refresh
    # fails we still push whatever's on disk. refresh() writes the fresh token back to the Keychain.
    try:
        _conn = connector_for_service(slug)
        if _conn is not None:
            _conn.refresh()
    except Exception:
        pass
    raw = kc_get("nx-channel-%s-token" % slug)
    if not raw:
        raise ChannelError("%s is not connected in the CLI — connect it first" % slug)
    try:
        tok = _json.loads(raw)
    except Exception:
        raise ChannelError("%s token is unreadable" % slug)
    access = str((tok or {}).get("access_token") or "").strip()
    if not access:
        raise ChannelError("%s has no access_token" % slug)
    base = os.environ.get("NX_AUTH_BASE") or "https://api.nexplora.ai"
    body = {"provider": slug, "access_token": access}
    if tok.get("refresh_token"):
        body["refresh_token"] = str(tok["refresh_token"])
    if tok.get("scopes"):
        body["scopes"] = tok["scopes"]
    if tok.get("expires_at"):
        try:
            body["expires_at"] = float(tok["expires_at"])
        except Exception:
            pass
    r = requests.post(base.rstrip("/") + "/api/nexplora/credential-import", json=body,
                      headers={"Authorization": "Bearer " + dtoken, "Content-Type": "application/json"}, timeout=20)
    if r.status_code >= 300:
        err = ""
        try:
            err = (r.json() or {}).get("error") or ""
        except Exception:
            err = (r.text or "")[:120]
        raise ChannelError("credential-import %d: %s" % (r.status_code, err or "failed"))
    try:
        return r.json() or {}
    except Exception:
        return {"ok": True}


# Public client IDs for any remaining local-loopback OAuth connectors.
# Canonical social providers intentionally do not appear here: Meta, X, and
# LinkedIn all initiate through Nexplora's server-side OAuth registry and write
# exactly one operator grant to the shared credential vault.
_NX_APP_CLIENT_IDS = {}


# ── Business-OS bridge (shared Nexplora apps — Meta, TikTok today) ──────────
# These two platforms connect through Nexplora's OWN registered app, the same
# model as the existing eBay/Amazon connectors in nx_ebay_tools.py — NOT the
# per-operator-app model the ChannelConnector base class below was built for.
# The OAuth dance, the client_secret, and the resulting token all live
# server-side in nexplora-v2 (lib/business-os/auth/oauth-flow.ts); NX CLI only
# opens the browser to Nexplora's OWN callback domain (never localhost) and
# polls for completion. Mirrors nx_ebay_tools.py's _cfg()/_token()/_base()
# pattern for consistency with the one bridge that already works end-to-end.
_BOS_PLATFORM = {
    "meta": "facebook", "tiktok": "tiktok",
    "google": "youtube", "snapchat": "snapchat",
}  # NX channel name -> business-os SupportedPlatform
_BOS_CONFIG = os.path.join(os.path.expanduser("~"), ".nx", "config.json")


def _bos_cfg() -> dict:
    try:
        with open(_BOS_CONFIG, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _bos_token() -> str:
    """The bearer token for an authed business-os call (api.nexplora.ai). That
    endpoint validates the gateway SESSION JWT (cfg["token"]) via
    supabase.auth.getUser — the tiyon-bridge nx_token is a DIFFERENT project's
    JWT that getUser rejects (401) — so prefer `token`, keep nx_token only as a
    fallback. Lazy-import nx_cli to avoid a circular import (nx_cli imports this
    module at startup)."""
    try:
        import nx_cli as _nc
        cfg = _nc.load_config() or {}
        try:
            cfg = _nc.refresh_token_if_needed(cfg)
        except Exception:
            pass
        tok = str(cfg.get("token") or cfg.get("nx_session_token") or cfg.get("nx_token") or "").strip()
        if tok:
            return tok
    except Exception:
        pass
    cfg = _bos_cfg()
    return str(cfg.get("token") or cfg.get("nx_session_token") or cfg.get("nx_token") or "").strip()


def _bos_base() -> str:
    b = os.environ.get("NX_AUTH_BASE")
    if not b:
        try:
            import nx_obfuscate as _o
            b = (getattr(_o, "AUTH", {}) or {}).get("base")
        except Exception:
            b = None
    return (b or "").rstrip("/")


def _bos_get(path: str, timeout: int = 15) -> dict:
    """GET against the Nexplora backend with the NX bearer token. Never
    raises — returns {"ok": False, "error": ...} on any failure so callers
    stay honest without try/except boilerplate at every call site."""
    tok, base = _bos_token(), _bos_base()
    if not tok:
        return {"ok": False, "error": "not_signed_in"}
    if not base:
        return {"ok": False, "error": "no_backend_base"}
    if requests is None:
        return {"ok": False, "error": "requests_unavailable"}
    try:
        r = requests.get(f"{base}{path}",
                         headers={"Authorization": f"Bearer {tok}", "Accept": "application/json"},
                         timeout=timeout)
        d = r.json() if r.content else {}
        if not isinstance(d, dict):
            return {"ok": False, "error": "bad_response_shape"}
        d.setdefault("ok", r.status_code < 400)
        return d
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}"}


def _bos_post(path: str, body: dict, timeout: int = 15) -> dict:
    tok, base = _bos_token(), _bos_base()
    if not tok:
        return {"ok": False, "error": "not_signed_in"}
    if not base:
        return {"ok": False, "error": "no_backend_base"}
    if requests is None:
        return {"ok": False, "error": "requests_unavailable"}
    try:
        r = requests.post(f"{base}{path}", json=body,
                          headers={"Authorization": f"Bearer {tok}", "Accept": "application/json"},
                          timeout=timeout)
        d = r.json() if r.content else {}
        if not isinstance(d, dict):
            return {"ok": False, "error": "bad_response_shape"}
        d.setdefault("ok", r.status_code < 400)
        return d
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}"}


def _bos_connections() -> list:
    """[{platform, status, connected_at, brand_id}, ...] for the signed-in operator."""
    d = _bos_get("/api/business-os/connections")
    return d.get("platforms", []) if d.get("ok") else []


def _bos_is_connected(bos_platform: str) -> bool:
    return any(p.get("platform") == bos_platform for p in _bos_connections())


def _bos_brand_id_for(bos_platform: str):
    for p in _bos_connections():
        if p.get("platform") == bos_platform:
            return p.get("brand_id")
    return None


def _bos_connect_url(bos_platform: str):
    """Ask the backend to generate the real OAuth URL for this platform —
    Nexplora's own callback domain, never localhost. Returns (url, error)."""
    d = _bos_get(f"/api/business-os/connect/{bos_platform}?format=json")
    if d.get("ok") and d.get("url"):
        return d["url"], None
    return None, d.get("error", "unknown_error")


def _bos_disconnect(bos_platform: str) -> dict:
    brand_id = _bos_brand_id_for(bos_platform)
    if not brand_id:
        return {"ok": False, "error": "not_connected"}
    return _bos_post(f"/api/business-os/connect/disconnect/{bos_platform}", {"brandId": brand_id})


class _BosBridgedChannel:
    """Mixin for channels that connect through Nexplora's OWN shared app
    (server-side OAuth in nexplora-v2's Business OS layer) instead of asking
    the operator to register their own. Compose via multiple inheritance,
    THIS MIXIN FIRST, so it takes priority over ChannelConnector's per-operator
    defaults: `class MetaChannel(_BosBridgedChannel, ChannelConnector)`.

    The connection itself is real end-to-end (token lives encrypted in
    nexplora-v2). Acting on it (publish a post, list pages) still needs a
    server-side proxy like nx_ebay_tools.py's /api/business-os/ebay/call —
    that doesn't exist yet for these platforms, so preflight() refuses those
    actions honestly rather than failing confusingly on a local token that
    will never exist locally."""

    # Unused: the real redirect_uri lives server-side in nexplora-v2's
    # oauth-config.ts (Nexplora's own callback domain), never localhost.
    redirect_uri = None

    @property
    def bos_platform(self) -> str:
        return _BOS_PLATFORM[self.name]

    def is_configured(self) -> bool:
        return True  # Nexplora's own app already exists server-side.

    def is_connected(self) -> bool:
        return _bos_is_connected(self.bos_platform)

    def disconnect(self) -> bool:
        return bool(_bos_disconnect(self.bos_platform).get("ok"))

    def preflight(self, action: str = "use") -> dict:
        if not self.is_connected():
            return {"ok": False, "detail": "not_connected",
                    "hint": f"/publish connect {self.name}"}
        if action in ("publish", "list"):
            return {"ok": False, "detail": "publish_not_wired_yet",
                    "hint": "Connected — publishing through NX is coming next."}
        return {"ok": True}


def _wait_with_spinner(check_fn, url, timeout=180, label="authorize in the browser"):
    """Poll check_fn() until truthy or timeout, showing a LIVE animated star + elapsed line so a connect never
    looks like a frozen black screen (the '5 minutes, then it finally shows something' complaint). Animates
    every ~0.5s; polls the backend every 3s. Returns {"ok":True} on success, else the not-completed dict."""
    import sys as _sys
    _G = "\033[38;2;200;164;74m"; _D = "\033[38;2;172;166;148m"; _R = "\033[0m"
    _star = ("✦", "✧")
    _t0 = time.time(); _i = 0
    deadline = time.time() + timeout
    # \r overwrites the line only on a real TTY. In a non-TTY (a pipe, or a web terminal that
    # doesn't process carriage-returns) each animated tick APPENDS → the "connecting…" line prints
    # dozens of times. So: animate in place on a TTY; on a non-TTY print the message ONCE and poll
    # silently. Either way the user sees the line at most once until connected/failed.
    _tty = False
    try:
        _tty = _sys.stdout.isatty()
    except Exception:
        _tty = False
    _clear = (lambda: (_sys.stdout.write("\r\033[2K"), _sys.stdout.flush())) if _tty else (lambda: None)
    if not _tty:
        _sys.stdout.write(f"  {_D}connecting… finish authorizing in the browser (esc to cancel){_R}\n")
        _sys.stdout.flush()
    try:
        while time.time() < deadline:
            if check_fn():
                _clear()
                return {"ok": True}
            for _ in range(6):  # ~6 × 0.5s ticks between 3s backend polls
                _i += 1
                if _tty:
                    try:
                        _el = int(time.time() - _t0)
                        _sys.stdout.write(f"\r  {_G}{_star[_i % 2]}{_R} {_D}connecting… waiting for you to {label}  ({_el}s · esc to cancel){_R}")
                        _sys.stdout.flush()
                    except Exception:
                        pass
                time.sleep(0.5)
    except KeyboardInterrupt:
        _clear()
        return {"ok": False, "detail": "cancelled", "url": url}
    _clear()
    return {"ok": False, "detail": "authorization_not_completed", "url": url}


def _connect_bos_bridged(channel, open_browser: bool = True, timeout: int = 180) -> dict:
    """Open Nexplora's real OAuth URL for this platform and poll until the
    server-side callback lands the connection (mirrors device_login()'s
    poll-until-complete UX in nx_cli.py)."""
    url, err = _bos_connect_url(channel.bos_platform)
    if not url:
        if err == "not_signed_in":
            return {"ok": False, "detail": "not_signed_in", "hint": "run /login first"}
        return {"ok": False, "detail": f"connect_url_failed:{err}"}
    if open_browser:
        try:
            import webbrowser
            webbrowser.open(url)
        except Exception:
            pass
    return _wait_with_spinner(lambda: _bos_is_connected(channel.bos_platform), url, timeout)


_SOCIAL_VAULT_FAMILIES = {
    "meta": {"meta", "instagram", "facebook", "threads"},
    "x": {"x"},
    "linkedin": {"linkedin"},
}


def _canonical_social_provider(provider: str) -> str:
    normalized = str(provider or "").strip().lower()
    for canonical, members in _SOCIAL_VAULT_FAMILIES.items():
        if normalized in members:
            return canonical
    return normalized


def _oauth_vault_connections() -> list:
    """Canonical operator connections shared by Nexplora web and NX.

    Metadata only. Tokens remain encrypted in Nexplora's credential vault.
    """
    d = _bos_get("/api/integrations/connections")
    return d.get("connections", []) if d.get("ok") else []


def _oauth_vault_connection(provider: str):
    family = _canonical_social_provider(provider)
    matches = []
    for connection in _oauth_vault_connections():
        slug = _canonical_social_provider(connection.get("providerSlug"))
        if slug == family:
            matches.append(connection)
    rank = {"needs_reauth": 4, "error": 3, "connected": 2, "configured": 1}
    return max(matches, key=lambda row: rank.get(row.get("status"), 0), default=None)


def _oauth_vault_is_connected(provider: str) -> bool:
    connection = _oauth_vault_connection(provider)
    return bool(connection and connection.get("status") == "connected")


def _oauth_vault_connect_url(provider: str):
    """Start the exact same OAuth flow used by the Nexplora web controls."""
    canonical = _canonical_social_provider(provider)
    d = _bos_post("/api/integrations/connect", {"providerSlug": canonical})
    if d.get("ok") and d.get("kind") == "redirect" and d.get("redirectUrl"):
        return d["redirectUrl"], None
    return None, d.get("error", "unknown_error")


def _oauth_vault_disconnect(provider: str) -> dict:
    return _bos_post(
        "/api/integrations/disconnect",
        {"providerSlug": _canonical_social_provider(provider)},
    )


class _NexploraOAuthBridgedChannel:
    """One operator grant for web + CLI, held only in Nexplora's vault."""

    redirect_uri = None
    requires_secret = False
    server_execution_available = False

    @property
    def vault_provider(self) -> str:
        return _canonical_social_provider(self.name)

    def is_configured(self) -> bool:
        # The registered app lives in Nexplora. Initiation still fails closed
        # with oauth_platform_not_configured when deployment env is incomplete.
        return True

    def setup(self, app_id: str, app_secret: str = None) -> bool:
        # Refuse a parallel per-device OAuth app/keychain record. The only
        # supported grant is the shared Nexplora account grant.
        return False

    def is_connected(self) -> bool:
        return _oauth_vault_is_connected(self.vault_provider)

    def disconnect(self) -> bool:
        return bool(_oauth_vault_disconnect(self.vault_provider).get("ok"))

    def preflight(self, action: str = "use") -> dict:
        connection = _oauth_vault_connection(self.vault_provider)
        if not connection:
            return {"ok": False, "detail": "not_connected",
                    "hint": f"/publish connect {self.name}"}
        if connection.get("status") == "needs_reauth":
            return {"ok": False, "detail": "needs_reauth",
                    "hint": f"/publish connect {self.name}"}
        if connection.get("status") != "connected":
            return {"ok": False, "detail": "connection_unavailable",
                    "hint": f"/publish connect {self.name}"}
        if action in ("publish", "list") and not self.server_execution_available:
            return {
                "ok": False,
                "detail": "server_execution_not_available",
                "hint": "Connected in the shared Nexplora vault; this provider action is not enabled yet.",
            }
        return {"ok": True}


def _connect_nexplora_oauth(channel, open_browser: bool = True, timeout: int = 180) -> dict:
    url, err = _oauth_vault_connect_url(channel.vault_provider)
    if not url:
        if err in ("not_signed_in", "unauthenticated"):
            return {"ok": False, "detail": "not_signed_in", "hint": "run /login first"}
        return {"ok": False, "detail": f"connect_url_failed:{err}"}
    if open_browser:
        try:
            import webbrowser
            webbrowser.open(url)
        except Exception:
            pass
    return _wait_with_spinner(
        lambda: _oauth_vault_is_connected(channel.vault_provider),
        url,
        timeout,
    )


# ── Google Workspace (Gmail/Calendar/Drive/Docs) — a SEPARATE system from the
# youtube-via-bos-bridge "google" channel above. That one is the narrow,
# already-shipped business-os bridge (youtube.readonly/upload + adwords).
# This one is the broader per-operator Google Workspace OAuth grant
# (lib/oauth-flows/google/ in nexplora-v2) — one grant covers Gmail, Calendar,
# Drive, Docs, Sheets. Connect goes through the generic
# /api/oauth/initiate/google route (not a bos-bridge endpoint), and status is
# read from /api/integrations/connections (providerSlug "google_workspace"),
# not /api/business-os/connections. Kept fully separate so neither system can
# silently regress the other.
_GOOGLE_WORKSPACE_READ_SCOPES = " ".join([
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",   # send-as-you — the CLI must REQUEST it here or no reconnect
                                                    # ever grants it (this list is passed to /api/oauth/initiate,
                                                    # overriding config.ts defaultScopes). The personal.gmail.send
                                                    # tool + per-send approval still gate the actual send.
    "https://www.googleapis.com/auth/gmail.modify",       # full e2e client — archive/star/trash/delete/mark-read +
                                                          # apply labels (users/me/messages/{id}/modify). Per-action
                                                          # approval (gmail.modify) still gates each mutation.
    "https://www.googleapis.com/auth/gmail.settings.basic",  # the "automate" primitive — create/list/delete filters
                                                             # (users/me/settings/filters). Approval-gated on create/delete.
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/calendar.events",       # Google world e2e — schedule/reschedule/cancel/RSVP/
                                                             # move/quick-add/reminders (calendar/v3 events writes).
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/drive",                 # Drive e2e — create/update/delete/copy/move/share/
                                                             # trash/restore/comments (drive/v3 writes).
    "https://www.googleapis.com/auth/documents.readonly",
    "https://www.googleapis.com/auth/documents",             # Docs e2e — create/batchUpdate/format/insert/delete.
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/spreadsheets",          # Sheets e2e — create/values/format/sort/chart/protect.
    # Tasks / Forms / Meet / Chat — same shared google grant; the personal routes (google-tasks/
    # forms/meet/chat) 403 *_unauthorized until these are REQUESTED here. Reads for all four;
    # Tasks also has write ops. Forms/Meet/Chat reads are the live-provable surface.
    "https://www.googleapis.com/auth/tasks.readonly",
    "https://www.googleapis.com/auth/tasks",                 # Tasks e2e — tasklist/task create/update/delete/move/clear.
    "https://www.googleapis.com/auth/forms.body.readonly",
    "https://www.googleapis.com/auth/forms.responses.readonly",
    "https://www.googleapis.com/auth/meetings.space.readonly",
    "https://www.googleapis.com/auth/chat.spaces.readonly",
    "https://www.googleapis.com/auth/chat.messages.readonly",
])


def _google_whoami() -> dict:
    """{ok, user_id, workspace_id} for the signed-in operator. NX never
    stores a workspace_id locally — this is how it learns its own."""
    return _bos_get("/api/oauth/whoami")


def _google_workspace_connections() -> list:
    d = _bos_get("/api/integrations/connections")
    return d.get("connections", []) if d.get("ok") else []


def _google_workspace_is_connected() -> bool:
    return any(c.get("providerSlug") == "google_workspace" and c.get("status") == "connected"
               for c in _google_workspace_connections())


def _google_workspace_connect_url():
    """Ask /api/oauth/initiate/google for Google's real consent URL. That
    route always 302s on success (it has no ?format=json mode like the
    bos-bridge routes) — read the Location header instead of following it."""
    tok, base = _bos_token(), _bos_base()
    if not tok:
        return None, "not_signed_in"
    if not base:
        return None, "no_backend_base"
    who = _google_whoami()
    if not who.get("ok"):
        return None, "not_signed_in"
    workspace_id = who.get("workspace_id")
    if not workspace_id:
        return None, "no_workspace"
    if requests is None:
        return None, "requests_unavailable"
    try:
        r = requests.get(
            f"{base}/api/oauth/initiate/google",
            # incremental=true (include_granted_scopes): a Workspace reconnect must ADD its scopes onto
            # the shared Google grant, never REPLACE it — otherwise it strips the youtube/adwords scopes
            # the "Google (Ads + YouTube)" connect added (the two connects share ONE provider:'google'
            # grant; last non-incremental connect wins and drops the other's scopes).
            params={"workspace_id": workspace_id, "scopes": _GOOGLE_WORKSPACE_READ_SCOPES, "incremental": "true"},
            headers={"Authorization": f"Bearer {tok}", "Accept": "application/json"},
            allow_redirects=False,
            timeout=15,
        )
        if r.status_code in (301, 302, 303, 307, 308):
            loc = r.headers.get("Location")
            if loc:
                return loc, None
        try:
            d = r.json()
        except Exception:
            d = {}
        return None, d.get("error", f"unexpected_status_{r.status_code}")
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"


def _google_workspace_disconnect() -> dict:
    return _bos_post("/api/integrations/disconnect", {"providerSlug": "google_workspace"})


class _GoogleWorkspaceBridgedChannel:
    """Mixin for the Google Workspace channel — same shape as
    _BosBridgedChannel (server-side OAuth, no local token, no setup step)
    but talks to the generic oauth-flows + integrations endpoints instead of
    the business-os bridge. Compose THIS MIXIN FIRST, same as
    _BosBridgedChannel: `class GoogleWorkspaceChannel(_GoogleWorkspaceBridgedChannel, ChannelConnector)`."""

    redirect_uri = None

    def is_configured(self) -> bool:
        return True

    def is_connected(self) -> bool:
        return _google_workspace_is_connected()

    def disconnect(self) -> bool:
        return bool(_google_workspace_disconnect().get("ok"))

    def preflight(self, action: str = "use") -> dict:
        if not self.is_connected():
            return {"ok": False, "detail": "not_connected",
                    "hint": f"/publish connect {self.name}"}
        if action not in ("profile",):
            return {"ok": False, "detail": f"{action}_not_wired_yet",
                    "hint": "Connected — gmail profile read is live; send is next."}
        return {"ok": True}


def _connect_google_workspace(open_browser: bool = True, timeout: int = 180) -> dict:
    url, err = _google_workspace_connect_url()
    if not url:
        if err == "not_signed_in":
            return {"ok": False, "detail": "not_signed_in", "hint": "run /login first"}
        if err == "no_workspace":
            return {"ok": False, "detail": "no_workspace",
                    "hint": "Open the Nexplora dashboard once to finish account setup, then retry."}
        return {"ok": False, "detail": f"connect_url_failed:{err}"}
    if open_browser:
        try:
            import webbrowser
            webbrowser.open(url)
        except Exception:
            pass
    return _wait_with_spinner(_google_workspace_is_connected, url, timeout)


# ── Google (Ads + YouTube) — the SAME shared Google grant as Workspace, just
# different scopes ──────────────────────────────────────────────────────────
# YouTube + Google Ads used to connect through the business-os bridge
# (/api/business-os/connect/youtube), whose SERVER-SIDE redirect_uri
# (/api/business-os/connect/callback/youtube) is NOT registered on Nexplora's
# Google Cloud OAuth client → Google returned "Error 400: redirect_uri_mismatch".
# It also stored the token in the business-os store, which the personal youtube
# route (executeWithCredential provider:'google') never reads. Fix: connect
# through the SAME web OAuth route as Workspace (/api/oauth/initiate/google →
# the REGISTERED redirect /api/oauth/callback/google) with incremental=true so
# the youtube/ads scopes are ADDED onto the operator's existing Google grant
# (never dropping Gmail/Drive/Calendar), landing in the ONE shared provider
# 'google' vault grant the personal youtube/ads tools resolve.
_GOOGLE_ADS_YOUTUBE_SCOPES = " ".join([
    "https://www.googleapis.com/auth/youtube.readonly",   # read: my channel · search · videos · playlists
    "https://www.googleapis.com/auth/youtube",            # manage: playlists · subscriptions · ratings
    "https://www.googleapis.com/auth/youtube.upload",     # publish: upload / update / delete videos
    "https://www.googleapis.com/auth/adwords",            # Google Ads — campaigns/reporting. NOTE: the Ads API ALSO
                                                          # needs a Google Ads developer token; OAuth consent alone
                                                          # grants the scope but won't authorize live Ads API calls.
    "https://www.googleapis.com/auth/userinfo.email",
])


def _google_ads_youtube_connect_url():
    """Consent URL for YouTube + Google Ads via the SAME /api/oauth/initiate/google
    route Workspace uses (so the REGISTERED /api/oauth/callback/google redirect_uri,
    NOT the unregistered business-os one that 400'd). incremental=true ⇒
    include_granted_scopes: the youtube/ads scopes ADD onto the existing Google
    grant, never dropping Gmail/Drive/Calendar. 302s on success — read Location."""
    tok, base = _bos_token(), _bos_base()
    if not tok:
        return None, "not_signed_in"
    if not base:
        return None, "no_backend_base"
    who = _google_whoami()
    if not who.get("ok"):
        return None, "not_signed_in"
    workspace_id = who.get("workspace_id")
    if not workspace_id:
        return None, "no_workspace"
    if requests is None:
        return None, "requests_unavailable"
    try:
        r = requests.get(
            f"{base}/api/oauth/initiate/google",
            params={"workspace_id": workspace_id,
                    "scopes": _GOOGLE_ADS_YOUTUBE_SCOPES,
                    "incremental": "true"},
            headers={"Authorization": f"Bearer {tok}", "Accept": "application/json"},
            allow_redirects=False,
            timeout=15,
        )
        if r.status_code in (301, 302, 303, 307, 308):
            loc = r.headers.get("Location")
            if loc:
                return loc, None
        try:
            d = r.json()
        except Exception:
            d = {}
        return None, d.get("error", f"unexpected_status_{r.status_code}")
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"


def _google_grant_is_connected() -> bool:
    """True when the ONE shared Google grant exists. Workspace + Ads/YouTube ride
    the same provider 'google' vault grant, recorded under the 'google_workspace'
    umbrella slug (the callback's `${provider}_workspace` catalog lookup)."""
    return any(c.get("providerSlug") in ("google_workspace", "google")
               and c.get("status") == "connected"
               for c in _google_workspace_connections())


class _GoogleAdsYouTubeBridgedChannel:
    """Mixin for Google (Ads + YouTube). Connects through the SAME web OAuth route
    as Google Workspace (/api/oauth/initiate/google) — reusing the REGISTERED
    redirect_uri AND the one shared provider 'google' vault grant — but requests
    the youtube + adwords scopes via incremental consent. NOT the business-os
    bridge (that path 400'd on an unregistered redirect_uri and stored the token
    where the personal youtube route can't read it). Compose THIS MIXIN FIRST:
    `class GoogleChannel(_GoogleAdsYouTubeBridgedChannel, ChannelConnector)`."""

    redirect_uri = None

    def is_configured(self) -> bool:
        return True

    def is_connected(self) -> bool:
        return _google_grant_is_connected()

    def disconnect(self) -> bool:
        # Shared grant: disconnecting removes the ONE Google grant (also ends
        # Workspace). Honest — it IS one grant; reconnect Workspace after to
        # keep Gmail/Drive/Calendar.
        return bool(_google_workspace_disconnect().get("ok"))

    def preflight(self, action: str = "use") -> dict:
        if not self.is_connected():
            return {"ok": False, "detail": "not_connected",
                    "hint": f"/publish connect {self.name}"}
        return {"ok": True}


def _connect_google_ads_youtube(open_browser: bool = True, timeout: int = 180) -> dict:
    url, err = _google_ads_youtube_connect_url()
    if not url:
        if err == "not_signed_in":
            return {"ok": False, "detail": "not_signed_in", "hint": "run /login first"}
        if err == "no_workspace":
            return {"ok": False, "detail": "no_workspace",
                    "hint": "Open the Nexplora dashboard once to finish account setup, then retry."}
        return {"ok": False, "detail": f"connect_url_failed:{err}"}
    if open_browser:
        try:
            import webbrowser
            webbrowser.open(url)
        except Exception:
            pass
    return _wait_with_spinner(_google_grant_is_connected, url, timeout)


def gmail_profile() -> dict:
    """Call the live personal.gmail.profile_get tool through
    /api/worlds/personal/dispatch — the real "use" proof, not just connect.
    Returns {ok, result} or {ok: False, error/detail}."""
    who = _google_whoami()
    if not who.get("ok"):
        return {"ok": False, "error": "not_signed_in"}
    workspace_id = who.get("workspace_id")
    if not workspace_id:
        return {"ok": False, "error": "no_workspace"}
    return _bos_post("/api/worlds/personal/dispatch", {
        "workspace_id": workspace_id,
        "tool": "gmail",
        "payload": {},
    })


class ChannelConnector:
    """Base connector. Subclasses implement the platform's OAuth + capabilities.
    Token shape stored in Keychain (JSON): {access_token, refresh_token?,
    expires_at (epoch), scopes:[...]}."""

    name = ""
    display_name = ""
    can_publish = False
    scopes: list = []
    # Confidential by default (needs a client_secret). PKCE public clients (e.g. X)
    # set this False — they connect with ONLY a client_id (no secret), so NX must
    # NOT demand a secret they don't have.
    requires_secret = True
    # Localhost loopback the OAuth redirect comes back to during `connect`.
    redirect_uri = "http://localhost:8723/nx/channels/callback"

    # ── credential + token storage (Keychain-only) ───────────────────────────
    def _svc_app_id(self):  return f"nx-channel-{self.name}-appid"
    def _svc_secret(self):  return f"nx-channel-{self.name}-secret"
    def _svc_token(self):   return f"nx-channel-{self.name}-token"

    def app_id(self):
        # operator's own app overrides; else Nexplora's shared public client_id
        # (only set for PKCE public clients — see _NX_APP_CLIENT_IDS).
        return kc_get(self._svc_app_id()) or _NX_APP_CLIENT_IDS.get(self.name)
    def app_secret(self):   return kc_get(self._svc_secret())

    def is_configured(self) -> bool:
        """Configured = we have what the platform's OAuth needs: a client_id always,
        plus a client_secret ONLY for confidential clients. A PKCE public client (X)
        is configured with just the client_id."""
        if not self.app_id():
            return False
        return bool(self.app_secret()) if self.requires_secret else True

    def setup(self, app_id: str, app_secret: str = None) -> bool:
        """Store the registered app's credentials in the Keychain. For a PKCE public
        client (requires_secret=False) the secret is optional. Values never leave this
        process except to the Keychain."""
        if not app_id:
            return False
        if self.requires_secret and not app_secret:
            return False
        ok1 = kc_set(self._svc_app_id(), app_id.strip())
        ok2 = kc_set(self._svc_secret(), app_secret.strip()) if app_secret else True
        return ok1 and ok2

    def _load_token(self):
        raw = kc_get(self._svc_token())
        if not raw:
            return None
        try:
            return json.loads(raw)
        except Exception:
            return None

    def _save_token(self, tok: dict) -> bool:
        return kc_set(self._svc_token(), json.dumps(tok))

    def disconnect(self) -> bool:
        return kc_delete(self._svc_token())

    def is_connected(self) -> bool:
        """True only with a non-expired access token actually on disk."""
        t = self._load_token()
        if not t or not t.get("access_token"):
            return False
        exp = t.get("expires_at")
        return True if not exp else (float(exp) > time.time())

    def status(self) -> dict:
        """Honest, inspectable state — what the /publish view renders."""
        t = self._load_token() or {}
        return {
            "name": self.name,
            "display_name": self.display_name,
            "configured": self.is_configured(),
            "connected": self.is_connected(),
            "expires_at": t.get("expires_at"),
            "scopes": t.get("scopes") or [],
        }

    # ── OAuth (subclasses implement the platform specifics) ───────────────────
    def auth_url(self, state: str) -> str:
        raise NotImplementedError

    def exchange_code(self, code: str) -> dict:
        raise NotImplementedError

    def refresh(self) -> bool:
        return False  # platforms without refresh re-run connect()

    def preflight(self, action: str = "use") -> dict:
        """Single gate every capability calls first. Returns {ok, detail, hint}
        — fail-closed and honest, never a guess."""
        if requests is None:
            return {"ok": False, "detail": "requests_unavailable",
                    "hint": "NX runtime is missing its HTTP client."}
        if not self.is_configured():
            return {"ok": False, "detail": "not_configured",
                    "hint": f"Register a {self.display_name} app, then: "
                            f"/publish setup {self.name}"}
        if not self.is_connected():
            return {"ok": False, "detail": "not_connected",
                    "hint": f"/publish connect {self.name}"}
        return {"ok": True}


class MetaChannel(_NexploraOAuthBridgedChannel, ChannelConnector):
    """Meta — Facebook Pages + Instagram, connected through Nexplora's own
    shared OAuth vault. The OAuth dance, Graph token, and scoped execution
    proxy all live server-side in nexplora-v2 — NX CLI never holds a Meta
    access token locally."""

    name = "meta"
    display_name = "Meta (Facebook + Instagram)"
    can_publish = True
    server_execution_available = True


def _pkce_pair():
    """PKCE verifier + S256 challenge (for public OAuth clients like X)."""
    import base64
    import hashlib
    import secrets as _secrets
    verifier = base64.urlsafe_b64encode(_secrets.token_bytes(32)).rstrip(b"=").decode()
    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    return verifier, challenge


class GoogleChannel(_GoogleAdsYouTubeBridgedChannel, ChannelConnector):
    """Google — YouTube (read/upload/publish) + Google Ads (campaigns). Connects
    through Nexplora's shared Google Cloud OAuth client via the SAME web OAuth
    route as Google Workspace (/api/oauth/initiate/google, incremental consent) —
    so the REGISTERED redirect_uri and the ONE shared provider 'google' vault
    grant the personal youtube/ads tools read. Previously bos-bridged, which
    400'd (redirect_uri_mismatch — its /api/business-os/connect/callback/youtube
    redirect isn't on the OAuth client) AND stored the token where the personal
    route couldn't read it. youtube round-trips on connect; live Google Ads API
    calls additionally need a Google Ads developer token (surfaced honestly)."""

    name = "google"
    display_name = "Google (Ads + YouTube)"
    can_publish = False


class GoogleWorkspaceChannel(_GoogleWorkspaceBridgedChannel, ChannelConnector):
    """Google Workspace — Gmail, Calendar, Drive, Docs, Sheets — ONE OAuth
    grant via Nexplora's own Google Cloud OAuth client (see
    _GoogleWorkspaceBridgedChannel). Separate from the `google` channel above
    (that one is youtube+ads only, narrower scopes, different bos-bridge
    system). Profile read is live (`nx_channels.gmail_profile()`); send is
    not wired yet — preflight() refuses it honestly rather than faking it.

    display_name deliberately avoids the substrings "google workspace" and
    "gmail" — dozens of pre-existing marketplace catalog entries across other
    worlds (recruiting/HR/ops/sales/etc.) are named exactly "Google Workspace"
    or "Gmail", and connector_for_service() fuzzy-matches a query string
    against `key in display_name.lower()`. A colliding display_name would
    silently reroute ALL of those unrelated listings onto this narrow,
    read-only-scopes connector — a real product decision that needs its own
    deliberate review, not a side effect of a name choice. Reachable only via
    the exact slug: `/publish connect google_workspace`.

    Also deliberately avoids the letter "x" — `key in display_name.lower()`
    means even a single-character query like "x" (XChannel's slug) matches
    as a substring of ANY display_name containing that letter anywhere (an
    earlier draft used "NX Google Connect", whose "Nx" silently hijacked
    `connector_for_service("x")` away from XChannel — caught by
    test_maddog_batch9.py::PublicVsConfidentialAuth::test_x_is_public_client_no_secret)."""

    name = "google_workspace"
    display_name = "Google Mail, Calendar, Drive, Docs"
    can_publish = False


class SnapchatChannel(_BosBridgedChannel, ChannelConnector):
    """Snapchat — Marketing API (ads/content), connected through Nexplora's
    own shared app (see _BosBridgedChannel). Same shape as Meta/TikTok/Google:
    OAuth + token live server-side; publishing isn't wired yet."""

    name = "snapchat"
    display_name = "Snapchat"
    can_publish = False


class XChannel(_NexploraOAuthBridgedChannel, ChannelConnector):
    """X — one Nexplora OAuth grant visible on web and in NX."""

    name = "x"
    display_name = "X (Twitter)"
    can_publish = False
    scopes = ["tweet.read", "users.read", "offline.access"]

    def publish_text(self, message: str, **_) -> dict:
        return self.preflight("publish")


class LinkedInChannel(_NexploraOAuthBridgedChannel, ChannelConnector):
    """LinkedIn — one Nexplora OAuth grant visible on web and in NX."""

    name = "linkedin"
    display_name = "LinkedIn"
    can_publish = False
    scopes = ["openid", "profile", "email"]

    def publish_text(self, message: str, **_) -> dict:
        return self.preflight("publish")


def _slug(name: str) -> str:
    """A Keychain-safe, stable slug for any service display name."""
    s = re.sub(r"[^a-z0-9]+", "-", (name or "").lower()).strip("-")
    return (s[:48] or "svc")


class TikTokChannel(_BosBridgedChannel, ChannelConnector):
    """TikTok — connected through Nexplora's own shared app (see
    _BosBridgedChannel). The OAuth dance + token live server-side in
    nexplora-v2; NX CLI never holds a TikTok access token locally anymore.
    Publishing (video, via the Content Posting API) isn't wired yet — no
    server-side proxy exists for this platform yet — preflight() refuses
    honestly rather than faking it."""

    name = "tiktok"
    display_name = "TikTok"
    can_publish = True


class PinterestChannel(ChannelConnector):
    """Pinterest — OAuth2 (Basic-auth token exchange). Connect + publish Pins.
    Publish requires image_url + board_id (Pins are image-based); caption → `message`."""

    name = "pinterest"
    display_name = "Pinterest"
    can_publish = True
    AUTH = "https://www.pinterest.com/oauth/"
    TOKEN = "https://api.pinterest.com/v5/oauth/token"
    scopes = ["boards:read", "pins:read", "pins:write", "user_accounts:read"]

    def auth_url(self, state: str) -> str:
        import urllib.parse
        return self.AUTH + "?" + urllib.parse.urlencode({
            "response_type": "code", "client_id": self.app_id() or "",
            "redirect_uri": self.redirect_uri, "scope": ",".join(self.scopes), "state": state,
        })

    def _basic(self):
        import base64
        return "Basic " + base64.b64encode(f"{self.app_id()}:{self.app_secret()}".encode()).decode()

    def exchange_code(self, code: str) -> dict:
        if not self.is_configured():
            raise ChannelError("not_configured")
        r = requests.post(self.TOKEN, data={
            "grant_type": "authorization_code", "code": code, "redirect_uri": self.redirect_uri,
        }, headers={"Authorization": self._basic(),
                    "Content-Type": "application/x-www-form-urlencoded"}, timeout=20)
        if r.status_code != 200:
            raise ChannelError(f"token_exchange_failed:{r.status_code}")
        d = r.json()
        if not d.get("access_token"):
            raise ChannelError("token_exchange_no_token")
        tok = {"access_token": d["access_token"], "refresh_token": d.get("refresh_token"),
               "expires_at": time.time() + int(d.get("expires_in") or 2592000),
               "scopes": list(self.scopes)}
        self._save_token(tok)
        return {"ok": True, "expires_at": tok["expires_at"]}

    def refresh(self) -> bool:
        t = self._load_token()
        if not t or not t.get("refresh_token") or not self.is_configured():
            return False
        try:
            r = requests.post(self.TOKEN, data={
                "grant_type": "refresh_token", "refresh_token": t["refresh_token"]},
                headers={"Authorization": self._basic(),
                         "Content-Type": "application/x-www-form-urlencoded"}, timeout=20)
            if r.status_code != 200:
                return False
            d = r.json()
            if not d.get("access_token"):
                return False
            t["access_token"] = d["access_token"]
            t["expires_at"] = time.time() + int(d.get("expires_in") or 2592000)
            return self._save_token(t)
        except Exception:
            return False

    def publish_text(self, message: str, image_url: str = None, board_id: str = None, **_) -> dict:
        pf = self.preflight("publish")
        if not pf["ok"]:
            return pf
        if not (image_url and board_id):
            return {"ok": False, "detail": "pinterest_requires_image_and_board",
                    "hint": "Pinterest publishes Pins — supply image_url + board_id "
                            "(caption goes in 'message')."}
        try:
            tok = (self._load_token() or {}).get("access_token")
            r = requests.post("https://api.pinterest.com/v5/pins",
                              json={"board_id": board_id, "description": (message or "")[:500],
                                    "media_source": {"source_type": "image_url", "url": image_url}},
                              headers={"Authorization": f"Bearer {tok}",
                                       "Content-Type": "application/json"}, timeout=30)
            d = r.json() if r.content else {}
            pid = d.get("id")
            if r.status_code in (200, 201) and pid:
                return {"ok": True, "post_id": pid}
            return {"ok": False, "detail": f"publish_failed:{r.status_code}", "body": r.text[:300]}
        except Exception as e:
            return {"ok": False, "detail": f"request_failed:{type(e).__name__}"}


# Populated from the OAuth endpoint sweep (real documented endpoints only).
# service display name -> {authorize, token, scopes:[...], pkce:bool}
OAUTH_ENDPOINTS = {}


class GenericOAuthConnector(ChannelConnector):
    """Config-driven OAuth2 connector. Given a service's REAL authorize/token
    endpoints, it takes the operator to that provider's actual login and
    completes the standard loopback exchange — the same flow as the hand-built
    connectors, with no per-service code."""

    def __init__(self, display_name, authorize_url, token_url, scopes=None,
                 pkce=False, scope_sep=" "):
        self.name = _slug(display_name)
        self.display_name = display_name
        self._authorize = authorize_url
        self._token = token_url
        self.scopes = list(scopes or [])
        self.uses_pkce = bool(pkce)
        self._scope_sep = scope_sep

    def auth_url(self, state: str) -> str:
        import urllib.parse
        params = {
            "client_id": self.app_id() or "",
            "redirect_uri": self.redirect_uri,
            "state": state,
            "response_type": "code",
        }
        if self.scopes:
            params["scope"] = self._scope_sep.join(self.scopes)
        if self.uses_pkce:
            verifier, challenge = _pkce_pair()
            self._pkce_verifier = verifier
            params["code_challenge"] = challenge
            params["code_challenge_method"] = "S256"
        sep = "&" if "?" in self._authorize else "?"
        return f"{self._authorize}{sep}{urllib.parse.urlencode(params)}"

    def exchange_code(self, code: str) -> dict:
        if not self.is_configured():
            raise ChannelError("not_configured")
        data = {
            "code": code,
            "client_id": self.app_id(),
            "client_secret": self.app_secret(),
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code",
        }
        if self.uses_pkce:
            v = getattr(self, "_pkce_verifier", None)
            if v:
                data["code_verifier"] = v
        r = requests.post(self._token, data=data, timeout=20)
        if r.status_code != 200:
            raise ChannelError(f"token_exchange_failed:{r.status_code}")
        d = r.json() if r.content else {}
        if not d.get("access_token"):
            raise ChannelError("token_exchange_no_token")
        tok = {
            "access_token": d["access_token"],
            "refresh_token": d.get("refresh_token"),
            "expires_at": time.time() + int(d.get("expires_in") or 3600),
            "scopes": list(self.scopes),
        }
        self._save_token(tok)
        return {"ok": True, "expires_at": tok["expires_at"]}

    def refresh(self) -> bool:
        t = self._load_token()
        if not t or not t.get("refresh_token") or not self.is_configured():
            return False
        try:
            r = requests.post(self._token, data={
                "client_id": self.app_id(),
                "client_secret": self.app_secret(),
                "refresh_token": t["refresh_token"],
                "grant_type": "refresh_token",
            }, timeout=20)
            if r.status_code != 200:
                return False
            d = r.json()
            if not d.get("access_token"):
                return False
            t["access_token"] = d["access_token"]
            t["expires_at"] = time.time() + int(d.get("expires_in") or 3600)
            return self._save_token(t)
        except Exception:
            return False


# Per-account OAuth providers: the authorize/token HOST contains the operator's
# own subdomain/domain, so there is no single static URL. NX prompts for the
# tenant once at setup, stores it, and substitutes it into the templates below —
# turning a {subdomain} placeholder (which would open a dead tab) into the real
# login. {tenant} is the substitution slot.
TENANT_OAUTH = {
    "Zendesk": {
        "authorize": "https://{tenant}.zendesk.com/oauth/authorizations/new",
        "token": "https://{tenant}.zendesk.com/oauth/tokens",
        "base_suffix": ".zendesk.com",
        "label": "Zendesk subdomain (e.g. acme for acme.zendesk.com)",
        "scopes": ["read", "write"], "pkce": False,
    },
    "Zendesk Guide / Help Center": {
        "authorize": "https://{tenant}.zendesk.com/oauth/authorizations/new",
        "token": "https://{tenant}.zendesk.com/oauth/tokens",
        "base_suffix": ".zendesk.com",
        "label": "Zendesk subdomain (e.g. acme for acme.zendesk.com)",
        "scopes": ["hc:read", "hc:write", "read", "write"], "pkce": False,
    },
    "Okta": {
        "authorize": "https://{tenant}/oauth2/v1/authorize",
        "token": "https://{tenant}/oauth2/v1/token",
        "base_suffix": None,  # tenant is the full Okta domain
        "label": "Okta domain (e.g. acme.okta.com)",
        "scopes": ["openid", "profile", "email"], "pkce": False,
    },
    "Gorgias": {
        "authorize": "https://{tenant}.gorgias.com/oauth/authorize",
        "token": "https://{tenant}.gorgias.com/oauth/token",
        "base_suffix": ".gorgias.com",
        "label": "Gorgias subdomain (e.g. acme for acme.gorgias.com)",
        "scopes": ["openid", "email", "write:all"], "pkce": False,
    },
    "Snowflake": {
        "authorize": "https://{tenant}.snowflakecomputing.com/oauth/authorize",
        "token": "https://{tenant}.snowflakecomputing.com/oauth/token-request",
        "base_suffix": ".snowflakecomputing.com",
        "label": "Snowflake account host (e.g. ab12345.us-east-2.aws)",
        "scopes": ["session:role:public"], "pkce": False,
    },
}


class TenantOAuthConnector(GenericOAuthConnector):
    """OAuth for per-account providers (Zendesk, Okta, Gorgias, Snowflake) whose
    authorize/token hosts include the operator's own subdomain/domain. The tenant
    is prompted once at setup, stored in the Keychain, and substituted into the
    endpoint templates at use-time — so the login URL is real, never a dead
    {subdomain} placeholder. Not configured until app creds AND tenant exist."""

    def __init__(self, display_name, authorize_tmpl, token_tmpl, base_suffix=None,
                 tenant_label="account", scopes=None, pkce=False, scope_sep=" "):
        # Stash templates BEFORE super().__init__ (whose assignment to
        # self._authorize routes through our property setter).
        self._auth_tmpl = authorize_tmpl
        self._token_tmpl = token_tmpl
        self.base_suffix = base_suffix
        self.tenant_label = tenant_label
        super().__init__(display_name, authorize_tmpl, token_tmpl, scopes=scopes,
                         pkce=pkce, scope_sep=scope_sep)

    def _svc_tenant(self):
        return f"nx-channel-{self.name}-tenant"

    def tenant(self):
        return kc_get(self._svc_tenant())

    def normalize_tenant(self, raw):
        if not raw:
            return ""
        v = raw.strip().split("://", 1)[-1].split("/", 1)[0].strip().strip(".")
        if self.base_suffix and v.lower().endswith(self.base_suffix):
            v = v[: -len(self.base_suffix)]
        return v.strip(".")

    def set_tenant(self, raw):
        v = self.normalize_tenant(raw)
        return bool(v) and kc_set(self._svc_tenant(), v)

    def _resolve(self, tmpl):
        t = self.tenant()
        return tmpl.replace("{tenant}", t) if t else tmpl

    # Templates resolve at use-time, so every inherited method (auth_url,
    # exchange_code, refresh) transparently hits the real per-account host.
    @property
    def _authorize(self):
        return self._resolve(self._auth_tmpl)

    @_authorize.setter
    def _authorize(self, v):
        self._auth_tmpl = v

    @property
    def _token(self):
        return self._resolve(self._token_tmpl)

    @_token.setter
    def _token(self, v):
        self._token_tmpl = v

    def is_configured(self) -> bool:
        return bool(self.app_id() and self.app_secret() and self.tenant())

    def disconnect(self) -> bool:
        kc_delete(self._svc_tenant())
        return super().disconnect()


class GenericApiKeyConnector(ChannelConnector):
    """For API-key services (Stripe, SendGrid, …) the 'login' is pasting the
    key, which we store in the Keychain. Connected == a key is present."""

    def __init__(self, display_name):
        self.name = _slug(display_name)
        self.display_name = display_name
        self.scopes = []

    def is_configured(self) -> bool:
        return True  # no app registration needed for a personal API key

    def is_connected(self) -> bool:
        return bool(kc_get(self._svc_token()))

    def set_api_key(self, key: str) -> bool:
        return kc_set(self._svc_token(), key) if key else False


# Registry — hand-built connectors (carry capabilities). Generic services are
# resolved on demand via connector_for_service().
REGISTRY = {
    MetaChannel.name: MetaChannel,          # Instagram + Facebook
    GoogleChannel.name: GoogleChannel,      # YouTube + Google Ads
    GoogleWorkspaceChannel.name: GoogleWorkspaceChannel,  # Gmail/Calendar/Drive/Docs
    XChannel.name: XChannel,                # X (Twitter)
    LinkedInChannel.name: LinkedInChannel,
    TikTokChannel.name: TikTokChannel,
    PinterestChannel.name: PinterestChannel,
    SnapchatChannel.name: SnapchatChannel,
}


def connector_for_service(name, auth=None):
    """Return a connectable object for ANY service:
      - a hand-built connector if one matches (Meta/Google/X/LinkedIn),
      - else a GenericOAuthConnector if we have its real endpoints,
      - else a GenericApiKeyConnector for api_key services,
      - else None (caller falls back to the resolver's discover path).
    """
    if not name:
        return None
    key = name.strip().lower()
    # hand-built (by name or alias)
    for slug, cls in REGISTRY.items():
        inst = cls()
        if key == slug or key in inst.display_name.lower():
            return inst
    # per-account (tenant) oauth — Zendesk/Okta/Gorgias/Snowflake. The host needs
    # the operator's subdomain/domain, prompted at setup. Checked BEFORE the
    # generic table so a tenant service never falls back to a placeholder URL.
    tspec = TENANT_OAUTH.get(name) or TENANT_OAUTH.get(name.strip())
    if not tspec:
        low = name.strip().lower()
        for k, v in TENANT_OAUTH.items():
            if k.lower() == low:
                tspec = v
                break
    if tspec:
        return TenantOAuthConnector(
            name, tspec["authorize"], tspec["token"],
            base_suffix=tspec.get("base_suffix"),
            tenant_label=tspec.get("label", "account"),
            scopes=tspec.get("scopes"), pkce=tspec.get("pkce", False),
        )
    # generic oauth from the endpoint registry (case-insensitive — the user may
    # type "notion" / "google workspace" but the keys are display-cased)
    spec = OAUTH_ENDPOINTS.get(name) or OAUTH_ENDPOINTS.get(name.strip())
    if not spec:
        low = name.strip().lower()
        for k, v in OAUTH_ENDPOINTS.items():
            if k.lower() == low:
                spec = v
                break
    if spec and spec.get("authorize") and spec.get("token"):
        return GenericOAuthConnector(
            name, spec["authorize"], spec["token"],
            scopes=spec.get("scopes"), pkce=spec.get("pkce", False),
            scope_sep=spec.get("scope_sep", " "),
        )
    if auth == "api_key":
        return GenericApiKeyConnector(name)
    # An OAuth service without a verified endpoint is, in practice, an API-key
    # service (the sweep flags these — Adobe, Cloudflare, Vercel, …). Connect
    # via key paste rather than a dead/guessed OAuth URL. Honest, never fake.
    if auth == "oauth":
        return GenericApiKeyConnector(name)
    return None


# Load the verified OAuth endpoint table (generated from the endpoint sweep) —
# but FILTER any endpoint that can't actually open a real login:
#   - placeholder / tenant-template hosts: <YOUR_OKTA_DOMAIN>, {subdomain}.zendesk.com
#   - confirmed-dead hosts (NXDOMAIN)
# Filtered services fall back to honest api-key connect instead of opening a
# dead browser tab (the same class of bug as google-workspace.com). Proven by a
# real network probe of every endpoint; guarded by test_no_placeholder_endpoints.
import re as _re_ep
_EP_PLACEHOLDER = _re_ep.compile(r"[<{]|YOUR_|example\.com", _re_ep.IGNORECASE)
_EP_DEAD_HOSTS = {"app.intercom.com"}  # confirmed NXDOMAIN; api.intercom.io is the API host


def _ep_usable(spec):
    import urllib.parse as _up
    a = (spec.get("authorize") or "").strip()
    t = (spec.get("token") or "").strip()
    if not a or not t:
        return False
    if _EP_PLACEHOLDER.search(a) or _EP_PLACEHOLDER.search(t):
        return False
    if _up.urlparse(a).netloc.lower() in _EP_DEAD_HOSTS:
        return False
    return True


try:
    from nx_oauth_endpoints import OAUTH_ENDPOINTS as _EP  # type: ignore
    for _k, _v in _EP.items():
        if _ep_usable(_v):
            OAUTH_ENDPOINTS[_k] = _v
except Exception:
    pass


def connect_service(name, auth=None, open_browser=True, prompt_secret=None):
    """Connect ANY directory service: OAuth services run the loopback login;
    api-key services prompt for a key. Honest + fail-closed throughout."""
    ch = connector_for_service(name, auth)
    if ch is None:
        return {"ok": False, "detail": "no_connector",
                "hint": "not a built/known service — use the resolver's discover path"}
    if isinstance(ch, GenericApiKeyConnector) or auth == "api_key":
        if prompt_secret is None:
            return {"ok": False, "detail": "need_key",
                    "hint": f"run /integrations {name} interactively to paste the API key"}
        key = prompt_secret(f"{ch.display_name} API key")
        if ch.set_api_key(key):
            return {"ok": True, "mode": "api_key"}
        return {"ok": False, "detail": "no_key"}
    # OAuth path — must be configured (app credentials) to reach a real login.
    if not ch.is_configured():
        return {"ok": False, "detail": "not_configured",
                "hint": f"register a {ch.display_name} app, then: /integrations {name} setup",
                "auth_url_preview": ch.auth_url("preview")}
    return connect_channel(ch, open_browser=open_browser)


# ── host-execute seam — the ONE entry point the Telegram/host-approval loop uses ─────────────────────────
# NX is one brain; CLI/web/Telegram are transports. When an operator approves an
# action from Telegram, it must run through the SAME proven local connector that
# `/publish` uses — never a parallel cloud re-implementation (that path 402'd and
# faked success). execute_channel_action() is that seam: (slug, method, args) →
# the operator's local connector → its honest result dict. It plugs straight into
# run_with_host_approval()'s execute_fn(server, tool, args) in nx_message.py.

# NATIVE connector methods the host loop may invoke directly — hand-coded on the connector class. NOT arbitrary
# getattr: only these vetted, side-effecting methods, so a staged action can never call an internal
# (_load_token, disconnect, …). REGISTRY actions (nx_channel_actions.ACTION_SPECS — slack/github/zoom/…) are
# ALSO invokable and checked separately, so the seam now covers native (x/linkedin/pinterest) + the registry A-Z.
_CHANNEL_NATIVE_METHODS = {"publish_text"}
# Back-compat alias (older imports reference _CHANNEL_ACTION_METHODS). The host-agent should prefer
# is_channel_action(slug, action), which also sees registry actions.
_CHANNEL_ACTION_METHODS = _CHANNEL_NATIVE_METHODS
# The preflight action-name each native method maps to (connectors gate publish vs read).
_CHANNEL_ACTION_PREFLIGHT = {"publish_text": "publish"}


def is_channel_action(slug, action):
    """True if (slug, action) is executable by a LOCAL connector — either a native whitelisted method on the
    connector class (publish_text on x/linkedin/pinterest) OR a registered action spec (nx_channel_actions).
    The host-agent uses this to route a claimed action to the channel seam vs an MCP tool (by slug+tool, not by
    name alone), so a channel action and an MCP tool that happen to share a name never get mis-routed."""
    action = (action or "").strip()
    if not slug or not action:
        return False
    try:
        from nx_channel_actions import has_registered_action
        if has_registered_action(slug, action):
            return True
    except Exception:
        pass
    try:
        import nx_channel_tools
        if nx_channel_tools.has_tool(slug, action):
            return True
    except Exception:
        pass
    if action in _CHANNEL_NATIVE_METHODS:
        try:
            ch = connector_for_service(slug)
        except Exception:
            ch = None
        return bool(ch is not None and callable(getattr(ch, action, None)))
    return False


def _channel_activity_path():
    return os.path.join(os.path.expanduser("~"), ".nx", "channel-activity.jsonl")


def _first_assigned_agent(slug):
    """Display name of the first agent /assign'd to this channel (~/.nx/channel-agents/<slug>.json), or None."""
    try:
        import re as _re
        _s = (_re.sub(r'[^a-z0-9_]', '_', str(slug).lower()).strip("_") or "channel")[:40]
        p = os.path.join(os.path.expanduser("~"), ".nx", "channel-agents", _s + ".json")
        if os.path.exists(p):
            data = json.load(open(p))
            ags = data.get("agents") or []
            if ags:
                return ags[0].get("display") or ags[0].get("key")
    except Exception:
        pass
    return None


def _log_channel_activity(slug, method, args, result, agent=None):
    """Append a REAL per-channel activity entry (channel · agent · action · time · result) to
    ~/.nx/channel-activity.jsonl. Attributes to `agent` if given, else the channel's ASSIGNED
    agent (/assign), else 'you'. This is what feeds the /publish → channel → /day·/week view."""
    try:
        import time as _t
        res = result if isinstance(result, dict) else {}
        who = agent or _first_assigned_agent(slug) or "you"
        summary = ""
        if isinstance(args, dict):
            for k in ("message", "text", "body", "content", "status", "title"):
                if args.get(k):
                    summary = str(args[k]).replace("\n", " ")[:90]; break
        entry = {"ts": _t.time(), "channel": str(slug), "agent": str(who), "action": str(method),
                 "summary": summary, "ok": bool(res.get("ok")),
                 "ref": str(res.get("post_id") or res.get("id") or "")[:60],
                 "detail": "" if res.get("ok") else str(res.get("detail", ""))[:60]}
        p = _channel_activity_path()
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass


def execute_channel_action(slug, method="publish_text", args=None, agent=None):
    """Run a connector action + record it to the real channel-activity log (attributed to the
    channel's assigned agent). The honest dispatch is unchanged — see _execute_channel_action_inner."""
    args = args if isinstance(args, dict) else {}
    result = _execute_channel_action_inner(slug, method, args)
    _log_channel_activity(slug, method, args, result, agent)
    return result


def _execute_channel_action_inner(slug, method="publish_text", args=None):
    """Run a connector action LOCALLY on this machine and return its HONEST result. Dispatch order:
      1) a NATIVE method on the connector (x/linkedin/pinterest publish_text) — preflight-gated,
      2) else a REGISTERED action spec (nx_channel_actions: slack/github/zoom/… + publish_text aliases),
      3) else honest action_not_wired.
    Returns {ok: True, post_id/id: …} on success or {ok: False, detail, hint?, body?} on failure — NEVER a
    faked success, and never raises (any error is caught and returned as {ok: False, detail})."""
    args = args if isinstance(args, dict) else {}
    if not slug:
        return {"ok": False, "detail": "missing_slug"}
    method = (method or "publish_text").strip()

    # (1) NATIVE connector method (only whitelisted, e.g. publish_text) — the proven X/LinkedIn/Pinterest path.
    if method in _CHANNEL_NATIVE_METHODS:
        try:
            ch = connector_for_service(slug)
        except Exception as e:
            return {"ok": False, "detail": f"resolver_failed:{type(e).__name__}"}
        fn = getattr(ch, method, None) if ch is not None else None
        if callable(fn):
            try:
                pf = ch.preflight(_CHANNEL_ACTION_PREFLIGHT.get(method, "use"))
            except Exception:
                pf = {"ok": True}
            if not (pf or {}).get("ok"):
                return pf
            try:
                out = fn(**args)
                return out if isinstance(out, dict) else {"ok": bool(out), "result": out}
            except TypeError as e:
                return {"ok": False, "detail": f"bad_args:{str(e)[:120]}"}
            except Exception as e:
                return {"ok": False, "detail": f"execution_failed:{type(e).__name__}"}
        # no native method for this connector — fall through to the registry (a generic connector may have a spec)

    # (2) REGISTERED action spec — the data-driven A-Z routes, honest by construction (real HTTP status).
    try:
        from nx_channel_actions import has_registered_action, run_registered_action
        if has_registered_action(slug, method):
            return run_registered_action(slug, method, args)
    except Exception as e:
        return {"ok": False, "detail": f"registry_error:{type(e).__name__}"}

    # (2b) CHANNEL TOOL CATALOG — the comprehensive per-app toolsets (X/YouTube/TikTok/Meta/GWorkspace/Ads/Snap/
    # eBay, ~200 tools). Routes by substrate (local token / BOS proxy / server dispatch); honest by construction.
    try:
        import nx_channel_tools
        if nx_channel_tools.has_tool(slug, method):
            return nx_channel_tools.call(slug, method, args)
    except Exception as e:
        return {"ok": False, "detail": f"catalog_error:{type(e).__name__}"}

    # (3) Honest: this connector CONNECTS but this action isn't wired yet (generic-OAuth shells + BOS bridges).
    try:
        ch = connector_for_service(slug)
        disp = getattr(ch, "display_name", slug) if ch is not None else slug
    except Exception:
        disp = slug
    if disp == slug and _norm_unknown(slug):
        return {"ok": False, "detail": f"unknown_connector:{slug}"}
    return {"ok": False, "detail": "action_not_wired",
            "hint": f"{disp} is connected but '{method}' isn't wired for it yet"}


def _norm_unknown(slug):
    """True if the slug resolves to NO connector at all (so we can say unknown_connector honestly)."""
    try:
        return connector_for_service(slug) is None
    except Exception:
        return False


def channel_execute_fn(server, tool, args):
    """execute_fn adapter for the host-agent / run_with_host_approval(): the host loop passes
    (server, tool, args) where server=connector slug, tool=action method (native or registry). Kept tiny +
    importable so the host-agent wires it in one line."""
    return execute_channel_action(server, tool, args)


def setup_service(name, auth=None, prompt_secret=None, prompt_value=None):
    """Store an operator's credentials for ANY service: OAuth → app Client ID +
    Secret; api-key → the key. Everything goes to the Keychain, never the
    screen/argv. Works for all 239 directory services, not just the built four.

    prompt_value (optional) is used for non-secret, echoed input — the per-account
    subdomain/domain of tenant providers (Zendesk/Okta/Gorgias/Snowflake). Falls
    back to prompt_secret when not supplied."""
    ch = connector_for_service(name, auth)
    if ch is None:
        return {"ok": False, "detail": "no_connector"}
    if isinstance(ch, _NexploraOAuthBridgedChannel):
        return {
            "ok": True,
            "mode": "shared_oauth",
            "provider": ch.vault_provider,
            "detail": "server_managed",
            "hint": f"/publish connect {ch.name}",
        }
    if prompt_secret is None:
        return {"ok": False, "detail": "need_interactive"}
    if isinstance(ch, GenericApiKeyConnector) or auth == "api_key":
        key = prompt_secret(f"{ch.display_name} API key")
        return {"ok": bool(ch.set_api_key(key)), "mode": "api_key"}
    # Per-account OAuth: prompt for the tenant (subdomain/domain) first, then the
    # app creds — without the tenant there is no real host to log in to.
    if isinstance(ch, TenantOAuthConnector):
        ask = prompt_value or prompt_secret
        tenant = ask(ch.tenant_label)
        if not ch.set_tenant(tenant):
            return {"ok": False, "detail": "bad_tenant",
                    "hint": f"need the {ch.tenant_label}"}
        cid = prompt_secret(f"{ch.display_name} Client ID")
        csecret = prompt_secret(f"{ch.display_name} Client Secret")
        return {"ok": bool(ch.setup(cid, csecret)), "mode": "oauth",
                "tenant": ch.tenant()}
    # OAuth: store the registered app's Client ID + Secret.
    cid = prompt_secret(f"{ch.display_name} Client ID")
    csecret = prompt_secret(f"{ch.display_name} Client Secret")
    return {"ok": bool(ch.setup(cid, csecret)), "mode": "oauth"}


def get_channel(name: str):
    cls = REGISTRY.get((name or "").lower())
    return cls() if cls else None


def all_channels():
    return [cls() for cls in REGISTRY.values()]


# ── OAuth connect (localhost loopback, like `gh auth login`) ─────────────────
def connect_channel(channel: "ChannelConnector", open_browser: bool = True,
                    timeout: int = 180) -> dict:
    """Run the authorization-code flow: open the platform's consent screen,
    catch the redirect on a one-shot localhost server, exchange the code.
    Fail-closed: refuses (with a setup hint) if the channel isn't configured.

    Shared-vault channels (Meta, X, LinkedIn) and BOS-bridged channels
    (TikTok, Snapchat) never reach the localhost-loopback code below: they
    connect through Nexplora's server-side apps and callback domain instead."""
    if isinstance(channel, _NexploraOAuthBridgedChannel):
        return _connect_nexplora_oauth(channel, open_browser=open_browser, timeout=timeout)
    if isinstance(channel, _BosBridgedChannel):
        return _connect_bos_bridged(channel, open_browser=open_browser, timeout=timeout)
    if isinstance(channel, _GoogleWorkspaceBridgedChannel):
        return _connect_google_workspace(open_browser=open_browser, timeout=timeout)
    if isinstance(channel, _GoogleAdsYouTubeBridgedChannel):
        return _connect_google_ads_youtube(open_browser=open_browser, timeout=timeout)
    if not channel.is_configured():
        return {"ok": False, "detail": "not_configured",
                "hint": f"/publish setup {channel.name}"}
    import secrets as _secrets
    import threading
    import urllib.parse
    import http.server

    state = _secrets.token_urlsafe(16)
    parsed = urllib.parse.urlparse(channel.redirect_uri)
    port = parsed.port or 8723
    cb_path = parsed.path or "/"
    holder = {}

    class _Handler(http.server.BaseHTTPRequestHandler):
        def log_message(self, *a):  # silence default logging
            pass

        def do_GET(self):
            u = urllib.parse.urlparse(self.path)
            qs = urllib.parse.parse_qs(u.query)
            ok = (u.path == cb_path and qs.get("state", [None])[0] == state
                  and "code" in qs)
            if ok:
                holder["code"] = qs["code"][0]
            self.send_response(200 if ok else 400)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            msg = (b"<h2>NX is connected. You can close this tab.</h2>" if ok
                   else b"<h2>NX authorization failed. Return to the terminal.</h2>")
            try:
                self.wfile.write(msg)
            except Exception:
                pass

    try:
        srv = http.server.HTTPServer(("localhost", port), _Handler)
    except Exception as e:
        return {"ok": False, "detail": f"loopback_bind_failed:{type(e).__name__}",
                "hint": f"free port {port} or set a different redirect"}
    srv.timeout = timeout
    url = channel.auth_url(state)
    if open_browser:
        try:
            import webbrowser
            webbrowser.open(url)
        except Exception:
            pass
    # Serve exactly one request (the redirect), bounded by timeout.
    t = threading.Thread(target=srv.handle_request, daemon=True)
    t.start()
    t.join(timeout + 2)
    try:
        srv.server_close()
    except Exception:
        pass

    code = holder.get("code")
    if not code:
        return {"ok": False, "detail": "authorization_not_completed", "url": url}
    try:
        channel.exchange_code(code)
        return {"ok": True}
    except ChannelError as e:
        return {"ok": False, "detail": str(e)}
    except Exception as e:
        return {"ok": False, "detail": f"exchange_failed:{type(e).__name__}"}


# ── presentation (canonical NX palette, kept cohesive with nx_terminal) ──────
_G = "\033[38;2;200;164;74m"     # gold
_GD = "\033[38;2;196;162;88m"    # gold-dim
_W = "\033[38;2;224;221;212m"    # near-white
_D = "\033[38;2;172;166;148m"    # readable dim
_DR = "\033[38;2;146;140;122m"   # dimmer
_GN = "\033[38;2;80;200;100m"    # green
_R = "\033[0m"


def render_status() -> str:
    """A clean, honest Publish panel — connected / configured / not set up,
    with the exact next action for each. No fake states."""
    out = [f"\n  {_G}✦  Publish{_R}   {_DR}publish where your operators live{_R}\n"]
    for ch in all_channels():
        s = ch.status()
        if s["connected"]:
            dot, label = f"{_GN}●{_R}", f"{_W}connected{_R}"
        elif s["configured"]:
            dot, label = f"{_GD}◐{_R}", f"{_GD}configured{_R} {_DR}— /publish connect {ch.name}{_R}"
        else:
            dot, label = f"{_DR}○{_R}", f"{_DR}not set up — /publish setup {ch.name}{_R}"
        out.append(f"  {dot}  {_G}{ch.display_name}{_R}")
        out.append(f"       {label}")
        if s["connected"] and s.get("expires_at"):
            import datetime
            try:
                when = datetime.datetime.fromtimestamp(float(s["expires_at"])).strftime("%b %d")
            except Exception:
                when = "—"
            out.append(f"       {_DR}token valid through {when}{_R}")
    out.append("")
    return "\n".join(out)


def handle_command(argv, prompt_secret=None) -> str:
    """Dispatch `/publish [status|setup|connect|disconnect] [platform]`.
    `prompt_secret(label)` collects App ID / Secret WITHOUT echoing (getpass);
    injected so it's testable and so secrets never transit argv or the screen."""
    argv = list(argv or [])
    sub = (argv[0].lower() if argv else "status")
    name = argv[1].lower() if len(argv) > 1 else ""

    if sub in ("", "status", "list"):
        return render_status()

    ch = get_channel(name)
    if not ch:
        avail = ", ".join(c.name for c in all_channels())
        return f"\n  {_GD}Unknown channel '{name}'. Available: {avail}{_R}\n"

    if sub == "setup":
        if isinstance(ch, (_NexploraOAuthBridgedChannel, _BosBridgedChannel, _GoogleWorkspaceBridgedChannel)):
            return (f"\n  {_GD}{ch.display_name} uses Nexplora's own app — nothing to "
                    f"register. Run /publish connect {ch.name}.{_R}\n")
        if prompt_secret is None:
            return (f"\n  {_GD}Register a {ch.display_name} app at the platform's "
                    f"developer console, then run /publish setup {ch.name} "
                    f"interactively to store the App ID + Secret in your Keychain.{_R}\n")
        app_id = prompt_secret(f"{ch.display_name} App ID")
        app_secret = prompt_secret(f"{ch.display_name} App Secret")
        if ch.setup(app_id, app_secret):
            return (f"\n  {_GN}✦ {ch.display_name} credentials saved to Keychain.{_R}  "
                    f"{_DR}Next: /publish connect {ch.name}{_R}\n")
        return f"\n  {_GD}Could not save credentials. Both App ID and Secret are required.{_R}\n"

    if sub == "connect":
        res = connect_channel(ch)
        if res.get("ok"):
            return f"\n  {_GN}✦ {ch.display_name} connected.{_R}\n"
        if res.get("detail") == "not_configured":
            return f"\n  {_GD}{ch.display_name} isn't set up yet — /publish setup {ch.name}{_R}\n"
        if res.get("detail") == "not_signed_in":
            return f"\n  {_GD}Run /login first, then /publish connect {ch.name}.{_R}\n"
        if res.get("detail") == "no_workspace":
            return f"\n  {_GD}{res.get('hint', 'Open the Nexplora dashboard once to finish account setup, then retry.')}{_R}\n"
        hint = f"  {_DR}{res.get('url','')}{_R}" if res.get("url") else ""
        return (f"\n  {_GD}Authorization didn't complete ({res.get('detail')}). "
                f"Try again.{_R}\n{hint}\n")

    if sub == "disconnect":
        disconnected = ch.disconnect()
        where = ("your Nexplora account"
                 if isinstance(ch, (_NexploraOAuthBridgedChannel, _BosBridgedChannel, _GoogleWorkspaceBridgedChannel))
                 else "your Keychain")
        if not disconnected:
            return (f"\n  {_GD}{ch.display_name} could not be disconnected from {where}. "
                    f"Nothing was reported as removed; try again.{_R}\n")
        return f"\n  {_D}{ch.display_name} disconnected — token removed from {where}.{_R}\n"

    if sub == "profile":
        if ch.name != GoogleWorkspaceChannel.name:
            return f"\n  {_GD}profile is only wired for {GoogleWorkspaceChannel.name} right now.{_R}\n"
        pf = ch.preflight("profile")
        if not pf.get("ok"):
            return (f"\n  {_GD}{ch.display_name}: {pf.get('detail')} — "
                    f"{pf.get('hint', '')}{_R}\n")
        res = gmail_profile()
        if not res.get("ok"):
            return f"\n  {_GD}Profile read failed: {res.get('error') or res.get('reason')}{_R}\n"
        result = res.get("result") or {}
        email = result.get("emailAddress") or result.get("email") or "(unknown)"
        return f"\n  {_GN}✦ Gmail connected as {email}{_R}\n"

    return f"\n  {_GD}Usage: /publish [status|setup|connect|disconnect|profile] [{name or 'platform'}]{_R}\n"
