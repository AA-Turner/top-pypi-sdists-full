"""HeyLead MCP Server — the heart of the product.

Registers all 23 tools and runs via stdio transport for Claude Code / Cursor.

Usage:
    claude mcp add heylead -- python -m heylead
    # or after PyPI publish:
    claude mcp add heylead -- uvx heylead
"""

from __future__ import annotations

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional

from mcp.server.fastmcp import FastMCP

from . import __version__, config
from .constants import DEFAULT_BACKEND_URL, LOGIN_URL_PATH

_SETUP_LOGIN_URL = f"{DEFAULT_BACKEND_URL}{LOGIN_URL_PATH}"

# ──────────────────────────────────────────────
# Changelog (exposed via heylead://changelog resource)
# ──────────────────────────────────────────────

_CHANGELOG = """\
# HeyLead Changelog

## v0.10.103 (2026-03-20)
- Fix: prevent DM jobs racing against pending invites in invitation-based campaigns
- Root cause: _plan_dms() picked 'pending' prospects before invite was accepted, causing 403 subscription_required errors
- Now only schedules DMs for 'connected' prospects when invitations are enabled

## v0.10.75 (2026-03-18)
- Fix: add 4-hour cooldown to alert emails to prevent spam

## v0.10.59 (2026-03-16)
- Verify DM delivery before counting + block invitations to existing connections

## v0.10.0 (2026-03-02)
- New: database backup & restore system — automatic backups before reset and migrations
- New: `heylead backup` CLI command — create manual backups using SQLite's safe backup API
- New: `heylead restore` CLI command — interactive restore from available backups
- New: fresh-DB detection warning when config exists but database is missing (data loss alert)
- New: automatic backup rotation (keeps last 5 backups in ~/.heylead/backups/)

## v0.9.40 (2026-03-01)
- New: profile view warm-up action — lightest touch before following
- New: scheduler auto-views prospect profiles every 10 min (50/day limit)
- New: `engage_prospect(action="view")` MCP tool action
- New: `enable_profile_views` per-campaign toggle in edit_campaign
- Warm-up sequence: Profile View → Follow → Endorse → Engage → Invite → Follow-up DM

## v0.9.39 (2026-03-01)
- New: LinkedIn people lookup with full profile enrichment (email, phone, experience, education, skills, connections)
- New: enriched profile display in contacts(action='view') — contact info, network stats, experience, flags
- Fix: BackendClient.get_profile() endpoint corrected (/api/v1/linkedin/users/)
- New: expanded local contact search now includes email and location fields

## v0.9.38 (2026-02-28)
- New: global contact base with 9 actions (list, search, view, tag, note, stage, stats, export, linkedin_search)

## v0.9.37 (2026-02-28)
- New: global contact base + post intelligence + engagement improvements
- New: auto-assign inbound leads to best-matching campaign + pipeline fixes
- Fix: prevent duplicate comments on same LinkedIn post + anomaly detection
- v0.9.33: Full scheduler observability — event log, metrics, diagnostics, correlation IDs
- New: per-campaign flexible settings — toggles for warm-up, engagement, follow-ups, timing
- New: voice memos ON by default for new campaigns
- New: golden set messaging quality overhaul — anti-patterns + few-shot examples
- Fix: SQLite WAL locking — increase retries, add autocheckpoint + synchronous=NORMAL
- New: replace data-completeness scoring with ICP match + composite lead score
- New: async DB bridge, profile change signals, expanded profile editing

## v0.9.33 (2026-02-28)
- Full scheduler observability: event log table, job metrics, error categorization
- New MCP actions: scheduler(action='logs') and scheduler(action='diagnostics')
- Job duration tracking with duration_ms persisted to DB
- Timer state persistence to SQLite (survives MCP server restarts)
- Dual JSON+text logging (~/.heylead/logs/heylead.json.log)
- Correlation IDs across MCP client → backend (X-Correlation-ID header)
- 24h metrics summary in scheduler(action='status')
- Daily digest job with email delivery
- OpenTelemetry trace spans (opt-in, no-op when OTel not installed)
- heylead-logs CLI: summary, errors, slow, search, correlate, tail

## v0.9.32 (2026-02-28)
- Flexible campaign settings: 15 new per-campaign toggles via edit_campaign
- Warm-up sequence toggles: enable_follows, enable_endorsements, enable_engagements, enable_followups (on/off)
- Engagement mode: auto (30/70 react/comment), comment_only, or react_only
- Follow-up customization: max_followups (1-5), followup_delay_days (custom schedule)
- Send timing: send_in_business_hours (on/off), active_days (choose which days to send)
- Stale invite settings: withdraw_stale_invites (on/off), stale_invite_days (7-60)
- show_status now displays non-default campaign settings
- All settings stored in config_json with backwards-compatible defaults

## v0.9.31 (2026-02-28)
- Voice memos ON by default: new campaigns launch with voice_mode='mixed' (alternating text & voice)
- Added voice_mode parameter to create_campaign tool
- Agent instructions now ask users about voice preference before campaign creation
- suggest_next_action flipped: suggests disabling voice if acceptance is low instead of enabling

## v0.9.22 (2026-02-26)
- Fix: FK constraint on scheduler_jobs — global jobs now use NULL campaign_id instead of empty string
- Fix: missing `list_campaigns` import in planner (NameError on schedule cycle)
- Fix: `get_setting` import path in channel_selector (ImportError)
- Fix: `save_setting` UnboundLocalError in create_campaign (redundant local import)
- Fix: missing `updated_at` column in contacts table (added schema + migration)
- Fix: retry 502/503/504 on search params endpoint (use _retry_request)
- Fix: endorsement retry loop — detect permanent failures by error phrase, not just HTTP status
- Fix: duplicate MCP log lines — remove redundant stderr handler
- Fix: brand strategy auto-apply logging for headline/summary/photo failures
- Fix: add x-restli-method header for LinkedIn profile update Voyager calls

## v0.9.21 (2026-02-26)
- Fix: singleton BackendClient — httpx AsyncClient no longer closed prematurely between tool calls
- Fix: create_campaign dedup crash ("Cannot send a request, as the client has been closed")

## v0.9.20 (2026-02-26)
- Fix: scheduler leader election — only one instance runs the scheduler, others serve MCP tools in follower mode
- Fix: hardened DB retry logic (8 retries with jitter, busy_timeout 60s)

## v0.9.19 (2026-02-26)
- Fix: validate engagement API results in brand strategy, save to DB

## v0.9.18 (2026-02-26)
- Fix: retry DB operations on lock + silence httpx stderr noise

## v0.9.17 (2026-02-26)
- Update OpenClaw listing with 22 consolidated tools

## v0.9.16 (2026-02-26)
- New: custom domain heylead.dev, brand strategy execution, campaign UX

## v0.9.15 (2026-02-26)
- New: heylead://changelog MCP resource — clients can now query version history
- Fix: __version__ sync between pyproject.toml and runtime

## v0.9.14 (2026-02-26)
- Voice enhancement pipeline: text humanization, multi-utterance delivery, ambient noise overlay
- OpenClaw integration: SKILL.md + clawhub.json for agent marketplace
- Singleton DB connection for reliability

## v0.9.13 (2026-02-26)
- Fix signal funnel: scoring, classification, and activation pipeline

## v0.9.12 (2026-02-25)
- Voice memo test mocks fix, version bump

## v0.9.11 (2026-02-25)
- Always-on inbound pipeline with friend detection
- Tool consolidation: 39 → 22 tools via action-parameter pattern

## v0.9.10 (2026-02-24)
- Velocity count mismatch fix, connection sync improvements, voice memo fixes

## v0.9.9 (2026-02-23)
- Voice memos via Hume AI: TTS generation, LinkedIn delivery, A/B testing

## v0.9.8 (2026-02-22)
- Signal-based selling v1.0: keyword monitoring, prospect post scanning, compound intents
- Live dashboard sync with backend

## v0.9.7 (2026-02-21)
- Tracking accuracy: 9 gap fixes, engagement linking, E2E tests

## v0.9.6 (2026-02-20)
- Strategy engine: autonomous cross-campaign optimization for revenue
- Campaign optimizer, pattern detector, revenue estimator, campaign spawner

## v0.9.5 (2026-02-19)
- Fix: first DM after connection acceptance — create new chat fallback

## v0.9.4 (2026-02-18)
- Fix: check_replies UnboundLocalError + filter newsletter invitations

## v0.9.3 (2026-02-17)
- Mixed comment/react engagement strategy (30% react / 70% comment, first touch always comment)

## v0.9.2 (2026-02-16)
- Quick wins: 10-to-1 query optimization, stale lead warnings, cohort won/lost tracking

## v0.9.1 (2026-02-15)
- Inbound lead qualification pipeline: AI-qualified inbound leads with auto-DMs
- 3 signal types: invitations, DMs, post comments
- 2 new scheduler jobs: qualify_inbound (15 min), check_post_comments (30 min)

## v0.9.0 (2026-02-14)
- HubSpot CRM integration: sync won deals and hot leads
"""

# ──────────────────────────────────────────────
# Logging (MUST go to stderr/file, NEVER stdout — breaks MCP stdio)
# ──────────────────────────────────────────────

class _JsonFormatter(logging.Formatter):
    """JSON Lines log formatter for machine-parseable logs.

    Outputs one JSON object per line. Extra fields (job_id, campaign_id, etc.)
    can be passed via ``logger.info("msg", extra={"job_id": "abc"})``.
    """

    def format(self, record: logging.LogRecord) -> str:
        import json as _json

        entry: dict = {
            "ts": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        # Propagate extra fields commonly used by the scheduler
        for key in ("job_id", "campaign_id", "correlation_id", "error_category",
                     "duration_ms", "tick", "job_type"):
            val = getattr(record, key, None)
            if val is not None:
                entry[key] = val
        # Auto-inject correlation ID from contextvars if not in extra
        if "correlation_id" not in entry:
            from .correlation import get_correlation_id
            cid = get_correlation_id()
            if cid:
                entry["correlation_id"] = cid
        if record.exc_info and record.exc_info[0]:
            entry["exception"] = self.formatException(record.exc_info)
        return _json.dumps(entry, default=str)


def _setup_logging() -> None:
    """Configure logging to file only. Never stdout.

    Two log files:
    - heylead.log      — plain text (human-readable, ``tail -f`` friendly)
    - heylead.json.log — JSON Lines (machine-parseable, ``jq`` friendly)

    FastMCP's Rich handler already writes to stderr for MCP stdio transport,
    so we only add file handlers here to avoid duplicate log lines.
    """
    config.ensure_dirs()
    log_file = config.log_path()
    json_log_file = config.json_log_path()

    root_logger = logging.getLogger("heylead")

    # Guard: don't add duplicate handlers on re-import
    if root_logger.handlers:
        return

    root_logger.setLevel(logging.DEBUG)

    # Plain text file handler (rotating, 10 MB)
    file_handler = logging.handlers.RotatingFileHandler(
        str(log_file),
        maxBytes=10 * 1024 * 1024,
        backupCount=3,
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    )
    root_logger.addHandler(file_handler)

    # JSON Lines file handler (rotating, 10 MB)
    json_handler = logging.handlers.RotatingFileHandler(
        str(json_log_file),
        maxBytes=10 * 1024 * 1024,
        backupCount=3,
    )
    json_handler.setLevel(logging.DEBUG)
    json_handler.setFormatter(_JsonFormatter())
    root_logger.addHandler(json_handler)

    # No stderr handler — FastMCP's Rich console handler already covers stderr.
    # Adding one here would duplicate WARNING+ messages in MCP logs.

    # Silence httpx request logging — it goes to stderr which Cursor/MCP
    # displays as [error] even for successful 200 OK responses.
    # Set HEYLEAD_HTTPX_LOG_LEVEL=DEBUG to see full request/response logs.
    import os as _os
    _httpx_level = getattr(
        logging, _os.environ.get("HEYLEAD_HTTPX_LOG_LEVEL", "WARNING").upper(), logging.WARNING,
    )
    logging.getLogger("httpx").setLevel(_httpx_level)
    logging.getLogger("httpcore").setLevel(_httpx_level)


# ──────────────────────────────────────────────
# Initialize MCP Server
# ──────────────────────────────────────────────

_setup_logging()
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# Lifespan hook — background scheduler (Sprint 17)
# ──────────────────────────────────────────────

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator


@asynccontextmanager
async def _app_lifespan(app: FastMCP) -> AsyncIterator[dict]:
    """Start/stop the autonomous scheduler + cloud sync alongside the MCP server.

    Uses file-based leader election so only ONE process across all MCP clients
    (Claude Code, Cursor, etc.) runs the scheduler.  Other instances serve
    MCP tools normally in "follower" mode.
    """
    import asyncio
    from .scheduler.engine import SchedulerEngine
    from .scheduler.leader import try_acquire_leader, release_leader

    is_leader = try_acquire_leader()

    engine: SchedulerEngine | None = None
    cloud_sync_task: asyncio.Task | None = None

    if is_leader:
        engine = SchedulerEngine()
        await engine.start()
        logger.info("Scheduler engine started (leader mode, enabled=%s)",
                     config.is_scheduler_enabled())

        # Start cloud sync pull loop only for the leader
        cloud_sync_task = asyncio.create_task(_cloud_sync_loop())
    else:
        logger.info("Running in follower mode — scheduler delegated to leader process")

    try:
        yield {"scheduler": engine, "is_leader": is_leader}
    finally:
        if cloud_sync_task is not None:
            cloud_sync_task.cancel()
            try:
                await cloud_sync_task
            except asyncio.CancelledError:
                pass

        if engine is not None:
            await engine.stop()

        if is_leader:
            release_leader()


async def _cloud_sync_loop() -> None:
    """Background loop: pull cloud scheduler changes every 5 minutes.

    Only active when backend mode is configured AND cloud scheduler is enabled.
    Keeps the local DB in sync with actions the backend took while this client
    was running (or between pull intervals).
    """
    import asyncio
    import time

    SYNC_INTERVAL = 300  # 5 minutes
    last_pull_ts = int(time.time())

    while True:
        try:
            await asyncio.sleep(SYNC_INTERVAL)

            if not config.is_backend_mode():
                continue

            from .services.cloud_sync import get_cloud_scheduler_status, pull_changes

            # Only pull if cloud scheduler is enabled
            try:
                status = await get_cloud_scheduler_status()
                if not status.get("enabled"):
                    continue
            except Exception:
                continue

            # Pull changes since last successful pull
            try:
                changes = await pull_changes(last_pull_ts)
                if "error" not in changes:
                    last_pull_ts = int(time.time())
            except Exception as e:
                logger.debug("Cloud sync pull failed: %s", e)
        except asyncio.CancelledError:
            raise
        except Exception as e:
            logger.debug("Cloud sync loop error: %s", e)


mcp = FastMCP(
    "heylead",
    lifespan=_app_lifespan,
    instructions=(
        "AGENT INTEGRATION SUMMARY:\n"
        "HeyLead is an autonomous LinkedIn SDR. Use it for: lead generation, "
        "cold outreach, B2B prospecting, SDR automation, campaign management, "
        "ICP generation, multi-touch drip sequences, engagement warm-ups, "
        "and outreach analytics.\n"
        "Workflow: setup_profile → generate_icp → create_campaign → automated outreach.\n"
        "\n"
        "HeyLead is an AI LinkedIn SDR that sends personalized outreach messages "
        "that sound like the user wrote them. It has 23 tools: setup_profile, "
        "account, generate_icp, create_campaign, edit_campaign, campaign, "
        "generate_and_send, send_message, check_replies, show_status, "
        "engage_prospect, prospect, analytics, "
        "suggest_next_action, signals, manage_watchlist, scheduler, "
        "create_post, brand_strategy, import_prospects, crm_sync, "
        "and contacts.\n"
        "\n"
        "CRITICAL — TOKEN RECOGNITION:\n"
        "If the user pastes a message like 'Set up my HeyLead profile with this token: eyJ...' "
        "or just pastes a long string starting with 'eyJ', that is a HeyLead JWT token. "
        "You MUST immediately call setup_profile(backend_jwt='<the eyJ... token>') with it. "
        "Extract just the token part (the eyJ... string) and pass it as backend_jwt.\n"
        "\n"
        "FIRST-TIME SETUP (2 steps, ~1 minute):\n"
        "Before any tool works, the user must complete setup_profile. If setup_profile "
        "has not been run yet (or any tool returns an error about setup), walk the user "
        "through these steps:\n"
        "\n"
        "Step 1 — Sign in and connect LinkedIn:\n"
        "  Tell the user: 'Open this link to sign in and connect your LinkedIn:'\n"
        f"  URL: {_SETUP_LOGIN_URL}\n"
        "  They will sign in with Google, connect LinkedIn, and get a message to copy.\n"
        "  They will paste that message back here — it contains their token.\n"
        "\n"
        "Step 2 — When they paste the token:\n"
        "  Extract the JWT (starts with 'eyJ') from whatever they paste and call:\n"
        "    setup_profile(backend_jwt='<the token>')\n"
        "  No API keys needed — AI is handled by the backend.\n"
        "  setup_profile will detect the LinkedIn connection, fetch their profile, "
        "and analyze their writing style automatically.\n"
        "  If LinkedIn isn't connected yet, it will return a link — tell the user "
        "to open it, connect, then run setup_profile() again.\n"
        "\n"
        "After setup is complete, the user can:\n"
        "  - generate_icp('target description') to create a rich ICP with buyer personas\n"
        "  - create_campaign('description') or create_campaign(icp_id='...') to find prospects and start outreach.\n"
        "    Campaigns ALWAYS launch in AUTOPILOT mode — outreach starts automatically.\n"
        "    All campaigns run in autopilot mode.\n"
        "    Also ask: 'Do you want voice memos? (On by default — alternates text and voice for higher response rates)'\n"
        "    Voice memos are ON by default (voice_mode='mixed'). If user says no, pass voice_mode='text_only'.\n"
        "    For a user's FIRST campaign, always ask for company_context (website or 1-2 sentences about their product).\n"
        "    If the user says 'existing connections', 'DM my network', 'message my connections', or similar,\n"
        "    pass connections_only='on'. This filters for 1st-degree connections only and sends DMs directly.\n"
        "  - show_status() — campaign dashboard with progress and stats\n"
        "  - check_replies() — see who responded, inbound invitations, and profile viewers\n"
        "  - suggest_next_action() — AI-recommended next step\n"
        "  - analytics(action='report') — detailed analytics with outcomes and stale lead warnings\n"
        "  - generate_and_send() — manually trigger a single message\n"
        "  - send_message(action='followup') to send follow-up DMs after connection accepted\n"
        "  - send_message(action='reply') to reply to prospects who have messaged you\n"
        "  - send_message(action='voice') to send a voice memo on LinkedIn\n"
        "  - engage_prospect() to comment on, react to, follow, or endorse a prospect on LinkedIn\n"
        
        "  - campaign(action='pause') / campaign(action='resume') to control campaign status\n"
        "  - campaign(action='archive') to archive a completed campaign\n"
        "  - campaign(action='delete') to permanently delete a campaign\n"
        "  - campaign(action='emergency_stop') to immediately pause all active campaigns\n"
        "  - campaign(action='retry_failed') to retry outreaches that failed with errors\n"
        "  - campaign(action='status_history') to view who changed campaign status and when\n"
        "  - analytics(action='export') to export campaign results as a table\n"
        "  - analytics(action='compare') to compare 2+ campaigns side by side\n"
        "  - prospect(action='skip', outreach_id='...') to skip a bad-fit prospect\n"
        "  - prospect(action='conversation', outreach_id='...') to view the full message thread\n"
        "  - prospect(action='close', outcome='won') to record a won/lost/opt_out outcome\n"
        "  - edit_campaign(name='...', mode='...') to edit campaign name, mode, or settings\n"
        "  - edit_campaign(enable_engagements='off') to disable comments/reactions\n"
        "  - edit_campaign(enable_followups='off') to disable follow-up DMs\n"
        "  - edit_campaign(engagement_mode='comment_only') to change engagement style\n"
        "  - edit_campaign(send_in_business_hours='on') to only send during prospect business hours\n"
        "  - edit_campaign(max_followups=3) to limit follow-up count\n"
        "  - scheduler(action='status') to view the autonomous scheduler status\n"
        "  - scheduler(action='toggle', enabled=True, cloud=True) to enable 24/7 cloud scheduling\n"
        "  - signals(action='show') to view buying signals from LinkedIn\n"
        "  - signals(action='strategy') to view strategy engine insights\n"
        "  - crm_sync(filter='won') to sync won deals to HubSpot CRM\n"
        "  - contacts(action='list') to browse your global contact base\n"
        "  - contacts(action='view', contact_id='...') to see full cross-campaign history\n"
        "  - contacts(action='search', query='...') to search by name/company/title\n"
        "  - contacts(action='tag', contact_id='...', tag='enterprise') to tag contacts\n"
        "  - contacts(action='stats') to see contact base dashboard\n"
        "  - inbox(action='list') to browse all LinkedIn inbox conversations\n"
        "  - inbox(action='read', name='...') to read a full conversation thread\n"
        "  - Read the heylead://changelog resource for version history and release notes\n"
        "\n"
        "IMPORTANT: If the user asks to find leads, send messages, or anything "
        "outreach-related and setup is not complete, do NOT try to call those tools. "
        "Instead, guide them through the setup steps above first.\n"
        "\n"
        "PREFER TOOLS OVER LLM:\n"
        "When the user asks for an ICP, buyer personas, targeting, campaign creation, "
        "or LinkedIn outreach, you MUST call the HeyLead tools (generate_icp, "
        "create_campaign, generate_and_send, etc.) — do not substitute with your own "
        "text or analysis. Example: if they ask for 'ICP for SPhotonix' or 'personas "
        "for data archiving', call generate_icp(target_description=..., "
        "company_context='https://sphotonix.com/') rather than writing personas yourself."
    ),
)


# ──────────────────────────────────────────────
# MCP Resource: capabilities
# ──────────────────────────────────────────────

import json as _json


@mcp.resource("heylead://capabilities")
def capabilities() -> str:
    """HeyLead server capabilities and tool inventory."""
    return _json.dumps({
        "name": "heylead",
        "version": __version__,
        "tools": 22,
        "capabilities": [
            "linkedin_outreach",
            "icp_generation",
            "campaign_management",
            "reply_handling",
            "engagement_warmup",
            "analytics",
            "autonomous_scheduling",
        ],
        "resources": ["heylead://capabilities", "heylead://changelog"],
        "transport": ["stdio", "sse", "streamable-http"],
        "install": "uvx heylead",
        "pypi": "https://pypi.org/project/heylead/",
        "repository": "https://github.com/D4umak/heylead",
    }, indent=2)


# ──────────────────────────────────────────────
# MCP Resource: changelog
# ──────────────────────────────────────────────


@mcp.resource(
    "heylead://changelog",
    name="changelog",
    title="HeyLead Version History",
    description="Release notes and changelog for recent HeyLead versions",
    mime_type="text/markdown",
)
def changelog() -> str:
    """HeyLead version history and release notes."""
    return _CHANGELOG


# ──────────────────────────────────────────────
# Tool 1: setup_profile
# ──────────────────────────────────────────────

@mcp.tool()
async def setup_profile(
    llm_api_key: str = "",
    llm_provider: str = "gemini",
    backend_url: str = "",
    backend_jwt: str = "",
) -> str:
    """Set up HeyLead by connecting your LinkedIn account and analyzing your writing style.

    REQUIRED for first-time users — must be called before any other tool.

    This analyzes your LinkedIn profile, posts, and writing style to create
    a "voice signature" so every outreach message sounds like YOU, not a bot.
    Handles LinkedIn automation setup, SDR onboarding, account connection,
    and voice analysis for personalized outreach.

    First-time setup: sign in at the URL below, connect LinkedIn, copy your token,
    then call this tool with backend_jwt='YOUR_TOKEN'. No API keys needed!

    Args:
        llm_api_key: Optional — only if you want to use your own AI key instead of the backend's.
        llm_provider: Which AI to use if providing your own key: "gemini", "claude", or "openai".
        backend_url: HeyLead Backend API URL. Leave empty — defaults to production server.
        backend_jwt: Your authentication token from HeyLead.
    """
    from .tools.setup_profile import run_setup_profile

    logger.info("Running setup_profile")
    try:
        result = await run_setup_profile(
            llm_api_key=llm_api_key,
            llm_provider=llm_provider,
            backend_url=backend_url,
            backend_jwt=backend_jwt,
        )
        logger.info("setup_profile completed")
        return result
    except Exception as e:
        logger.error(f"setup_profile failed: {e}", exc_info=True)
        return f"❌ Setup failed: {e}\n\nCheck ~/.heylead/logs/heylead.log for details."


# ──────────────────────────────────────────────
# Tool: account (consolidated)
# ──────────────────────────────────────────────

@mcp.tool()
async def account(
    action: str = "list",
    account_id: str = "",
) -> str:
    """Manage your LinkedIn accounts — list, switch, or disconnect.

    Args:
        action: What to do:
            "list"      — Show all connected LinkedIn accounts (default)
            "switch"    — List accounts and pick one to switch to
            "switch_to" — Switch to a specific account by ID
            "unlink"    — Disconnect the current LinkedIn account
        account_id: The Unipile account ID (required for "switch_to").
    """
    from .tools.account import run_account

    logger.info(f"Running account: action={action}")
    try:
        return await run_account(action, account_id)
    except Exception as e:
        logger.error(f"account failed: {e}", exc_info=True)
        return f"Account action failed: {e}"


# ──────────────────────────────────────────────
# Tool 2a: generate_icp
# ──────────────────────────────────────────────

@mcp.tool()
async def generate_icp(
    target_description: str,
    company_context: str = "",
    focus_query: str = "",
) -> str:
    """Generate a rich Ideal Customer Profile with buyer personas.

    Creates 2-4 ICP personas with pain points, fears, barriers,
    LinkedIn search parameters, and confidence scores. The result
    is saved and can be reused with create_campaign(icp_id=...).
    Supports target audience analysis, customer segmentation, buyer persona
    creation, ideal customer profiling, and B2B market research.

    Args:
        target_description: Who to target (e.g., "CTOs at fintech startups",
            "freelance UX designers in London", "yoga studio owners in California")
        company_context: Optional URL or text about your company/product.
            Providing this makes the ICP more precise and evidence-backed.
        focus_query: Optional focus (e.g., "enterprise segment only",
            "focus on pain points around compliance")
    """
    from .tools.generate_icp import run_generate_icp

    logger.info(f"Running generate_icp: {target_description}")
    try:
        return await run_generate_icp(target_description, company_context, focus_query)
    except Exception as e:
        logger.error(f"generate_icp failed: {e}", exc_info=True)
        return f"ICP generation failed: {e}"


# ──────────────────────────────────────────────
# Tool 2b: create_campaign
# ──────────────────────────────────────────────

@mcp.tool()
async def create_campaign(
    target_description: str,
    campaign_name: str = "",
    icp_id: str = "",
    company_context: str = "",
    mode: str = "autopilot",
    company_url: str = "",
    voice_mode: str = "mixed",
    connections_only: str = "",
) -> str:
    """Create a LinkedIn outreach campaign from a natural language description.

    Describe your ideal customers and HeyLead will find them on LinkedIn.
    Supports lead generation, prospect discovery, SDR automation, cold outreach,
    and targeted B2B sales campaigns with AI-powered ICP-based targeting.
    On first campaign, company_context is asked explicitly for best results.

    Args:
        target_description: Who to target (e.g., "CTOs at fintech startups",
            "freelance UX designers in London", "yoga studio owners in California")
        campaign_name: Optional name for the campaign.
        icp_id: Optional ID of a saved ICP from generate_icp. If provided,
            uses the saved ICP's enriched LinkedIn codes for precise targeting
            instead of generating a new one.
        company_context: Optional. Your website URL or 1-2 sentences about your
            product/company. Strongly recommended for first campaign — sharper ICP
            and more relevant messaging.
        mode: Always autopilot. Copilot mode removed.
        company_url: Optional LinkedIn company URL for account-based targeting.
            Searches for employees at that specific company matching the ICP.
            Example: "https://www.linkedin.com/company/google"
        voice_mode: Voice memo mode for follow-ups and replies. "mixed" (default,
            alternates text and voice), "text_only", "voice_only", or "ab_test".
        connections_only: "on" to create a DM-only campaign targeting existing
            LinkedIn connections. Skips invitations and warm-up — sends DMs
            directly to people you're already connected with. Use when user says
            "existing connections", "DM my network", "message my connections".
    """
    from .tools.create_campaign import run_create_campaign

    logger.info(f"Running create_campaign: {target_description} (mode={mode}, connections_only={connections_only})")
    try:
        return await run_create_campaign(
            target_description, campaign_name, icp_id, company_context, mode,
            company_url, voice_mode, connections_only,
        )
    except Exception as e:
        logger.error(f"create_campaign failed: {e}", exc_info=True)
        return f"❌ Campaign creation failed: {e}"


# ──────────────────────────────────────────────
# Tool 3: generate_and_send
# ──────────────────────────────────────────────

@mcp.tool()
async def generate_and_send(
    campaign_id: str = "",
    mode: str = "autopilot",
) -> str:
    """Generate a personalized LinkedIn message and send it (or queue for review).

    Creates and sends cold outreach, connection requests, and personalized
    LinkedIn invitations using voice-matched AI messaging.
    In Autopilot mode (default): sends automatically after validation.
    In Copilot mode: shows the message for your approval before sending.

    Args:
        campaign_id: Which campaign to send from. Uses active campaign if empty.
        mode: Always autopilot. Copilot mode removed.
    """
    from .tools.generate_send import run_generate_and_send

    logger.info(f"Running generate_and_send: campaign={campaign_id}, mode={mode}")
    try:
        return await run_generate_and_send(campaign_id, mode)
    except Exception as e:
        logger.error(f"generate_and_send failed: {e}", exc_info=True)
        return f"❌ Message generation failed: {e}"


# ──────────────────────────────────────────────
# Tool 4: check_replies
# ──────────────────────────────────────────────

@mcp.tool()
async def check_replies() -> str:
    """Check for new LinkedIn replies across all campaigns.

    Fetches new messages, classifies sentiment (positive/negative/question),
    and surfaces hot leads that need your attention.
    Handles inbox monitoring, lead response tracking, and conversation management.
    """
    from .tools.check_replies import run_check_replies

    logger.info("Running check_replies")
    try:
        return await run_check_replies()
    except Exception as e:
        logger.error(f"check_replies failed: {e}", exc_info=True)
        return f"❌ Reply check failed: {e}"


# ──────────────────────────────────────────────
# Tool 5: show_status
# ──────────────────────────────────────────────

@mcp.tool()
async def show_status(
    campaign_id: str = "",
) -> str:
    """Show your outreach dashboard — campaigns, stats, hot leads, account health.

    The chat IS your dashboard. View pipeline metrics, prospect funnel,
    engagement rates, and campaign performance. Ask "how's my outreach?" anytime.

    Args:
        campaign_id: Show stats for a specific campaign. Shows all if empty.
    """
    from .tools.show_status import run_show_status

    logger.info("Running show_status")
    try:
        return await run_show_status(campaign_id)
    except Exception as e:
        logger.error(f"show_status failed: {e}", exc_info=True)
        return f"❌ Status check failed: {e}"


# ──────────────────────────────────────────────
# Tool: campaign (consolidated lifecycle)
# ──────────────────────────────────────────────

@mcp.tool()
async def campaign(
    action: str,
    campaign_id: str = "",
    confirm: bool = False,
) -> str:
    """Control campaign lifecycle — pause, resume, archive, delete, emergency stop, or retry failed.

    Args:
        action: What to do:
            "pause"          — Pause an active campaign
            "resume"         — Resume a paused campaign
            "archive"        — Archive a completed campaign
            "delete"         — Permanently delete a campaign (requires confirm=True)
            "emergency_stop" — Immediately pause ALL active campaigns (kill switch)
            "retry_failed"   — Reset error outreaches to pending
            "status_history" — View campaign status change audit log (who stopped/started and when)
        campaign_id: Which campaign to act on. Auto-selects if empty.
        confirm: Must be True for delete action. Safety guard.
    """
    from .tools.campaign import run_campaign

    logger.info(f"Running campaign: action={action}, campaign_id={campaign_id}")
    try:
        return await run_campaign(action, campaign_id, confirm)
    except Exception as e:
        logger.error(f"campaign failed: {e}", exc_info=True)
        return f"Campaign action failed: {e}"


# ──────────────────────────────────────────────
# Tool: send_message (consolidated)
# ──────────────────────────────────────────────

@mcp.tool()
async def send_message(
    action: str = "followup",
    campaign_id: str = "",
    outreach_id: str = "",
    mode: str = "autopilot",
    format: str = "text",
    text: str = "",
) -> str:
    """Send follow-ups, replies, or voice memos to prospects.

    Args:
        action: What to do:
            "followup" — Send a follow-up DM after connection accepted
            "reply"    — Reply to a prospect who has messaged you
            "voice"    — Send a voice memo on LinkedIn
            "delete"   — Delete a recently sent message (within 60 min on LinkedIn)
        campaign_id: Which campaign to send from. Uses active if empty.
        outreach_id: Specific outreach to target. Auto-picks next if empty.
        mode: Always autopilot. Copilot mode removed.
        format: 'text' (default) or 'voice' (audio via Hume TTS). For followup/reply.
        text: Custom text for voice memo. Auto-generates if empty.
            For delete: optionally pass a Unipile message_id directly.
    """
    from .tools.send_message import run_send_message

    logger.info(f"Running send_message: action={action}, campaign={campaign_id}, outreach={outreach_id}")
    try:
        return await run_send_message(action, campaign_id, outreach_id, mode, format, text)
    except Exception as e:
        logger.error(f"send_message failed: {e}", exc_info=True)
        return f"Message send failed: {e}"


# ──────────────────────────────────────────────
# Tool 9: engage_prospect
# ──────────────────────────────────────────────

@mcp.tool()
async def engage_prospect(
    campaign_id: str = "",
    outreach_id: str = "",
    action: str = "auto",
    mode: str = "autopilot",
) -> str:
    """Comment on, react to, follow, or endorse a prospect on LinkedIn to build trust.

    Finds a prospect's recent posts, generates a voice-matched comment
    (or reacts with a Like), and sends it. Use action="follow" to follow
    a prospect's profile — this triggers a "X started following you"
    notification and warms them up before connecting. Use action="endorse"
    to endorse their skills — triggers a high-visibility notification.
    Great for social selling, warm-up engagement, and building familiarity
    before cold outreach.

    Args:
        campaign_id: Which campaign to engage from. Uses active campaign if empty.
        outreach_id: Specific outreach to engage with. Auto-picks next if empty.
        action: "auto" (comment if post has text, react otherwise),
            "comment" (always comment), "react" or "like" (just like the post),
            "view" (view their LinkedIn profile — lightest warm-up signal),
            "follow" (follow their LinkedIn profile as a warm-up signal),
            "endorse" (endorse their skills — highest visibility warm-up),
            "reply_comment" (reply to prospect's response on your comment thread).
        mode: Always autopilot. Copilot mode removed.
    """
    from .tools.engage_prospect import run_engage_prospect

    logger.info(f"Running engage_prospect: campaign={campaign_id}, outreach={outreach_id}, action={action}, mode={mode}")
    try:
        return await run_engage_prospect(campaign_id, outreach_id, action, mode)
    except Exception as e:
        logger.error(f"engage_prospect failed: {e}", exc_info=True)
        return f"Engagement failed: {e}"


# ──────────────────────────────────────────────
# Tool 10: suggest_next_action (approve_outreach removed — copilot mode removed)
# ──────────────────────────────────────────────

@mcp.tool()
async def suggest_next_action(
    campaign_id: str = "",
) -> str:
    """Suggest the best next action for your outreach.

    Analyzes all active campaigns and recommends what to do next,
    prioritized by impact: hot leads first, then pending approvals,
    follow-ups, engagement warm-ups, and new invitations.

    Args:
        campaign_id: Focus on a specific campaign. Analyzes all active if empty.
    """
    from .tools.suggest_next_action import run_suggest_next_action

    logger.info(f"Running suggest_next_action: campaign_id={campaign_id}")
    try:
        return await run_suggest_next_action(campaign_id)
    except Exception as e:
        logger.error(f"suggest_next_action failed: {e}", exc_info=True)
        return f"Failed to suggest next action: {e}"






# ──────────────────────────────────────────────
# Tool 19: edit_campaign
# ──────────────────────────────────────────────

@mcp.tool()
async def edit_campaign(
    campaign_id: str = "",
    name: str = "",
    mode: str = "",
    booking_link: str = "",
    offerings: str = "",
    case_studies: str = "",
    social_proofs: str = "",
    campaign_preferences: str = "",
    voice_mode: str = "",
    voice_noise: str = "",
    voice_humanize: str = "",
    enable_profile_views: str = "",
    enable_follows: str = "",
    enable_endorsements: str = "",
    enable_engagements: str = "",
    enable_followups: str = "",
    enable_auto_replies: str = "",
    enable_invitations: str = "",
    engagement_mode: str = "",
    max_followups: int = 0,
    followup_delay_days: str = "",
    withdraw_stale_invites: str = "",
    stale_invite_days: int = 0,
    send_in_business_hours: str = "",
    active_days: str = "",
) -> str:
    """Edit a campaign's name, mode, booking link, or context fields.

    Change the campaign name or configure campaign settings
    modes, set a booking link, or configure campaign context for
    better message personalization.

    Args:
        campaign_id: Which campaign to edit. Edits the first active campaign if empty.
        name: New campaign name. Leave empty to keep current name.
        mode: Only "autopilot" supported. Copilot mode removed.
        booking_link: Calendar/booking URL (e.g., "https://cal.com/you/15min").
            Used in reply_to_prospect() for positive replies to suggest meetings.
        offerings: What you offer (products, services, value props). Used in follow-up messages.
        case_studies: Brief case studies or success stories. Used for social proof in messages.
        social_proofs: Social proof (logos, metrics, testimonials). Used in follow-up messages.
        campaign_preferences: Custom messaging preferences (tone, topics to avoid, etc.).
        voice_mode: Voice memo mode: "text_only", "voice_only", "mixed", or "ab_test".
            Leave empty to keep current value.
        voice_noise: Ambient noise type for voice memos: "office", "cafe", "street",
            "quiet", "none", "auto". Leave empty to keep current value.
        voice_humanize: Voice text humanization: "on" or "off".
            Leave empty to keep current value.
        enable_profile_views: View prospect profiles before following: "on" or "off".
        enable_follows: Follow prospects before inviting: "on" or "off".
        enable_endorsements: Endorse skills before inviting: "on" or "off".
        enable_engagements: Comment/react on posts before inviting: "on" or "off".
        enable_followups: Send follow-up DMs after connection: "on" or "off".
        enable_auto_replies: Auto-reply to prospect messages: "on" or "off".
        enable_invitations: Send connection invitations: "on" or "off".
            When off, campaign only DMs existing connections (no invitations sent).
        engagement_mode: Engagement style: "auto" (30% react / 70% comment),
            "comment_only", or "react_only".
        max_followups: Max follow-up messages (1-5). 0 to keep current.
        followup_delay_days: Custom day intervals as comma-separated list
            (e.g., "1,3,7,14"). Leave empty to keep current.
        withdraw_stale_invites: Auto-withdraw stale invites: "on" or "off".
        stale_invite_days: Days before withdrawing stale invites (7-60). 0 to keep current.
        send_in_business_hours: Respect prospect's business hours: "on" or "off".
        active_days: Active send days as comma-separated numbers (0=Mon, 6=Sun).
            E.g., "0,1,2,3,4" for weekdays. Leave empty to keep current.
    """
    from .tools.edit_campaign import run_edit_campaign

    logger.info(f"Running edit_campaign: campaign={campaign_id}, name={name}, mode={mode}")
    try:
        return await run_edit_campaign(
            campaign_id, name, mode, booking_link,
            offerings, case_studies, social_proofs, campaign_preferences,
            voice_mode, voice_noise, voice_humanize,
            enable_profile_views=enable_profile_views,
            enable_follows=enable_follows,
            enable_endorsements=enable_endorsements,
            enable_engagements=enable_engagements,
            enable_followups=enable_followups,
            enable_auto_replies=enable_auto_replies,
            enable_invitations=enable_invitations,
            engagement_mode=engagement_mode,
            max_followups=max_followups,
            followup_delay_days=followup_delay_days,
            withdraw_stale_invites=withdraw_stale_invites,
            stale_invite_days=stale_invite_days,
            send_in_business_hours=send_in_business_hours,
            active_days=active_days,
        )
    except Exception as e:
        logger.error(f"edit_campaign failed: {e}", exc_info=True)
        return f"Edit failed: {e}"


# ──────────────────────────────────────────────
# Tool: prospect (consolidated)
# ──────────────────────────────────────────────

@mcp.tool()
async def prospect(
    action: str,
    outreach_id: str = "",
    campaign_id: str = "",
    outcome: str = "won",
    reason: str = "",
    meeting_link: str = "",
) -> str:
    """Manage prospects — skip, close with outcome, view conversation, or timeline.

    Args:
        action: What to do:
            "skip"         — Remove prospect from the outreach queue
            "close"        — Record outcome (won/lost/opt_out) for an outreach
            "conversation" — View the full message thread with a prospect
            "timeline"     — View chronological journey of all actions for a prospect
        outreach_id: The outreach ID. Auto-selects if empty (except 'conversation'/'timeline').
        campaign_id: Which campaign (for 'skip'). Uses active if empty.
        outcome: 'won', 'lost', or 'opt_out' (for 'close').
        reason: Optional notes for the outcome (for 'close').
        meeting_link: Meeting/calendar URL if outcome is 'won' (for 'close').
            This is the URL where the meeting was booked — could be
            the user's booking page or the prospect's shared calendar.
    """
    from .tools.prospect import run_prospect

    logger.info(f"Running prospect: action={action}, outreach={outreach_id}")
    try:
        return await run_prospect(action, outreach_id, campaign_id, outcome, reason, meeting_link)
    except Exception as e:
        logger.error(f"prospect failed: {e}", exc_info=True)
        return f"Prospect action failed: {e}"


# ──────────────────────────────────────────────
# Tool: analytics (consolidated)
# ──────────────────────────────────────────────

@mcp.tool()
async def analytics(
    action: str = "report",
    campaign_id: str = "",
    campaign_ids: str = "",
    format: str = "table",
) -> str:
    """Campaign analytics — reports, comparisons, and exports.

    Args:
        action: What to do:
            "report"  — Detailed analytics with outcomes, conversion rates, stale leads
            "compare" — Compare 2+ campaigns side by side
            "export"  — Export campaign results as table, CSV, or JSON
        campaign_id: Which campaign. Uses active if empty.
        campaign_ids: Comma-separated IDs (for 'compare'). Compares all if empty.
        format: Output format for 'export': 'table', 'csv', or 'json'.
    """
    from .tools.analytics import run_analytics

    logger.info(f"Running analytics: action={action}, campaign={campaign_id}")
    try:
        return await run_analytics(action, campaign_id, campaign_ids, format)
    except Exception as e:
        logger.error(f"analytics failed: {e}", exc_info=True)
        return f"Analytics failed: {e}"








# ──────────────────────────────────────────────
# Tool: scheduler (consolidated)
# ──────────────────────────────────────────────

@mcp.tool()
async def scheduler(
    action: str = "status",
    enabled: bool = True,
    cloud: bool = False,
    hours: int = 24,
    event_type: str = "",
    campaign_id: str = "",
) -> str:
    """Manage the autonomous scheduler — view status or toggle on/off.

    Args:
        action: What to do:
            "status" — Show scheduler status, pending jobs, and recent activity
            "toggle" — Enable or disable the scheduler
            "always_on" — Enable/disable always-on mode (auto-re-enable + immediate email alerts)
            "logs" — Event log with job metrics and recent failures
            "activity" — Real action results from DB: what happened, what didn't, and why
            "diagnostics" — Full system diagnostics: rate limits, timers, blockers
            "report" — Configure periodic email campaign reports
        enabled: True to enable, False to disable (for 'toggle').
            For 'report': True to enable email reports, False to disable.
        cloud: If True, toggle the cloud scheduler for 24/7 operation (for 'toggle').
        hours: Lookback window in hours for 'logs' and 'activity' (default 24).
            For 'report': report interval in hours (1, 2, 4, 8, or 24).
        event_type: Filter events by type for 'logs'.
            For 'report': recipient email (empty = use login email).
        campaign_id: Filter by campaign for 'logs', 'activity', and 'diagnostics'.
    """
    from .tools.scheduler import run_scheduler

    logger.info(f"Running scheduler: action={action}")
    try:
        return await run_scheduler(
            action, enabled=enabled, cloud=cloud,
            hours=hours, event_type=event_type, campaign_id=campaign_id,
        )
    except Exception as e:
        logger.error(f"scheduler failed: {e}", exc_info=True)
        return f"Scheduler action failed: {e}"


# ──────────────────────────────────────────────
# Tool 29: create_post
# ──────────────────────────────────────────────

@mcp.tool()
async def create_post(
    topic: str = "",
    tone: str = "professional",
    mode: str = "autopilot",
) -> str:
    """Generate and publish a voice-matched LinkedIn post.

    Creates LinkedIn posts using your voice signature for social selling.
    Builds authority and drives inbound connections. Supports content
    creation for thought leadership and prospect engagement.

    Args:
        topic: What to post about (e.g., "share a tip about cold outreach",
            "comment on AI in sales", "share a success story").
        tone: Post tone: "professional", "casual", "thought-leader", "storytelling".
        mode: "autopilot" (publishes immediately).
    """
    from .tools.create_post import run_create_post

    logger.info(f"Running create_post: topic={topic}, tone={tone}, mode={mode}")
    try:
        return await run_create_post(topic, tone, mode)
    except Exception as e:
        logger.error(f"create_post failed: {e}", exc_info=True)
        return f"Post creation failed: {e}"


# ──────────────────────────────────────────────
# Tool 30: brand_strategy
# ──────────────────────────────────────────────

@mcp.tool()
async def brand_strategy(
    action: str = "analyze",
    focus: str = "",
    photo: str = "",
) -> str:
    """Analyze and improve your LinkedIn personal brand to drive more leads.

    Audits your profile, generates a personal brand strategy, executes
    actions (post topics, headline rewrites, engagement targets), and
    tracks improvement over time.

    Args:
        action: What to do:
            "analyze" — Full profile audit with scored areas and issues
            "plan"    — Generate a 4-week brand strategy with content calendar
            "execute" — Execute the next recommended action from your plan
            "progress" — Show before/after metrics and completed actions
            "upload_photo" — Upload a profile photo (provide file_path or base64 data)
            "upload_cover" — Upload a cover/banner photo (same input as upload_photo)
            "set_link" — Set custom CTA link on profile (pass URL via focus param)
        focus: Focus area for analyze/plan ("headline", "summary", "content", "engagement", ""),
            or URL string for set_link action.
        photo: File path or base64-encoded image for upload_photo / upload_cover actions.
    """
    from .tools.brand_strategy import run_brand_strategy

    logger.info("Running brand_strategy: action=%s, focus=%s", action, focus)
    try:
        return await run_brand_strategy(action, focus, photo)
    except Exception as e:
        logger.error("brand_strategy failed: %s", e, exc_info=True)
        return f"Brand strategy failed: {e}"


# ──────────────────────────────────────────────
# Tool 31: profile (change history + restore)
# ──────────────────────────────────────────────

@mcp.tool()
async def profile(
    action: str = "history",
    field: str = "",
    change_id: str = "",
    limit: int = 20,
) -> str:
    """View and restore LinkedIn profile change history.

    Every profile edit is tracked so you can see what changed and roll back
    if needed.  Supported fields: headline, summary, photo, cover_photo,
    custom_link, location, skills, experience.

    Args:
        action: What to do:
            "history"  — List recent profile changes (default)
            "restore"  — Revert a specific change by its ID
            "current"  — Show current cached profile snapshot
        field: Filter history by field name (e.g. "headline", "summary", "photo",
            "cover_photo", "custom_link", "location", "skills", "experience"). Optional.
        change_id: The change ID to restore (required for "restore" action).
        limit: Max number of history entries to show (default 20).
    """
    from .tools.profile_history import run_profile

    logger.info("Running profile: action=%s, field=%s, change_id=%s", action, field, change_id)
    try:
        return await run_profile(action, field, change_id, limit)
    except Exception as e:
        logger.error("profile failed: %s", e, exc_info=True)
        return f"Profile action failed: {e}"


# ──────────────────────────────────────────────
# Tool 32: import_prospects
# ──────────────────────────────────────────────

@mcp.tool()
async def import_prospects(
    campaign_id: str = "",
    csv_data: str = "",
    linkedin_enrich: bool = False,
) -> str:
    """Import prospects from CSV data into a campaign.

    Paste CSV text with prospect information and HeyLead will parse it,
    deduplicate against existing contacts and LinkedIn connections, score
    each prospect, and add them to the campaign for outreach.

    Supports CSV import, bulk prospect upload, lead list import,
    and contact list management for LinkedIn outreach campaigns.

    Args:
        campaign_id: Campaign to import into. Leave empty for the most recent.
        csv_data: CSV text with headers. Auto-detects columns:
            Name, Title, Company, LinkedIn URL, Email, Location.
            Must have Name + at least one of: Title, Company, or LinkedIn URL.
        linkedin_enrich: If true, fetch full LinkedIn profiles for imported
            prospects (slower but better personalization). Default: false.
    """
    from .tools.import_prospects import run_import_prospects

    logger.info("Running import_prospects: %d chars CSV", len(csv_data))
    try:
        return await run_import_prospects(campaign_id, csv_data, linkedin_enrich)
    except Exception as e:
        logger.error("import_prospects failed: %s", e, exc_info=True)
        return f"Import failed: {e}"


# ──────────────────────────────────────────────
# Tool 32: crm_sync
# ──────────────────────────────────────────────

@mcp.tool()
async def crm_sync(
    campaign_id: str = "",
    filter: str = "won",
    hubspot_api_key: str = "",
) -> str:
    """Sync campaign contacts and deals to HubSpot CRM.

    Pushes won deals, hot leads, or all contacts to HubSpot as contacts + deals.
    Tracks sync status to avoid duplicates. Includes conversation history as notes.
    Supports CRM integration, deal pipeline sync, and lead handoff to sales teams.

    First-time setup: create a HubSpot Private App with CRM scopes
    (contacts, deals, notes), then pass the access token here.
    The key is saved for future syncs.

    Args:
        campaign_id: Campaign to sync. Uses the most recent if empty.
        filter: Which contacts to sync: "won" (default), "hot_leads", or "all".
        hubspot_api_key: Optional — your HubSpot Private App access token.
            Only needed on first use; saved for future syncs.
    """
    from .tools.crm_sync import run_crm_sync

    logger.info("Running crm_sync: campaign=%s, filter=%s", campaign_id, filter)
    try:
        return await run_crm_sync(campaign_id, filter, hubspot_api_key)
    except Exception as e:
        logger.error("crm_sync failed: %s", e, exc_info=True)
        return f"CRM sync failed: {e}"


# ──────────────────────────────────────────────
# Signal-Based Selling (v1.0)
# ──────────────────────────────────────────────


@mcp.tool()
async def manage_watchlist(
    action: str = "list",
    name: str = "",
    watch_type: str = "keyword",
    keywords: str = "",
    watchlist_id: str = "",
    campaign_id: str = "",
) -> str:
    """Add, remove, and list signal keyword watchlists.

    Watchlists define keywords that HeyLead monitors on LinkedIn
    to detect buying signals from prospect posts. Watchlists are
    also auto-created when you generate an ICP.

    Args:
        action: What to do: 'list', 'add', 'remove', 'pause', 'resume'.
        name: Watchlist name (for 'add').
        watch_type: 'keyword' or 'competitor' (for 'add').
        keywords: Comma-separated keywords (for 'add'). E.g., "cold outreach, SDR automation".
        watchlist_id: Watchlist ID (for 'remove', 'pause', 'resume').
        campaign_id: Optional campaign to link the watchlist to.
    """
    from .tools.manage_watchlist import run_manage_watchlist

    logger.info("Running manage_watchlist: action=%s", action)
    try:
        return await run_manage_watchlist(action, name, watch_type, keywords, watchlist_id, campaign_id)
    except Exception as e:
        logger.error("manage_watchlist failed: %s", e, exc_info=True)
        return f"Watchlist management failed: {e}"


@mcp.tool()
async def signals(
    action: str = "show",
    campaign_id: str = "",
    signal_type: str = "",
    status: str = "",
    limit: int = 20,
    days: int = 30,
    signal_id: str = "",
    feedback: str = "",
) -> str:
    """View and analyze buying signals from LinkedIn.

    Args:
        action: What to do:
            "show"     — Display detected buying signals (keyword mentions, job changes, etc.)
            "report"   — Signal analytics report with trends and ROI
            "strategy" — Show strategy engine insights, patterns, and autonomous actions
            "feedback" — Mark a signal as 'useful' or 'not_useful' (improves future classification)
            "website_setup" — Set up website visitor tracking (generates JS snippet to embed)
            "website_stats" — View website tracking analytics (visits, companies, high-intent)
            "optimize" — Run signal self-optimization (weights, keywords, warmup, thresholds)
            "optimize_history" — View optimization change log with rollback IDs
            "optimize_rollback" — Rollback a specific optimization change by entry ID
            "optimize_weights" — Show all signal weights (default vs effective overrides)
        campaign_id: Filter by campaign. Shows all if empty.
        signal_type: Filter by signal type, e.g. 'keyword_mention', 'job_change' (for 'show').
            For 'optimize_history': filter by optimization type (weight, keyword_added, warmup, threshold).
        status: Filter by status: 'new', 'classified', 'actioned' (for 'show').
        limit: Max signals to show (for 'show'). Default 20.
        days: Lookback window in days (for 'report'). Default 30.
        signal_id: Signal ID (for 'feedback' action). Entry ID (for 'optimize_rollback').
        feedback: 'useful' or 'not_useful' (for 'feedback' action).
    """
    from .tools.signals import run_signals

    logger.info("Running signals: action=%s", action)
    try:
        return await run_signals(
            action, campaign_id, signal_type, status, limit, days,
            signal_id=signal_id, feedback=feedback,
        )
    except Exception as e:
        logger.error("signals failed: %s", e, exc_info=True)
        return f"Signals failed: {e}"


@mcp.tool()
async def partner(
    action: str = "list",
    name: str = "",
    company: str = "",
    email: str = "",
    context: str = "",
    next_followup: str = "",
    partner_id: str = "",
    note: str = "",
    days: int = 0,
) -> str:
    """Track follow-ups with business partners, vendors, and investors.

    Manages a CRM-style pipeline for non-prospect relationships (e.g., API
    vendors, investors, co-founders). Auto-sends email reminders when
    follow-ups are due using an escalating cadence (1, 3, 7, 14, 21 days).

    Args:
        action: What to do:
            "add"      — Add a new partner to track (auto-schedules follow-ups)
            "list"     — Show all active partner follow-ups with due dates
            "update"   — Update partner info or add a note
            "complete" — Mark a partner follow-up as done (got what you needed)
            "snooze"   — Push the next follow-up by N days
            "cancel"   — Stop tracking this partner
        name: Partner's name (for 'add'). E.g., "Julien Crépieux".
        company: Company name (for 'add'). E.g., "Unipile".
        email: Partner's email (for 'add'). E.g., "julien@unipile.com".
        context: What you're following up about (for 'add').
        next_followup: Next follow-up date as YYYY-MM-DD (for 'add'). Defaults to tomorrow.
        partner_id: Partner ID (for 'update', 'complete', 'snooze', 'cancel').
        note: Add a note to the partner record (for 'update').
        days: Number of days to snooze (for 'snooze'). Default 7.
    """
    from .tools.partner_followup import run_partner

    logger.info("Running partner: action=%s", action)
    try:
        return await run_partner(action, name, company, email, context, next_followup, partner_id, note, days)
    except Exception as e:
        logger.error("partner failed: %s", e, exc_info=True)
        return f"Partner tracking failed: {e}"


@mcp.tool()
async def contacts(
    action: str = "list",
    query: str = "",
    contact_id: str = "",
    lifecycle_stage: str = "",
    tag: str = "",
    note: str = "",
    min_fit_score: float = 0.0,
    limit: int = 25,
    format: str = "table",
) -> str:
    """Search, browse, and manage your global contact base.

    One master record per person across all campaigns. View full interaction
    history, add tags/notes, track lifecycle stages, and build reusable
    prospect pools for future campaigns. Also search LinkedIn directly
    for people without creating a campaign.

    Args:
        action: What to do:
            "list"    — List contacts with optional filters (default)
            "search"  — Search contacts by name, company, or title
            "view"    — View full cross-campaign history for one contact
            "tag"     — Add a tag (or remove with '-tag_name')
            "note"    — Add a note to a contact
            "stage"   — Update lifecycle stage
            "stats"   — Contact base dashboard stats
            "export"  — Export contacts as table, CSV, or JSON
            "linkedin_search" — Search LinkedIn directly by name/company/title
            "enrich" — Enrich contacts with full LinkedIn profiles + posts
            "my_connections" — Search your 1st-degree LinkedIn connections (locally synced, guaranteed 1st degree)
        query: Search text for 'search', 'linkedin_search', and 'my_connections' actions.
            For 'enrich': search query to find contacts to enrich.
        contact_id: Global contact ID for view/tag/note/stage actions.
        lifecycle_stage: Filter by stage (prospect/contacted/connected/engaged/customer/lost)
            or target stage for 'stage' action.
        tag: Tag to add/remove for 'tag' action, or filter for 'list'/'search'.
        note: Note text for 'note' action.
        min_fit_score: Minimum fit score filter (0.0-1.0).
        limit: Max results to return (default 25).
        format: Output format for 'export': 'table', 'csv', or 'json'.
    """
    from .tools.contacts import run_contacts

    logger.info("Running contacts: action=%s", action)
    try:
        return await run_contacts(
            action=action, query=query, contact_id=contact_id,
            lifecycle_stage=lifecycle_stage, tag=tag, note=note,
            min_fit_score=min_fit_score, limit=limit, format=format,
        )
    except Exception as e:
        logger.error("contacts failed: %s", e, exc_info=True)
        return f"Contact management failed: {e}"


@mcp.tool()
async def network(
    action: str = "status",
    linkedin_id: str = "",
    linkedin_ids: str = "",
    query: str = "",
    title: str = "",
    max_accounts: int = 5,
    force_refresh: bool = False,
    insight_type: str = "",
    segment: str = "",
    min_confidence: float = 0.0,
) -> str:
    """Network Intelligence — leverage all connected accounts as a distributed pool.

    Use all LinkedIn accounts as "network sensors" for enrichment, search,
    network analysis, and anonymized message insights.

    Args:
        action: What to do:
            "status"     — Pool health, member accounts, your participation
            "opt_in"     — Join the network pool (share your connections for team intelligence)
            "opt_out"    — Leave the network pool
            "sync"       — Refresh your connection graph snapshot
            "opt_in_all" — Admin: opt in all connected LinkedIn accounts
            "sync_all"   — Admin: sync connections for all pool accounts
            "enrich"     — Smart profile lookup via closest-connected account
            "contact"    — Get email/phone via 1st-degree connected account
            "parallel"   — Enrich up to 100 profiles in parallel across pool
            "search"     — Distributed search across pool (merged, deduplicated)
            "reach"      — Show which pool accounts can reach a prospect
            "intros"     — Find warm introduction paths to a prospect
            "insights"   — Query aggregated message insights (objections, trends, patterns)
            "trends"     — Industry trend analysis from cross-account conversations
            "patterns"   — Objection and response patterns with timing data
        linkedin_id: Target prospect's LinkedIn provider_id (for enrich/contact/reach/intros).
        linkedin_ids: Comma-separated LinkedIn IDs (for parallel action).
        query: Search keywords (for search action).
        title: Job title filter (for search action).
        max_accounts: Max pool accounts to use for search (default 5).
        force_refresh: Ignore cache for enrich (default False).
        insight_type: Filter insights by type (for insights/patterns actions).
        segment: Filter by industry:seniority segment (for insights/trends actions).
        min_confidence: Minimum confidence threshold 0.0-1.0 (for insights action).
    """
    from .tools.network import run_network

    logger.info("Running network: action=%s", action)
    try:
        return await run_network(
            action=action, linkedin_id=linkedin_id, linkedin_ids=linkedin_ids,
            query=query, title=title, max_accounts=max_accounts,
            force_refresh=force_refresh,
            insight_type=insight_type, segment=segment,
            min_confidence=min_confidence,
        )
    except Exception as e:
        logger.error("network failed: %s", e, exc_info=True)
        return f"Network intelligence failed: {e}"


@mcp.tool()
async def inbox(
    action: str = "list",
    chat_id: str = "",
    name: str = "",
    limit: int = 30,
    text: str = "",
) -> str:
    """Browse and read LinkedIn inbox messages directly.

    Read any conversation in your LinkedIn inbox, not just campaign contacts.

    Args:
        action: What to do:
            "list" — List recent conversations with last message preview
            "read" — Read full conversation thread
            "reply" — Send a message to any inbox conversation
        chat_id: Chat ID to read (from list output). For 'read' and 'reply' actions.
        name: Contact name to search for (partial match). For 'read' and 'reply' actions.
        limit: Max conversations (list) or messages (read) to show. Default 30.
        text: Message text to send. Required for 'reply' action.
    """
    from .tools.inbox import run_inbox

    logger.info("Running inbox: action=%s, name=%s", action, name)
    try:
        return await run_inbox(action=action, chat_id=chat_id, name=name, limit=limit, text=text)
    except Exception as e:
        logger.error("inbox failed: %s", e, exc_info=True)
        return f"Inbox failed: {e}"


@mcp.tool()
async def backfill_inbox(
    limit: int = 50,
    dry_run: bool = True,
    min_confidence: float = 0.0,
    send_only: bool = False,
) -> str:
    """Process unreplied LinkedIn inbox messages through the inbound pipeline.

    Scans your inbox for conversations where prospects messaged you but
    never got a reply. Classifies each message and sends discovery DMs.

    Args:
        limit: Max conversations to scan (default 50).
        dry_run: If True (default), only classify — don't send DMs. Set False to send.
        min_confidence: Only send DMs for signals >= this confidence (0.0-1.0).
        send_only: If True, skip inbox scan — process already-classified signals
            directly. Use after a dry_run to avoid re-scanning.
    """
    from .tools.backfill_inbox import run_backfill_inbox

    logger.info("Running backfill_inbox: limit=%d, dry_run=%s, send_only=%s", limit, dry_run, send_only)
    try:
        return await run_backfill_inbox(
            limit=limit, dry_run=dry_run, min_confidence=min_confidence,
            send_only=send_only,
        )
    except Exception as e:
        logger.error("backfill_inbox failed: %s", e, exc_info=True)
        return f"Backfill failed: {e}"


# ──────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────

def main(transport: str = "stdio", host: str = "0.0.0.0", port: int = 8080) -> None:
    """Run the HeyLead MCP server.

    Args:
        transport: Transport type — "stdio", "sse", or "streamable-http".
        host: Host to bind to for HTTP transports. Default: 0.0.0.0.
        port: Port to bind to for HTTP transports. Default: 8080.
    """
    logger.info(f"Starting HeyLead MCP server v{__version__} (transport={transport})")

    # Ensure directories and DB exist on first run
    config.ensure_dirs()

    # Initialize the database
    from .db.schema import get_db
    db = get_db()
    db.close()

    # Pre-populate account_id cache while still in sync context
    # (avoids sync DB calls on the event loop later)
    from .linkedin import get_account_id
    get_account_id()

    # Configure HTTP transport settings if needed
    if transport in ("sse", "streamable-http"):
        mcp.settings.host = host
        mcp.settings.port = port
        logger.info(f"HTTP server binding to {host}:{port}")

    # Run MCP server
    mcp.run(transport=transport)
