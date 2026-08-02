"""
nx_creator — the Universal Creator: turn a user's "connect/create X" into a PROVEN integration.

Primary v1 path (highest-yield + most honest): the user POINTS NX at an MCP server → NX discovers its REAL tools
(ListTools) → the PROOF GATE (nx_proof_gate) proves each (reads fired for real, writes schema-validated, bounded
auto-fix) → ONLY gate-proven tools are exposed as `ready`. Nothing is ever presented as ready without real evidence.
NO API-shape inference (deferred): the tools are REAL tools from a real server, not guessed.

classify_tool_kind: drafted by the NX apprentice model (reviewed + accepted).
"""


def classify_tool_kind(name: str) -> str:
    """'write' if the tool name implies a side-effecting/destructive action, else 'read'."""
    write_kinds = {
        "create", "update", "delete", "post", "send", "add", "set", "edit",
        "modify", "remove", "merge", "close", "archive", "publish", "write",
        "insert", "assign", "move", "cancel", "fork", "push", "deploy", "upload",
    }
    lower = (name or "").lower()
    return "write" if any(k in lower for k in write_kinds) else "read"


def create_integration_from_mcp(server, name=None, max_prove=15, args_source=None, fix=True):
    """Create an integration by pointing NX at an MCP server (an already-connected slug, or one you connect first).
    Discovers the server's REAL tools and PROVES each through the gate. A tool is `ready` ONLY if the gate granted it.
    Returns:
      { name, server, discovered:int,
        proven_tools:[{name, kind, ready, evidence|fail, attempts}],
        ready_count:int, ready:bool, error? }
    The integration `ready` is True iff >=1 tool is gate-proven. NEVER exposes an unproven tool as ready."""
    import nx_proof_gate as G
    rec = {"name": name or server, "server": server, "discovered": 0,
           "proven_tools": [], "ready_count": 0, "ready": False}
    # 1) prove the server itself — ListTools = real evidence it's live + authed
    srv = G.prove({"type": "mcp_server", "server": server})
    if not srv.ready:
        rec["error"] = srv.fail
        return rec
    # 2) discover the real tool names
    try:
        import nx_mcp_tools as T
        names = [t.get("name", "") for t in (T._session(server).list_tools() or [])
                 if isinstance(t, dict) and t.get("name")]
    except Exception as e:
        rec["error"] = {"class": "transport", "detail": "list_tools failed: %s" % type(e).__name__}
        return rec
    rec["discovered"] = len(names)
    # 3) prove each (cap the create-pass at max_prove; the rest stay discovered-pending, never faked-ready)
    fixer = G.default_fixer if fix else None
    for tn in names[:max_prove]:
        kind = classify_tool_kind(tn)
        art = {"type": "mcp_tool", "server": server, "tool": tn,
               "args": (args_source or {}).get(tn, {}), "kind": kind}
        v = G.prove_with_fix(art, fixer=fixer, max_attempts=3)
        rec["proven_tools"].append({"name": tn, "kind": kind, "ready": v.ready,
                                    "evidence": v.evidence, "fail": v.fail, "attempts": v.attempts})
        if v.ready:
            rec["ready_count"] += 1
    rec["ready"] = rec["ready_count"] >= 1
    return rec


# ── G3: fresh-integration generation from a USER-SUPPLIED spec (no MCP server needed) ─────────────────────
def _classify_rest_kind(method: str) -> str:
    return "read" if (method or "GET").upper() in ("GET", "HEAD") else "write"


def create_integration_from_spec(name, base_url, actions, auth=None, max_prove=15):
    """Create an integration from a USER-SUPPLIED spec (for a service NX never shipped + has no MCP server):
    base_url + a list of action specs [{name, method, path, args?}] (which the model can generate from an OpenAPI
    doc or the user's description). The PROOF GATE fires each READ for real (real HTTP status) and schema-validates
    each WRITE (never fired). Same honest-or-held discipline as create_integration_from_mcp.

    A READ is `ready` ONLY on real evidence — a 2xx. A WRITE is never fired (you can't prove a write by performing
    it), so it can only be `ready` when a real read CORROBORATES that the base + credential actually work
    (base_confirmed). This mirrors MCP semantics (a write tool is trusted only because ListTools already proved the
    server live). With no corroborating read, a well-formed write is HELD 'base_unconfirmed' — never faked-ready —
    so a wrong/dead base can't come back partially ready off schema-validation alone (docs-found != proven).
    Returns { name, base_url, discovered, proven_tools:[...], ready_count, base_confirmed, ready }."""
    import nx_proof_gate as G
    acts = list(actions or [])[:max_prove]
    rec = {"name": name or base_url, "base_url": base_url, "discovered": len(acts),
           "proven_tools": [], "ready_count": 0, "base_confirmed": False, "ready": False}
    # Pass 1: fire the reads. base_confirmed = a MEANINGFUL 2xx — a GET (not HEAD, which proves only reachability)
    # to a NON-root path (root/landing/SPA-catch-all is not corroboration), fired with the same auth the writes use.
    # Only such a read is real evidence the base + credential actually work (closes: HEAD-to-root / any-2xx-to-/
    # blessing fabricated writes).
    read_v = {}
    for i, a in enumerate(acts):
        if _classify_rest_kind(a.get("method", "GET")) != "read":
            continue
        read_v[i] = G.prove({"type": "rest_action", "base_url": base_url, "path": a.get("path"),
                             "method": a.get("method", "GET"), "args": a.get("args") or {}, "auth": auth, "kind": "read"})

    def _confirms(idx):
        v = read_v.get(idx)
        if not v or not v.ready:
            return False
        act = acts[idx]
        if str(act.get("method") or "GET").upper() == "HEAD":
            return False
        p = str(act.get("path") or "").strip()
        return p not in ("", "/")
    base_confirmed = any(_confirms(i) for i in read_v)
    # Pass 2: assemble in order. Writes are validated-ready ONLY if base_confirmed; else held (no real evidence).
    for i, a in enumerate(acts):
        method = a.get("method", "GET")
        kind = _classify_rest_kind(method)
        label = a.get("name") or ("%s %s" % (method, a.get("path")))
        if kind == "read":
            v = read_v[i]
            ready, ev, fail = v.ready, v.evidence, v.fail
        else:
            vv = G.prove({"type": "rest_action", "base_url": base_url, "path": a.get("path"),
                          "method": method, "args": a.get("args") or {}, "auth": auth, "kind": "write"})
            if vv.ready and base_confirmed:
                ready, ev, fail = True, vv.evidence, None
            elif vv.ready:  # spec valid but no read confirmed the base — honest hold, never faked
                ready, ev, fail = False, None, {"class": "base_unconfirmed",
                                                "detail": "write spec valid, but no read confirmed the base/credential — add a read to corroborate"}
            else:
                ready, ev, fail = False, None, vv.fail
        rec["proven_tools"].append({"name": label, "kind": kind, "ready": ready, "evidence": ev, "fail": fail})
        if ready:
            rec["ready_count"] += 1
    rec["base_confirmed"] = base_confirmed
    rec["ready"] = rec["ready_count"] >= 1 and base_confirmed
    _save_generated_integration(rec)
    return rec


def _integrations_dir():
    import os
    return os.path.join(os.path.expanduser("~"), ".nx", "generated_integrations")


def _save_generated_integration(rec):
    """Persist a generated integration with honest status (proven iff the gate confirmed >=1 real tool)."""
    import os, json, re
    name = rec.get("name")
    if not name:
        return
    try:
        d = _integrations_dir(); os.makedirs(d, exist_ok=True)
        slug = re.sub(r"[^a-zA-Z0-9_-]", "_", str(name))[:64] or "integration"
        rec2 = dict(rec); rec2["status"] = "proven" if rec.get("ready") else "pending"
        with open(os.path.join(d, slug + ".json"), "w", encoding="utf-8") as f:
            json.dump(rec2, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


def list_user_integrations():
    """The 'my integrations' list (generated ones) with HONEST status: [{name, base_url, status, ready_count, discovered}]."""
    import os, glob, json
    out = []
    for f in glob.glob(os.path.join(_integrations_dir(), "*.json")):
        try:
            with open(f, encoding="utf-8") as fh:
                d = json.load(fh)
        except Exception:
            continue
        if not d.get("name"):
            continue
        out.append({"name": d.get("name"), "base_url": d.get("base_url"),
                    "status": d.get("status", "pending"), "ready_count": d.get("ready_count", 0),
                    "discovered": d.get("discovered", 0)})
    return sorted(out, key=lambda i: str(i.get("name")))


# ── G4: web-enriched generation — fetch REAL docs → generate specs → gate proves by REAL call ─────────────
# THE LAW: research/docs are INPUT, never proof. A documented endpoint that does not actually respond 2xx is HELD,
# no matter how good the doc looked. Only the gate's real calls confer readiness; the fetch confers nothing.
def _openapi_to_actions(spec, max_actions=20):
    """Deterministically turn an OpenAPI 3 doc into ACTION_SPECS — structure comes straight from paths/methods/
    operationId + parameters, NO inference. The gate still proves each by a real call."""
    actions = []
    paths = (spec or {}).get("paths") or {}
    if not isinstance(paths, dict):
        return actions
    for path, ops in paths.items():
        if not isinstance(ops, dict):
            continue
        for method, op in ops.items():
            if str(method).upper() not in ("GET", "HEAD", "POST", "PUT", "PATCH", "DELETE"):
                continue
            op = op if isinstance(op, dict) else {}
            name = op.get("operationId") or ("%s %s" % (str(method).upper(), path))
            args = {}
            for p in (op.get("parameters") or []):  # fill required query params from example/default/enum
                if isinstance(p, dict) and p.get("in") == "query" and p.get("required"):
                    schema = p.get("schema") or {}
                    val = schema.get("example")
                    if val is None:
                        val = schema.get("default")
                    if val is None and isinstance(schema.get("enum"), list) and schema["enum"]:
                        val = schema["enum"][0]
                    if val is not None:
                        args[p.get("name")] = val
            actions.append({"name": name, "method": str(method).upper(), "path": path, "args": args})
            if len(actions) >= max_actions:
                return actions
    return actions


def _resolve_openapi_base(spec, doc_url=None):
    """Base URL for the API from OpenAPI servers[0].url — a relative server path is resolved against the doc host
    (that IS the documented API location), an absolute one is used as-is. If NO server is declared, return None: we
    do NOT guess the doc-hosting host as the API base (a reachable doc host is not a working API — docs-found !=
    proven; with no base, create_integration_from_spec confirms nothing and holds every action)."""
    import urllib.parse as _up
    servers = (spec or {}).get("servers") or []
    if servers and isinstance(servers[0], dict) and servers[0].get("url"):
        base = str(servers[0]["url"])
        if base.startswith("/") and doc_url:
            u = _up.urlparse(doc_url)
            return "%s://%s%s" % (u.scheme, u.netloc, base)
        if base.startswith("http"):
            return base
    return None


def generate_integration_from_openapi(openapi_url, name=None, base_url=None, auth=None, max_prove=12):
    """WEB-ENRICHED generation: fetch a REAL OpenAPI doc (research = INPUT), deterministically turn it into
    ACTION_SPECS, then let the PROOF GATE prove each by a REAL call. LAW: docs-found != proven — a documented
    endpoint that doesn't actually respond 2xx is HELD, however good the doc looked. Only the gate's real calls
    confer readiness; the fetch confers nothing.
    Returns the create_integration_from_spec rec, plus {doc_fetched, source_doc}."""
    import json as _json
    import nx_proof_gate as G
    ok, text, status = G.fetch_doc(openapi_url)
    if not ok:
        return {"name": name or openapi_url, "error": {"class": "docs", "detail": "couldn't fetch docs: %s" % status},
                "doc_fetched": False, "ready": False, "proven_tools": [], "ready_count": 0, "discovered": 0}
    try:
        spec = _json.loads(text)
    except Exception:
        return {"name": name or openapi_url, "error": {"class": "docs", "detail": "docs not valid OpenAPI JSON"},
                "doc_fetched": True, "ready": False, "proven_tools": [], "ready_count": 0, "discovered": 0}
    actions = _openapi_to_actions(spec, max_actions=max_prove)
    base = base_url or _resolve_openapi_base(spec, openapi_url)
    title = ((spec.get("info") or {}).get("title")) if isinstance(spec.get("info"), dict) else None
    rec = create_integration_from_spec(name or title or base, base, actions, auth=auth, max_prove=max_prove)
    rec["doc_fetched"] = True      # the doc was fetched — but this line is NOT readiness; rec['ready'] is the gate's
    rec["source_doc"] = openapi_url
    return rec


# ── G5: fresh-tool generation — sandboxed compute + walled action, the gate EXECUTES to prove ─────────────
def _tools_dir():
    import os
    return os.path.join(os.path.expanduser("~"), ".nx", "generated_tools")


def create_tool(name, code=None, kind="compute", server=None, action=None, args="", schema=None, probe_input=None, save=True):
    """Create a GENERATED tool and PROVE it. compute: an NX-written PURE function, EXECUTED in the structural sandbox
    (nx_tool_sandbox) with a probe input — ready iff real output + no escape (an escape attempt is contained + HELD).
    action: a declarative binding to an external effect; it MUST declare its real target (server, action) so the WALL
    (guarded_loop_action, is_untouchable FIRST) classifies EVERY call — a T3-untouchable is HELD at the wall, never
    fired. Saves to ~/.nx/generated_tools/<name>.json as pending|proven (the gate is the ONLY authority).
    Returns { name, kind, origin, ready, status, evidence|fail }."""
    import os, json
    import nx_proof_gate as G
    origin = "generated:" + str(name)
    v = G.prove({"type": "tool", "name": name, "kind": kind, "code": code, "input": probe_input,
                 "server": server, "action": action, "args": args})
    status = "proven" if v.ready else "pending"
    rec = {"name": name, "kind": kind, "origin": origin, "server": server, "action": action,
           "code": code, "schema": schema, "args": args, "probe_input": probe_input, "status": status, "proof": v.to_dict()}
    if save:
        try:
            d = _tools_dir(); os.makedirs(d, exist_ok=True)
            with open(os.path.join(d, str(name) + ".json"), "w", encoding="utf-8") as f:
                json.dump(rec, f, indent=2, ensure_ascii=False)
        except Exception:
            pass
    return {"name": name, "kind": kind, "origin": origin, "ready": v.ready, "status": status,
            "evidence": v.evidence, "fail": v.fail}


def prove_and_mark_tool(name, probe_input=None):
    """Re-run a saved generated tool through the gate and rewrite proven|pending + proof. Gate is the ONLY authority."""
    import os, json
    import nx_proof_gate as G
    path = os.path.join(_tools_dir(), str(name).lstrip("$") + ".json")
    try:
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
    except Exception:
        return G.Verdict.failed("not_found", "tool %s not found" % name)
    v = G.prove({"type": "tool", "name": d.get("name"), "kind": d.get("kind", "compute"), "code": d.get("code"),
                 "input": probe_input if probe_input is not None else d.get("probe_input"),
                 "server": d.get("server"), "action": d.get("action"), "args": d.get("args", "")})
    d["status"] = "proven" if v.ready else "pending"
    d["proof"] = v.to_dict()
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2, ensure_ascii=False)
    except Exception:
        pass
    return v


def list_user_tools():
    """The 'my tools' list with HONEST status: [{name, kind, status, origin, fail?}]. Nothing hidden."""
    import os, glob, json
    out = []
    for f in glob.glob(os.path.join(_tools_dir(), "*.json")):
        try:
            with open(f, encoding="utf-8") as fh:
                d = json.load(fh)
        except Exception:
            continue
        if not d.get("name"):
            continue
        out.append({"name": d.get("name"), "kind": d.get("kind", "compute"),
                    "status": d.get("status", "pending"), "origin": d.get("origin"),
                    "fail": (d.get("proof") or {}).get("fail")})
    return sorted(out, key=lambda t: str(t.get("name")))


# ── B6: the same gate replicated to messages / agents / skills ───────────────────────────────────────────
def create_message_flow(channel, name=None):
    """Create a message flow — proven by a REAL delivery to `channel` (held if it can't deliver, never faked)."""
    import nx_proof_gate as G
    v = G.prove({"type": "message", "channel": channel})
    return {"name": name or ("message:" + channel), "channel": channel, "ready": v.ready, "evidence": v.evidence, "fail": v.fail}


def create_agent(key=None, task="Reply with the single word READY.", name=None, agent_id=None):
    """Create/adopt an agent — proven by RUNNING one real turn (RUN-IS-REAL); held if the run doesn't happen.
    Custom agents pass agent_id (canonical ones pass key)."""
    import nx_proof_gate as G
    v = G.prove({"type": "agent", "key": key, "agentId": agent_id, "task": task})
    return {"name": name or ("agent:" + (agent_id or key or "?")), "key": key, "agentId": agent_id,
            "ready": v.ready, "evidence": v.evidence, "fail": v.fail}


def create_skill(name, probe="hello", expect=None):
    """Create a skill — proven by RUNNING it (overlay + probe); ready iff non-empty output AND (if declared) it
    contains `expect`. Closes 'saved but never tested'."""
    import nx_proof_gate as G
    v = G.prove({"type": "skill", "name": name, "probe": probe, "expect": expect})
    return {"name": name, "ready": v.ready, "evidence": v.evidence, "fail": v.fail}


# ── G1: fresh-skill generation — status model (pending → proven, gate is the ONLY authority) ──────────────
def _skills_dir():
    import os
    return os.path.join(os.path.expanduser("~"), ".nx", "skills")


def prove_and_mark_skill(cmd, probe=None):
    """Run a CREATED skill through the gate (a real run of its overlay) and write proven|pending back to its JSON.
    The gate is the ONLY thing that flips pending→proven; a skill that produces no output STAYS pending (honest,
    never faked). fixer=None: a skill's proof is not arg-auto-fixed (we want the user to see a genuinely bad skill).
    Returns the Verdict."""
    import os, json
    import nx_proof_gate as G
    name = (cmd or "").lstrip("$")
    path = os.path.join(_skills_dir(), name + ".json")
    try:
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
    except Exception:
        return G.Verdict.failed("not_found", "skill %s not found" % cmd)
    v = G.prove_with_fix(
        {"type": "skill", "name": name, "probe": probe or d.get("desc") or "run this skill", "expect": d.get("expect")},
        fixer=None, max_attempts=1)
    d["status"] = "proven" if v.ready else "pending"
    d["proof"] = v.to_dict()
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2, ensure_ascii=False)
    except Exception:
        pass
    return v


def list_user_skills():
    """The 'my skills' list with HONEST status: [{cmd, desc, status:'pending'|'proven', fail?}]. Nothing hidden —
    pending skills show alongside proven ones, clearly marked."""
    import os, glob, json
    out = []
    for f in glob.glob(os.path.join(_skills_dir(), "*.json")):
        b = os.path.basename(f)
        if b in ("manifest.json", "summary.json"):
            continue
        try:
            with open(f, encoding="utf-8") as fh:
                d = json.load(fh)
        except Exception:
            continue
        if not d.get("cmd"):
            continue
        out.append({"cmd": d.get("cmd"), "desc": d.get("desc", ""),
                    "status": d.get("status", "pending"),
                    "fail": (d.get("proof") or {}).get("fail")})
    return sorted(out, key=lambda s: str(s.get("cmd")))


# ── G2: fresh-agent generation — RUN-IS-REAL proof + honest pending/proven status ─────────────────────────
# Agents live server-side (POST /api/agents); we keep a LOCAL proof cache so the my-agents list can show honest
# pending/proven, exactly like skills. The gate (a real /api/agents/run) is the ONLY thing that grants proven.
def _agent_proofs_path():
    import os
    return os.path.join(os.path.expanduser("~"), ".nx", "agent_proofs.json")


def _load_agent_proofs():
    import json
    try:
        with open(_agent_proofs_path(), encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, dict) else {}
    except Exception:
        return {}


def _save_agent_proofs(d):
    import os, json
    p = _agent_proofs_path()
    try:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


def prove_and_mark_agent(agent_id, name=None, task="Reply with the single word READY."):
    """RUN a created agent once (RUN-IS-REAL) through the gate and cache proven|pending locally. The gate is the ONLY
    authority that flips pending→proven; a run that doesn't happen (bad id, auth, endpoint error) STAYS pending
    (honest, never faked). Returns the Verdict."""
    import nx_proof_gate as G
    if not agent_id:
        return G.Verdict.failed("not_found", "no agent id")
    v = G.prove({"type": "agent", "agentId": agent_id, "task": task})
    store = _load_agent_proofs()
    store[str(agent_id)] = {"name": name or store.get(str(agent_id), {}).get("name") or str(agent_id),
                            "status": "proven" if v.ready else "pending", "proof": v.to_dict()}
    _save_agent_proofs(store)
    return v


def list_user_agents(auth_base=None, token=None):
    """The 'my agents' list with HONEST status: [{agentId, name, status:'pending'|'proven', fail?}]. Prefers the
    server roster (source of truth for what exists) joined with the local proof cache; falls back to cache-only when
    the roster is unreachable. Never invents proven."""
    import nx_agents as A
    proofs = _load_agent_proofs()
    out, seen = [], set()
    customs = None
    try:
        if auth_base and token:
            _, customs = A._fetch_roster(auth_base, token)
    except Exception:
        customs = None
    for c in (customs or []):
        aid = str(c.get("agentId") or "")
        if not aid:
            continue
        seen.add(aid)
        pr = proofs.get(aid, {})
        out.append({"agentId": aid, "name": c.get("name") or pr.get("name") or "agent",
                    "status": pr.get("status", "pending"), "fail": (pr.get("proof") or {}).get("fail")})
    for aid, pr in proofs.items():  # cached agents not in the (maybe-unreachable) roster
        if aid in seen:
            continue
        out.append({"agentId": aid, "name": pr.get("name") or "agent",
                    "status": pr.get("status", "pending"), "fail": (pr.get("proof") or {}).get("fail")})
    return sorted(out, key=lambda a: str(a.get("name")))


def creation_summary(rec) -> str:
    """One HONEST human line for a created integration — what's proven ready, what's held (never hidden)."""
    if rec.get("error"):
        return "❌ %s — couldn't create: %s" % (rec.get("name"), (rec.get("error") or {}).get("detail", "failed"))
    held = [t["name"] for t in rec["proven_tools"] if not t["ready"]]
    line = "✅ %s — %d/%d tools PROVEN ready (of %d discovered)" % (
        rec.get("name"), rec["ready_count"], len(rec["proven_tools"]), rec["discovered"])
    if held:
        line += "  ·  held (unproven, NOT exposed): %s" % ", ".join(held[:6])
    return line
