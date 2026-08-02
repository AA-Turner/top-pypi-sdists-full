"""
nx_proof_gate — THE PROOF GATE for the Universal Creator.

One callable, `prove(artifact) -> Verdict`, that runs a created thing (MCP tool/server, channel action, …) END-TO-END
and grants `ready` ONLY on REAL evidence from a REAL call. "created"/"connected"/"saved" is never "ready" — the gate
is the only thing that can grant ready. It does NOT reinvent proof: it dispatches per artifact-type to the honest-by-
construction executors already built this session (nx_mcp_tools.call, nx_channels.execute_channel_action, …), which
never fake success — the gate inherits that and unifies it behind one verdict.

HONESTY LAWS baked in:
  • ready is True ONLY with real evidence (real tool output / real ListTools / real 2xx). Never on a label.
  • WRITE/destructive tools are NEVER auto-fired to "prove" them (you can't prove a delete by deleting) — they are
    schema-validated (exists + callable + authed), evidence honestly marked weaker than a fired read.
  • On fail, the bounded auto-fix loop tries ≤N corrections then HONEST-FAILS — never loops, never fakes.

Verdict dataclass: drafted by NX (apprentice) under review, accepted as-is.
"""
from dataclasses import dataclass, asdict


@dataclass
class Verdict:
    ready: bool
    evidence: dict | None
    fail: dict | None
    attempts: int = 1

    @classmethod
    def ok(cls, kind: str, sample: str) -> "Verdict":
        return cls(ready=True, evidence={"kind": kind, "sample": (sample or "")[:1000]}, fail=None)

    @classmethod
    def failed(cls, cls_: str, detail: str, http: int | None = None) -> "Verdict":
        return cls(ready=False, evidence=None, fail={"class": cls_, "detail": (detail or "")[:400], "http": http})

    def to_dict(self) -> dict:
        return asdict(self)


# Fail classes the bounded auto-fix loop knows how to react to.
FAIL_CLASSES = ("auth", "scope", "endpoint", "arg_shape", "not_found", "empty", "transport")


def _classify(status, detail) -> str:
    """Map an executor's (status, detail) to a fail class the auto-fix loop can act on."""
    d = (detail or "").lower()
    s = status or 0
    if s == 401 or any(k in d for k in ("unauthor", "not_signed", "not_connected", "not authenticated", "http_401", "token")):
        return "auth"
    if s in (402, 403) or any(k in d for k in ("forbidden", "scope", "insufficient", "credits", "payment", "http_402", "http_403")):
        return "scope"
    if s == 404 or any(k in d for k in ("not found", "unknown_tool", "unknown_operation", "unknown_connector", "not_wired", "http_404")):
        return "not_found"
    if any(k in d for k in ("missing_arg", "invalid arg", "-32602", "required", "validation", "bad_arg", "zoderror", "invalid_type", "bad_args")):
        return "arg_shape"
    if any(k in d for k in ("bos_proxy", "not_deployed", "pending", "session did not", "did not init")):
        return "endpoint"
    if not detail and not status:
        return "empty"
    if any(k in d for k in ("request_failed", "timeout", "econnreset", "transport")):
        return "transport"
    return "endpoint"


# ── adapters: each calls an EXISTING honest executor and maps to a Verdict ────────────────────────────────
def _prove_mcp_server(server) -> Verdict:
    """Point-at-an-MCP-server proof (the primary creation path): ListTools returning REAL tools proves the server
    is live + authed. Safe — no side effects. Evidence = the real tool names. (nx_mcp_tools._session/list_tools)."""
    if not server:
        return Verdict.failed("not_found", "no server")
    try:
        import nx_mcp_tools as T
        sess = T._session(server)
        if sess is None:
            return Verdict.failed("endpoint", "%s: session did not initialize (reconnect)" % server)
        tools = sess.list_tools() or []
        names = [(t.get("name", "") if isinstance(t, dict) else str(t)) for t in tools]
        names = [n for n in names if n]
        if not names:
            return Verdict.failed("empty", "%s: connected but ListTools returned 0 tools" % server)
        return Verdict.ok("mcp_listtools", "%s: %d tools — %s" % (server, len(names), ", ".join(names[:15])))
    except Exception as e:
        return Verdict.failed("transport", "list_tools failed: %s" % type(e).__name__)


def _prove_mcp_tool(server, tool, args, kind="read") -> Verdict:
    """Single MCP tool. READ: fire for REAL, real data = evidence. WRITE: NEVER auto-fire — validate the tool
    exists in ListTools (real + callable), evidence kind='schema_validated' (honestly weaker than a fired read)."""
    if not (server and tool):
        return Verdict.failed("not_found", "server + tool required")
    import nx_mcp_tools as T
    if kind == "write":
        try:
            sess = T._session(server)
            if sess is None:
                return Verdict.failed("endpoint", "%s: session did not initialize" % server)
            tools = sess.list_tools() or []
        except Exception as e:
            return Verdict.failed("transport", "list_tools failed: %s" % type(e).__name__)
        if not any(isinstance(t, dict) and t.get("name") == tool for t in tools):
            return Verdict.failed("not_found", "%s.%s not in the server's tool list" % (server, tool))
        return Verdict.ok("schema_validated", "%s.%s exists + authed (WRITE tool — validated, NOT fired)" % (server, tool))
    r = T.call(server, tool, args if isinstance(args, dict) else {}) or {}
    if r.get("ok"):
        return Verdict.ok("tool_output", str(r.get("text", "")))
    err = str(r.get("error", ""))
    return Verdict.failed(_classify(None, err), err or "call failed")


def _prove_channel_action(slug, action, args, kind="read") -> Verdict:
    """Channel action (X/registry/BOS via nx_channels.execute_channel_action — honest by construction). READ: fire
    for real. WRITE: never auto-fire a real post to 'prove' it — validate the action is wired + reachable."""
    if not (slug and action):
        return Verdict.failed("not_found", "slug + action required")
    import nx_channels as C
    if kind == "write":
        try:
            wired = C.is_channel_action(slug, action)
        except Exception:
            wired = False
        if not wired:
            return Verdict.failed("not_found", "%s.%s is not a wired channel action" % (slug, action))
        return Verdict.ok("action_wired", "%s.%s is wired + reachable (WRITE — validated, NOT fired)" % (slug, action))
    r = C.execute_channel_action(slug, action, args if isinstance(args, dict) else {}) or {}
    ok = r.get("ok", r.get("success"))
    if ok:
        return Verdict.ok("http_2xx", str(r.get("text") or r.get("post_id") or r.get("id") or r))
    detail = str(r.get("detail") or r.get("error") or "failed")
    return Verdict.failed(_classify(r.get("status"), detail), detail, r.get("status"))


# ── B6 adapters: replicate the gate to messages / agents / skills ────────────────────────────────────────
def _prove_message(channel, text=None) -> Verdict:
    """Prove a message flow by sending a REAL test message to `channel` via its own sender; ready iff it delivered.
    Closes the 'reported working but never delivered' failure. Never fakes."""
    if not channel:
        return Verdict.failed("not_found", "no channel")
    try:
        import nx_message as M
        entry = (M.channels_state() or {}).get(channel)
        if not entry or not (entry.get("active") and entry.get("configured")):
            return Verdict.failed("not_found", "%s not active/configured" % channel)
        sender = (getattr(M, "_SENDERS", {}) or {}).get(channel)
        if not callable(sender):
            return Verdict.failed("not_found", "no sender wired for %s" % channel)
        sender(text or "NX message-flow proof ✅", entry)  # raises on a real delivery failure
        return Verdict.ok("delivered", "%s: delivered" % channel)
    except Exception as e:
        # Surface the REAL reason (the sender puts the osascript/HTTP detail in the message), not just the
        # exception type — "RuntimeError" tells the operator nothing; "imessage: Not authorized to send Apple
        # events" tells them exactly what to fix.
        detail = (str(e) or type(e).__name__).strip()
        return Verdict.failed("transport", "%s send failed: %s" % (channel, detail[:200]))


def _prove_agent(key, task="Reply with the single word READY.", agent_id=None) -> Verdict:
    """Prove an agent by RUNNING one real turn (RUN-IS-REAL) via POST /api/agents/run — ready iff a real run/ops
    come back. Never a def-only pass. Custom agents run by agentId (canonical `key` is canonical-only server-side)."""
    if not key and not agent_id:
        return Verdict.failed("not_found", "no agent key")
    try:
        import nx_message as _m
        cfg = _m._load_config() or {}
        token = str(cfg.get("token") or cfg.get("nx_token") or "").strip()
        base = _m._auth_base().rstrip("/")
        if not token:
            return Verdict.failed("auth", "not signed in")
        import nx_cloud_dispatch as _cd
        body = {"task": task}
        if agent_id:
            body["agentId"] = agent_id
        else:
            body["key"] = key
        st, d = _cd._req("POST", "%s/api/agents/run" % base, token, body=body, timeout=120)
        d = d or {}
        # RUN-IS-REAL, but an explicit ok:false or error body is a FAILED run — the presence of a trace/ops field
        # doesn't launder it into ready (a failed orchestration still returns a trace).
        ok_field = d.get("ok")
        if st in (200, 201) and ok_field is not False and not d.get("error") and (ok_field or d.get("ops") or d.get("result") or d.get("trace")):
            return Verdict.ok("agent_run", str(d.get("result") or d.get("ops") or d.get("trace") or "ran"))
        return Verdict.failed(_classify(st, str(d.get("error", ""))), str(d.get("error") or ("http_%d" % st)), st)
    except Exception as e:
        return Verdict.failed("transport", "agent run failed: %s" % type(e).__name__)


def _prove_skill(name, probe="hello", expect=None) -> Verdict:
    """Prove a skill by RUNNING it (its overlay + a probe) as a one-shot; ready iff it produces non-empty output AND
    (if the skill declares `expect`) the output contains it. Closes 'saved but never tested'. Best-effort subprocess."""
    if not name:
        return Verdict.failed("not_found", "no skill name")
    import subprocess
    try:
        r = subprocess.run(["nx", "--prompt", probe, "--skill", name], capture_output=True, text=True, timeout=120)
        out = (r.stdout or "").strip()
    except Exception as e:
        return Verdict.failed("transport", "skill run failed: %s" % type(e).__name__)
    if r.returncode != 0:
        return Verdict.failed("run_error", "skill exited %d: %s" % (r.returncode, (r.stderr or out)[:100]))
    if not out:
        return Verdict.failed("empty", "skill produced no output")
    # A CLI error/usage banner is NOT proof — a non-empty error message must never satisfy the probe.
    low = out.lower()
    _BANNERS = ("sign-in required", "session expired", "usage:", "no skill", "not found", "unknown skill",
                "error:", "traceback (most recent", "not signed in")
    if any(low.startswith(b) or (len(out) < 200 and b in low) for b in _BANNERS):
        return Verdict.failed("run_error", "skill output looks like an error banner, not a real run: %s" % out[:80])
    if expect and expect.lower() not in low:
        return Verdict.failed("arg_shape", "output missing declared expect=%r" % expect)
    return Verdict.ok("skill_output", out)


def _is_internal_host(host: str) -> bool:
    """True for loopback / private / link-local / internal hostnames — refused even when operator-supplied (SSRF
    floor). Name-based (best-effort) plus the obvious private IPv4 ranges."""
    h = (host or "").lower().strip("[]")
    if not h or h == "localhost" or h.endswith(".local") or h.endswith(".internal") or h == "::1":
        return True
    if h in ("0.0.0.0",) or h.startswith("127.") or h.startswith("10.") or h.startswith("192.168.") or h.startswith("169.254."):
        return True
    if h.startswith("172."):  # 172.16.0.0 – 172.31.255.255
        try:
            second = int(h.split(".")[1])
            if 16 <= second <= 31:
                return True
        except Exception:
            pass
    return False


def _resolves_internal(host: str) -> bool:
    """Resolve the host and reject if ANY resolved address is private/loopback/link-local/reserved — closes the
    DNS-to-private SSRF bypass a name-only check misses (e.g. evil.com → 127.0.0.1), which matters once base_urls
    can derive from web-researched docs. Resolution failure → False (the real request will then fail honestly)."""
    try:
        import socket, ipaddress
        for info in socket.getaddrinfo(host, None):
            ip = info[4][0]
            try:
                addr = ipaddress.ip_address(ip.split("%")[0])
            except Exception:
                continue
            if (addr.is_private or addr.is_loopback or addr.is_link_local or addr.is_reserved
                    or addr.is_multicast or addr.is_unspecified):
                return True
    except Exception:
        return True  # FAIL-CLOSED: if we can't resolve the host, we can't prove it's safe → treat as internal/refuse
    return False


def fetch_doc(url, timeout=25):
    """Read-only, SSRF-guarded GET of a docs / OpenAPI URL. Returns (ok, text, status_or_err). RiskTier-SAFE: read
    only, same https + internal-host floor as the gate's rest reads. Generation uses this to fetch docs as INPUT —
    the fetch NEVER confers readiness (docs-found != proven); only the gate's real calls do."""
    import urllib.parse as _up
    try:
        u = _up.urlparse(url)
    except Exception:
        return (False, "", "unparseable url")
    if u.scheme != "https":
        return (False, "", "docs url must be https")
    if _is_internal_host(u.hostname or "") or _resolves_internal(u.hostname or ""):
        return (False, "", "refusing internal/loopback host")
    try:
        import requests
        # allow_redirects=False: a redirect target is NEVER re-checked by requests, so a 3xx from an allowed host
        # to loopback/metadata would bypass the internal-host guard. A doc that redirects is held; supply the final URL.
        r = requests.get(url, timeout=timeout, headers={"Accept": "application/json, */*"}, allow_redirects=False)
        return (200 <= r.status_code < 300, r.text or "", r.status_code)
    except Exception as e:
        return (False, "", "fetch failed: %s" % type(e).__name__)


def _prove_rest_action(base_url, path, method="GET", args=None, auth=None, kind=None) -> Verdict:
    """Prove a GENERATED integration action against a user-supplied REST endpoint. READ (GET/HEAD): fire it for real
    and surface the REAL HTTP status (ready iff 2xx; 401/403 → auth-held; else held with the real status). WRITE
    (POST/PUT/PATCH/DELETE): schema-VALIDATED, NEVER fired — you can't prove a write by performing it. Honest by
    construction: a real status or an honest hold, never a faked success.
    SAFETY: HTTPS-only + no loopback/private host — the endpoint is operator-supplied via chat, but we still refuse
    obviously-internal targets. Reads only ever fire; writes never touch the network here (so no side effects, and
    the RiskTier wall is never bypassed by the proof itself)."""
    import urllib.parse as _up
    if not base_url or not path:
        return Verdict.failed("arg_shape", "missing base_url or path")
    url = str(base_url).rstrip("/") + "/" + str(path).lstrip("/")
    try:
        u = _up.urlparse(url)
    except Exception:
        return Verdict.failed("arg_shape", "unparseable url")
    if u.scheme != "https":
        return Verdict.failed("insecure", "endpoint must be https (got %r)" % (u.scheme or "none"))
    if _is_internal_host(u.hostname or "") or _resolves_internal(u.hostname or ""):
        return Verdict.failed("insecure", "refusing internal/loopback host %r" % (u.hostname or ""))
    m = (method or "GET").upper()
    k = kind or ("read" if m in ("GET", "HEAD") else "write")
    if k == "write":
        if m not in ("POST", "PUT", "PATCH", "DELETE"):
            return Verdict.failed("arg_shape", "write method invalid: %s" % m)
        return Verdict.ok("rest_write_validated", "spec well-formed: %s %s (write not fired to prove it)" % (m, url))
    headers = {}
    if isinstance(auth, dict):
        if auth.get("bearer"):
            headers["Authorization"] = "Bearer " + str(auth["bearer"])
        elif auth.get("header") and auth.get("value"):
            headers[str(auth["header"])] = str(auth["value"])
    try:
        import requests
        # allow_redirects=False: don't let a 3xx from an allowed host reach an internal target the guard already
        # cleared the ORIGINAL host for (SSRF-via-redirect). A redirect is a real non-2xx status → held, not followed.
        r = requests.request(m, url, headers=headers, params=(args or {}) if m in ("GET", "HEAD") else None,
                             timeout=25, allow_redirects=False)
        status = r.status_code
    except Exception as e:
        return Verdict.failed("transport", "call failed: %s" % type(e).__name__)
    if 200 <= status < 300:
        try:
            body = (r.text or "")[:180]
        except Exception:
            body = ""
        return Verdict.ok("rest_read", "HTTP %d — %s" % (status, body))
    if status in (401, 403):
        return Verdict.failed("auth", "endpoint rejected the credential (HTTP %d)" % status, status)
    return Verdict.failed(_classify(status, ""), "HTTP %d" % status, status)


def _prove_tool(name, code=None, tool_input=None, kind="compute", server=None, action=None, args="") -> Verdict:
    """Prove a GENERATED tool. Two kinds, both un-fakeable and un-bypassable:
      compute — EXECUTE the pure function in the structural sandbox (nx_tool_sandbox) with a probe input; ready iff
        real output + no escape. An escape attempt (import/IO/loop/spawn) is contained and HELD, never proven.
      action  — the tool binds to an external effect; it must DECLARE its real target (server, action). The proof
        routes that target through the WALL (guarded_loop_action → is_untouchable FIRST). A T3-untouchable is HELD
        at the wall; anything else is a declarative binding to an already-honest executor, schema-validated NOT
        fired. The declared target — not the 'generated:<name>' origin — is what the wall classifies, so a generated
        tool can neither escape the sandbox nor launder an untouchable past the wall."""
    if kind == "action":
        if not server or not action:
            return Verdict.failed("arg_shape", "action tool must declare its target (server, action) for the wall")
        try:
            import autonomy_loop as AL
            v = AL.guarded_loop_action(str(server), str(action), str(args or ""))
        except Exception as e:
            return Verdict.failed("transport", "wall check failed: %s" % type(e).__name__)
        if v.tier == "T3":
            return Verdict.failed("untouchable", "HELD at the wall — %s" % v.reason)
        return Verdict.ok("tool_action_validated", "wall %s: %s (write not fired to prove it)" % (v.tier, v.reason))
    if not code:
        return Verdict.failed("arg_shape", "compute tool has no code")
    try:
        import nx_tool_sandbox as SB
        r = SB.run_pure(code, tool_input if tool_input is not None else {})
    except Exception as e:
        return Verdict.failed("transport", "sandbox failed: %s" % type(e).__name__)
    if r.get("ok"):
        return Verdict.ok("tool_output", "sandbox(%s) → %s" % (r.get("sandbox_level"), str(r.get("output"))[:160]))
    return Verdict.failed("escape" if r.get("escaped") else "tool_error", str(r.get("error"))[:160])


# ── the gate ─────────────────────────────────────────────────────────────────────────────────────────────
def prove(artifact) -> Verdict:
    """Run `artifact` end-to-end and return a Verdict. artifact = {type, ...}:
      {type:'mcp_server', server}                              — ListTools proof (safe)
      {type:'mcp_tool', server, tool, args?, kind?}            — read: fire; write: schema-validate
      {type:'channel_action', slug, action, args?, kind?}      — read: fire; write: validate wired
    Never raises; never fakes ready."""
    if not isinstance(artifact, dict):
        return Verdict.failed("empty", "no artifact")
    t = artifact.get("type")
    try:
        if t == "mcp_server":
            return _prove_mcp_server(artifact.get("server"))
        if t == "mcp_tool":
            return _prove_mcp_tool(artifact.get("server"), artifact.get("tool"), artifact.get("args") or {}, artifact.get("kind", "read"))
        if t == "channel_action":
            return _prove_channel_action(artifact.get("slug"), artifact.get("action"), artifact.get("args") or {}, artifact.get("kind", "read"))
        if t == "message":
            return _prove_message(artifact.get("channel"), artifact.get("text"))
        if t == "agent":
            return _prove_agent(artifact.get("key"), artifact.get("task", "Reply with the single word READY."), artifact.get("agentId"))
        if t == "skill":
            return _prove_skill(artifact.get("name"), artifact.get("probe", "hello"), artifact.get("expect"))
        if t == "rest_action":
            return _prove_rest_action(artifact.get("base_url"), artifact.get("path"), artifact.get("method", "GET"),
                                      artifact.get("args") or {}, artifact.get("auth"), artifact.get("kind"))
        if t == "tool":
            return _prove_tool(artifact.get("name"), artifact.get("code"), artifact.get("input"),
                               artifact.get("kind", "compute"), artifact.get("server"), artifact.get("action"),
                               artifact.get("args", ""))
        return Verdict.failed("not_found", "unknown artifact type: %s" % t)
    except Exception as e:
        return Verdict.failed("transport", "prove crashed: %s" % type(e).__name__)


# ── B2: the default auto-fix POLICY (diagnose fail class -> bounded patch) ────────────────────────────────
def _mcp_tool_schema(server, tool) -> dict:
    """The input JSON-schema for an MCP tool (from ListTools), or {}. Used to fill missing required args."""
    try:
        import nx_mcp_tools as T
        sess = T._session(server)
        for t in (sess.list_tools() or []):
            if isinstance(t, dict) and t.get("name") == tool:
                return t.get("inputSchema") or t.get("input_schema") or t.get("parameters") or {}
    except Exception:
        pass
    return {}


def _fill_required(schema, have):
    """Fill a tool's REQUIRED args that are missing, from the tool's own schema (enum/type-sane defaults). Returns
    (new_args, filled_keys). This is 'the user doesn't get stuck' — NX supplies sane values instead of erroring."""
    props = (schema or {}).get("properties", {}) or {}
    req = (schema or {}).get("required", []) or []
    out = dict(have or {})
    filled = []
    for k in req:
        if str(out.get(k, "")).strip():
            continue
        p = props.get(k, {}) or {}
        ty = p.get("type")
        if p.get("enum"):
            out[k] = p["enum"][0]
        elif ty in ("number", "integer"):
            out[k] = 1
        elif ty == "boolean":
            out[k] = False
        elif ty == "array":
            out[k] = []
        elif ty == "object":
            out[k] = {}
        else:
            kn = k.lower()
            out[k] = "nexplora" if any(s in kn for s in ("query", "search", "term", "name", "title", "text", "q")) else "test"
        filled.append(k)
    return out, filled


def default_fixer(artifact, verdict):
    """Bounded auto-fix policy — reacts to the fail CLASS and returns a patched artifact, or None when it's NOT
    auto-fixable (→ surface honestly to the user, never fabricate a pass). Only touches genuinely-fixable classes:
      • arg_shape → fill missing required args from the tool's schema (read tools only; never mutate a write to pass)
      • transport → one retry
    auth/scope/not_found/endpoint are NOT auto-fixed here (they need a user cred/scope or a real correction)."""
    if not getattr(verdict, "fail", None):
        return None
    cls = verdict.fail.get("class")
    if cls == "arg_shape" and artifact.get("type") == "mcp_tool" and artifact.get("kind", "read") == "read":
        schema = _mcp_tool_schema(artifact.get("server"), artifact.get("tool"))
        newargs, filled = _fill_required(schema, artifact.get("args") or {})
        if filled:
            b = dict(artifact)
            b["args"] = newargs
            return b
    if cls == "transport":
        return dict(artifact)  # single bounded retry
    return None  # honest surface — not auto-fixable


def prove_with_fix(artifact, fixer=None, max_attempts=3) -> Verdict:
    """Prove; on fail, call fixer(artifact, verdict) -> artifact|None to attempt a BOUNDED correction, then re-prove.
    Stops at `ready` or `max_attempts` — then HONEST-FAILS with the last verdict. Never loops forever, never fakes.
    `fixer` is the auto-fix policy (diagnose class -> patch args/endpoint/scope); None = single-shot prove."""
    v = prove(artifact)
    v.attempts = 1
    a = artifact
    n = 1
    while (not v.ready) and fixer and n < max(1, max_attempts):
        try:
            a2 = fixer(a, v)
        except Exception:
            a2 = None
        if not a2:
            break
        a = a2
        n += 1
        v = prove(a)
        v.attempts = n
    return v
