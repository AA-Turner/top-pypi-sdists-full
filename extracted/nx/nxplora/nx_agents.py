"""NX AGENTS — the crew under `/crew` in the CLI (Vinny/Halley/Claudia/Azur/Rosetta + create-your-own).

Thin client over the ONE backend (nexplora-v2 /api/agents). The runtime + roster live server-side (MIRROR-0, D2);
this surface shows the crew, toggles agents LIVE, and creates custom ones. No agent logic lives here.

`/crew` opens an interactive picker: the 5 presets (LIVE badge when toggled on) + "＋ Create your own", with the
active crew summarized at the bottom. Toggling adopts (forks the code preset) on first use — rank stays PROSPECT
(the 5 earn 'commissioned' via the gauntlet). `/vinny` etc. remain direct toggle shortcuts. RUN-IS-REAL (invoking
the agent loop) is the backend run route (Stage 4).
"""
import nx_cloud_dispatch as _cd

GOLD = "\033[38;2;212;175;55m"
DIM = "\033[38;2;150;150;150m"
GREEN = "\033[38;2;80;200;120m"
RED = "\033[38;2;220;90;90m"
RESET = "\033[0m"

# key -> (display name, one-line mandate). Cosmetic — the enforced definition lives server-side.
CANONICAL = {
    "vinny": ("Vinny", "Revenue spine — grow → close → capital"),
    "halley": ("Halley", "Build / deliver — what gets made"),
    "claudia": ("Claudia", "Protect / capital-guard — legal, funded, safe"),
    "azur": ("Azur", "Grow / demand — brings the market in"),
    "rosetta": ("Rosetta", "Run / people / care — the running org"),
    # research corps (safe-ops)
    "scout":  ("Scout",  "General web research — find out about X, cited"),
    "scan":   ("Scan",   "Competitor & market scan — landscape, positioning, pricing signal"),
    "verify": ("Verify", "Fact-check — is this claim true, with real sources"),
    "watch":  ("Watch",  "Monitoring & news — what's new on X"),
    "enrich": ("Enrich", "Company / lead enrichment — firmographics & contacts (PDL)"),
}
ORDER = ["vinny", "halley", "claudia", "azur", "rosetta"]

# Friendly labels for the closed-5 opcodes — the run trace reads human, not raw opcode names.
_OP_ACTION = {
    "read_memory": "recalled context",
    "write_graph_node": "created a node",
    "write_brain": "captured a note",
    "emit_value_event": "recorded value",
    "cross_world_signal": "sent a signal",
}

# Each agent's HOME WORLD (a real NX_WORLD_CONTEXT key) — carries the rich role objective the persona pairs with.
AGENT_WORLD = {"vinny": "sales", "halley": "product", "claudia": "finance", "azur": "marketing", "rosetta": "ops",
               # RESEARCH CORPS — the universal safe-ops researchers (standalone + Phase-2 swarm sub-agent corps).
               # All operate in the research world (deep-reasoning tier). RiskTier-SAFE BY CONSTRUCTION: scoped only
               # to search/read reach, so every tool they can hold resolves SAFE — they read the web, return CITED
               # facts, write nothing. Scout/Scan/Verify/Watch need no new key (compose Tavily/Exa); Enrich composes
               # People Data Labs (Victor provisions PDL_API_KEY — until then its firmographic reach is pending).
               "scout": "research", "scan": "research", "verify": "research", "watch": "research", "enrich": "research"}
RESEARCHERS = ["scout", "scan", "verify", "watch", "enrich"]


# Per-agent integration DOMAIN — the keyword set that decides which of the operator's connected integrations a
# crew member actually gets hands on. Without this, every agent was handed the SAME undifferentiated all-24 blob;
# the 110-tool cap (rank-ordered by op-class) then filled up with whatever integration happened to sort first
# (Canva 18, Linear 18, Asana 15…) and STARVED the role-relevant ones — Stripe surfaced 1 of its 11 tools, so
# the finance agent concluded "no financial tools connected" while Stripe sat right there. Scoping to the domain
# gives each agent a focused, role-distinct toolset (Stripe's full 11 for finance, the pipeline tools for sales),
# and is also why the agents stop sounding identical: different hands → different work. Overlap is intentional
# (the moat). Matched substring-either-way so 'monday-com'/'atlassian'/'mcp-deepwiki-com' all resolve.
AGENT_INTEGRATIONS = {
    # revenue spine: CRM, pipeline, payments, commerce, outreach
    "vinny":   ["stripe", "paypal", "square", "hubspot", "salesforce", "pipedrive", "close", "copper",
                "monday", "clickup", "notion", "airtable", "zapier", "apollo", "outreach", "gong",
                "calendly", "ebay", "shopify", "woocommerce", "wix"],
    # build / deliver: eng + product tracking
    "halley":  ["linear", "github", "gitlab", "atlassian", "jira", "confluence", "notion", "clickup",
                "asana", "vercel", "netlify", "sentry", "sourcegraph", "supabase", "cloudflare", "monday",
                "figma", "deepwiki", "globalping", "snowflake"],
    # protect / capital-guard: finance, risk, compliance, ledgers
    "claudia": ["stripe", "paypal", "square", "supabase", "snowflake", "sentry", "quickbooks", "xero",
                "mercury", "brex", "ramp", "plaid", "docusign", "ironclad", "cloudflare", "vercel"],
    # grow / demand: content, web, social, research, campaigns
    "azur":    ["canva", "webflow", "wix", "cloudinary", "notion", "mailchimp", "hubspot", "tiktok",
                "youtube", "instagram", "linkedin", "facebook", "meta", "buffer", "hootsuite", "google",
                "exa", "tavily", "zapier", "ebay"],
    # run / people / care: coordination, tickets, HR, comms
    "rosetta": ["asana", "clickup", "monday", "notion", "linear", "zapier", "atlassian", "jira",
                "confluence", "google", "gmail", "calendar", "slack", "discord", "gorgias", "gusto",
                "rippling", "bamboohr", "sourcegraph"],
    # RESEARCH CORPS — scoped ONLY to search/read reach (Tavily/Exa are the connected web-search tools; both are
    # search-only, so every tool resolves RiskTier-SAFE). This scoping IS the safety: a researcher literally has no
    # write/money/send tool in hand. Enrich adds PDL when the key lands (still read-only firmographic fetch).
    "scout":   ["tavily", "exa"],                    # general web research
    "scan":    ["tavily", "exa"],                    # competitor / market
    "verify":  ["tavily", "exa"],                    # fact-check (cited)
    "watch":   ["tavily", "exa"],                    # monitoring / news
    "enrich":  ["tavily", "exa", "pdl", "peopledatalabs", "apollo", "clearbit"],  # company/lead (PDL pending key)
}


def agent_slugs(key, connected):
    """The subset of CONNECTED integration slugs that fall in this agent's domain, so each crew member gets a
    FOCUSED, role-relevant tool set instead of the same all-integrations blob (see AGENT_INTEGRATIONS). Falls
    back to ALL connected when the agent's domain matches nothing connected — an agent is never left tool-blind."""
    key = (key or "").lstrip("/").lower()
    conn = [s for s in (connected or [])]
    want = AGENT_INTEGRATIONS.get(key)
    if not want:
        return conn
    picked = []
    for slug in conn:
        s = str(slug).lower()
        if any(w and (w in s or s in w) for w in want):
            picked.append(slug)
    return picked or conn


# Auto-delegate signals — phrases specific enough that a single hit is a real domain cue (NOT generic words that
# fire on casual chat). classify_agent scores per agent and only auto-adopts on a CLEAR unique winner, so ordinary
# conversation is never hijacked into an agent turn.
_CLASSIFY_SIGNALS = {
    "vinny":   [" pipeline", " deal", "prospect", " leads", " lead ", " quota", "outreach", "cold email",
                "cold outreach", "upsell", "close the", "closing the", " mrr", " arr", "demo call", "proposal for",
                "discount", "follow up with", "opportunit", "sales call", "book a call", "revenue this"],
    "claudia": ["runway", "burn rate", " burn ", "cash flow", "cashflow", "our budget", " invoice", " expense",
                " margin", "p&l", "fundrais", "cap table", "valuation", "compliance", "contract", " legal",
                "liabilit", "financ", "stripe balance", "cost of", "reconcile", "audit the"],
    "halley":  ["ship ", "the feature", "this feature", "the bug", "this bug", "fix the", "roadmap", " sprint",
                "backlog", "pull request", " deploy", "refactor", "the spec", " mvp", "architecture", "build the",
                " release", "linear issue", "the codebase", "ticket for", "tech debt"],
    "azur":    ["campaign", "content calendar", "content plan", " seo", "our ads", "ad copy", "social post",
                "the funnel", " cac", "landing page", "newsletter", " brand ", "audience", "go to market", " gtm ",
                "positioning", "messaging", "growth loop", "top of funnel"],
    "rosetta": ["onboard", " hire", "hiring", "recruit", "the process", " sop ", "standup", "stand-up", "our team",
                "workflow", "schedule a", "coordinate", "operations", "checklist", "cadence", "people ops",
                " hr ", "meeting notes", "who owns", "assign owner"],
}


def classify_agent(message):
    """Best-fit crew agent for a plain message, or None to stay as plain NX. Conservative keyword scoring: fires
    only on a clear, UNIQUE domain signal (ties or no signal → None) so casual/general chat is never auto-routed."""
    if not message:
        return None
    m = message.strip()
    if m.startswith(("/", "$")):
        return None
    low = f" {m.lower()} "
    scores = {}
    for key, sigs in _CLASSIFY_SIGNALS.items():
        n = sum(1 for s in sigs if s in low)
        if n:
            scores[key] = n
    if not scores:
        return None
    top = max(scores.values())
    winners = [k for k, v in scores.items() if v == top]
    return winners[0] if len(winners) == 1 else None


# DISTINCT personas — each crew member is a specialist with its OWN voice, priorities, and vocabulary (not a
# generic advisor). NX operates IN this role for the turn; the persona never renames the assistant.
PERSONAS = {
    "vinny": (
        "You're the operator's revenue closer. You live in the pipeline: every answer moves a specific deal "
        "forward, qualifies a lead IN, or kills a dead one to free the calendar. You think in cohorts and conversion "
        "math, never vibes — 'which source/title/segment actually closes, and is this deal above or below that "
        "baseline?' Blunt, hungry, impatient with fluff; allergic to hope-as-strategy. You never invent numbers — if "
        "a CRM is connected you pull the real deals, if not you say so and tell them to connect it. End on the ONE "
        "next action that moves money this week."
    ),
    "halley": (
        "You're the operator's builder. You care about one thing: what actually ships. Every feature is a "
        "bet, so you cut scope to the smallest core that proves the bet and ship THAT first. You think in tradeoffs "
        "and MVPs — 'what's the smallest thing that's real?' — and you're allergic to gold-plating and roadmap "
        "theater. Pragmatic, craft-driven, calm. You'll tell the operator when an idea is secretly two ideas, or "
        "when 'v1' is really v3. You push toward a concrete artifact, not a plan about a plan."
    ),
    "claudia": (
        "You're the operator's guardian. Your first instinct is 'what could go wrong, and where's the "
        "exposure?' You protect capital, legality, and safety: you lead with the risk, flag every assumption, and "
        "never speculate on outcomes. On anything legal or financial you open by telling the operator to get real "
        "counsel — you draft, a professional signs off. You treat any unverified figure as unverified and refuse to "
        "let it ride uncaveated. Careful, precise, quietly skeptical — the one who spots the landmine before anyone "
        "steps on it. Never alarmist; always specific about the real exposure and the cheapest way to close it."
    ),
    "azur": (
        "You're the operator's growth engine. You obsess over one scarce resource: attention. Every idea is "
        "judged by 'what earns attention vs wastes it' — the hook, the angle, the channel that compounds. You think "
        "in loops and CAC/payback, not spray-and-pray; you kill an expensive channel without sentiment and double "
        "down on what works. Punchy, creative, a little contrarian — you find the non-obvious wedge. Ground channel "
        "claims in real spend/analytics when connected, and end with the single highest-leverage test to run next."
    ),
    "rosetta": (
        "You're the operator's operator. Your rule: if it needs a hero to work, it's not a system, it's a "
        "liability. You turn chaos into repeatable process, and you weigh people decisions by their long tails — a "
        "wrong hire costs 3x what anyone budgets. Calm, structured, humane. You make invisible operational debt "
        "visible (the thing with no owner, no next step, no cadence) and design the smallest system that removes the "
        "hero. You leave a concrete process or checklist behind, never just advice."
    ),
    # ── RESEARCH CORPS ── read the web, return CITED facts, invent nothing.
    "scout": (
        "You're the operator's researcher. Give them the real, current picture of whatever they ask about — a "
        "company, a topic, a market — pulled from live web search, synthesized into tight facts they can act on. "
        "You lead with the answer, then the few sources it rests on. You never pad, never speculate, and never "
        "state a 'fact' you didn't actually find — if the search comes back thin, you say exactly that."
    ),
    "scan": (
        "You're the operator's market scout. You map a landscape: who the players are, how they position, what the "
        "pricing/GTM signal is, where the gap is. You pull it from live search, name each competitor with the source "
        "that proves it, and end with the one non-obvious opening. No hand-wavy 'the market is growing' — specifics, "
        "cited, or an honest 'couldn't confirm.'"
    ),
    "verify": (
        "You're the operator's fact-checker. You take a claim and you settle it: true, false, or unverifiable — with "
        "the REAL sources that decide it, quoted and linked. You NEVER manufacture a citation; a made-up source is a "
        "firing offense. If the web doesn't support the claim, you say 'unverified' and show what you searched. Your "
        "whole value is that the operator can trust what you return without re-checking it."
    ),
    "watch": (
        "You're the operator's monitor. You answer 'what's new on X' — recent developments, dated, sourced, ordered "
        "newest-first. You separate signal from noise and flag what actually changed vs churn. If nothing material is "
        "new, you say so plainly rather than dress up old news."
    ),
    "enrich": (
        "You're the operator's enrichment desk. Given a company or person, you return real firmographic and contact "
        "facts — size, industry, role, verified contact points — from People Data Labs. You return ONLY what the "
        "source actually has; you never invent an employee count, an email, or a title. Missing field → 'not found,' "
        "never a plausible guess. You hand clean, real data up to whoever asked (a founder, or a leader like Vinny)."
    ),
}


def agent_persona(key):
    """The per-turn persona: NX operating IN this crew role — a DISTINCT specialist voice, never a generic advisor
    and never a renamed assistant. Pairs with the forced home world's objective + the operator's real tools."""
    key = (key or "").lstrip("/").lower()
    name = CANONICAL.get(key, (key.title() or "Agent", ""))[0]
    persona = PERSONAS.get(key)
    if not persona:
        persona = f"You're the operator's {name} specialist."
    return (
        f"{persona}\n\n"
        f"The operator's crew calls this seat \"{name}\" — that is only a label for your role, NOT a product, "
        f"project, company, or the subject of the task; never ask what \"{name}\" is, and never treat your own seat "
        f"name as the thing being discussed. Do not announce or explain your identity — just do the work. The "
        f"operator's message is a task for YOU to handle in this domain. When they ask about their OWN data "
        f"(pipeline, deals, finances, roadmap, customers, channels, etc.), READ it via the connected tools FIRST — "
        f"do NOT ask them to describe what a tool could show you; only ask a question if NO connected tool can "
        f"surface the answer. When you call a tool, give REAL arguments and never guess an argument NAME — if a "
        f"tool returns an argument or validation error, read the EXACT field it says it needs (e.g. Linear wants "
        f"'teamId' not 'team'; Stripe wants a 'resource:query' string) and retry immediately with that field; do "
        f"not give up, re-emit the same wrong call, or ask the operator to do it. Reason from the operator's real "
        f"data, USE the available tools and the shell to actually execute, and produce a concrete result — in your "
        f"own distinct voice, not a neutral assistant tone and not generic steps. When a step belongs to another "
        f"crew seat, name it and hand off. "
        f"HUMAN VOICE (this is the bar): sound like a sharp human operator talking to a peer — NOT an AI assistant. "
        f"Ban the tells: no 'As an AI', no 'I'd be happy to', no 'Certainly!', no 'Great question', no 'Let me…' "
        f"preambles, no 'In conclusion', no hedging throat-clearing, no bulleted filler unless it's genuinely the "
        f"clearest form. Have a point of view, use contractions, be direct, cut the 20%% of words that add nothing. "
        f"If a real operator wouldn't say it out loud to a colleague, don't write it."
        + ((" RESEARCH DISCIPLINE: you READ and RETURN facts and NEVER write / send / pay / delete (your tools are "
            "search-only by construction). Cite the REAL source for every non-obvious claim; if you didn't find it, "
            "say 'not found' — NEVER invent a fact, number, email, or citation (a fabricated source is a firing "
            "offense). Lead with the answer + the sources it rests on; hand the clean result UP to whoever asked.")
           if key in RESEARCHERS else "")
    )


def _fetch_roster(auth_base, token):
    """Return (canon_map, customs). canon_map: {key: {agentId, rank, active, name}}. customs: [ {name, active, …} ].
    Returns (None, None) on auth failure so the caller can prompt sign-in."""
    try:
        st, d = _cd._req("GET", f"{auth_base}/api/agents", token)
    except Exception:
        return {}, []
    if st == 401:
        return None, None
    canon, customs = {}, []
    if st == 200 and isinstance(d, dict):
        for a in (d.get("agents") or []):
            ck = str(a.get("canonicalKey") or "").lower()
            entry = {
                "agentId": a.get("agentId"),
                "rank": str(a.get("rank") or "prospect"),
                "active": bool(a.get("active")),
                "name": a.get("name"),
                "goal": a.get("goal"),  # custom agents carry their own mandate (shown in the crew list)
            }
            if ck in CANONICAL:
                canon[ck] = entry
            else:
                customs.append(entry)
    return canon, customs


def _post(auth_base, token, body):
    try:
        st, d = _cd._req("POST", f"{auth_base}/api/agents", token, body=body)
        return st, (d if isinstance(d, dict) else {})
    except Exception:
        return 0, {}


def _live_names(canon, customs):
    names = [CANONICAL[k][0] for k in ORDER if canon.get(k, {}).get("active")]
    names += [str(c.get("name") or "agent") for c in customs if c.get("active")]
    return names


def _run_and_print(auth_base, token, body, name):
    """RUN an agent via /api/agents/run and print the REAL op trace (RUN-IS-REAL) — the ops actually executed."""
    print(f"\n  {DIM}{name} running…{RESET}")
    try:
        st, d = _cd._req("POST", f"{auth_base}/api/agents/run", token, body=body, timeout=120)
    except Exception:
        print(f"  {RED}Couldn't reach {name} right now.{RESET}")
        return
    if st == 401:
        print(f"  {DIM}Session expired — sign in again (/who).{RESET}")
        return
    if not (st == 200 and isinstance(d, dict) and d.get("ok")):
        _msg = (d if isinstance(d, dict) else {}).get("error", "unknown")
        print(f"  {RED}{name} run failed: {_msg}{RESET}")
        return
    res = d.get("result") or {}
    steps = res.get("steps") or []
    world = d.get("worldId", "")
    landed = sum(1 for s in steps if s.get("ok"))

    def _n(cap):
        return sum(1 for s in steps if s.get("ok") and s.get("capability") == cap)

    # A clean, natural summary in the agent's voice — grounded in the real ops it took (not narration).
    bits = []
    n = _n("write_graph_node")
    if n:
        bits.append(f"created {n} node{'s' if n != 1 else ''}" + (f" in {world}" if world else ""))
    n = _n("emit_value_event")
    if n:
        bits.append(f"recorded {n} value event{'s' if n != 1 else ''}")
    n = _n("write_brain")
    if n:
        bits.append(f"captured {n} note{'s' if n != 1 else ''}")
    n = _n("cross_world_signal")
    if n:
        bits.append(f"sent {n} signal{'s' if n != 1 else ''}")
    if _n("read_memory"):
        bits.append("recalled your context")

    hdr = f"\n  {GOLD}✦ {name}{RESET}"
    if world:
        hdr += f"  {DIM}· {world}{RESET}"
    print(hdr)
    for s in steps:
        label = _OP_ACTION.get(s.get("capability", ""), s.get("capability", "?"))
        if s.get("ok"):
            print(f"    {GREEN}●{RESET} {DIM}{label}{RESET}")
        else:
            print(f"    {RED}✗{RESET} {DIM}{label} — {s.get('detail', '') or 'no-op'}{RESET}")
    if bits:
        print(f"  {GOLD}{name}:{RESET} {'; '.join(bits)}.")
    elif not steps:
        print(f"  {GOLD}{name}:{RESET} {DIM}nothing to do ({res.get('haltReason', '')}){RESET}")
    print(f"  {DIM}✓ {landed} real op{'s' if landed != 1 else ''} landed{RESET}\n")


def run_agent_command(key, auth_base, token, task=""):
    """`/vinny <task>` RUNS the agent (RUN-IS-REAL); bare `/vinny` toggles LIVE (adopt-fork on first use)."""
    key = (key or "").lstrip("/").lower()
    if key not in CANONICAL:
        print(f"  {RED}unknown agent: /{key}{RESET}")
        return
    name, mandate = CANONICAL[key]
    if not token or not auth_base:
        print(f"  {DIM}Sign in to summon your crew (see /who).{RESET}")
        return
    if (task or "").strip():
        _run_and_print(auth_base, token, {"key": key, "task": task.strip()}, name)
        return
    canon, _ = _fetch_roster(auth_base, token)
    if canon is None:
        print(f"  {DIM}Session expired — sign in again (/who).{RESET}")
        return
    cur = canon.get(key)
    want_active = not (cur and cur.get("active"))
    st, d = _post(auth_base, token, {"key": key, "active": want_active})
    if st == 401:
        print(f"  {DIM}Session expired — sign in again (/who).{RESET}")
        return
    if not (st in (200, 201) and d.get("ok")):
        print(f"  {RED}Couldn't toggle {name}: {d.get('error', 'unknown')}{RESET}")
        return
    rank = str(d.get("rank") or "prospect")
    if want_active:
        print(f"\n  {GREEN}✦ {name} — LIVE{RESET}  {DIM}({rank}) — {mandate}{RESET}\n")
    else:
        print(f"\n  {DIM}○ {name} — off{RESET}\n")


def _create_flow(auth_base, token):
    """Create-your-own (manual): name + goal → a custom prospect agent, then PROVE it runs (RUN-IS-REAL) before
    calling it ready. Created ≠ proven: the agent shows 🟡 pending until a real run lands, 🟢 proven after."""
    try:
        name = input(f"  {GOLD}New agent — name › {RESET}").strip()
        if not name:
            return
        goal = input(f"  {GOLD}What does {name} do? › {RESET}").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return
    st, d = _post(auth_base, token, {"name": name, "goal": goal})
    if st == 401:
        print(f"  {DIM}Session expired — sign in again (/who).{RESET}")
        return
    if not (st in (200, 201) and d.get("ok")):
        print(f"  {RED}Couldn't create: {d.get('error', 'unknown')}{RESET}")
        return
    disp = d.get("name", name)
    agent_id = d.get("agentId")
    print(f"\n  {GREEN}✦ {disp} created{RESET} {DIM}· LIVE on your crew (prospect) · 🟡 pending{RESET}")
    # PROVE it runs — RUN-IS-REAL — before we call it ready. Never claim proven without a real run.
    print(f"  {DIM}proving {disp} can run…{RESET}")
    try:
        import nx_creator as CR
        v = CR.prove_and_mark_agent(agent_id, name=disp)
    except Exception:
        v = None
    if v is not None and getattr(v, "ready", False):
        print(f"  {GREEN}🟢 proven{RESET} {DIM}— {disp} ran for real (RUN-IS-REAL).{RESET}\n")
    else:
        reason = ""
        try:
            reason = (v.fail or {}).get("detail", "") if v is not None else "no run"
        except Exception:
            reason = ""
        tail = (" (" + reason + ")") if reason else ""
        print(f"  {DIM}🟡 pending — couldn't prove a run yet{tail}. It proves on first real use.{RESET}\n")


def run_crew_command(auth_base, token):
    """`/crew` — interactive crew: 5 presets + create-your-own; active agents pinned at the bottom."""
    if not token or not auth_base:
        print(f"  {DIM}Sign in to summon your crew (see /who).{RESET}")
        return
    while True:
        canon, customs = _fetch_roster(auth_base, token)
        if canon is None:
            print(f"  {DIM}Session expired — sign in again (/who).{RESET}")
            return
        try:
            choice = _crew_menu(canon, customs)
        except Exception:
            # No TTY / prompt_toolkit unavailable — fall back to a printed roster.
            _print_crew(canon, customs)
            return
        if choice is None:
            return
        action, val = choice
        if action == "toggle":
            cur = canon.get(val)
            want = not (cur and cur.get("active"))
            _post(auth_base, token, {"key": val, "active": want})
        elif action == "create":
            _create_flow(auth_base, token)
        # loop: re-fetch + re-render


def _print_crew(canon, customs):
    print(f"\n  {GOLD}CREW{RESET}")
    for key in ORDER:
        name, mandate = CANONICAL[key]
        live = bool(canon.get(key, {}).get("active"))
        badge = f"{GREEN}● LIVE{RESET}" if live else f"{DIM}○ off{RESET}"
        print(f"    {GOLD}{name:<9}{RESET} {badge}  {DIM}{mandate}{RESET}")
    for c in customs:
        nm = str(c.get("name") or "agent")
        cmandate = str(c.get("goal") or "").strip() or "your custom agent"
        cbadge = f"{GREEN}● LIVE{RESET}" if c.get("active") else f"{DIM}○ off{RESET}"
        print(f"    {GOLD}{nm:<9}{RESET} {cbadge}  {DIM}{cmandate}  · created{RESET}")
    live = _live_names(canon, customs)
    print(f"\n  {DIM}ACTIVE: {(', '.join(n + ' LIVE' for n in live)) if live else 'none — /vinny toggles one on'}{RESET}\n")


def _crew_menu(canon, customs):
    """prompt_toolkit picker. Returns ("toggle", key) | ("create", None) | None."""
    from prompt_toolkit.application import Application
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.layout import Layout
    from prompt_toolkit.layout.containers import Window
    from prompt_toolkit.layout.controls import FormattedTextControl
    from prompt_toolkit.styles import Style

    items = []
    for key in ORDER:
        name, mandate = CANONICAL[key]
        entry = canon.get(key)
        items.append({"type": "agent", "key": key, "name": name, "mandate": mandate,
                      "live": bool(entry and entry.get("active")), "rank": str((entry or {}).get("rank") or "prospect")})
    # user-created agents — listed in the MAIN crew like the presets (name · LIVE · their own mandate), not just
    # the ACTIVE footer. Server can't toggle a custom yet, so these are display rows (Enter is a no-op on them).
    for c in customs:
        nm = str(c.get("name") or "agent")
        goal = str(c.get("goal") or "").strip()
        items.append({"type": "custom", "key": str(c.get("agentId") or nm), "name": nm,
                      "mandate": goal or "your custom agent", "live": bool(c.get("active")),
                      "rank": str(c.get("rank") or "prospect")})
    items.append({"type": "create"})

    state = {"selected": 0}

    def menu_text():
        lines = [("class:gold", "\n  CREW\n"), ("class:dim", "  " + "─" * 54 + "\n")]
        for i, it in enumerate(items):
            sel = i == state["selected"]
            if it["type"] in ("agent", "custom"):
                marker = "❯" if sel else " "
                cls = "class:selected" if sel else "class:cmd"
                lines.append((cls, f"  {marker} {it['name']:<10}"))
                lines.append(("class:live" if it["live"] else "class:off", "  ● LIVE" if it["live"] else "  ○ off "))
                lines.append(("class:desc", f"  {it['mandate']}"))
                lines.append(("class:dim", "  · created\n" if it["type"] == "custom" else "\n"))
            else:
                marker = "❯" if sel else " "
                cls = "class:selected" if sel else "class:create"
                lines.append((cls, f"  {marker} ＋ Create your own\n"))
        live = _live_names(canon, customs)
        lines.append(("class:dim", "  " + "─" * 54 + "\n"))
        if live:
            lines.append(("class:gold", "  ACTIVE  "))
            lines.append(("class:live", "  ".join(f"{n} LIVE" for n in live) + "\n"))
        else:
            lines.append(("class:dim", "  ACTIVE  none — toggle an agent to bring it LIVE\n"))
        lines.append(("class:dim", "  ↑↓ navigate   Enter toggle/select   Esc close\n"))
        return lines

    kb = KeyBindings()

    @kb.add("up")
    def _up(event):
        del event
        state["selected"] = (state["selected"] - 1) % len(items)

    @kb.add("down")
    def _down(event):
        del event
        state["selected"] = (state["selected"] + 1) % len(items)

    @kb.add("enter")
    def _enter(event):
        it = items[state["selected"]]
        if it["type"] == "agent":
            event.app.exit(result=("toggle", it["key"]))
        elif it["type"] == "create":
            event.app.exit(result=("create", None))
        # custom agents have no server-side toggle yet — Enter is a gentle no-op; they stay LIVE + listed

    @kb.add("escape")
    @kb.add("q")
    @kb.add("c-c")
    @kb.add("c-d")
    def _close(event):
        event.app.exit(result=None)

    app = Application(
        layout=Layout(Window(content=FormattedTextControl(menu_text, focusable=True))),
        key_bindings=kb,
        style=Style.from_dict({
            "gold": "#c8a44a bold",
            "dim": "#9a958a",
            "cmd": "#d6d2c6",
            "desc": "#b0aa98",
            "selected": "bg:#1a1600 #e8c860 bold",
            "live": "#50c878 bold",
            "off": "#807b70",
            "create": "#c8a44a",
        }),
        full_screen=True,
        mouse_support=False,
    )
    return app.run()
