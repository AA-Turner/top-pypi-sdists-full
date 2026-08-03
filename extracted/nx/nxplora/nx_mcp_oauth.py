"""
nx_mcp_oauth.py — connect to a REMOTE MCP server the way Claude Code / Codex do:
OAuth 2.1 + Dynamic Client Registration (DCR) + PKCE.

There is NO app to register and NO secret to ship. The client registers itself
with the provider's auth server on the fly (getting an ephemeral, public
client_id), opens the browser, you sign into YOUR account, and the token is
stored in the macOS Keychain. This is why "it just connects once you sign in" —
the provider IS the OAuth authorization server; NX is only a public client.

Flow (RFC 9728 protected-resource + RFC 8414 auth-server metadata + RFC 7591
DCR + OAuth 2.1 PKCE). Proven live against Notion / Linear / Sentry / Asana /
Atlassian / GitHub / Stripe / PayPal:
  1. POST initialize → 401 + WWW-Authenticate → protected-resource metadata URL
  2. protected-resource metadata → authorization server
  3. auth-server metadata → authorize / token / register endpoints
  4. DCR → ephemeral client_id (token_endpoint_auth_method = none)
  5. PKCE authorize → browser → you sign in → loopback → code
  6. token exchange (PKCE) → access_token (+ refresh) → Keychain
"""
import base64
import hashlib
import json
import secrets
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request

try:
    # reuse NX's Keychain-only secret storage
    from nx_channels import kc_get as _kc_get, kc_set as _kc_set, kc_delete as _kc_delete
except Exception:  # pragma: no cover - standalone fallback
    import subprocess, sys as _sys
    _ACC = "nx"
    _MAC = _sys.platform == "darwin"
    def _kc_get(s):
        if not _MAC:
            from nx_keystore import kr_get; return kr_get(_ACC, s)
        r = subprocess.run(["security", "find-generic-password", "-a", _ACC, "-s", s, "-w"],
                           capture_output=True, text=True)
        return r.stdout.strip() if r.returncode == 0 else None
    def _kc_set(s, v):
        if not _MAC:
            from nx_keystore import kr_set; return kr_set(_ACC, s, v)
        return subprocess.run(["security", "add-generic-password", "-a", _ACC, "-s", s,
                               "-w", v, "-U"]).returncode == 0
    def _kc_delete(s):
        if not _MAC:
            from nx_keystore import kr_delete; return kr_delete(_ACC, s)
        return subprocess.run(["security", "delete-generic-password", "-a", _ACC, "-s", s]).returncode == 0

REDIRECT_URI = "http://localhost:8723/nx/mcp/callback"
_UA = "NX-MCP/1.0 (Nexplora)"
_CTX = ssl.create_default_context()


class MCPOAuthError(Exception):
    pass


# ── curated remote MCP servers (provider-hosted, OAuth via DCR) ──────────────
# slug → {url, name}. Probed live: each returns 401+WWW-Authenticate or
# protected-resource metadata and supports Dynamic Client Registration.
REMOTE_MCP = {
    "airtable": {"url": "https://mcp.airtable.com/mcp", "name": "Airtable"},
    "algolia": {"url": "https://mcp.algolia.com/mcp", "name": "Algolia"},
    "asana": {"url": "https://mcp.asana.com/mcp", "name": "Asana"},
    "atlassian": {"url": "https://mcp.atlassian.com/v1/mcp", "name": "Atlassian (Jira/Confluence)"},
    "box": {"url": "https://mcp.box.com/mcp", "name": "Box"},
    "buildkite": {"url": "https://mcp.buildkite.com/mcp", "name": "Buildkite"},
    "calendly": {"url": "https://mcp.calendly.com", "name": "Calendly"},
    "canva": {"url": "https://mcp.canva.com/mcp", "name": "Canva"},
    "clickup": {"url": "https://mcp.clickup.com/mcp", "name": "ClickUp"},
    "cloudflare": {"url": "https://mcp.cloudflare.com/mcp", "name": "Cloudflare"},
    "cloudinary": {"url": "https://asset-management.mcp.cloudinary.com/sse", "name": "Cloudinary"},
    "docusign": {"url": "https://mcp.docusign.com/mcp", "name": "DocuSign"},
    "drata": {"url": "https://mcp.drata.com/mcp/", "name": "Drata"},
    # GitLab's MCP URL is kept for explicit re-probe / future enablement, but normal NX connect must NOT route
    # here by default: real accounts can finish OAuth and still get POST /api/v4/mcp → 404 when GitLab MCP
    # access/prereqs are disabled. See MCP_BROKEN below; the working path is the Nexplora GitLab REST connector.
    # Workable remains live MCP one-click DCR.
    "gitlab": {"url": "https://gitlab.com/api/v4/mcp", "name": "GitLab"},
    "workable": {"url": "https://mcp.workable.com/mcp", "name": "Workable"},
    "dropbox": {"url": "https://mcp.dropbox.com/mcp", "name": "Dropbox"},
    "exa": {"url": "https://mcp.exa.ai/mcp", "name": "Exa"},
    "figma": {"url": "https://mcp.figma.com/mcp", "name": "Figma"},
    "freshdesk": {"url": "https://mcp.freshdesk.com/mcp", "name": "Freshdesk"},
    "github": {"url": "https://api.githubcopilot.com/mcp/", "name": "GitHub"},
    "globalping": {"url": "https://mcp.globalping.dev/mcp", "name": "Globalping"},
    "gohighlevel": {"url": "https://mcp.gohighlevel.com/mcp", "name": "GoHighLevel"},
    "gong": {"url": "https://mcp.gong.io/mcp", "name": "Gong"},
    "heroku": {"url": "https://mcp.heroku.com/mcp", "name": "Heroku"},
    "hubspot": {"url": "https://mcp.hubspot.com/anthropic", "name": "HubSpot"},
    "hugging-face": {"url": "https://huggingface.co/mcp", "name": "Hugging Face"},
    "linear": {"url": "https://mcp.linear.app/mcp", "name": "Linear"},
    "monday-com": {"url": "https://mcp.monday.com/mcp", "name": "Monday.com"},
    "notion": {"url": "https://mcp.notion.com/mcp", "name": "Notion"},
    "pagerduty": {"url": "https://mcp.pagerduty.com/mcp", "name": "PagerDuty"},
    "paypal": {"url": "https://mcp.paypal.com/mcp", "name": "PayPal"},
    "productboard": {"url": "https://mcp.productboard.com/sse", "name": "Productboard"},
    "rippling": {"url": "https://mcp.rippling.com/mcp", "name": "Rippling"},
    "sentry": {"url": "https://mcp.sentry.dev/mcp", "name": "Sentry"},
    "slack": {"url": "https://mcp.slack.com/mcp", "name": "Slack"},
    "sourcegraph": {"url": "https://sourcegraph.com/.api/mcp/v1", "name": "Sourcegraph"},
    "square": {"url": "https://mcp.squareup.com/mcp", "name": "Square"},
    "stripe": {"url": "https://mcp.stripe.com", "name": "Stripe"},
    "supabase": {"url": "https://mcp.supabase.com/mcp", "name": "Supabase"},
    "tavily": {"url": "https://mcp.tavily.com/mcp", "name": "Tavily"},
    "vanta": {"url": "https://mcp.vanta.com/mcp", "name": "Vanta"},
    "vercel": {"url": "https://mcp.vercel.com", "name": "Vercel"},
    "webflow": {"url": "https://mcp.webflow.com/mcp", "name": "Webflow"},
    "wix": {"url": "https://mcp.wix.com/mcp", "name": "Wix"},
    "xero": {"url": "https://mcp.xero.com/mcp", "name": "Xero"},
    "zapier": {"url": "https://mcp.zapier.com/api/mcp/mcp", "name": "Zapier"},
    # Verified live in the "rest" sweep (2026-06-24): real MCP servers on the
    # provider's canonical domain with a consistent auth host. (Rejected:
    # mcp.pipedrive.ai — wrong TLD; mcp.netsuite.com — unverifiable host.)
    "railway": {"url": "https://mcp.railway.app/", "name": "Railway"},
    "ramp": {"url": "https://mcp.ramp.com/mcp", "name": "Ramp"},
    # 2026-07-16 sweep: first-party hosted MCP servers, each VERIFIED live via the CLI's own discover+register
    # (21 one-click DCR + render/front/smartsheet token). Moves these off the personal-OAuth "not registered"
    # path onto real MCP sign-in. (jira/confluence already alias to atlassian above.)
    # gitlab: remote MCP fails live initialize (mcp_unreachable, Victor-confirmed 2026-07-16) — falls to api-key
    # (MCP_BROKEN + MCP_FORCE_APIKEY below). URL kept for re-verify: https://gitlab.com/api/v4/mcp
    "netlify": {"url": "https://netlify-mcp.netlify.app/mcp", "name": "Netlify"},
    "planetscale": {"url": "https://mcp.pscale.dev/mcp/planetscale", "name": "PlanetScale"},
    "neon": {"url": "https://mcp.neon.tech/mcp", "name": "Neon"},
    "pulumi": {"url": "https://mcp.ai.pulumi.com/mcp", "name": "Pulumi"},
    "launchdarkly": {"url": "https://mcp.launchdarkly.com/mcp/launchdarkly", "name": "LaunchDarkly"},
    # datadog: remote MCP OAuth rejects our loopback ("Invalid redirect URI", Victor-confirmed 2026-07-16) —
    # falls to its byok api-key connector (MCP_BROKEN below). URL kept: https://mcp.datadoghq.com/api/unstable/mcp-server/mcp
    "grafana": {"url": "https://mcp.grafana.com/mcp", "name": "Grafana"},
    "posthog": {"url": "https://mcp.posthog.com/mcp", "name": "PostHog"},
    # mixpanel: MCP is org-flag-gated ("not part of an Org that has mcp access enabled", Victor 2026-07-17) →
    # falls to its byok api-key connector (15 tools). URL kept: https://mcp.mixpanel.com/mcp
    "amplitude": {"url": "https://mcp.amplitude.com/mcp", "name": "Amplitude"},
    "pipedrive": {"url": "https://mcp.pipedrive.ai/mcp", "name": "Pipedrive"},
    # intercom: MCP authorize repeatedly errors ("We're having technical difficulties", Victor-confirmed on
    # TWO accounts 2026-07-17) → falls to its byok Access Token connector (20 tools). URL kept: https://mcp.intercom.com/mcp
    "klaviyo": {"url": "https://mcp.klaviyo.com/mcp", "name": "Klaviyo"},
    "convertkit": {"url": "https://app.kit.com/mcp", "name": "Kit (ConvertKit)"},
    "beehiiv": {"url": "https://mcp.beehiiv.com/mcp", "name": "beehiiv"},
    "miro": {"url": "https://mcp.miro.com", "name": "Miro"},
    # newrelic: MCP is entitlement-gated (http 403 "Missing required entitlements", Victor 2026-07-17) →
    # falls to its byok api-key connector (17 tools). URL kept: https://mcp.newrelic.com/mcp/
    "trello": {"url": "https://mcp.trello.com/v1", "name": "Trello"},
    "render": {"url": "https://mcp.render.com/mcp", "name": "Render"},
    "front": {"url": "https://mcp.frontapp.com/mcp", "name": "Front"},
    "smartsheet": {"url": "https://mcp.smartsheet.com", "name": "Smartsheet"},
    # 2026-07-16 sweep #2: providers the research mis-filed as "needs OAuth app" that actually run a hosted MCP,
    # verified live (discover+register). 5 one-click DCR + 5 token (atlas/bamboohr/okta/youtrack/zoom).
    "zendesk": {"url": "https://mcp.zendesk.com/api/mcp", "name": "Zendesk"},
    "openrouter": {"url": "https://mcp.openrouter.ai/mcp", "name": "OpenRouter"},
    "atlas": {"url": "https://mcp.mongodb.com/mcp", "name": "MongoDB Atlas"},
    "bamboohr": {"url": "https://mcp.bamboohr.com/mcp", "name": "BambooHR"},
    "youtrack": {"url": "https://mcp.youtrack.cloud/mcp", "name": "YouTrack"},
    # REMOVED (2026-07-16, live-initialize re-probe): bitbucket → mcp.atlassian.com is Jira/Confluence (wrong
    # product; Bitbucket has no MCP); hootsuite/okta/zoom → 404; workable → HTML. They fall back to OAuth/api-key.
}
# Common aliases → canonical slug (so /integrations jira hits Atlassian, etc.)
_MCP_ALIASES = {
    "jira": "atlassian", "confluence": "atlassian", "atlassian confluence": "atlassian",
    "atlassian jira": "atlassian", "monday": "monday-com", "huggingface": "hugging-face",
    "hugging face": "hugging-face", "quickbooks online": "quickbooks",
}


_CUSTOM_KEY = "nx-mcp-custom-servers"  # Keychain JSON: {slug: {url, name}}


def _custom():
    raw = _kc_get(_CUSTOM_KEY)
    try:
        return json.loads(raw) if raw else {}
    except Exception:
        return {}


def add_custom_server(url, name=None):
    """BYO: register any remote MCP server URL. Returns its slug."""
    import re
    host = urllib.parse.urlparse(url).netloc or url
    slug = re.sub(r"[^a-z0-9]+", "-", host.lower()).strip("-") or "custom"
    servers = _custom()
    servers[slug] = {"url": url, "name": name or host}
    _kc_set(_CUSTOM_KEY, json.dumps(servers))
    return slug


# ── menu metadata: category grouping + tier (for the /integrations menu) ─────
# Static so the menu renders instantly (no live probe). The ACTUAL connect mode
# is auto-detected at connect time; this is display-only. dcr = one-click sign-in;
# everything not listed token is dcr.
_MCP_CAT = {
    "Sales": ["gohighlevel", "hubspot", "gong"],
    "Code": ["linear", "sentry", "github", "vercel", "cloudflare",
             "railway", "buildkite", "sourcegraph", "heroku", "supabase",
             "globalping", "pagerduty"],
    "Cowork": ["notion", "asana", "clickup", "monday-com", "atlassian",
               "productboard", "calendly", "zapier", "airtable"],
    "Design": ["figma", "canva", "webflow", "wix", "cloudinary"],
    "Finance": ["stripe", "paypal", "ramp", "xero", "square"],
    "Research": ["tavily", "exa", "algolia"],
    "People": ["rippling"],
    "Support": ["freshdesk"],
    "Compliance": ["vanta", "drata"],
    "Docs": ["docusign", "box", "dropbox"],
    "Data/AI": ["hugging-face"],
}
# Token-paste servers (menu badge "token"). Each either has no working DCR, gates behind a confidential app,
# bridges to a foreign auth host, or blocks discovery — so a personal token is the only path. railway/heroku/
# stripe do real one-click OAuth now (badge "sign in"); figma/dropbox/algolia/globalping REGAINED working DCR
# (re-verified 2026-07-16) and are back to "sign in" — keep this set == the connect path (_FORCE_TOKEN) so the
# badge never disagrees with what connect actually does.
# box/pagerduty/slack removed 2026-07-17: their MCP has no DCR, but Nexplora HAS an OAuth app for each
# (NEXPLORA_OAUTH_{BOX,PAGERDUTY,SLACK}_CLIENT_ID in Vercel) → they sign in via backend OAuth (routed in
# nx_cli _NX_OAUTH), not a pasted token. Slack especially: it's the canonical OAuth "Add to Slack" service.
_MCP_TOKEN = {"hubspot", "gong", "github", "docusign", "xero", "freshdesk", "rippling"}

# Connectors whose LIVE remote MCP endpoint is proven broken (redirect-URI mismatch, mcp_unreachable,
# 404, or wrong-product routing) but which have a working api-key / OAuth path instead. POLICY (Victor
# 2026-07-16): keep them LISTED, never route connect to the dead MCP — fall to the key/OAuth path. Add a
# slug here the moment its remote MCP is proven broken by a LIVE `initialize` (not just OAuth discovery).
# is_remote_mcp() returns False for these so the /integrations dispatch skips the MCP branch.
MCP_BROKEN = frozenset({
    # gitlab: OAuth can succeed, then POST /api/v4/mcp returns 404 when GitLab MCP access/prereqs are disabled.
    # Keep URL in REMOTE_MCP for explicit re-probe, but default /integrations gitlab routes to the GitLab REST
    # connector (backend OAuth when provisioned; PAT fallback otherwise), never the dead MCP initialize path.
    "gitlab",
    # workable REMOVED 2026-07-21 → its MCP is live again (see REMOTE_MCP); DCR one-click sign-in.
    "datadog", "coda", "bitbucket", "opsgenie",
    "hootsuite", "okta", "zoom",
    # heroku: mcp.heroku.com 500s on authenticated `initialize` (empty body — Victor-confirmed 2026-07-22:
    # session_expired then http 500). No Nexplora OAuth app yet, but heroku has a personal API-token client
    # (HRKU-, /api/personal/heroku, same shared vault as the web) → it's in _NX_OAUTH + _FORCE_TOKEN so it
    # token-pastes now and flips to one-click OAuth the moment an app is provisioned.
    "heroku",
    # account-entitlement-gated MCPs (sign-in works, provider 403s initialize: "enable mcp access" /
    # "missing required entitlements") — most accounts lack the flag; the genuine api-key connector is the real
    # path (New Relic User key / Mixpanel service account), NOT a lazy byok — no OAuth product exists for either.
    "mixpanel", "newrelic",
    # intercom: MCP authorize repeatedly errors on multiple accounts → routes to backend OAuth (in _OAUTH_PENDING).
    "intercom",
})
# Of the broken set, the OAuth-native services (you sign in, you don't paste a key) with NO OAuth app
# provisioned yet → badge "coming soon" (Victor 2026-07-16: "they're not api keys"). When the app lands
# in Vercel they flip to "sign in" — zoom already has one so it stays sign-in. hootsuite's manifest
# mislabels it byok; it's really OAuth, so it belongs here, not in the api-key set.
# zoho_desk (2026-07-17): the app IS provisioned but Zoho rejects it ("Invalid Client") — DC/config-
# gated upstream; parked here until the round-trip is proven. Its initiate SUCCEEDS (client_id resolves,
# authorize URL builds), so the EARLY gate in nx_cli (before the browser opens) is what actually parks
# it — membership alone only sets the "coming soon" badge in the menu.
# The 13 net-new OAuth connectors (2026-07-17): each needs its own provider OAuth app + (often)
# partner review or per-tenant host handling. Deferred to "coming soon" while we prove the ~50+
# already-connected connectors end-to-end via the web. Flip back to "sign in" as each app lands.
# MCP_COMING_SOON is the EARLY gate (before the browser opens) — reserved for connectors whose OAuth initiate
# SUCCEEDS (client_id resolves, authorize URL builds) but the PROVIDER rejects the app (pending review / DC-gated),
# so the downstream error branch never fires and a browser would open to a broken auth page (e.g. zoho_desk:
# Zoho returns "Invalid Client").
#
# SELF-HEALING (2026-07-21): the ~15 OAuth-native connectors (auth0/okta/opsgenie/intercom/datadog/bitbucket/
# digitalocean/databricks/salesforce/servicenow/typeform/mailchimp/hootsuite/buffer/lever) are NOT parked here.
# They live in nx_cli _NX_OAUTH; while their Nexplora OAuth app is unprovisioned, the initiate FAILS (no client_id)
# → the LATER error branch shows "coming shortly" (guarded from byok by `chosen not in _nxoauth_by_slug`, so an
# OAuth-native connector is NEVER downgraded to a pasted key). The moment NEXPLORA_OAUTH_<SLUG>_CLIENT_ID lands in
# Vercel, the initiate succeeds and the SAME pick connects one-click — no CLI change, no republish needed.
_OAUTH_PENDING = frozenset({"zoho_desk"})
MCP_COMING_SOON = _OAUTH_PENDING


def _cat_of(slug):
    for cat, slugs in _MCP_CAT.items():
        if slug in slugs:
            return cat
    return "More"


def tier_of(slug):
    """Connect METHOD for the menu badge: 'url' (paste your personal server URL —
    Zapier), 'token' (paste a PAT/key — no-DCR servers + DCR-broken-upstream like
    Globalping), or 'dcr' (one-click browser sign-in). _URL_PASTE/_FORCE_TOKEN are
    defined later in the module; referenced at call time so the forward ref is fine."""
    s = _canon(slug)
    if s in _URL_PASTE:
        return "url"
    # GitHub: sign-in (device flow) once an OAuth App client_id is configured,
    # otherwise token-paste.
    if s == "github":
        return "dcr" if _github_client_id() else "token"
    if s in _FORCE_TOKEN or s in _MCP_TOKEN:
        return "token"
    return "dcr"


def menu_registry():
    """REMOTE_MCP shaped like the marketplace registry, for the /integrations
    menu — grouped by menu category, tier instead of tool counts. Keyed by
    display name (get_server resolves names too)."""
    reg = {}
    for slug, e in REMOTE_MCP.items():
        tier = tier_of(slug)
        if tier == "dcr":
            desc = "sign in — no setup, no secret"
        elif tier == "url":
            desc = "paste your personal server URL (NX will ask)"
        else:
            desc = "connect with your own token (PAT / key)"
        reg[e["name"]] = {
            "worlds": [_cat_of(slug).lower()],
            "tier": tier,
            "tools_count": 0,
            "description": desc,
            "slug": slug,
        }
    return reg


def get_server(slug):
    """Resolve a slug, alias, OR display name to {url, name} from the curated set
    OR a BYO custom server."""
    raw = (slug or "").strip().lower()
    key = _MCP_ALIASES.get(raw, raw)
    # _custom() FIRST so a stored personal URL override (e.g. a Zapier per-user
    # MCP URL set via connect_with_url) wins over the built-in default.
    e = _custom().get(key) or REMOTE_MCP.get(key)
    if e:
        return e
    # the menu passes display names ("Monday.com", "Atlassian (Jira/Confluence)")
    for v in list(REMOTE_MCP.values()) + list(_custom().values()):
        if v.get("name", "").strip().lower() == raw:
            return v
    return None


def all_servers():
    out = dict(REMOTE_MCP)
    out.update(_custom())
    return out


def is_remote_mcp(slug):
    # A proven-broken remote MCP must NOT claim the MCP connect branch — its endpoint fails live.
    # Return False so /integrations routes it to the api-key / OAuth path instead (MCP_BROKEN policy).
    raw = (slug or "").strip().lower()
    if _MCP_ALIASES.get(raw, raw) in MCP_BROKEN or raw in MCP_BROKEN:
        return False
    return get_server(slug) is not None


# ── HTTP helpers ─────────────────────────────────────────────────────────────
def _req(url, method="GET", headers=None, data=None, timeout=15):
    h = {"User-Agent": _UA, "Accept": "application/json"}
    h.update(headers or {})
    if isinstance(data, dict):
        data = json.dumps(data).encode()
        h.setdefault("Content-Type", "application/json")
    elif isinstance(data, str):
        data = data.encode()
        # the only string bodies we send are JSON-RPC (discover's initialize probe);
        # strict servers (GoHighLevel) 415 a POST with no Content-Type, killing
        # discovery before the WWW-Authenticate is ever seen. Set it explicitly.
        h.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, method=method, headers=h, data=data)
    try:
        r = urllib.request.urlopen(req, timeout=timeout, context=_CTX)
        return r.status, dict(r.getheaders()), r.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.getheaders()), (e.read() if e.fp else b"")


def _json(body):
    try:
        return json.loads(body)
    except Exception:
        return {}


# ── 1-3. discovery ───────────────────────────────────────────────────────────
def _wk_candidates(issuer):
    """All well-known metadata URLs for an issuer that may carry a path. RFC 8414
    INSERTS .well-known between host and path (host/.well-known/oauth-authorization-server/oauth2/v1)
    — Airtable, Stripe, GoHighLevel use this. OIDC APPENDS it (host/oauth2/v1/.well-known/...).
    NX previously tried only the appended form and failed those servers, dropping
    them to token-paste / 'no OAuth'. Try insert-form first, then append, then bare host."""
    p = urllib.parse.urlparse(issuer)
    host = f"{p.scheme}://{p.netloc}"
    path = p.path.rstrip("/")
    out = []
    for wk in ("oauth-authorization-server", "openid-configuration"):
        if path:
            out.append(f"{host}/.well-known/{wk}{path}")   # RFC 8414 (insert)
            out.append(f"{host}{path}/.well-known/{wk}")    # OIDC (append)
        out.append(f"{host}/.well-known/{wk}")              # bare host
    # de-dupe, preserve order
    seen, uniq = set(), []
    for u in out:
        if u not in seen:
            seen.add(u); uniq.append(u)
    return uniq


def discover(server_url):
    """Return {authorize, token, register, scopes, resource} for a remote MCP
    server, via WWW-Authenticate → protected-resource metadata → auth-server
    metadata. Raises MCPOAuthError if the server doesn't speak MCP OAuth."""
    # nudge the server to reveal its auth metadata
    st, hdrs, _ = _req(server_url, method="POST",
                       headers={"Accept": "application/json, text/event-stream"},
                       data='{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}')
    wa = hdrs.get("WWW-Authenticate") or hdrs.get("www-authenticate") or ""
    prm_url = ""
    if "resource_metadata=" in wa:
        prm_url = wa.split("resource_metadata=", 1)[1].split(",")[0].strip().strip('"')
    p = urllib.parse.urlparse(server_url)
    base = f"{p.scheme}://{p.netloc}"
    candidates = [prm_url] if prm_url else []
    candidates += [base + "/.well-known/oauth-protected-resource" + p.path,
                   base + "/.well-known/oauth-protected-resource"]
    prm = {}
    for u in candidates:
        if not u:
            continue
        s, _, b = _req(u)
        if s == 200:
            prm = _json(b)
            break
    auth_servers = prm.get("authorization_servers") or []
    resource = prm.get("resource") or server_url
    # if no protected-resource doc, fall back to the server's own auth metadata
    auth_bases = auth_servers or [base]
    asm = {}
    for asu in auth_bases:
        for u in _wk_candidates(asu):
            s, _, b = _req(u)
            if s == 200:
                cand = _json(b)
                # only accept a doc that actually carries the endpoints — some
                # hosts 200 a generic page at a wrong well-known path.
                if cand.get("authorization_endpoint") and cand.get("token_endpoint"):
                    asm = cand
                    break
        if asm:
            break
    if not asm.get("authorization_endpoint") or not asm.get("token_endpoint"):
        raise MCPOAuthError("server does not advertise OAuth endpoints")
    return {
        "authorize": asm["authorization_endpoint"],
        "token": asm["token_endpoint"],
        "register": asm.get("registration_endpoint"),
        "scopes": prm.get("scopes_supported") or asm.get("scopes_supported") or [],
        "pkce": asm.get("code_challenge_methods_supported") or ["S256"],
        "resource": resource,
    }


# ── 4. dynamic client registration ───────────────────────────────────────────
def register_client(register_url, redirect_uri=REDIRECT_URI, client_name="NX (Nexplora)"):
    """RFC 7591 DCR. Returns (client_id, client_secret|None). No pre-shared app.
    NOTE: we do NOT send `scope` at all. RFC 7591 makes scope optional, and strict
    servers (Railway, Supabase) 400 on an empty-string scope ("scope must be a
    non-empty string if provided") — which silently dropped them to token-paste.
    Omitting it lets the server apply its default scopes. We also sanitise the
    client_name to alphanumerics/space/hyphen — Calendly rejects the em-dash and
    parens in names like "NX — Atlassian (Jira/Confluence)"."""
    import re as _re
    safe_name = _re.sub(r"\s+", " ", _re.sub(r"[^A-Za-z0-9 -]", " ", client_name)).strip() or "NX"
    st, _, body = _req(register_url, method="POST", data={
        "client_name": safe_name,
        "redirect_uris": [redirect_uri],
        "grant_types": ["authorization_code", "refresh_token"],
        "response_types": ["code"],
        "token_endpoint_auth_method": "none",
    })
    d = _json(body)
    cid = d.get("client_id")
    if not cid:
        raise MCPOAuthError(f"registration failed (http {st})")
    return cid, d.get("client_secret")


# ── 5. PKCE authorize URL ────────────────────────────────────────────────────
def _pkce():
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(40)).rstrip(b"=").decode()
    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    return verifier, challenge


def build_authorize_url(meta, client_id, state, challenge, redirect_uri=REDIRECT_URI):
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "resource": meta.get("resource", ""),
    }
    if meta.get("scopes"):
        params["scope"] = " ".join(meta["scopes"])
    sep = "&" if "?" in meta["authorize"] else "?"
    return f"{meta['authorize']}{sep}{urllib.parse.urlencode(params)}"


# ── 6. token exchange ────────────────────────────────────────────────────────
def exchange_code(meta, client_id, code, verifier, redirect_uri=REDIRECT_URI,
                  client_secret=None):
    fields = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "code_verifier": verifier,
        "resource": meta.get("resource", ""),
    }
    # Some auth servers ignore our requested "none" and issue a CONFIDENTIAL client
    # (DCR returns a client_secret) whose token endpoint only accepts
    # client_secret_basic/post — a public exchange 422s (Supabase). Send the secret
    # (client_secret_post) when we have one.
    if client_secret:
        fields["client_secret"] = client_secret
    st, _, body = _req(meta["token"], method="POST",
                       data=urllib.parse.urlencode(fields),
                       headers={"Content-Type": "application/x-www-form-urlencoded",
                                "Accept": "application/json"})
    d = _json(body)
    if st != 200 or not d.get("access_token"):
        raise MCPOAuthError(f"token exchange failed (http {st})")
    return d


# ── token storage (Keychain) ─────────────────────────────────────────────────
def _current_uid():
    """The signed-in Nexplora user-id, read from ~/.nx/config.json. Connections are
    namespaced by it so two DIFFERENT Nexplora accounts on the SAME Mac never share
    credentials (the long-flagged isolation gap) — and so the local Keychain can be
    reconciled against the per-user server vault. '' when signed out → legacy
    slug-only keys (full back-compat)."""
    try:
        import os as _os, json as _j
        cf = _os.path.join(_os.path.expanduser("~"), ".nx", "config.json")
        with open(cf, "r", encoding="utf-8") as f:
            c = _j.load(f)
        uid = (c.get("nx_user_id") or c.get("user_id") or "")
        uid = str(uid).strip()
        return "" if uid in ("", "anonymous") else uid
    except Exception:
        return ""


def _canon(slug):
    """Resolve any slug / alias / display name to the CANONICAL REMOTE_MCP key.
    Keychain keys are derived from this, so a token saved via an alias
    (`/integrations jira`) or a display name (`Hugging Face`, `Monday.com`)
    lands under the SAME key that connected_slugs()/is_connected() read. Without
    it, an aliased connect orphaned its token under e.g. 'jira' / 'hugging face'
    while every lookup used the canonical 'atlassian' / 'hugging-face' — so the
    service connected but never showed as connected. No-op for canonical slugs."""
    raw = (slug or "").strip().lower()
    if raw in REMOTE_MCP:
        return raw
    aliased = _MCP_ALIASES.get(raw)
    if aliased:
        return aliased
    for k, v in REMOTE_MCP.items():
        if v.get("name", "").strip().lower() == raw:
            return k
    cust = _custom()
    if raw in cust:
        return raw
    for k, v in cust.items():
        if v.get("name", "").strip().lower() == raw:
            return k
    return raw


def _tok_key(slug):
    s = _canon(slug)
    u = _current_uid()
    return f"nx-mcp-{u}-{s}-token" if u else f"nx-mcp-{s}-token"


def _client_key(slug):
    s = _canon(slug)
    u = _current_uid()
    return f"nx-mcp-{u}-{s}-client" if u else f"nx-mcp-{s}-client"


def _client_secret_key(slug):
    s = _canon(slug)
    u = _current_uid()
    return f"nx-mcp-{u}-{s}-csecret" if u else f"nx-mcp-{s}-csecret"


def _legacy_tok_key(slug):
    return f"nx-mcp-{_canon(slug)}-token"


def save_token(slug, tok):
    # PUBLIC (no-auth) server: store just the sentinel — no access_token to persist.
    if tok.get("public"):
        return _kc_set(_tok_key(slug), json.dumps({"public": True}))
    rec = {
        "access_token": tok["access_token"],
        "refresh_token": tok.get("refresh_token"),
        "expires_at": time.time() + int(tok.get("expires_in") or 3600),
        "scope": tok.get("scope", ""),
    }
    # Persist the refresh route so a later silent refresh needs no re-discovery.
    if tok.get("token_endpoint"):
        rec["token_endpoint"] = tok["token_endpoint"]
    if tok.get("resource"):
        rec["resource"] = tok["resource"]
    ok = _kc_set(_tok_key(slug), json.dumps(rec))
    # One-account: push this connection to the Nexplora vault so it shows on the web
    # too. Best-effort + fail-open — no-op when signed out / offline / endpoint not
    # deployed (see nx_vault_sync).
    try:
        import nx_vault_sync as _vs
        _vs.push(slug, rec)
    except Exception:
        pass
    return ok


def load_token(slug):
    raw = _kc_get(_tok_key(slug))
    if not raw and _current_uid():
        # Migrate-on-read: a connection made BEFORE namespacing lives under the
        # legacy slug-only key. Find it, return it, and migrate it forward to the
        # user-namespaced key so existing connections are never lost.
        legacy = _kc_get(_legacy_tok_key(slug))
        if legacy:
            try:
                _kc_set(_tok_key(slug), legacy)
            except Exception:
                pass
            raw = legacy
    return _json(raw) if raw else None


def refresh(slug):
    """Mint a fresh access token from the stored refresh_token, in place. This is
    what keeps a sign-in connected PAST the (often 1-hour) access-token lifetime —
    without it every DCR connection silently drops off /connected and its tools
    stop working until the user signs in again. Non-destructive: a transient
    failure keeps the existing record so it never looks like a surprise logout.
    Returns True on a successful refresh."""
    slug = (slug or "").strip().lower()
    rec = load_token(slug)
    if not rec:
        return False
    rt = rec.get("refresh_token")
    if not rt:
        return False
    te = rec.get("token_endpoint")
    resource = rec.get("resource", "")
    if not te:  # records saved before refresh existed didn't store the route
        entry = get_server(slug)
        if not entry:
            return False
        try:
            meta = discover(entry["url"])
        except Exception:
            return False
        te = meta.get("token")
        resource = resource or meta.get("resource", "")
    if not te:
        return False
    params = {"grant_type": "refresh_token", "refresh_token": rt}
    cid = _kc_get(_client_key(slug))
    if cid:
        params["client_id"] = cid
    csecret = _kc_get(_client_secret_key(slug))
    if csecret and csecret != "__public__":   # confidential client (Supabase) — needed at refresh too
        params["client_secret"] = csecret
    if resource:
        params["resource"] = resource
    try:
        st, _, body = _req(te, method="POST",
                           data=urllib.parse.urlencode(params),
                           headers={"Content-Type": "application/x-www-form-urlencoded",
                                    "Accept": "application/json"})
    except Exception:
        return False
    d = _json(body)
    if st != 200 or not d.get("access_token"):
        return False
    d.setdefault("refresh_token", rt)   # reuse the old RT if the server didn't rotate it
    d["token_endpoint"] = te
    if resource:
        d["resource"] = resource
    save_token(slug, d)
    return True


def is_connected(slug):
    """LOCAL, no network: do we hold a usable credential? A token connect or an
    unexpired sign-in is connected; an expired sign-in still counts if it carries
    a refresh_token (revived lazily at point-of-use — see usable_token). Keeping
    this local is what makes /connected instant and hang-free across many servers,
    instead of firing a refresh round-trip per expired entry while you list."""
    t = load_token(slug)
    if not t:
        return False
    if t.get("public"):
        return True   # public no-auth server (sentinel credential, no token)
    if not t.get("access_token"):
        return False
    return (not _expired(t.get("expires_at"))) or bool(t.get("refresh_token"))


def _expired(exp):
    """True if expires_at is in the past. A corrupt/non-numeric value (Keychain
    tampering) is treated as expired — fail-safe — rather than raising ValueError."""
    if not exp:
        return False
    try:
        return float(exp) <= time.time()
    except (TypeError, ValueError):
        return True


def usable_token(slug):
    """A guaranteed-fresh access token for an actual call: refreshes silently if
    the stored one has expired. Returns None if there's no credential or the
    refresh fails — so the caller fails closed instead of sending a dead token."""
    t = load_token(slug)
    if not t or not t.get("access_token"):
        return None
    if _expired(t.get("expires_at")):
        if not (t.get("refresh_token") and refresh(slug)):
            return None
        t = load_token(slug)
    return t.get("access_token") if t else None


def connected_slugs():
    """Every server with a live Keychain credential — DCR sign-ins AND pasted
    tokens alike (both land under _tok_key, both verified before save). Drives
    the /connected list and auto-connect's "already connected?" check, so no
    path treats a connected service as missing. A slug stays listed as long as
    its credential lives: token connects never expire, and sign-ins are silently
    refreshed (see is_connected -> refresh) so they persist past the short
    access-token lifetime until the refresh token is revoked or the user logs
    out."""
    out = []
    for slug in all_servers():
        try:
            if is_connected(slug):
                out.append(slug)
        except Exception:
            pass
    return out


def _has_credential_fast(slug):
    """PURE read-only presence check for the connected COUNT: is there a usable
    token under the namespaced key? Unlike is_connected() it does NOT take the
    migrate-on-read write path (load_token) and never refreshes — so it is safe to
    run from many threads at once (concurrent Keychain READS only, zero writes)."""
    try:
        raw = _kc_get(_tok_key(slug))
        if not raw:
            return False
        t = _json(raw)
        if not t:
            return False
        if t.get("public"):
            return True
        if not t.get("access_token"):
            return False
        return (not _expired(t.get("expires_at"))) or bool(t.get("refresh_token"))
    except Exception:
        return False


def connected_slugs_fast():
    """Parallel, read-only variant of connected_slugs() for the welcome-banner COUNT.
    connected_slugs() scans all ~71 servers SERIALLY — each a `security` subprocess
    read (~5s+ total) — which blows the banner's 4s budget so the "N connected" count
    silently drops. This runs the pure-read presence check across a bounded pool (well
    under 1s): no migrate-on-read, no refresh, so parallelizing is safe. Only misses
    legacy un-migrated tokens (none after a vault sync) — fine for a display count."""
    servers = list(all_servers())
    import concurrent.futures as _cf
    try:
        with _cf.ThreadPoolExecutor(max_workers=16) as _ex:
            return [s for s in _ex.map(lambda sl: sl if _has_credential_fast(sl) else None, servers) if s]
    except Exception:
        return [s for s in servers if _has_credential_fast(s)]


def disconnect(slug):
    _kc_delete(_client_key(slug))
    _kc_delete(_client_secret_key(slug))
    # drop a personal URL override (Zapier etc.) so disconnect fully forgets it and
    # a later reconnect starts clean from the built-in default.
    try:
        servers = _custom()
        c = _canon(slug)
        if c in servers:
            del servers[c]
            _kc_set(_CUSTOM_KEY, json.dumps(servers))
    except Exception:
        pass
    # delete BOTH the namespaced and the legacy slug-only key so a disconnect is
    # complete regardless of which era the connection was stored in.
    _kc_delete(_legacy_tok_key(slug))
    return _kc_delete(_tok_key(slug))


# ── GitHub: device-flow sign-in ──────────────────────────────────────────────
# GitHub's MCP has no DCR, so OAuth needs a pre-registered app. Device flow needs
# ONLY the client_id (public, no secret) — perfect for a shipped CLI. Set the
# Nexplora GitHub OAuth App's client_id below (or via Keychain "nx-github-oauth-
# client" / env NX_GITHUB_CLIENT_ID). Empty => GitHub falls back to token-paste.
# Nexplora's GitHub App client_id (PUBLIC — device flow needs no secret). base64
# only to match the package's no-plaintext convention; this is not a secret.
GH_CLIENT_ID = base64.b64decode("SXYyM2xpT2NURExhNERhOHJxc2M=").decode()


def _github_client_id():
    return (_kc_get("nx-github-oauth-client")
            or _os_env("NX_GITHUB_CLIENT_ID")
            or GH_CLIENT_ID).strip()


def _os_env(k):
    import os
    return os.environ.get(k, "") or ""


def _github_device_connect(slug, client_id, open_browser=True, timeout=300):
    """OAuth 2.0 Device Authorization Grant for GitHub. No secret, no loopback:
    request a user code, send the operator to github.com/login/device, poll until
    they approve, then verify the token against the MCP endpoint and save."""
    import time as _t
    scope = "repo read:org read:user gist workflow"
    st, _, body = _req("https://github.com/login/device/code", method="POST",
                       headers={"Accept": "application/json",
                                "Content-Type": "application/x-www-form-urlencoded"},
                       data=urllib.parse.urlencode({"client_id": client_id, "scope": scope}))
    d = _json(body)
    device_code = d.get("device_code")
    user_code = d.get("user_code")
    verify_uri = d.get("verification_uri") or "https://github.com/login/device"
    interval = int(d.get("interval") or 5)
    expires_in = int(d.get("expires_in") or 900)
    if not device_code or not user_code:
        return {"ok": False, "detail": "device_code_failed",
                "hint": d.get("error_description") or f"http {st}"}
    print(f"\n  \033[38;2;200;164;74mGitHub sign-in:\033[0m enter code "
          f"\033[1m{user_code}\033[0m at \033[4m{verify_uri}\033[0m")
    if open_browser:
        try:
            import webbrowser
            webbrowser.open(verify_uri)
        except Exception:
            pass
    deadline = _t.time() + min(timeout, expires_in)
    entry = get_server(slug)
    while _t.time() < deadline:
        _t.sleep(interval)
        s2, _, b2 = _req("https://github.com/login/oauth/access_token", method="POST",
                         headers={"Accept": "application/json",
                                  "Content-Type": "application/x-www-form-urlencoded"},
                         data=urllib.parse.urlencode({
                             "client_id": client_id, "device_code": device_code,
                             "grant_type": "urn:ietf:params:oauth:grant-type:device_code"}))
        t = _json(b2)
        at = t.get("access_token")
        if at:
            try:
                import nx_mcp_client as _cl
                _cl.MCPSession(entry["url"], at).initialize()
            except Exception as e:
                return {"ok": False, "detail": "token_rejected",
                        "hint": f"GitHub authorized, but the MCP endpoint rejected the "
                                f"token ({type(e).__name__}) — your account may lack Copilot/MCP access."}
            save_token(slug, {"access_token": at,
                              "refresh_token": t.get("refresh_token"),
                              "expires_in": int(t.get("expires_in") or 10 ** 9),
                              "scope": t.get("scope", "")})
            return {"ok": True, "name": entry["name"], "mode": "device"}
        err = t.get("error")
        if err == "authorization_pending":
            continue
        if err == "slow_down":
            interval += 5
            continue
        if err in ("expired_token", "access_denied", "incorrect_device_code"):
            return {"ok": False, "detail": "device_" + err, "hint": t.get("error_description", "")}
    return {"ok": False, "detail": "device_timeout", "hint": "sign-in not completed in time"}


# ── orchestration: the full connect ──────────────────────────────────────────
def connect(slug, open_browser=True, timeout=300, _opener=None):
    """Run the whole DCR + PKCE loopback flow for a remote MCP server slug.
    Opens the provider's login, captures the redirect on localhost, exchanges
    the code, stores the token. Returns {ok, ...}. Honest/fail-closed."""
    slug = (slug or "").strip().lower()
    entry = get_server(slug)
    if not entry:
        return {"ok": False, "detail": "not_remote_mcp"}
    # GitHub: no DCR — use device flow when an OAuth App client_id is configured.
    if _canon(slug) == "github":
        cid = _github_client_id()
        if cid:
            return _github_device_connect(slug, cid, open_browser=open_browser, timeout=timeout)
        return {"ok": False, "detail": "no_dcr",
                "hint": "GitHub needs your token (no OAuth app configured yet)"}
    try:
        meta = discover(entry["url"])
    except MCPOAuthError as e:
        # No OAuth advertised. Some MCP servers are PUBLIC (no auth) — probe the
        # endpoint with no token; if it serves MCP, connect it as a public server.
        pub = _try_public(slug, entry)
        if pub.get("ok"):
            return pub
        return {"ok": False, "detail": "discovery_failed", "hint": str(e)}
    if not meta.get("register"):
        return {"ok": False, "detail": "no_dcr",
                "hint": "server requires a pre-registered client"}
    # Register a FRESH DCR client on every connect. Some servers (Supabase) purge/rotate their ephemeral DCR
    # clients, so a cached client_id later gets "Unrecognized client_id" at the AUTHORIZE step — which happens
    # in the browser, where we can't catch it and re-register. Registering fresh each time sidesteps the stale-
    # client trap entirely; the fresh client is cached for this connection's silent refresh. Fall back to a
    # cached client only if registration is unavailable/rate-limited.
    try:
        cid, new_secret = register_client(meta["register"], client_name=f"NX — {entry['name']}")
        _kc_set(_client_key(slug), cid)
        csecret = new_secret or "__public__"
        _kc_set(_client_secret_key(slug), csecret)
    except MCPOAuthError:
        cid = _kc_get(_client_key(slug))
        csecret = _kc_get(_client_secret_key(slug))
        if not cid or not csecret:
            # DCR endpoint gated/rate-limited AND no usable cached client → fall back to a user-brought token
            return {"ok": False, "detail": "no_dcr",
                    "hint": "this server needs your own token"}
    real_secret = csecret if csecret and csecret != "__public__" else None

    state = secrets.token_urlsafe(16)
    verifier, challenge = _pkce()
    url = build_authorize_url(meta, cid, state, challenge)

    code = _run_loopback(url, state, open_browser=open_browser, timeout=timeout,
                         opener=_opener)
    if not code:
        return {"ok": False, "detail": "no_code", "hint": "authorization not completed"}
    try:
        tok = exchange_code(meta, cid, code, verifier, client_secret=real_secret)
    except MCPOAuthError as e:
        return {"ok": False, "detail": "exchange_failed", "hint": str(e)}
    tok["token_endpoint"] = meta.get("token")   # so silent refresh needs no re-discovery
    tok["resource"] = meta.get("resource", "")
    # VERIFY the MCP endpoint actually works before declaring connected. OAuth
    # succeeding does NOT mean the server serves MCP at this URL — a wrong
    # transport/path (e.g. an /sse-only endpoint) 404s on initialize. Without
    # this check a broken endpoint saved a token and showed "ready", then failed
    # the moment a tool was called. Fail closed instead (like connect_with_token).
    try:
        import nx_mcp_client as _cl
        _cl.MCPSession(entry["url"], tok["access_token"]).initialize()
    except Exception as e:
        # A 401 here is NOT an unreachable endpoint — it responded and rejected
        # the token. That usually means the provider needs account-side MCP setup
        # (e.g. Zapier: create your MCP server + pick actions first), not a bug in
        # the connect flow. Say that honestly instead of "didn't respond".
        if isinstance(e, _cl.MCPAuthError):
            return {"ok": False, "detail": "needs_account_setup",
                    "hint": f"signed in, but {entry['name']} rejected the token at its MCP "
                            f"endpoint — this provider likely needs you to set up its MCP "
                            f"server in your {entry['name']} account first, then reconnect."}
        return {"ok": False, "detail": "mcp_unreachable",
                "hint": f"signed in, but {entry['name']}'s MCP endpoint rejected initialize "
                        f"[{e}] — not saving a connection that can't be used."}
    save_token(slug, tok)
    return {"ok": True, "name": entry["name"], "scope": tok.get("scope", "")}


def _try_public(slug, entry=None):
    """Probe an MCP endpoint with NO auth. If it initializes, it's a PUBLIC server
    (e.g. DeepWiki) — store a public sentinel credential (no token) so it becomes
    first-class in the native loop. MCPSession omits the Authorization header when
    the token is None. Fails closed if the server actually needs auth."""
    entry = entry or get_server(slug)
    if not entry:
        return {"ok": False, "detail": "not_remote_mcp"}
    try:
        import nx_mcp_client as _cl
        _cl.MCPSession(entry["url"], None).initialize()
    except Exception as e:
        return {"ok": False, "detail": "not_public", "hint": type(e).__name__}
    save_token(slug, {"public": True, "expires_in": 10 ** 9})
    return {"ok": True, "name": entry["name"], "mode": "public"}


def connect_with_token(slug, token):
    """Connect a remote MCP server that doesn't support DCR (GitHub, Stripe) with
    a bearer token the OPERATOR brings — their own GitHub PAT / Stripe key. No app
    to register, no secret shipped. The token is verified with a live initialize
    and stored in the Keychain. Honest: fails closed if the server rejects it."""
    slug = (slug or "").strip().lower()
    entry = get_server(slug)
    if not entry:
        return {"ok": False, "detail": "not_remote_mcp"}
    if not token:
        return {"ok": False, "detail": "no_token"}
    # verify the token actually authorizes against the server before saving
    try:
        import nx_mcp_client as _cl
        sess = _cl.MCPSession(entry["url"], token)
        sess.initialize()
    except Exception as e:
        return {"ok": False, "detail": "token_rejected", "hint": type(e).__name__}
    save_token(slug, {"access_token": token, "expires_in": 10 ** 9})  # user token, no expiry
    return {"ok": True, "name": entry["name"], "mode": "token"}


# Servers that advertise DCR / OAuth but whose one-click flow can't actually
# complete for a public DCR client, so we force bring-your-own-token instead of
# running a doomed browser flow. All verified live 2026-06-30:
#   globalping — /authorize bridges to auth.globalping.io which rejects DCR
#                clients ("Invalid parameter: publicCodeId").
#   algolia    — advertises a registration_endpoint that 400s every client
#                ("This client is not allowed to register") — an allowlist trap.
#   box        — no DCR; confidential app only (client_secret_*), no public "none".
#   docusign   — RBAC-gated; expects a DocuSign-issued JWT (account setup needed).
#   pagerduty  — auth host app.pagerduty.com differs; public DCR can't complete.
#   rippling   — Cloudflare blocks metadata discovery for non-browser clients.
#   dropbox, figma, github, gong, hubspot, slack, xero, freshdesk — no usable
#                public-client DCR path; a personal token is the route.
# NOTE: supabase + railway were REMOVED — both have WORKING DCR (verified live:
# supabase /platform/oauth/apps/register returns a client_id), so they do real
# one-click sign-in. github has NO DCR and NX ships no GitHub OAuth app, so it
# stays token-only until a GitHub OAuth App client_id is registered for NX.
_FORCE_TOKEN = {
    # No usable DCR (no registration endpoint or discovery blocked) — a pasted token is the only path.
    # Re-verified 2026-07-16: figma/dropbox/algolia/globalping REGAINED working DCR since the 2026-06-30 sweep
    # and are back to one-click sign-in; these stay token because their DCR is genuinely absent/broken.
    # box/pagerduty/slack removed 2026-07-17 → backend OAuth (they have Nexplora OAuth apps; see _MCP_TOKEN note).
    "docusign", "gong", "hubspot", "rippling", "xero", "freshdesk", "heroku", "bitbucket",
    # GitLab's hosted MCP can OAuth successfully and then 404 initialize unless MCP is enabled account/group-side.
    # The default NX path is the REST connector; keep the menu badge honest if this entry is shown from REMOTE_MCP.
    "gitlab",
    # DCR is advertised but their authorize endpoint needs a provider-specific param the generic flow can't
    # supply — Buildkite wants organization_uuid, Productboard wants a workspace. Both MCP endpoints DO accept a
    # Bearer PAT (verified: 401 invalid_token on a bad token), so paste-a-token is the working path.
    "buildkite", "productboard",
    # 2026-07-16 sweep: hosted MCP servers with NO DCR (no registration endpoint) — paste a token.
    "render", "front", "smartsheet",
    "atlas", "bamboohr", "youtrack",
}  # github handled separately (device flow when client_id set, else token)


def needs_token(slug):
    """True if this remote MCP server has no usable DCR — connect via a pasted
    token. Covers servers with no registration endpoint AND servers whose DCR is
    advertised but broken upstream (_FORCE_TOKEN)."""
    s = _canon(slug)
    # GitHub: token only until an OAuth App client_id is configured (then device flow).
    if s == "github":
        return not bool(_github_client_id())
    if s in _FORCE_TOKEN:
        return True
    entry = get_server(slug)
    if not entry:
        return False
    try:
        meta = discover(entry["url"])
        return not meta.get("register")
    except MCPOAuthError:
        return True


# Servers that are NOT one-click OAuth: the user creates a personal MCP server in
# the provider's dashboard and gets a URL that carries its own key (Zapier). The
# generic OAuth endpoint mints a token its MCP endpoint then rejects (401), so the
# only reliable connect is paste-your-personal-URL.
_URL_PASTE = {"zapier"}


def needs_url_paste(slug):
    return _canon(slug) in _URL_PASTE


def set_server_url(slug, url, name=None):
    """Override the endpoint URL for a known slug with a user-supplied one (e.g. a
    personal Zapier MCP URL that carries its own key). Stored in the custom-server
    table so get_server() returns it and it survives restarts."""
    s = _canon(slug)
    servers = _custom()
    servers[s] = {"url": url, "name": name or (get_server(s) or {}).get("name") or s}
    _kc_set(_CUSTOM_KEY, json.dumps(servers))
    return s


def connect_with_url(slug, url, name=None):
    """Connect a server whose PERSONAL URL carries the credential — Zapier's
    mcp.zapier.com/api/mcp/s/<key>/mcp URL. The URL self-authorizes, so we try a
    no-bearer initialize first; if the URL turns out to still want a sign-in we
    fall back to the normal DCR flow against that same URL. Verified live before
    saving — never stores a connection that can't be used."""
    s = _canon(slug)
    url = (url or "").strip()
    if not url.lower().startswith("https://"):
        return {"ok": False, "detail": "bad_url",
                "hint": "paste the full https:// MCP server URL from the provider"}
    name = name or (get_server(s) or {}).get("name") or s
    set_server_url(s, url, name)            # so verify + future calls hit this URL
    import nx_mcp_client as _cl
    # 1) URL-as-credential (key embedded in the URL → no bearer needed)
    try:
        _cl.MCPSession(url, None).initialize()
        save_token(s, {"public": True, "expires_in": 10 ** 9})
        return {"ok": True, "name": name, "mode": "url"}
    except _cl.MCPAuthError:
        pass                                # URL still wants a sign-in → DCR below
    except Exception as e:
        return {"ok": False, "detail": "mcp_unreachable", "hint": str(e) or type(e).__name__}
    # 2) fall back to DCR + PKCE against the personal URL
    return connect(s)


def connect_url(url, name=None, open_browser=True, timeout=300, _opener=None):
    """BYO: connect ANY remote MCP server by URL — same DCR + PKCE flow, no
    secret. Registers it, then runs the sign-in. Returns the connect result."""
    slug = add_custom_server(url, name)
    res = connect(slug, open_browser=open_browser, timeout=timeout, _opener=_opener)
    res["slug"] = slug
    return res


_ACTIVE_LOOPBACK = None  # the in-flight callback HTTPServer, so a NEW sign-in can reclaim 8723 from an abandoned one


def _run_loopback(auth_url, state, open_browser=True, timeout=180, opener=None):
    import http.server
    import threading
    import webbrowser
    import time as _time
    global _ACTIVE_LOOPBACK

    parsed = urllib.parse.urlparse(REDIRECT_URI)
    port = parsed.port or 8723
    cb_path = parsed.path or "/"
    holder = {}

    class _H(http.server.BaseHTTPRequestHandler):
        def log_message(self, *a):
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
            threading.Thread(target=self.server.shutdown, daemon=True).start()

    # RECLAIM 8723 from an ABANDONED prior sign-in in THIS process. If the user opened a connect and never
    # finished it (e.g. the provider's OAuth page errored, like Productboard's workspace error), that loopback
    # keeps the callback port bound — and then EVERY other connect fails to bind. Tear the old one down first.
    _prev = _ACTIVE_LOOPBACK
    if _prev is not None:
        try: _prev.shutdown()
        except Exception: pass
        try: _prev.server_close()
        except Exception: pass
        _ACTIVE_LOOPBACK = None
    # allow_reuse_address so a just-closed socket in TIME_WAIT doesn't block the next connect in the
    # same nx session (the fixed callback port 8723 is reused for every MCP sign-in).
    class _ReusableHTTPServer(http.server.HTTPServer):
        allow_reuse_address = True
    srv = None
    for _attempt in range(2):
        try:
            srv = _ReusableHTTPServer(("127.0.0.1", port), _H)
            break
        except OSError as e:
            if _attempt == 0:
                _time.sleep(0.5)  # a TIME_WAIT socket clears quickly; retry once
                continue
            raise MCPOAuthError(
                f"loopback port {port} is busy — a previous sign-in is still open. "
                f"Close that browser tab (or restart nx) and try again. [{e}]")
    _ACTIVE_LOOPBACK = srv
    srv.timeout = timeout
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    if opener:
        opener(auth_url)
    elif open_browser:
        webbrowser.open(auth_url)
    t.join(timeout)
    try:
        srv.shutdown()
    except Exception:
        pass
    # CRITICAL: server_close() RELEASES the listening socket. shutdown() only stops serve_forever;
    # without server_close() port 8723 stays bound for the whole nx REPL session, so the SECOND
    # (and every later) MCP connect in that session failed "Address already in use".
    try:
        srv.server_close()
    except Exception:
        pass
    if _ACTIVE_LOOPBACK is srv:
        _ACTIVE_LOOPBACK = None
    return holder.get("code")
