"""Project Management CLI commands for Plato simulator workflow."""

import asyncio
import json
import os
import re
import shutil
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import httpx
import typer
import yaml
from rich.table import Table

from plato._generated.api.v1.env import get_simulator_by_name, get_simulators
from plato._generated.api.v1.organization import get_organization_members
from plato._generated.api.v1.simulator import (
    add_simulator_review,
    update_simulator,
    update_simulator_status,
    update_tag,
)
from plato._generated.models import (
    AddReviewRequest,
    AppApiV1SimulatorRoutesUpdateSimulatorRequest,
    Authentication,
    Outcome,
    ReviewType,
    SimReviewComment,
    UpdateStatusRequest,
    UpdateTagRequest,
)
from plato.cli.utils import (
    console,
    handle_async,
    read_plato_config,
    require_api_key,
    require_plato_config_field,
)
from plato.v1.flow_executor import FlowExecutor
from plato.v1.models.flow import Flow
from plato.v1.sdk import Plato

# =============================================================================
# CONSTANTS
# =============================================================================

# UUID pattern for detecting artifact IDs in sim:artifact notation
UUID_PATTERN = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE)

CHRONOS_URL = "https://chronos.plato.so"
DEFAULT_ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY", "")
DEFAULT_DATAGEN_API_KEY = os.getenv("PLATO_DATAGEN_API_KEY", "")
DEFAULT_WORLD_PACKAGE_STRUCTURED = "plato-world-structured-execution"
DEFAULT_WORLD_PACKAGE_INTERACTIVE = "plato-world-interactive"
DEFAULT_ANCHOR_KEY = os.getenv("ANCHOR_API_KEY", "")
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

pm_app.add_typer(list_app, name="list")
pm_app.add_typer(review_app, name="review")
pm_app.add_typer(submit_app, name="submit")
pm_app.add_typer(start_app, name="start")


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


def validate_status_transition(current_status: str, expected_status: str, command_name: str):
    """Validate that current status matches expected status for the command."""
    if current_status != expected_status:
        console.print(f"[red]❌ Invalid status for {command_name}[/red]")
        console.print(f"\n[yellow]Current status:[/yellow]  {current_status}")
        console.print(f"[yellow]Expected status:[/yellow] {expected_status}")
        console.print(f"\n[yellow]Cannot run {command_name} from status '{current_status}'[/yellow]")
        raise typer.Exit(1)


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
    """Find the extensions/data-review/templates directory."""
    package_dir = Path(__file__).resolve().parent.parent  # plato/
    is_installed = "site-packages" in str(package_dir)

    if is_installed:
        templates_dir = package_dir / "extensions" / "data-review" / "templates"
    else:
        repo_root = package_dir.parent.parent  # plato-client/
        templates_dir = repo_root / "extensions" / "data-review" / "templates"

    # Fallback to env var
    if not templates_dir.exists():
        plato_client_dir_env = os.getenv("PLATO_CLIENT_DIR")
        if plato_client_dir_env:
            env_path = Path(plato_client_dir_env) / "extensions" / "data-review" / "templates"
            if env_path.exists():
                templates_dir = env_path

    return templates_dir


def _load_template(name: str) -> dict:
    """Load a JSON launch template by name."""
    templates_dir = _find_templates_dir()
    template_path = templates_dir / name
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")
    with open(template_path) as f:
        return json.load(f)


def _get_last_chronos_session(tags: list[str], api_key: str) -> dict | None:
    """Get the most recent Chronos session matching all given tags. Returns session dict or None."""
    try:
        with httpx.Client(timeout=15.0) as client:
            params = [("tag", t) for t in tags] + [("limit", "1")]
            resp = client.get(
                f"{CHRONOS_URL}/api/sessions",
                params=params,
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


async def _launch_env_world(
    action: str,
    simulator_name: str,
    artifact_id: str,
    feedback: str,
    api_key: str,
    current_config: dict,
    action_inputs: dict | None = None,
) -> str | None:
    """Launch a structured world (fresh or resume) after env reject. Returns session_id or None.

    action_inputs: Pre-collected inputs from the caller. For fresh: {"github_url": "..."}.
                   For resume: {"resume_session": "..."}.
    """
    datagen_api_key = DEFAULT_DATAGEN_API_KEY
    world_package = DEFAULT_WORLD_PACKAGE_STRUCTURED
    inputs = action_inputs or {}

    try:
        if action == "fresh":
            github_url = inputs.get("github_url", "")
            if not github_url:
                console.print("[yellow]No GitHub URL provided, skipping launch.[/yellow]")
                return None

            template = _load_template("env-create-launch.json")
            config = template["world"]["config"]
            config["sim_name"] = simulator_name
            config["github_url"] = github_url
            config["plato_api_key"] = datagen_api_key
            config["anthropic_api_key"] = DEFAULT_ANTHROPIC_KEY
            config["skill_runner"]["config"]["plato_api_key"] = datagen_api_key
            config["skill_runner"]["config"]["anthropic_api_key"] = DEFAULT_ANTHROPIC_KEY
            template["world"]["package"] = world_package
            template["tags"].append(simulator_name)

        else:
            # Resume
            base_artifact_id = current_config.get("base_artifact_id")
            if not base_artifact_id:
                console.print("[red]Simulator has no base_artifact_id. Cannot launch resume.[/red]")
                return None

            resume_session = inputs.get("resume_session", "")

            template = _load_template("env-fix-launch.json")
            config = template["world"]["config"]
            config["sim_name"] = simulator_name
            config["artifact_id"] = base_artifact_id
            config["feedback"] = feedback
            config["plato_api_key"] = datagen_api_key
            config["anthropic_api_key"] = DEFAULT_ANTHROPIC_KEY
            config["skill_runner"]["config"]["plato_api_key"] = datagen_api_key
            config["skill_runner"]["config"]["anthropic_api_key"] = DEFAULT_ANTHROPIC_KEY
            config["state"]["resume_session"] = resume_session
            template["world"]["package"] = world_package
            template["tags"].append(simulator_name)

        console.print("[cyan]Launching world on Chronos...[/cyan]")
        session_id = _launch_on_chronos(template, api_key)
        return session_id

    except FileNotFoundError as e:
        console.print(f"[red]❌ {e}[/red]")
        return None
    except Exception as e:
        console.print(f"[red]❌ World launch failed: {e}[/red]")
        return None


async def _launch_datagen_world(
    simulator_name: str,
    artifact_id: str,
    api_key: str,
    iterations: int = 2,
) -> str | None:
    """Launch an interactive datagen world. Returns session_id or None."""
    datagen_api_key = DEFAULT_DATAGEN_API_KEY
    world_package = DEFAULT_WORLD_PACKAGE_INTERACTIVE

    try:
        template = _load_template("datagen-launch.json")

        # Fetch DB configs for MCP setup
        with httpx.Client(timeout=30.0) as client:
            resp = client.get(
                f"{_get_base_url()}/api/v1/simulator/{artifact_id}/db_config",
                headers={"X-API-Key": api_key},
            )
            db_configs = resp.json() if resp.status_code == 200 else []
            if not isinstance(db_configs, list):
                db_configs = [db_configs]

        # Build MCPs
        mcps = []
        for db in db_configs:
            mcps.append(
                {
                    "type": "db",
                    "db_type": db.get("db_type"),
                    "db_port": db.get("db_port"),
                    "db_user": db.get("db_user"),
                    "db_password": db.get("db_password"),
                    "db_database": db.get("db_database"),
                    "service": simulator_name,
                }
            )
        mcps.append({"type": "vm"})
        mcps.append({"type": "browser"})
        mcps.append({"type": "functions", "session_id": f"run-{simulator_name}", "service": simulator_name})

        config = template["world"]["config"]
        config["anthropic_api_key"] = DEFAULT_ANTHROPIC_KEY
        config["plato_api_key"] = datagen_api_key
        config["anchor_api_key"] = DEFAULT_ANCHOR_KEY
        config["mcps"] = mcps
        config["envs"] = [{"artifact_id": artifact_id, "alias": simulator_name}]
        template["world"]["package"] = world_package

        # Update iterations
        msg = config["initial_messages"][0]
        msg["iterations"] = iterations
        prompt = msg["message"]
        msg["continuation_prompt"] = (
            f"Continue working on the task below. Review what you've done so far, then pick up where you left off.\n\n---\n\n{prompt}"
        )

        template["tags"].append(simulator_name)

        console.print("[cyan]Launching datagen world on Chronos...[/cyan]")
        session_id = _launch_on_chronos(template, api_key)
        return session_id

    except FileNotFoundError as e:
        console.print(f"[red]❌ {e}[/red]")
        return None
    except Exception as e:
        console.print(f"[red]❌ Datagen launch failed: {e}[/red]")
        return None


# =============================================================================
# START COMMANDS
# =============================================================================


@start_app.command(name="env")
def start_env(
    simulators: list[str] = typer.Argument(..., help="Simulator name(s)"),
    resume: bool = typer.Option(False, "--resume", "-r", help="Resume from last simcreator session instead of fresh"),
):
    """Start simcreator (env pipeline) for one or more simulators.

    Moves status to env_in_progress and launches simcreator on Chronos.

    Examples:
        plato pm start env aureus memos docmost
        plato pm start env aureus -r    # resume from last session
    """
    api_key = require_api_key()

    async def _start():
        base_url = _get_base_url()
        datagen_api_key = DEFAULT_DATAGEN_API_KEY
        world_package = DEFAULT_WORLD_PACKAGE_STRUCTURED

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
                current_config = sim.config or {}
                github_url = current_config.get("source_code_url", "")
                base_artifact_id = current_config.get("base_artifact_id", "")
                status = current_config.get("status", "not_started")

                if not github_url:
                    console.print(f"[yellow]⚠️  {sim_name}: no source_code_url, skipping[/yellow]")
                    continue

                entry = {
                    "name": sim_name,
                    "id": sim.id,
                    "status": status,
                    "github_url": github_url,
                    "base_artifact_id": base_artifact_id,
                }

                # For resume, find the last simcreator session
                if resume:
                    last = _get_last_chronos_session(tags=["simcreator", sim_name], api_key=api_key)
                    entry["resume_session"] = last["public_id"] if last else ""
                    if not entry["resume_session"]:
                        console.print(
                            f"[yellow]⚠️  {sim_name}: no previous simcreator session found, will start fresh[/yellow]"
                        )

                to_launch.append(entry)
            except Exception as e:
                console.print(f"[red]❌ {sim_name}: {e}[/red]")

        if not to_launch:
            console.print("[yellow]Nothing to launch.[/yellow]")
            return

        mode = "resume" if resume else "fresh"
        console.print(f"\n[bold]Will launch simcreator ({mode}) for {len(to_launch)} simulator(s):[/bold]")
        for s in to_launch:
            extra = f"resume={s.get('resume_session', '')[:12]}" if resume else s["github_url"]
            console.print(f"  {s['name']} ({s['status']}) — {extra}")

        if not typer.confirm("\nProceed?", default=True):
            console.print("[yellow]Cancelled.[/yellow]")
            return

        for s in to_launch:
            try:
                async with httpx.AsyncClient(base_url=base_url, timeout=60.0) as client:
                    await update_simulator_status.asyncio(
                        client=client,
                        simulator_id=s["id"],
                        body=UpdateStatusRequest(status="env_in_progress"),
                        x_api_key=api_key,
                    )

                template = _load_template("env-create-launch.json")
                config = template["world"]["config"]
                config["sim_name"] = s["name"]
                config["github_url"] = s["github_url"]
                config["plato_api_key"] = datagen_api_key
                config["anthropic_api_key"] = DEFAULT_ANTHROPIC_KEY
                config["skill_runner"]["config"]["plato_api_key"] = datagen_api_key
                config["skill_runner"]["config"]["anthropic_api_key"] = DEFAULT_ANTHROPIC_KEY
                if resume:
                    config["state"]["resume_session"] = s.get("resume_session", "")
                template["world"]["package"] = world_package
                template["tags"].append(s["name"])

                session_id = _launch_on_chronos(template, api_key)
                console.print(f"[green]✅ {s['name']}:[/green] {session_id}")
            except Exception as e:
                console.print(f"[red]❌ {s['name']}: {e}[/red]")

    handle_async(_start())


@start_app.command(name="data")
def start_data(
    simulators: list[str] = typer.Argument(..., help="Simulator name(s)"),
    resume: bool = typer.Option(False, "--resume", "-r", help="Resume datagen from review comments instead of fresh"),
    iterations: int = typer.Option(2, "--iterations", "-i", help="Datagen iterations"),
):
    """Start datagen (data pipeline) for one or more simulators.

    Moves status to data_in_progress, sets default assignees if missing,
    and launches an interactive datagen world on Chronos.

    Examples:
        plato pm start data aureus memos
        plato pm start data aureus -i 3
        plato pm start data aureus -r    # resume with review comments
    """
    api_key = require_api_key()

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
                current_config = sim.config or {}
                status = current_config.get("status", "not_started")
                artifact_id = current_config.get("base_artifact_id", "")

                if not artifact_id:
                    console.print(f"[yellow]⚠️  {sim_name}: no base_artifact_id, skipping[/yellow]")
                    continue

                to_launch.append(
                    {
                        "name": sim_name,
                        "id": sim.id,
                        "status": status,
                        "artifact_id": artifact_id,
                        "data_assignees": current_config.get("data_assignees"),
                        "data_review_assignees": current_config.get("data_review_assignees"),
                    }
                )
            except Exception as e:
                console.print(f"[red]❌ {sim_name}: {e}[/red]")

        if not to_launch:
            console.print("[yellow]Nothing to launch.[/yellow]")
            return

        mode = "resume" if resume else "fresh"
        console.print(
            f"\n[bold]Will launch datagen ({mode}, {iterations} iterations) for {len(to_launch)} simulator(s):[/bold]"
        )
        for s in to_launch:
            console.print(f"  {s['name']} ({s['status']}) — artifact {s['artifact_id'][:8]}...")

        if not typer.confirm("\nProceed?", default=True):
            console.print("[yellow]Cancelled.[/yellow]")
            return

        for s in to_launch:
            try:
                # Set default assignees if missing
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

                    # Move to data_in_progress
                    await update_simulator_status.asyncio(
                        client=client,
                        simulator_id=s["id"],
                        body=UpdateStatusRequest(status="data_in_progress"),
                        x_api_key=api_key,
                    )

                # Launch datagen
                launched = await _launch_datagen_world(
                    simulator_name=s["name"],
                    artifact_id=s["artifact_id"],
                    api_key=api_key,
                    iterations=iterations,
                )
                if launched:
                    console.print(f"[green]✅ {s['name']}:[/green] {launched}")
                else:
                    console.print(f"[red]❌ {s['name']}: launch returned None[/red]")
            except Exception as e:
                console.print(f"[red]❌ {s['name']}: {e}[/red]")

    handle_async(_start())


# =============================================================================
# ARCHIVE COMMAND
# =============================================================================


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
                current_config = sim.config or {}
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
                        body=UpdateStatusRequest(status="out_of_service"),
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
    """
    api_key = require_api_key()

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
            current_config = sim.config or {}
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
                        await executor.execute()
                        console.print("[green]✅ Local flow executed successfully[/green]")
                    except Exception as e:
                        console.print(f"[yellow]⚠️  Flow execution error: {e}[/yellow]")
                else:
                    # Use default login via env.login() (v1 API takes Page, not Browser)
                    if fake_time:
                        console.print("[yellow]⚠️  --clock with default login may not work correctly.[/yellow]")
                        console.print("[yellow]   Use --local with a flow file for reliable clock testing.[/yellow]")
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
                            console.print(json.dumps(state_data, indent=2, default=str))
                            if mutations:
                                has_mutations = True
                                console.print(f"\n[bold red]Mutations ({len(mutations)}):[/bold red]")
                                console.print(json.dumps(mutations, indent=2, default=str))
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
                    comments = recent_review.get("comments")
                    if comments:
                        console.print(f"[yellow]Reviewer Comments:[/yellow] {comments}")

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
                                        console.print(json.dumps(state_data, indent=2, default=str))
                                        if mutations:
                                            console.print(f"\n[bold]Mutations ({len(mutations)}):[/bold]")
                                            console.print(json.dumps(mutations, indent=2, default=str))
                                        else:
                                            console.print("\n[yellow]No mutations recorded[/yellow]")
                                else:
                                    console.print(json.dumps(state_data, indent=2, default=str))
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
                validate_status_transition(current_status, "env_review_requested", "review env pass")
                new_status = "env_approved"
            else:
                validate_status_transition(current_status, "env_review_requested", "review env reject")
                new_status = "env_in_progress"

            # Collect all inputs BEFORE submitting anything
            # (so Ctrl+C at any prompt means nothing gets submitted)
            reject_comments: str = ""
            reject_assignee_id = None
            reject_action = None
            reject_action_inputs = {}
            pass_start_datagen = False
            pass_datagen_iterations = 2

            if outcome == "pass":
                if typer.confirm("Auto-start datagen?", default=False):
                    pass_start_datagen = True
                    pass_datagen_iterations = int(typer.prompt("Iterations", default="2").strip() or "2")

            elif outcome == "reject":
                comments = ""
                while not comments:
                    comments = typer.prompt("Comments (required for reject)").strip()
                    if not comments:
                        console.print("[yellow]Comments are required when rejecting. Please provide feedback.[/yellow]")
                reject_comments = comments

                # Assign env assignee
                existing_assignees = current_config.get("env_assignees") or []
                if existing_assignees:
                    console.print(f"[cyan]Current env assignees:[/cyan] {existing_assignees}")
                assignee_input = typer.prompt("Add env assignee (user ID, enter to skip)", default="").strip()
                if assignee_input:
                    try:
                        reject_assignee_id = int(assignee_input)
                    except ValueError:
                        console.print(f"[yellow]⚠️  Invalid user ID: {assignee_input}[/yellow]")

                # Optionally launch a world
                github_url_from_config = current_config.get("source_code_url", "")
                base_artifact = current_config.get("base_artifact_id", "")
                console.print("\n[bold]Launch a world?[/bold]")
                console.print("  1. none")
                if github_url_from_config:
                    console.print(f"  2. fresh (simcreator — {github_url_from_config})")
                else:
                    console.print("  2. fresh (simcreator — no GitHub URL in config)")
                if base_artifact:
                    console.print(f"  3. resume (simcreator_resume — artifact {base_artifact[:8]}...)")
                else:
                    console.print("  3. resume (simcreator_resume — [red]no base_artifact_id[/red])")
                action_choice = typer.prompt("Choice [1/2/3]", default="1").strip()

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
                    resume_session = typer.prompt(
                        "Resume session (enter for above, 'none' for fresh)", default=default_resume
                    ).strip()
                    if resume_session.lower() == "none":
                        resume_session = ""
                    reject_action_inputs["resume_session"] = resume_session

            # --- All inputs collected. Confirm before submitting. ---

            console.print("\n[bold]Review summary:[/bold]")
            console.print(f"  Outcome: {outcome}")
            if reject_comments:
                console.print(f"  Comments: {reject_comments}")
            if reject_assignee_id is not None:
                console.print(f"  Add env assignee: {reject_assignee_id}")
            if reject_action:
                action_desc = reject_action
                if reject_action == "fresh":
                    action_desc += f" ({reject_action_inputs.get('github_url', '')})"
                elif reject_action == "resume":
                    rs = reject_action_inputs.get("resume_session", "")
                    action_desc += f" ({rs[:12]}...)" if rs else " (fresh state)"
                console.print(f"  World: {action_desc}")
            if pass_start_datagen:
                console.print(f"  Datagen: fresh ({pass_datagen_iterations} iterations)")

            if not typer.confirm("Submit?", default=True):
                console.print("[yellow]Cancelled — nothing submitted.[/yellow]")
                return

            async with httpx.AsyncClient(base_url=base_url, timeout=60.0) as api_client:
                # Update status
                await update_simulator_status.asyncio(
                    client=api_client,
                    simulator_id=simulator_id,
                    body=UpdateStatusRequest(status=new_status),
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

                    # 2. Assign env reviewer (re-fetch to avoid stale data)
                    if reject_assignee_id is not None:
                        try:
                            # Re-fetch current config to get latest assignees
                            async with httpx.AsyncClient(base_url=base_url, timeout=60.0) as http_client:
                                fresh_sim = await get_simulator_by_name.asyncio(
                                    client=http_client,
                                    name=simulator_name,
                                    x_api_key=api_key,
                                )
                            fresh_config = fresh_sim.config or {}
                            existing = fresh_config.get("env_assignees") or []
                            merged = list(set(existing + [reject_assignee_id]))
                            await update_simulator.asyncio(
                                client=api_client,
                                simulator_id=simulator_id,
                                body=AppApiV1SimulatorRoutesUpdateSimulatorRequest(
                                    env_assignees=merged,
                                ),
                                x_api_key=api_key,
                            )
                            console.print(f"[green]✅ Assigned env assignee: {reject_assignee_id}[/green]")
                        except Exception as e:
                            console.print(f"[yellow]⚠️  Could not set assignee: {e}[/yellow]")

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

                # If passed, automatically tag artifact as prod-latest
                if outcome == "pass" and artifact_id:
                    console.print("\n[cyan]Tagging artifact as prod-latest...[/cyan]")
                    try:
                        # simulator_name and artifact_id are guaranteed to be set at this point
                        assert simulator_name is not None
                        await update_tag.asyncio(
                            client=api_client,
                            body=UpdateTagRequest(
                                simulator_name=simulator_name,
                                artifact_id=artifact_id,
                                tag_name="prod-latest",
                                dataset="base",
                            ),
                            x_api_key=api_key,
                        )
                        console.print(f"[green]✅ Tagged {artifact_id[:8]}... as prod-latest[/green]")
                    except Exception as e:
                        console.print(f"[yellow]⚠️  Could not tag as prod-latest: {e}[/yellow]")

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
                        fresh_config = fresh_sim.config or {}
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

                    # Move to data_in_progress
                    await update_simulator_status.asyncio(
                        client=api_client,
                        simulator_id=simulator_id,
                        body=UpdateStatusRequest(status="data_in_progress"),
                        x_api_key=api_key,
                    )
                    console.print(f"[cyan]Status:[/cyan] {new_status} → data_in_progress")

                    # Launch datagen
                    launched_session = await _launch_datagen_world(
                        simulator_name=simulator_name,
                        artifact_id=artifact_id,
                        api_key=api_key,
                        iterations=pass_datagen_iterations,
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
    """
    api_key = require_api_key()

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
                config = sim.config or {}

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
            try:
                await env.reset()
                console.print("[green]✅ Environment reset complete![/green]")
            except Exception as e:
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
                        console.print(json.dumps(state_data, indent=2, default=str))
                        if mutations:
                            console.print(f"\n[bold red]⚠️  Mutations ({len(mutations)}):[/bold red]")
                            console.print(json.dumps(mutations, indent=2, default=str))
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
                    if DEFAULT_ANTHROPIC_KEY:
                        await options_page.fill("#anthropicApiKey", DEFAULT_ANTHROPIC_KEY)
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
            current_config = sim.config or {}
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
                body=UpdateStatusRequest(status="env_review_requested"),
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
            current_config = sim.config or {}
            current_status = current_config.get("status", "not_started")

            # Validate status transition
            validate_status_transition(current_status, "data_in_progress", "submit data")

            # Show info and submit
            console.print(f"[cyan]Simulator:[/cyan]      {simulator_name}")
            console.print(f"[cyan]Artifact ID:[/cyan]    {artifact_id}")
            console.print(f"[cyan]Current Status:[/cyan] {current_status}")
            console.print()

            # Update simulator status
            await update_simulator_status.asyncio(
                client=client,
                simulator_id=simulator_id,
                body=UpdateStatusRequest(status="data_review_requested"),
                x_api_key=api_key,
            )

            # Set data_artifact_id via tag update (simulator_name and artifact_id already asserted above)
            try:
                await update_tag.asyncio(
                    client=client,
                    body=UpdateTagRequest(
                        simulator_name=simulator_name,
                        artifact_id=artifact_id,
                        tag_name="data-pending-review",
                        dataset="base",
                    ),
                    x_api_key=api_key,
                )
            except Exception as e:
                console.print(f"[yellow]⚠️  Could not set artifact tag: {e}[/yellow]")

            console.print("[green]✅ Data review requested successfully![/green]")
            console.print(f"[cyan]Status:[/cyan] {current_status} → data_review_requested")
            console.print(f"[cyan]Data Artifact:[/cyan] {artifact_id}")

    handle_async(_submit_data())
