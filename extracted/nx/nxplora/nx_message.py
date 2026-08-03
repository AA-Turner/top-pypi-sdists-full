"""GRAIL Phase 5 follow-up #1 — per-operator report-back channels (`/message`).

Where the autonomy loop (and, later, any agent/action) sends its report-back is the OPERATOR's choice, not a
hardcoded Telegram. This module owns the channel registry + the fan-out:

    /message                      show configured channels + which are active for reports
    /message telegram             configure Telegram (bot token → Keychain, chat_id auto-resolved)
    /message email                configure SMTP email
    /message imessage <handle>    configure iMessage (macOS, via osascript — no secret)
    /message whatsapp             configure WhatsApp via Twilio
    /message on|off <channel>     toggle a channel for autonomy reports

Secrets (bot tokens, SMTP/Twilio passwords) go to the macOS Keychain via getpass — NEVER argv/screen/config.
Non-secret prefs (chat_id, smtp host, imessage handle, active flags) live in ~/.nx/config.json under
"message_channels". send_report(text, cfg) fans out to every ACTIVE + configured channel and returns an honest
per-channel status — the loop treats a run as reported only if at least one channel actually delivered.
"""
import os
import json
import subprocess

try:
    from nx_channels import kc_get, kc_set, kc_delete   # reuse the audited Keychain helpers (getpass-fed)
except Exception:  # pragma: no cover - keychain optional in some test envs
    def kc_get(service):
        return os.environ.get("NXKC_" + service)
    def kc_set(service, value):
        os.environ["NXKC_" + service] = value; return True
    def kc_delete(service):
        os.environ.pop("NXKC_" + service, None); return True

CHANNELS = ("telegram", "email", "imessage", "whatsapp", "sms")


def channel_handle(channel: str, entry: dict) -> str:
    """WHERE a report-back channel's address lives in its config entry — the ONE rule.

    Telegram stores a numeric `chat_id` (Telegram issues it; there is no "to" address to type). Every other
    channel stores `to`. That asymmetry used to be re-stated inline wherever an address was read, and the
    /channels reach hub duly re-stated it WRONG — it asked telegram for "to", got nothing, and rendered a
    permanently blank address column for the flagship channel while /message showed the chat id correctly
    for the same config. Two surfaces disagreeing about one binding is exactly what a second copy of a rule
    buys you. There is one copy now, and both read it."""
    e = entry or {}
    return str((e.get("chat_id") if channel == "telegram" else e.get("to")) or "").strip()


_CONFIG = os.path.join(os.path.expanduser("~"), ".nx", "config.json")

# Keychain service names for each channel's secret.
_KC = {"telegram": "msg-telegram-token", "email": "msg-email-pass",
       "whatsapp": "msg-whatsapp-token", "sms": "msg-sms-token"}


# ── config read/modify/write (only the message_channels subtree) ─────────────────────────────────────────

def _load_config():
    try:
        with open(_CONFIG) as f:
            return json.load(f)
    except Exception:
        return {}


def _save_channels(mc):
    """Persist the message_channels subtree without disturbing the rest of ~/.nx/config.json."""
    cfg = _load_config()
    cfg["message_channels"] = mc
    tmp = _CONFIG + ".tmp"
    with open(tmp, "w") as f:
        json.dump(cfg, f, indent=2)
    os.replace(tmp, _CONFIG)


def channels_state(cfg=None):
    """{channel: {"configured": bool, "active": bool, ...prefs}} — merges config prefs + keychain presence."""
    cfg = cfg if cfg is not None else _load_config()
    mc = (cfg or {}).get("message_channels") or {}
    out = {}
    for ch in CHANNELS:
        c = dict(mc.get(ch) or {})
        secret = bool(kc_get(_KC[ch])) if ch in _KC else True   # imessage has no secret
        # a channel is "configured" if its secret (if any) is present AND its required pref is set
        if ch == "telegram":
            configured = secret
        elif ch == "email":
            # hosted (via Nexplora / hello@nexplora.ai) needs only the recipient; BYOK-SMTP
            # needs the full host/user/to + the app-password in Keychain.
            configured = bool(c.get("to")) if c.get("hosted") else (secret and bool(c.get("host") and c.get("user") and c.get("to")))
        elif ch == "imessage":
            configured = bool(c.get("to"))
        elif ch == "whatsapp":
            configured = secret and bool(c.get("sid") and c.get("from") and c.get("to"))
        elif ch == "sms":
            # Twilio SMS BYOK: send FROM the operator's own Twilio number (e.g. 929) — needs the
            # auth token in Keychain + sid/from/to. This is the ONLY channel where the "from" is the
            # operator's, not the Mac's Apple ID (iMessage) or Nexplora's relay.
            configured = secret and bool(c.get("sid") and c.get("from") and c.get("to"))
        else:
            configured = False
        out[ch] = dict(c, configured=configured, active=bool(c.get("active")))
    return out


def set_active(channel, active):
    """Toggle a channel on/off for autonomy reports."""
    if channel not in CHANNELS:
        raise ValueError("unknown channel: " + str(channel))
    cfg = _load_config()
    mc = cfg.get("message_channels") or {}
    mc.setdefault(channel, {})["active"] = bool(active)
    _save_channels(mc)


def _set_prefs(channel, **prefs):
    cfg = _load_config()
    mc = cfg.get("message_channels") or {}
    entry = mc.setdefault(channel, {})
    entry.update({k: v for k, v in prefs.items() if v is not None})
    _save_channels(mc)


# ── configure (secrets → Keychain via the caller's getpass; prefs → config) ──────────────────────────────

def configure_telegram(token, chat_id=None):
    kc_set(_KC["telegram"], token)                    # token → Keychain
    _set_prefs("telegram", chat_id=chat_id, active=True)


def _smtp_host_for(address):
    """Derive the SMTP host from an email address so the operator never types it. Falls back
    to smtp.<domain> for anything not in the common map."""
    dom = (str(address or "").split("@")[-1] or "").strip().lower()
    common = {
        "gmail.com": "smtp.gmail.com", "googlemail.com": "smtp.gmail.com",
        "outlook.com": "smtp-mail.outlook.com", "hotmail.com": "smtp-mail.outlook.com",
        "live.com": "smtp-mail.outlook.com", "msn.com": "smtp-mail.outlook.com",
        "yahoo.com": "smtp.mail.yahoo.com", "icloud.com": "smtp.mail.me.com",
        "me.com": "smtp.mail.me.com", "mac.com": "smtp.mail.me.com", "aol.com": "smtp.aol.com",
    }
    return common.get(dom, ("smtp." + dom) if dom else "")


def _safe_port(port, default=587):
    try:
        return int(str(port).strip())
    except (TypeError, ValueError):
        return default


def configure_email(host, port, user, password, to):
    kc_set(_KC["email"], password)
    _set_prefs("email", host=host, port=_safe_port(port), user=user, to=to, active=True, hosted=False)


def configure_email_hosted(to):
    """Nexplora-hosted email: NX sends FROM hello@nexplora.ai TO the operator's address via the
    server relay. No SMTP creds on the client — the operator only gives where to receive."""
    _set_prefs("email", to=to, hosted=True, active=True)


def configure_imessage(to_handle, hosted=False):
    """`hosted=True`: NX texts the number FROM the Nexplora number via the server relay (SMS —
    reaches iMessage AND Android). `hosted=False`: local macOS iMessage via Messages.app."""
    _set_prefs("imessage", to=to_handle, hosted=bool(hosted), active=True)


def configure_whatsapp(sid, token, from_num, to_num):
    kc_set(_KC["whatsapp"], token)
    _set_prefs("whatsapp", sid=sid, **{"from": from_num, "to": to_num}, active=True)


def configure_sms(sid, token, from_num, to_num):
    """Twilio SMS BYOK — NX sends SMS FROM the operator's own Twilio number (`from_num`, e.g. 929) to
    `to_num`. `token` (the Twilio auth token) goes to the Keychain, never config/argv/chat; sid/from/to are
    non-secret prefs. Swap `from_num` to the verified number later with a single re-configure — nothing else
    changes."""
    kc_set(_KC["sms"], token)
    _set_prefs("sms", sid=sid, **{"from": from_num, "to": to_num}, active=True)


# ── senders (each raises on failure; send_report catches + records honestly) ─────────────────────────────

def _send_telegram(text, entry):
    import nx_loop
    cfg = _load_config()
    tok = os.environ.get("TELEGRAM_BOT_TOKEN") or kc_get(_KC["telegram"]) or cfg.get("telegram_bot_token")
    if not tok:
        raise RuntimeError("no telegram token")
    # let nx_loop resolve/send (chat_id from env → config pref → getUpdates)
    merged = dict(cfg, telegram_bot_token=tok, telegram_chat_id=entry.get("chat_id") or cfg.get("telegram_chat_id"))
    nx_loop.send_telegram_message(text, merged)


def _send_via_relay(channel, to, text, subject=None):
    """Nexplora-hosted send: POST the message to the server relay (/api/nexplora/notify), which
    sends it FROM Nexplora's identity (SMS from the Nexplora number · email from hello@nexplora.ai).
    The operator holds NO provider creds — just their own device-flow token (from config)."""
    import requests
    if not to:
        raise RuntimeError("no recipient handle")
    cfg = _load_config() or {}
    token = str(cfg.get("token") or cfg.get("nx_token") or "").strip()
    if not token:
        raise RuntimeError("sign in first (run nx) — Nexplora-hosted channels need your account")
    try:
        from nx_obfuscate import AUTH as _A
        base = os.environ.get("NX_AUTH_BASE") or _A["base"]
    except Exception:
        base = os.environ.get("NX_AUTH_BASE") or "https://api.nexplora.ai"
    body = {"channel": channel, "to": to, "text": text}
    if subject:
        body["subject"] = subject
    r = requests.post(base.rstrip("/") + "/api/nexplora/notify", json=body,
                      headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"},
                      timeout=20)
    if r.status_code >= 300:
        err = ""
        try:
            err = (r.json() or {}).get("error") or ""
        except Exception:
            err = (r.text or "")[:120]
        raise RuntimeError("relay %d: %s" % (r.status_code, err or "send failed"))


# ── reply-to-act: report a STAGED action for reply-approval ──────────────────────────────────────────────

# CLI report-back channel → server endpoint channel. Telegram = native reply; imessage/sms ride Twilio SMS (operator
# replies "approve NX-XXXX"); whatsapp = same ref model on WhatsApp; email = an authenticated deep-link (email reply-
# approval is disabled server-side because SMTP From can't be trusted — see docs/REPLY-TO-ACT.md).
_REPORT_CHANNEL_MAP = {"telegram": "telegram", "imessage": "sms", "sms": "sms", "whatsapp": "whatsapp", "email": "email"}


def _pick_reply_channel(cfg):
    """Choose the operator's first ACTIVE report-back channel that can carry a reply-approval, with its handle.
    Returns (cli_channel, handle) or (None, None)."""
    mc = (cfg or {}).get("message_channels") or {}
    for ch in ("telegram", "imessage", "sms", "whatsapp", "email"):
        entry = mc.get(ch) or {}
        if not entry.get("active"):
            continue
        handle = channel_handle(ch, entry)
        if handle:
            return ch, handle
    return None, None


def _post_reply_endpoint(path, base_body, channel, to):
    """Shared POST to a reply-to-act server endpoint (report-action / stage-action): resolves the account device token +
    AUTH base, maps the CLI channel → endpoint channel + recipient field, POSTs, and returns parsed JSON (raises on
    failure). Standardizes on cfg['token'] (the canonical device-flow token), never the retired nx_token."""
    import requests
    cfg = _load_config() or {}
    token = str(cfg.get("token") or cfg.get("nx_token") or "").strip()
    if not token:
        raise RuntimeError("sign in first (run nx) — reply-approval needs your account")
    if not channel:
        channel, to = _pick_reply_channel(cfg)
    ep = _REPORT_CHANNEL_MAP.get(channel or "")
    if not ep:
        raise RuntimeError("no active reply-approval channel — set one with /message (telegram, text/iMessage, whatsapp, or email)")
    try:
        from nx_obfuscate import AUTH as _A
        base = os.environ.get("NX_AUTH_BASE") or _A["base"]
    except Exception:
        base = os.environ.get("NX_AUTH_BASE") or "https://api.nexplora.ai"
    body = dict(base_body)
    body["channel"] = ep
    if ep == "telegram":
        body["telegram_chat_id"] = str(to or "")
    else:
        body["to"] = str(to or "")
    r = requests.post(base.rstrip("/") + path, json=body,
                      headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"},
                      timeout=20)
    if r.status_code >= 300:
        err = ""
        try:
            err = (r.json() or {}).get("error") or ""
        except Exception:
            err = (r.text or "")[:120]
        raise RuntimeError("%s %d: %s" % (path.rsplit("/", 1)[-1], r.status_code, err or "failed"))
    try:
        return r.json() or {}
    except Exception:
        return {"ok": True}


def report_action(request_id, channel=None, to=None, note=None):
    """Report an EXISTING staged GATE-1 action (by request_id) to the operator for reply-approval. The server mints the
    channel's single-use reply capability + sends the report from Nexplora's identity; the operator replies to approve.
    Returns the server JSON ({ok, channel, reply_enabled}); raises on failure. Requires a signed-in account."""
    if not request_id:
        raise RuntimeError("no staged request_id to report")
    base_body = {"request_id": str(request_id)}
    if note:
        base_body["note"] = str(note)
    return _post_reply_endpoint("/api/nexplora/report-action", base_body, channel, to)


def stage_and_report(pack_id, action_id, requested_action, workspace_id=None, run_id=None, channel=None, to=None, note=None):
    """STAGE a GATE-1 pack action on the server AND report it for reply-approval, in one call — the CLI→server hand-off.
    The server evaluates the action through GATE-1 (persisting the request) and, if it needs approval, mints the reply
    capability + sends the report. Returns {ok, request_id, gate_status, reported, reply_enabled}; the operator then
    approves by replying on their channel, which fires the action server-side. For GATE-1 PACK actions (pack_id/
    action_id/requested_action) — not generic local MCP tool calls."""
    if not (pack_id and action_id and requested_action):
        raise RuntimeError("pack_id, action_id, requested_action required")
    cfg = _load_config() or {}
    base_body = {
        "pack_id": str(pack_id),
        "action_id": str(action_id),
        "requested_action": str(requested_action),
        "workspace_id": str(workspace_id or cfg.get("workspace_id") or ""),
    }
    if run_id:
        base_body["run_id"] = str(run_id)
    if note:
        base_body["note"] = str(note)
    return _post_reply_endpoint("/api/nexplora/stage-action", base_body, channel, to)


# ── host-executed (local MCP) approvals — the autonomy-loop local-execute flow ───────────────────────────

def stage_mcp(server, tool, args=None, description=None, workspace_id=None, run_id=None, channel=None, to=None):
    """Stage a LOCAL (host-executed) MCP tool call for reply-approval. The server records it + reports "approve NXM-xxxx"
    to the operator's channel; the operator approves by replying; poll_mcp_approval() then returns 'approved' and the
    caller runs the tool locally. Needs a phone/Telegram/WhatsApp channel (email can't carry it). Returns the server
    JSON ({ok, approval_id, ref, reply_enabled}); raises on failure."""
    if not (server and tool):
        raise RuntimeError("server and tool required")
    cfg = _load_config() or {}
    base_body = {
        "server": str(server),
        "tool": str(tool),
        "args": args if isinstance(args, dict) else {},
        "description": str(description or (str(server) + " · " + str(tool))),
        "workspace_id": str(workspace_id or cfg.get("workspace_id") or ""),
    }
    if run_id:
        base_body["run_id"] = str(run_id)
    return _post_reply_endpoint("/api/nexplora/stage-mcp", base_body, channel, to)


def poll_mcp_approval(approval_id, timeout_s=900, interval_s=5):
    """Poll a staged host-approval until decided or timeout. Returns the final status dict ({status: approved|rejected|
    expired|pending, …}); stays 'pending' on timeout. Blocking — call from a foreground/supervised path."""
    import time as _t
    import requests
    if not approval_id:
        raise RuntimeError("no approval_id")
    cfg = _load_config() or {}
    token = str(cfg.get("token") or cfg.get("nx_token") or "").strip()
    if not token:
        raise RuntimeError("sign in first (run nx)")
    try:
        from nx_obfuscate import AUTH as _A
        base = os.environ.get("NX_AUTH_BASE") or _A["base"]
    except Exception:
        base = os.environ.get("NX_AUTH_BASE") or "https://api.nexplora.ai"
    url = base.rstrip("/") + "/api/nexplora/mcp-approval"
    deadline = _t.time() + max(0, timeout_s)
    last = {"status": "pending"}
    while _t.time() < deadline:
        try:
            r = requests.get(url, params={"id": str(approval_id)},
                             headers={"Authorization": "Bearer " + token}, timeout=15)
            if r.status_code < 300:
                last = r.json() or last
                if last.get("status") in ("approved", "rejected", "expired"):
                    return last
        except Exception:
            pass
        _t.sleep(max(1, interval_s))
    return last


def _host_result_summary(result):
    """(ok, one-line-summary) from whatever execute_fn returned — dict with success/output/response/result, or a scalar."""
    try:
        if isinstance(result, dict):
            ok = bool(result.get("success", not result.get("error")))
            body = result.get("output")
            if body is None:
                body = result.get("result", result.get("response", result.get("error", "")))
            if isinstance(body, (dict, list)):
                body = json.dumps(body)
            body = str(body).strip()
            return ok, (body[:280] if body else ("ok" if ok else "failed"))
        return True, (str(result).strip()[:280] if result is not None else "done")
    except Exception:
        return True, "done"


def _report_host_result(approval_id, server, tool, result):
    """Close the loop: after a host action runs locally, relay its RESULT back to the operator. PRIMARY path is the
    SERVER (POST /api/nexplora/mcp-approval) — it delivers over the SAME channel the approval was reported on (the
    server's own bot), so the "✅ Done: …" summary arrives automatically with NO operator-local channel config, exactly
    like the approval DM. Falls back to the operator's local /message channels only if the server can't deliver.
    Best-effort — never raises. Returns a small dict describing what happened."""
    ok, summary = _host_result_summary(result)
    server_res = {}
    try:
        if approval_id:
            import requests
            cfg = _load_config() or {}
            token = str(cfg.get("token") or cfg.get("nx_token") or "").strip()
            try:
                from nx_obfuscate import AUTH as _A
                base = os.environ.get("NX_AUTH_BASE") or _A["base"]
            except Exception:
                base = os.environ.get("NX_AUTH_BASE") or "https://api.nexplora.ai"
            if token:
                r = requests.post(base.rstrip("/") + "/api/nexplora/mcp-approval",
                                  json={"approval_id": str(approval_id), "ok": bool(ok), "summary": summary},
                                  headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"}, timeout=20)
                server_res = (r.json() if r.status_code < 300 else {"error": "http_%d" % r.status_code}) or {}
    except Exception as e:
        server_res = {"error": (str(e) or repr(e))[:120]}
    if server_res.get("delivered"):
        return {"via": "server", "delivered": True}
    # Fallback: the operator's LOCAL report-back channels (needs /message setup — the server path above is preferred).
    try:
        icon = "✅ Done" if ok else "⚠️ Failed"
        local = send_report("{}: {} · {}\n{}".format(icon, server, tool, summary))
        return {"via": "local", "delivered": any_delivered(local), "server": server_res, "local": local}
    except Exception as e:
        return {"via": "none", "delivered": False, "server": server_res, "error": (str(e) or repr(e))[:120]}


def run_with_host_approval(server, tool, args, description, execute_fn,
                           workspace_id=None, run_id=None, channel=None, to=None, timeout_s=900):
    """Supervised host action: stage it for reply-approval, wait for the operator's reply, and on 'approved' run
    execute_fn(server, tool, args) LOCALLY — then REPORT the result back to the operator. Returns
    {status, executed: bool, result?, reported?}. execute_fn is the CLI's own executor (e.g. the autonomy loop's
    guarded runner) — the tool runs on THIS machine, never server-side. The operator sees the report DM say
    "…running it", then this closes the loop with "✅ Done: <result>" once it actually ran."""
    staged = stage_mcp(server, tool, args, description, workspace_id=workspace_id, run_id=run_id, channel=channel, to=to)
    approval_id = (staged or {}).get("approval_id")
    if not approval_id:
        return {"status": "stage_failed", "executed": False, "detail": (staged or {}).get("error")}
    decided = poll_mcp_approval(approval_id, timeout_s=timeout_s)
    if (decided or {}).get("status") != "approved":
        return {"status": (decided or {}).get("status", "pending"), "executed": False}
    result = execute_fn(server, tool, args)
    # Close the loop — relay the ACTUAL result to the operator via the SERVER (same channel as the approval, automatic).
    reported = _report_host_result(approval_id, server, tool, result)
    return {"status": "approved", "executed": True, "result": result, "reported": reported}


# ── host-agent — run operator-approved actions initiated from ANOTHER surface (Telegram/web) ─────────────
# run_with_host_approval() above is CLI-INITIATED (the CLI stages, then polls its own id). When the operator
# approves from Telegram/web, the CLOUD is the initiator and the CLI has no id to poll — so the host-agent
# DISCOVERS approved actions via an atomic server-side claim, runs each locally through the SAME proven
# connectors /publish uses, and reports the result back. This is "NX runs it on your machine" made real.

def _auth_base():
    """Resolve the Nexplora API base (env override → obfuscated default)."""
    try:
        from nx_obfuscate import AUTH as _A
        return os.environ.get("NX_AUTH_BASE") or _A["base"]
    except Exception:
        return os.environ.get("NX_AUTH_BASE") or "https://api.nexplora.ai"


def _refresh_device_token():
    """Keep the (short-lived) device token fresh for a long-running loop. Returns the current bearer token
    post-refresh, or '' if not signed in. Best-effort — never raises (lazy nx_cli import avoids a cycle)."""
    cfg = _load_config() or {}
    try:
        import nx_cli
        cfg = nx_cli.refresh_token_if_needed(cfg) or cfg
    except Exception:
        pass
    return str((cfg or {}).get("token") or (cfg or {}).get("nx_token") or "").strip()


def claim_next_host_action(token=None):
    """Atomically claim the next APPROVED host action for this operator (POST /api/nexplora/mcp-approvals/
    claim, bearer), or None if the queue is empty. The claim is race-free + run-once (M716 FOR UPDATE SKIP
    LOCKED). Returns {approval_id, server, tool, args, description, run_id} or None. Best-effort — returns
    None on any transport/auth error so the loop simply polls again."""
    import requests
    if token is None:
        cfg = _load_config() or {}
        token = str(cfg.get("token") or cfg.get("nx_token") or "").strip()
    if not token:
        return None
    try:
        r = requests.post(_auth_base().rstrip("/") + "/api/nexplora/mcp-approvals/claim",
                          json={}, headers={"Authorization": "Bearer " + token,
                                            "Content-Type": "application/json"}, timeout=20)
        if r.status_code >= 300:
            return None
        return ((r.json() or {}).get("action")) or None
    except Exception:
        return None


def execute_host_action(server, tool, args):
    """Route a claimed host action to the right LOCAL executor and return its honest result dict:
      - CHANNEL action (tool is a known connector action method, e.g. 'publish_text') → the proven
        /publish connector via nx_channels.channel_execute_fn (the exact path /publish uses),
      - else an MCP tool → nx_mcp.execute_mcp_tool.
    Never raises — any failure returns {ok: False, detail: …}, never a faked success."""
    args = args if isinstance(args, dict) else {}
    try:
        import nx_channels
        # Route by (slug, tool) — is_channel_action sees BOTH native methods (publish_text) and registry actions
        # (slack/github/…), and disambiguates from an MCP tool that shares a name.
        if nx_channels.is_channel_action(server, tool):
            return nx_channels.channel_execute_fn(server, tool, args)
    except Exception as e:
        return {"ok": False, "detail": "channel_executor_error:%s" % type(e).__name__}
    # MCP tool → the PROVEN connected-session dispatcher (nx_mcp_tools.call), the same path /connected + the REPL
    # use for the OAuth-connected servers (tavily/github/notion/…). NOT nx_mcp.execute_mcp_tool, which checks the
    # separate "/install"-ed local-MCP registry and wrongly reports connected OAuth servers as "not installed".
    try:
        import nx_mcp_tools
        r = nx_mcp_tools.call(server, tool, args) or {}
        ok = bool(r.get("ok"))
        return {"ok": ok, "success": ok,
                "output": r.get("text") if ok else None,
                "detail": None if ok else (r.get("error") or "failed")}
    except Exception as e:
        return {"ok": False, "detail": "no_executor:%s" % type(e).__name__}


def run_host_agent(poll_s=5, once=False, max_seconds=None, on_event=None):
    """THE HOST-AGENT loop: continuously claim operator-approved host actions and RUN them LOCALLY on this
    machine, reporting each result back over the channel it was approved on. The operator approves from
    Telegram/web; THIS loop (CLI + proven /publish connectors) is the executor — no cloud re-impl. Blocking;
    Ctrl-C to stop. Returns a summary dict on exit.

    poll_s: seconds between empty polls. once: claim+run at most one action, then return. max_seconds: stop
    after N seconds (None = until interrupted). on_event(event, data): optional UI hook ('claimed'|'ran'|'idle')."""
    import time as _t
    ran = 0
    started = _t.time()
    last_sync = 0.0  # epoch of the last connection-snapshot push (0 = never)

    def _emit(ev, data=None):
        try:
            if on_event:
                on_event(ev, data or {})
        except Exception:
            pass

    while True:
        token = _refresh_device_token()
        # Keep the server's view of "what's connected here" fresh so Telegram/web show the same set (best-effort,
        # metadata-only). Push at startup then every ~60s.
        if token and (_t.time() - last_sync) > 60:
            try:
                # ONE canonical push (connections + creations + /supply bindings) so a duty loop that runs
                # for hours keeps the web's view of this machine complete, not just partly fresh.
                push_all_snapshots()
            except Exception:
                pass
            last_sync = _t.time()
        action = claim_next_host_action(token=token) if token else None
        if action:
            approval_id = action.get("approval_id")
            server = action.get("server")
            tool = action.get("tool")
            args = action.get("args") or {}
            _emit("claimed", {"server": server, "tool": tool, "approval_id": approval_id})
            result = execute_host_action(server, tool, args)
            reported = _report_host_result(approval_id, server, tool, result)
            ran += 1
            ok, summary = _host_result_summary(result)
            _emit("ran", {"server": server, "tool": tool, "ok": ok, "summary": summary, "reported": reported})
            if once:
                return {"ran": ran, "last": {"server": server, "tool": tool, "ok": ok}}
            continue  # drain: immediately try the next queued action before sleeping
        _emit("idle")
        if once:
            return {"ran": ran, "idle": True}
        if max_seconds is not None and (_t.time() - started) >= max_seconds:
            return {"ran": ran, "stopped": "max_seconds"}
        try:
            _t.sleep(max(1, poll_s))
        except KeyboardInterrupt:
            return {"ran": ran, "stopped": "interrupt"}


# ── unified connections — report the CLI's LOCAL connected set so Telegram + web see the same account ─────────
# NX is one account across CLI/Telegram/web. The CLI connects things locally (Keychain) that the cloud can't see.
# collect_local_connections() builds a METADATA-ONLY snapshot (names/status/scopes — NEVER a credential) and
# push_connections_snapshot() POSTs it to /api/nexplora/cli-connections, so GET /api/nexplora/connected shows the
# same set everywhere. Credentials stay in the local Keychain, exactly as the isolation rule requires.

def _registry_action_slugs():
    try:
        from nx_channel_actions import ACTION_SPECS
        return list(ACTION_SPECS.keys())
    except Exception:
        return []


def collect_local_connections():
    """A metadata-only snapshot of everything connected locally: channel connectors (+ whether they can execute),
    connected generic-OAuth connectors that have a wired action, MCP servers, and messaging channels. Returns a
    list of {slug, kind, display_name, configured, connected, can_publish, scopes, expires_at}. NO credentials."""
    out = []
    seen = set()

    def _add(slug, kind, display_name, configured, connected, can_publish, scopes=None, expires_at=None):
        s = (slug or "").strip().lower()
        if not s or s in seen:
            return
        seen.add(s)
        out.append({"slug": s, "kind": kind, "display_name": display_name or s,
                    "configured": bool(configured), "connected": bool(connected), "can_publish": bool(can_publish),
                    "scopes": list(scopes or []), "expires_at": expires_at})

    # (1) hand-built channel connectors + whether they can execute (native publish_text OR a registry action)
    try:
        import nx_channels as C
        try:
            from nx_channel_actions import action_names as _anames
        except Exception:
            _anames = lambda s: ()
        for slug, cls in getattr(C, "REGISTRY", {}).items():
            try:
                inst = cls()
                st = inst.status() if hasattr(inst, "status") else {}
                can = callable(getattr(inst, "publish_text", None)) or bool(_anames(slug))
                _add(slug, "channel", st.get("display_name") or getattr(inst, "display_name", slug),
                     st.get("configured"), st.get("connected"), can, st.get("scopes"), st.get("expires_at"))
            except Exception:
                continue
        # (1b) connected generic-OAuth connectors that have a wired action (only if actually connected — don't
        # dump the whole 69-entry catalog; report what the operator has really linked)
        for slug in _registry_action_slugs():
            if slug in seen:
                continue
            try:
                conn = C.connector_for_service(slug)
                if conn is None or not (hasattr(conn, "is_connected") and conn.is_connected()):
                    continue
                t = conn._load_token() if hasattr(conn, "_load_token") else {}
                _add(slug, "channel", getattr(conn, "display_name", slug), True, True, True,
                     (t or {}).get("scopes"), (t or {}).get("expires_at"))
            except Exception:
                continue
    except Exception:
        pass

    # (2) MCP servers connected in the Keychain
    try:
        import nx_mcp_oauth as _M
        for slug in (_M.connected_slugs() or []):
            _add(slug, "mcp", slug, True, True, True)
    except Exception:
        pass

    # (3) messaging / report-back channels
    try:
        st = channels_state() or {}
        for name, s in st.items():
            _add(name, "messaging", str(name).title(), s.get("configured"), s.get("active"), s.get("active"))
    except Exception:
        pass

    return out


def push_connections_snapshot(workspace_id=None):
    """POST the local connection snapshot to the server so Telegram/web show the same connected set. Metadata
    only (no credentials). Best-effort — returns the server JSON or {ok: False, error}; never raises."""
    try:
        import requests
        cfg = _load_config() or {}
        token = str(cfg.get("token") or cfg.get("nx_token") or "").strip()
        if not token:
            return {"ok": False, "error": "not_signed_in"}
        body = {"connections": collect_local_connections()}
        ws = workspace_id or cfg.get("workspace_id")
        if ws:
            body["workspace_id"] = str(ws)
        r = requests.post(_auth_base().rstrip("/") + "/api/nexplora/cli-connections", json=body,
                          headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"}, timeout=20)
        return (r.json() if r.status_code < 300 else {"ok": False, "error": "http_%d" % r.status_code}) or {"ok": False}
    except Exception as e:
        return {"ok": False, "error": (str(e) or repr(e))[:120]}


def collect_local_agent_channels():
    """A METADATA-ONLY snapshot of ~/.nx/agent-channels/ — which agent can send as what.

    /supply binds an agent to a channel (email · telegram · sms · whatsapp · imessage) and stores the
    binding locally; the SECRET goes to the Keychain, never into the JSON. Until now nothing pushed these
    bindings anywhere, so an operator who supplied an agent in the CLI saw nothing on the web — two
    surfaces, two different ideas of the same crew. This is the collector for the sync that fixes that.

    Emits [{agentKey, display, channel, handle, verifiedAt}]. `verifiedAt` is the CLI's own `verified`
    date, which is written ONLY after a real test send succeeded — so the server can promote the row to
    'active' on evidence rather than on a claim. No password, token, host, or port is included: the web
    never needs them, and the send path stays here.
    """
    out = []
    try:
        from pathlib import Path as _P
        import json as _j
        d = _P.home() / ".nx" / "agent-channels"
        if not d.is_dir():
            return out
        for f in sorted(d.glob("*.json")):
            try:
                b = _j.load(open(f))
            except Exception:
                continue
            key = str(b.get("name") or "").strip()
            if not key:
                continue
            display = str(b.get("display") or key).strip()
            for kind, ch in (b.get("channels") or {}).items():
                if not isinstance(ch, dict):
                    continue
                handle = str(ch.get("handle") or "").strip()
                if not handle:
                    continue
                out.append({
                    "agentKey": key,
                    "display": display,
                    "channel": str(kind),
                    "handle": handle,
                    "verifiedAt": str(ch.get("verified") or "") or None,
                })
    except Exception:
        return out
    return out


def push_agent_channels_snapshot(workspace_id=None):
    """POST the local /supply bindings to the server so the web shows the SAME crew this CLI supplied.

    Metadata only (handles + verified dates; never a password or bot token). Best-effort — returns the
    server JSON or {ok: False, error}; never raises, because a sync failure must never break /supply
    itself. Mirrors push_connections_snapshot -> /api/nexplora/cli-connections.
    """
    try:
        import requests
        cfg = _load_config() or {}
        token = str(cfg.get("token") or cfg.get("nx_token") or "").strip()
        if not token:
            return {"ok": False, "error": "not_signed_in"}
        chans = collect_local_agent_channels()
        if not chans:
            # An empty local set is NOT sent as a full snapshot. collect_local_agent_channels reads the
            # whole ~/.nx/agent-channels/ directory, so "" could mean "operator revoked everything" OR "the
            # directory momentarily couldn't be read" — and the server would revoke the operator's entire
            # crew on the latter. Refusing to send empty is the safe read; the last-binding-revoked edge
            # self-heals the next time any binding exists to anchor a non-empty full snapshot.
            return {"ok": True, "synced": 0}
        # full=True: this IS the complete local set (the collector read the entire directory), which
        # authorizes the server to revoke any CLI-supplied binding no longer present — the receive half of
        # /supply revoke. The server's origin filter guarantees a web-created binding is never touched.
        body = {"channels": chans, "full": True}
        ws = workspace_id or cfg.get("workspace_id")
        if ws:
            body["workspace_id"] = str(ws)
        r = requests.post(_auth_base().rstrip("/") + "/api/nexplora/agent-channels", json=body,
                          headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"}, timeout=20)
        return (r.json() if r.status_code < 300 else {"ok": False, "error": "http_%d" % r.status_code}) or {"ok": False}
    except Exception as e:
        return {"ok": False, "error": (str(e) or repr(e))[:120]}


def fetch_web_duty(workspace_id=None):
    """Which (agentKey, channel) pairs has the operator marked ON DUTY on the web?

    /takeoff on the web sets a binding's dispatched_at; this reads that set back so the CLI's duty loop can
    honor the operator's web selection. Returns a set of (agentKey, channel) tuples, or None on ANY failure
    (not signed in, offline, store not migrated) — the caller treats None as "no web curation, dispatch as
    before", so a transient read never silently narrows who goes on duty. An EMPTY set means the web is
    reachable and the operator has curated nothing on duty there.
    """
    try:
        import requests
        cfg = _load_config() or {}
        token = str(cfg.get("token") or cfg.get("nx_token") or "").strip()
        if not token:
            return None
        url = _auth_base().rstrip("/") + "/api/nexplora/agent-channels"
        ws = workspace_id or cfg.get("workspace_id")
        if ws:
            url += "?workspace_id=" + str(ws)
        r = requests.get(url, headers={"Authorization": "Bearer " + token}, timeout=20)
        if r.status_code >= 300:
            return None
        chans = (r.json() or {}).get("channels") or []
        return {(str(c.get("agentId")), str(c.get("channel")))
                for c in chans if c.get("dispatchedAt") and c.get("status") == "active"}
    except Exception:
        return None


def report_duty(reports, workspace_id=None):
    """Tell the server the CLI is ACTUALLY on duty and how many messages it has sent, so the web Activity
    mirrors reality instead of an optimistic flag.

    `reports` = [{agentId, channel, sent}] where `sent` is a non-negative DELTA of messages sent since the
    last report. The server increments messages_sent by the delta and stamps dispatched_at. Best-effort —
    returns the server JSON or {ok: False, error}; never raises, because a reporting failure must never
    interrupt the duty loop that is answering real people.
    """
    try:
        import requests
        cfg = _load_config() or {}
        token = str(cfg.get("token") or cfg.get("nx_token") or "").strip()
        if not token:
            return {"ok": False, "error": "not_signed_in"}
        body = {"action": "duty-report", "reports": list(reports or [])}
        ws = workspace_id or cfg.get("workspace_id")
        if ws:
            body["workspace_id"] = str(ws)
        r = requests.patch(_auth_base().rstrip("/") + "/api/nexplora/agent-channels", json=body,
                           headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"}, timeout=20)
        return (r.json() if r.status_code < 300 else {"ok": False, "error": "http_%d" % r.status_code}) or {"ok": False}
    except Exception as e:
        return {"ok": False, "error": (str(e) or repr(e))[:120]}


def collect_local_creations():
    """A metadata-only snapshot of everything the operator has GENERATED locally — skills, generated integrations,
    tools — each with its HONEST proven/pending status, so web + Telegram show the same 'what you've created' set as
    `nx created`. NO code bodies, NO credentials — just {kind, slug, name, status, detail}. (Agents already live
    server-side in the roster, so they need no sync.) Every source is try/except-swallowed → returns partial, never
    fails."""
    import nx_creator as CR
    out, seen = [], set()

    def _add(kind, slug, name, status, detail=""):
        s = (str(slug or "")).strip().lower()
        key = kind + ":" + s
        if not s or key in seen:
            return
        seen.add(key)
        out.append({"kind": kind, "slug": s, "name": name or s,
                    "status": "proven" if status == "proven" else "pending", "detail": (detail or "")[:200]})

    try:
        for sk in CR.list_user_skills():
            _add("skill", str(sk.get("cmd") or "").lstrip("$"), sk.get("cmd"), sk.get("status"), sk.get("desc"))
    except Exception:
        pass
    try:
        for ig in CR.list_user_integrations():
            _add("integration", ig.get("name"), ig.get("name"), ig.get("status"),
                 "%s/%s tools proven" % (ig.get("ready_count", 0), ig.get("discovered", 0)))
    except Exception:
        pass
    try:
        for tl in CR.list_user_tools():
            _add("tool", tl.get("name"), tl.get("name"), tl.get("status"), tl.get("kind"))
    except Exception:
        pass
    return out


def push_creations_snapshot(workspace_id=None):
    """POST the local CREATIONS snapshot so web + Telegram show the same 'what you've created' set with honest
    proven/pending. Metadata only (no code, no credentials). Best-effort — returns the server JSON or
    {ok: False, error}; never raises. Mirrors push_connections_snapshot exactly."""
    try:
        import requests
        cfg = _load_config() or {}
        token = str(cfg.get("token") or cfg.get("nx_token") or "").strip()
        if not token:
            return {"ok": False, "error": "not_signed_in"}
        body = {"creations": collect_local_creations()}
        ws = workspace_id or cfg.get("workspace_id")
        if ws:
            body["workspace_id"] = str(ws)
        r = requests.post(_auth_base().rstrip("/") + "/api/nexplora/cli-creations", json=body,
                          headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"}, timeout=20)
        return (r.json() if r.status_code < 300 else {"ok": False, "error": "http_%d" % r.status_code}) or {"ok": False}
    except Exception as e:
        return {"ok": False, "error": (str(e) or repr(e))[:120]}


def push_all_snapshots(workspace_id=None):
    """Push EVERY outbound metadata snapshot in one call: connections + creations + /supply bindings.

    ONE canonical outbound push, because there are four places that auto-sync (CLI launch, the host-agent
    loop, /connected, and `nx sync-*`) and each used to hand-list which snapshots it sent. That is a
    disagreement attractor: `agent-channels` shipped and got added to none of them, so an operator who
    supplied an agent in the CLI saw nothing on the web until they re-ran /supply by hand. A new snapshot
    kind added here reaches every auto-sync site at once, instead of three of the four.

    Best-effort per snapshot — one failure never blocks the others, and nothing raises. Returns
    {kind: result} so a caller that wants to report (`nx sync-supply`) can, while the background callers
    ignore it. No credential is in any of these payloads.
    """
    out = {}
    for _kind, _fn in (("connections", push_connections_snapshot),
                       ("creations", push_creations_snapshot),
                       ("agent_channels", push_agent_channels_snapshot)):
        try:
            out[_kind] = _fn(workspace_id=workspace_id)
        except Exception as e:
            out[_kind] = {"ok": False, "error": (str(e) or repr(e))[:120]}
    return out


def pull_creations():
    """GET the operator's creations snapshot (the PULL half — server → CLI) so anything created on ANOTHER
    surface (web / Telegram) becomes visible here. Writes ~/.nx/synced-creations.json for the /created view.
    Metadata only (no bodies). Best-effort — returns the list or []; never raises. Mirror of push_creations_snapshot."""
    try:
        import requests
        cfg = _load_config() or {}
        token = str(cfg.get("token") or cfg.get("nx_token") or "").strip()
        if not token:
            return []
        r = requests.get(_auth_base().rstrip("/") + "/api/nexplora/cli-creations",
                         headers={"Authorization": "Bearer " + token, "Accept": "application/json"}, timeout=20)
        if r.status_code >= 300:
            return []
        data = r.json() if r.content else {}
        creations = data.get("creations") if isinstance(data, dict) else None
        creations = creations if isinstance(creations, list) else []
        try:
            import json as _json
            p = os.path.join(os.path.expanduser("~"), ".nx", "synced-creations.json")
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                _json.dump({"creations": creations}, f)
        except Exception:
            pass
        return creations
    except Exception:
        return []


def push_skill_bodies():
    """BODY sync (CLI -> web): push the operator's CLI-authored skill BODIES to nexplora_user_skills via
    /api/nexplora/cli-skills so a skill created in the CLI becomes RUNNABLE on web. Reads ~/.nx/skills/*.json
    ({cmd, desc, system_prompt, needs}). Best-effort — returns the server JSON or {ok:False}; never raises."""
    try:
        import glob
        import json as _json
        cfg = _load_config() or {}
        token = str(cfg.get("token") or cfg.get("nx_token") or "").strip()
        if not token:
            return {"ok": False, "error": "not_signed_in"}
        skills_dir = os.path.join(os.path.expanduser("~"), ".nx", "skills")
        skills = []
        for p in glob.glob(os.path.join(skills_dir, "*.json")):
            try:
                d = _json.load(open(p, encoding="utf-8"))
            except Exception:
                continue
            cmd = str(d.get("cmd") or "").lstrip("$").strip()
            sp = str(d.get("system_prompt") or "").strip()
            if not cmd or not sp:
                continue
            skills.append({"slug": cmd, "name": cmd, "description": d.get("desc") or "",
                           "instructions": sp, "needs": d.get("needs") or ""})
        if not skills:
            return {"ok": True, "synced": 0}
        import requests
        r = requests.post(_auth_base().rstrip("/") + "/api/nexplora/cli-skills", json={"skills": skills},
                          headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"}, timeout=20)
        return (r.json() if r.status_code < 300 else {"ok": False, "error": "http_%d" % r.status_code}) or {"ok": False}
    except Exception as e:
        return {"ok": False, "error": (str(e) or repr(e))[:120]}


def pull_skill_bodies():
    """BODY sync (web -> CLI): pull authored skill BODIES from nexplora_user_skills so a skill created on web
    (or another CLI) RUNS here. Writes ~/.nx/skills/<slug>.json for any skill NOT already present locally
    (never clobbers a local edit). Best-effort — returns the count written; never raises."""
    try:
        import json as _json
        cfg = _load_config() or {}
        token = str(cfg.get("token") or cfg.get("nx_token") or "").strip()
        if not token:
            return 0
        import requests
        r = requests.get(_auth_base().rstrip("/") + "/api/nexplora/cli-skills",
                         headers={"Authorization": "Bearer " + token, "Accept": "application/json"}, timeout=20)
        if r.status_code >= 300:
            return 0
        data = r.json() if r.content else {}
        skills = data.get("skills") if isinstance(data, dict) else None
        if not isinstance(skills, list):
            return 0
        skills_dir = os.path.join(os.path.expanduser("~"), ".nx", "skills")
        os.makedirs(skills_dir, exist_ok=True)
        wrote = 0
        for s in skills:
            if not isinstance(s, dict):
                continue
            slug = str(s.get("slug") or "").strip()
            instr = str(s.get("instructions") or "").strip()
            if not slug or not instr:
                continue
            path = os.path.join(skills_dir, slug + ".json")
            if os.path.exists(path):
                continue  # a local version is authoritative — never clobber an operator's own edit
            try:
                with open(path, "w", encoding="utf-8") as f:
                    _json.dump({"cmd": "$" + slug, "desc": str(s.get("description") or "")[:80],
                                "system_prompt": instr, "needs": s.get("needs") or "",
                                "synced_from": "web"}, f, indent=2, ensure_ascii=False)
                wrote += 1
            except Exception:
                pass
        return wrote
    except Exception:
        return 0


# BODY sync for AGENTS + TOOLS (companion to the skill body path). Local stores:
#   agents -> ~/.nx/agents/*.json         (author form: {name, desc, lane, prompt, ...})
#   tools  -> ~/.nx/generated_tools/*.json (generated tool definition)
# The body IS the file (an authored definition, never a credential). `proof` (run evidence) is stripped.
_AUTHORED_BODY_DIRS = (("agent", "agents"), ("tool", "generated_tools"))


def _body_slug(name):
    import re
    return re.sub(r"[^a-z0-9_]", "_", str(name or "").lower()).strip("_")


def push_authored_bodies():
    """BODY sync (CLI -> web): push authored AGENT + TOOL bodies to nx_cli_creations.body via
    /api/nexplora/cli-authored-bodies so an agent/tool authored in the CLI is carried to web (and other CLIs).
    Best-effort — returns the server JSON or {ok:False}; never raises. Needs the M732 body column server-side."""
    try:
        import glob
        import json as _json
        cfg = _load_config() or {}
        token = str(cfg.get("token") or cfg.get("nx_token") or "").strip()
        if not token:
            return {"ok": False, "error": "not_signed_in"}
        base_dir = os.path.join(os.path.expanduser("~"), ".nx")
        items = []
        for kind, sub in _AUTHORED_BODY_DIRS:
            for p in glob.glob(os.path.join(base_dir, sub, "*.json")):
                try:
                    d = _json.load(open(p, encoding="utf-8"))
                except Exception:
                    continue
                name = str(d.get("name") or "").strip()
                if not name or not isinstance(d, dict):
                    continue
                body = {k: v for k, v in d.items() if k != "proof"}  # strip run-evidence; keep the authored definition
                items.append({"kind": kind, "slug": _body_slug(name), "name": name[:120], "body": body})
        if not items:
            return {"ok": True, "synced": 0}
        import requests
        r = requests.post(_auth_base().rstrip("/") + "/api/nexplora/cli-authored-bodies", json={"items": items},
                          headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"}, timeout=20)
        return (r.json() if r.status_code < 300 else {"ok": False, "error": "http_%d" % r.status_code}) or {"ok": False}
    except Exception as e:
        return {"ok": False, "error": (str(e) or repr(e))[:120]}


def pull_authored_bodies():
    """BODY sync (web -> CLI): pull authored AGENT + TOOL bodies and write them into ~/.nx/agents and
    ~/.nx/generated_tools so an agent/tool authored on web (or another CLI) is usable here. Writes only files
    NOT already present locally (never clobbers a local edit). Best-effort — returns the count written."""
    try:
        import json as _json
        cfg = _load_config() or {}
        token = str(cfg.get("token") or cfg.get("nx_token") or "").strip()
        if not token:
            return 0
        import requests
        r = requests.get(_auth_base().rstrip("/") + "/api/nexplora/cli-authored-bodies",
                         headers={"Authorization": "Bearer " + token, "Accept": "application/json"}, timeout=20)
        if r.status_code >= 300:
            return 0
        data = r.json() if r.content else {}
        items = data.get("items") if isinstance(data, dict) else None
        if not isinstance(items, list):
            return 0
        dir_for = {kind: sub for kind, sub in _AUTHORED_BODY_DIRS}
        base_dir = os.path.join(os.path.expanduser("~"), ".nx")
        wrote = 0
        for it in items:
            if not isinstance(it, dict):
                continue
            kind = str(it.get("kind") or "")
            slug = str(it.get("slug") or "").strip()
            body = it.get("body")
            sub = dir_for.get(kind)
            if not sub or not slug or not isinstance(body, dict):
                continue
            d = os.path.join(base_dir, sub)
            os.makedirs(d, exist_ok=True)
            path = os.path.join(d, slug + ".json")
            if os.path.exists(path):
                continue  # a local version is authoritative — never clobber
            body.setdefault("name", it.get("name") or slug)
            body["synced_from"] = "web"
            try:
                with open(path, "w", encoding="utf-8") as f:
                    _json.dump(body, f, indent=2, ensure_ascii=False)
                wrote += 1
            except Exception:
                pass
        return wrote
    except Exception:
        return 0


def _send_email(text, entry):
    if entry.get("hosted"):
        return _send_via_relay("email", entry.get("to"), text, subject="NX report")
    import smtplib
    from email.mime.text import MIMEText
    passwd = kc_get(_KC["email"])
    if not (passwd and entry.get("host") and entry.get("user") and entry.get("to")):
        raise RuntimeError("email not configured")
    msg = MIMEText(text)
    msg["Subject"] = "NX autonomy report"
    msg["From"] = entry["user"]
    msg["To"] = entry["to"]
    with smtplib.SMTP(entry["host"], int(entry.get("port", 587)), timeout=20) as s:
        s.starttls()
        s.login(entry["user"], passwd)
        s.sendmail(entry["user"], [entry["to"]], msg.as_string())


def _send_imessage(text, entry):
    to = entry.get("to")
    if entry.get("hosted"):
        return _send_via_relay("sms", to, text)   # Nexplora texts them (iMessage + Android) — cross-platform
    if not to:
        raise RuntimeError("no imessage handle")
    import sys
    if sys.platform != "darwin":
        # Local iMessage drives macOS Messages.app via osascript — impossible off-darwin.
        # Honest message (send_report records this per-channel) instead of a raw "[Errno 2] osascript".
        raise RuntimeError("iMessage is macOS-only — this device can't drive Messages. Use Email, Telegram, or SMS.")
    # macOS only — drive Messages.app via AppleScript. Pass the message + handle as run
    # ARGUMENTS (not embedded in the script text) so newlines / emoji / quotes can never
    # break the AppleScript parse — the old json.dumps-into-the-script approach did (it hit
    # "syntax error: Expected \" but found unknown token" on a multi-line emoji report).
    # Messages' AppleScript surface shifts across macOS releases: `participant <handle>` throws
    # "Can't make participant into type integer (-1700)" on recent versions, where `buddy <handle>` is the
    # form that resolves. Try the buddy forms first, then participant, then service-vs-account — so a single
    # send works across Ventura/Sonoma/Sequoia instead of hard-coding one incantation that breaks on the next.
    script = (
        'on run {msg, h}\n'
        '  tell application "Messages"\n'
        '    try\n'
        '      send msg to buddy h of (1st account whose service type = iMessage)\n'
        '    on error\n'
        '      try\n'
        '        send msg to buddy h of (1st service whose service type = iMessage)\n'
        '      on error\n'
        '        send msg to participant h of (1st account whose service type = iMessage)\n'
        '      end try\n'
        '    end try\n'
        '  end tell\n'
        'end run'
    )
    r = subprocess.run(["osascript", "-e", script, text, str(to)],
                       capture_output=True, text=True, timeout=20)
    if r.returncode != 0:
        raise RuntimeError("imessage: " + (r.stderr or "osascript failed")[:160])


def _send_whatsapp(text, entry):
    import requests
    tok = kc_get(_KC["whatsapp"])
    sid, frm, to = entry.get("sid"), entry.get("from"), entry.get("to")
    if not (tok and sid and frm and to):
        raise RuntimeError("whatsapp not configured")
    r = requests.post(
        "https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json".format(sid),
        data={"From": "whatsapp:" + frm, "To": "whatsapp:" + to, "Body": text[:1500]},
        auth=(sid, tok), timeout=20,
    )
    if r.status_code >= 300:
        raise RuntimeError("whatsapp {}: {}".format(r.status_code, (r.text or "")[:120]))


def _send_sms(text, entry):
    """Twilio SMS: send FROM the operator's Twilio number (entry['from']) to entry['to']. Plain SMS = the same
    Twilio Messages API as WhatsApp, without the 'whatsapp:' prefix. NOTE: `from` MUST be a number owned by the
    Twilio account — Twilio rejects a carrier line (e.g. a Boost number) it didn't provision."""
    import requests
    tok = kc_get(_KC["sms"])
    sid, frm, to = entry.get("sid"), entry.get("from"), entry.get("to")
    if not (tok and sid and frm and to):
        raise RuntimeError("sms not configured (need Twilio sid + auth token + from + to)")
    r = requests.post(
        "https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json".format(sid),
        data={"From": frm, "To": to, "Body": text[:1500]},
        auth=(sid, tok), timeout=20,
    )
    if r.status_code >= 300:
        raise RuntimeError("sms {}: {}".format(r.status_code, (r.text or "")[:160]))


_SENDERS = {
    "telegram": _send_telegram, "email": _send_email,
    "imessage": _send_imessage, "whatsapp": _send_whatsapp, "sms": _send_sms,
}


def send_report(text, cfg=None):
    """Fan out `text` to every ACTIVE + configured channel. Returns {channel: {"sent": bool, "error": str|None}}.
    Honest: a channel that isn't active/configured is simply absent; a sender that raises is recorded, not hidden."""
    state = channels_state(cfg)
    results = {}
    for ch in CHANNELS:
        entry = state[ch]
        if not (entry["active"] and entry["configured"]):
            continue
        try:
            _SENDERS[ch](text, entry)
            results[ch] = {"sent": True, "error": None}
        except Exception as e:
            results[ch] = {"sent": False, "error": (str(e) or repr(e))[:160]}
    return results


def any_delivered(results):
    return any(v.get("sent") for v in (results or {}).values())


# ── the /message command surface ─────────────────────────────────────────────────────────────────────────

def render_state(cfg=None):
    st = channels_state(cfg)
    lines = ["Report-back channels (where autonomy runs report):"]
    for ch in CHANNELS:
        e = st[ch]
        mark = "●" if (e["active"] and e["configured"]) else ("○" if e["configured"] else "·")
        status = "active" if (e["active"] and e["configured"]) else ("configured" if e["configured"] else "not set")
        extra = ""
        if ch == "telegram" and e.get("chat_id"):
            extra = " (chat %s)" % e["chat_id"]
        elif ch == "imessage" and e.get("to"):
            extra = " (%s)" % e["to"]
        elif ch == "email" and e.get("to"):
            extra = " (%s)" % e["to"]
        lines.append("  %s %-9s %s%s" % (mark, ch, status, extra))
    lines.append("Set up: /message telegram · /message imessage <handle> · /message email · /message whatsapp")
    lines.append("Toggle: /message on <channel> · /message off <channel>")
    return "\n".join(lines)


def handle_message_command(argv, cfg=None, prompt_secret=None, prompt=None):
    """`/message [telegram|imessage <handle>|email|whatsapp|on <ch>|off <ch>]`. prompt_secret(label)->hidden str;
    prompt(label)->str for non-secret fields. Returns a string to print."""
    argv = list(argv or [])
    if not argv:
        return render_state(cfg)
    sub = argv[0].lower()

    if sub in ("on", "off"):
        if len(argv) < 2 or argv[1].lower() not in CHANNELS:
            return "usage: /message %s <%s>" % (sub, "|".join(CHANNELS))
        set_active(argv[1].lower(), sub == "on")
        return "%s → %s" % (argv[1].lower(), "active" if sub == "on" else "off")

    if sub == "telegram":
        tok = (prompt_secret or (lambda _l: None))("Telegram bot token")
        if not tok:
            return "cancelled (no token)"
        configure_telegram(tok)
        cid = None
        try:
            import nx_loop
            cid = nx_loop.resolve_telegram_chat_id({"telegram_bot_token": tok})
            if cid:
                _set_prefs("telegram", chat_id=cid)
        except Exception:
            pass
        return "telegram configured + active" + (
            " (chat %s)" % cid if cid else " — now DM the bot (/start), then run /message telegram again to resolve the chat")

    if sub in ("imessage", "text"):
        # Default = Nexplora-hosted SMS (Nexplora texts you from its number — iMessage AND Android),
        # just your phone, no creds. Advanced: `/message text local <handle>` = local macOS iMessage.
        local = len(argv) > 1 and argv[1].lower() == "local"
        rest = argv[2:] if local else argv[1:]
        handle = rest[0] if rest else ((prompt or (lambda _l: None))(
            "your phone number (Nexplora texts you — iMessage or Android)") or "")
        if not handle:
            return "usage: /message text <phone>"
        configure_imessage(handle, hosted=not local)
        return "text → %s (active, %s)" % (handle, "local iMessage" if local else "via Nexplora")

    if sub == "email":
        if not prompt:
            return "email setup needs an interactive prompt"
        # Advanced BYOK: `/message email smtp` → send from YOUR mailbox via your SMTP.
        if len(argv) > 1 and argv[1].lower() == "smtp":
            if not prompt_secret:
                return "email setup needs an interactive prompt"
            user = prompt("your email address (NX sends reports FROM here)")
            if not user or "@" not in user:
                return "cancelled — need a valid email address"
            host = _smtp_host_for(user)
            to = prompt("send reports TO (Enter = your own address)") or user
            pw = prompt_secret("email app-password (Gmail/iCloud: an APP password, not your login)")
            if not pw:
                return "cancelled — missing app-password"
            configure_email(host, 587, user, pw, to)
            return "email configured + active (%s → %s via %s · your SMTP)" % (user, to, host)
        # Default = Nexplora-hosted: NX emails you FROM hello@nexplora.ai. Just your address.
        to = prompt("your email (NX emails you from hello@nexplora.ai)")
        if not to or "@" not in to:
            return "cancelled — need a valid email address"
        configure_email_hosted(to)
        return "email → %s (active, via Nexplora)" % to

    if sub == "whatsapp":
        if not (prompt and prompt_secret):
            return "whatsapp setup needs an interactive prompt"
        sid = prompt("Twilio Account SID"); frm = prompt("Twilio WhatsApp from-number (+…)")
        to = prompt("send reports TO (+…)"); tok = prompt_secret("Twilio auth token")
        if not (sid and frm and to and tok):
            return "cancelled (missing field)"
        configure_whatsapp(sid, tok, frm, to)
        return "whatsapp configured + active (%s → %s)" % (frm, to)

    return render_state(cfg)
