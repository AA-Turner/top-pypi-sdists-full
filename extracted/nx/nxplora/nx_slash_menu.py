"""
nx_slash_menu.py - NX slash command menu with prompt_toolkit navigation.
"""

from __future__ import annotations

import os
import re
import sys

# POSIX-only raw-mode reads; on Windows we fall back to msvcrt.getwch in
# _read_first_char so the menu still works there.
try:
    import termios  # type: ignore
    import tty      # type: ignore
    _HAVE_TERMIOS = True
except ImportError:
    termios = None  # type: ignore
    tty = None      # type: ignore
    _HAVE_TERMIOS = False

GOLD = "\033[38;2;200;164;74m"
GOLD_DIM = "\033[38;2;120;96;40m"
WHITE = "\033[38;2;220;220;220m"
DIM = "\033[38;2;150;150;150m"
GREEN = "\033[38;2;80;200;120m"
RESET = "\033[0m"

SECTIONS = [
    {
        "title": "COMMANDS",
        "commands": [
            {"cmd": "/help",         "desc": "Show all commands"},
            {"cmd": "/mode",         "desc": "How NX works  Partner · Autopilot · Study · Refine"},
            {"cmd": "/effort",       "desc": "Effort  low · mid · high · extra · council"},
            {"cmd": "/crew",         "desc": "Your agent crew — 5 presets + create your own"},
            {"cmd": "/go",           "desc": "Continue on the go — web · iMessage · Telegram"},
            {"cmd": "/brain",        "desc": "Your company Brain — live context map"},
            {"cmd": "/supply",       "desc": "The agent's own accounts — email · phone · social it acts as"},
            {"cmd": "/takeoff",      "desc": "Dispatch agents on live email duty — reply to people, alert you on system alerts"},
            {"cmd": "/skills",       "desc": "Browse your imported skills"},
            {"cmd": "/create",       "desc": "Skills · commands · MCPs · integrations"},
            {"cmd": "/integrations", "desc": "Browse and connect integrations"},
            {"cmd": "/connected",    "desc": "Show connected integrations"},
            {"cmd": "/publish",      "desc": "Publish out  Meta · Google · TikTok · LinkedIn · X"},
            {"cmd": "/channels",     "desc": "Reach NX besides here  Telegram · WhatsApp · Text · Email"},
            {"cmd": "/message",      "desc": "Where NX reports back  Telegram · WhatsApp · Text · Email"},
            {"cmd": "/save",         "desc": "Save last response"},
            {"cmd": "/resume",       "desc": "Pick up your last conversation"},
            {"cmd": "/login",        "desc": "Re-authenticate without leaving"},
            {"cmd": "/logout",       "desc": "Sign out"},
        ],
    },
]

# ── Modes ────────────────────────────────────────────────────────────────────
# The five Nexplora modes shown in the /mode picker (clean numbered list, like the
# onboarding role picker). The first four are POSTURES that change how NX reasons
# (each is a system-prompt gate in nx_prompts.NX_MODE_GATES); Flight is the born-safe
# autonomy loop that runs a task end-to-end. `short` is the terse label rendered in
# the picker so it never wraps in a narrow terminal; `desc` is the full line.
# Customize ("shape how NX works") is reached via /customize or Settings — not a mode.
MODES = [
    {"name": "Partner",   "kind": "mode",   "short": "think it through",  "desc": "Think it through with you, step by step"},
    {"name": "Autopilot", "kind": "mode",   "short": "handle & report",   "desc": "Go handle it and report back when it's done"},
    {"name": "Study",     "kind": "mode",   "short": "answer with proof", "desc": "Learn from your sources and answer with proof"},
    {"name": "Refine",    "kind": "mode",   "short": "draft & polish",    "desc": "Draft, sharpen, and polish until it's right"},
    {"name": "Customize", "kind": "action", "short": "make it yours",     "desc": "Shape how NX works for you — modes, model, and defaults"},
    {"name": "Flight",    "kind": "action", "short": "run end to end",    "desc": "Run it end to end — autonomous, gated"},
]

# ── Report-back channels (the /message picker) ───────────────────────────────
# The per-operator channels NX can send its reports to. `key` is the internal channel id handled by
# nx_message.handle_message_command.
#
# MUST COVER nx_message.CHANNELS. This list carried only four for a long time while the module supported
# five, so `sms` was configurable by typing `/message sms` but UNREACHABLE from any picker — and the
# /channels hub, which lists all five, offered a row an operator could not act on. A picker that omits a
# real channel is a dead end you only find by already knowing the command.
#
# "Text" is no longer used as a display name: /channels lists SMS and iMessage side by side, so one word
# naming whichever of the two happened to be nearest was a genuine trap. Both are spelled out.
MESSAGE_CHANNELS = [
    {"name": "Telegram", "key": "telegram", "desc": "your bot — NX DMs reports to you"},
    {"name": "iMessage", "key": "imessage", "desc": "Nexplora texts you — iMessage or Android"},
    {"name": "SMS",      "key": "sms",      "desc": "Twilio (BYOK) — texts from your own number"},
    {"name": "Email",    "key": "email",    "desc": "Nexplora emails you — from hello@nexplora.ai"},
    {"name": "WhatsApp", "key": "whatsapp", "desc": "Twilio (BYOK) — reports to your number"},
]

SLASH_COMMANDS = [
    command
    for section in SECTIONS
    for command in section["commands"]
]

# ── World picker — grouped by category ───────────────────────────────────────
# Source of truth for the full set is nx_routing.WORLD_CONFIG / nx_prompts.
# NX_WORLD_CONTEXT (28 worlds, kept in sync by assert_world_registries_consistent
# in nx_routing.py). "lead"/"leads" and "crm" are each their own first-class
# world — NOT aliases of "sales" — with their own tier + context block.
WORLD_GROUPS = [
    {"title": "BUSINESS",          "worlds": ["cowork", "strategy", "finance", "capital", "research", "product"]},
    {"title": "REVENUE",           "worlds": ["sales", "leads", "lead", "crm", "customers", "marketing", "growth", "brand"]},
    {"title": "PEOPLE & OPS",      "worlds": ["hr", "people", "recruiting", "onboarding", "ops", "support", "knowledge"]},
    {"title": "LEGAL & COMPLIANCE","worlds": ["legal", "compliance"]},
    {"title": "TECH",              "worlds": ["code", "devops", "nx-code"]},
    {"title": "AGENT",             "worlds": ["nx-1", "agents"]},
]

SKILLS_SECTIONS = [
    {
        "title": "AUTOMATION",
        "skills": [
            {"cmd": "$browse", "desc": "NX opens a browser + does the task — then send a URL + what to do"},
            {"cmd": "$desktop", "desc": "NX runs desktop missions handed off from the web — polls, then drives your Mac (you approve each action)"},
            {"cmd": "$mission", "desc": "NX runs an autonomous mission (sales · outreach · research) over your integrations + the web — dry-run by default, you authorize live"},
            {"cmd": "$dispatch", "desc": "NX runs a business action — approval-gated (marketing · sales · leads · …)"},
        ],
    },
    {
        "title": "COUNCIL",
        "skills": [
            {"cmd": "$council", "desc": "3-AI council debates your question"},
        ],
    },
    {
        "title": "MEMORY",
        "skills": [
            {"cmd": "$brain", "desc": "Save this to your Nexplora brain"},
            {"cmd": "$brain_search", "desc": "Search your brain for context"},
            {"cmd": "$brain_note", "desc": "Add a note or insight to brain"},
            {"cmd": "$brain_connect", "desc": "Connect two ideas in your brain"},
        ],
    },
    {
        "title": "REVENUE",
        "skills": [
            {"cmd": "$cold_outreach", "desc": "Write cold outreach sequences"},
            {"cmd": "$deal_analysis", "desc": "Analyse deal health and risk"},
            {"cmd": "$lead_qualify", "desc": "Qualify an inbound lead (pass/nurture/AE)"},
            {"cmd": "$objection_handler", "desc": "Handle sales objections"},
            {"cmd": "$pipeline_review", "desc": "Review and prioritise pipeline"},
            {"cmd": "$pricing_model", "desc": "Build pricing model and tiers"},
            {"cmd": "$proposal_writer", "desc": "Write a sales proposal"},
            {"cmd": "$revenue_forecast", "desc": "Forecast revenue by segment"},
            {"cmd": "$win_loss_analysis", "desc": "Analyse win/loss patterns"},
        ],
    },
    {
        "title": "GROWTH",
        "skills": [
            {"cmd": "$campaign_builder", "desc": "Build multi-channel campaign"},
            {"cmd": "$content_calendar", "desc": "Plan content calendar"},
            {"cmd": "$funnel_audit", "desc": "Audit and fix conversion funnel"},
            {"cmd": "$growth_model", "desc": "Model growth levers and impact"},
            {"cmd": "$launch_plan", "desc": "Plan a product or feature launch"},
            {"cmd": "$seo_audit", "desc": "Audit SEO and surface fixes"},
        ],
    },
    {
        "title": "STRATEGY",
        "skills": [
            {"cmd": "$competitive_map", "desc": "Map competitive landscape"},
            {"cmd": "$market_sizing", "desc": "Size a market TAM/SAM/SOM"},
            {"cmd": "$okr_builder", "desc": "Build OKRs for a team or org"},
            {"cmd": "$positioning", "desc": "Define product positioning"},
            {"cmd": "$strategic_plan", "desc": "Write a strategic plan"},
            {"cmd": "$swot_analysis", "desc": "Run a SWOT analysis"},
        ],
    },
    {
        "title": "FINANCE",
        "skills": [
            {"cmd": "$burn_analysis", "desc": "Analyse burn rate and runway"},
            {"cmd": "$financial_model", "desc": "Build a financial model"},
            {"cmd": "$unit_economics", "desc": "Calculate unit economics"},
            {"cmd": "$valuation", "desc": "Estimate company valuation"},
        ],
    },
    {
        "title": "PRODUCT",
        "skills": [
            {"cmd": "$prd_writer", "desc": "Write a product requirements doc"},
            {"cmd": "$roadmap_builder", "desc": "Build a prioritised roadmap"},
            {"cmd": "$user_story", "desc": "Write user stories and ACs"},
            {"cmd": "$feature_spec", "desc": "Spec a feature end to end"},
        ],
    },
    {
        "title": "PEOPLE",
        "skills": [
            {"cmd": "$hiring_plan", "desc": "Build a hiring plan"},
            {"cmd": "$interview_kit", "desc": "Write interview questions"},
            {"cmd": "$job_description", "desc": "Write a job description"},
            {"cmd": "$performance_review", "desc": "Write a performance review"},
            {"cmd": "$onboarding_plan", "desc": "Build an onboarding plan"},
        ],
    },
    {
        "title": "OPS",
        "skills": [
            {"cmd": "$sop_writer", "desc": "Write a standard operating procedure"},
            {"cmd": "$meeting_summary", "desc": "Summarise a meeting"},
            {"cmd": "$project_plan", "desc": "Build a project plan"},
            {"cmd": "$status_report", "desc": "Write a status report"},
        ],
    },
    {
        "title": "LEGAL",
        "skills": [
            {"cmd": "$contract_review", "desc": "Review a contract for risks"},
            {"cmd": "$nda_drafter", "desc": "Draft an NDA"},
            {"cmd": "$terms_summary", "desc": "Summarise terms and conditions"},
        ],
    },
    {
        "title": "CODE",
        "skills": [
            {"cmd": "$code_review", "desc": "Review code for issues"},
            {"cmd": "$debug", "desc": "Debug an error or issue"},
            {"cmd": "$api_spec", "desc": "Write an API specification"},
            {"cmd": "$test_writer", "desc": "Write tests for a function"},
        ],
    },
]


def _all_known_commands() -> list[dict]:
    """Every dispatchable slash-command, so the palette can NEVER say 'No matches' for a command that `/help` lists.
    SINGLE SOURCE: nx_cli.HELP_GROUPS (the authoritative grouped list) + the /worlds footer — read at runtime (nx_cli
    is always loaded during the REPL), so the two lists cannot drift. Falls back to the curated SECTIONS off-REPL."""
    out = list(SLASH_COMMANDS)
    seen = {c["cmd"] for c in out}
    try:
        import nx_cli  # already loaded during the REPL (a no-op re-import); safe + cheap standalone too
        groups = getattr(nx_cli, "HELP_GROUPS", None)
    except Exception:
        groups = None
    if groups:
        for _hdr, cmds in groups:
            for cmd, desc in cmds:
                if cmd not in seen:
                    seen.add(cmd)
                    out.append({"cmd": cmd, "desc": desc})
        if "/worlds" not in seen:  # the /help WORLDS footer — a real, dispatchable command
            out.append({"cmd": "/worlds", "desc": "Switch world — cowork · sales · research · … (28 total)"})
    return out


def filter_commands(query: str) -> list[dict]:
    # strip() BEFORE the empty-check: a whitespace-only query ('  ', tab) is
    # truthy but q.split() is [], so the old `q.split()[0] if q else ""` raised
    # IndexError — reachable live by pressing space twice in the bare / menu.
    q = query.lower().strip().lstrip("/").strip()
    if not q:
        return SLASH_COMMANDS  # empty filter → the curated featured set (default view stays small)
    head = q.split()[0] if q.split() else ""
    # a typed query filters the FULL registry — every /help command is reachable, not just the featured 10.
    return [
        command
        for command in _all_known_commands()
        if q in command["cmd"].lower()
        or q in command["desc"].lower()
        or (head and command["cmd"].lower().lstrip("/").startswith(head))
    ]


def _build_display_items(search: str) -> list[dict]:
    if search:
        return [{"type": "cmd", **command} for command in filter_commands("/" + search)]

    items = []
    for section in SECTIONS:
        items.append({"type": "header", "title": section["title"]})
        for command in section["commands"]:
            items.append({"type": "cmd", **command})
    return items


def _clamp_selection(items: list[dict], selected: int) -> tuple[int, list[int]]:
    cmd_indices = [index for index, item in enumerate(items) if item.get("type") == "cmd"]
    if not cmd_indices:
        return 0, []
    if selected not in cmd_indices:
        return cmd_indices[0], cmd_indices
    return selected, cmd_indices


def _visible_items(items: list[dict], selected: int, limit: int = 20) -> list[dict]:
    if len(items) <= limit:
        return items

    start = max(0, selected - limit + 1)
    max_start = max(0, len(items) - limit)
    start = min(start, max_start)
    return items[start : start + limit]


def _build_menu_text(display_items: list[dict], state: dict, limit: int = 20) -> list[tuple[str, str]]:
    filt = state.get("filter", "")
    # Once the operator types a command token + a space, they're composing ARGS to send (e.g. "/vinny <task>"),
    # not picking a command from the list — drop the "No matches / ↑↓ navigate" picker chrome and show a clean
    # send line so it reads like a normal command being typed.
    if " " in filt:
        return [
            ("class:gold", f"  /{filt}"),
            ("class:dim", "   ↵ send\n"),
        ]
    selected, _ = _clamp_selection(display_items, state.get("selected", 0))
    state["selected"] = selected

    lines: list[tuple[str, str]] = [
        ("class:gold", f"  /{filt}\n"),
        ("class:dim", "  " + "─" * 54 + "\n"),
    ]

    if not display_items:
        lines.append(("class:dim", "  No matches\n"))
    else:
        visible_items = _visible_items(display_items, selected, limit=limit)
        for item in visible_items:
            if item["type"] == "header":
                lines.append(("class:gold", f"  {item['title']}\n"))
                continue

            is_selected = display_items[selected] is item
            cmd_text = item["cmd"][:28]
            desc_text = item.get("desc", "")[:36]
            if is_selected:
                lines.append(("class:selected", f"  ❯ {cmd_text:<28}  {desc_text}\n"))
            else:
                lines.append(("class:dim", f"    {cmd_text:<28}  "))
                lines.append(("class:desc", f"{desc_text}\n"))

    lines.append(("class:dim", "  " + "─" * 54 + "\n"))
    lines.append(("class:dim", "  ↑↓ navigate   Enter select   Esc close   type to filter\n"))
    return lines


def _clean_integration_description(description: str) -> str:
    desc = (description or "").strip()
    desc = desc.split("—")[0].strip()
    desc = desc.split(" - ")[0].strip()
    desc = desc.split("(")[0].strip()
    return desc[:40]


# Pretty labels for channel / commerce rows that key on a lowercase slug and have no personal-connector
# manifest entry (their tools live in the channels / business-os substrate, not /api/personal). Title-case
# is the fallback; this map fixes the ones title-case gets wrong (X, eBay, TikTok, GoHighLevel, LinkedIn…).
_CHANNEL_PRETTY = {
    "x": "X", "ebay": "eBay", "tiktok": "TikTok", "gohighlevel": "GoHighLevel",
    "linkedin": "LinkedIn", "openai": "OpenAI", "paypal": "PayPal", "youtube": "YouTube",
    "googleworkspace": "Google Workspace", "google": "Google", "meta": "Meta",
    "pinterest": "Pinterest", "snapchat": "Snapchat", "amazon": "Amazon", "shopify": "Shopify",
    "quickbooks": "QuickBooks", "bigquery": "BigQuery", "circleci": "CircleCI", "pagerduty": "PagerDuty",
    "clickup": "ClickUp", "sourcegraph": "Sourcegraph", "webflow": "Webflow", "wix": "Wix",
}


# Services that connect via ONE vendor OAuth app (server-side /api/oauth/initiate aliases them). They COLLAPSE into a
# single menu row per vendor — one Google grant powers Gmail+Drive+Docs+Sheets+…; one Microsoft grant powers the M365
# suite. So the menu shows "Google" and "Microsoft 365", not 20 per-service rows.
_GOOGLE_FAMILY = {
    "gmail", "google-drive", "google-calendar", "google-docs", "google-sheets", "google-chat",
    "google-meet", "google-forms", "google-tasks", "bigquery",
}
_MICROSOFT_FAMILY = {
    "outlook", "outlook-calendar", "teams", "excel", "word", "powerpoint", "onenote", "onedrive",
    "sharepoint", "bookings",
}
_ATLASSIAN_FAMILY = {"confluence", "jira", "trello"}   # already covered by the "Atlassian" MCP row — don't duplicate
_VENDOR_OAUTH_SLUGS = _GOOGLE_FAMILY | _MICROSOFT_FAMILY | _ATLASSIAN_FAMILY


def _build_integrations_menu_items(
    registry: dict,
    active_world: str = "cowork",
    query: str = "",
) -> list[dict]:
    by_world: dict[str, list[tuple[str, dict]]] = {}
    query_text = query.lower().strip()

    def _norm(s: str) -> str:
        # collapse slug/name spelling differences: "hugging-face"=="huggingface", "google_workspace"=="googleworkspace"
        return "".join(ch for ch in str(s).lower() if ch.isalnum())

    # The manifest = the REAL personal-connector set (provider slug + op list + pretty name/category).
    try:
        import nx_tool_manifest as _ntm_all
        _mani_conns = (_ntm_all.load_manifest() or {}).get("connectors") or []
    except Exception:
        _mani_conns = []
    # Index by NORMALIZED key (slug AND pretty name) → real op count + pretty name. This is what lets a
    # directory row whose slug is spelled differently than the connector still resolve its true count.
    _mani_idx: dict[str, dict] = {}
    for _c in _mani_conns:
        _p = _c.get("provider", "")
        _cnt = len(_c.get("actions", []) or [])
        _nm = _c.get("name") or _p
        for _k in {_norm(_p), _norm(_nm)}:
            if _k:
                _mani_idx.setdefault(_k, {"count": _cnt, "name": _nm, "slug": _p})

    _slug_alias = {"atlassian": "jira", "monday-com": "monday"}
    _alias_norm = {_norm(v) for v in _slug_alias.values()}  # jira/googledrive/monday already shown via a directory row

    # --- directory / channel / commerce / oauth rows (the passed-in registry) ---
    # Each stays LABELLED under its world(s), but the menu lists EVERY world's set (every connector is global,
    # connectable from any world). Resolve each row's REAL op count from the manifest (normalized) so a built
    # connector shows its count even when the directory spells the slug differently; and upgrade an ugly
    # lowercase/slug display name to the manifest's pretty name. `_reg_norm` then guards the merge from dup-listing.
    _reg_norm: set = set()
    for name, mcp in registry.items():
        # The stale third-party-MCP google-drive / google-workspace registry rows (npx *-mcp servers) are
        # superseded by the native Google connectors. They collapse into the single "Google Workspace"
        # vendor row below — skip here so they neither render as duplicate rows nor shadow its tool count.
        if name in ("google-drive", "google-workspace"):
            continue
        worlds = mcp.get("worlds", [])
        if not worlds:
            continue
        if query_text:
            haystacks = [name.lower(), mcp.get("description", "").lower()]
            if not any(query_text in value for value in haystacks):
                continue
        _slug = mcp.get("slug", "")
        _reg_norm.add(_norm(_slug))
        _reg_norm.add(_norm(name))
        _hit = (_mani_idx.get(_norm(_slug_alias.get(_slug, _slug)))
                or _mani_idx.get(_norm(_slug))
                or _mani_idx.get(_norm(name)))
        _mcp2 = dict(mcp)
        _mcp2["slug"] = mcp.get("slug") or name   # registry rows: explicit slug, else the key IS the slug
        if _hit:
            _mcp2["tools_count"] = _hit["count"]
        _disp = name
        if _hit and _hit["name"] and (name.islower() or name == _slug):
            _disp = _hit["name"]  # "sendgrid" -> "SendGrid", "shopify" -> "Shopify"
        elif name.islower():
            # channel / commerce rows key on a lowercase slug and have no manifest connector — prettify the label
            _disp = _CHANNEL_PRETTY.get(_norm(name), name.replace("_", " ").replace("-", " ").title())
        by_world.setdefault(worlds[0], []).append((_disp, _mcp2))

    # --- every manifest connector NOT already represented above (deduped by normalized slug OR name) ---
    _google_tools = 0  # collapse Google / Microsoft 365 per-service connectors into ONE vendor row each
    _ms_tools = 0
    _ads_yt_tools = 0  # YouTube (+ Google Ads) → a SEPARATE "Google (Ads + YouTube)" row (narrower scopes than Workspace)
    for _c in _mani_conns:
        _cslug = _c.get("provider", "")
        _cname = _c.get("name") or _cslug
        if not _cslug:
            continue
        if (_norm(_cslug) in _reg_norm or _norm(_cname) in _reg_norm
                or _norm(_cslug) in _alias_norm):
            continue  # already listed as a directory/commerce/oauth row — keep that one
        # ONE Google / ONE Microsoft 365 / ONE Atlassian — a single OAuth grant covers every service, so fold the
        # per-service connectors into one vendor row (sum their tool counts) instead of 20 separate rows.
        # These folds run BEFORE the per-connector query filter on purpose: a folded service never renders as its
        # own row, so filtering it individually here would undercount the vendor row AND drop it entirely when the
        # query is not a literal substring of a member slug — typing "goo"/"google" dropped Gmail+BigQuery (162→134)
        # and dropped YouTube outright (no Ads+YouTube row). The collapsed rows apply the query themselves at emit
        # time against the vendor's full keyword bag, so a search always surfaces the vendor with its FULL count.
        if _cslug in _GOOGLE_FAMILY:
            _google_tools += len(_c.get("actions", []) or [])
            continue
        if _cslug in ("youtube", "google_ads", "google-ads"):
            _ads_yt_tools += len(_c.get("actions", []) or [])
            continue
        if _cslug in _MICROSOFT_FAMILY:
            _ms_tools += len(_c.get("actions", []) or [])
            continue
        if _cslug in _ATLASSIAN_FAMILY:
            continue  # the "Atlassian" MCP row already covers Jira / Confluence / Trello
        # non-folded connector: it renders as its OWN row, so filter it individually by slug/name substring.
        if query_text and query_text not in _cname.lower() and query_text not in _cslug.lower():
            continue
        _ccat = (_c.get("category") or "MORE").lower()
        _ctier = "dcr" if _c.get("auth") == "oauth" else "token"  # oauth → sign in · byok → paste your key
        # Broken-remote-MCP OAuth services with no OAuth app yet (gitlab/bitbucket/hootsuite): show
        # "coming soon" — they sign in, they don't paste a key, and the app isn't provisioned. See MCP_COMING_SOON.
        try:
            import nx_mcp_oauth as _mcpo_fk
            if _cslug in _mcpo_fk.MCP_COMING_SOON:
                _ctier = "soon"
        except Exception:
            pass
        by_world.setdefault(_ccat, []).append((_cname, {
            "worlds": [_ccat], "tier": _ctier, "tools_count": len(_c.get("actions", []) or []),
            "description": f"your own {_cname} account", "slug": _cslug,
        }))

    # the collapsed vendor rows — connecting once grants the whole suite (slug routes to the vendor OAuth app).
    # Each row carries a keyword bag covering ALL its member services so a search ("goo"/"google"/"gmail"/"drive"/
    # "youtube"/"ads"/"outlook"/"teams"/"excel") surfaces the vendor row with its FULL tool count. "google"/"goo"
    # is in BOTH Google bags on purpose — searching Google shows Workspace AND Ads+YouTube; "gmail" shows only
    # Workspace; "youtube"/"ads" shows only Ads+YouTube.
    def _vendor_matches(keywords: str) -> bool:
        return (not query_text) or (query_text in keywords)

    if _google_tools and _vendor_matches(
            "google workspace googleworkspace gmail drive calendar docs sheets slides meet forms tasks chat bigquery"):
        by_world.setdefault("productivity", []).append(("Google Workspace", {
            "worlds": ["productivity"], "tier": "oauth", "tools_count": _google_tools,
            "description": "Gmail · Drive · Calendar · Docs · Sheets · Meet & more — one sign-in", "slug": "google_workspace",
        }))
    if _ads_yt_tools and _vendor_matches("google ads googleads adwords youtube video marketing"):
        by_world.setdefault("marketing", []).append(("Google (Ads + YouTube)", {
            "worlds": ["marketing"], "tier": "oauth", "tools_count": _ads_yt_tools,
            "description": "YouTube + Google Ads — one sign-in (separate scopes from Workspace)", "slug": "google",
        }))
    if _ms_tools and _vendor_matches(
            "microsoft 365 microsoft365 m365 outlook teams excel word powerpoint onedrive sharepoint office"):
        by_world.setdefault("productivity", []).append(("Microsoft 365", {
            "worlds": ["productivity"], "tier": "oauth", "tools_count": _ms_tools,
            "description": "Outlook · Teams · Excel · Word · OneDrive · SharePoint & more — one sign-in", "slug": "outlook",
        }))

    worlds = sorted(by_world.keys())
    if active_world in worlds:
        worlds.remove(active_world)
        worlds = [active_world] + worlds

    items: list[dict] = []
    for world in worlds:
        items.append({"type": "header", "title": world.upper()})
        for name, mcp in sorted(by_world[world], key=lambda item: item[0].lower()):
            items.append(
                {
                    "type": "integration",
                    "name": name,
                    "slug": mcp.get("slug", ""),   # the connector SLUG — connect routing keys on this, not the label
                    "tools": mcp.get("tools_count", 0),
                    "tier": mcp.get("tier"),
                    "desc": _clean_integration_description(mcp.get("description", "")),
                }
            )

    return items


def _clamp_integration_selection(items: list[dict], selected: int) -> tuple[int, list[int]]:
    indices = [index for index, item in enumerate(items) if item.get("type") == "integration"]
    if not indices:
        return 0, []
    if selected not in indices:
        return indices[0], indices
    return selected, indices


def _window_by_lines(display_items: list[dict], selected: int, limit: int) -> tuple[list[dict], int, bool]:
    """Scroll-window display_items by RENDERED-LINE budget, not item count.

    A category header renders as two lines ("\\n  Title\\n"), so a count-based
    window overflows a short pane and prompt_toolkit clips the bottom — the
    selected row and the footer simply vanish (the "Rippling disappears at the
    end" bug). Budgeting by line keeps `selected` and the footer on screen no
    matter how many headers land in the window.

    Returns (visible_items, start_index, at_end).
    """
    if not display_items:
        return [], 0, True
    selected = max(0, min(selected, len(display_items) - 1))
    costs = [2 if it.get("type") == "header" else 1 for it in display_items]
    budget = max(3, limit)
    start = selected
    used = costs[selected]
    above_room = budget // 2  # keep a little context above the selection
    i = selected - 1
    while i >= 0 and used + costs[i] <= above_room:
        used += costs[i]
        start = i
        i -= 1
    # snap the top up to a category header when it still fits the budget
    while (start > 0 and display_items[start].get("type") != "header"
           and used + costs[start - 1] <= budget):
        used += costs[start - 1]
        start -= 1
    # fill downward with whatever budget remains
    end = selected + 1
    used = sum(costs[start:end])
    while end < len(display_items) and used + costs[end] <= budget:
        used += costs[end]
        end += 1
    return display_items[start:end], start, end >= len(display_items)


def _build_integrations_menu_text(
    display_items: list[dict],
    state: dict,
    total_integrations: int,
    total_tools: int,
    limit: int = 20,
) -> list[tuple[str, str]]:
    selected, _ = _clamp_integration_selection(display_items, state.get("selected", 0))
    state["selected"] = selected

    lines: list[tuple[str, str]] = [("class:gold", "  INTEGRATIONS")]
    if state.get("filter"):
        lines.append(("class:gold", f"  · {state['filter']}"))
    lines.append(("class:gold", "\n"))
    lines.append(("class:dim", "  " + "─" * 56 + "\n"))

    if not display_items:
        lines.append(("class:dim", "  No matches\n"))
    else:
        visible_items, start, at_end = _window_by_lines(display_items, selected, limit)

        for offset, item in enumerate(visible_items, start=start):
            if item["type"] == "header":
                lines.append(("class:gold", f"\n  {item['title']}\n"))
                continue

            name = item["name"][:22]
            tier = item.get("tier")
            is_selected = offset == selected
            if tier:
                # Show the connect METHOD: OAuth (sign in) vs a pasted personal URL
                # (Zapier) vs a pasted PAT/API key (token).
                # OAuth tiers: dcr (MCP sign-in), oauth (commerce/SP-API), channel (social).
                if tier == "soon":
                    badge = "coming soon"
                elif tier in ("dcr", "oauth", "channel"):
                    badge = "sign in"
                elif tier == "url":
                    badge = "paste url"
                else:
                    badge = "api key"
                tools = item.get("tools", 0)
                # Show the real tool count alongside the connect method for EVERY connector (sign in / api key /
                # paste url) — "19 tools · api key" reads the same weight as "19 tools · sign in", so api-key rows
                # don't look empty next to the OAuth ones. The label states HOW you connect; the count states WHAT.
                meta = f"{tools} tools · {badge}" if tools else badge
                desc = item["desc"][:30]
                if is_selected:
                    lines.append(("class:current", f"  ❯ {name:<22}{meta:>20}   {desc}\n"))
                else:
                    lines.append(("class:dim", f"    {name:<22}{meta:>20}   "))
                    lines.append(("class:desc", f"{desc}\n"))
            else:
                # npx marketplace fallback: original tool-count format (unchanged)
                tools = item["tools"]
                desc = item["desc"][:36]
                if is_selected:
                    lines.append(("class:current", f"  ❯ {name:<22}{tools:>6} tools   {desc}\n"))
                else:
                    lines.append(("class:dim", f"    {name:<22}{tools:>6} tools   "))
                    lines.append(("class:desc", f"{desc}\n"))

    # End-of-list affordance: when the list is scrolled, say plainly whether
    # there's more below or this is the end — so the bottom (e.g. Rippling) is
    # unmistakably the last item, not a vanished cursor.
    if display_items and len(visible_items) < len(display_items):
        lines.append(("class:dim", "  · end of list ·\n" if at_end else "  ↓ more below\n"))
    lines.append(("class:dim", "\n  " + "─" * 56 + "\n"))
    if total_tools:
        lines.append(("class:dim", f"  {total_integrations} integrations  {total_tools:,} tools\n"))
    else:
        lines.append(("class:dim", f"  {total_integrations} integrations  ·  sign in or your token, no secret\n"))
    lines.append(("class:dim", "  ↑↓ scroll   Enter connect   Esc close   type to filter\n"))
    return lines


def run_integrations_menu(registry: dict, active_world: str = "cowork") -> str | None:
    """
    Interactive integration picker using prompt_toolkit.
    Arrow keys navigate. Enter selects. Esc cancels.
    Returns the chosen integration name or None.
    """
    # Always show FRESH data: a long-running session caches the manifest at startup, so the picker
    # could otherwise render a stale connector set (missing youtube, wrong tool counts) even after an
    # upgrade. Force a re-fetch on every open so /integrations is never stale.
    try:
        import nx_tool_manifest as _ntm_fresh
        _ntm_fresh.load_manifest(force=True)
    except Exception:
        pass

    from prompt_toolkit.application import Application
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.layout import Layout
    from prompt_toolkit.layout.containers import Window
    from prompt_toolkit.layout.controls import FormattedTextControl
    from prompt_toolkit.styles import Style

    # Count from the ACTUAL built item set (directory + all merged personal connectors), not just `registry` —
    # otherwise the footer says "69 integrations" while the list shows 137.
    _all_built = [it for it in _build_integrations_menu_items(registry, active_world=active_world, query="")
                  if it.get("type") == "integration"]
    total_integrations = len(_all_built)
    total_tools = sum(int(it.get("tools", 0) or 0) for it in _all_built)
    state = {"selected": 0, "filter": "", "result": None}

    def display_items() -> list[dict]:
        return _build_integrations_menu_items(registry, active_world=active_world, query=state["filter"])

    def menu_text() -> list[tuple[str, str]]:
        # Size the scroll window to the ACTUAL terminal height — a fixed 20-row
        # window overflows a short pane and prompt_toolkit clips the bottom
        # (can't scroll past it). Leave ~8 rows for header + footer + prompt.
        import shutil
        rows = shutil.get_terminal_size((80, 24)).lines
        # `limit` is now a RENDERED-LINE budget for the item region (see
        # _window_by_lines). Reserve ~10 rows for header + end-marker + footer +
        # prompt so the bottom never clips.
        limit = max(6, rows - 10)
        return _build_integrations_menu_text(
            display_items(),
            state,
            total_integrations=total_integrations,
            total_tools=total_tools,
            limit=limit,
        )

    def _reset_selected() -> None:
        state["selected"], _ = _clamp_integration_selection(display_items(), state["selected"])

    kb = KeyBindings()

    @kb.add("up")
    def _up(event):
        del event
        current, indices = _clamp_integration_selection(display_items(), state["selected"])
        state["selected"] = current
        previous = [index for index in indices if index < current]
        if previous:
            state["selected"] = previous[-1]

    @kb.add("down")
    def _down(event):
        del event
        current, indices = _clamp_integration_selection(display_items(), state["selected"])
        state["selected"] = current
        following = [index for index in indices if index > current]
        if following:
            state["selected"] = following[0]

    @kb.add("enter")
    def _enter(event):
        items = display_items()
        current, _ = _clamp_integration_selection(items, state["selected"])
        if items and 0 <= current < len(items) and items[current].get("type") == "integration":
            # Return the connector SLUG (connect routing keys on it), not the display label.
            state["result"] = items[current].get("slug") or items[current]["name"]
        event.app.exit(result=state["result"])

    @kb.add("escape")
    def _escape(event):
        event.app.exit(result=None)

    @kb.add("backspace")
    def _backspace(event):
        del event
        state["filter"] = state["filter"][:-1]
        _reset_selected()

    @kb.add("<any>")
    def _any(event):
        text = event.data or ""
        if len(text) == 1 and text.isprintable():
            state["filter"] += text
            _reset_selected()

    app = Application(
        layout=Layout(Window(content=FormattedTextControl(menu_text, focusable=True))),
        key_bindings=kb,
        style=Style.from_dict(
            {
                "gold": "#c8a44a bold",
                "dim": "#9a958a",
                "desc": "#b0aa98",
                "current": "#ffffff bold",
            }
        ),
        full_screen=True,
        mouse_support=True,
    )

    return app.run()


def run_mode_menu(current_mode: str = "") -> str | None:
    """Clean numbered 5-mode picker (Partner · Autopilot · Study · Refine · Flight),
    laid out like the onboarding role picker — press 1-5 to jump-select, or ↑↓+Enter.
    Returns the chosen name (e.g. 'Partner', 'Flight') or None."""
    from prompt_toolkit.application import Application
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.layout import Layout
    from prompt_toolkit.layout.containers import Window
    from prompt_toolkit.layout.controls import FormattedTextControl
    from prompt_toolkit.styles import Style

    def _user_modes():
        # User-authored modes (/create → Mode) from ~/.nx/modes/*.json, surfaced
        # below the built-in five. Each carries its own behavior overlay ("prompt").
        import glob as _g, os as _os, json as _j
        out = []
        try:
            for _f in sorted(_g.glob(_os.path.join(_os.path.expanduser("~"), ".nx", "modes", "*.json"))):
                try:
                    _d = _j.load(open(_f))
                    if _d.get("name"):
                        out.append({"name": _d["name"], "kind": "user",
                                    "short": _d.get("short") or _d.get("desc", ""),
                                    "desc": _d.get("desc", ""), "prompt": _d.get("prompt", "")})
                except Exception:
                    pass
        except Exception:
            pass
        return out
    _modes = list(MODES) + _user_modes()

    state = {"selected": 0, "result": None}
    # Normalize so a legacy stored value (e.g. "PEER") still pre-selects the right
    # posture (Partner) instead of falling back to the first item.
    try:
        from nx_prompts import normalize_mode as _nm
        cur = _nm(current_mode) if current_mode else ""
    except Exception:
        cur = (current_mode or "").upper()
    # pre-select current mode (names are Title-case; normalized mode is UPPER)
    for idx, m in enumerate(_modes):
        if m["name"].upper() == cur:
            state["selected"] = idx
            break

    def menu_text() -> list[tuple[str, str]]:
        sel = state["selected"]
        lines: list[tuple[str, str]] = [
            ("class:gold",  "  MODE\n"),
            ("class:dim",   "  " + "─" * 30 + "\n"),
        ]
        # Clean numbered list (matches the onboarding role picker's 1-N layout).
        for idx, m in enumerate(_modes):
            n = idx + 1
            name = m["name"]
            short = m.get("short") or m["desc"]
            active = bool(cur) and (name.upper() == cur)   # the currently-set mode — marked with a ● dot
            dot = "●" if active else " "
            if idx == sel:
                lines.append(("class:selected", f"  ❯ {n} {dot} {name:<9} {short}\n"))
            else:
                lines.append(("class:dim",      f"    {n} "))
                lines.append(("class:gold" if active else "class:dim", f"{dot} "))
                lines.append(("class:dim",      f"{name:<9} "))
                lines.append(("class:desc",     f"{short}\n"))
        lines.append(("class:dim", "  " + "─" * 30 + "\n"))
        lines.append(("class:dim", "  Customize NX in /customize · Settings\n"))
        lines.append(("class:dim", "  ● current · ↑↓ · 1-5 jump · Enter · Esc\n"))
        return lines

    kb = KeyBindings()

    @kb.add("up")
    def _up(event):
        state["selected"] = max(0, state["selected"] - 1)

    @kb.add("down")
    def _down(event):
        state["selected"] = min(len(_modes) - 1, state["selected"] + 1)

    @kb.add("enter")
    def _enter(event):
        state["result"] = _modes[state["selected"]]["name"]
        event.app.exit(result=state["result"])

    @kb.add("escape")
    def _escape(event):
        event.app.exit(result=None)

    @kb.add("c-c")
    def _ctrl_c(event):
        event.app.exit(result=None)

    # Press 1-9 to jump straight to a mode and select it (like the role picker's [1-5]).
    def _make_jump(i):
        def _jump(event):
            if 0 <= i < len(_modes):
                state["selected"] = i
                state["result"] = _modes[i]["name"]
                event.app.exit(result=state["result"])
        return _jump
    for _i in range(min(9, len(_modes))):
        kb.add(str(_i + 1))(_make_jump(_i))

    app = Application(
        layout=Layout(Window(content=FormattedTextControl(menu_text, focusable=True))),
        key_bindings=kb,
        style=Style.from_dict({
            "gold":     "#c8a44a bold",
            "dim":      "#9a958a",
            "desc":     "#b0aa98",
            "selected": "bg:#1a1600 #e8c860 bold",
        }),
        full_screen=False,
        mouse_support=False,
    )
    return app.run()


def run_effort_menu(current: str = "") -> str | None:
    """Effort-level picker (Auto · Low · Mid · High · Extra · Council) — same numbered
    up/down + 1-N layout as run_mode_menu. Returns the chosen level lowercase
    ('high', 'auto', ...) or None. The terminal form of the web effort bar."""
    from prompt_toolkit.application import Application
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.layout import Layout
    from prompt_toolkit.layout.containers import Window
    from prompt_toolkit.layout.controls import FormattedTextControl
    from prompt_toolkit.styles import Style

    _levels = [
        {"key": "auto",    "name": "Auto",    "short": "Nexplora picks per task"},
        {"key": "low",     "name": "Low",     "short": "fast, cheapest"},
        {"key": "mid",     "name": "Mid",     "short": "balanced"},
        {"key": "high",    "name": "High",    "short": "deeper reasoning"},
        {"key": "extra",   "name": "Extra",   "short": "maximum reasoning"},
        {"key": "council", "name": "Council", "short": "multi-voice debate"},
    ]
    cur = (current or "auto").strip().lower()
    state = {"selected": 0, "result": None}
    for idx, lv in enumerate(_levels):
        if lv["key"] == cur:
            state["selected"] = idx
            break

    def menu_text() -> list[tuple[str, str]]:
        sel = state["selected"]
        lines: list[tuple[str, str]] = [
            ("class:gold", "  EFFORT\n"),
            ("class:dim",  "  " + "─" * 30 + "\n"),
        ]
        for idx, lv in enumerate(_levels):
            n = idx + 1
            active = (lv["key"] == cur)   # the currently-set effort — marked with a ● dot
            dot = "●" if active else " "
            if idx == sel:
                lines.append(("class:selected", f"  ❯ {n} {dot} {lv['name']:<9} {lv['short']}\n"))
            else:
                lines.append(("class:dim",  f"    {n} "))
                lines.append(("class:gold" if active else "class:dim", f"{dot} "))
                lines.append(("class:dim",  f"{lv['name']:<9} "))
                lines.append(("class:desc", f"{lv['short']}\n"))
        lines.append(("class:dim", "  " + "─" * 30 + "\n"))
        lines.append(("class:dim", "  ● current · ↑↓ · 1-6 jump · Enter · Esc\n"))
        return lines

    kb = KeyBindings()

    @kb.add("up")
    def _up(event):
        state["selected"] = max(0, state["selected"] - 1)

    @kb.add("down")
    def _down(event):
        state["selected"] = min(len(_levels) - 1, state["selected"] + 1)

    @kb.add("enter")
    def _enter(event):
        state["result"] = _levels[state["selected"]]["key"]
        event.app.exit(result=state["result"])

    @kb.add("escape")
    def _escape(event):
        event.app.exit(result=None)

    @kb.add("c-c")
    def _ctrl_c(event):
        event.app.exit(result=None)

    def _make_jump(i):
        def _jump(event):
            if 0 <= i < len(_levels):
                state["selected"] = i
                state["result"] = _levels[i]["key"]
                event.app.exit(result=state["result"])
        return _jump
    for _i in range(min(9, len(_levels))):
        kb.add(str(_i + 1))(_make_jump(_i))

    app = Application(
        layout=Layout(Window(content=FormattedTextControl(menu_text, focusable=True))),
        key_bindings=kb,
        style=Style.from_dict({
            "gold":     "#c8a44a bold",
            "dim":      "#9a958a",
            "desc":     "#b0aa98",
            "selected": "bg:#1a1600 #e8c860 bold",
        }),
        full_screen=False,
        mouse_support=False,
    )
    return app.run()


def run_choice_menu(title: str, options: list, current: int = 0) -> "int | None":
    """Generic arrow-key picker — the same ↑↓ · 1-9 jump · Enter · Esc feel as run_mode_menu /
    run_effort_menu, but for any ad-hoc list. `options` is a list of {"label": str, "hint"?: str}
    (or plain strings). Returns the selected index, or None on Esc/Ctrl-C. Raises if
    prompt_toolkit / a TTY isn't usable — callers fall back to numbered input()."""
    from prompt_toolkit.application import Application
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.layout import Layout
    from prompt_toolkit.layout.containers import Window
    from prompt_toolkit.layout.controls import FormattedTextControl
    from prompt_toolkit.styles import Style

    opts = []
    for o in (options or []):
        if isinstance(o, dict):
            opts.append({"label": str(o.get("label", "")), "hint": str(o.get("hint", ""))})
        else:
            opts.append({"label": str(o), "hint": ""})
    if not opts:
        return None
    W = max(8, min(28, max((len(o["label"]) for o in opts), default=8)))
    state = {"selected": max(0, min(int(current or 0), len(opts) - 1))}

    def menu_text() -> list:
        sel = state["selected"]
        lines = [("class:gold", f"  {title}\n"), ("class:dim", "  " + "─" * 34 + "\n")]
        for idx, o in enumerate(opts):
            marker = f"{idx + 1}  " if idx < 9 else "   "
            if idx == sel:
                lines.append(("class:selected", f"  ❯ {marker}{o['label']:<{W}} {o['hint']}\n"))
            else:
                lines.append(("class:dim", f"    {marker}{o['label']:<{W}} "))
                lines.append(("class:desc", f"{o['hint']}\n"))
        lines.append(("class:dim", "  " + "─" * 34 + "\n"))
        lines.append(("class:dim", "  ↑↓ · 1-9 jump · Enter · Esc\n"))
        return lines

    kb = KeyBindings()

    @kb.add("up")
    def _up(event):
        state["selected"] = max(0, state["selected"] - 1)

    @kb.add("down")
    def _down(event):
        state["selected"] = min(len(opts) - 1, state["selected"] + 1)

    @kb.add("enter")
    def _enter(event):
        event.app.exit(result=state["selected"])

    @kb.add("escape")
    def _escape(event):
        event.app.exit(result=None)

    @kb.add("c-c")
    def _ctrl_c(event):
        event.app.exit(result=None)

    def _make_jump(i):
        def _jump(event):
            if 0 <= i < len(opts):
                event.app.exit(result=i)
        return _jump
    for _i in range(min(9, len(opts))):
        kb.add(str(_i + 1))(_make_jump(_i))

    app = Application(
        layout=Layout(Window(content=FormattedTextControl(menu_text, focusable=True))),
        key_bindings=kb,
        style=Style.from_dict({
            "gold":     "#c8a44a bold",
            "dim":      "#9a958a",
            "desc":     "#b0aa98",
            "selected": "bg:#1a1600 #e8c860 bold",
        }),
        full_screen=False,
        mouse_support=False,
    )
    return app.run()


def run_message_menu(states: dict | None = None) -> str | None:
    """Report-back channel picker for /message. `states` = {channel_key: {configured, active}}
    (from nx_message.channels_state) to mark which are set/on. Returns the chosen channel key
    (telegram/whatsapp/imessage/email) or None."""
    from prompt_toolkit.application import Application
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.layout import Layout
    from prompt_toolkit.layout.containers import Window
    from prompt_toolkit.layout.controls import FormattedTextControl
    from prompt_toolkit.styles import Style

    states = states or {}
    state = {"selected": 0, "result": None}

    def menu_text() -> list[tuple[str, str]]:
        sel = state["selected"]
        lines: list[tuple[str, str]] = [
            ("class:gold", "  MESSAGE — where NX reports back\n"),
            ("class:dim",  "  " + "─" * 54 + "\n"),
        ]
        for idx, ch in enumerate(MESSAGE_CHANNELS):
            st = states.get(ch["key"], {})
            mark = "● on " if st.get("active") else (" · set" if st.get("configured") else "     ")
            name, desc = ch["name"], ch["desc"]
            if idx == sel:
                lines.append(("class:selected", f"  ❯ {name:<10} {mark:<6}  {desc}\n"))
            else:
                lines.append(("class:dim",  f"    {name:<10} {mark:<6}  "))
                lines.append(("class:desc", f"{desc}\n"))
        lines.append(("class:dim", "  " + "─" * 54 + "\n"))
        lines.append(("class:dim", "  Enter to set up / configure that channel\n"))
        lines.append(("class:dim", "  ↑↓ navigate   Enter select   Esc close\n"))
        return lines

    kb = KeyBindings()

    @kb.add("up")
    def _up(event):
        state["selected"] = max(0, state["selected"] - 1)

    @kb.add("down")
    def _down(event):
        state["selected"] = min(len(MESSAGE_CHANNELS) - 1, state["selected"] + 1)

    @kb.add("enter")
    def _enter(event):
        state["result"] = MESSAGE_CHANNELS[state["selected"]]["key"]
        event.app.exit(result=state["result"])

    @kb.add("escape")
    def _escape(event):
        event.app.exit(result=None)

    @kb.add("c-c")
    def _ctrl_c(event):
        event.app.exit(result=None)

    app = Application(
        layout=Layout(Window(content=FormattedTextControl(menu_text, focusable=True))),
        key_bindings=kb,
        style=Style.from_dict({
            "gold":     "#c8a44a bold",
            "dim":      "#9a958a",
            "desc":     "#b0aa98",
            "selected": "bg:#1a1600 #e8c860 bold",
        }),
        full_screen=False,
        mouse_support=False,
    )
    return app.run()


# ── /create menu ─────────────────────────────────────────────────────────────
_CREATE_ITEMS = [
    {"cmd": "create",    "desc": "Build a new skill · command · MCP"},
    {"cmd": "installed", "desc": "Browse skills · commands · integrations"},
]


def run_create_menu() -> str | None:
    """Two-item picker: 'create' or 'installed'. Returns the choice or None."""
    from prompt_toolkit.application import Application
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.layout import Layout
    from prompt_toolkit.layout.containers import Window
    from prompt_toolkit.layout.controls import FormattedTextControl
    from prompt_toolkit.styles import Style

    state = {"selected": 0, "result": None}

    def menu_text() -> list[tuple[str, str]]:
        sel = state["selected"]
        lines: list[tuple[str, str]] = [
            ("class:gold", "  CREATE\n"),
            ("class:dim",  "  " + "─" * 54 + "\n"),
        ]
        for idx, item in enumerate(_CREATE_ITEMS):
            cmd  = f"/{item['cmd']}"
            desc = item["desc"]
            if idx == sel:
                lines.append(("class:selected", f"  ❯ {cmd:<16}  {desc}\n"))
            else:
                lines.append(("class:dim",      f"    {cmd:<16}  "))
                lines.append(("class:desc",     f"{desc}\n"))
        lines.append(("class:dim", "  " + "─" * 54 + "\n"))
        lines.append(("class:dim", "  ↑↓ navigate   Enter select   Esc close\n"))
        return lines

    kb = KeyBindings()

    @kb.add("up")
    def _up(event):
        state["selected"] = max(0, state["selected"] - 1)

    @kb.add("down")
    def _down(event):
        state["selected"] = min(len(_CREATE_ITEMS) - 1, state["selected"] + 1)

    @kb.add("enter")
    def _enter(event):
        state["result"] = _CREATE_ITEMS[state["selected"]]["cmd"]
        event.app.exit(result=state["result"])

    @kb.add("escape")
    def _escape(event):
        event.app.exit(result=None)

    @kb.add("c-c")
    def _ctrl_c(event):
        event.app.exit(result=None)

    app = Application(
        layout=Layout(Window(content=FormattedTextControl(menu_text, focusable=True))),
        key_bindings=kb,
        style=Style.from_dict({
            "gold":     "#c8a44a bold",
            "dim":      "#9a958a",
            "desc":     "#b0aa98",
            "selected": "bg:#1a1600 #e8c860 bold",
        }),
        full_screen=False,
        mouse_support=False,
    )
    return app.run()


# ── /publish — clean numbered picker of the publish connectors + Assign ──────
def run_publish_menu(states):
    """Clean numbered /publish picker: the publish connectors with a status glyph,
    plus an 'Assign agents' row. `states` = [{name, display, glyph}]. Press 1-N to jump.
    Returns a channel name, '__assign__', or None.

    NAMED /publish, not /channels. This surface publishes OUT to an audience; the
    web has always called the other direction — the ways to reach Nexplora — its
    Channels surface, and one word meaning opposite things on the two surfaces
    misleads whichever operator learned the other one first."""
    from prompt_toolkit.application import Application
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.layout import Layout
    from prompt_toolkit.layout.containers import Window
    from prompt_toolkit.layout.controls import FormattedTextControl
    from prompt_toolkit.styles import Style

    items = list(states) + [
        {"name": "__assign__", "display": "Assign agents to a channel", "glyph": "+"},
        {"name": "__report__", "display": "Report — agent activity across all channels", "glyph": "/"},
    ]
    state = {"selected": 0, "result": None}

    def menu_text() -> list[tuple[str, str]]:
        sel = state["selected"]
        lines: list[tuple[str, str]] = [
            ("class:gold", "  PUBLISH\n"),
            ("class:dim",  "  " + "─" * 34 + "\n"),
        ]
        for idx, it in enumerate(items):
            n = idx + 1
            row = f"{it.get('glyph', '·')} {it['display']}"
            if idx == sel:
                lines.append(("class:selected", f"  ❯ {n:>2}  {row}\n"))
            else:
                lines.append(("class:dim",      f"    {n:>2}  {row}\n"))
        lines.append(("class:dim", "  " + "─" * 34 + "\n"))
        lines.append(("class:dim", "  ● connected  ◐ configured  ○ off · Enter · Esc\n"))
        return lines

    kb = KeyBindings()

    @kb.add("up")
    def _up(event):
        state["selected"] = max(0, state["selected"] - 1)

    @kb.add("down")
    def _down(event):
        state["selected"] = min(len(items) - 1, state["selected"] + 1)

    @kb.add("enter")
    def _enter(event):
        state["result"] = items[state["selected"]]["name"]
        event.app.exit(result=state["result"])

    @kb.add("escape")
    def _escape(event):
        event.app.exit(result=None)

    @kb.add("c-c")
    def _ctrl_c(event):
        event.app.exit(result=None)

    def _make_jump(i):
        def _jump(event):
            if 0 <= i < len(items):
                state["result"] = items[i]["name"]
                event.app.exit(result=state["result"])
        return _jump
    for _i in range(min(9, len(items))):
        kb.add(str(_i + 1))(_make_jump(_i))

    app = Application(
        layout=Layout(Window(content=FormattedTextControl(menu_text, focusable=True))),
        key_bindings=kb,
        style=Style.from_dict({
            "gold":     "#c8a44a bold",
            "dim":      "#9a958a",
            "desc":     "#b0aa98",
            "selected": "bg:#1a1600 #e8c860 bold",
        }),
        full_screen=False,
        mouse_support=False,
    )
    return app.run()


# ── /supply hub — give an agent its own channel (send AS that agent) ─────────
# Two kinds, and the difference is what the operator actually gets:
#   conversation — the agent sends to a person and can be replied to; /takeoff can put it on duty
#   publishing   — the agent posts to an audience; nothing comes back, so there is no duty to be on
# Order MUST match lib/desk/supply-channels.ts on the web. Operators read a numbered list positionally,
# so interleaving a channel silently renumbers every one below it on one surface and not the other.
_SUPPLY_ITEMS = [
    {"cmd": "email",     "name": "Email",     "desc": "send as the agent",              "kind": "conversation"},
    {"cmd": "telegram",  "name": "Telegram",  "desc": "the agent's own bot",            "kind": "conversation"},
    {"cmd": "sms",       "name": "SMS",       "desc": "the agent's number",             "kind": "conversation"},
    {"cmd": "whatsapp",  "name": "WhatsApp",  "desc": "business number",                "kind": "conversation"},
    {"cmd": "imessage",  "name": "iMessage",  "desc": "mac only — sends from this Mac", "kind": "conversation"},
    {"cmd": "discord",   "name": "Discord",   "desc": "the agent's own bot",            "kind": "conversation"},
    {"cmd": "x",         "name": "X",         "desc": "post as the agent — paid API",   "kind": "publishing"},
    {"cmd": "facebook",  "name": "Facebook",  "desc": "post to a Page",                 "kind": "publishing"},
    {"cmd": "instagram", "name": "Instagram", "desc": "post to a business account",     "kind": "publishing"},
    {"cmd": "linkedin",  "name": "LinkedIn",  "desc": "post as a company page",         "kind": "publishing"},
    {"cmd": "tiktok",    "name": "TikTok",    "desc": "post to an account",             "kind": "publishing"},
    {"cmd": "youtube",   "name": "YouTube",   "desc": "post to a channel",              "kind": "publishing"},
    {"cmd": "pinterest", "name": "Pinterest", "desc": "pin from an account",            "kind": "publishing"},
    {"cmd": "active",    "name": "Active",    "desc": "agents + channels",              "kind": "manage"},
    {"cmd": "revoke",    "name": "Revoke",    "desc": "remove a channel",               "kind": "manage"},
]

# Rendered above the first item of each kind. Headers are DRAWN, never selectable — they must not shift
# the numbering, or the digit an operator presses stops matching the row they are looking at.
_SUPPLY_GROUPS = [
    ("conversation", "the agent sends, and can be replied to"),
    ("publishing",   "the agent posts — one-way, nothing comes back"),
    ("manage",       ""),
]


def run_supply_menu() -> str | None:
    """The /supply hub — give one of your agents its own account so NX sends AS that agent.

    Two groups, matching the web: CONVERSATION (Email · Telegram · SMS · WhatsApp · iMessage · Discord)
    where the agent can be replied to, and PUBLISHING (X · Facebook · Instagram · LinkedIn · TikTok ·
    YouTube · Pinterest) where it posts one-way. Then Active · Revoke.

    Numbered list; 1-9 jump, arrows reach the rest. Returns the key or None."""
    from prompt_toolkit.application import Application
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.layout import Layout
    from prompt_toolkit.layout.containers import Window
    from prompt_toolkit.layout.controls import FormattedTextControl
    from prompt_toolkit.styles import Style

    items = _SUPPLY_ITEMS
    state = {"selected": 0, "result": None}

    def menu_text() -> list[tuple[str, str]]:
        sel = state["selected"]
        lines: list[tuple[str, str]] = [
            ("class:gold", "  SUPPLY\n"),
            ("class:dim",  "  " + "─" * 30 + "\n"),
        ]
        seen_kinds: set[str] = set()
        for idx, it in enumerate(items):
            n = idx + 1
            kind = it.get("kind", "")
            if kind and kind not in seen_kinds:
                seen_kinds.add(kind)
                note = dict(_SUPPLY_GROUPS).get(kind, "")
                if note:
                    lines.append(("class:desc", f"\n    {kind.upper()}  {note}\n"))
                else:
                    lines.append(("class:desc", "\n"))
            # Numbers past 9 are shown but NOT bound to a key (prompt_toolkit has no "10"), so they are
            # dimmed differently — a number that looks pressable and isn't is worse than no number.
            mark = f"{n}" if n <= 9 else "·"
            if idx == sel:
                lines.append(("class:selected", f"  ❯ {mark}  {it['name']:<10} {it['desc']}\n"))
            else:
                lines.append(("class:dim",  f"    {mark}  {it['name']:<10} "))
                lines.append(("class:desc", f"{it['desc']}\n"))
        lines.append(("class:dim", "  " + "─" * 30 + "\n"))
        lines.append(("class:dim", "  give an agent its own channel · 1-9 or ↑↓ · Enter · Esc\n"))
        return lines

    kb = KeyBindings()

    @kb.add("up")
    def _up(event):
        state["selected"] = max(0, state["selected"] - 1)

    @kb.add("down")
    def _down(event):
        state["selected"] = min(len(items) - 1, state["selected"] + 1)

    @kb.add("enter")
    def _enter(event):
        state["result"] = items[state["selected"]]["cmd"]
        event.app.exit(result=state["result"])

    @kb.add("escape")
    def _escape(event):
        event.app.exit(result=None)

    @kb.add("c-c")
    def _ctrl_c(event):
        event.app.exit(result=None)

    def _make_jump(i):
        def _jump(event):
            if 0 <= i < len(items):
                state["result"] = items[i]["cmd"]
                event.app.exit(result=state["result"])
        return _jump
    # BOUNDED AT 9 — there is no key "10". prompt_toolkit raises on kb.add("10"),
    # and the /supply caller wraps this in a bare `except Exception`, so a 10th
    # item would not traceback: the picker would silently render nothing and drop
    # the operator back at the prompt. Every other picker in this file already
    # bounds the same way; these two were the exceptions. Items past 9 stay
    # reachable by arrow keys.
    for _i in range(min(9, len(items))):
        kb.add(str(_i + 1))(_make_jump(_i))

    app = Application(
        layout=Layout(Window(content=FormattedTextControl(menu_text, focusable=True))),
        key_bindings=kb,
        style=Style.from_dict({
            "gold":     "#c8a44a bold",
            "dim":      "#9a958a",
            "desc":     "#b0aa98",
            "selected": "bg:#1a1600 #e8c860 bold",
        }),
        full_screen=False,
        mouse_support=False,
    )
    return app.run()


# ── /create hub — pick what to build (all saved under the operator's "/") ────
_CREATE_TYPE_ITEMS = [
    {"cmd": "skill",       "name": "Skill",       "desc": "shapes NX's output"},
    {"cmd": "mode",        "name": "Mode",        "desc": "your way NX works"},
    {"cmd": "agent",       "name": "Agent",       "desc": "a crew member"},
    {"cmd": "integration", "name": "Integration", "desc": "connect an app"},
    {"cmd": "channel",     "name": "Channel",     "desc": "publish + report"},
    {"cmd": "installed",   "name": "Browse",      "desc": "what you've made"},
]


def run_create_type_menu() -> str | None:
    """The /create hub — pick what to build: skill · mode · agent · integration ·
    channel · (browse). Clean numbered list; press 1-6 to jump. Returns the key or None."""
    from prompt_toolkit.application import Application
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.layout import Layout
    from prompt_toolkit.layout.containers import Window
    from prompt_toolkit.layout.controls import FormattedTextControl
    from prompt_toolkit.styles import Style

    items = _CREATE_TYPE_ITEMS
    state = {"selected": 0, "result": None}

    def menu_text() -> list[tuple[str, str]]:
        sel = state["selected"]
        lines: list[tuple[str, str]] = [
            ("class:gold", "  CREATE\n"),
            ("class:dim",  "  " + "─" * 30 + "\n"),
        ]
        for idx, it in enumerate(items):
            n = idx + 1
            if idx == sel:
                lines.append(("class:selected", f"  ❯ {n}  {it['name']:<12} {it['desc']}\n"))
            else:
                lines.append(("class:dim",  f"    {n}  {it['name']:<12} "))
                lines.append(("class:desc", f"{it['desc']}\n"))
        lines.append(("class:dim", "  " + "─" * 30 + "\n"))
        lines.append(("class:dim", "  saved under your /   ·   1-6 · Enter · Esc\n"))
        return lines

    kb = KeyBindings()

    @kb.add("up")
    def _up(event):
        state["selected"] = max(0, state["selected"] - 1)

    @kb.add("down")
    def _down(event):
        state["selected"] = min(len(items) - 1, state["selected"] + 1)

    @kb.add("enter")
    def _enter(event):
        state["result"] = items[state["selected"]]["cmd"]
        event.app.exit(result=state["result"])

    @kb.add("escape")
    def _escape(event):
        event.app.exit(result=None)

    @kb.add("c-c")
    def _ctrl_c(event):
        event.app.exit(result=None)

    def _make_jump(i):
        def _jump(event):
            if 0 <= i < len(items):
                state["result"] = items[i]["cmd"]
                event.app.exit(result=state["result"])
        return _jump
    # BOUNDED AT 9 — there is no key "10". prompt_toolkit raises on kb.add("10"),
    # and the /supply caller wraps this in a bare `except Exception`, so a 10th
    # item would not traceback: the picker would silently render nothing and drop
    # the operator back at the prompt. Every other picker in this file already
    # bounds the same way; these two were the exceptions. Items past 9 stay
    # reachable by arrow keys.
    for _i in range(min(9, len(items))):
        kb.add(str(_i + 1))(_make_jump(_i))

    app = Application(
        layout=Layout(Window(content=FormattedTextControl(menu_text, focusable=True))),
        key_bindings=kb,
        style=Style.from_dict({
            "gold":     "#c8a44a bold",
            "dim":      "#9a958a",
            "desc":     "#b0aa98",
            "selected": "bg:#1a1600 #e8c860 bold",
        }),
        full_screen=False,
        mouse_support=False,
    )
    return app.run()


# ── /create → mode picker (chat vs manual) ──────────────────────────────────
_CREATE_MODE_ITEMS = [
    {"cmd": "chat",   "desc": "NX asks what it should do — builds it with you"},
    {"cmd": "manual", "desc": "Fill in every field yourself, step by step"},
]


def run_create_mode_menu() -> str | None:
    """Picker: 'chat' or 'manual'. Returns the choice or None."""
    from prompt_toolkit.application import Application
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.layout import Layout
    from prompt_toolkit.layout.containers import Window
    from prompt_toolkit.layout.controls import FormattedTextControl
    from prompt_toolkit.styles import Style

    state = {"selected": 0, "result": None}

    def menu_text() -> list[tuple[str, str]]:
        sel = state["selected"]
        lines: list[tuple[str, str]] = [
            ("class:gold", "  HOW TO CREATE\n"),
            ("class:dim",  "  " + "─" * 54 + "\n"),
        ]
        for idx, item in enumerate(_CREATE_MODE_ITEMS):
            cmd  = item["cmd"]
            desc = item["desc"]
            if idx == sel:
                lines.append(("class:selected", f"  ❯ {cmd:<10}  {desc}\n"))
            else:
                lines.append(("class:dim",      f"    {cmd:<10}  "))
                lines.append(("class:desc",     f"{desc}\n"))
        lines.append(("class:dim", "  " + "─" * 54 + "\n"))
        lines.append(("class:dim", "  ↑↓ navigate   Enter select   Esc close\n"))
        return lines

    kb = KeyBindings()

    @kb.add("up")
    def _up(event):
        state["selected"] = max(0, state["selected"] - 1)

    @kb.add("down")
    def _down(event):
        state["selected"] = min(len(_CREATE_MODE_ITEMS) - 1, state["selected"] + 1)

    @kb.add("enter")
    def _enter(event):
        state["result"] = _CREATE_MODE_ITEMS[state["selected"]]["cmd"]
        event.app.exit(result=state["result"])

    @kb.add("escape")
    def _escape(event):
        event.app.exit(result=None)

    @kb.add("c-c")
    def _ctrl_c(event):
        event.app.exit(result=None)

    app = Application(
        layout=Layout(Window(content=FormattedTextControl(menu_text, focusable=True))),
        key_bindings=kb,
        style=Style.from_dict({
            "gold":     "#c8a44a bold",
            "dim":      "#9a958a",
            "desc":     "#b0aa98",
            "selected": "bg:#1a1600 #e8c860 bold",
        }),
        full_screen=False,
        mouse_support=False,
    )
    return app.run()


def _world_menu_rows() -> list[dict]:
    """Flatten WORLD_GROUPS into header + world rows for the picker."""
    rows: list[dict] = []
    for group in WORLD_GROUPS:
        rows.append({"type": "header", "title": group["title"]})
        for name in group["worlds"]:
            rows.append({"type": "world", "name": name})
    return rows


def _world_menu_lines(rows: list[dict], cur: str, selected: int, limit: int) -> list[tuple[str, str]]:
    """Pure render of the world picker → prompt_toolkit (style, text) tuples.

    Two things this gets right that the old inline render didn't:
      1. The active-world dot is a SEPARATE gold style-fragment, never raw ANSI
         embedded in the text. prompt_toolkit renders escape bytes inside a
         (style, text) tuple LITERALLY — the "^[[38;2;200;164;74m●^[[0m" leak at
         the top of the list. A styled fragment renders as an actual gold dot.
      2. It scroll-windows by rendered-line budget (via _window_by_lines, the same
         helper the integrations/skills pickers use) so the SELECTED row always
         stays on screen. The old render drew every row unwindowed, so on a short
         pane the viewport never followed the cursor — arrow past the fold and the
         selection "vanished" and the list wouldn't scroll.
    """
    lines: list[tuple[str, str]] = [
        ("class:gold", "  WORLD\n"),
        ("class:dim",  "  " + "─" * 54 + "\n"),
    ]
    visible, start, at_end = _window_by_lines(rows, selected, limit)
    for offset, row in enumerate(visible, start=start):
        if row["type"] == "header":
            lines.append(("class:gold", f"\n  {row['title']}\n"))
            continue
        name = row["name"]
        is_active = name == cur
        is_sel = offset == selected
        row_style = "class:selected" if is_sel else "class:dim"
        lines.append((row_style, "  ❯ " if is_sel else "    "))
        if is_active:
            # gold dot when active; on the selected row it rides the highlight style
            lines.append((row_style if is_sel else "class:gold", "● "))
        else:
            lines.append((row_style, "  "))
        lines.append((row_style, f"{name}\n"))
    # End-of-list affordance so the bottom group (AGENT) is unmistakably the last
    # item, not a vanished cursor — mirrors the integrations picker.
    if len(visible) < len(rows):
        lines.append(("class:dim", "  · end of list ·\n" if at_end else "  ↓ more below\n"))
    lines.append(("class:dim", "\n  " + "─" * 54 + "\n"))
    if cur:
        lines.append(("class:gold", f"  active: {cur}\n"))
    lines.append(("class:dim", "  ↑↓ navigate   Enter select   Esc close\n"))
    return lines


def run_world_menu(current_world: str = "") -> str | None:
    """Grouped 28-world picker (6 categories). Returns the chosen world name
    (e.g. 'crm') or None. 'lead' and 'crm' are listed as their own entries —
    each is a first-class world in WORLD_CONFIG/NX_WORLD_CONTEXT, not an
    alias of 'sales'."""
    from prompt_toolkit.application import Application
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.layout import Layout
    from prompt_toolkit.layout.containers import Window
    from prompt_toolkit.layout.controls import FormattedTextControl
    from prompt_toolkit.styles import Style

    rows = _world_menu_rows()
    world_indices = [i for i, r in enumerate(rows) if r["type"] == "world"]
    cur = (current_world or "").strip().lower()

    state = {"selected": world_indices[0] if world_indices else 0}
    for i in world_indices:
        if rows[i]["name"] == cur:
            state["selected"] = i
            break

    def menu_text() -> list[tuple[str, str]]:
        # Size the scroll window to the ACTUAL terminal height (like the
        # integrations picker) — a fixed full render clips the bottom on a short
        # pane. `limit` is a rendered-line budget; reserve ~10 rows for the WORLD
        # header, end-marker, active line + footer so the bottom never clips.
        import shutil
        term_rows = shutil.get_terminal_size((80, 24)).lines
        limit = max(6, term_rows - 10)
        return _world_menu_lines(rows, cur, state["selected"], limit)

    kb = KeyBindings()

    @kb.add("up")
    def _up(event):
        del event
        earlier = [i for i in world_indices if i < state["selected"]]
        if earlier:
            state["selected"] = earlier[-1]

    @kb.add("down")
    def _down(event):
        del event
        later = [i for i in world_indices if i > state["selected"]]
        if later:
            state["selected"] = later[0]

    @kb.add("enter")
    def _enter(event):
        event.app.exit(result=rows[state["selected"]]["name"])

    @kb.add("escape")
    def _escape(event):
        event.app.exit(result=None)

    @kb.add("c-c")
    def _ctrl_c(event):
        event.app.exit(result=None)

    app = Application(
        layout=Layout(Window(content=FormattedTextControl(menu_text, focusable=True))),
        key_bindings=kb,
        style=Style.from_dict({
            "gold":     "#c8a44a bold",
            "dim":      "#9a958a",
            "desc":     "#b0aa98",
            "selected": "bg:#1a1600 #e8c860 bold",
        }),
        full_screen=True,
        mouse_support=False,
    )
    return app.run()


def _run_prompt_toolkit_menu(world: str) -> str | None:
    del world

    from prompt_toolkit.application import Application
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.layout import Layout
    from prompt_toolkit.layout.containers import Window
    from prompt_toolkit.layout.controls import FormattedTextControl
    from prompt_toolkit.styles import Style

    initial_items = _build_display_items("")
    cmd_indices = [index for index, item in enumerate(initial_items) if item.get("type") == "cmd"]
    state = {
        "selected": cmd_indices[0] if cmd_indices else 0,
        "filter": "",
        "result": None,
    }

    def display_items() -> list[dict]:
        return _build_display_items(state["filter"])

    def menu_text() -> list[tuple[str, str]]:
        items = display_items()
        return _build_menu_text(items, state)

    kb = KeyBindings()

    @kb.add("up")
    def _up(event):
        del event
        items = display_items()
        current, cmd_indices = _clamp_selection(items, state["selected"])
        state["selected"] = current
        previous = [index for index in cmd_indices if index < current]
        if previous:
            state["selected"] = previous[-1]

    @kb.add("down")
    def _down(event):
        del event
        items = display_items()
        current, cmd_indices = _clamp_selection(items, state["selected"])
        state["selected"] = current
        following = [index for index in cmd_indices if index > current]
        if following:
            state["selected"] = following[0]

    @kb.add("enter")
    def _enter(event):
        items = display_items()
        current, _ = _clamp_selection(items, state["selected"])
        if items and 0 <= current < len(items):
            item = items[current]
            if item.get("type") == "cmd":
                # The HIGHLIGHTED command always wins: arrow-navigate to /integrations then
                # press Enter runs /integrations — NOT the partial "/in" typed to filter.
                # (Previously the typed filter overrode the highlight, so a filtered pick
                # submitted the raw text and dispatched as "unknown: /in — /help".)
                state["result"] = item["cmd"]
            elif state["filter"]:
                state["result"] = "/" + state["filter"]
        elif state["filter"]:
            state["result"] = "/" + state["filter"]
        event.app.exit(result=state["result"])

    @kb.add("escape")
    def _escape(event):
        event.app.exit(result=None)

    @kb.add("c-c")
    def _ctrl_c(event):
        state["result"] = "/exit"
        event.app.exit(result=state["result"])

    @kb.add("backspace")
    def _backspace(event):
        # When there's nothing typed after the "/", the only character left is the "/" trigger itself — so backspace
        # deletes IT: close the menu and return to an empty input line (previously this was a no-op and the "/" +
        # menu stayed stuck on screen).
        if not state["filter"]:
            event.app.exit(result=None)
            return
        state["filter"] = state["filter"][:-1]
        state["selected"], _ = _clamp_selection(display_items(), state["selected"])

    @kb.add("<any>")
    def _any(event):
        text = event.data or ""
        if len(text) == 1 and text.isprintable() and text != "/":
            state["filter"] += text
            state["selected"], _ = _clamp_selection(display_items(), state["selected"])

    app = Application(
        layout=Layout(Window(content=FormattedTextControl(menu_text, focusable=True))),
        key_bindings=kb,
        style=Style.from_dict(
            {
                "gold": "#c8a44a bold",
                "dim": "#9a958a",                       # readable, not the old #383828 murk
                "desc": "#b0aa98",                      # readable command descriptions
                "cmd": "#d6d2c6",                       # near-white command names
                "selected": "bg:#1a1600 #e8c860 bold",  # clear highlight on the active row
            }
        ),
        full_screen=False,
        # Wipe the inline menu render when the app exits — otherwise the "No matches / ↑↓ navigate" footer is left
        # on screen and the reply prints UNDER it. With this, the picker vanishes the moment a command is sent.
        erase_when_done=True,
        mouse_support=False,
    )

    return app.run()


def _user_skills_section() -> dict | None:
    """Load user-created skills from ~/.nx/skills/*.json into a section dict."""
    import json as _json
    import pathlib as _pl
    skills_dir = _pl.Path.home() / ".nx" / "skills"
    if not skills_dir.exists():
        return None
    skills = []
    for path in sorted(skills_dir.glob("*.json")):
        if path.name in ("manifest.json", "summary.json"):
            continue
        try:
            with open(path) as fh:
                d = _json.load(fh)
            if d.get("cmd"):
                skills.append({"cmd": d["cmd"], "desc": d.get("desc", "")})
        except Exception:
            pass
    if not skills:
        return None
    return {"title": "MY SKILLS", "skills": skills}


def _bundled_skills_sections() -> list[dict]:
    """The 108 gate-proven, clean-room NX-native skills (nx_bundled_skills.BUNDLED_SKILLS), grouped by
    department for the /skills menu — surfaced under '<DEPT> · NX' headers below the featured catalog."""
    try:
        from nx_bundled_skills import BUNDLED_SKILLS
    except Exception:
        return []
    by_dept: dict[str, list] = {}
    for name, d in BUNDLED_SKILLS.items():
        dept = (d.get("dept") or d.get("world") or "skills").upper()
        by_dept.setdefault(dept, []).append({"cmd": "$" + name, "desc": d.get("desc", "")})
    return [
        {"title": f"{dept} · NX", "skills": sorted(by_dept[dept], key=lambda s: s["cmd"])}
        for dept in sorted(by_dept)
    ]


def _build_skills_display_items(search: str) -> list[dict]:
    query = search.lower().strip()
    items: list[dict] = []

    all_sections = list(SKILLS_SECTIONS)  # the featured WEB section ($browse) is first by construction
    user_section = _user_skills_section()
    if user_section:
        # keep the featured top section (WEB · $browse) pinned at the very top; the operator's own imported
        # skills come right after it, then the rest of the catalog.
        all_sections = all_sections[:1] + [user_section] + all_sections[1:]
    all_sections = all_sections + _bundled_skills_sections()  # 108 gate-proven NX-native skills, by dept

    for section in all_sections:
        matches = section["skills"]
        if query:
            matches = [
                skill
                for skill in section["skills"]
                if query in skill["cmd"].lower() or query in skill["desc"].lower()
            ]
            if not matches:
                continue

        items.append({"type": "header", "title": section["title"]})
        for skill in matches:
            items.append({"type": "skill", **skill})

    return items


def _clamp_skill_selection(items: list[dict], selected: int) -> tuple[int, list[int]]:
    skill_indices = [index for index, item in enumerate(items) if item.get("type") == "skill"]
    if not skill_indices:
        return 0, []
    if selected not in skill_indices:
        return skill_indices[0], skill_indices
    return selected, skill_indices


def _build_skills_menu_text(display_items: list[dict], state: dict, limit: int = 0) -> list[tuple[str, str]]:
    # limit=0 → size the visible window to the terminal height so the FULL catalog is browsable (all 106
    # bundled NX skills + the operator's own, grouped by department) instead of a fixed 20-line slice. The
    # window still follows the selection via _window_by_lines, so a short terminal scrolls smoothly through
    # every skill; a tall terminal shows them all at once.
    if not limit:
        try:
            import shutil
            rows = shutil.get_terminal_size((80, 24)).lines
        except Exception:
            rows = 24
        # reserve ~7 lines for the header/search/footer chrome; never below 20, and cap the render cost so a
        # huge terminal doesn't rebuild thousands of lines per keystroke.
        limit = max(20, min(len(display_items) * 2 + 4, rows - 7))
    selected, _ = _clamp_skill_selection(display_items, state.get("selected", 0))
    state["selected"] = selected

    lines: list[tuple[str, str]] = []

    # Visible search bar at top — like Codex
    search_display = state["filter"] if state["filter"] else ""
    lines.append(("class:gold", "  SKILLS\n"))
    lines.append(("class:dim", "  " + "─" * 54 + "\n"))
    lines.append(("class:searchbar", f"  🔍  {search_display}▌\n"))
    lines.append(("class:dim", "  " + "─" * 54 + "\n"))

    skill_idx = [i for i, it in enumerate(display_items) if it.get("type") == "skill"]
    total_skills = len(skill_idx)
    cur_pos = (skill_idx.index(selected) + 1) if selected in skill_idx else 0

    if not display_items:
        lines.append(("class:dim", "  No matches\n"))
    else:
        visible_items, start, _at_end = _window_by_lines(display_items, selected, limit)
        end = start + len(visible_items)
        hidden_above = sum(1 for i in skill_idx if i < start)
        hidden_below = sum(1 for i in skill_idx if i >= end)

        if hidden_above:
            lines.append(("class:dim", f"  ▲ {hidden_above} more above · ↑ scroll\n"))
        for offset, item in enumerate(visible_items, start=start):
            if item["type"] == "header":
                lines.append(("class:section", f"\n  {item['title']}\n"))
                continue

            cmd_text = item["cmd"][:26]
            desc_text = item.get("desc", "")[:40]
            if offset == selected:
                lines.append(("class:selected", f"  ❯ {cmd_text:<26}  {desc_text}\n"))
            else:
                lines.append(("class:cmd", f"    {cmd_text:<26}"))
                lines.append(("class:desc", f"  {desc_text}\n"))
        if hidden_below:
            lines.append(("class:dim", f"  ▼ {hidden_below} more below · ↓ scroll\n"))

    lines.append(("class:dim", "\n  " + "─" * 54 + "\n"))
    # Show the total so it's unambiguous the FULL catalog is here (all bundled NX skills + your own),
    # not a truncated slice — this is what makes "where are my other skills?" answerable at a glance.
    footer = (
        f"  {cur_pos} / {total_skills} skills   ·   ↑↓ scroll   Enter activate   type to filter   Esc close\n"
        if total_skills
        else "  ↑↓ navigate   Enter activate   q / Esc / ^C close\n"
    )
    lines.append(("class:dim", footer))
    return lines


def run_skills_menu(active_world: str = "cowork") -> str | None:
    """
    $ skills picker organized by operating section.
    Returns the chosen skill command or None.
    """
    del active_world

    from prompt_toolkit.application import Application
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.layout import Layout
    from prompt_toolkit.layout.containers import Window
    from prompt_toolkit.layout.controls import FormattedTextControl
    from prompt_toolkit.styles import Style

    initial_items = _build_skills_display_items("")
    skill_indices = [index for index, item in enumerate(initial_items) if item.get("type") == "skill"]
    state = {
        "selected": skill_indices[0] if skill_indices else 0,
        "filter": "",
        "result": None,
    }

    def display_items() -> list[dict]:
        return _build_skills_display_items(state["filter"])

    def menu_text() -> list[tuple[str, str]]:
        return _build_skills_menu_text(display_items(), state)

    def _reset_selected() -> None:
        state["selected"], _ = _clamp_skill_selection(display_items(), state["selected"])

    kb = KeyBindings()

    @kb.add("up")
    def _up(event):
        del event
        current, skill_positions = _clamp_skill_selection(display_items(), state["selected"])
        state["selected"] = current
        previous = [index for index in skill_positions if index < current]
        if previous:
            state["selected"] = previous[-1]

    @kb.add("down")
    def _down(event):
        del event
        current, skill_positions = _clamp_skill_selection(display_items(), state["selected"])
        state["selected"] = current
        following = [index for index in skill_positions if index > current]
        if following:
            state["selected"] = following[0]

    @kb.add("enter")
    def _enter(event):
        items = display_items()
        current, _ = _clamp_skill_selection(items, state["selected"])
        if items and 0 <= current < len(items) and items[current].get("type") == "skill":
            state["result"] = items[current]["cmd"]
        event.app.exit(result=state["result"])

    @kb.add("escape")
    def _escape(event):
        event.app.exit(result=None)

    @kb.add("c-c")
    @kb.add("c-d")
    def _cancel(event):
        # Ctrl+C / Ctrl+D always back out cleanly — the operator is never forced
        # to pick a skill.
        event.app.exit(result=None)

    @kb.add("q")
    def _q(event):
        # 'q' quits when you haven't started searching; once filtering, 'q' is
        # just a character (so you can still find "QuickBooks", etc.).
        if not state["filter"]:
            event.app.exit(result=None)
        else:
            state["filter"] += "q"
            _reset_selected()

    @kb.add("backspace")
    def _backspace(event):
        del event
        state["filter"] = state["filter"][:-1]
        _reset_selected()

    @kb.add("<any>")
    def _any(event):
        text = event.data or ""
        if len(text) == 1 and text.isprintable():
            state["filter"] += text
            _reset_selected()

    app = Application(
        layout=Layout(Window(content=FormattedTextControl(menu_text, focusable=True))),
        key_bindings=kb,
        style=Style.from_dict(
            {
                "gold":      "#c8a44a bold",
                "section":   "#b89a5e bold",   # readable section headers
                "dim":       "#9a958a",        # readable, not the old #484840 murk
                "cmd":       "#d6d2c6",        # near-white names
                "desc":      "#b0aa98",        # readable descriptions
                "selected":  "bg:#1a1600 #e8c860 bold",
                "searchbar": "#e0ddd4 bold",  # bright — visible search input
            }
        ),
        # Render INLINE in the chat/input area (like the / menu), not a full-screen takeover — the skills list
        # appears right where you're typing, and is wiped on select so the reply prints cleanly under it.
        full_screen=False,
        erase_when_done=True,
        mouse_support=False,
    )

    return app.run()


_prompt_toolkit_menu = _run_prompt_toolkit_menu


def _mode_display(active_mode: str, world: str) -> str:
    """Label for the status chip — the locked mode, else the world's default posture,
    Title-cased (Partner / Autopilot / Study / Refine)."""
    name = (active_mode or "").strip()
    if not name:
        try:
            import nx_routing as _r
            name = (_r.WORLD_CONFIG.get(world) or {}).get("default_voice", "PARTNER")
        except Exception:
            name = "PARTNER"
    try:
        from nx_prompts import normalize_mode
        name = normalize_mode(name)
    except Exception:
        name = name.upper()
    return name.title()


def _readline_line(prompt: str, first: str) -> str:
    """Read a line with a FIXED, non-editable prompt and the already-read first char
    pre-inserted as (editable) text. Using readline's own prompt is what makes the
    "›" un-backspaceable — the old code hand-drew the prompt then called bare input(),
    so the line editor treated the drawn prefix as deletable text. Falls back to an
    echo+input() path when readline is absent or stdin isn't a TTY (piped/CI). The first
    char is NEVER lost: if the readline startup hook can't pre-insert it (broken/libedit
    readline), it is prepended to the result. An unexpected input() error skips the turn
    rather than re-running input() (which would double-prompt). Returns the stripped
    line, or "/exit" on EOF / ^C / ^D."""
    plain_prompt = prompt.replace("\001", "").replace("\002", "")
    try:
        is_tty = sys.stdin.isatty() and sys.stdout.isatty()
    except Exception:
        is_tty = False
    readline = None
    if is_tty:
        try:
            import readline as _rl
            readline = _rl
        except Exception:
            readline = None
    if readline is not None:
        inserted = {"ok": False}

        def _hook():
            try:
                readline.insert_text(first)
                readline.redisplay()
                inserted["ok"] = True
            except Exception:
                inserted["ok"] = False

        readline.set_startup_hook(_hook)
        try:
            line = input(prompt)
        except (EOFError, KeyboardInterrupt):
            return "/exit"
        except Exception:
            # Unexpected input() failure — do NOT fall through and re-run input()
            # (double-prompt / terminal corruption). Skip; the REPL re-prompts.
            return ""
        finally:
            readline.set_startup_hook(None)
        # Hook couldn't pre-insert the char → recover it so it's never silently dropped.
        if not inserted["ok"]:
            line = first + line
        return line.strip()
    # No TTY or no readline: echo the first char, read the rest, recombine.
    try:
        sys.stdout.write(plain_prompt + first)
        sys.stdout.flush()
        rest = input()
        return (first + rest).strip()
    except (EOFError, KeyboardInterrupt):
        return "/exit"


def _status_bits(world: str, active_mode: str, active_effort: str = "") -> tuple[str, str]:
    """(the active 'world · Mode · effort' label, the FOLDER nx is running in) for the input bar —
    e.g. ('cowork · Partner · mid', 'plasi.ai'). FULL words, not cryptic initials (the old 'C·P'
    read as a bug — nobody could tell what the letters meant): the label says which world
    you're in and how NX is reasoning, in plain language. The effort tail appears only when the
    operator has SET one (auto/unset stays quiet, so the bar doesn't nag). The second bit is the
    project's own name (basename of the launch cwd) — cd into plasi.ai and it says `plasi.ai`, not
    a home-relative path. Home itself shows `~`."""
    W = (world or "cowork").strip()
    mode = _mode_display(active_mode, world)  # Title-case posture (Partner/Autopilot/…)
    label = f"{W} · {mode}" if mode else W
    eff = (active_effort or "").strip().lower()
    if eff and eff != "auto":
        label = f"{label} · {eff}"
    try:
        cwd = os.getcwd()
        home = os.path.expanduser("~")
        folder = "~" if (home and cwd == home) else (os.path.basename(cwd.rstrip("/")) or "/")
    except Exception:
        folder = "~"
    if len(folder) > 24:
        folder = folder[:23] + "…"
    return label, folder


def _footer_text(world: str, active_mode: str, active_skills: list, active_effort: str = "") -> str:
    """The shaded status footer under the input: `nx  <world · Mode · effort>  ·  <cwd>` (· skills).
    cwd is the folder nx is run in (os.getcwd via _status_bits)."""
    label, cwd = _status_bits(world, active_mode, active_effort)
    skills_txt = ("   " + "  ".join(active_skills)) if active_skills else ""
    return f" nx   {label}   ·   {cwd}{skills_txt} "


def _read_input_bar(world: str, active_mode: str, active_skills: list, prefill: str = "",
                    active_effort: str = "") -> tuple[str, str | None]:
    """Read ONE input line. On a TTY with prompt_toolkit: a two-line HSplit — the "›" input line on top and the
    status `nx  <world · Mode>  ·  <folder>` DIRECTLY BELOW it (folder = the project nx runs in). Native
    line-editing via load_key_bindings(); `/` or `$` on an EMPTY buffer opens the command / skills menu (surfaced as
    the trigger). Falls back to a plain readline line elsewhere. Returns (text, trigger) — trigger ∈ {"/", "$", None};
    ("/exit", None) on EOF / ^C."""
    footer = _footer_text(world, active_mode, active_skills, active_effort)
    GOLDD = "\033[38;2;196;162;88m"
    RESET = "\033[0m"
    try:
        is_tty = sys.stdin.isatty() and sys.stdout.isatty()
    except Exception:
        is_tty = False
    if is_tty:
        try:
            from prompt_toolkit.application import Application
            from prompt_toolkit.buffer import Buffer
            from prompt_toolkit.document import Document
            from prompt_toolkit.enums import EditingMode
            from prompt_toolkit.formatted_text import ANSI
            from prompt_toolkit.key_binding import KeyBindings, merge_key_bindings
            from prompt_toolkit.key_binding.defaults import load_key_bindings
            from prompt_toolkit.layout import Layout
            from prompt_toolkit.layout.containers import HSplit, Window
            from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
            from prompt_toolkit.layout.processors import BeforeInput

            DIMC = "\033[38;2;150;146;136m"
            state = {"trigger": None, "exit": False}
            buf = Buffer(multiline=False, document=Document(prefill, cursor_position=len(prefill)))
            kb = KeyBindings()

            @kb.add("enter")
            def _accept(event):
                event.app.exit(result=buf.text)
            # NOTE: we do NOT remap c-j (\n) to insert a newline — on terminals that deliver
            # the ENTER key itself as \n (notably WSL), that would break submit and hang the
            # prompt. Multi-line paste is handled atomically by prompt_toolkit's bracketed
            # paste (Keys.BracketedPaste) on terminals that support it.

            @kb.add("/")
            def _sl(event):
                if buf.text:
                    buf.insert_text("/")
                else:  # first char on an empty line → open the command menu
                    state["trigger"] = "/"
                    event.app.exit(result="")

            @kb.add("$")
            def _dl(event):
                t = buf.text
                # Open the skills picker at a fresh token boundary (empty line, or
                # right after a space) so you can compose several $skills; otherwise
                # insert a literal "$" (mid-word, or a price like $5).
                if t and not t.endswith(" "):
                    buf.insert_text("$")
                else:
                    state["trigger"] = "$"
                    event.app.exit(result=t)   # carry the current line as the prefix

            @kb.add("c-c")
            @kb.add("c-d")
            def _quit(event):
                state["exit"] = True
                event.app.exit(result=None)

            # A REAL two-line bar: the › input on top, the `nx …` status DIRECTLY BELOW it (HSplit), both anchored at
            # the cursor. NOT bottom_toolbar — that pins to the terminal's absolute bottom, marooning the status far
            # below with a gap (and its render path left a doubled ›). load_key_bindings() keeps native editing
            # (backspace, arrows, ^A/^E, kill/yank); our binds override enter / slash / dollar / ^C-^D.
            # Growable, WRAPPING input: a long line (a paragraph, a phone number + message) now wraps across
            # up to 8 rows instead of scrolling off a single invisible row. multiline=False keeps Enter=submit;
            # wrap_lines=True + a min1..max8 height is what makes what you typed actually visible.
            from prompt_toolkit.layout.dimension import Dimension as _Dim
            input_win = Window(
                BufferControl(buffer=buf, input_processors=[BeforeInput(ANSI(f"  {GOLDD}›{RESET}   "))]),
                height=_Dim(min=1, max=8), wrap_lines=True,
            )
            status_win = Window(FormattedTextControl(lambda: ANSI(f"  {DIMC}{footer.strip()}{RESET}")), height=1)
            app = Application(
                layout=Layout(HSplit([input_win, status_win]), focused_element=input_win),
                key_bindings=merge_key_bindings([load_key_bindings(), kb]),
                editing_mode=EditingMode.EMACS,
                full_screen=False,
                mouse_support=False,
                erase_when_done=True,   # erase the interactive bar on exit — see echo below
            )
            text = app.run()
            # Without erase_when_done, prompt_toolkit left its two-line bar (› + `nx …`) on
            # screen after EVERY submit; an empty Enter re-prompts (repl `continue`s) and a
            # long turn can flush buffered Enters, so 4-6 empty bars stacked. Now the bar is
            # erased on exit and we echo the SUBMITTED query ourselves — Codex-style, your
            # prompt persists above the answer, the status footer does not. Empty submits and
            # menu triggers echo nothing, so re-prompts leave no trail.
            if state["trigger"] is None and text and text.strip():
                # SANITIZE before echoing: buf.text is raw and a paste can carry ANSI/C0
                # escapes (colorized output, a log line). Writing them verbatim would let
                # e.g. \x1b[2J clear the screen — wiping the transcript this echo exists to
                # preserve. Strip control chars but KEEP tab + newline (we split on \n).
                _clean = re.sub(r"[\x00-\x08\x0b-\x1f\x7f]", "",
                                text.replace("\r\n", "\n").replace("\r", "\n"))
                if _clean.strip():
                    _lines = _clean.split("\n")
                    sys.stdout.write(f"  {GOLDD}›{RESET}   {_lines[0]}\n")
                    for _cont in _lines[1:]:
                        sys.stdout.write(f"      {_cont}\n")
                    sys.stdout.flush()
            if state["exit"]:
                return ("/exit", None)
            return (text or "", state["trigger"])
        except (EOFError, KeyboardInterrupt):
            return ("/exit", None)
        except Exception:
            pass  # prompt_toolkit missing / broken → plain path below
    try:
        line = input("  › ")
    except (EOFError, KeyboardInterrupt):
        return ("/exit", None)
    return (line, None)


def slash_input(world: str = "cowork", active_skills: list = None, active_mode: str = "", prefill: str = "",
                active_effort: str = "") -> str:
    """
    The REPL input bar: a "›" input line with the status `nx  <world · Mode>  ·  <folder>`
    (the project nx runs in) DIRECTLY BELOW it — a two-line HSplit, not a bottom-of-screen toolbar.
    Native line-editing. / opens the command menu, $ the skills picker. Plain-readline fallback off-TTY.
    `prefill` seeds the input line (used to drop a picked "$skill " in for composition).
    """
    active_skills = active_skills or []
    text, trigger = _read_input_bar(world, active_mode, active_skills, prefill, active_effort)

    if trigger == "/":
        try:
            result = _run_prompt_toolkit_menu(world)
        except Exception:
            result = None
        if result == "/skills":
            try:
                skill = run_skills_menu(world)
            except Exception:
                skill = None
            if skill:
                # Drop "$skill " into the input line to compose (same as the $ picker).
                return slash_input(world=world, active_skills=active_skills,
                                   active_mode=active_mode, prefill=f"{skill} ", active_effort=active_effort)
            return ""
        if result == "/mode":
            try:
                chosen_mode = run_mode_menu(current_mode=active_mode)
            except Exception:
                chosen_mode = None
            if not chosen_mode:
                return ""
            cl = chosen_mode.strip().lower()
            # The two ACTIONS route to their own sentinels; the four postures lock a mode.
            if cl == "flight":
                return "__flight__"
            if cl == "customize":
                return "__customize__"
            return f"__mode__{chosen_mode}"
        if result == "/message":
            try:
                import nx_message as _m
                _states = _m.channels_state()
            except Exception:
                _states = {}
            try:
                chosen_ch = run_message_menu(states=_states)
            except Exception:
                chosen_ch = None
            if chosen_ch:
                return f"__message__{chosen_ch}"
            return ""
        if result in ("/worlds", "/world"):
            try:
                chosen_world = run_world_menu(current_world=world)
            except Exception:
                chosen_world = None
            if chosen_world:
                return f"__world__{chosen_world}"
            return ""
        if result == "/create":
            # The hub: pick what to build. Modes + agents are authored locally and
            # emit a __create_<kind>__ sentinel the REPL turns into a guided form;
            # integrations + channels connect through the account; skill keeps its
            # chat/manual builder; browse drops a picked skill into the input line.
            try:
                kind = run_create_type_menu()
            except Exception:
                kind = None
            if not kind:
                return ""
            if kind in ("mode", "agent", "channel", "integration"):
                return f"__create_{kind}__"
            if kind == "installed":
                try:
                    skill = run_skills_menu(world)
                except Exception:
                    skill = None
                if skill:
                    return slash_input(world=world, active_skills=active_skills,
                                       active_mode=active_mode, prefill=f"{skill} ", active_effort=active_effort)
                return ""
            # kind == "skill" → the existing chat / manual skill builder
            try:
                mode = run_create_mode_menu()
            except Exception:
                mode = None
            if mode == "manual":
                return "__skill_manual__"
            if mode == "chat":
                sys.stdout.write(
                    f"\n  {GOLD}✦{RESET}  Hey! What should this skill do?\n"
                    f"  {DIM}Describe it — purpose, what NX should output, any context.{RESET}\n\n"
                    f"  {GOLD}›{RESET}  "
                )
                sys.stdout.flush()
                try:
                    desc = input("").strip()
                except (KeyboardInterrupt, EOFError):
                    return ""
                if not desc:
                    return ""
                return f"__skill_chat__{desc}"
            return ""
        return result or ""

    elif trigger == "$":
        # Insert the picked "$skill " into the input line and REOPEN the bar so the
        # operator can chain more $skills or add a query before Enter (compose in place).
        prefix = text or ""
        try:
            result = run_skills_menu(world)
        except Exception:
            result = None
        if result:
            sep = "" if (not prefix or prefix.endswith(" ")) else " "
            return slash_input(world=world, active_skills=active_skills,
                               active_mode=active_mode, prefill=f"{prefix}{sep}{result} ", active_effort=active_effort)
        # Nothing picked — reopen preserving whatever was already typed.
        return slash_input(world=world, active_skills=active_skills,
                           active_mode=active_mode, prefill=prefix, active_effort=active_effort)

    # Plain input (or "/exit" from EOF/^C) — hand it back to the REPL.
    return (text or "").strip()


def _read_first_char() -> str:
    """Block until user presses a key. Cross-platform.

    POSIX: termios raw mode + os.read.
    Windows: msvcrt.getwch (already returns a char without echo).
    Non-tty: sys.stdin.read(1) so piped input still works for CI.
    """
    try:
        fd = sys.stdin.fileno()
        is_tty = os.isatty(fd)
    except (ValueError, OSError):
        is_tty = False

    if not is_tty:
        ch = sys.stdin.read(1)
        return ch if ch else "\x04"

    if _HAVE_TERMIOS:
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            b0 = os.read(fd, 1)
            if not b0:
                return "\x04"
            # Multibyte UTF-8: a lead byte alone (emoji / accented first keystroke)
            # decodes to '' and used to return EOF while its continuation bytes
            # corrupted the next read. Derive the sequence length from the lead byte
            # and pull the rest — only bytes already waiting (a real char arrives as
            # one atomic keystroke), so a truncated sequence can never block.
            lead = b0[0]
            n = 1 if lead < 0x80 else 4 if lead >= 0xF0 else 3 if lead >= 0xE0 else 2 if lead >= 0xC0 else 1
            buf = bytearray(b0)
            if n > 1:
                import select as _sel
                while len(buf) < n and _sel.select([fd], [], [], 0.1)[0]:
                    nxt = os.read(fd, 1)
                    if not nxt:
                        break
                    buf += nxt
            ch = bytes(buf).decode("utf-8", errors="ignore")
            return ch if ch else "\x04"
        except Exception:
            return "\x04"
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

    # Windows path — msvcrt
    try:
        import msvcrt  # type: ignore
        ch = msvcrt.getwch()
        return ch if ch else "\x04"
    except Exception:
        # Final fallback — line buffered read
        try:
            return sys.stdin.readline()[:1] or "\x04"
        except Exception:
            return "\x04"
