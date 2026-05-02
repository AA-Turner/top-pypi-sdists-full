"""Top-level operator dashboard launcher for local Aegis checkouts."""

from __future__ import annotations

from argparse import SUPPRESS, ArgumentParser
from collections.abc import Mapping
from dataclasses import dataclass, replace
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import time
from typing import Any
import urllib.error
import urllib.request
import webbrowser

from apps.cli.cli_main_support import CliCardSection, _print_cli_card


REPO_ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_APP_DIR = REPO_ROOT / "apps" / "dashboard"
DASHBOARD_PACKAGE_PATH = DASHBOARD_APP_DIR / "package.json"
DASHBOARD_NODE_MODULES = DASHBOARD_APP_DIR / "node_modules"
DASHBOARD_DIST_DIR = DASHBOARD_APP_DIR / "dist"
DASHBOARD_DIST_INDEX = DASHBOARD_DIST_DIR / "index.html"
API_PROBE_TIMEOUT_SECONDS = 0.35
API_CONSOLE_PROBE_TIMEOUT_SECONDS = 15.0


@dataclass(frozen=True, slots=True)
class DashboardLaunchPlan:
    state_dir: Path
    profile_dir: Path
    api_database: Path
    api_host: str
    api_port: int
    ui_host: str
    ui_port: int
    dashboard_assets_present: bool
    dashboard_static_assets_present: bool
    frontend_dependencies_present: bool
    npm_available: bool

    @property
    def api_url(self) -> str:
        return f"http://{self.api_host}:{self.api_port}"

    @property
    def ui_url(self) -> str:
        return f"http://{self.ui_host}:{self.ui_port}"


def _build_parser(
    *,
    default_state_dir: Path | None = None,
    default_profile_dir: Path | None = None,
) -> ArgumentParser:
    parser = ArgumentParser(
        prog="aegis dashboard",
        description="Launch the local operator dashboard when frontend assets are present.",
    )
    parser.add_argument("--state-dir", default=default_state_dir, type=Path, help=SUPPRESS)
    parser.add_argument("--profile-dir", default=default_profile_dir, type=Path, help=SUPPRESS)
    parser.add_argument("--api-database", default=None, type=Path, help="Override the API database path.")
    parser.add_argument("--api-host", default="127.0.0.1")
    parser.add_argument("--api-port", default=8000, type=int)
    parser.add_argument("--host", dest="ui_host", default="127.0.0.1")
    parser.add_argument("--port", dest="ui_port", default=4174, type=int)
    parser.add_argument("--open", dest="open", action="store_true", default=True, help="Open the dashboard URL in the default browser.")
    parser.add_argument("--no-open", dest="open", action="store_false", help="Print the dashboard URL without opening a browser.")
    parser.add_argument(
        "--reuse-api",
        action="store_true",
        help="Attach to an existing healthy API on the requested API port instead of starting a fresh API.",
    )
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Skip the one-time dashboard frontend build check before launching.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the launch plan and readiness notes without starting any processes.",
    )
    return parser


def _build_plan(args) -> DashboardLaunchPlan:
    state_dir = Path(args.state_dir).expanduser()
    profile_dir = Path(args.profile_dir).expanduser()
    api_database = (
        Path(args.api_database).expanduser()
        if args.api_database is not None
        else state_dir / "aegis.sqlite3"
    )
    return DashboardLaunchPlan(
        state_dir=state_dir,
        profile_dir=profile_dir,
        api_database=api_database,
        api_host=str(args.api_host),
        api_port=int(args.api_port),
        ui_host=str(args.ui_host),
        ui_port=int(args.ui_port),
        dashboard_assets_present=DASHBOARD_PACKAGE_PATH.exists(),
        dashboard_static_assets_present=DASHBOARD_DIST_INDEX.exists(),
        frontend_dependencies_present=DASHBOARD_NODE_MODULES.exists(),
        npm_available=shutil.which("npm") is not None,
    )


def _print_plan(plan: DashboardLaunchPlan, *, ready_to_launch: bool) -> None:
    dependency_state = "ready" if plan.frontend_dependencies_present else "missing"
    asset_state = "present" if plan.dashboard_assets_present else "missing"
    static_asset_state = "present" if plan.dashboard_static_assets_present else "missing"
    npm_state = "ready" if plan.npm_available else "missing"
    sections = [
        CliCardSection(
            "Launch plan",
            (
                f"state_dir · {plan.state_dir}",
                f"profile_dir · {plan.profile_dir}",
                f"api_database · {plan.api_database}",
                f"api_url · {plan.api_url}",
                f"ui_url · {plan.ui_url}",
            ),
        ),
        CliCardSection(
            "Readiness",
            (
                f"dashboard_assets · {asset_state}",
                f"dashboard_static_assets · {static_asset_state}",
                f"npm · {npm_state}",
                f"frontend_dependencies · {dependency_state}",
                f"ready_to_launch · {'yes' if ready_to_launch else 'no'}",
            ),
        ),
    ]
    next_commands: tuple[str, ...] = ()
    if not plan.dashboard_assets_present and not plan.dashboard_static_assets_present:
        sections.append(
            CliCardSection(
                "Recovery",
                (
                    "This install does not include apps/dashboard frontend assets.",
                    "Use a local repo checkout and its launcher when you need the operator web surface.",
                ),
            )
        )
    elif plan.dashboard_assets_present and not plan.dashboard_static_assets_present and not plan.frontend_dependencies_present:
        sections.append(
            CliCardSection(
                "Recovery",
                (
                    "Install the dashboard frontend dependencies first:",
                    "npm --prefix apps/dashboard ci",
                ),
            )
        )
        next_commands = ("npm --prefix apps/dashboard ci", "aegis dashboard")
    _print_cli_card(
        "Aegis dashboard",
        "Operator dashboard launch plan over the live CLI state database.",
        sections=tuple(sections),
        next_commands=next_commands,
    )


def _terminate_process(process: subprocess.Popen[str] | None) -> None:
    if process is None or process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def _api_health_payload(plan: DashboardLaunchPlan) -> Mapping[str, Any] | None:
    request = urllib.request.Request(
        f"{plan.api_url}/healthz",
        headers={"Accept": "application/json"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=API_PROBE_TIMEOUT_SECONDS) as response:
            if response.status != 200:
                return None
            payload = json.loads(response.read().decode("utf-8"))
    except (OSError, TimeoutError, urllib.error.URLError, ValueError):
        return None
    return payload if isinstance(payload, Mapping) else None


def _api_health_ready(payload: Mapping[str, Any] | None) -> bool:
    return payload is not None and payload.get("service") == "aegis-api" and payload.get("status") == "ok"


def _api_console_ready(plan: DashboardLaunchPlan) -> bool:
    request = urllib.request.Request(
        f"{plan.api_url}/v1/operator/console",
        headers={"Accept": "application/json"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=API_CONSOLE_PROBE_TIMEOUT_SECONDS) as response:
            if response.status != 200:
                return False
            payload = json.loads(response.read().decode("utf-8"))
    except (OSError, TimeoutError, urllib.error.URLError, ValueError):
        return False
    return isinstance(payload, Mapping) and isinstance(payload.get("console"), Mapping)


def _find_free_api_port(plan: DashboardLaunchPlan) -> int:
    for port in range(plan.api_port + 1, plan.api_port + 40):
        candidate = replace(plan, api_port=port)
        if not _api_port_occupied(candidate):
            return port
    raise RuntimeError(f"Could not find a free API port near {plan.api_port}.")


def _api_port_occupied(plan: DashboardLaunchPlan) -> bool:
    return _port_occupied(plan.api_host, plan.api_port)


def _find_free_ui_port(plan: DashboardLaunchPlan) -> int:
    for port in range(plan.ui_port + 1, plan.ui_port + 40):
        if not _port_occupied(plan.ui_host, port):
            return port
    raise RuntimeError(f"Could not find a free dashboard UI port near {plan.ui_port}.")


def _ui_port_occupied(plan: DashboardLaunchPlan) -> bool:
    return _port_occupied(plan.ui_host, plan.ui_port)


def _port_occupied(host: str, port: int) -> bool:
    try:
        with socket.create_connection(
            (host, port),
            timeout=API_PROBE_TIMEOUT_SECONDS,
        ):
            return True
    except OSError:
        return False


def _ui_command(plan: DashboardLaunchPlan) -> list[str]:
    command = ["npm", "--prefix", str(DASHBOARD_APP_DIR), "run", "dev"]
    command.extend(["--", "--host", plan.ui_host, "--port", str(plan.ui_port), "--strictPort"])
    return command


def _static_dashboard_command(plan: DashboardLaunchPlan) -> list[str]:
    return [
        sys.executable,
        "-m",
        "apps.dashboard_static_server",
        "--host",
        plan.ui_host,
        "--port",
        str(plan.ui_port),
        "--database",
        str(plan.api_database),
        "--static-dir",
        str(DASHBOARD_DIST_DIR),
    ]


def _frontend_build_command() -> list[str]:
    return ["npm", "--prefix", str(DASHBOARD_APP_DIR), "run", "build"]


def _run_frontend_build() -> int:
    build = subprocess.run(_frontend_build_command(), cwd=REPO_ROOT, text=True)
    return build.returncode


def _prepare_dashboard_ports(plan: DashboardLaunchPlan, *, reuse_api: bool) -> tuple[DashboardLaunchPlan, bool]:
    reuse_existing_api = False
    if reuse_api:
        api_health = _api_health_payload(plan)
        reuse_existing_api = _api_health_ready(api_health) and _api_console_ready(plan)
    if not reuse_existing_api and _api_port_occupied(plan):
        plan = replace(plan, api_port=_find_free_api_port(plan))
    if _ui_port_occupied(plan):
        plan = replace(plan, ui_port=_find_free_ui_port(plan))
    return plan, reuse_existing_api


def _api_command(plan: DashboardLaunchPlan) -> list[str]:
    return [
        sys.executable,
        "-m",
        "apps.api",
        "--host",
        plan.api_host,
        "--port",
        str(plan.api_port),
        "--database",
        str(plan.api_database),
    ]


def _api_status_label(reuse_existing_api: bool) -> str:
    if reuse_existing_api:
        return "reusing existing healthy API"
    return "starting fresh local API"


def _build_status_label(build_frontend: bool) -> str:
    if build_frontend:
        return "building latest dashboard assets before launch"
    return "skipped by --skip-build"


def _use_source_dashboard(plan: DashboardLaunchPlan) -> bool:
    return plan.dashboard_assets_present and plan.frontend_dependencies_present and plan.npm_available


def _use_packaged_dashboard(plan: DashboardLaunchPlan) -> bool:
    return plan.dashboard_static_assets_present and not _use_source_dashboard(plan)


def _run_dashboard(
    plan: DashboardLaunchPlan,
    *,
    open_browser: bool,
    build_frontend: bool = True,
    reuse_api: bool = False,
) -> int:
    if not plan.dashboard_assets_present and not plan.dashboard_static_assets_present:
        _print_plan(plan, ready_to_launch=False)
        return 1
    if plan.dashboard_assets_present and not plan.dashboard_static_assets_present and not plan.npm_available:
        _print_cli_card(
            "Aegis dashboard",
            "npm is required to launch the dashboard frontend.",
            sections=(CliCardSection("Recovery", ("Install Node.js and npm, then rerun `aegis dashboard`.",)),),
        )
        return 1
    if plan.dashboard_assets_present and not plan.dashboard_static_assets_present and not plan.frontend_dependencies_present:
        _print_plan(plan, ready_to_launch=False)
        return 1
    use_packaged_dashboard = _use_packaged_dashboard(plan)
    if build_frontend and _use_source_dashboard(plan):
        build_status = _run_frontend_build()
        if build_status != 0:
            return build_status or 1
        plan = replace(plan, dashboard_static_assets_present=DASHBOARD_DIST_INDEX.exists())
        use_packaged_dashboard = False
    plan, reuse_existing_api = _prepare_dashboard_ports(
        plan,
        reuse_api=False if use_packaged_dashboard else reuse_api,
    )
    api_command = _api_command(plan)

    ui_env = os.environ.copy()
    ui_env["VITE_AEGIS_API_BASE_URL"] = plan.api_url
    ui_env["AEGIS_DASHBOARD_API_AUTO_START"] = "0"

    _print_cli_card(
        "Aegis dashboard",
        "Launching the operator dashboard against the live CLI state database.",
        sections=(
            CliCardSection(
                "Endpoints",
                (
                    f"api_url · {plan.api_url}",
                    f"ui_url · {plan.ui_url}",
                    f"api_database · {plan.api_database}",
                    f"api_status · {'same-process packaged API' if use_packaged_dashboard else _api_status_label(reuse_existing_api)}",
                    f"frontend_build · {'using packaged dashboard assets' if use_packaged_dashboard else _build_status_label(build_frontend)}",
                ),
            ),
        ),
    )

    api_process: subprocess.Popen[str] | None = None
    ui_process: subprocess.Popen[str] | None = None
    try:
        if use_packaged_dashboard:
            ui_process = subprocess.Popen(_static_dashboard_command(plan), cwd=REPO_ROOT, text=True)
        elif not reuse_existing_api:
            api_process = subprocess.Popen(api_command, cwd=REPO_ROOT, text=True)
            time.sleep(0.5)
            if api_process.poll() is not None:
                return api_process.returncode or 1
        if not use_packaged_dashboard:
            ui_process = subprocess.Popen(_ui_command(plan), cwd=REPO_ROOT, env=ui_env, text=True)
        time.sleep(0.8)
        if ui_process.poll() is not None:
            return ui_process.returncode or 1
        opened = False
        if open_browser:
            opened = webbrowser.open(plan.ui_url)
        if not opened:
            print(f"Aegis dashboard URL: {plan.ui_url}")
        while True:
            if api_process is not None and api_process.poll() is not None:
                return api_process.returncode or 1
            if ui_process.poll() is not None:
                return ui_process.returncode or 1
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nStopping Aegis dashboard...")
        return 0
    finally:
        _terminate_process(ui_process)
        _terminate_process(api_process)


def command_main(
    argv: list[str] | None = None,
    *,
    default_state_dir: Path | None = None,
    default_profile_dir: Path | None = None,
) -> int:
    parser = _build_parser(
        default_state_dir=default_state_dir,
        default_profile_dir=default_profile_dir,
    )
    args = parser.parse_args(argv)
    plan = _build_plan(args)
    ready_to_launch = _use_source_dashboard(plan) or plan.dashboard_static_assets_present
    if args.dry_run:
        _print_plan(plan, ready_to_launch=ready_to_launch)
        return 0
    return _run_dashboard(
        plan,
        open_browser=bool(args.open),
        build_frontend=not bool(args.skip_build),
        reuse_api=bool(args.reuse_api),
    )


__all__ = ["command_main"]
