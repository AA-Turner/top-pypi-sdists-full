"""
nx_channel_actions — data-driven per-connector ACTION registry + one HONEST executor.

The CLI can CONNECT ~80 services but historically only x/linkedin/pinterest could EXECUTE (they hand-code a
publish_text). Rather than hand-code a method per connector, each connector's real write action is a data spec
here, and run_registered_action() executes any of them generically against the connector's locally-stored
(macOS Keychain) OAuth token.

HONEST BY CONSTRUCTION — the single most important property: the executor surfaces the connector's REAL HTTP
response. A spec whose endpoint/payload is slightly wrong returns {ok: False, detail: "http_404", body: …} —
it NEVER fabricates a success. Specs are best-effort per each provider's PUBLIC API docs; unverified-live specs
are safe precisely because a wrong one fails loudly. Unknown (slug, action) → honest "action_not_wired".
Missing required args → honest "missing_arg:<k>". Not connected → honest "not_connected".

Adding a connector = add one ACTION_SPECS entry (a dict). That is the whole "per-channel execution route".
"""

import json
import re as _re


# Path-segment args substituted into a spec url ({owner}/{repo}/{project_id}/…) must not contain characters that
# could path-traverse or inject a query on the provider's OWN host. (The host itself can't change — it's literal
# before the first placeholder — so this is defense-in-depth, not an SSRF fix.) BODY args (e.g. slack channel
# "#general") are unaffected; only url placeholders are validated.
_URL_ARG_BAD = _re.compile(r"[/?#%\s]|\.\.")


def _url_placeholders(tpl):
    return _re.findall(r"\{([a-zA-Z0-9_]+)\}", tpl or "")


# ── spec helpers ─────────────────────────────────────────────────────────────
def _ok_2xx(status, data):
    return 200 <= status < 300


def _slack_ok(status, data):
    # Slack returns HTTP 200 with {"ok": true|false, ...}. Require an EXPLICIT ok:true — a MISSING/None ok (e.g. a
    # proxy/captive-portal/WAF returning 200 with a non-JSON or empty body, which parses to {}) must NEVER be read
    # as success. Positive-confirmation only, mirroring the native publish_text paths. Never fake success.
    return status == 200 and data.get("ok") is True


def _get(d, *path, default=None):
    cur = d
    for p in path:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(p)
    return cur if cur is not None else default


# ── the registry ─────────────────────────────────────────────────────────────
# Each spec: method, url (may contain {arg} placeholders filled from args+ctx), needs (required arg keys →
# honest missing_arg), auth ('bearer' adds Authorization: Bearer <token>), headers, body (fn(args, ctx)->obj or
# form-string), prefetch (optional fn(token, args)->ctx dict; may return {'_error': ...} to fail honestly),
# ok (fn(status, data)->bool), id (fn(data)->str|None), scopes (doc only), content ('json'|'form').
ACTION_SPECS = {
    # Slack — post a message to a channel. User/bot token; needs the channel id/name.
    "slack": {
        "send_message": {
            "method": "POST", "url": "https://slack.com/api/chat.postMessage",
            "needs": ["channel", "message"], "auth": "bearer", "content": "json",
            "headers": {"Content-Type": "application/json; charset=utf-8"},
            "body": lambda a, c: {"channel": a["channel"], "text": a["message"]},
            "ok": _slack_ok, "id": lambda d: _get(d, "ts"), "scopes": "chat:write",
            "hint": "needs {channel: '#name' or C-id, message}",
        },
    },
    # GitHub — open an issue on a repo.
    "github": {
        "create_issue": {
            "method": "POST", "url": "https://api.github.com/repos/{owner}/{repo}/issues",
            "needs": ["owner", "repo", "title"], "auth": "bearer", "content": "json",
            "headers": {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"},
            "body": lambda a, c: {"title": a["title"], "body": a.get("body") or a.get("message") or ""},
            "ok": lambda s, d: s == 201, "id": lambda d: _get(d, "html_url") or _get(d, "number"),
            "scopes": "repo", "hint": "needs {owner, repo, title, body?}",
        },
    },
    # GitLab — open an issue on a project (numeric project id or url-encoded path).
    "gitlab": {
        "create_issue": {
            "method": "POST", "url": "https://gitlab.com/api/v4/projects/{project_id}/issues",
            "needs": ["project_id", "title"], "auth": "bearer", "content": "json",
            "headers": {"Content-Type": "application/json"},
            "body": lambda a, c: {"title": a["title"], "description": a.get("body") or a.get("message") or ""},
            "ok": lambda s, d: s in (200, 201), "id": lambda d: _get(d, "web_url") or _get(d, "iid"),
            "scopes": "api", "hint": "needs {project_id, title, body?}",
        },
    },
    # Zoom — create a meeting for the authorized user.
    "zoom": {
        "create_meeting": {
            "method": "POST", "url": "https://api.zoom.us/v2/users/me/meetings",
            "needs": ["topic"], "auth": "bearer", "content": "json",
            "headers": {"Content-Type": "application/json"},
            "body": lambda a, c: {"topic": a["topic"], "type": 2,
                                  **({"start_time": a["start_time"]} if a.get("start_time") else {})},
            "ok": lambda s, d: s in (200, 201), "id": lambda d: _get(d, "join_url") or _get(d, "id"),
            "scopes": "meeting:write", "hint": "needs {topic, start_time? ISO8601}",
        },
    },
    # HubSpot — create a CRM contact.
    "hubspot": {
        "create_contact": {
            "method": "POST", "url": "https://api.hubapi.com/crm/v3/objects/contacts",
            "needs": ["email"], "auth": "bearer", "content": "json",
            "headers": {"Content-Type": "application/json"},
            "body": lambda a, c: {"properties": {k: v for k, v in {
                "email": a.get("email"), "firstname": a.get("firstname"), "lastname": a.get("lastname"),
                "company": a.get("company"), "phone": a.get("phone"),
            }.items() if v}},
            "ok": lambda s, d: s in (200, 201), "id": lambda d: _get(d, "id"),
            "scopes": "crm.objects.contacts.write", "hint": "needs {email, firstname?, lastname?, company?}",
        },
    },
    # Asana — create a task in a workspace (or project).
    "asana": {
        "create_task": {
            "method": "POST", "url": "https://app.asana.com/api/1.0/tasks",
            "needs": ["workspace", "name"], "auth": "bearer", "content": "json",
            "headers": {"Content-Type": "application/json"},
            "body": lambda a, c: {"data": {k: v for k, v in {
                "name": a.get("name"), "notes": a.get("notes") or a.get("message"),
                "workspace": a.get("workspace"),
                "projects": [a["project"]] if a.get("project") else None,
            }.items() if v}},
            "ok": lambda s, d: s in (200, 201), "id": lambda d: _get(d, "data", "gid"),
            "scopes": "default", "hint": "needs {workspace (gid), name, project? (gid), notes?}",
        },
    },
    # Notion — create a page under a database or page parent (minimal title-only page).
    "notion": {
        "create_page": {
            "method": "POST", "url": "https://api.notion.com/v1/pages",
            "needs": ["parent_id", "title"], "auth": "bearer", "content": "json",
            "headers": {"Content-Type": "application/json", "Notion-Version": "2022-06-28"},
            "body": lambda a, c: _notion_page_body(a),
            "ok": lambda s, d: s == 200, "id": lambda d: _get(d, "url") or _get(d, "id"),
            "scopes": "insert", "hint": "needs {parent_id, title, parent_type? 'database'|'page' (default database)}",
        },
    },
}


def _notion_page_body(a):
    parent_type = (a.get("parent_type") or "database").lower()
    parent = {"database_id": a["parent_id"]} if parent_type.startswith("data") else {"page_id": a["parent_id"]}
    title_prop = "title"
    body = {
        "parent": parent,
        "properties": {title_prop: {"title": [{"text": {"content": a.get("title", "")}}]}},
    }
    text = a.get("body") or a.get("message")
    if text:
        body["children"] = [{
            "object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": str(text)[:1900]}}]},
        }]
    return body


# Canonical text-post verb: "publish_text" (what the Telegram host-post fast-path stages) maps to each
# connector's primary post-text action, so "post to slack: …" reaches slack.send_message. Connectors whose
# primary action is NOT posting text (github/notion/asana/…) are NOT aliased — publish_text for them honestly
# returns action_not_wired, and the richer action name (create_issue, …) must be used explicitly.
PUBLISH_TEXT_ALIAS = {
    "slack": "send_message",
}


def action_names(slug):
    """The registered action names for a slug (empty tuple if none)."""
    reg = ACTION_SPECS.get(_norm(slug)) or {}
    return tuple(reg.keys())


def has_registered_action(slug, action):
    """True if (slug, action) is wired in the registry (including the publish_text alias)."""
    reg = ACTION_SPECS.get(_norm(slug))
    if not reg:
        return False
    if action in reg:
        return True
    return action == "publish_text" and PUBLISH_TEXT_ALIAS.get(_norm(slug)) in reg


def _norm(slug):
    return (slug or "").strip().lower()


def _resolve_action(slug, action):
    reg = ACTION_SPECS.get(_norm(slug)) or {}
    if action in reg:
        return action, reg[action]
    if action == "publish_text":
        alias = PUBLISH_TEXT_ALIAS.get(_norm(slug))
        if alias and alias in reg:
            return alias, reg[alias]
    return None, None


def run_registered_action(slug, action, args, load_token=None):
    """Execute a registered connector action LOCALLY and return an HONEST result dict.

    load_token: optional callable(slug)->token_dict; defaults to reading the connector's Keychain token via
    nx_channels.connector_for_service(slug)._load_token(). Returns {ok: True, id, status} on a real 2xx, or
    {ok: False, detail, hint?, body?} otherwise. NEVER raises; NEVER fabricates success."""
    args = args if isinstance(args, dict) else {}
    real_action, spec = _resolve_action(slug, action)
    if not spec:
        return {"ok": False, "detail": "action_not_wired:%s.%s" % (_norm(slug), action)}

    missing = [k for k in spec.get("needs", []) if not str(args.get(k) or "").strip()]
    if missing:
        return {"ok": False, "detail": "missing_arg:" + ",".join(missing), "hint": spec.get("hint")}

    # Token: caller-supplied loader or the connector's own Keychain token.
    tok = None
    try:
        if load_token is not None:
            t = load_token(slug)
        else:
            from nx_channels import connector_for_service
            conn = connector_for_service(slug)
            t = conn._load_token() if (conn is not None and hasattr(conn, "_load_token")) else None
        if isinstance(t, dict):
            tok = t.get("access_token")
    except Exception as e:
        return {"ok": False, "detail": "token_load_failed:%s" % type(e).__name__}
    if not tok:
        return {"ok": False, "detail": "not_connected", "hint": "connect %s first" % _norm(slug)}

    # Optional prefetch (e.g. resolve a user/org id). May fail honestly via {'_error': ...}.
    ctx = {}
    pf = spec.get("prefetch")
    if pf:
        try:
            ctx = pf(tok, args) or {}
        except Exception as e:
            return {"ok": False, "detail": "prefetch_failed:%s" % type(e).__name__}
        if isinstance(ctx, dict) and ctx.get("_error"):
            return {"ok": False, "detail": ctx["_error"]}

    import requests
    merged = {**args, **ctx}
    # Reject unsafe url-placeholder values BEFORE formatting (path traversal / query injection on the host).
    for ph in _url_placeholders(spec["url"]):
        if _URL_ARG_BAD.search(str(merged.get(ph, ""))):
            return {"ok": False, "detail": "bad_arg:%s" % ph, "hint": spec.get("hint")}
    try:
        url = spec["url"].format(**merged)
    except Exception as e:
        return {"ok": False, "detail": "bad_url_args:%s" % type(e).__name__, "hint": spec.get("hint")}
    headers = dict(spec.get("headers") or {})
    if spec.get("auth", "bearer") == "bearer":
        headers["Authorization"] = "Bearer " + tok
    body = spec.get("body")
    payload = body(args, ctx) if callable(body) else body

    try:
        method = spec.get("method", "POST").upper()
        kw = {"headers": headers, "timeout": 25}
        if payload is not None:
            if spec.get("content") == "form":
                kw["data"] = payload
            else:
                kw["json"] = payload
        r = requests.request(method, url, **kw)
        try:
            data = r.json() if r.content else {}
        except Exception:
            data = {}
        ok_fn = spec.get("ok") or _ok_2xx
        if ok_fn(r.status_code, data):
            idf = spec.get("id")
            _id = idf(data) if callable(idf) else None
            return {"ok": True, "id": _id, "status": r.status_code, "action": real_action}
        # Honest failure: surface the real status + the provider's own error body (truncated).
        detail = "http_%d" % r.status_code
        if isinstance(data, dict) and (data.get("error") or data.get("message")):
            detail = "%s:%s" % (detail, str(data.get("error") or data.get("message"))[:120])
        return {"ok": False, "detail": detail, "body": (r.text or "")[:300]}
    except Exception as e:
        return {"ok": False, "detail": "request_failed:%s" % type(e).__name__}
