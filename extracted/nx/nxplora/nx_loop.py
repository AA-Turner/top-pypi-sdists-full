"""GRAIL Phase 5 — live wiring for the autonomy loop.

The pure, gated loop logic lives in `autonomy_loop.py` (unit-proven, all seams injected). This module binds
those seams to the live CLI at RUNTIME: enumerate connected tools per world, fire a SAFE read through the
double gate, send the report to Telegram, tee the durable half to the brain, and persist an audit record.

Imports of the heavy CLI internals (`nx_cli`, `nx_mcp_tools`, `requests`) are LAZY — inside the adapter
closures — so importing this module is cheap and non-circular (nx_cli's `/loop` entry lazily imports this).

SAFETY: the fire adapter calls `nx_cli._guarded_mcp_call` with `{_noninteractive:True, _approve_ok:False}`,
so it is DOUBLE-GATED — `autonomy_loop.guarded_loop_action` already decided T1, and the CLI chokepoint
independently re-checks `is_untouchable()` + tier and hard-blocks anything non-SAFE (no TTY → fail-closed).
"""
import os
import json
import time
import uuid

try:  # bare-module (nx/cli on path) or package submodule
    import autonomy_loop as _al
except ImportError:  # pragma: no cover
    from . import autonomy_loop as _al


# ── adapters over the live seams ─────────────────────────────────────────────────────────────────────────

# ── world-scoped enumeration: which connected servers are relevant to which world ────────────────────────
# Non-agent worlds (research/finance/…) otherwise fall back to ALL connected tools (agent_slugs only maps crew
# agents). This narrows each world to its relevant servers — better relevance + fewer wasted reads. Substring
# match on the server name/slug. FALLBACK to all-connected when a world has no map OR no connected server
# matches, so a world never enumerates empty when tools are actually connected.
WORLD_SERVERS = {
    "finance": ("stripe", "quickbooks", "xero", "mercury", "brex", "ramp", "plaid", "wise", "gusto", "bill", "expensify", "netsuite", "square"),
    "capital": ("stripe", "mercury", "carta", "pulley", "brex", "angellist", "ramp"),
    "sales": ("hubspot", "salesforce", "pipedrive", "close", "apollo", "gong", "outreach", "salesloft", "clari", "attio"),
    "crm": ("hubspot", "salesforce", "pipedrive", "attio", "close", "copper", "zoho"),
    "customers": ("hubspot", "salesforce", "zendesk", "intercom", "gainsight", "vitally"),
    "leads": ("apollo", "clay", "zoominfo", "hunter", "tavily", "exa", "linkedin", "phantombuster", "instantly"),
    "marketing": ("hubspot", "mailchimp", "marketo", "meta", "google", "linkedin", "buffer", "hootsuite", "sprout", "klaviyo"),
    "growth": ("amplitude", "mixpanel", "ga", "googleanalytics", "posthog", "segment", "heap"),
    "brand": ("canva", "figma", "frontify", "adobe", "webflow"),
    "support": ("zendesk", "intercom", "frontapp", "helpscout", "gorgias", "freshdesk"),
    "hr": ("rippling", "gusto", "bamboohr", "workday", "deel", "greenhouse", "lever", "ashby"),
    "recruiting": ("greenhouse", "lever", "ashby", "linkedin", "gem", "workable"),
    "legal": ("docusign", "ironclad", "pandadoc", "hellosign", "notion", "google"),
    "compliance": ("drata", "vanta", "secureframe", "onetrust", "notion"),
    "devops": ("github", "gitlab", "vercel", "netlify", "sentry", "datadog", "pagerduty", "cloudflare", "aws", "supabase"),
    "code": ("github", "gitlab", "linear", "jira", "sentry", "atlassian"),
    "product": ("linear", "jira", "productboard", "notion", "figma", "amplitude", "atlassian"),
    "research": ("tavily", "exa", "notion", "google", "perplexity", "arxiv", "firecrawl"),
    "knowledge": ("notion", "confluence", "google", "slack", "coda", "atlassian"),
    "strategy": ("notion", "google", "tavily", "exa"),
    "ops": ("notion", "asana", "clickup", "monday", "airtable", "linear"),
    "cowork": ("slack", "notion", "google", "asana", "clickup"),
    "onboarding": ("notion", "hubspot", "slack", "arcade"),
}


def _filter_world_servers(world, gathered):
    """Keep only WORLD_SERVERS-relevant servers; fall back to ALL when unmapped or nothing matches."""
    pats = WORLD_SERVERS.get((world or "").strip().lower())
    if not pats or not gathered:
        return gathered
    filt = {}
    for slug, entry in gathered.items():
        name = ((entry or {}).get("name", slug) or "").lower()
        s = (slug or "").lower()
        if any(p in name or p in s for p in pats):
            filt[slug] = entry
    return filt or gathered


def make_enumerate_fn(cfg):
    """enumerate_fn(world) -> [(server, tool)] from the world's connected tools. Lazy nx_mcp_tools/nx_agents."""
    def enumerate_fn(world):
        import nx_mcp_tools as _mt
        try:
            from nx_agents import agent_slugs as _aslugs
        except Exception:
            _aslugs = None
        slugs = _mt.connected_slugs()
        scope = _aslugs(world, slugs) if _aslugs else slugs   # world→agent domain, or all-connected fallback
        gathered = _filter_world_servers(world, _mt.gather_tools(scope) if scope else {})
        out = []
        for slug, entry in (gathered or {}).items():
            name = (entry or {}).get("name", slug)
            for tool in (entry or {}).get("tools", []) or []:
                tn = tool.get("name") if isinstance(tool, dict) else None
                if tn:
                    out.append((name, tn))
        return out
    return enumerate_fn


def make_fire_fn(cfg):
    """fire_fn(world, server, tool, args) -> (ok, output). Double-gated headless SAFE read via _guarded_mcp_call."""
    fire_cfg = dict(cfg or {})
    fire_cfg["_noninteractive"] = True
    fire_cfg["_approve_ok"] = False    # SAFE-only; the CLI chokepoint hard-blocks DESTRUCTIVE/T3 with no TTY
    def fire_fn(world, server, tool, args=""):
        import nx_cli
        res = nx_cli._guarded_mcp_call(server, tool, args or "", fire_cfg) or {}
        if res.get("ok"):
            return (True, res.get("text", ""))
        return (False, res.get("error") or res.get("reason") or "blocked")
    return fire_fn


def make_dry_fire_fn():
    """A dry-run fire_fn: classifies + reports but NEVER invokes a real read."""
    def fire_fn(world, server, tool, args=""):
        return (True, "[dry-run — not fired]")
    return fire_fn


def resolve_telegram_chat_id(cfg=None, token=None):
    """After the operator DMs the bot (/start), read the chat_id from getUpdates. Reads the token from
    env/config (never a literal held here). Returns the most-recent chat_id str, or None if no message yet."""
    import requests
    cfg = cfg or {}
    token = token or os.environ.get("TELEGRAM_BOT_TOKEN") or cfg.get("telegram_bot_token")
    if not token:
        raise RuntimeError("no telegram bot token (TELEGRAM_BOT_TOKEN / telegram_bot_token)")
    r = requests.get("https://api.telegram.org/bot{}/getUpdates".format(token), timeout=12)
    data = r.json() if r.status_code == 200 else {}
    chat_id = None
    for upd in (data.get("result") or []):
        chat = ((upd.get("message") or upd.get("edited_message") or {}).get("chat") or {})
        if chat.get("id") is not None:
            chat_id = str(chat["id"])   # latest message wins
    return chat_id


def send_telegram_message(text, cfg=None):
    """Direct Telegram Bot API sendMessage (BYOK). The token comes from env/config; the chat_id from env/config
    or, if absent, auto-resolved from getUpdates (operator must have DM'd the bot). Raises on missing token /
    unresolved chat / non-200 — report() records the failure honestly."""
    import requests
    cfg = cfg or {}
    token = os.environ.get("TELEGRAM_BOT_TOKEN") or cfg.get("telegram_bot_token")
    if not token:
        raise RuntimeError("telegram not configured (TELEGRAM_BOT_TOKEN / telegram_bot_token)")
    chat_id = (os.environ.get("TELEGRAM_CHAT_ID") or cfg.get("telegram_chat_id")
               or resolve_telegram_chat_id(cfg, token))
    if not chat_id:
        raise RuntimeError("no telegram chat_id — DM the bot (/start) first, or set TELEGRAM_CHAT_ID")
    if len(text) > 4000:                                   # Telegram hard limit is 4096; truncate as a safety net
        text = text[:3970] + "\n… (truncated)"
    r = requests.post(
        "https://api.telegram.org/bot{}/sendMessage".format(token),
        json={"chat_id": chat_id, "text": text}, timeout=12,
    )
    if r.status_code != 200:
        raise RuntimeError("telegram {}: {}".format(r.status_code, (r.text or "")[:120]))


def _default_channel_send(cfg):
    """The loop's default report sender: fan out to the operator's configured /message channels (nx_message),
    falling back to the legacy single Telegram (env TELEGRAM_CHAT_ID / config telegram_bot_token) so the pilot
    keeps working. Raises only if NOTHING delivered — so report() records the outcome honestly."""
    def _send(text):
        try:
            import nx_message
            res = nx_message.send_report(text, cfg)
            if nx_message.any_delivered(res):
                return
        except Exception:
            pass
        send_telegram_message(text, cfg)   # legacy fallback; raises if unconfigured
    return _send


def make_brain_write(cfg):
    """brain_write(text, loop_run) -> tee the run summary to the unified brain (local-first, never blocks)."""
    def brain_write(text, loop_run):
        import nx_cli
        uid = (cfg or {}).get("user_id") or (cfg or {}).get("nx_user_id")
        nx_cli._brain_write_async("loop", cfg, uid, text, "autonomy_run", "loop",
                                  {"loop_run": True, "counts": loop_run.counts})
    return brain_write


RUNS_LOG = os.path.expanduser("~/.nx/autonomy_runs.jsonl")


def persist_run(record, path=RUNS_LOG):
    """Append the audit record to the runs log (observable/replayable). Best-effort; returns bool."""
    try:
        d = os.path.dirname(path)
        if d:
            os.makedirs(d, exist_ok=True)
        with open(path, "a") as f:
            f.write(json.dumps(record) + "\n")
        return True
    except Exception:
        return False


# ── (B) the LLM read-planner: propose SAFE READS WITH ARGS so reads actually return data ─────────────────
# A-only fires connected reads with EMPTY args → most fail (need a query/id). The planner proposes reads with
# sensible arguments grounded in the world. It is UNtrusted by construction — every proposal still passes
# guarded_loop_action downstream, so a proposed write/send is STAGED, never fired. Only the args make a read useful.

def parse_planned_reads(text):
    """Extract [(server, tool, args_json_str)] from a model's JSON response. Tolerant: finds the first JSON
    array, skips malformed entries. args is re-serialized to a JSON string (dicts/lists) or passed through."""
    import json, re
    if not text:
        return []
    m = re.search(r"\[.*\]", text, re.S)
    if not m:
        return []
    try:
        arr = json.loads(m.group(0))
    except Exception:
        return []
    out = []
    for p in arr if isinstance(arr, list) else []:
        if not isinstance(p, dict):
            continue
        server, tool = p.get("server"), p.get("tool")
        if not server or not tool:
            continue
        args = p.get("args")
        args_str = json.dumps(args) if isinstance(args, (dict, list)) else (str(args) if args else "")
        out.append((str(server), str(tool), args_str))
    return out


def _world_read_catalog(cfg, world, limit=40):
    """The world's connected READ tools + their param names — the grounding the planner chooses from."""
    import nx_mcp_tools as _mt
    try:
        from nx_agents import agent_slugs as _aslugs
    except Exception:
        _aslugs = None
    try:
        from risk_tiers import is_read_only
    except Exception:
        from .risk_tiers import is_read_only
    slugs = _mt.connected_slugs()
    scope = _aslugs(world, slugs) if _aslugs else slugs
    gathered = _filter_world_servers(world, _mt.gather_tools(scope) if scope else {})
    cat = []
    for slug, entry in (gathered or {}).items():
        name = (entry or {}).get("name", slug)
        for tool in (entry or {}).get("tools", []) or []:
            if not isinstance(tool, dict):
                continue
            tn = tool.get("name")
            if tn and is_read_only(name, tn):
                schema = tool.get("inputSchema") or {}
                props = schema.get("properties") or {}
                required = set(schema.get("required") or [])
                params = []
                for pn, spec in list(props.items())[:8]:
                    pt = (spec or {}).get("type", "any")            # give the model the TYPE + required(*)
                    params.append("%s%s:%s" % (pn, "*" if pn in required else "", pt))
                desc = (tool.get("description") or "").strip().replace("\n", " ")[:70]
                cat.append({"server": name, "tool": tn, "params": params, "desc": desc})
    return cat[:limit]


def make_llm_fn(cfg, max_reads=8):
    """llm_fn(world, prior=None) -> [(server, tool, args_json)] — the model proposes safe reads WITH args. When
    `prior` (round-1 ActionResults) is given, the planner may chain: use IDs/values found to fill follow-up reads."""
    def llm_fn(world, prior=None):
        import nx_cli
        catalog = _world_read_catalog(cfg, world)
        if not catalog:
            return []
        sys_p = (
            "You are NX's autonomy planner. Pick a SHORT list of SAFE READ actions for this world and fill their "
            "arguments with sensible, relevant values (e.g. a real search query, a plausible lookup). For each read, "
            "include EVERY required param (marked *) and match each param's type exactly (string/integer/boolean/"
            "array/object). Use the exact param NAMES shown — do not invent params. READS ONLY — never writes/sends/"
            'deletes. Output STRICT JSON only: [{"server":"<server>","tool":"<tool>","args":{<name>:<value>}}]. '
            "At most %d items." % max_reads
        )
        catalog_lines = "\n".join(
            "- %s · %s — params[%s]%s" % (
                c["server"], c["tool"], ", ".join(c["params"]),
                (" — " + c["desc"]) if c.get("desc") else "")
            for c in catalog)
        user_p = ("World: %s\nAvailable read tools (param* = required, name:type):\n%s\n"
                  "Respond with the JSON array only." % (world, catalog_lines))
        if prior:                                          # chaining: give the model what round-1 returned
            found = "\n".join(
                "%s.%s → %s" % (a.server, a.tool, str(a.output)[:180])
                for a in prior if getattr(a, "ok", False))[:2000]
            if found:
                user_p += ("\n\nYou already ran these reads. Use any IDs / names / values they returned to fill "
                           "FOLLOW-UP reads (e.g. fetch a specific record by the id you found). Do NOT repeat a read "
                           "you already ran:\n" + found)
        try:
            result = nx_cli.resolve_route_result(cfg, world, user_p)
            chunks = []
            for ch in nx_cli.stream_chat(
                [{"role": "system", "content": sys_p}, {"role": "user", "content": user_p}], cfg,
                api_key=getattr(result, "api_key", None), model=getattr(result, "model", None),
                provider=getattr(result, "provider", None), extra_body=getattr(result, "extra_body", None),
            ):
                chunks.append(ch)
            return parse_planned_reads("".join(chunks))[:max_reads]
        except Exception:
            return []   # planner failure never breaks the run — A-side reads (if any) still fire
    return llm_fn


# ── (chaining) multi-round per-world plan→gate→fire — each round's results feed the next round's planner ──
def _run_world_chained(world, llm_fn, fire_fn, rounds, max_fires):
    """Round 1 plans + fires reads; round 2+ re-plans WITH round-1's results (so a read can use an id found in
    round 1). Only reads fire; writes/money stage; dedup across rounds; the per-world cap bounds total fires."""
    import autonomy_loop as _al
    fired, staged, capped, seen = [], [], [], set()
    prior = None
    for _r in range(max(1, int(rounds or 1))):
        proposals = llm_fn(world, prior) or []
        round_fired = []
        for x in proposals:
            s, t = x[0], x[1]
            a = x[2] if len(x) > 2 else ""
            key = (s, t, a)
            if key in seen:
                continue
            seen.add(key)
            v = _al.guarded_loop_action(s, t, a)
            if v.fires:
                if max_fires is not None and len(fired) >= max_fires:
                    capped.append(_al.Candidate(s, t, a, "planned"))
                    continue
                ok, out = fire_fn(world, s, t, a)
                ar = _al.ActionResult(s, t, a, bool(ok), out, "planned")
                fired.append(ar)
                round_fired.append(ar)
            else:
                staged.append(_al.StagedAction(s, t, a, v.tier, v.reason, "planned"))
        if not round_fired:
            break                                          # nothing new fired → a further round can't chain
        prior = round_fired
    return _al.WorldRunResult(world, _al.world_coarse_tier(world), fired, staged, capped)


# ── entry-point arg parsing (pure + testable; the nx_cli handlers stay thin) ─────────────────────────────
DEFAULT_PILOT_WORLDS = ["research", "knowledge"]   # T1-heavy, pure reads — the safe first-run default


def parse_loop_args(argv):
    """Parse `--loop` / `/loop` flags: [--dry-run] [--llm] [--all] [--world <w>]... → dict."""
    argv = list(argv or [])
    worlds = []
    i = 0
    while i < len(argv):
        if argv[i] == "--world" and i + 1 < len(argv):
            worlds.append(argv[i + 1]); i += 2
        else:
            i += 1
    return {
        "worlds": worlds,
        "dry_run": "--dry-run" in argv,
        "use_llm": "--llm" in argv,
        "all_worlds": "--all" in argv,
        "rounds": 2 if "--chain" in argv else 1,   # --chain → 2-round planning (chaining)
    }


def resolve_worlds(parsed, all_world_keys):
    """Resolve flags to a concrete world list: --all → every world; --world X → those (valid only); else the
    T1-heavy pilot default. Never returns an empty list (falls back to the pilot)."""
    valid = set(all_world_keys)
    if parsed.get("all_worlds"):
        return list(all_world_keys)
    picked = [w for w in parsed.get("worlds", []) if w in valid]
    return picked or list(DEFAULT_PILOT_WORLDS)


# ── the live orchestrator ────────────────────────────────────────────────────────────────────────────────

def cli_loop(cfg, worlds, use_llm=False, dry_run=False, send=True, max_fires=25, rounds=1,
             enumerate_fn=None, fire_fn=None, llm_fn=None, telegram_send=None, brain_write=None,
             persist=True, now=None):
    """Run the a–z autonomy loop live: plan (A[+B]) → gate → fire T1 (or dry-run) → report → record.

    Adapters default to the live ones built from cfg, but are injectable for testing. In dry_run, nothing is
    fired and nothing is sent/persisted (local preview). Returns (loop_run, report_result, record).
    """
    # A (fixed connected reads, EMPTY args) vs B (LLM planner, reads WITH args). With --llm, prefer B and
    # suppress the empty-arg A reads (they mostly fail for want of a query/id); without --llm, A fires.
    if enumerate_fn is None:
        enumerate_fn = (lambda w: []) if use_llm else make_enumerate_fn(cfg)
    if use_llm and llm_fn is None:
        llm_fn = make_llm_fn(cfg)
    plan_fn = _al.compose_plan(enumerate_fn, llm_fn)
    fire_fn = fire_fn or (make_dry_fire_fn() if dry_run else make_fire_fn(cfg))

    clock = now or (lambda: int(time.time()))
    started = clock()
    if use_llm and int(rounds or 1) > 1 and llm_fn is not None:
        # chaining: per-world multi-round planning (round N+1 sees round N's results)
        loop_run = _al.LoopRun([_run_world_chained(w, llm_fn, fire_fn, rounds, max_fires) for w in list(worlds)])
    else:
        loop_run = _al.run_autonomy_loop(list(worlds), plan_fn, fire_fn, max_fires=max_fires)
    ended = clock()

    live = send and not dry_run   # a dry-run NEVER sends/tees, even if a sender was injected — it's a local preview
    if live:
        tg = telegram_send if telegram_send is not None else _default_channel_send(cfg)
        br = brain_write if brain_write is not None else make_brain_write(cfg)
    else:
        tg = br = None
    header = "NX autonomy DRY-RUN" if dry_run else "NX autonomy run"
    rr = _al.report(loop_run, telegram_send=tg, brain_write=br, header=header)

    record = _al.run_record(loop_run, rr, run_id=uuid.uuid4().hex, started_at=started, ended_at=ended)
    if persist and not dry_run:
        persist_run(record)
    return loop_run, rr, record
