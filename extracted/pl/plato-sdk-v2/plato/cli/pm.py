"""Project Management CLI commands for Plato simulator workflow."""

import asyncio
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import httpx
import typer
import yaml
from rich.table import Table

from plato._generated.api.v1.env import create_simulator, get_simulator_by_name, get_simulators
from plato._generated.api.v1.env import update_simulator as env_update_simulator
from plato._generated.api.v1.organization import get_organization_members
from plato._generated.api.v1.simulator import (
    add_simulator_review,
    update_simulator,
    update_simulator_status,
    update_tag,
)
from plato._generated.models import (
    AddReviewRequest,
    AppApiV1EnvRoutesUpdateSimulatorRequest,
    AppApiV1SimulatorRoutesUpdateSimulatorRequest,
    Authentication,
    CreateSimulatorRequest,
    Outcome,
    ReviewType,
    SimReviewComment,
    SimulatorConfig,
    Status,
    UpdateStatusRequest,
    UpdateTagRequest,
)
from plato.cli.utils import (
    console,
    handle_async,
    read_plato_config,
    require_api_key,
    require_plato_config_field,
    safe_print,
)
from plato.utils.sim_config import sim_config_dict
from plato.v1.flow_executor import FlowExecutor
from plato.v1.models.flow import Flow
from plato.v1.sdk import Plato
from plato.v2 import Env as EnvV2
from plato.v2 import Plato as PlatoV2

# =============================================================================
# CONSTANTS
# =============================================================================

# UUID pattern for detecting artifact IDs in sim:artifact notation
UUID_PATTERN = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE)

CHRONOS_URL = "https://chronos.plato.so"
DEFAULT_DATAGEN_API_KEY = os.getenv("PLATO_DATAGEN_API_KEY", "")
DEFAULT_ANCHOR_KEY = os.getenv("ANCHOR_API_KEY", "")
DEFAULT_BROWSERBASE_KEY = os.getenv("BROWSERBASE_API_KEY", "")

# Keychain service name used by Claude Code to store OAuth credentials
_CLAUDE_KEYCHAIN_SERVICE = "Claude Code-credentials"


def _sanitize_mcp_name(raw: str) -> str:
    """Coerce an arbitrary identifier into a valid MCP name (alphanumeric + underscore)."""
    cleaned = re.sub(r"[^a-zA-Z0-9_]+", "_", raw).strip("_")
    return cleaned or "db"


def _db_mcp_name(db: dict) -> str:
    """Build an MCP name from `{db_database}_{db_schema}` (schema defaults to `base`)."""
    database = _sanitize_mcp_name(db.get("db_database") or "db")
    schema = _sanitize_mcp_name(db.get("db_schema") or "base")
    return f"{database}_{schema}"


def _build_unique_db_mcp_names(db_configs: list[dict]) -> list[str]:
    """Return one MCP name per db_config, raising if any two collide.

    Two configs collide when they share both `db_database` and `db_schema`
    (including the case where neither sets a schema — both default to `base`).
    """
    names = [_db_mcp_name(db) for db in db_configs]
    first_seen: dict[str, int] = {}
    collisions: list[str] = []
    for i, (db, name) in enumerate(zip(db_configs, names)):
        if name in first_seen:
            other = db_configs[first_seen[name]]
            collisions.append(
                f"{name} (db_database={db.get('db_database')!r}, "
                f"db_schema={db.get('db_schema')!r}; also produced by entry "
                f"with db_database={other.get('db_database')!r}, "
                f"db_schema={other.get('db_schema')!r})"
            )
        else:
            first_seen[name] = i
    if collisions:
        raise ValueError(
            "Duplicate db MCP names — every db_config must have a unique "
            f"(db_database, db_schema) tuple. Collisions: {'; '.join(collisions)}"
        )
    return names


def _get_claude_credentials() -> tuple[str, str]:
    """Get Claude credentials, preferring OAuth from Keychain, falling back to API key.

    Returns:
        (config_key, value) — either ("claude_oauth_credentials", "<json>")
        or ("anthropic_api_key", "<key>").
    """
    # 1. Try macOS Keychain for OAuth credentials (macOS only)
    if sys.platform == "darwin":
        try:
            raw = subprocess.run(
                ["security", "find-generic-password", "-s", _CLAUDE_KEYCHAIN_SERVICE, "-w"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if raw.returncode == 0 and raw.stdout.strip():
                creds = json.loads(raw.stdout.strip())
                # Show token expiry info
                oauth = creds.get("claudeAiOauth", {})
                expires_at = oauth.get("expiresAt")
                expiry_msg = ""
                if expires_at:
                    try:
                        exp_dt = datetime.fromtimestamp(expires_at / 1000)
                        remaining = exp_dt - datetime.now()
                        mins = int(remaining.total_seconds() / 60)
                        if mins < 0:
                            expiry_msg = f" [yellow](expired {-mins}m ago!)[/yellow]"
                        elif mins < 60:
                            expiry_msg = f" [yellow](expires in {mins}m)[/yellow]"
                        else:
                            expiry_msg = f" [dim](expires in {mins // 60}h {mins % 60}m)[/dim]"
                    except (ValueError, TypeError, OSError):
                        pass
                console.print(f"[green]Using Claude OAuth from Keychain[/green]{expiry_msg}")
                return "claude_oauth_credentials", json.dumps(creds, separators=(",", ":"))
        except (FileNotFoundError, PermissionError, subprocess.TimeoutExpired, json.JSONDecodeError):
            pass

    # 2. Try ~/.claude/.credentials.json (written by `claude` CLI login on any platform)
    creds_path = Path.home() / ".claude" / ".credentials.json"
    if creds_path.exists():
        try:
            creds = json.loads(creds_path.read_text())
            oauth = creds.get("claudeAiOauth", {})
            if oauth:
                expires_at = oauth.get("expiresAt")
                expiry_msg = ""
                if expires_at:
                    try:
                        exp_dt = datetime.fromtimestamp(expires_at / 1000)
                        remaining = exp_dt - datetime.now()
                        mins = int(remaining.total_seconds() / 60)
                        if mins < 0:
                            expiry_msg = f" [yellow](expired {-mins}m ago!)[/yellow]"
                        elif mins < 60:
                            expiry_msg = f" [yellow](expires in {mins}m)[/yellow]"
                        else:
                            expiry_msg = f" [dim](expires in {mins // 60}h {mins % 60}m)[/dim]"
                    except (ValueError, TypeError, OSError):
                        pass
                console.print(f"[green]Using Claude OAuth from credentials file[/green]{expiry_msg}")
                return "claude_oauth_credentials", json.dumps(creds, separators=(",", ":"))
        except (PermissionError, json.JSONDecodeError):
            pass

    # 3. Fall back to ANTHROPIC_API_KEY env var
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    if api_key:
        masked = api_key[:10] + "..." + api_key[-4:] if len(api_key) > 14 else "****"
        console.print(f"[cyan]Using ANTHROPIC_API_KEY from environment[/cyan] [dim]({masked})[/dim]")
        return "anthropic_api_key", api_key

    console.print(
        "[yellow]Warning: No Claude credentials found. Run 'claude' to authenticate or set ANTHROPIC_API_KEY.[/yellow]"
    )
    return "anthropic_api_key", ""


def _set_claude_credentials(config: dict, key: str, value: str) -> None:
    """Set the appropriate credential key on a config dict, removing the stale one."""
    config[key] = value
    # Remove the other credential key to avoid stale placeholders
    other_key = "anthropic_api_key" if key == "claude_oauth_credentials" else "claude_oauth_credentials"
    config.pop(other_key, None)


DEFAULT_DATA_ASSIGNEES = [771]
DEFAULT_DATA_REVIEW_ASSIGNEES = [32]

# =============================================================================
# APP STRUCTURE
# =============================================================================

pm_app = typer.Typer(help="Project management for simulator workflow")
list_app = typer.Typer(help="List simulators by status")
review_app = typer.Typer(help="Review simulator artifacts")
submit_app = typer.Typer(help="Submit simulator artifacts for review")
start_app = typer.Typer(help="Start env or data pipelines for simulators")
register_app = typer.Typer(help="Create or complete simulator records")
experiment_app = typer.Typer(help="Manage experiment configs in Chronos")
experiment_env_app = typer.Typer(help="Env pipeline experiments")
experiment_env_base_app = typer.Typer(help="Env base (fresh create) experiment")
experiment_env_fix_app = typer.Typer(help="Env fix experiment")
experiment_data_app = typer.Typer(help="Data pipeline experiments")
experiment_data_base_app = typer.Typer(help="Data base experiment")
experiment_data_unified_app = typer.Typer(help="Data unified (multi-sim) experiment")
experiment_check_app = typer.Typer(help="Sim-checker experiments")
experiment_check_base_app = typer.Typer(help="Sim-checker base experiment")
experiment_blank_app = typer.Typer(help="Blankdata pipeline experiments")
experiment_blank_base_app = typer.Typer(
    help="Simcreator-blank base experiment (used by `start blank` and by env-create/env-fix's chain step)"
)
experiment_agent_app = typer.Typer(help="AgentSession experiments")
experiment_agent_data_load_app = typer.Typer(help="Agent data-load experiment")

pm_app.add_typer(list_app, name="list")
pm_app.add_typer(review_app, name="review")
pm_app.add_typer(submit_app, name="submit")
pm_app.add_typer(start_app, name="start")
pm_app.add_typer(register_app, name="register")
pm_app.add_typer(experiment_app, name="experiment")
experiment_app.add_typer(experiment_env_app, name="env")
experiment_app.add_typer(experiment_data_app, name="data")
experiment_app.add_typer(experiment_check_app, name="check")
experiment_app.add_typer(experiment_blank_app, name="blank")
experiment_app.add_typer(experiment_agent_app, name="agent")
experiment_env_app.add_typer(experiment_env_base_app, name="base")
experiment_env_app.add_typer(experiment_env_fix_app, name="fix")
experiment_data_app.add_typer(experiment_data_base_app, name="base")
experiment_data_app.add_typer(experiment_data_unified_app, name="unified")
experiment_check_app.add_typer(experiment_check_base_app, name="base")
experiment_blank_app.add_typer(experiment_blank_base_app, name="base")
experiment_agent_app.add_typer(experiment_agent_data_load_app, name="data-load")


# =============================================================================
# SHARED HELPERS
# =============================================================================


def parse_simulator_artifact(
    simulator: str | None,
    artifact: str | None,
    require_artifact: bool = False,
    command_name: str = "command",
) -> tuple[str | None, str | None]:
    """
    Parse simulator and artifact from CLI args, supporting colon notation.

    Supports:
        -s simulator                    # Simulator only
        -s simulator -a <artifact-uuid> # Explicit artifact
        -s simulator:<artifact-uuid>    # Colon notation

    Args:
        simulator: The -s/--simulator arg value
        artifact: The -a/--artifact arg value
        require_artifact: If True, artifact is required
        command_name: Name of command for error messages

    Returns:
        (simulator_name, artifact_id) tuple
    """
    simulator_name = None
    artifact_id = artifact or ""

    if simulator:
        # Check for colon notation: sim:artifact
        if ":" in simulator:
            sim_part, colon_part = simulator.split(":", 1)
            simulator_name = sim_part
            if UUID_PATTERN.match(colon_part):
                artifact_id = colon_part
            else:
                console.print(f"[red]❌ Invalid artifact UUID after colon: '{colon_part}'[/red]")
                console.print()
                console.print("[yellow]Usage:[/yellow]")
                console.print(f"  plato pm {command_name} -s <simulator>                      # Simulator only")
                console.print(f"  plato pm {command_name} -s <simulator> -a <artifact-uuid>   # With artifact")
                console.print(f"  plato pm {command_name} -s <simulator>:<artifact-uuid>      # Colon notation")
                raise typer.Exit(1)
        else:
            simulator_name = simulator

    if not simulator_name:
        console.print("[red]❌ Simulator name is required[/red]")
        console.print()
        console.print("[yellow]Usage:[/yellow]")
        console.print(f"  plato pm {command_name} -s <simulator>                      # Simulator only")
        console.print(f"  plato pm {command_name} -s <simulator> -a <artifact-uuid>   # With artifact")
        console.print(f"  plato pm {command_name} -s <simulator>:<artifact-uuid>      # Colon notation")
        raise typer.Exit(1)

    if require_artifact and not artifact_id:
        console.print("[red]❌ Artifact ID is required[/red]")
        console.print()
        console.print("[yellow]Usage:[/yellow]")
        console.print(f"  plato pm {command_name} -s <simulator> -a <artifact-uuid>   # With artifact flag")
        console.print(f"  plato pm {command_name} -s <simulator>:<artifact-uuid>      # Colon notation")
        raise typer.Exit(1)

    return simulator_name, artifact_id or None


def _get_base_url() -> str:
    """Get base URL with /api suffix stripped."""
    base_url = os.getenv("PLATO_BASE_URL", "https://plato.so")
    if base_url.endswith("/api"):
        base_url = base_url[:-4]
    return base_url.rstrip("/")


def _split_sim_colon_arg(raw: str, command_name: str) -> tuple[str, str | None]:
    """Split a positional ``sim`` / ``sim:<uuid>`` arg for commands that take
    simulators as positional args (e.g. ``pm open``, ``pm start from-template``).

    Distinct from ``parse_simulator_artifact``, which prints usage guidance
    using the ``-s`` flag — that's misleading for commands where the simulator
    is a positional argument. Returns ``(sim_name, artifact_id_or_None)``.
    Raises ``typer.Exit`` on malformed colon notation.
    """
    if ":" not in raw:
        return raw, None
    sim_part, colon_part = raw.split(":", 1)
    if UUID_PATTERN.match(colon_part):
        return sim_part, colon_part
    console.print(f"[red]❌ Invalid artifact UUID after colon: '{colon_part}'[/red]")
    console.print()
    console.print("[yellow]Usage:[/yellow]")
    console.print(f"  plato pm {command_name} <simulator>                      # Simulator only")
    console.print(f"  plato pm {command_name} <simulator>:<artifact-uuid>      # Colon notation")
    console.print(f"  plato pm {command_name} <artifact-uuid>                  # Bare artifact UUID")
    raise typer.Exit(1)


def validate_status_transition(current_status: str, expected_status: str, command_name: str):
    """Validate that current status matches expected status for the command."""
    if current_status != expected_status:
        console.print(f"[red]❌ Invalid status for {command_name}[/red]")
        console.print(f"\n[yellow]Current status:[/yellow]  {current_status}")
        console.print(f"[yellow]Expected status:[/yellow] {expected_status}")
        console.print(f"\n[yellow]Cannot run {command_name} from status '{current_status}'[/yellow]")
        raise typer.Exit(1)


def _extract_review_comment_texts(review: dict) -> list[str]:
    """Extract comment text from a review, supporting both sim_comments and legacy comments."""
    sim_comments = review.get("sim_comments")
    if isinstance(sim_comments, list):
        comments = []
        for item in sim_comments:
            if not isinstance(item, dict):
                continue
            comment_text = (item.get("comment") or "").strip()
            if comment_text:
                comments.append(comment_text)
        return comments

    legacy_comments = (review.get("comments") or "").strip()
    return [legacy_comments] if legacy_comments else []


def _get_latest_rejected_env_review_comments(reviews: list[dict]) -> list[str]:
    """Get the latest rejected env-review comments."""
    rejected_env_reviews = [
        review
        for review in reviews
        if isinstance(review, dict) and review.get("review_type") == "env" and review.get("outcome") == "reject"
    ]
    rejected_env_reviews.sort(key=lambda review: review.get("timestamp_iso", ""), reverse=True)
    if not rejected_env_reviews:
        return []

    return _extract_review_comment_texts(rejected_env_reviews[0])


def _get_latest_rejected_data_review_comments(reviews: list[dict]) -> list[str]:
    """Get the latest rejected data-review comments."""
    rejected_data_reviews = [
        review
        for review in reviews
        if isinstance(review, dict) and review.get("review_type") == "data" and review.get("outcome") == "reject"
    ]
    rejected_data_reviews.sort(key=lambda review: review.get("timestamp_iso", ""), reverse=True)
    if not rejected_data_reviews:
        return []

    return _extract_review_comment_texts(rejected_data_reviews[0])


def _render_data_artifact_section(data_artifact_id: str | None) -> str:
    """Build the prose block injected as {data_artifact_section} into env-fix's `fix` step.

    Two variants — populated (reference available, agent can spin it up on demand)
    and empty (no data artifact attached, sim never went through datagen or hasn't
    yet). Rendered at CLI time rather than via runtime template logic so the agent
    never sees a literal {placeholder} or an awkward "if empty" branch.
    """
    if data_artifact_id:
        return (
            "## Two Environments — Diagnose on Data, Fix on Base\n\n"
            f"**Reference (data) artifact:** `{data_artifact_id}`\n\n"
            "The reviewer's feedback above describes what they saw on the **data artifact**, not on the empty base. "
            "Default workflow:\n\n"
            "1. **Reproduce the symptom on the data artifact** (read-only reference sandbox).\n"
            "2. **Once you have conviction about the cause, switch to the base sandbox and patch it there.**\n"
            "3. Two distinct VMs with distinct DB + filesystem state — don't mix them up.\n\n"
            "### Reproduce on the data ref\n\n"
            "```\n"
            f"plato sandbox start -a {data_artifact_id} -w /tmp/data-ref --json\n"
            "# every command targeting this sandbox needs -w /tmp/data-ref. Commands without it hit your base /workspace sandbox.\n"
            "plato sandbox state -w /tmp/data-ref --json | jq '.results[].state.db'\n"
            "plato sandbox flow -w /tmp/data-ref --headless --flow-name login\n"
            "ssh -F /tmp/data-ref/.plato/ssh_config sandbox   # for DB queries\n"
            "```\n\n"
            "Don't move on until you can describe the cause concretely. Then stop the ref so you don't "
            "accidentally run fix commands against it:\n\n"
            "```\n"
            "plato sandbox stop -w /tmp/data-ref\n"
            "```\n\n"
            "### Patch the base\n\n"
            "Apply the fix in /workspace as usual. All subsequent steps in this session (audit_verify, "
            "mutation_test, snapshot, cleanup) operate on /workspace.\n\n"
            "### When to skip the data ref\n\n"
            "If the reviewer feedback is unambiguously about something visible in base config files (e.g. "
            '"plato-config.yml is malformed", "wrong credentials in flows.yml") and you can see it '
            "immediately, skip. For any runtime symptom (login behavior, mutation patterns, endpoint "
            "errors, rendering bugs), boot the ref first.\n\n"
            "### Hard rules\n\n"
            "- The data ref is **READ-ONLY**. Don't snapshot it, don't modify it, don't run cleanup against it.\n"
            "- Every command on the ref uses `-w /tmp/data-ref`. Without that flag, commands hit the base — mixing them up is the most common way to waste an hour.\n"
            "- The output of THIS session is the **base** artifact only. The ref gets discarded."
        )
    return (
        "## Reference Data Artifact\n\n"
        "None — this sim has no data artifact attached. The fix runs against the base /workspace sandbox only."
    )


def _render_operator_message_section(message: str | None) -> str:
    """Build the prose block injected as {operator_message_section} into simcreator-blank's
    `plan` step. Empty string when no -m message was passed (omits the section entirely).
    """
    msg = (message or "").strip()
    if not msg:
        return ""
    return f"## Operator note\n\n{msg}\n\nHint, not spec. Trust your observations if they conflict.\n\n"


def _build_datagen_review_prompt(simulator_name: str, comments: list[str], base_prompt: str) -> str:
    """Wrap the base datagen prompt with reviewer feedback, matching the review extension."""
    comment_lines = "\n".join(f"  {i + 1}. {comment}" for i, comment in enumerate(comments))

    return (
        f"This is a REVIEW FOLLOW-UP for {simulator_name}. The application was previously populated with data, "
        "but a reviewer found issues that need to be fixed.\n\n"
        "== REVIEW COMMENTS (must be addressed FIRST) ==\n\n"
        f"{comment_lines or '  (No specific comments)'}\n\n"
        "== YOUR TASK ==\n\n"
        "Follow the same AUDIT → GENERATE workflow, but prioritize the review comments.\n\n"
        "In your AUDIT step:\n"
        "  - First check every review comment above against the current app state.\n"
        "  - Then do the full systematic audit (dashboard, all sections, detail tabs, diversity, links).\n"
        "  - Include both review-comment issues AND any new gaps in your gap report.\n\n"
        "In your GENERATE step:\n"
        "  - Fix review comment issues first — these are blocking.\n"
        "  - Then fix all other gaps from the audit.\n"
        "  - The reviewer checks EVERYTHING, not just what they listed. Any remaining gap will\n"
        "    cause another rejection.\n\n"
        "== ORIGINAL DATA GENERATION INSTRUCTIONS ==\n\n"
        f"{base_prompt}"
    )


# =============================================================================
# LIST COMMANDS
# =============================================================================


def _list_by_status(
    target_status: str, title: str, columns: list[dict], docker_app_only: bool = False, sort_by: str = "name"
):
    """Generic helper to list simulators filtered by status."""
    api_key = require_api_key()

    async def _list():
        base_url = _get_base_url()

        async with httpx.AsyncClient(base_url=base_url, timeout=60.0) as client:
            simulators = await get_simulators.asyncio(
                client=client,
                x_api_key=api_key,
            )

            # Fetch organization members to map user IDs to usernames
            user_id_to_name: dict[int, str] = {}
            try:
                members = await get_organization_members.asyncio(
                    client=client,
                    x_api_key=api_key,
                )
                for member in members:
                    user_id = member.get("id")
                    username = member.get("username") or member.get("email", "")
                    if user_id is not None:
                        user_id_to_name[user_id] = username
            except Exception:
                pass

            # Filter
            matched = []
            for sim in simulators:
                config = sim.get("config", {}) if isinstance(sim, dict) else getattr(sim, "config", {})
                if not isinstance(config, dict):
                    continue
                status = config.get("status", "not_started")
                if status != target_status:
                    continue
                if docker_app_only and config.get("type") != "docker_app":
                    continue
                matched.append(sim)

            if not matched:
                console.print(f"[yellow]No simulators with status '{target_status}'[/yellow]")
                return

            table = Table(title=f"{title} ({len(matched)})")
            for col in columns:
                col_kwargs = {k: v for k, v in col.items() if not k.startswith("_")}
                table.add_column(**col_kwargs)

            def _sort_key(s):
                cfg = s.get("config", {}) if isinstance(s, dict) else getattr(s, "config", {})
                if not isinstance(cfg, dict):
                    cfg = {}
                nm = (s.get("name") or getattr(s, "name", "")) if isinstance(s, dict) else getattr(s, "name", "")
                if sort_by == "name":
                    return (nm,)
                # Sort by config field (e.g. assignee list), then name
                val = cfg.get(sort_by, []) or []
                first = str(val[0]) if val else "zzz"
                return (first, nm)

            for sim in sorted(matched, key=_sort_key):
                if isinstance(sim, dict):
                    name = sim.get("name", "N/A")
                    config = sim.get("config", {})
                else:
                    name = getattr(sim, "name", "N/A")
                    config = getattr(sim, "config", {})

                row = []
                for col in columns:
                    key = col.get("_key", "")
                    if key == "name":
                        row.append(name)
                    elif key == "notes":
                        row.append(config.get("notes", "") or "-")
                    elif key == "source_code_url":
                        row.append(config.get("source_code_url", "") or "-")
                    elif key == "license":
                        row.append(config.get("license", "") or "-")
                    elif key in ("base_artifact_id", "data_artifact_id"):
                        row.append(config.get(key, "") or "-")
                    elif key == "env_assignees":
                        ids = config.get("env_assignees", []) or []
                        row.append(", ".join(user_id_to_name.get(uid, str(uid)) for uid in ids) or "-")
                    elif key == "env_review_assignees":
                        ids = config.get("env_review_assignees", []) or []
                        row.append(", ".join(user_id_to_name.get(uid, str(uid)) for uid in ids) or "-")
                    elif key == "data_assignees":
                        ids = config.get("data_assignees", []) or []
                        row.append(", ".join(user_id_to_name.get(uid, str(uid)) for uid in ids) or "-")
                    elif key == "data_review_assignees":
                        ids = config.get("data_review_assignees", []) or []
                        row.append(", ".join(user_id_to_name.get(uid, str(uid)) for uid in ids) or "-")
                    else:
                        row.append("-")
                table.add_row(*row)

            console.print(table)

    handle_async(_list())


# Column definitions reused across list commands
_COL_NAME = {"header": "Name", "style": "cyan", "no_wrap": True, "_key": "name"}
_COL_NOTES = {"header": "Notes", "style": "yellow", "max_width": 40, "_key": "notes"}
_COL_URL = {"header": "GitHub URL", "style": "blue", "_key": "source_code_url"}
_COL_LICENSE = {"header": "License", "style": "white", "_key": "license"}
_COL_BASE_ART = {"header": "base_artifact_id", "style": "green", "no_wrap": True, "_key": "base_artifact_id"}
_COL_DATA_ART = {"header": "data_artifact_id", "style": "green", "no_wrap": True, "_key": "data_artifact_id"}
_COL_ENV_ASSIGNEES = {"header": "Env Assignees", "style": "magenta", "no_wrap": True, "_key": "env_assignees"}
_COL_ENV_REVIEW_ASSIGNEES = {"header": "Reviewers", "style": "magenta", "no_wrap": True, "_key": "env_review_assignees"}
_COL_DATA_ASSIGNEES = {"header": "Data Assignees", "style": "magenta", "no_wrap": True, "_key": "data_assignees"}
_COL_DATA_REVIEW_ASSIGNEES = {
    "header": "Reviewers",
    "style": "magenta",
    "no_wrap": True,
    "_key": "data_review_assignees",
}


@list_app.command(name="not-started")
def list_not_started():
    """List not_started docker_app simulators."""
    _list_by_status("not_started", "Not Started", [_COL_NAME, _COL_URL, _COL_LICENSE, _COL_NOTES], docker_app_only=True)


@list_app.command(name="env-wip")
def list_env_wip():
    """List simulators with env in progress."""
    _list_by_status(
        "env_in_progress",
        "Env In Progress",
        [_COL_NAME, _COL_ENV_ASSIGNEES, _COL_BASE_ART, _COL_NOTES],
        sort_by="env_assignees",
    )


@list_app.command(name="env")
def list_env():
    """List simulators pending env review."""
    _list_by_status(
        "env_review_requested", "Pending Env Review", [_COL_NAME, _COL_ENV_REVIEW_ASSIGNEES, _COL_BASE_ART, _COL_NOTES]
    )


@list_app.command(name="env-ready")
def list_env_ready():
    """List simulators with env approved (ready for data)."""
    _list_by_status("env_approved", "Env Approved", [_COL_NAME, _COL_ENV_ASSIGNEES, _COL_BASE_ART, _COL_NOTES])


@list_app.command(name="data-wip")
def list_data_wip():
    """List simulators with data in progress."""
    _list_by_status("data_in_progress", "Data In Progress", [_COL_NAME, _COL_DATA_ASSIGNEES, _COL_BASE_ART, _COL_NOTES])


@list_app.command(name="data")
def list_data():
    """List simulators pending data review."""
    _list_by_status(
        "data_review_requested",
        "Pending Data Review",
        [_COL_NAME, _COL_DATA_REVIEW_ASSIGNEES, _COL_DATA_ART, _COL_NOTES],
    )


# =============================================================================
# WORLD LAUNCH HELPERS
# =============================================================================


def _find_templates_dir() -> Path:
    """Find the templates directory (repo root ``templates/`` — not shipped in wheel).

    Templates are Plato-internal infra bundles pushed to Chronos via
    ``plato pm experiment ... push``. They're intentionally excluded from the
    published SDK so external installs don't carry them.
    """
    # plato/cli/pm.py -> plato/cli/ -> plato/ -> <repo root>/ -> templates/
    repo_root = Path(__file__).resolve().parent.parent.parent
    return repo_root / "templates"


def _load_template(name: str) -> dict:
    """Load a JSON launch template by name."""
    templates_dir = _find_templates_dir()
    template_path = templates_dir / name
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")
    with open(template_path) as f:
        return json.load(f)


# Maps (pipeline, mode) → experiment name in Chronos
_EXPERIMENT_NAMES: dict[tuple[str, str], str] = {
    ("env", "base"): "env-create-launch",
    ("env", "fix"): "env-fix-launch",
    ("data", "base"): "datagen-launch",
    ("data", "unified"): "datagen-unified-launch",
    ("check", "base"): "sim-checker-launch",
    ("blank", "base"): "simcreator-blank-launch",
    # AgentSession experiments — drop the legacy ``-launch`` suffix; these
    # are long-lived session configs, not one-shot launch templates.
    ("agent", "data-load"): "agent-data-load",
}


def _render_step_instructions(world_config: dict, **substitutions: str) -> None:
    """Replace ``{key}`` placeholders in each step's instruction in place.

    Templates live in structured_execution_world and use ``{sim_name}``,
    ``{github_url}``, ``{feedback}``, ``{artifact_id}``, ``{data_artifact_section}``,
    etc. We render them here at launch time so the world receives plain strings — no
    runtime substitution engine required. Unknown placeholders are left intact; if
    a step's instruction doesn't reference a substitution, that's fine (only
    env-fix's ``fix`` step uses ``{data_artifact_section}``, for example).
    """
    for step in world_config.get("steps", []):
        instr = step.get("instruction", "")
        for key, value in substitutions.items():
            instr = instr.replace(f"{{{key}}}", str(value))
        step["instruction"] = instr


def _render_step_verify(world_config: dict, **substitutions: str) -> None:
    """Replace ``{key}`` placeholders in every step's verify shell commands.

    Extract-screenshots bakes API credentials and the Plato base URL into the
    upload verify shell, so we render those the same way we render instructions.
    """
    for step in world_config.get("steps", []):
        verify = step.get("verify")
        if not isinstance(verify, list):
            continue
        rendered: list[str] = []
        for cmd in verify:
            if not isinstance(cmd, str):
                rendered.append(cmd)
                continue
            for key, value in substitutions.items():
                cmd = cmd.replace(f"{{{key}}}", str(value))
            rendered.append(cmd)
        step["verify"] = rendered


def _fetch_experiment_config(pipeline: str, mode: str, api_key: str) -> tuple[dict, str]:
    """Fetch latest experiment config from Chronos by name. Raises if not found.

    Returns (config_json, version_public_id) so callers can attach sessions back.
    """
    name = _EXPERIMENT_NAMES.get((pipeline, mode))
    if name is None:
        raise ValueError(f"Unknown experiment: {pipeline}/{mode}")
    with httpx.Client(timeout=10.0) as client:
        resp = client.get(
            f"{CHRONOS_URL}/api/experiments/files",
            headers={"X-API-Key": api_key},
        )
        if resp.status_code != 200:
            raise Exception(f"Failed to fetch experiments: HTTP {resp.status_code}: {resp.text}")
        files = resp.json().get("files", [])
        match = next((f for f in files if f["name"] == name), None)
        if not match:
            raise Exception(
                f"Experiment '{name}' not found in Chronos. Run: plato pm experiment {pipeline} {mode} push"
            )
        latest = match.get("latest_version") or {}
        config = latest.get("config_json")
        if config is None:
            raise Exception(f"Experiment '{name}' has no config_json in latest version")
        version_public_id = latest.get("public_id", "")
        if not version_public_id:
            console.print(f"[yellow]⚠️  Experiment '{name}' version has no public_id — session won't be linked[/yellow]")
        return config, version_public_id


def _get_last_chronos_session(tags: list[str], api_key: str) -> dict | None:
    """Get the most recent Chronos session matching all given tags. Returns session dict or None."""
    try:
        with httpx.Client(timeout=15.0) as client:
            resp = client.get(
                f"{CHRONOS_URL}/api/sessions",
                params=[("tag", t) for t in tags] + [("limit", "1")],  # pyright: ignore[reportArgumentType]
                headers={"X-API-Key": api_key},
            )
            if resp.status_code != 200:
                return None
            sessions = resp.json().get("sessions", [])
            return sessions[0] if sessions else None
    except Exception:
        return None


def _launch_on_chronos(launch_config: dict, api_key: str) -> str:
    """POST launch config to Chronos, return session_id."""
    with httpx.Client(timeout=60.0) as client:
        resp = client.post(
            f"{CHRONOS_URL}/api/jobs/launch",
            content=json.dumps(launch_config).encode("utf-8"),
            headers={"X-API-Key": api_key, "Content-Type": "application/json"},
        )
        if resp.status_code != 200:
            raise Exception(f"Chronos launch failed: HTTP {resp.status_code}: {resp.text}")
        return resp.json()["session_id"]


def _attach_session_to_experiment(version_public_id: str, session_id: str, api_key: str) -> None:
    """Attach a launched session to its experiment version. Warns on failure."""
    if not version_public_id:
        return
    try:
        with httpx.Client(base_url=CHRONOS_URL, timeout=httpx.Timeout(3.0, connect=2.0)) as client:
            from plato.chronos.api.experiments import attach_session_to_experiment_version

            attach_session_to_experiment_version.sync(
                client=client,
                public_id=version_public_id,
                session_public_id=session_id,
                x_api_key=api_key,
            )
    except Exception as e:
        console.print(f"[yellow]⚠️  Failed to link session {session_id} to experiment: {e}[/yellow]")


async def _launch_env_world(
    action: str,
    simulator_name: str,
    artifact_id: str,
    feedback: str,
    api_key: str,
    current_config: dict,
    action_inputs: dict | None = None,
) -> str | None:
    """Launch a structured world (fresh, resume, or fix) after env reject. Returns session_id or None.

    action_inputs: Pre-collected inputs from the caller.
        For fresh: {"github_url": "..."}.
        For resume: {"resume_from": "..."}.
        For fix: {"resume_from": "..."}.
    """
    datagen_api_key = DEFAULT_DATAGEN_API_KEY
    inputs = action_inputs or {}

    try:
        if action == "fresh":
            github_url = inputs.get("github_url", "")
            if not github_url:
                console.print("[yellow]No GitHub URL provided, skipping launch.[/yellow]")
                return None

            template, version_id = _fetch_experiment_config("env", "base", api_key)
            config = template["world"]["config"]
            config["sim_name"] = simulator_name
            config["github_url"] = github_url
            _render_step_instructions(
                config,
                sim_name=simulator_name,
                github_url=github_url,
                workspace="/workspace",
            )
            _render_step_verify(config, sim_name=simulator_name, github_url=github_url)
            cred_key, cred_val = _get_claude_credentials()
            config["plato_api_key"] = datagen_api_key
            _set_claude_credentials(config, cred_key, cred_val)
            config["agent"]["config"]["plato_api_key"] = datagen_api_key
            _set_claude_credentials(config["agent"]["config"], cred_key, cred_val)
            template["tags"].append(simulator_name)

        elif action == "resume":
            resume_from = inputs.get("resume_from", "")

            template, version_id = _fetch_experiment_config("env", "base", api_key)
            config = template["world"]["config"]
            config["sim_name"] = simulator_name
            github_url = current_config.get("source_code_url", "")
            config["github_url"] = github_url
            _render_step_instructions(
                config,
                sim_name=simulator_name,
                github_url=github_url,
                workspace="/workspace",
            )
            _render_step_verify(config, sim_name=simulator_name, github_url=github_url)
            cred_key, cred_val = _get_claude_credentials()
            config["plato_api_key"] = datagen_api_key
            _set_claude_credentials(config, cred_key, cred_val)
            config["agent"]["config"]["plato_api_key"] = datagen_api_key
            _set_claude_credentials(config["agent"]["config"], cred_key, cred_val)
            config["state"]["resume_from"] = resume_from
            template["tags"].append(simulator_name)
            template["tags"].append("resume")

        elif action == "fix":
            base_artifact_id = current_config.get("base_artifact_id")
            if not base_artifact_id:
                console.print("[red]Simulator has no base_artifact_id. Cannot launch fix.[/red]")
                return None
            data_artifact_id = current_config.get("data_artifact_id") or ""

            resume_from = inputs.get("resume_from", "")

            template, version_id = _fetch_experiment_config("env", "fix", api_key)
            config = template["world"]["config"]
            config["sim_name"] = simulator_name
            _render_step_instructions(
                config,
                sim_name=simulator_name,
                feedback=feedback,
                artifact_id=base_artifact_id,
                data_artifact_section=_render_data_artifact_section(data_artifact_id),
                workspace="/workspace",
            )
            cred_key, cred_val = _get_claude_credentials()
            config["plato_api_key"] = datagen_api_key
            _set_claude_credentials(config, cred_key, cred_val)
            config["agent"]["config"]["plato_api_key"] = datagen_api_key
            _set_claude_credentials(config["agent"]["config"], cred_key, cred_val)
            config["state"]["resume_from"] = resume_from
            template["tags"].append(simulator_name)

        else:
            console.print(f"[red]Unknown action: {action}[/red]")
            return None

        console.print("[cyan]Launching world on Chronos...[/cyan]")
        session_id = _launch_on_chronos(template, api_key)
        _attach_session_to_experiment(version_id, session_id, api_key)
        return session_id

    except Exception as e:
        console.print(f"[red]❌ World launch failed: {e}[/red]")
        return None


def _compute_reject_walk(current_status: str, target: str) -> list[str] | None:
    """Compute the DATA_REVIEWER-allowed status walk from current_status to target.

    Mirrors DATA_REVIEWER_TRANSITIONS in plato/services/app/src/app/api/v1/simulator_routes.py.
    Returns the list of intermediate + final statuses (empty = already there), or None
    if there's no valid walk from the given starting state.
    """
    # DATA_REVIEWER allowed transitions:
    #   data_review_requested ↔ data_in_progress
    #   data_review_requested ↔ ready
    #   data_in_progress → env_approved → env_review_requested → env_in_progress
    to_data_in_progress: dict[str, list[str]] = {
        "data_in_progress": [],
        "data_review_requested": ["data_in_progress"],
        "ready": ["data_review_requested", "data_in_progress"],
    }
    env_suffix = ["env_approved", "env_review_requested", "env_in_progress"]

    if target == "data_in_progress":
        return to_data_in_progress.get(current_status)

    if target == "env_in_progress":
        # Starting states on the env side (if user is re-running after partial walk)
        mid_env = {
            "env_in_progress": [],
            "env_review_requested": ["env_in_progress"],
            "env_approved": ["env_review_requested", "env_in_progress"],
        }
        if current_status in mid_env:
            return mid_env[current_status]
        prefix = to_data_in_progress.get(current_status)
        if prefix is None:
            return None
        return prefix + env_suffix

    return None


async def _submit_reject_no_browser(
    simulator_name: str,
    artifact_id_arg: str | None,
    message: str,
    api_key: str,
) -> None:
    """Submit a reject review from a CLI message without opening the browser.

    Mirrors the data-review extension's reject flow: prompts for level (data vs env)
    and per-level sub-action, walks status back, posts reviews, updates assignees, and
    optionally launches a datagen/env world.
    """
    base_url = _get_base_url()

    async with httpx.AsyncClient(base_url=base_url, timeout=60.0) as client:
        sim = await get_simulator_by_name.asyncio(
            client=client,
            name=simulator_name,
            x_api_key=api_key,
        )
        simulator_id = sim.id
        current_config = sim_config_dict(sim.config)
        current_status = current_config.get("status", "not_started")

        artifact_id = artifact_id_arg or current_config.get("data_artifact_id")
        if not artifact_id:
            console.print("[red]❌ No artifact ID available.[/red]")
            console.print(
                "[yellow]Specify artifact with: plato pm reject <sim> --artifact <uuid> -m ... "
                "(or <sim>:<uuid>)[/yellow]"
            )
            raise typer.Exit(1)

        console.print(f"[cyan]Artifact:[/cyan] {artifact_id}")
        console.print(f"[cyan]Current status:[/cyan] {current_status}")
        console.print(f"[cyan]Review message:[/cyan] {message}")

        console.print("\n[bold]Reject level:[/bold]")
        console.print("  1. data (bounce back to datagen)")
        console.print("  2. env  (bounce all the way back to env)")
        level_choice = typer.prompt("Choice [1/2]", default="1").strip()
        if level_choice not in ("1", "2"):
            console.print("[red]❌ Invalid choice.[/red]")
            raise typer.Exit(1)

        if level_choice == "1":
            await _handle_data_level_reject(
                client=client,
                simulator_id=simulator_id,
                simulator_name=simulator_name,
                artifact_id=artifact_id,
                message=message,
                current_status=current_status,
                current_config=current_config,
                api_key=api_key,
            )
        else:
            await _handle_env_level_reject(
                client=client,
                simulator_id=simulator_id,
                simulator_name=simulator_name,
                artifact_id=artifact_id,
                message=message,
                current_status=current_status,
                current_config=current_config,
                api_key=api_key,
            )


async def _handle_data_level_reject(
    client: httpx.AsyncClient,
    simulator_id: int,
    simulator_name: str,
    artifact_id: str,
    message: str,
    current_status: str,
    current_config: dict,
    api_key: str,
) -> None:
    """Data-level reject: status → data_in_progress, post data review, optional datagen."""
    walk = _compute_reject_walk(current_status, "data_in_progress")
    if walk is None:
        console.print(f"[red]❌ Cannot walk from status '{current_status}' to data_in_progress as DATA_REVIEWER.[/red]")
        console.print("[yellow]Use plato pm set-status if you need to force-set the status.[/yellow]")
        raise typer.Exit(1)

    console.print("\n[bold]Launch datagen?[/bold]")
    console.print("  1. none")
    console.print("  2. fresh (new datagen run)")
    console.print("  3. resume (rerun with review feedback)")
    datagen_choice = typer.prompt("Choice [1/2/3]", default="1").strip()
    if datagen_choice not in ("1", "2", "3"):
        console.print(f"[red]❌ Invalid choice '{datagen_choice}'. Expected 1, 2, or 3.[/red]")
        raise typer.Exit(1)

    datagen_action = None
    if datagen_choice in ("2", "3"):
        datagen_action = "fresh" if datagen_choice == "2" else "resume"

    status_walk_str = " → ".join([current_status] + walk) if walk else f"{current_status} (no change)"
    console.print("\n[bold]Review summary:[/bold]")
    console.print("  Level:   data")
    console.print("  Outcome: reject")
    console.print(f"  Comment: {message}")
    console.print(f"  Status:  {status_walk_str}")
    if datagen_action:
        console.print(f"  Datagen: {datagen_action}")

    if not typer.confirm("Submit?", default=True):
        console.print("[yellow]Cancelled — nothing submitted.[/yellow]")
        return

    for target_status in walk:
        await update_simulator_status.asyncio(
            client=client,
            simulator_id=simulator_id,
            body=UpdateStatusRequest(status=Status(target_status)),
            x_api_key=api_key,
        )
    await add_simulator_review.asyncio(
        client=client,
        simulator_id=simulator_id,
        body=AddReviewRequest(
            review_type=ReviewType.data,
            outcome=Outcome.reject,
            artifact_id=artifact_id,
            sim_comments=[SimReviewComment(comment=message)],
        ),
        x_api_key=api_key,
    )

    existing_data_assignees = current_config.get("data_assignees") or []
    existing_data_review_assignees = current_config.get("data_review_assignees") or []
    updates: dict = {}
    if not existing_data_assignees:
        updates["data_assignees"] = DEFAULT_DATA_ASSIGNEES
    if not existing_data_review_assignees:
        updates["data_review_assignees"] = DEFAULT_DATA_REVIEW_ASSIGNEES
    if updates:
        await update_simulator.asyncio(
            client=client,
            simulator_id=simulator_id,
            body=AppApiV1SimulatorRoutesUpdateSimulatorRequest(**updates),
            x_api_key=api_key,
        )

    console.print("\n[green]✅ Review submitted: reject (data level)[/green]")
    console.print(f"[cyan]Status:[/cyan] {status_walk_str}")

    if datagen_action:
        launched_session = await _launch_datagen_world(
            simulator_name=simulator_name,
            artifact_id=artifact_id,
            api_key=api_key,
            review_comments=[message] if datagen_action == "resume" else None,
        )
        if launched_session:
            console.print(f"[green]✅ Datagen launched: {launched_session}[/green]")
            console.print(f"[cyan]View:[/cyan] https://chronos.plato.so/sessions/{launched_session}")


async def _handle_env_level_reject(
    client: httpx.AsyncClient,
    simulator_id: int,
    simulator_name: str,
    artifact_id: str,
    message: str,
    current_status: str,
    current_config: dict,
    api_key: str,
) -> None:
    """Env-level reject: walk status back to env_in_progress, post data+env reviews, optional env world."""
    walk = _compute_reject_walk(current_status, "env_in_progress")
    if walk is None:
        console.print(f"[red]❌ Cannot walk from status '{current_status}' to env_in_progress as DATA_REVIEWER.[/red]")
        console.print("[yellow]Use plato pm set-status if you need to force-set the status.[/yellow]")
        raise typer.Exit(1)

    github_url_from_config = current_config.get("source_code_url", "")
    existing_env_assignees = current_config.get("env_assignees") or []

    console.print("\n[bold]Launch a world?[/bold]")
    console.print("  1. none")
    if github_url_from_config:
        console.print(f"  2. fresh (create from scratch — {github_url_from_config})")
    else:
        console.print("  2. fresh (create from scratch — no GitHub URL in config)")
    console.print("  3. resume (continue create pipeline from last session)")
    console.print(f"  4. fix (fix pipeline — data artifact {artifact_id[:8]}... + message as feedback)")
    action_choice = typer.prompt("Choice [1/2/3/4]", default="1").strip()
    if action_choice not in ("1", "2", "3", "4"):
        console.print(f"[red]❌ Invalid choice '{action_choice}'. Expected 1, 2, 3, or 4.[/red]")
        raise typer.Exit(1)

    env_action: str | None = None
    env_action_inputs: dict = {}
    clear_assignees = False

    if action_choice == "2":
        env_action = "fresh"
        github_url = typer.prompt("GitHub URL", default=github_url_from_config).strip()
        if github_url:
            env_action_inputs["github_url"] = github_url
        else:
            console.print("[yellow]No GitHub URL provided, skipping launch.[/yellow]")
            env_action = None
    elif action_choice == "3":
        env_action = "resume"
        last_session = _get_last_chronos_session(tags=["simcreator", simulator_name], api_key=api_key)
        default_resume = ""
        if last_session:
            sid = last_session["public_id"]
            status = last_session.get("status", "?")
            created = last_session.get("created_at", "")[:16].replace("T", " ")
            console.print(f"[cyan]Last simcreator session:[/cyan] {sid} ({status}, {created})")
            default_resume = sid
        resume_from = typer.prompt("Resume session (enter for above, 'none' for fresh)", default=default_resume).strip()
        if resume_from.lower() == "none":
            resume_from = ""
        env_action_inputs["resume_from"] = resume_from
    elif action_choice == "4":
        env_action = "fix"

    # On "none", auto-clear env assignees (nobody's been asked to do anything,
    # so leave the env pool empty for re-triage). Other actions keep them.
    if action_choice == "1" and existing_env_assignees:
        console.print(f"[cyan]Current env assignees:[/cyan] {existing_env_assignees} — will be cleared")
        clear_assignees = True

    status_walk_str = " → ".join([current_status] + walk) if walk else f"{current_status} (no change)"
    console.print("\n[bold]Review summary:[/bold]")
    console.print("  Level:   env")
    console.print("  Outcome: reject")
    console.print(f"  Comment: {message}")
    console.print(f"  Status walk: {status_walk_str}")
    if env_action:
        action_desc = env_action
        if env_action == "fresh":
            action_desc += f" ({env_action_inputs.get('github_url', '')})"
        elif env_action == "resume":
            rs = env_action_inputs.get("resume_from", "")
            action_desc += f" ({rs[:12]}...)" if rs else " (fresh state)"
        console.print(f"  World:   {action_desc}")
        console.print(f"  Env assignees: → {DEFAULT_DATA_ASSIGNEES}")
    elif clear_assignees:
        console.print("  Clear env assignees: yes")

    if not typer.confirm("Submit?", default=True):
        console.print("[yellow]Cancelled — nothing submitted.[/yellow]")
        return

    # Walk status back using the DATA_REVIEWER-allowed path computed above
    for target_status in walk:
        await update_simulator_status.asyncio(
            client=client,
            simulator_id=simulator_id,
            body=UpdateStatusRequest(status=Status(target_status)),
            x_api_key=api_key,
        )

    await add_simulator_review.asyncio(
        client=client,
        simulator_id=simulator_id,
        body=AddReviewRequest(
            review_type=ReviewType.data,
            outcome=Outcome.reject,
            artifact_id=artifact_id,
            sim_comments=[SimReviewComment(comment=message)],
        ),
        x_api_key=api_key,
    )
    await add_simulator_review.asyncio(
        client=client,
        simulator_id=simulator_id,
        body=AddReviewRequest(
            review_type=ReviewType.env,
            outcome=Outcome.reject,
            artifact_id=artifact_id,
            sim_comments=[SimReviewComment(comment=message)],
        ),
        x_api_key=api_key,
    )

    if env_action:
        try:
            await update_simulator.asyncio(
                client=client,
                simulator_id=simulator_id,
                body=AppApiV1SimulatorRoutesUpdateSimulatorRequest(
                    env_assignees=DEFAULT_DATA_ASSIGNEES,
                ),
                x_api_key=api_key,
            )
            console.print(f"[green]✅ Set env_assignees → {DEFAULT_DATA_ASSIGNEES}[/green]")
        except Exception as e:
            console.print(f"[yellow]⚠️  Could not set env assignees: {e}[/yellow]")
    elif clear_assignees:
        try:
            await update_simulator.asyncio(
                client=client,
                simulator_id=simulator_id,
                body=AppApiV1SimulatorRoutesUpdateSimulatorRequest(
                    env_assignees=[],
                ),
                x_api_key=api_key,
            )
            console.print("[green]✅ Cleared env assignees[/green]")
        except Exception as e:
            console.print(f"[yellow]⚠️  Could not clear assignees: {e}[/yellow]")

    console.print("\n[green]✅ Reviews submitted: reject (data + env)[/green]")
    console.print(f"[cyan]Status:[/cyan] {status_walk_str}")

    if env_action:
        # env-fix uses the sim's actual base_artifact_id as the artifact to
        # fix-and-snapshot, with the data artifact (the one the reviewer was
        # looking at, also the sim's current data_artifact_id) made available
        # to the agent as a read-only reference. This matches the policy:
        # output is always the base artifact, with cleared data and any fixes
        # baked in; the data artifact is for diagnosing data-shaped symptoms
        # only. _launch_env_world reads both fields from current_config — no
        # override needed.
        launched_session = await _launch_env_world(
            action=env_action,
            simulator_name=simulator_name,
            artifact_id=artifact_id,
            feedback=message,
            api_key=api_key,
            current_config=current_config,
            action_inputs=env_action_inputs,
        )
        if launched_session:
            console.print(f"[green]✅ World launched: {launched_session}[/green]")
            console.print(f"[cyan]View:[/cyan] https://chronos.plato.so/sessions/{launched_session}")


async def _launch_datagen_world(
    simulator_name: str,
    artifact_id: str,
    api_key: str,
    review_comments: list[str] | None = None,
) -> str | None:
    """Launch an interactive datagen world. Returns session_id or None."""
    datagen_api_key = DEFAULT_DATAGEN_API_KEY

    if not DEFAULT_ANCHOR_KEY:
        console.print(
            "[yellow]⚠️  ANCHOR_API_KEY is not set. The datagen session will fail to launch a browser.[/yellow]"
        )
        console.print("[yellow]   Set it with: export ANCHOR_API_KEY=<your-key>[/yellow]")
        if not typer.confirm("Continue anyway?", default=False):
            return None

    try:
        template, version_id = _fetch_experiment_config("data", "base", api_key)

        # Fetch DB configs for MCP setup
        with httpx.Client(timeout=30.0) as client:
            resp = client.get(
                f"{_get_base_url()}/api/v1/simulator/{artifact_id}/db_config",
                headers={"X-API-Key": api_key},
            )
            db_configs = resp.json() if resp.status_code == 200 else []
            if not isinstance(db_configs, list):
                db_configs = [db_configs]

        # Build MCPs — each instance has an explicit `name` (unique per env).
        mcps = []
        db_names = _build_unique_db_mcp_names(db_configs)
        for db_name, db in zip(db_names, db_configs):
            mcps.append(
                {
                    "type": "db",
                    "name": db_name,
                    "db_type": db.get("db_type"),
                    "db_port": db.get("db_port"),
                    "db_user": db.get("db_user"),
                    "db_password": db.get("db_password"),
                    "db_database": db.get("db_database"),
                    "db_schema": db.get("db_schema"),
                    "service": simulator_name,
                }
            )
        mcps.append({"type": "vm", "name": "vm"})
        mcps.append({"type": "browser", "name": "browser"})
        mcps.append(
            {
                "type": "functions",
                "name": "functions",
                "session_id": f"run-{simulator_name}",
                "service": simulator_name,
            }
        )

        config = template["world"]["config"]
        cred_key, cred_val = _get_claude_credentials()
        _set_claude_credentials(config, cred_key, cred_val)
        # Also set credentials on agent.config (used by claude-code agent)
        agent_config = config.get("agent", {}).get("config")
        if agent_config is not None:
            _set_claude_credentials(agent_config, cred_key, cred_val)
        config["plato_api_key"] = datagen_api_key
        config["anchor_api_key"] = DEFAULT_ANCHOR_KEY
        config["browserbase_api_key"] = DEFAULT_BROWSERBASE_KEY
        config["envs"] = [
            {
                "env": {"artifact_id": artifact_id, "alias": simulator_name},
                "mcps": mcps,
                "default": True,
            }
        ]
        config["sim_name"] = simulator_name

        # Template ships with [generate, audit_and_fill]. Reject other shapes
        # so a template change doesn't silently drop steps.
        template_steps = config.get("steps") or []
        step_names = [s.get("name") if isinstance(s, dict) else None for s in template_steps]
        if step_names != ["generate", "audit_and_fill"]:
            raise ValueError(f"datagen template must be [generate, audit_and_fill], got {step_names}")
        if review_comments is not None:
            template_steps[0]["instruction"] = _build_datagen_review_prompt(
                simulator_name, review_comments, template_steps[0]["instruction"]
            )
        _render_step_instructions(config, sim_name=simulator_name, workspace="/workspace")

        template["tags"].append(simulator_name)
        if review_comments is not None:
            template["tags"].append("resume")

        console.print("[cyan]Launching datagen world on Chronos...[/cyan]")
        session_id = _launch_on_chronos(template, api_key)
        _attach_session_to_experiment(version_id, session_id, api_key)
        return session_id

    except Exception as e:
        console.print(f"[red]❌ Datagen launch failed: {e}[/red]")
        return None


async def _launch_datagen_unified_world(
    sims: list[dict],
    api_key: str,
) -> str | None:
    """Launch a unified datagen session covering multiple sims in one session.

    Each sim becomes its own env with its full MCP set (db, vm, browser,
    functions). Tool names are env-prefixed (e.g. ``<alias>_db_select_context``)
    by structured-execution's runtime, and the world writes per-env state.json
    files so the final cross_verify step can snapshot each env independently.

    ``sims`` is a list of ``{name, artifact_id}`` dicts.
    """
    datagen_api_key = DEFAULT_DATAGEN_API_KEY

    if not DEFAULT_ANCHOR_KEY:
        console.print("[yellow]⚠️  ANCHOR_API_KEY is not set. Datagen browsers will fail to launch.[/yellow]")
        console.print("[yellow]   Set it with: export ANCHOR_API_KEY=<your-key>[/yellow]")
        if not typer.confirm("Continue anyway?", default=False):
            return None

    try:
        template, version_id = _fetch_experiment_config("data", "unified", api_key)

        envs: list[dict] = []
        base_url = _get_base_url()
        with httpx.Client(timeout=30.0) as client:
            for idx, sim in enumerate(sims):
                sim_name = sim["name"]
                artifact_id = sim["artifact_id"]

                resp = client.get(
                    f"{base_url}/api/v1/simulator/{artifact_id}/db_config",
                    headers={"X-API-Key": api_key},
                )
                db_configs = resp.json() if resp.status_code == 200 else []
                if not isinstance(db_configs, list):
                    db_configs = [db_configs]

                mcps: list[dict] = []
                db_names = _build_unique_db_mcp_names(db_configs)
                for db_name, db in zip(db_names, db_configs):
                    mcps.append(
                        {
                            "type": "db",
                            "name": db_name,
                            "db_type": db.get("db_type"),
                            "db_port": db.get("db_port"),
                            "db_user": db.get("db_user"),
                            "db_password": db.get("db_password"),
                            "db_database": db.get("db_database"),
                            "db_schema": db.get("db_schema"),
                            "service": sim_name,
                        }
                    )
                mcps.append({"type": "vm", "name": "vm"})
                mcps.append({"type": "browser", "name": "browser"})
                mcps.append(
                    {
                        "type": "functions",
                        "name": "functions",
                        "session_id": f"run-{sim_name}",
                        "service": sim_name,
                    }
                )

                envs.append(
                    {
                        "env": {"artifact_id": artifact_id, "alias": sim_name},
                        "mcps": mcps,
                        "default": idx == 0,
                    }
                )

        config = template["world"]["config"]
        cred_key, cred_val = _get_claude_credentials()
        _set_claude_credentials(config, cred_key, cred_val)
        agent_config = config.get("agent", {}).get("config")
        if agent_config is not None:
            _set_claude_credentials(agent_config, cred_key, cred_val)
        config["plato_api_key"] = datagen_api_key
        config["anchor_api_key"] = DEFAULT_ANCHOR_KEY
        config["browserbase_api_key"] = DEFAULT_BROWSERBASE_KEY
        config["envs"] = envs
        config["sim_names"] = [s["name"] for s in sims]
        # Fallback simulator_name in per-env state.json when env.simulator is None
        # (artifact-restored envs). The world picks the env's own alias when available,
        # but config.sim_name is the last-resort fallback; keep it non-empty.
        config["sim_name"] = sims[0]["name"]

        _render_step_instructions(config, workspace="/workspace")

        for sim in sims:
            template["tags"].append(sim["name"])

        console.print(f"[cyan]Launching unified datagen world on Chronos ({len(sims)} sims)...[/cyan]")
        session_id = _launch_on_chronos(template, api_key)
        _attach_session_to_experiment(version_id, session_id, api_key)
        return session_id

    except Exception as e:
        console.print(f"[red]❌ Unified datagen launch failed: {e}[/red]")
        return None


async def _launch_sim_checker_world(
    simulator_name: str,
    artifact_id: str,
    api_key: str,
) -> str | None:
    """Launch a structured-execution sim-checker session. Returns session_id or None.

    Runs the sim-checker-launch template against a single artifact: walks the app,
    performs mutations, queries audit state, and writes the verdict to the Chronos
    session result via the set_session_output builtin verifier.
    """
    datagen_api_key = DEFAULT_DATAGEN_API_KEY

    if not DEFAULT_ANCHOR_KEY:
        console.print(
            "[yellow]⚠️  ANCHOR_API_KEY is not set. The sim-checker session will fail to launch a browser.[/yellow]"
        )
        console.print("[yellow]   Set it with: export ANCHOR_API_KEY=<your-key>[/yellow]")
        if not typer.confirm("Continue anyway?", default=False):
            return None

    try:
        template, version_id = _fetch_experiment_config("check", "base", api_key)

        # Fetch DB configs for MCP setup (same pattern as datagen).
        with httpx.Client(timeout=30.0) as client:
            resp = client.get(
                f"{_get_base_url()}/api/v1/simulator/{artifact_id}/db_config",
                headers={"X-API-Key": api_key},
            )
            db_configs = resp.json() if resp.status_code == 200 else []
            if not isinstance(db_configs, list):
                db_configs = [db_configs]

        mcps: list[dict] = []
        db_names = _build_unique_db_mcp_names(db_configs)
        for db_name, db in zip(db_names, db_configs):
            mcps.append(
                {
                    "type": "db",
                    "name": db_name,
                    "db_type": db.get("db_type"),
                    "db_port": db.get("db_port"),
                    "db_user": db.get("db_user"),
                    "db_password": db.get("db_password"),
                    "db_database": db.get("db_database"),
                    "db_schema": db.get("db_schema"),
                    "service": simulator_name,
                }
            )
        mcps.append({"type": "vm", "name": "vm"})
        mcps.append({"type": "browser", "name": "browser", "backend": "browserbase"})

        config = template["world"]["config"]
        cred_key, cred_val = _get_claude_credentials()
        _set_claude_credentials(config, cred_key, cred_val)
        agent_config = config.get("agent", {}).get("config")
        if agent_config is not None:
            _set_claude_credentials(agent_config, cred_key, cred_val)
        config["plato_api_key"] = datagen_api_key
        config["anchor_api_key"] = DEFAULT_ANCHOR_KEY
        config["browserbase_api_key"] = DEFAULT_BROWSERBASE_KEY
        config["envs"] = [
            {
                "env": {"artifact_id": artifact_id, "alias": simulator_name},
                "mcps": mcps,
                "default": True,
            }
        ]
        config["sim_name"] = simulator_name
        config["artifact_id"] = artifact_id

        _render_step_instructions(
            config,
            sim_name=simulator_name,
            artifact_id=artifact_id,
            mutation_threshold=str(config.get("mutation_threshold", 40)),
        )

        template["tags"].append(simulator_name)

        console.print("[cyan]Launching sim-checker world on Chronos...[/cyan]")
        session_id = _launch_on_chronos(template, api_key)
        _attach_session_to_experiment(version_id, session_id, api_key)
        return session_id

    except Exception as e:
        console.print(f"[red]❌ Sim-checker launch failed: {e}[/red]")
        return None


# Supported MCP types for local-template launches.
_SUPPORTED_TEMPLATE_MCPS: frozenset[str] = frozenset({"browser", "vm", "db", "functions"})


async def _build_mcps_for_sim(
    mcps_required: list[str],
    simulator_name: str,
    artifact_id: str,
    api_key: str,
) -> list[dict]:
    """Materialize the MCP list for one attached env from ``mcps_required``.

    ``browser`` and ``vm`` are static. ``db`` fetches the sim's db_config from
    the Plato API and may expand to multiple entries (multi-DB sims).
    ``functions`` is stamped with a per-sim session_id.
    """
    unknown = [m for m in mcps_required if m not in _SUPPORTED_TEMPLATE_MCPS]
    if unknown:
        raise ValueError(f"Unsupported MCPs in mcps_required: {unknown}. Supported: {sorted(_SUPPORTED_TEMPLATE_MCPS)}")

    mcps: list[dict] = []
    base_url = _get_base_url()

    browser_backend = "browserbase" if DEFAULT_BROWSERBASE_KEY else "anchor"
    for mcp_type in mcps_required:
        if mcp_type == "browser":
            mcps.append({"type": "browser", "name": "browser", "backend": browser_backend})
        elif mcp_type == "vm":
            mcps.append({"type": "vm", "name": "vm"})
        elif mcp_type == "db":
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.get(
                    f"{base_url}/api/v1/simulator/{artifact_id}/db_config",
                    headers={"X-API-Key": api_key},
                )
            db_configs = resp.json() if resp.status_code == 200 else []
            if not isinstance(db_configs, list):
                db_configs = [db_configs]
            db_names = _build_unique_db_mcp_names(db_configs)
            for db_name, db in zip(db_names, db_configs):
                mcps.append(
                    {
                        "type": "db",
                        "name": db_name,
                        "db_type": db.get("db_type"),
                        "db_port": db.get("db_port"),
                        "db_user": db.get("db_user"),
                        "db_password": db.get("db_password"),
                        "db_database": db.get("db_database"),
                        "db_schema": db.get("db_schema"),
                        "service": simulator_name,
                    }
                )
        elif mcp_type == "functions":
            mcps.append(
                {
                    "type": "functions",
                    "name": "functions",
                    "session_id": f"run-{simulator_name}",
                    "service": simulator_name,
                }
            )

    return mcps


async def _launch_from_template_world(
    template_path: Path,
    simulator_name: str,
    artifact_id: str,
    api_key: str,
) -> str | None:
    """Launch a structured-execution session from a local JSON template.

    The template's root-level ``mcps_required`` list declares which MCPs to
    wire up per attached env. Supported: ``browser``, ``vm``, ``db``,
    ``functions``.
    """
    datagen_api_key = DEFAULT_DATAGEN_API_KEY

    if not DEFAULT_ANCHOR_KEY:
        console.print("[yellow]⚠️  ANCHOR_API_KEY is not set. The session will fail to launch a browser.[/yellow]")
        console.print("[yellow]   Set it with: export ANCHOR_API_KEY=<your-key>[/yellow]")
        if not typer.confirm("Continue anyway?", default=False):
            return None

    try:
        with open(template_path) as f:
            template = json.load(f)

        mcps_required = template.pop("mcps_required", ["browser"])
        mcps = await _build_mcps_for_sim(mcps_required, simulator_name, artifact_id, api_key)

        config = template["world"]["config"]
        cred_key, cred_val = _get_claude_credentials()
        _set_claude_credentials(config, cred_key, cred_val)
        agent_config = config.get("agent", {}).get("config")
        if agent_config is not None:
            _set_claude_credentials(agent_config, cred_key, cred_val)
        config["plato_api_key"] = datagen_api_key
        config["anchor_api_key"] = DEFAULT_ANCHOR_KEY
        config["browserbase_api_key"] = DEFAULT_BROWSERBASE_KEY
        config["envs"] = [
            {
                "env": {"artifact_id": artifact_id, "alias": simulator_name},
                "mcps": mcps,
                "default": True,
            }
        ]
        config["sim_name"] = simulator_name
        config["artifact_id"] = artifact_id

        plato_base_url = _get_base_url()
        subs: dict[str, str] = {
            "sim_name": simulator_name,
            "artifact_id": artifact_id,
            "plato_api_key": datagen_api_key,
            "plato_base_url": plato_base_url,
            "workspace": "/workspace",
            "mutation_threshold": str(config.get("mutation_threshold", 40)),
        }
        _render_step_instructions(config, **subs)
        _render_step_verify(config, **subs)

        template.setdefault("tags", []).append(simulator_name)

        console.print(f"[cyan]Launching {template_path.name} on Chronos for {simulator_name}...[/cyan]")
        session_id = _launch_on_chronos(template, api_key)
        return session_id

    except Exception as e:
        console.print(f"[red]❌ from-template launch failed: {e}[/red]")
        return None


async def _launch_from_template_unified(
    template_path: Path,
    sims: list[dict],
    api_key: str,
) -> str | None:
    """Launch ONE session from a local template with multiple sims attached as envs.

    Mirrors ``_launch_datagen_unified_world`` but reads the template from disk.
    ``sims`` is a list of ``{"name": str, "artifact_id": str}`` dicts. Template
    authors should reference ``config.sim_names`` (plural) rather than the
    per-sim ``{sim_name}`` placeholder — the latter is not substituted in
    unified mode.
    """
    datagen_api_key = DEFAULT_DATAGEN_API_KEY

    if not DEFAULT_ANCHOR_KEY:
        console.print("[yellow]⚠️  ANCHOR_API_KEY is not set. Browsers will fail to launch.[/yellow]")
        console.print("[yellow]   Set it with: export ANCHOR_API_KEY=<your-key>[/yellow]")
        if not typer.confirm("Continue anyway?", default=False):
            return None

    try:
        with open(template_path) as f:
            template = json.load(f)

        mcps_required = template.pop("mcps_required", ["browser"])

        envs: list[dict] = []
        for idx, sim in enumerate(sims):
            sim_mcps = await _build_mcps_for_sim(mcps_required, sim["name"], sim["artifact_id"], api_key)
            envs.append(
                {
                    "env": {"artifact_id": sim["artifact_id"], "alias": sim["name"]},
                    "mcps": sim_mcps,
                    "default": idx == 0,
                }
            )

        config = template["world"]["config"]
        cred_key, cred_val = _get_claude_credentials()
        _set_claude_credentials(config, cred_key, cred_val)
        agent_config = config.get("agent", {}).get("config")
        if agent_config is not None:
            _set_claude_credentials(agent_config, cred_key, cred_val)
        config["plato_api_key"] = datagen_api_key
        config["anchor_api_key"] = DEFAULT_ANCHOR_KEY
        config["browserbase_api_key"] = DEFAULT_BROWSERBASE_KEY
        config["envs"] = envs
        config["sim_names"] = [s["name"] for s in sims]
        # config.sim_name is populated (first sim) for templates that read from
        # world config directly, but {sim_name} placeholders in step instructions
        # / verify commands are NOT rendered in unified mode — there is no single
        # sim to substitute. Templates used with --unified should reference
        # config.sim_names (plural) from within the world, not rely on
        # placeholder substitution.
        config["sim_name"] = sims[0]["name"]

        plato_base_url = _get_base_url()
        subs: dict[str, str] = {
            "plato_api_key": datagen_api_key,
            "plato_base_url": plato_base_url,
            "workspace": "/workspace",
            "mutation_threshold": str(config.get("mutation_threshold", 40)),
        }
        _render_step_instructions(config, **subs)
        _render_step_verify(config, **subs)

        tags = template.setdefault("tags", [])
        for sim in sims:
            tags.append(sim["name"])

        console.print(f"[cyan]Launching {template_path.name} on Chronos (unified, {len(sims)} sims)...[/cyan]")
        session_id = _launch_on_chronos(template, api_key)
        return session_id

    except Exception as e:
        console.print(f"[red]❌ unified from-template launch failed: {e}[/red]")
        return None


# =============================================================================
# START COMMANDS
# =============================================================================


@start_app.command(name="env")
def start_env(
    simulators: list[str] = typer.Argument(None, help="Simulator name(s)"),
    url: str = typer.Option(
        "",
        "--url",
        help="GitHub URL for a simulator that has no record yet; the pipeline's register step creates it.",
    ),
    resume: bool = typer.Option(False, "--resume", "-r", help="Resume create pipeline from last simcreator session"),
    resume_from: str = typer.Option("", "--resume-from", help="Resume from a specific session ID"),
    fix: bool = typer.Option(False, "--fix", "-f", help="Fix rejected sim using latest env review feedback"),
    next_n: int = typer.Option(
        0,
        "--next",
        "-n",
        help="Auto-pick the N most recent not-started docker_app simulators (default 1 if flag given without value).",
    ),
):
    """Start simcreator (env pipeline) for one or more simulators.

    Moves status to env_in_progress and launches simcreator on Chronos.

    Modes:
        fresh (default): Full create pipeline from GitHub URL
        --resume / -r:   Resume create pipeline from last session's state
        --resume-from ID: Resume from a specific session ID
        --fix / -f:      Fix pipeline using base artifact + latest env review feedback

    Examples:
        plato pm start env aureus memos docmost
        plato pm start env aureus -r    # resume from last session
        plato pm start env aureus --resume-from abc123  # resume from specific session
        plato pm start env aureus -f    # fix from artifact with review feedback
        plato pm start env -n 1          # start 1 most recent not-started sim
        plato pm start env -n 10         # start 10 most recent not-started sims
    """
    if resume_from:
        resume = True
    if resume and fix:
        console.print("[red]❌ Cannot use --resume and --fix together. Pick one.[/red]")
        raise typer.Exit(1)

    if next_n < 0:
        console.print("[red]❌ -n value must be positive[/red]")
        raise typer.Exit(1)

    mode = "fix" if fix else ("resume" if resume else "fresh")
    api_key = require_api_key()

    if not simulators and next_n <= 0:
        console.print("[red]❌ No simulators specified. Provide names or use -n.[/red]")
        raise typer.Exit(1)

    async def _start():
        base_url = _get_base_url()
        datagen_api_key = DEFAULT_DATAGEN_API_KEY

        # When -n is used, fetch the full not-started pool and pick valid ones
        if next_n > 0:
            async with httpx.AsyncClient(base_url=base_url, timeout=60.0) as client:
                all_sims = await get_simulators.asyncio(client=client, x_api_key=api_key)
            candidates = []
            for s in all_sims:
                config = s.get("config", {}) if isinstance(s, dict) else getattr(s, "config", {})
                if not isinstance(config, dict):
                    continue
                if config.get("status") != "not_started":
                    continue
                if config.get("type") != "docker_app":
                    continue
                name = (s.get("name") or "") if isinstance(s, dict) else (getattr(s, "name", None) or "")
                if name:
                    candidates.append((name, s))
            if not candidates:
                console.print("[red]❌ No not-started docker_app simulators found[/red]")
                raise typer.Exit(1)
            candidates.sort(key=lambda x: x[0])
            sim_names = [name for name, _ in candidates]
        else:
            sim_names = list(simulators)

        # Fetch all sim configs, skipping ineligible ones and backfilling when using -n
        to_launch = []
        idx = 0
        target = next_n if next_n > 0 else len(sim_names)
        while idx < len(sim_names) and len(to_launch) < target:
            sim_name = sim_names[idx]
            idx += 1
            try:
                sim = None
                try:
                    async with httpx.AsyncClient(base_url=base_url, timeout=60.0) as client:
                        sim = await get_simulator_by_name.asyncio(
                            client=client,
                            name=sim_name,
                            x_api_key=api_key,
                        )
                except Exception:
                    if not (mode == "fresh" and url):
                        raise
                if sim is None:
                    if not (mode == "fresh" and url):
                        console.print(
                            f"[red]❌ {sim_name}: not found (pass --url to register it in the pipeline)[/red]"
                        )
                        continue
                    # No record yet: the pipeline's register step creates it and
                    # moves it to env_in_progress, so there is nothing to update here.
                    to_launch.append(
                        {
                            "name": sim_name,
                            "id": None,
                            "status": "unregistered",
                            "github_url": url,
                            "base_artifact_id": "",
                            "current_config": {},
                        }
                    )
                    continue
                current_config = sim_config_dict(sim.config)
                github_url = current_config.get("source_code_url", "")
                base_artifact_id = current_config.get("base_artifact_id", "")
                status = current_config.get("status", "not_started")

                if mode == "fresh" and not github_url:
                    console.print(f"[yellow]⚠️  {sim_name}: no source_code_url, skipping[/yellow]")
                    continue

                if mode == "fix" and not base_artifact_id:
                    console.print(f"[yellow]⚠️  {sim_name}: no base_artifact_id, skipping (required for fix)[/yellow]")
                    continue

                entry = {
                    "name": sim_name,
                    "id": sim.id,
                    "status": status,
                    "github_url": github_url,
                    "base_artifact_id": base_artifact_id,
                    "current_config": current_config,
                }

                # For resume or fix, find the session to resume from
                if mode in ("resume"):
                    if resume_from:
                        entry["resume_from"] = resume_from
                    else:
                        last = _get_last_chronos_session(tags=["simcreator", sim_name], api_key=api_key)
                        entry["resume_from"] = last["public_id"] if last else ""
                        if not entry["resume_from"]:
                            console.print(
                                f"[yellow]⚠️  {sim_name}: no previous simcreator session found, will start fresh[/yellow]"
                            )

                # For fix, get latest env review feedback
                if mode == "fix":
                    reviews = current_config.get("reviews") or []
                    feedback_comments = _get_latest_rejected_env_review_comments(reviews)
                    entry["feedback"] = "\n".join(feedback_comments) if feedback_comments else ""
                    if not entry["feedback"]:
                        console.print(
                            f"[yellow]⚠️  {sim_name}: no rejected env review comments found, will fix without feedback[/yellow]"
                        )

                to_launch.append(entry)
            except Exception as e:
                console.print(f"[red]❌ {sim_name}: {e}[/red]")

        if not to_launch:
            console.print("[yellow]Nothing to launch.[/yellow]")
            return

        console.print(f"\n[bold]Will launch simcreator ({mode}) for {len(to_launch)} simulator(s):[/bold]")
        for s in to_launch:
            if mode == "resume":
                extra = f"resume={s.get('resume_from', '')[:12]}"
            elif mode == "fix":
                feedback_preview = s.get("feedback", "")[:60]
                extra = f"artifact={s['base_artifact_id'][:8]}... feedback={'yes' if feedback_preview else 'none'}"
            else:
                extra = s["github_url"]
            console.print(f"  {s['name']} ({s['status']}) — {extra}")

        if not typer.confirm("\nProceed?", default=True):
            console.print("[yellow]Cancelled.[/yellow]")
            return

        # Resolve credentials once before the loop to avoid redundant subprocess calls
        cred_key, cred_val = _get_claude_credentials()

        for s in to_launch:
            try:
                if s["id"] is not None:
                    async with httpx.AsyncClient(base_url=base_url, timeout=60.0) as client:
                        await update_simulator_status.asyncio(
                            client=client,
                            simulator_id=s["id"],
                            body=UpdateStatusRequest(status=Status("env_in_progress")),
                            x_api_key=api_key,
                        )

                if mode == "fresh":
                    template, version_id = _fetch_experiment_config("env", "base", api_key)
                    config = template["world"]["config"]
                    config["sim_name"] = s["name"]
                    config["github_url"] = s["github_url"]
                    _render_step_instructions(
                        config,
                        sim_name=s["name"],
                        github_url=s["github_url"],
                        workspace="/workspace",
                    )
                    _render_step_verify(config, sim_name=s["name"], github_url=s["github_url"])
                    config["plato_api_key"] = datagen_api_key
                    _set_claude_credentials(config, cred_key, cred_val)
                    config["agent"]["config"]["plato_api_key"] = datagen_api_key
                    _set_claude_credentials(config["agent"]["config"], cred_key, cred_val)
                    template["tags"].append(s["name"])

                elif mode == "resume":
                    template, version_id = _fetch_experiment_config("env", "base", api_key)
                    config = template["world"]["config"]
                    config["sim_name"] = s["name"]
                    config["github_url"] = s["github_url"]
                    _render_step_instructions(
                        config,
                        sim_name=s["name"],
                        github_url=s["github_url"],
                        workspace="/workspace",
                    )
                    _render_step_verify(config, sim_name=s["name"], github_url=s["github_url"])
                    config["plato_api_key"] = datagen_api_key
                    _set_claude_credentials(config, cred_key, cred_val)
                    config["agent"]["config"]["plato_api_key"] = datagen_api_key
                    _set_claude_credentials(config["agent"]["config"], cred_key, cred_val)
                    config["state"]["resume_from"] = s.get("resume_from", "")
                    template["tags"].append(s["name"])
                    template["tags"].append("resume")

                else:  # fix
                    template, version_id = _fetch_experiment_config("env", "fix", api_key)
                    config = template["world"]["config"]
                    config["sim_name"] = s["name"]
                    data_artifact_id = s.get("current_config", {}).get("data_artifact_id") or ""
                    _render_step_instructions(
                        config,
                        sim_name=s["name"],
                        feedback=s.get("feedback", ""),
                        artifact_id=s["base_artifact_id"],
                        data_artifact_section=_render_data_artifact_section(data_artifact_id),
                        workspace="/workspace",
                    )
                    config["plato_api_key"] = datagen_api_key
                    _set_claude_credentials(config, cred_key, cred_val)
                    config["agent"]["config"]["plato_api_key"] = datagen_api_key
                    _set_claude_credentials(config["agent"]["config"], cred_key, cred_val)
                    config["state"]["resume_from"] = s.get("resume_from", "")
                    template["tags"].append(s["name"])
                session_id = _launch_on_chronos(template, api_key)
                _attach_session_to_experiment(version_id, session_id, api_key)
                console.print(f"[green]✅ {s['name']}:[/green] {session_id}")
            except Exception as e:
                console.print(f"[red]❌ {s['name']}: {e}[/red]")

    handle_async(_start())


@start_app.command(name="data")
def start_data(
    simulators: list[str] = typer.Argument(..., help="Simulator name(s)"),
    resume: bool = typer.Option(
        False,
        "--resume",
        "-r",
        help="Rerun datagen from the current data artifact using the latest rejected data review comments",
    ),
    unified: bool = typer.Option(
        False,
        "--unified",
        help="Run all listed sims in one session with a shared scenario. Each sim gets its own env + MCPs; snapshots are created per env but no data artifact is submitted for review.",
    ),
):
    """Start datagen (data pipeline) for one or more simulators.

    Moves status to data_in_progress, sets default assignees if missing,
    and launches an interactive datagen world on Chronos.

    Examples:
        plato pm start data aureus memos
        plato pm start data aureus -r    # rerun from current data_artifact_id with latest reject comments
        plato pm start data crm gmail pm --unified    # one session with shared scenario across sims
    """
    api_key = require_api_key()

    if unified and resume:
        console.print(
            "[red]--unified and --resume are not supported together yet (resume replays per-sim review comments).[/red]"
        )
        raise typer.Exit(1)
    if unified and len(simulators) < 2:
        console.print(
            "[red]--unified requires 2 or more sims. Use plain `plato pm start data <sim>` for a single sim.[/red]"
        )
        raise typer.Exit(1)
    if unified:
        seen: set[str] = set()
        duplicates: list[str] = []
        for sim_name in simulators:
            if sim_name in seen and sim_name not in duplicates:
                duplicates.append(sim_name)
            seen.add(sim_name)
        if duplicates:
            console.print(
                f"[red]--unified requires unique simulator names (each becomes an env alias). Duplicates: {', '.join(duplicates)}[/red]"
            )
            raise typer.Exit(1)

    async def _start():
        base_url = _get_base_url()

        # Fetch all sim configs
        to_launch = []
        for sim_name in simulators:
            try:
                async with httpx.AsyncClient(base_url=base_url, timeout=60.0) as client:
                    sim = await get_simulator_by_name.asyncio(
                        client=client,
                        name=sim_name,
                        x_api_key=api_key,
                    )
                current_config = sim_config_dict(sim.config)
                status = current_config.get("status", "not_started")
                base_artifact_id = current_config.get("base_artifact_id", "")
                data_artifact_id = current_config.get("data_artifact_id", "")
                artifact_id = data_artifact_id if resume and data_artifact_id else base_artifact_id

                if resume and (not data_artifact_id) and base_artifact_id:
                    console.print(
                        f"[yellow]⚠️  {sim_name}: no data_artifact_id, falling back to base_artifact_id for resume[/yellow]"
                    )

                if not artifact_id:
                    missing_field = "data_artifact_id/base_artifact_id" if resume else "base_artifact_id"
                    console.print(f"[yellow]⚠️  {sim_name}: no {missing_field}, skipping[/yellow]")
                    continue

                to_launch.append(
                    {
                        "name": sim_name,
                        "id": sim.id,
                        "status": status,
                        "artifact_id": artifact_id,
                        "data_assignees": current_config.get("data_assignees"),
                        "data_review_assignees": current_config.get("data_review_assignees"),
                        "review_comments": None,
                    }
                )

                if resume:
                    reviews = current_config.get("reviews") or []
                    latest_reject_comments = _get_latest_rejected_data_review_comments(reviews)

                    if latest_reject_comments:
                        to_launch[-1]["review_comments"] = latest_reject_comments
                    else:
                        console.print(
                            f"[yellow]⚠️  {sim_name}: no rejected data review found, will launch with the base datagen prompt[/yellow]"
                        )
            except Exception as e:
                console.print(f"[red]❌ {sim_name}: {e}[/red]")

        if not to_launch:
            console.print("[yellow]Nothing to launch.[/yellow]")
            return

        mode = "unified" if unified else ("rerun" if resume else "fresh")
        label = (
            f"\n[bold]Will launch unified datagen ({len(to_launch)} sims in one session):[/bold]"
            if unified
            else f"\n[bold]Will launch datagen ({mode}) for {len(to_launch)} simulator(s):[/bold]"
        )
        console.print(label)
        for s in to_launch:
            extra = f"artifact {s['artifact_id'][:8]}..."
            if resume:
                comments = s.get("review_comments")
                if comments is not None:
                    extra += f", review_comments={len(comments)}"
            console.print(f"  {s['name']} ({s['status']}) — {extra}")

        if not typer.confirm("\nProceed?", default=True):
            console.print("[yellow]Cancelled.[/yellow]")
            return

        async def _prep_sim(s: dict) -> None:
            async with httpx.AsyncClient(base_url=base_url, timeout=60.0) as client:
                updates = {}
                if not s["data_assignees"]:
                    updates["data_assignees"] = DEFAULT_DATA_ASSIGNEES
                if not s["data_review_assignees"]:
                    updates["data_review_assignees"] = DEFAULT_DATA_REVIEW_ASSIGNEES
                if updates:
                    await update_simulator.asyncio(
                        client=client,
                        simulator_id=s["id"],
                        body=AppApiV1SimulatorRoutesUpdateSimulatorRequest(**updates),
                        x_api_key=api_key,
                    )

                if s["status"] != "data_in_progress":
                    await update_simulator_status.asyncio(
                        client=client,
                        simulator_id=s["id"],
                        body=UpdateStatusRequest(status=Status("data_in_progress")),
                        x_api_key=api_key,
                    )
                else:
                    console.print(f"[cyan]{s['name']}: already in data_in_progress, re-launching datagen[/cyan]")

        if unified:
            try:
                for s in to_launch:
                    await _prep_sim(s)

                launched = await _launch_datagen_unified_world(
                    sims=[{"name": s["name"], "artifact_id": s["artifact_id"]} for s in to_launch],
                    api_key=api_key,
                )
                if launched:
                    console.print(
                        f"[green]✅ unified session for {', '.join(s['name'] for s in to_launch)}:[/green] {launched}"
                    )
                else:
                    console.print("[red]❌ unified datagen: launch returned None[/red]")
            except Exception as e:
                console.print(f"[red]❌ unified datagen: {e}[/red]")
            return

        for s in to_launch:
            try:
                await _prep_sim(s)
                launched = await _launch_datagen_world(
                    simulator_name=s["name"],
                    artifact_id=s["artifact_id"],
                    api_key=api_key,
                    review_comments=s.get("review_comments") if resume else None,
                )
                if launched:
                    console.print(f"[green]✅ {s['name']}:[/green] {launched}")
                else:
                    console.print(f"[red]❌ {s['name']}: launch returned None[/red]")
            except Exception as e:
                console.print(f"[red]❌ {s['name']}: {e}[/red]")

    handle_async(_start())


@start_app.command(name="checker")
def start_checker(
    simulators: list[str] = typer.Argument(..., help="Simulator name(s)"),
    artifact: str = typer.Option(
        "",
        "-a",
        "--artifact",
        help="Override artifact ID (skips simulator lookup, exactly one simulator name required)",
    ),
    use_base: bool = typer.Option(
        False,
        "--base",
        help="Check base_artifact_id instead of data_artifact_id (pre-datagen check)",
    ),
):
    """Run the sim-checker QA pass for one or more simulators.

    Spins up a structured-execution session per simulator that verifies the app loads,
    walks every main nav section, performs 2-3 real DB mutations, and writes a
    pass/fail verdict with warning flags to the Chronos session result
    (result.data.output = sim-check-result.json).

    By default each sim's data_artifact_id is checked; falls back to base_artifact_id
    if no data artifact exists. Pass --base to force checking base_artifact_id.

    Examples:
        plato pm start checker aureus
        plato pm start checker aureus memos
        plato pm start checker aureus --base
        plato pm start checker aureus -a 9c744a5b-f52c-40a7-ad67-c3863b34c68d
    """
    api_key = require_api_key()

    if artifact and len(simulators) != 1:
        console.print("[red]❌ --artifact can only be used with exactly one simulator name[/red]")
        raise typer.Exit(code=1)

    async def _start():
        base_url = _get_base_url()

        to_launch = []
        if artifact:
            to_launch.append({"name": simulators[0], "artifact_id": artifact, "source": "override"})
        else:
            for sim_name in simulators:
                try:
                    async with httpx.AsyncClient(base_url=base_url, timeout=60.0) as client:
                        sim = await get_simulator_by_name.asyncio(
                            client=client,
                            name=sim_name,
                            x_api_key=api_key,
                        )
                    current_config = sim_config_dict(sim.config)
                    base_artifact_id = current_config.get("base_artifact_id", "")
                    data_artifact_id = current_config.get("data_artifact_id", "")

                    if use_base:
                        artifact_id = base_artifact_id
                        source = "base_artifact_id"
                    else:
                        artifact_id = data_artifact_id or base_artifact_id
                        source = "data_artifact_id" if data_artifact_id else "base_artifact_id"

                    if not artifact_id:
                        missing = "base_artifact_id" if use_base else "data_artifact_id/base_artifact_id"
                        console.print(f"[yellow]⚠️  {sim_name}: no {missing}, skipping[/yellow]")
                        continue

                    to_launch.append({"name": sim_name, "artifact_id": artifact_id, "source": source})
                except Exception as e:
                    console.print(f"[red]❌ {sim_name}: {e}[/red]")

        if not to_launch:
            console.print("[yellow]Nothing to launch.[/yellow]")
            return

        console.print(f"\n[bold]Will launch sim-checker for {len(to_launch)} simulator(s):[/bold]")
        for s in to_launch:
            console.print(f"  {s['name']} — artifact {s['artifact_id'][:8]}... ({s['source']})")

        if not typer.confirm("\nProceed?", default=True):
            console.print("[yellow]Cancelled.[/yellow]")
            return

        for s in to_launch:
            try:
                launched = await _launch_sim_checker_world(
                    simulator_name=s["name"],
                    artifact_id=s["artifact_id"],
                    api_key=api_key,
                )
                if launched:
                    console.print(f"[green]✅ {s['name']}:[/green] {launched}")
                else:
                    console.print(f"[red]❌ {s['name']}: launch returned None[/red]")
            except Exception as e:
                console.print(f"[red]❌ {s['name']}: {e}[/red]")

    handle_async(_start())


async def _launch_simcreator_blank_world(
    simulator_name: str,
    artifact_id: str,
    api_key: str,
    operator_message: str | None = None,
) -> str | None:
    """Launch a simcreator-blank session, fetching the template from Chronos.

    Same template shape as the legacy `_launch_from_template_world` path
    (root-level `mcps_required`, structured-execution world.config), but the
    config is pulled from the `simcreator-blank-launch` experiment version
    instead of a local JSON file. That removes the "ship a new SDK to the
    box launching this" dependency — you push the experiment once, every
    caller (manual + the simcreator chain step) picks it up.
    """
    datagen_api_key = DEFAULT_DATAGEN_API_KEY

    if not DEFAULT_ANCHOR_KEY:
        console.print("[yellow]⚠️  ANCHOR_API_KEY is not set. The session will fail to launch a browser.[/yellow]")
        console.print("[yellow]   Set it with: export ANCHOR_API_KEY=<your-key>[/yellow]")

    try:
        template, version_id = _fetch_experiment_config("blank", "base", api_key)

        mcps_required = template.pop("mcps_required", ["browser"])
        mcps = await _build_mcps_for_sim(mcps_required, simulator_name, artifact_id, api_key)

        config = template["world"]["config"]
        cred_key, cred_val = _get_claude_credentials()
        _set_claude_credentials(config, cred_key, cred_val)
        agent_config = config.get("agent", {}).get("config")
        if agent_config is not None:
            _set_claude_credentials(agent_config, cred_key, cred_val)
        config["plato_api_key"] = datagen_api_key
        config["anchor_api_key"] = DEFAULT_ANCHOR_KEY
        config["browserbase_api_key"] = DEFAULT_BROWSERBASE_KEY
        config["envs"] = [
            {
                "env": {"artifact_id": artifact_id, "alias": simulator_name},
                "mcps": mcps,
                "default": True,
            }
        ]
        config["sim_name"] = simulator_name
        config["artifact_id"] = artifact_id

        plato_base_url = _get_base_url()
        subs: dict[str, str] = {
            "sim_name": simulator_name,
            "artifact_id": artifact_id,
            "plato_api_key": datagen_api_key,
            "plato_base_url": plato_base_url,
            "workspace": "/workspace",
            "mutation_threshold": str(config.get("mutation_threshold", 40)),
            "operator_message_section": _render_operator_message_section(operator_message),
        }
        _render_step_instructions(config, **subs)
        _render_step_verify(config, **subs)

        template.setdefault("tags", []).append(simulator_name)

        console.print(f"[cyan]Launching simcreator-blank on Chronos for {simulator_name}...[/cyan]")
        session_id = _launch_on_chronos(template, api_key)
        _attach_session_to_experiment(version_id, session_id, api_key)
        return session_id

    except Exception as e:
        console.print(f"[red]❌ simcreator-blank launch failed: {e}[/red]")
        return None


@start_app.command(name="blank")
def start_blank(
    simulators: list[str] = typer.Argument(..., help="Simulator name(s)"),
    artifact: str = typer.Option(
        "",
        "-a",
        "--artifact-id",
        help="Explicit artifact UUID. Requires exactly one simulator name.",
    ),
    use_base: bool = typer.Option(
        False,
        "--base",
        help="Use base_artifact_id (pre-datagen snapshot). This is the default for `start blank`.",
    ),
    use_data: bool = typer.Option(
        False,
        "--data",
        help="Use data_artifact_id (post-datagen snapshot). Opt in when you specifically want to clean the data-side artifact (rare for manual blank).",
    ),
    yes: bool = typer.Option(
        False,
        "-y",
        "--yes",
        help="Skip the interactive confirmation prompt (for non-interactive callers like the simcreator chain).",
    ),
    message: str = typer.Option(
        "",
        "-m",
        "--message",
        help="Optional operator note injected into the agent's plan step (e.g. 'leftover Test Company LLC in clients'). Hint, not spec.",
    ),
):
    """Run the simcreator-blank pipeline on one or more simulators.

    Strips synthetic data from a sim's artifact, leaving the app in a
    "fresh deploy + admin user" state, and promotes the cleaned artifact
    as the new base_artifact_id. Also walks any first-run wizard exposed
    by the clear and does the snapshot-hygiene pass (clear audit_log via
    clear-audit, leaving the audit triggers and audit_log table in place)
    so the artifact stays clean across reset() with audit infra intact.

    Fetches the launch config from the ``simcreator-blank-launch`` Chronos
    experiment. Push a new version with ``plato pm experiment blank base push``.

    Examples:
        plato pm start blank espocrm
        plato pm start blank espocrm memos --base
        plato pm start blank espocrm -a 56f85a14-8e82-4053-a7df-8490c31a14e3
        plato pm start blank espocrm -m "two leftover rows in clients table"
    """
    if use_base and use_data:
        console.print("[red]❌ --base and --data are mutually exclusive.[/red]")
        raise typer.Exit(1)

    api_key = require_api_key()

    if artifact and len(simulators) != 1:
        console.print("[red]❌ --artifact-id can only be used with exactly one simulator name[/red]")
        raise typer.Exit(1)

    async def _start():
        base_url = _get_base_url()

        to_launch = []
        for raw in simulators:
            if UUID_PATTERN.match(raw):
                to_launch.append({"name": f"artifact-{raw[:8]}", "artifact_id": raw, "source": "raw_artifact_uuid"})
                continue

            sim_name, colon_artifact = _split_sim_colon_arg(raw, command_name="start blank")
            if colon_artifact:
                to_launch.append({"name": sim_name, "artifact_id": colon_artifact, "source": "colon_notation"})
                continue

            if artifact and raw == simulators[0] and len(simulators) == 1:
                to_launch.append({"name": sim_name, "artifact_id": artifact, "source": "override"})
                continue

            try:
                async with httpx.AsyncClient(base_url=base_url, timeout=60.0) as client:
                    sim = await get_simulator_by_name.asyncio(client=client, name=sim_name, x_api_key=api_key)
                current_config = sim_config_dict(sim.config)
                base_artifact_id = current_config.get("base_artifact_id", "")
                data_artifact_id = current_config.get("data_artifact_id", "")

                if use_data:
                    artifact_id = data_artifact_id
                    source = "data_artifact_id"
                else:
                    # Default: prefer base (the clean env-approved snapshot). The
                    # data artifact often has datagen-induced state that breaks
                    # cleanup heuristics (e.g. permission rows wiped, broken
                    # admin nav). Opt into --data only when you specifically
                    # want to clean the data-side artifact.
                    artifact_id = base_artifact_id
                    source = "base_artifact_id"

                if not artifact_id:
                    missing = "data_artifact_id" if use_data else "base_artifact_id"
                    console.print(f"[yellow]⚠️  {sim_name}: no {missing}, skipping[/yellow]")
                    continue

                to_launch.append({"name": sim_name, "artifact_id": artifact_id, "source": source})
            except Exception as e:
                console.print(f"[red]❌ {sim_name}: {e}[/red]")

        if not to_launch:
            console.print("[yellow]Nothing to launch.[/yellow]")
            return

        console.print(f"\n[bold]Will launch simcreator-blank (one session per {len(to_launch)} simulator(s)):[/bold]")
        for s in to_launch:
            console.print(f"  {s['name']} — artifact {s['artifact_id'][:8]}... ({s['source']})")

        if not yes and not typer.confirm("\nProceed?", default=True):
            console.print("[yellow]Cancelled.[/yellow]")
            return

        for s in to_launch:
            try:
                launched = await _launch_simcreator_blank_world(
                    simulator_name=s["name"],
                    artifact_id=s["artifact_id"],
                    api_key=api_key,
                    operator_message=message,
                )
                if launched:
                    console.print(f"[green]✅ {s['name']}:[/green] {launched}")
                else:
                    console.print(f"[red]❌ {s['name']}: launch returned None[/red]")
            except Exception as e:
                console.print(f"[red]❌ {s['name']}: {e}[/red]")

    handle_async(_start())


@start_app.command(name="from-template")
def start_from_template(
    template: str = typer.Argument(
        ..., help="Path to a local JSON launch template (e.g. extract-screenshots-launch.json)"
    ),
    simulators: list[str] = typer.Argument(..., help="Simulator name(s)"),
    artifact: str = typer.Option(
        "",
        "-a",
        "--artifact-id",
        help="Explicit artifact UUID. Requires exactly one simulator name.",
    ),
    use_base: bool = typer.Option(
        False,
        "--base",
        help="Use base_artifact_id (pre-datagen snapshot).",
    ),
    use_data: bool = typer.Option(
        False,
        "--data",
        help="Use data_artifact_id (post-datagen snapshot). Default behavior already falls back to base if missing.",
    ),
    unified: bool = typer.Option(
        False,
        "--unified",
        help="Launch ONE session with all sims attached as envs (mirrors datagen unified mode). The template must be written to handle multiple envs (reference config.sim_names).",
    ),
    yes: bool = typer.Option(
        False,
        "-y",
        "--yes",
        help="Skip the interactive confirmation prompt (for non-interactive callers).",
    ),
):
    """Launch Chronos session(s) from a local JSON template.

    Scoped for templates that attach a simulator env with a browser (and
    optionally vm) MCP — i.e. sim-checker and extract_screenshots. The template
    is read from disk; nothing is uploaded to Chronos. The template's root-level
    ``mcps_required`` list declares which MCPs to wire up per env. ``{sim_name}``,
    ``{artifact_id}``, ``{plato_api_key}``, ``{plato_base_url}``, and
    ``{workspace}`` are substituted into each step's instruction and verify.

    Default mode launches one session per simulator. ``--unified`` launches a
    single session with all simulators attached as separate envs (only
    ``{plato_api_key}``, ``{plato_base_url}``, ``{workspace}`` are substituted —
    per-sim placeholders are skipped since there is more than one).

    By default each sim's data_artifact_id is used, falling back to
    base_artifact_id if no data artifact exists. Pass ``--base`` to force base,
    or ``-a <uuid>`` to override explicitly.

    Examples:
        plato pm start from-template python-sdk/templates/extract-screenshots-launch.json aureus memos
        plato pm start from-template ./extract-screenshots-launch.json aureus --base
        plato pm start from-template ./extract-screenshots-launch.json aureus -a 9c744a5b-f52c-40a7-ad67-c3863b34c68d
        plato pm start from-template ./extract-screenshots-unified.json aureus memos docmost --unified
    """
    if use_base and use_data:
        console.print("[red]❌ --base and --data are mutually exclusive.[/red]")
        raise typer.Exit(1)

    template_path = Path(template).expanduser().resolve()
    if not template_path.exists():
        console.print(f"[red]❌ Template not found: {template_path}[/red]")
        raise typer.Exit(1)

    api_key = require_api_key()

    if artifact and len(simulators) != 1:
        console.print("[red]❌ --artifact-id can only be used with exactly one simulator name[/red]")
        raise typer.Exit(1)

    if unified and artifact:
        console.print(
            "[red]❌ --unified and --artifact-id are mutually exclusive (unified resolves artifacts per sim).[/red]"
        )
        raise typer.Exit(1)

    async def _start():
        base_url = _get_base_url()

        to_launch = []
        for raw in simulators:
            # Bare artifact UUID: use directly, skip sim-name lookup. --artifact-id
            # override doesn't apply here (the positional IS the artifact).
            if UUID_PATTERN.match(raw):
                to_launch.append({"name": f"artifact-{raw[:8]}", "artifact_id": raw, "source": "raw_artifact_uuid"})
                continue

            # sim:<uuid> colon notation: explicit artifact, no API lookup.
            sim_name, colon_artifact = _split_sim_colon_arg(raw, command_name="start from-template")
            if colon_artifact:
                to_launch.append({"name": sim_name, "artifact_id": colon_artifact, "source": "colon_notation"})
                continue

            # --artifact-id override applies to the (single) sim name.
            if artifact and raw == simulators[0] and len(simulators) == 1:
                to_launch.append({"name": sim_name, "artifact_id": artifact, "source": "override"})
                continue

            try:
                async with httpx.AsyncClient(base_url=base_url, timeout=60.0) as client:
                    sim = await get_simulator_by_name.asyncio(client=client, name=sim_name, x_api_key=api_key)
                current_config = sim_config_dict(sim.config)
                base_artifact_id = current_config.get("base_artifact_id", "")
                data_artifact_id = current_config.get("data_artifact_id", "")

                if use_base:
                    artifact_id = base_artifact_id
                    source = "base_artifact_id"
                else:
                    artifact_id = data_artifact_id or base_artifact_id
                    source = "data_artifact_id" if data_artifact_id else "base_artifact_id"

                if not artifact_id:
                    missing = "base_artifact_id" if use_base else "data_artifact_id/base_artifact_id"
                    console.print(f"[yellow]⚠️  {sim_name}: no {missing}, skipping[/yellow]")
                    continue

                to_launch.append({"name": sim_name, "artifact_id": artifact_id, "source": source})
            except Exception as e:
                console.print(f"[red]❌ {sim_name}: {e}[/red]")

        if not to_launch:
            console.print("[yellow]Nothing to launch.[/yellow]")
            return

        mode_label = "unified session across" if unified else "one session per"
        console.print(f"\n[bold]Will launch {template_path.name} ({mode_label} {len(to_launch)} simulator(s)):[/bold]")
        for s in to_launch:
            console.print(f"  {s['name']} — artifact {s['artifact_id'][:8]}... ({s['source']})")

        if not yes and not typer.confirm("\nProceed?", default=True):
            console.print("[yellow]Cancelled.[/yellow]")
            return

        if unified:
            try:
                launched = await _launch_from_template_unified(
                    template_path=template_path,
                    sims=[{"name": s["name"], "artifact_id": s["artifact_id"]} for s in to_launch],
                    api_key=api_key,
                )
                if launched:
                    console.print(f"[green]✅ unified:[/green] {launched}")
                else:
                    console.print("[red]❌ unified: launch returned None[/red]")
            except Exception as e:
                console.print(f"[red]❌ unified: {e}[/red]")
            return

        for s in to_launch:
            try:
                launched = await _launch_from_template_world(
                    template_path=template_path,
                    simulator_name=s["name"],
                    artifact_id=s["artifact_id"],
                    api_key=api_key,
                )
                if launched:
                    console.print(f"[green]✅ {s['name']}:[/green] {launched}")
                else:
                    console.print(f"[red]❌ {s['name']}: launch returned None[/red]")
            except Exception as e:
                console.print(f"[red]❌ {s['name']}: {e}[/red]")

    handle_async(_start())


# =============================================================================
# OPEN COMMAND — interactive Playwright session
# =============================================================================


@pm_app.command(name="open")
def open_sim(
    simulators: list[str] = typer.Argument(
        ...,
        help="Simulator name(s), bare artifact UUIDs, or sim:<artifact-uuid> colon notation.",
    ),
    artifact: str = typer.Option(
        "",
        "-a",
        "--artifact-id",
        help="Explicit artifact UUID. Requires exactly one simulator name.",
    ),
    use_base: bool = typer.Option(
        False,
        "--base",
        help="Use base_artifact_id (pre-datagen snapshot).",
    ),
    use_data: bool = typer.Option(
        False,
        "--data",
        help="Use data_artifact_id (post-datagen snapshot). Default already falls back to base if missing.",
    ),
    headless: bool = typer.Option(
        False,
        "--headless",
        help="Run Playwright headless (default: headed).",
    ),
    dataset: str = typer.Option(
        "base",
        "--dataset",
        help="Flow dataset. 'base' runs the 'login' flow; any other value runs the flow with that name.",
    ),
    timeout: int = typer.Option(
        1800,
        "--timeout",
        help="VM ready timeout in seconds (default: 1800).",
    ),
):
    """Open one or more sims in a Playwright browser with the login flow executed.

    Creates a single Plato session with one env per simulator, resets, runs the
    sim's declared login flow in a shared Playwright context, and blocks until
    you press Enter. One tab per sim.

    Each positional argument is one of:
        - a simulator name (resolves via --base/--data/-a)
        - a bare artifact UUID (used directly, skips sim lookup)
        - ``sim:<artifact-uuid>`` colon notation for an explicit artifact

    ``-a`` is equivalent to colon notation but requires a single simulator arg.

    Examples:
        plato pm open mattermost
        plato pm open mattermost --base
        plato pm open mattermost aureus memos                       # three tabs, one session
        plato pm open mattermost:1b642f11-...                       # colon notation
        plato pm open b07fcb30-6af9-4e28-bef3-1aa6764b93c9           # bare artifact UUID
        plato pm open b07fcb30-... 5eea5b08-...                      # two bare UUIDs
        plato pm open mattermost -a 1b642f11-...
        plato pm open mattermost --headless --dataset login_admin
    """
    if use_base and use_data:
        console.print("[red]❌ --base and --data are mutually exclusive.[/red]")
        raise typer.Exit(1)
    if artifact and len(simulators) != 1:
        console.print("[red]❌ --artifact-id can only be used with exactly one simulator name[/red]")
        raise typer.Exit(1)
    if artifact and simulators and UUID_PATTERN.match(simulators[0]):
        console.print("[red]❌ --artifact-id was given but the positional is already an artifact UUID. Pick one.[/red]")
        raise typer.Exit(1)

    api_key = require_api_key()

    async def _resolve() -> list[dict]:
        base_url = _get_base_url()
        resolved: list[dict] = []
        for raw in simulators:
            # Bare artifact UUIDs skip the sim-name lookup entirely.
            if UUID_PATTERN.match(raw):
                resolved.append({"name": f"artifact-{raw[:8]}", "artifact_id": raw, "source": "raw_artifact_uuid"})
                continue

            sim_name, colon_artifact = _split_sim_colon_arg(raw, command_name="open")
            override = artifact or colon_artifact

            if override:
                resolved.append({"name": sim_name, "artifact_id": override, "source": "override"})
                continue

            try:
                async with httpx.AsyncClient(base_url=base_url, timeout=60.0) as client:
                    sim = await get_simulator_by_name.asyncio(client=client, name=sim_name, x_api_key=api_key)
                current_config = sim_config_dict(sim.config)
                base_artifact_id = current_config.get("base_artifact_id", "")
                data_artifact_id = current_config.get("data_artifact_id", "")

                if use_base:
                    artifact_id = base_artifact_id
                    source = "base_artifact_id"
                else:
                    artifact_id = data_artifact_id or base_artifact_id
                    source = "data_artifact_id" if data_artifact_id else "base_artifact_id"

                if not artifact_id:
                    missing = "base_artifact_id" if use_base else "data_artifact_id/base_artifact_id"
                    console.print(f"[yellow]⚠️  {sim_name}: no {missing}, skipping[/yellow]")
                    continue

                resolved.append({"name": sim_name, "artifact_id": artifact_id, "source": source})
            except Exception as e:
                console.print(f"[red]❌ {sim_name}: {e}[/red]")
        return resolved

    to_open = handle_async(_resolve())
    if not to_open:
        console.print("[yellow]Nothing to open.[/yellow]")
        raise typer.Exit(1)

    console.print(f"\n[bold]Will open {len(to_open)} sim(s) in one Playwright session:[/bold]")
    for s in to_open:
        console.print(f"  {s['name']} — artifact {s['artifact_id'][:8]}... ({s['source']})")

    # Playwright is not a runtime dep, import lazily so the rest of `plato pm`
    # keeps working without it installed.
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        console.print(
            "[red]❌ playwright is not installed. Run: uv pip install playwright && playwright install chromium[/red]"
        )
        raise typer.Exit(1) from None

    plato = PlatoV2()
    session = None
    try:
        envs = [EnvV2.artifact(s["artifact_id"]) for s in to_open]
        console.print("[cyan]Creating session...[/cyan]")
        session = plato.sessions.create(envs=envs, timeout=timeout)
        console.print(f"[green]Session ready:[/green] {session.session_id}")

        console.print("[cyan]Resetting session...[/cyan]")
        session.reset()

        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=headless)
            try:
                console.print(f"[cyan]Running '{dataset}' flow on each env...[/cyan]")
                login_result = session.login(browser, dataset=dataset)

                console.print("\n[bold green]Logged in. Pages:[/bold green]")
                for alias, page in login_result.pages.items():
                    console.print(f"  {alias}: {page.url}")

                console.print("\n[bold]Browser is open. Press Enter to close session and quit.[/bold]")
                try:
                    input()
                except EOFError:
                    pass
            finally:
                browser.close()
    finally:
        if session is not None:
            console.print("[cyan]Closing session...[/cyan]")
            try:
                session.close()
            except Exception as e:
                console.print(f"[yellow]⚠️  Session close failed: {e}[/yellow]")
        plato.close()


# =============================================================================
# ARCHIVE COMMAND
# =============================================================================


@register_app.command(name="env")
def register_env(
    name: str = typer.Argument(..., help="Simulator name (lowercase letters and underscores)"),
    url: str = typer.Option(..., "--url", help="GitHub URL of the app"),
    description: str | None = typer.Option(None, "--description", "-d", help="One-line description"),
    img_url: str | None = typer.Option(None, "--img-url", help="Favicon / logo URL"),
    check: bool = typer.Option(False, "--check", help="Verify only: exit 1 unless the record is complete"),
    json_output: bool = typer.Option(False, "--json", help="Print the record as JSON"),
):
    """Create or complete the simulator record the env pipeline builds into.

    Idempotent — the pipeline's ``register`` step runs it, and re-running is safe:
    creates the record if missing (docker_app, oss, enabled), fills url /
    description / favicon when given, and moves ``not_started`` →
    ``env_in_progress``. A simulator in any other status is left alone.

    Examples:
        plato pm register env grist --url https://github.com/gristlabs/grist-core \
            -d "Grist — the evolution of spreadsheets" --img-url https://www.getgrist.com/favicon.ico
        plato pm register env grist --url https://github.com/gristlabs/grist-core --check
    """
    api_key = require_api_key()
    base_url = _get_base_url()

    async def _run() -> bool:
        async with httpx.AsyncClient(base_url=base_url, timeout=60.0) as client:
            try:
                sim = await get_simulator_by_name.asyncio(client=client, name=name, x_api_key=api_key)
            except Exception:
                sim = None

            def _record(sim_obj, created: bool) -> dict:
                cfg = sim_config_dict(sim_obj.config) if sim_obj else {}
                extra = getattr(sim_obj, "model_extra", None) or {}
                return {
                    "name": name,
                    "id": getattr(sim_obj, "id", None),
                    "created": created,
                    "enabled": bool(getattr(sim_obj, "enabled", False)),
                    "status": cfg.get("status"),
                    "url": getattr(sim_obj, "url", None),
                    "description": getattr(sim_obj, "description", None),
                    "img_url": getattr(sim_obj, "img_url", None) or extra.get("imgUrl") or extra.get("img_url"),
                }

            def _missing(rec: dict) -> list[str]:
                problems = []
                if rec["id"] is None:
                    return ["record does not exist"]
                if not rec["enabled"]:
                    problems.append("enabled is false (start-services cannot find a disabled sim in Gitea)")
                if rec["status"] != "env_in_progress":
                    problems.append(f"status is {rec['status']!r}, expected env_in_progress")
                for field in ("url", "description", "img_url"):
                    if not rec[field]:
                        problems.append(f"{field} is empty")
                return problems

            if check:
                rec = _record(sim, False)
                problems = _missing(rec)
                if json_output:
                    print(json.dumps({**rec, "problems": problems}))
                elif problems:
                    for problem in problems:
                        console.print(f"[red]❌ {name}: {problem}[/red]")
                else:
                    console.print(f"[green]✅ {name}: registered (id={rec['id']}, {rec['status']})[/green]")
                return not problems

            created = False
            if sim is None:
                body = CreateSimulatorRequest(
                    name=name,
                    url=url,
                    description=description or "",
                    # model_validate: the generated SimulatorConfig types `type`/`status` as enums and
                    # has no `source_code_url` field, but the backend reads it (pm start env does too).
                    config=SimulatorConfig.model_validate(
                        {"type": "docker_app", "status": "not_started", "source_code_url": url}
                    ),
                    enabled=True,
                    kind="oss",
                    simType="docker_app",
                )
                sim = await create_simulator.asyncio(client=client, body=body, x_api_key=api_key)
                created = True

            cfg = sim_config_dict(sim.config)
            status = cfg.get("status") or "not_started"
            if status not in ("not_started", "env_in_progress"):
                console.print(
                    f"[red]❌ {name}: status is {status!r}; refusing to touch a simulator past env_in_progress[/red]"
                )
                return False

            update = AppApiV1EnvRoutesUpdateSimulatorRequest()
            changed = False
            if not sim.enabled:
                update.enabled = True
                changed = True
            if url and sim.url != url:
                update.url = url
                changed = True
            if description and sim.description != description:
                update.description = description
                changed = True
            if img_url:
                # The generated model predates imgUrl; the backend reads it by alias.
                update.__pydantic_extra__ = {**(update.__pydantic_extra__ or {}), "imgUrl": img_url}
                changed = True
            if changed:
                sim = await env_update_simulator.asyncio(client=client, id=sim.id, body=update, x_api_key=api_key)

            if status == "not_started":
                await update_simulator_status.asyncio(
                    client=client,
                    simulator_id=sim.id,
                    body=UpdateStatusRequest(status=Status("env_in_progress")),
                    x_api_key=api_key,
                )
                sim = await get_simulator_by_name.asyncio(client=client, name=name, x_api_key=api_key)

            rec = _record(sim, created)
            if json_output:
                print(json.dumps(rec))
            else:
                verb = "created" if created else "updated"
                console.print(f"[green]✅ {name}: {verb} (id={rec['id']}, {rec['status']})[/green]")
            return True

    if not handle_async(_run()):
        raise typer.Exit(1)


@pm_app.command(name="set-status")
def set_status(
    simulators: list[str] = typer.Argument(..., help="Simulator name(s)"),
    status: str = typer.Option(..., "--status", "-s", help="Target status to set"),
):
    """Force-set the status of one or more simulators.

    Useful for unsticking simulators in a bad state (e.g. env_in_progress → env_review_requested).

    Examples:
        plato pm set-status espocrm -s env_review_requested
        plato pm set-status espocrm memos -s data_in_progress
    """
    api_key = require_api_key()
    base_url = _get_base_url()

    async def _run():
        async with httpx.AsyncClient(base_url=base_url, timeout=30.0) as client:
            for sim_name in simulators:
                try:
                    sim = await get_simulator_by_name.asyncio(client=client, name=sim_name, x_api_key=api_key)
                    if not sim:
                        console.print(f"[red]❌ {sim_name}: not found[/red]")
                        continue
                    await update_simulator_status.asyncio(
                        client=client,
                        simulator_id=sim.id,
                        x_api_key=api_key,
                        body=UpdateStatusRequest(status=Status(status)),
                    )
                    console.print(f"[green]✅ {sim_name}:[/green] → {status}")
                except Exception as e:
                    console.print(f"[red]❌ {sim_name}: {e}[/red]")

    handle_async(_run())


@pm_app.command(name="update-base")
def update_base(
    simulator: str = typer.Argument(..., help="Simulator name"),
    artifact_id: str = typer.Argument(..., help="Artifact UUID to set as base_artifact_id"),
):
    """Set a simulator's base_artifact_id to the given artifact UUID.

    Useful for manually promoting a snapshot when the blank pipeline's
    auto-promotion failed, or for populating an empty base slot.

    Example:
        plato pm update-base espocrm 56f85a14-8e82-4053-a7df-8490c31a14e3
    """
    api_key = require_api_key()
    base_url = _get_base_url()

    async def _run():
        async with httpx.AsyncClient(base_url=base_url, timeout=30.0) as client:
            sim = await get_simulator_by_name.asyncio(client=client, name=simulator, x_api_key=api_key)
            if not sim:
                console.print(f"[red]❌ {simulator}: not found[/red]")
                return
            try:
                await update_simulator.asyncio(
                    client=client,
                    simulator_id=sim.id,
                    x_api_key=api_key,
                    body=AppApiV1SimulatorRoutesUpdateSimulatorRequest(base_artifact_id=artifact_id),
                )
                console.print(f"[green]✅ {simulator}:[/green] base_artifact_id → {artifact_id}")
            except Exception as e:
                console.print(f"[red]❌ {simulator}: {e}[/red]")

    handle_async(_run())


@pm_app.command(name="reject")
def reject(
    simulator: str = typer.Argument(
        ...,
        help="Simulator name. Supports colon notation: sim:<artifact-uuid>",
    ),
    message: str = typer.Option(
        ...,
        "--message",
        "-m",
        help="Reject message — required. Saved as a sim_comment on the review record.",
    ),
    artifact: str = typer.Option(
        None,
        "--artifact",
        "-a",
        help="Artifact UUID to reject. If not provided, uses server's data_artifact_id.",
    ),
):
    """Reject a sim without opening the browser.

    Posts a reject review record with your message, walks status back using
    DATA_REVIEWER-allowed transitions, and prompts for reject level (data vs env)
    + a follow-up world action (none / fresh / resume / fix).

    Works from any DATA_REVIEWER-walkable starting status (data_review_requested,
    ready, data_in_progress, mid-env-walk states). For stuck sims, use
    `plato pm set-status` instead.

    Examples:
        plato pm reject activepieces -m "login timeouts"
        plato pm reject fathom:<uuid> -m "missing entries in X section"
        plato pm reject boltcms -m "env needs fixing" -a <uuid>
    """
    api_key = require_api_key()

    simulator_name, artifact_id = parse_simulator_artifact(
        simulator, artifact, require_artifact=False, command_name="reject"
    )
    assert simulator_name is not None, "simulator_name must be set"

    msg = message.strip()
    if not msg:
        console.print("[red]❌ --message must be non-empty[/red]")
        raise typer.Exit(1)

    console.print(f"[cyan]Simulator:[/cyan] {simulator_name}")

    handle_async(
        _submit_reject_no_browser(
            simulator_name=simulator_name,
            artifact_id_arg=artifact_id,
            message=msg,
            api_key=api_key,
        )
    )


@pm_app.command(name="archive")
def archive(
    simulators: list[str] = typer.Argument(..., help="Simulator name(s)"),
    note: str = typer.Option(..., "--note", "-n", help="Reason for archiving (required)"),
):
    """Move simulators to out_of_service and append a note.

    Works from any status.

    Examples:
        plato pm archive glpi shelf -n "no docker compose, proxy only"
    """
    api_key = require_api_key()

    async def _archive():
        base_url = _get_base_url()

        to_archive = []
        for sim_name in simulators:
            try:
                async with httpx.AsyncClient(base_url=base_url, timeout=60.0) as client:
                    sim = await get_simulator_by_name.asyncio(
                        client=client,
                        name=sim_name,
                        x_api_key=api_key,
                    )
                current_config = sim_config_dict(sim.config)
                status = current_config.get("status", "not_started")
                existing_notes = current_config.get("notes", "") or ""
                to_archive.append(
                    {
                        "name": sim_name,
                        "id": sim.id,
                        "status": status,
                        "existing_notes": existing_notes,
                    }
                )
            except Exception as e:
                console.print(f"[red]❌ {sim_name}: {e}[/red]")

        if not to_archive:
            console.print("[yellow]Nothing to archive.[/yellow]")
            return

        console.print(f"\n[bold]Will archive {len(to_archive)} simulator(s) → out_of_service:[/bold]")
        for s in to_archive:
            console.print(f"  {s['name']} ({s['status']})")
        console.print(f"[bold]Note:[/bold] {note}")

        if not typer.confirm("\nProceed?", default=True):
            console.print("[yellow]Cancelled.[/yellow]")
            return

        for s in to_archive:
            try:
                async with httpx.AsyncClient(base_url=base_url, timeout=60.0) as client:
                    # Append note to existing notes
                    new_notes = f"{s['existing_notes']} | {note}".strip(" |") if s["existing_notes"] else note
                    await update_simulator.asyncio(
                        client=client,
                        simulator_id=s["id"],
                        body=AppApiV1SimulatorRoutesUpdateSimulatorRequest(notes=new_notes),
                        x_api_key=api_key,
                    )

                    await update_simulator_status.asyncio(
                        client=client,
                        simulator_id=s["id"],
                        body=UpdateStatusRequest(status=Status("out_of_service")),
                        x_api_key=api_key,
                    )
                console.print(f"[green]✅ {s['name']}:[/green] {s['status']} → out_of_service")
            except Exception as e:
                console.print(f"[red]❌ {s['name']}: {e}[/red]")

    handle_async(_archive())


# =============================================================================
# REVIEW COMMANDS
# =============================================================================


@review_app.command(name="env")
def review_env(
    simulator: str = typer.Argument(
        None,
        help="Simulator name. Supports colon notation: sim:<artifact-uuid>",
    ),
    artifact: str = typer.Option(
        None,
        "--artifact",
        "-a",
        help="Artifact UUID to review. If not provided, uses server's base_artifact_id.",
    ),
    skip_review: bool = typer.Option(
        False,
        "--skip-review",
        help="Run login flow and check state, but skip interactive review. For automated verification.",
    ),
    local: str = typer.Option(
        None,
        "--local",
        "-l",
        help="Path to a local flow YAML file to run instead of the default login flow.",
    ),
    clock: str = typer.Option(
        None,
        "--clock",
        help="Set fake browser time (ISO format or offset like '-30d' for 30 days ago).",
    ),
    next_sim: bool = typer.Option(
        False,
        "--next",
        "-n",
        help="Auto-pick the last simulator from 'plato pm list env' (pending env review).",
    ),
):
    """Review environment artifact for a simulator.

    Creates an environment from the artifact, launches a browser for testing,
    runs the login flow, and checks for database mutations. After testing,
    choose pass (→ env_approved) or reject (→ env_in_progress).

    Requires simulator status: env_review_requested

    Options:
        -s, --simulator: Simulator name. Supports colon notation for artifact:
            '-s sim' (uses server's base_artifact_id) or '-s sim:<uuid>'
        -a, --artifact: Explicit artifact UUID to review. Overrides server's value.
        --skip-review: Run automated checks without interactive review session.
        -n, --next: Auto-pick the last simulator pending env review.
    """
    api_key = require_api_key()

    if next_sim:
        # Fetch the last simulator from the env_review_requested list
        async def _pick_next():
            base_url = _get_base_url()
            async with httpx.AsyncClient(base_url=base_url, timeout=60.0) as client:
                sims = await get_simulators.asyncio(client=client, x_api_key=api_key)
                matched = []
                for s in sims:
                    config = s.get("config", {}) if isinstance(s, dict) else getattr(s, "config", {})
                    if not isinstance(config, dict):
                        continue
                    if config.get("status") == "env_review_requested":
                        name = (s.get("name") or "") if isinstance(s, dict) else (getattr(s, "name", None) or "")
                        matched.append(name)
                if not matched:
                    console.print("[red]❌ No simulators pending env review[/red]")
                    raise typer.Exit(1)
                matched.sort()
                return matched[-1]

        picked = handle_async(_pick_next())
        console.print(f"[cyan]▶ Auto-selected:[/cyan] {picked}")
        simulator = picked

    # Parse simulator and artifact from args (artifact not required - falls back to server config)
    simulator_name, artifact_id_input = parse_simulator_artifact(
        simulator, artifact, require_artifact=False, command_name="review env"
    )

    async def _review_env():
        import warnings

        base_url = _get_base_url()
        # v1 SDK expects base_url to include /api suffix
        v1_base_url = f"{base_url}/api"
        # Suppress the deprecation warning from v1 Plato
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            plato = Plato(api_key=api_key, base_url=v1_base_url)
        env = None
        playwright = None
        browser = None

        try:
            # simulator_name is guaranteed set by parse_simulator_artifact (or we exit)
            assert simulator_name is not None, "simulator_name must be set"

            # Get simulator by name using httpx for API calls
            async with httpx.AsyncClient(base_url=base_url, timeout=60.0) as http_client:
                sim = await get_simulator_by_name.asyncio(
                    client=http_client,
                    name=simulator_name,
                    x_api_key=api_key,
                )
            simulator_id = sim.id
            current_config = sim_config_dict(sim.config)
            current_status = current_config.get("status", "not_started")

            console.print(f"[cyan]Current status:[/cyan] {current_status}")

            # Use provided artifact ID or fall back to base_artifact_id from server config
            artifact_id: str | None = artifact_id_input if artifact_id_input else current_config.get("base_artifact_id")
            if not artifact_id:
                console.print("[red]❌ No artifact ID provided.[/red]")
                console.print(
                    "[yellow]This simulator hasn't been submitted yet, so there's no base artifact on record.[/yellow]"
                )
                console.print(
                    "[yellow]Specify the artifact ID from your snapshot using: plato pm review env --artifact <artifact_id>[/yellow]"
                )
                raise typer.Exit(1)

            console.print(f"[cyan]Using artifact:[/cyan] {artifact_id}")

            # Try to create environment from artifact using v1 API
            try:
                console.print(f"[cyan]Creating {simulator_name} environment with artifact {artifact_id}...[/cyan]")
                env = await plato.make_environment(
                    env_id=simulator_name,
                    artifact_id=artifact_id,
                )
                console.print(f"[green]✅ Environment created: {env.id}[/green]")

                # Wait for environment to be ready
                console.print("[cyan]Waiting for environment to be ready...[/cyan]")
                await env.wait_for_ready(timeout=300)
                console.print("[green]✅ Environment ready![/green]")

                # Reset
                console.print("[cyan]Resetting environment...[/cyan]")
                await env.reset()
                console.print("[green]✅ Environment reset complete![/green]")

                # Get public URL (v1 returns string directly)
                public_url = await env.get_public_url()
                console.print(f"[cyan]Public URL:[/cyan] {public_url}")

                # Launch Playwright browser and login
                console.print("[cyan]Launching browser and logging in...[/cyan]")
                from playwright.async_api import async_playwright

                # Clear existing browser data for a fresh session
                user_data_dir = Path.home() / ".plato" / "chrome-data-base"
                if user_data_dir.exists():
                    shutil.rmtree(user_data_dir, ignore_errors=True)
                user_data_dir.mkdir(parents=True, exist_ok=True)

                playwright = await async_playwright().start()
                browser = await playwright.chromium.launch_persistent_context(
                    str(user_data_dir),
                    headless=False,
                )

                # Install fake clock if requested
                fake_time: datetime | None = None
                if clock:
                    # Parse clock option: ISO format or offset like '-30d'
                    if clock.startswith("-") and clock[-1] in "dhms":
                        # Offset format: -30d, -1h, -30m, -60s
                        unit = clock[-1]
                        amount = int(clock[1:-1])
                        if unit == "d":
                            fake_time = datetime.now() - timedelta(days=amount)
                        elif unit == "h":
                            fake_time = datetime.now() - timedelta(hours=amount)
                        elif unit == "m":
                            fake_time = datetime.now() - timedelta(minutes=amount)
                        elif unit == "s":
                            fake_time = datetime.now() - timedelta(seconds=amount)
                        else:
                            raise ValueError(f"Invalid clock offset unit: {unit}")
                    else:
                        # ISO format
                        fake_time = datetime.fromisoformat(clock)

                    assert fake_time is not None, f"Failed to parse clock value: {clock}"
                    console.print(f"[cyan]Setting fake browser time to:[/cyan] {fake_time.isoformat()}")

                if local:
                    # Use local flow file instead of default login
                    local_path = Path(local)
                    if not local_path.exists():
                        console.print(f"[red]❌ Local flow file not found: {local}[/red]")
                        raise typer.Exit(1)

                    console.print(f"[cyan]Loading local flow from: {local}[/cyan]")
                    with open(local_path) as f:
                        flow_dict = yaml.safe_load(f)

                    # Find login flow (or first flow if only one)
                    flows = flow_dict.get("flows", [])
                    if not flows:
                        console.print("[red]❌ No flows found in flow file[/red]")
                        raise typer.Exit(1)

                    # Try to find 'login' flow, otherwise use first flow
                    flow_data = next((f for f in flows if f.get("name") == "login"), flows[0])
                    flow = Flow.model_validate(flow_data)
                    console.print(f"[cyan]Running flow: {flow.name}[/cyan]")

                    # Create page and navigate to public URL
                    page = await browser.new_page()

                    # Install fake clock if requested
                    if fake_time:
                        await page.clock.install(time=fake_time)
                        console.print(f"[green]✅ Fake clock installed: {fake_time.isoformat()}[/green]")

                    if public_url:
                        await page.goto(public_url)

                    # Execute the flow
                    try:
                        executor = FlowExecutor(page, flow)
                        await executor.execute_flow()
                        console.print("[green]✅ Local flow executed successfully[/green]")
                    except Exception as e:
                        console.print(f"[yellow]⚠️  Flow execution error: {e}[/yellow]")
                else:
                    # Use default login via env.login() (v1 API takes Page, not Browser)
                    if fake_time:
                        console.print("[yellow]⚠️  --clock with default login may not work correctly.[/yellow]")
                        console.print("[yellow]   Use --local with a flow file for reliable clock testing.[/yellow]")
                    page = None
                    try:
                        # Create page and navigate to public URL first
                        page = await browser.new_page()
                        if fake_time:
                            await page.clock.install(time=fake_time)
                            console.print(f"[green]✅ Fake clock installed: {fake_time.isoformat()}[/green]")
                        if public_url:
                            await page.goto(public_url)
                        # v1 login takes a Page and uses from_api=True to fetch flows from server
                        await env.login(page, dataset="base", from_api=True)
                        console.print("[green]✅ Logged into environment[/green]")
                    except Exception as e:
                        console.print(f"[yellow]⚠️  Login error: {e}[/yellow]")
                        # Page already created above, just navigate if not already done
                        if public_url and page:
                            try:
                                await page.goto(public_url)
                            except Exception:
                                pass

                # ALWAYS check state after login to verify no mutations
                console.print("\n[cyan]Checking environment state after login...[/cyan]")
                has_mutations = False
                has_errors = False
                try:
                    # v1 API: env.get_state() returns state dict directly
                    state_data = await env.get_state(merge_mutations=True)
                    console.print(f"\n[bold cyan]Environment {env.id}:[/bold cyan]")

                    if isinstance(state_data, dict):
                        # Check for error in state response (only if error has a truthy value)
                        if state_data.get("error"):
                            has_errors = True
                            console.print("\n[bold red]❌ State API Error:[/bold red]")
                            console.print(f"[red]{state_data['error']}[/red]")
                        else:
                            mutations = state_data.pop("mutations", [])
                            console.print("\n[bold]State:[/bold]")
                            safe_print(json.dumps(state_data, indent=2, default=str))
                            if mutations:
                                has_mutations = True
                                console.print(f"\n[bold red]Mutations ({len(mutations)}):[/bold red]")
                                safe_print(json.dumps(mutations, indent=2, default=str))
                            else:
                                console.print("\n[green]No mutations recorded[/green]")
                    else:
                        console.print(f"[yellow]Unexpected state format: {type(state_data)}[/yellow]")

                    if has_errors:
                        console.print("\n[bold red]❌ State check failed due to errors![/bold red]")
                        console.print("[yellow]The worker may not be properly connected.[/yellow]")
                    elif has_mutations:
                        console.print("\n[bold red]⚠️  WARNING: Login flow created mutations![/bold red]")
                        console.print("[yellow]The login flow should NOT modify database state.[/yellow]")
                    else:
                        console.print("\n[bold green]✅ Login flow verified - no mutations created[/bold green]")
                except Exception as e:
                    console.print(f"[red]❌ Error getting state: {e}[/red]")

                # If skip_review, exit without interactive loop
                if skip_review:
                    console.print("\n[cyan]Skipping interactive review (--skip-review)[/cyan]")
                    return

                console.print("\n" + "=" * 60)
                console.print("[bold green]Environment Review Session Active[/bold green]")
                console.print("=" * 60)
                console.print("[bold]Commands:[/bold]")
                console.print("  - 'state' or 's': Show environment state and mutations")
                console.print("  - 'finish' or 'f': Exit loop and submit review outcome")
                console.print("=" * 60)

                # Show recent env review if available
                reviews = current_config.get("reviews") or []
                env_reviews = [r for r in reviews if r.get("review_type") == "env"]
                if env_reviews:
                    env_reviews.sort(key=lambda r: r.get("timestamp_iso", ""), reverse=True)
                    recent_review = env_reviews[0]
                    outcome = recent_review.get("outcome", "unknown")
                    timestamp = recent_review.get("timestamp_iso", "")[:10]
                    console.print()
                    if outcome == "reject":
                        console.print(f"[bold red]📋 Most Recent Base Review: REJECTED[/bold red] ({timestamp})")
                    else:
                        console.print(f"[bold green]📋 Most Recent Base Review: PASSED[/bold green] ({timestamp})")
                    comment_texts = _extract_review_comment_texts(recent_review)
                    for comment_text in comment_texts:
                        console.print(f"[yellow]Reviewer Comments:[/yellow] {comment_text}")

                console.print()

                # Interactive loop
                while True:
                    try:
                        command = input("Enter command: ").strip().lower()

                        if command in ["finish", "f"]:
                            console.print("\n[yellow]Finishing review...[/yellow]")
                            break
                        elif command in ["state", "s"]:
                            console.print("\n[cyan]Getting environment state with mutations...[/cyan]")
                            try:
                                # v1 API: env.get_state() returns state dict directly
                                state_data = await env.get_state(merge_mutations=True)
                                console.print(f"\n[bold cyan]Environment {env.id}:[/bold cyan]")

                                if isinstance(state_data, dict):
                                    # Check for error in state response (only if error has a truthy value)
                                    if state_data.get("error"):
                                        console.print("\n[bold red]❌ State API Error:[/bold red]")
                                        console.print(f"[red]{state_data['error']}[/red]")
                                    else:
                                        mutations = state_data.pop("mutations", [])
                                        console.print("\n[bold]State:[/bold]")
                                        safe_print(json.dumps(state_data, indent=2, default=str))
                                        if mutations:
                                            console.print(f"\n[bold]Mutations ({len(mutations)}):[/bold]")
                                            safe_print(json.dumps(mutations, indent=2, default=str))
                                        else:
                                            console.print("\n[yellow]No mutations recorded[/yellow]")
                                else:
                                    safe_print(json.dumps(state_data, indent=2, default=str))
                                console.print()
                            except Exception as e:
                                console.print(f"[red]❌ Error getting state: {e}[/red]")
                        else:
                            console.print("[yellow]Unknown command. Use 'state' or 'finish'[/yellow]")

                    except KeyboardInterrupt:
                        console.print("\n[yellow]Interrupted! Finishing review...[/yellow]")
                        break

            except Exception as env_error:
                console.print(f"[yellow]⚠️  Environment creation failed: {env_error}[/yellow]")
                console.print("[yellow]You can still submit a review without testing the environment.[/yellow]")

            # Prompt for outcome
            console.print("\n[bold]Choose outcome:[/bold]")
            console.print("  1. pass")
            console.print("  2. reject")
            console.print("  3. skip (no status update)")
            outcome_choice = typer.prompt("Choice [1/2/3]").strip()

            if outcome_choice == "1":
                outcome = "pass"
            elif outcome_choice == "2":
                outcome = "reject"
            elif outcome_choice == "3":
                console.print("[yellow]Review session ended without status update[/yellow]")
                return
            else:
                console.print("[red]❌ Invalid choice. Aborting.[/red]")
                raise typer.Exit(1)

            # Validate status BEFORE submitting outcome
            if outcome == "pass":
                if current_status == "data_in_progress":
                    # Already approved and datagen was attempted — allow re-launching
                    console.print(
                        "[yellow]⚠️  Status is already data_in_progress (prior datagen may have failed).[/yellow]"
                    )
                    new_status = "data_in_progress"
                else:
                    validate_status_transition(current_status, "env_review_requested", "review env pass")
                    new_status = "env_approved"
            else:
                validate_status_transition(current_status, "env_review_requested", "review env reject")
                new_status = "env_in_progress"

            # Collect all inputs BEFORE submitting anything
            # (so Ctrl+C at any prompt means nothing gets submitted)
            reject_comments: str = ""
            clear_assignees = False
            reject_action = None
            reject_action_inputs = {}
            pass_start_datagen = False

            if outcome == "pass":
                if typer.confirm("Auto-start datagen?", default=True):
                    pass_start_datagen = True

            elif outcome == "reject":
                comments = ""
                while not comments:
                    comments = typer.prompt("Comments (required for reject)").strip()
                    if not comments:
                        console.print("[yellow]Comments are required when rejecting. Please provide feedback.[/yellow]")
                reject_comments = comments

                # Clear env assignees option — re-fetch to avoid stale data
                try:
                    async with httpx.AsyncClient(base_url=base_url, timeout=60.0) as http_client:
                        fresh_sim = await get_simulator_by_name.asyncio(
                            client=http_client,
                            name=simulator_name,
                            x_api_key=api_key,
                        )
                    existing_assignees = sim_config_dict(fresh_sim.config).get("env_assignees") or []
                except Exception:
                    existing_assignees = current_config.get("env_assignees") or []
                if existing_assignees:
                    console.print(f"[cyan]Current env assignees:[/cyan] {existing_assignees}")
                    clear_assignees = typer.confirm("Clear env assignees?", default=False)

                # Optionally launch a world
                github_url_from_config = current_config.get("source_code_url", "")
                base_artifact = current_config.get("base_artifact_id", "")
                console.print("\n[bold]Launch a world?[/bold]")
                console.print("  1. none")
                if github_url_from_config:
                    console.print(f"  2. fresh (create from scratch — {github_url_from_config})")
                else:
                    console.print("  2. fresh (create from scratch — no GitHub URL in config)")
                console.print("  3. resume (continue create pipeline from last session)")
                if base_artifact:
                    console.print(f"  4. fix (fix pipeline — artifact {base_artifact[:8]}... + review feedback)")
                else:
                    console.print("  4. fix (fix pipeline — [red]no base_artifact_id[/red])")
                action_choice = typer.prompt("Choice [1/2/3/4]", default="1").strip()

                if action_choice == "2":
                    reject_action = "fresh"
                    # Pre-collect GitHub URL (auto-default from sim config)
                    github_url = typer.prompt("GitHub URL", default=github_url_from_config).strip()
                    if github_url:
                        reject_action_inputs["github_url"] = github_url
                    else:
                        console.print("[yellow]No GitHub URL provided, skipping launch.[/yellow]")
                        reject_action = None
                elif action_choice == "3":
                    reject_action = "resume"
                    # Look up last simcreator session for this sim
                    last_session = _get_last_chronos_session(tags=["simcreator", simulator_name], api_key=api_key)
                    default_resume = ""
                    if last_session:
                        sid = last_session["public_id"]
                        status = last_session.get("status", "?")
                        created = last_session.get("created_at", "")[:16].replace("T", " ")
                        console.print(f"[cyan]Last simcreator session:[/cyan] {sid} ({status}, {created})")
                        default_resume = sid
                    resume_from = typer.prompt(
                        "Resume session (enter for above, 'none' for fresh)", default=default_resume
                    ).strip()
                    if resume_from.lower() == "none":
                        resume_from = ""
                    reject_action_inputs["resume_from"] = resume_from
                elif action_choice == "4":
                    reject_action = "fix"

            # --- All inputs collected. Confirm before submitting. ---

            console.print("\n[bold]Review summary:[/bold]")
            console.print(f"  Outcome: {outcome}")
            if reject_comments:
                console.print(f"  Comments: {reject_comments}")
            if reject_action:
                console.print(f"  Env assignees: → {DEFAULT_DATA_ASSIGNEES}")
            elif clear_assignees:
                console.print("  Clear env assignees: yes")
            if reject_action:
                action_desc = reject_action
                if reject_action == "fresh":
                    action_desc += f" ({reject_action_inputs.get('github_url', '')})"
                elif reject_action in ("resume"):
                    rs = reject_action_inputs.get("resume_from", "")
                    action_desc += f" ({rs[:12]}...)" if rs else " (fresh state)"
                console.print(f"  World: {action_desc}")
            if pass_start_datagen:
                console.print("  Datagen: fresh")

            if not typer.confirm("Submit?", default=True):
                console.print("[yellow]Cancelled — nothing submitted.[/yellow]")
                return

            async with httpx.AsyncClient(base_url=base_url, timeout=60.0) as api_client:
                # Update status (skip if already at target status, e.g. re-launching datagen)
                if current_status != new_status:
                    await update_simulator_status.asyncio(
                        client=api_client,
                        simulator_id=simulator_id,
                        body=UpdateStatusRequest(status=Status(new_status)),
                        x_api_key=api_key,
                    )

                if outcome == "reject":
                    # 1. Submit review
                    await add_simulator_review.asyncio(
                        client=api_client,
                        simulator_id=simulator_id,
                        body=AddReviewRequest(
                            review_type=ReviewType.env,
                            outcome=Outcome.reject,
                            artifact_id=artifact_id,
                            sim_comments=[SimReviewComment(comment=reject_comments)],
                        ),
                        x_api_key=api_key,
                    )

                    # 2. Update env assignees
                    if reject_action:
                        # When launching a world, assign env to DEFAULT_DATA_ASSIGNEES (matches extension behavior)
                        try:
                            await update_simulator.asyncio(
                                client=api_client,
                                simulator_id=simulator_id,
                                body=AppApiV1SimulatorRoutesUpdateSimulatorRequest(
                                    env_assignees=DEFAULT_DATA_ASSIGNEES,
                                ),
                                x_api_key=api_key,
                            )
                            console.print(f"[green]✅ Set env_assignees → {DEFAULT_DATA_ASSIGNEES}[/green]")
                        except Exception as e:
                            console.print(f"[yellow]⚠️  Could not set env assignees: {e}[/yellow]")
                    elif clear_assignees:
                        try:
                            await update_simulator.asyncio(
                                client=api_client,
                                simulator_id=simulator_id,
                                body=AppApiV1SimulatorRoutesUpdateSimulatorRequest(
                                    env_assignees=[],
                                ),
                                x_api_key=api_key,
                            )
                            console.print("[green]✅ Cleared env assignees[/green]")
                        except Exception as e:
                            console.print(f"[yellow]⚠️  Could not clear assignees: {e}[/yellow]")

                    # 3. Launch world if requested
                    if reject_action:
                        launched_session = await _launch_env_world(
                            action=reject_action,
                            simulator_name=simulator_name,
                            artifact_id=artifact_id,
                            feedback=reject_comments,
                            api_key=api_key,
                            current_config=current_config,
                            action_inputs=reject_action_inputs,
                        )
                        if launched_session:
                            console.print(f"[green]✅ World launched: {launched_session}[/green]")
                            console.print(f"[cyan]View:[/cyan] https://chronos.plato.so/sessions/{launched_session}")

                console.print(f"\n[green]✅ Review submitted: {outcome}[/green]")
                console.print(f"[cyan]Status:[/cyan] {current_status} → {new_status}")

                # prod-latest is synced backend-side on the transition to
                # `ready` (POST /api/v1/simulator/{id}/status), so the client
                # no longer moves the tag here.

                # If passed + auto-start datagen
                if outcome == "pass" and pass_start_datagen and artifact_id:
                    # Ensure assignees are set
                    try:
                        async with httpx.AsyncClient(base_url=base_url, timeout=60.0) as http_client:
                            fresh_sim = await get_simulator_by_name.asyncio(
                                client=http_client,
                                name=simulator_name,
                                x_api_key=api_key,
                            )
                        fresh_config = sim_config_dict(fresh_sim.config)
                        updates = {}
                        if not fresh_config.get("data_assignees"):
                            updates["data_assignees"] = DEFAULT_DATA_ASSIGNEES
                            console.print(f"[cyan]Setting data_assignees → {DEFAULT_DATA_ASSIGNEES}[/cyan]")
                        if not fresh_config.get("data_review_assignees"):
                            updates["data_review_assignees"] = DEFAULT_DATA_REVIEW_ASSIGNEES
                            console.print(
                                f"[cyan]Setting data_review_assignees → {DEFAULT_DATA_REVIEW_ASSIGNEES}[/cyan]"
                            )
                        if updates:
                            await update_simulator.asyncio(
                                client=api_client,
                                simulator_id=simulator_id,
                                body=AppApiV1SimulatorRoutesUpdateSimulatorRequest(**updates),
                                x_api_key=api_key,
                            )
                    except Exception as e:
                        console.print(f"[yellow]⚠️  Could not set assignees: {e}[/yellow]")

                    # Move to data_in_progress (skip if already there from a prior attempt)
                    if new_status != "data_in_progress":
                        await update_simulator_status.asyncio(
                            client=api_client,
                            simulator_id=simulator_id,
                            body=UpdateStatusRequest(status=Status("data_in_progress")),
                            x_api_key=api_key,
                        )
                        console.print(f"[cyan]Status:[/cyan] {new_status} → data_in_progress")
                    else:
                        console.print("[cyan]Status already data_in_progress, re-launching datagen[/cyan]")

                    # Launch datagen
                    launched_session = await _launch_datagen_world(
                        simulator_name=simulator_name,
                        artifact_id=artifact_id,
                        api_key=api_key,
                    )
                    if launched_session:
                        console.print(f"[green]✅ Datagen launched: {launched_session}[/green]")
                        console.print(f"[cyan]View:[/cyan] https://chronos.plato.so/sessions/{launched_session}")

        except typer.Exit:
            raise
        except Exception as e:
            console.print(f"[red]❌ Error during review session: {e}[/red]")
            raise

        finally:
            # Cleanup
            try:
                if browser:
                    await browser.close()
                if playwright:
                    await playwright.stop()
            except Exception as e:
                console.print(f"[yellow]⚠️  Browser cleanup error: {e}[/yellow]")

            if env:
                try:
                    console.print("[cyan]Shutting down environment...[/cyan]")
                    await env.close()
                    console.print("[green]✅ Environment shut down[/green]")
                except Exception as e:
                    console.print(f"[yellow]⚠️  Environment cleanup error: {e}[/yellow]")

            try:
                await plato.close()
            except Exception as e:
                console.print(f"[yellow]⚠️  Client cleanup error: {e}[/yellow]")

    handle_async(_review_env())


@review_app.command(name="data")
def review_data(
    simulator: str = typer.Argument(
        None,
        help="Simulator name. Supports colon notation: sim:<artifact-uuid>",
    ),
    artifact: str = typer.Option(
        None,
        "--artifact",
        "-a",
        help="Artifact UUID to review. If not provided, uses server's data_artifact_id.",
    ),
    next_sim: bool = typer.Option(
        False,
        "--next",
        "-n",
        help="Auto-pick the last simulator pending data review.",
    ),
):
    """
    Launch browser with Data Review extension for data review.

    Opens Chrome with the Data Review extension installed for reviewing
    data artifacts. Close the browser when done.

    SPECIFYING SIMULATOR AND ARTIFACT:

        -s <simulator>                      Use server's data_artifact_id
        -s <simulator> -a <artifact-uuid>   Explicit artifact
        -s <simulator>:<artifact-uuid>      Colon notation (same as above)

    EXAMPLES:

        plato pm review data -s fathom
        plato pm review data -s fathom -a e9c25ca5-1234-5678-9abc-def012345678
        plato pm review data -s fathom:e9c25ca5-1234-5678-9abc-def012345678

    Requires simulator status: data_review_requested
        -n, --next: Auto-pick the last simulator pending data review.

    To reject without opening the browser, use: plato pm reject <sim> -m "<message>"
    """
    api_key = require_api_key()

    if next_sim:

        async def _pick_next():
            base_url = _get_base_url()
            async with httpx.AsyncClient(base_url=base_url, timeout=60.0) as client:
                sims = await get_simulators.asyncio(client=client, x_api_key=api_key)
                matched = []
                for s in sims:
                    config = s.get("config", {}) if isinstance(s, dict) else getattr(s, "config", {})
                    if not isinstance(config, dict):
                        continue
                    if config.get("status") == "data_review_requested":
                        name = (s.get("name") or "") if isinstance(s, dict) else (getattr(s, "name", None) or "")
                        matched.append(name)
                if not matched:
                    console.print("[red]❌ No simulators pending data review[/red]")
                    raise typer.Exit(1)
                matched.sort()
                return matched[-1]

        picked = handle_async(_pick_next())
        console.print(f"[cyan]▶ Auto-selected:[/cyan] {picked}")
        simulator = picked

    # Parse simulator and artifact from args (artifact not required - falls back to server config)
    simulator_name, artifact_id = parse_simulator_artifact(
        simulator, artifact, require_artifact=False, command_name="review data"
    )

    console.print(f"[cyan]Simulator:[/cyan] {simulator_name}")

    # Fetch simulator config and get artifact ID if not provided
    data_reviews = []

    async def _fetch_artifact_info():
        nonlocal artifact_id
        # simulator_name is guaranteed set by parse_simulator_artifact (or we exit)
        assert simulator_name is not None, "simulator_name must be set"

        base_url = _get_base_url()
        async with httpx.AsyncClient(base_url=base_url, timeout=60.0) as client:
            try:
                sim = await get_simulator_by_name.asyncio(
                    client=client,
                    name=simulator_name,
                    x_api_key=api_key,
                )
                config = sim_config_dict(sim.config)

                # If no artifact provided, try to get data_artifact_id from server
                if not artifact_id:
                    artifact_id = config.get("data_artifact_id")
                    if artifact_id:
                        console.print(f"[cyan]Using data_artifact_id from server:[/cyan] {artifact_id}")
                    else:
                        console.print("[yellow]No artifact specified and no data_artifact_id on server[/yellow]")

                # Find all data reviews, sorted by most recent first
                reviews = config.get("reviews") or []
                found_reviews = [r for r in reviews if r.get("review_type") == "data"]
                if found_reviews:
                    found_reviews.sort(key=lambda r: r.get("timestamp_iso", ""), reverse=True)
                    return found_reviews
            except Exception as e:
                console.print(f"[yellow]⚠️  Could not fetch simulator info: {e}[/yellow]")
            return []

    data_reviews = handle_async(_fetch_artifact_info())

    if artifact_id:
        console.print(f"[cyan]Artifact:[/cyan] {artifact_id}")

    # Find Chrome extension source
    package_dir = Path(__file__).resolve().parent.parent  # plato/
    is_installed = "site-packages" in str(package_dir)

    if is_installed:
        extension_source_path = package_dir / "extensions" / "data-review"
    else:
        repo_root = package_dir.parent.parent  # plato-client/
        extension_source_path = repo_root / "extensions" / "data-review"

    # Fallback to env var
    if not extension_source_path.exists():
        plato_client_dir_env = os.getenv("PLATO_CLIENT_DIR")
        if plato_client_dir_env:
            env_path = Path(plato_client_dir_env) / "extensions" / "data-review"
            if env_path.exists():
                extension_source_path = env_path

    if not extension_source_path.exists():
        console.print("[red]❌ Data Review extension not found[/red]")
        console.print(f"\n[yellow]Expected location:[/yellow] {extension_source_path}")
        raise typer.Exit(1)

    # Copy extension to temp directory
    temp_ext_dir = Path(tempfile.mkdtemp(prefix="plato-extension-"))
    extension_path = temp_ext_dir / "data-review"

    console.print("[cyan]Copying extension to temp directory...[/cyan]")
    shutil.copytree(extension_source_path, extension_path, dirs_exist_ok=False)
    console.print(f"[green]✅ Extension copied to: {extension_path}[/green]")

    async def _review_data():
        import warnings

        base_url = _get_base_url()
        # v1 SDK expects base_url to include /api suffix
        v1_base_url = f"{base_url}/api"
        # Suppress the deprecation warning from v1 Plato
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            plato = Plato(api_key=api_key, base_url=v1_base_url)
        env = None
        playwright = None
        browser = None

        try:
            # Check if we have an artifact ID to create a session
            if not artifact_id:
                console.print("[red]❌ No artifact ID available. Cannot create session.[/red]")
                console.print("[yellow]Specify artifact with: plato pm review data -s simulator:artifact_id[/yellow]")
                raise typer.Exit(1)

            # Create environment with artifact using v1 API
            assert simulator_name is not None, "simulator_name must be set"
            console.print(f"[cyan]Creating {simulator_name} environment with artifact {artifact_id}...[/cyan]")
            env = await plato.make_environment(
                env_id=simulator_name,
                artifact_id=artifact_id,
            )
            console.print(f"[green]✅ Session created: {env.id}[/green]")

            # Wait for environment to be ready (non-fatal — browser should still open)
            console.print("[cyan]Waiting for environment to be ready...[/cyan]")
            try:
                await env.wait_for_ready(timeout=300)
                console.print("[green]✅ Environment ready![/green]")
            except Exception as e:
                console.print(f"[yellow]⚠️  Wait for ready failed: {e}[/yellow]")
                console.print("[yellow]   Continuing anyway...[/yellow]")

            # Reset environment (non-fatal — browser should still open)
            console.print("[cyan]Resetting environment...[/cyan]")
            reset_error = None
            try:
                await env.reset()
                console.print("[green]✅ Environment reset complete![/green]")
            except Exception as e:
                reset_error = e
                console.print(f"[yellow]⚠️  Reset failed: {e}[/yellow]")
                console.print("[yellow]   Continuing without reset...[/yellow]")

            # Get public URL
            public_url = await env.get_public_url()
            console.print(f"[cyan]Public URL:[/cyan] {public_url}")

            user_data_dir = Path.home() / ".plato" / "chrome-data"
            # Clear existing browser data for a fresh session
            if user_data_dir.exists():
                shutil.rmtree(user_data_dir, ignore_errors=True)
            user_data_dir.mkdir(parents=True, exist_ok=True)

            console.print("[cyan]Launching Chrome with Data Review extension...[/cyan]")

            from playwright.async_api import async_playwright

            playwright = await async_playwright().start()

            browser = await playwright.chromium.launch_persistent_context(
                str(user_data_dir),
                headless=False,
                args=[
                    f"--disable-extensions-except={extension_path}",
                    f"--load-extension={extension_path}",
                ],
            )

            # Wait for extension to load
            await asyncio.sleep(2)

            # Find extension ID via CDP
            extension_id = None
            temp_page = await browser.new_page()
            try:
                cdp = await temp_page.context.new_cdp_session(temp_page)
                targets_result = await cdp.send("Target.getTargets")
                for target_info in targets_result.get("targetInfos", []):
                    ext_url = target_info.get("url", "")
                    if "chrome-extension://" in ext_url:
                        parts = ext_url.replace("chrome-extension://", "").split("/")
                        if parts:
                            extension_id = parts[0]
                            break
            except Exception as e:
                console.print(f"[yellow]⚠️  CDP query failed: {e}[/yellow]")
            finally:
                await temp_page.close()

            if extension_id:
                console.print("[green]✅ Extension loaded[/green]")
            else:
                console.print("[yellow]⚠️  Could not find extension ID. Please set API key manually.[/yellow]")

            # Navigate to public URL and auto-login
            console.print("[cyan]Opening environment...[/cyan]")
            main_page = await browser.new_page()
            if public_url:
                await main_page.goto(public_url)
                console.print(f"[green]✅ Loaded: {public_url}[/green]")

            # Auto-login using env.login() (same as review env)
            console.print("[cyan]Logging into environment...[/cyan]")
            try:
                await env.login(main_page, dataset="base", from_api=True)
                console.print("[green]✅ Logged into environment[/green]")
            except Exception as e:
                console.print(f"[yellow]⚠️  Auto-login failed: {e}[/yellow]")
                console.print("[yellow]   You may need to log in manually[/yellow]")

            # Check state after login to verify no mutations
            console.print("\n[cyan]Checking environment state after login...[/cyan]")
            if reset_error is not None:
                console.print("[yellow]⚠️  Skipping state check because reset did not complete successfully.[/yellow]")
                console.print(f"[yellow]   Reset failure: {reset_error}[/yellow]")
            else:
                try:
                    state_data = await env.get_state(merge_mutations=True)
                    console.print(f"\n[bold cyan]Environment {env.id}:[/bold cyan]")

                    if isinstance(state_data, dict):
                        if state_data.get("error"):
                            console.print("\n[bold red]❌ State API Error:[/bold red]")
                            console.print(f"[red]{state_data['error']}[/red]")
                            console.print("[yellow]The worker may not be properly connected.[/yellow]")
                        else:
                            mutations = state_data.pop("mutations", [])
                            console.print("\n[bold]State:[/bold]")
                            safe_print(json.dumps(state_data, indent=2, default=str))
                            if mutations:
                                console.print(f"\n[bold red]⚠️  Mutations ({len(mutations)}):[/bold red]")
                                safe_print(json.dumps(mutations, indent=2, default=str))
                            else:
                                console.print("\n[green]No mutations recorded[/green]")
                    else:
                        console.print(f"[yellow]Unexpected state format: {type(state_data)}[/yellow]")
                except Exception as e:
                    console.print(f"[red]❌ Error getting state: {e}[/red]")

            # Use options page to set API key
            if extension_id:
                options_page = await browser.new_page()
                try:
                    await options_page.goto(
                        f"chrome-extension://{extension_id}/options.html",
                        wait_until="domcontentloaded",
                        timeout=5000,
                    )

                    # Set API keys
                    await options_page.fill("#platoApiKey", api_key)
                    if DEFAULT_DATAGEN_API_KEY:
                        await options_page.fill("#platoDatagenApiKey", DEFAULT_DATAGEN_API_KEY)
                    _cred_key, _cred_val = _get_claude_credentials()
                    if _cred_val:
                        await options_page.fill("#claudeOauthCredentials", _cred_val)
                    if DEFAULT_ANCHOR_KEY:
                        await options_page.fill("#anchorApiKey", DEFAULT_ANCHOR_KEY)
                    save_button = options_page.locator('button:has-text("Save")')
                    if await save_button.count() > 0:
                        await save_button.click()
                        await asyncio.sleep(0.3)
                    console.print("[green]✅ API keys saved[/green]")

                except Exception as e:
                    console.print(f"[yellow]⚠️  Could not set up extension: {e}[/yellow]")
                finally:
                    await options_page.close()

            # Bring main page to front
            if main_page:
                await main_page.bring_to_front()

            console.print()
            console.print("[bold]Instructions:[/bold]")
            console.print("  1. Click the Data Review extension icon to open the sidebar")
            console.print(f"  2. Enter '{simulator_name}' as the simulator name and click Start Review")
            console.print("  3. Take screenshots and add comments for any issues")
            console.print("  4. Select Pass or Reject and submit the review")
            console.print("  5. When done, press Control-C to exit")

            # Show all data reviews if available
            if data_reviews:
                console.print()
                console.print("=" * 60)
                console.print(f"[bold]📋 Data Reviews ({len(data_reviews)}):[/bold]")
                for review in data_reviews:
                    outcome = review.get("outcome", "unknown")
                    timestamp = review.get("timestamp_iso", "")[:10]  # Just the date
                    if outcome == "reject":
                        console.print(f"\n[red]REJECTED[/red] ({timestamp})")
                    else:
                        console.print(f"\n[green]PASSED[/green] ({timestamp})")

                    # Handle both old 'comments' field and new 'sim_comments' structure
                    sim_comments = review.get("sim_comments")
                    if sim_comments:
                        for item in sim_comments:
                            comment_text = item.get("comment", "")
                            if comment_text:
                                console.print(f"  - {comment_text}")
                    else:
                        # Fallback to old comments field
                        comments = review.get("comments")
                        if comments:
                            console.print(f"  {comments}")
                console.print("=" * 60)

            console.print()
            console.print("[bold]Press Control-C when done[/bold]")

            try:
                await asyncio.Event().wait()
            except KeyboardInterrupt:
                console.print("\n[yellow]Interrupted by user[/yellow]")
            except Exception:
                pass

            console.print("\n[green]✅ Browser closed. Review session ended.[/green]")

            # --- Post-review actions (mirrors env review flow) ---
            # Re-fetch simulator to check if a review was submitted via the extension
            try:
                async with httpx.AsyncClient(base_url=base_url, timeout=60.0) as post_client:
                    post_sim = await get_simulator_by_name.asyncio(
                        client=post_client,
                        name=simulator_name,
                        x_api_key=api_key,
                    )
                post_config = sim_config_dict(post_sim.config)
                post_status = post_config.get("status", "")
                simulator_id = post_sim.id

                # Check if the extension submitted a reject (status went back to data_in_progress)
                if post_status == "data_in_progress":
                    console.print("\n[bold yellow]Review was rejected — post-review options:[/bold yellow]")

                    # Option to launch datagen world
                    reviews = post_config.get("reviews") or []
                    latest_reject_comments = _get_latest_rejected_data_review_comments(reviews)

                    console.print("\n[bold]Launch datagen?[/bold]")
                    console.print("  1. none")
                    console.print("  2. fresh (new datagen run)")
                    console.print("  3. resume (rerun with review feedback)")
                    datagen_choice = typer.prompt("Choice [1/2/3]", default="1").strip()

                    datagen_action = None
                    if datagen_choice in ("2", "3"):
                        datagen_action = "fresh" if datagen_choice == "2" else "resume"

                    # Confirm
                    if datagen_action:
                        console.print("\n[bold]Post-review summary:[/bold]")
                        console.print(f"  Datagen: {datagen_action}")
                        if datagen_action == "resume" and latest_reject_comments:
                            console.print(f"  Review feedback: {len(latest_reject_comments)} comment(s)")

                        if not typer.confirm("Proceed?", default=True):
                            console.print("[yellow]Cancelled — no post-review actions taken.[/yellow]")
                        else:
                            async with httpx.AsyncClient(base_url=base_url, timeout=60.0) as action_client:
                                # Set default assignees if missing
                                existing_data_assignees = post_config.get("data_assignees") or []
                                existing_data_review_assignees = post_config.get("data_review_assignees") or []
                                updates = {}
                                if not existing_data_assignees:
                                    updates["data_assignees"] = DEFAULT_DATA_ASSIGNEES
                                if not existing_data_review_assignees:
                                    updates["data_review_assignees"] = DEFAULT_DATA_REVIEW_ASSIGNEES
                                if updates:
                                    await update_simulator.asyncio(
                                        client=action_client,
                                        simulator_id=simulator_id,
                                        body=AppApiV1SimulatorRoutesUpdateSimulatorRequest(**updates),
                                        x_api_key=api_key,
                                    )

                                launched_session = await _launch_datagen_world(
                                    simulator_name=simulator_name,
                                    artifact_id=artifact_id,
                                    api_key=api_key,
                                    review_comments=latest_reject_comments if datagen_action == "resume" else None,
                                )
                                if launched_session:
                                    console.print(f"[green]✅ Datagen launched: {launched_session}[/green]")
                                    console.print(
                                        f"[cyan]View:[/cyan] https://chronos.plato.so/sessions/{launched_session}"
                                    )

                elif post_status == "ready":
                    console.print("\n[green]✅ Review passed — simulator is now ready[/green]")

                elif post_status == "data_review_requested":
                    console.print("\n[yellow]No review was submitted (status unchanged).[/yellow]")

                else:
                    console.print(f"\n[cyan]Current status:[/cyan] {post_status}")

            except Exception as e:
                console.print(f"[yellow]⚠️  Could not fetch post-review status: {e}[/yellow]")

        except Exception as e:
            console.print(f"[red]❌ Error during review session: {e}[/red]")
            raise

        finally:
            try:
                if env:
                    await env.close()
                if browser:
                    await browser.close()
                if playwright:
                    await playwright.stop()
                if temp_ext_dir.exists():
                    shutil.rmtree(temp_ext_dir, ignore_errors=True)
            except Exception as e:
                console.print(f"[yellow]⚠️  Cleanup error: {e}[/yellow]")

    handle_async(_review_data())


# =============================================================================
# SUBMIT COMMANDS
# =============================================================================


@submit_app.command(name="env")
def submit_env():
    """Submit environment artifact for review after snapshot.

    Reads simulator name and artifact_id from .plato/state.json, syncs metadata from
    plato-config.yml to the server, and transitions status to env_review_requested.
    Run from the simulator directory after creating a snapshot.

    Requires simulator status: env_in_progress
    No arguments needed - reads everything from .plato/state.json and plato-config.yml.
    """
    api_key = require_api_key()

    # Read sandbox state from .plato/state.json (written by plato sandbox snapshot)
    state_file = Path(".plato/state.json")
    if not state_file.exists():
        console.print("[red]No .plato/state.json found[/red]")
        console.print("[yellow]Run 'plato sandbox snapshot' first.[/yellow]")
        raise typer.Exit(1)
    sandbox_data = json.loads(state_file.read_text())

    artifact_id = sandbox_data.get("artifact_id")
    if not artifact_id:
        console.print("[red]No artifact_id in .plato/state.json[/red]")
        console.print("[yellow]Run 'plato sandbox snapshot' to create one.[/yellow]")
        raise typer.Exit(1)

    plato_config_path = sandbox_data.get("plato_config_path", "plato-config.yml")

    # Read plato-config.yml to get simulator name and metadata
    plato_config = read_plato_config(plato_config_path)
    simulator_name = require_plato_config_field(plato_config, "service")

    # Extract metadata from plato-config.yml
    datasets = plato_config.get("datasets", {})
    base_dataset = datasets.get("base", {})
    metadata = base_dataset.get("metadata", {})

    # Get metadata fields
    config_description = metadata.get("description")
    config_license = metadata.get("license")
    config_source_code_url = metadata.get("source_code_url")
    config_start_url = metadata.get("start_url")
    config_favicon_url = metadata.get("favicon_url")  # Explicit favicon URL

    # Get authentication from variables
    variables = metadata.get("variables", [])
    username = None
    password = None
    for var in variables:
        if isinstance(var, dict):
            var_name = var.get("name", "").lower()
            var_value = var.get("value")
            if var_name in ("username", "user", "email", "admin_email", "adminmail"):
                username = var_value
            elif var_name in ("password", "pass", "admin_password", "adminpass"):
                password = var_value

    # Use explicit favicon_url from config, or warn if missing
    favicon_url = config_favicon_url
    if not favicon_url:
        console.print("[yellow]⚠️  No favicon_url in plato-config.yml metadata - favicon will not be set[/yellow]")
        console.print(
            "[yellow]   Add 'favicon_url: https://www.google.com/s2/favicons?domain=APPNAME.com&sz=32' to metadata[/yellow]"
        )

    async def _submit_env():
        base_url = _get_base_url()

        async with httpx.AsyncClient(base_url=base_url, timeout=60.0) as client:
            # Get simulator by name
            sim = await get_simulator_by_name.asyncio(
                client=client,
                name=simulator_name,
                x_api_key=api_key,
            )
            simulator_id = sim.id
            current_config = sim_config_dict(sim.config)
            current_status = current_config.get("status", "not_started")

            # Validate status transition
            validate_status_transition(current_status, "env_in_progress", "submit env")

            # Show info and submit
            console.print(f"[cyan]Simulator:[/cyan]      {simulator_name}")
            console.print(f"[cyan]Artifact ID:[/cyan]    {artifact_id}")
            console.print(f"[cyan]Current Status:[/cyan] {current_status}")
            console.print()

            # Sync metadata from plato-config.yml to server
            console.print("[cyan]Syncing metadata to server...[/cyan]")

            # Build update request with metadata from plato-config.yml
            update_fields: dict = {}

            if config_description:
                update_fields["description"] = config_description
                console.print(f"  [dim]description:[/dim] {config_description[:50]}...")

            if favicon_url:
                update_fields["img_url"] = favicon_url
                console.print(f"  [dim]img_url:[/dim] {favicon_url}")

            if config_license:
                update_fields["license"] = config_license
                console.print(f"  [dim]license:[/dim] {config_license}")

            if config_source_code_url:
                update_fields["source_code_url"] = config_source_code_url
                console.print(f"  [dim]source_code_url:[/dim] {config_source_code_url}")

            if config_start_url:
                update_fields["start_url"] = config_start_url
                console.print(f"  [dim]start_url:[/dim] {config_start_url}")

            if username and password:
                update_fields["authentication"] = Authentication(user=username, password=password)
                console.print(f"  [dim]authentication:[/dim] {username} / {'*' * len(password)}")

            # Always include base_artifact_id
            update_fields["base_artifact_id"] = artifact_id

            try:
                await update_simulator.asyncio(
                    client=client,
                    simulator_id=simulator_id,
                    body=AppApiV1SimulatorRoutesUpdateSimulatorRequest(**update_fields),
                    x_api_key=api_key,
                )
                console.print("[green]✅ Metadata synced to server[/green]")
            except Exception as e:
                console.print(f"[yellow]⚠️  Could not sync metadata: {e}[/yellow]")

            console.print()

            # Update simulator status
            await update_simulator_status.asyncio(
                client=client,
                simulator_id=simulator_id,
                body=UpdateStatusRequest(status=Status("env_review_requested")),
                x_api_key=api_key,
            )

            console.print("[green]✅ Environment review requested successfully![/green]")
            console.print(f"[cyan]Status:[/cyan] {current_status} → env_review_requested")
            console.print(f"[cyan]Base Artifact:[/cyan] {artifact_id}")

    handle_async(_submit_env())


@submit_app.command(name="data")
def submit_data(
    simulator: str = typer.Argument(
        None,
        help="Simulator name. Supports colon notation: sim:<artifact-uuid>",
    ),
    artifact: str = typer.Option(
        None,
        "--artifact",
        "-a",
        help="Artifact UUID to submit for data review (required).",
    ),
):
    """Submit data artifact for review after data generation.

    Transitions simulator from data_in_progress → data_review_requested and
    tags the artifact as 'data-pending-review'.

    Requires simulator status: data_in_progress

    Options:
        -s, --simulator: Simulator name. Supports colon notation:
            '-s sim:<uuid>' or use separate -a flag
        -a, --artifact: Artifact UUID to submit (required)
    """
    api_key = require_api_key()

    # Parse simulator and artifact from args (artifact IS required for data submit)
    simulator_name, artifact_id = parse_simulator_artifact(
        simulator, artifact, require_artifact=True, command_name="submit data"
    )

    async def _submit_data():
        # simulator_name and artifact_id are guaranteed set by parse_simulator_artifact with require_artifact=True
        assert simulator_name is not None, "simulator_name must be set"
        assert artifact_id is not None, "artifact_id must be set"

        base_url = _get_base_url()

        async with httpx.AsyncClient(base_url=base_url, timeout=60.0) as client:
            # Get simulator by name
            sim = await get_simulator_by_name.asyncio(
                client=client,
                name=simulator_name,
                x_api_key=api_key,
            )
            simulator_id = sim.id
            current_config = sim_config_dict(sim.config)
            current_status = current_config.get("status", "not_started")

            # Validate status transition
            validate_status_transition(current_status, "data_in_progress", "submit data")

            # Show info and submit
            console.print(f"[cyan]Simulator:[/cyan]      {simulator_name}")
            console.print(f"[cyan]Artifact ID:[/cyan]    {artifact_id}")
            console.print(f"[cyan]Current Status:[/cyan] {current_status}")
            console.print()

            await update_simulator_status.asyncio(
                client=client,
                simulator_id=simulator_id,
                body=UpdateStatusRequest(status=Status("data_review_requested")),
                x_api_key=api_key,
            )

            # Record the data artifact on the sim config so review/resume can
            # find it. update_tag below only tags the artifact; it does not
            # write data_artifact_id.
            await update_simulator.asyncio(
                client=client,
                simulator_id=simulator_id,
                body=AppApiV1SimulatorRoutesUpdateSimulatorRequest(data_artifact_id=artifact_id),
                x_api_key=api_key,
            )

            # update_tag requires SIM_DATA_REVIEWER and returns 200 with
            # {success: false} on auth rejection — so check the body, not just
            # HTTP status. Tolerate failure since data_artifact_id above is the
            # load-bearing field for downstream flows.
            try:
                tag_resp = await update_tag.asyncio(
                    client=client,
                    body=UpdateTagRequest(
                        simulator_name=simulator_name,
                        artifact_id=artifact_id,
                        tag_name="data-pending-review",
                        dataset="base",
                    ),
                    x_api_key=api_key,
                )
                if not tag_resp.success:
                    console.print(f"[yellow]⚠️  Could not set artifact tag: {tag_resp.error}[/yellow]")
            except Exception as e:
                console.print(f"[yellow]⚠️  Could not set artifact tag: {e}[/yellow]")

            console.print("[green]✅ Data review requested successfully![/green]")
            console.print(f"[cyan]Status:[/cyan] {current_status} → data_review_requested")
            console.print(f"[cyan]Data Artifact:[/cyan] {artifact_id}")

    handle_async(_submit_data())


# =============================================================================
# EXPERIMENT COMMANDS
# plato pm experiment env base push
# plato pm experiment env fix push
# plato pm experiment data base push
# =============================================================================


def _push_experiment(pipeline: str, mode: str, api_key: str) -> None:
    """Create a new experiment version in Chronos (creates the file if it doesn't exist)."""
    name = _EXPERIMENT_NAMES[(pipeline, mode)]
    template_file = {
        ("env", "base"): "env-create-launch.json",
        ("env", "fix"): "env-fix-launch.json",
        ("data", "base"): "datagen-launch.json",
        ("data", "unified"): "datagen-unified-launch.json",
        ("check", "base"): "sim-checker-launch.json",
        ("blank", "base"): "simcreator-blank-launch.json",
        ("agent", "data-load"): "agent-data-load.json",
    }[(pipeline, mode)]
    description = {
        ("env", "base"): "Run via: plato pm start env <sim> (fresh create) or plato pm review env <sim> (action=fresh)",
        ("env", "fix"): "Run via: plato pm review env <sim> (action=fix, after rejection)",
        ("data", "base"): "Run via: plato pm start data <sim>",
        ("data", "unified"): "Run via: plato pm start data --unified <sim1> <sim2> ...",
        ("check", "base"): "Run via: plato pm start checker <sim>",
        (
            "blank",
            "base",
        ): "Run via: plato pm start blank <sim> (also chained automatically by simcreator's env-create / env-fix as their terminal phase)",
        ("agent", "data-load"): "AgentSession recipe for loading user-supplied source data into a sim",
    }[(pipeline, mode)]
    world_key = {
        ("env", "base"): "structured-execution",
        ("env", "fix"): "structured-execution",
        ("data", "base"): "interactive",
        ("data", "unified"): "structured-execution",
        ("check", "base"): "structured-execution",
        ("blank", "base"): "structured-execution",
        ("agent", "data-load"): "structured-execution",
    }[(pipeline, mode)]
    config_json = _load_template(template_file)

    with httpx.Client(timeout=30.0) as client:
        resp = client.get(
            f"{CHRONOS_URL}/api/experiments/files",
            headers={"X-API-Key": api_key},
        )
        resp.raise_for_status()
        files = resp.json().get("files", [])
        match = next((f for f in files if f["name"] == name), None)

        if not match:
            resp = client.post(
                f"{CHRONOS_URL}/api/experiments/files",
                json={
                    "name": name,
                    "description": description,
                    "world_key": world_key,
                    "config_json": config_json,
                },
                headers={"X-API-Key": api_key},
            )
            resp.raise_for_status()
            console.print(f"[green]✅ Created experiment '{name}' (v1)[/green]")
        else:
            file_id = match["public_id"]
            patch_resp = client.patch(
                f"{CHRONOS_URL}/api/experiments/files/{file_id}",
                json={"description": description},
                headers={"X-API-Key": api_key},
            )
            patch_resp.raise_for_status()
            resp = client.post(
                f"{CHRONOS_URL}/api/experiments/files/{file_id}/versions",
                json={"config_json": config_json},
                headers={"X-API-Key": api_key},
            )
            resp.raise_for_status()
            version_num = resp.json().get("latest_version", {}).get("version_number", "?")
            console.print(f"[green]✅ Pushed experiment '{name}' → v{version_num}[/green]")


@experiment_env_base_app.command(name="push")
def experiment_env_base_push() -> None:
    """Push local env-create-launch.json to Chronos as a new experiment version."""
    api_key = require_api_key()
    _push_experiment("env", "base", api_key)


@experiment_env_fix_app.command(name="push")
def experiment_env_fix_push() -> None:
    """Push local env-fix-launch.json to Chronos as a new experiment version."""
    api_key = require_api_key()
    _push_experiment("env", "fix", api_key)


@experiment_data_base_app.command(name="push")
def experiment_data_base_push() -> None:
    """Push local datagen-launch.json to Chronos as a new experiment version."""
    api_key = require_api_key()
    _push_experiment("data", "base", api_key)


@experiment_data_unified_app.command(name="push")
def experiment_data_unified_push() -> None:
    """Push local datagen-unified-launch.json to Chronos as a new experiment version."""
    api_key = require_api_key()
    _push_experiment("data", "unified", api_key)


@experiment_check_base_app.command(name="push")
def experiment_check_base_push() -> None:
    """Push local sim-checker-launch.json to Chronos as a new experiment version."""
    api_key = require_api_key()
    _push_experiment("check", "base", api_key)


@experiment_blank_base_app.command(name="push")
def experiment_blank_base_push() -> None:
    """Push local simcreator-blank-launch.json to Chronos as a new experiment version."""
    api_key = require_api_key()
    _push_experiment("blank", "base", api_key)


@experiment_agent_data_load_app.command(name="push")
def experiment_agent_data_load_push() -> None:
    """Push local agent-data-load.json to Chronos as a new experiment version."""
    api_key = require_api_key()
    _push_experiment("agent", "data-load", api_key)
