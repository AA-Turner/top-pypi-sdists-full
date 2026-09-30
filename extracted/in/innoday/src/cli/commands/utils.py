"""
InnoDay CLI Utility Commands

Handles utility operations like status, ping, version, etc.
"""

import argparse
import asyncio
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import httpx
from packaging.version import InvalidVersion, Version
from rich.markup import escape

from src.cli.client import APIError, InnoDayAPIClient
from src.cli.commands.session import _fetch_me
from src.cli.commands.upgrade import _fetch_pypi_latest, _versions_equal
from src.cli.utils import guidance
from src.cli.utils.formatters import (
    OutputFormatter,
    ProgressReporter,
    format_datetime,
    format_error,
    format_success,
)
from src.cli.utils.presentation import (
    make_console,
    print_command_header,
    print_identity,
    print_step,
)
from src.version import get_version

console = make_console()


class UtilityCommands:
    """Utility commands for system status and information."""

    @staticmethod
    def setup_parser(parser: argparse.ArgumentParser, command_name: str) -> None:
        if command_name == "ping":
            parser.add_argument("service", choices=["api"], help="Service to ping")

    @staticmethod
    async def execute(args: argparse.Namespace, config) -> int:
        command = args.command

        if command == "status":
            return await UtilityCommands._handle_status(args, config)
        elif command == "ping":
            return await UtilityCommands._handle_ping(args, config)
        elif command == "health":
            return await UtilityCommands._handle_health(args, config)
        elif command == "version":
            return await UtilityCommands._handle_version(args, config)
        else:
            console.print(format_error(f"Unknown utility command: {command}"))
            return 1

    @staticmethod
    async def _handle_status(args: argparse.Namespace, config) -> int:
        formatter = OutputFormatter(
            format_type=getattr(args, "format", None) or config.get_output_format(),
            color_enabled=config.is_color_enabled(),
        )

        status_data = {
            "api_url": config.get_api_url(),
            "organization": config.get_current_organization(),
        }

        async with InnoDayAPIClient(config) as client:
            try:
                with ProgressReporter("Checking API status..."):
                    await client.ping_api()
                status_data["api_status"] = "healthy"
            except APIError:
                status_data["api_status"] = "unreachable"

        formatter.format_status(status_data)
        return 0

    @staticmethod
    async def _handle_ping(args: argparse.Namespace, config) -> int:
        async with InnoDayAPIClient(config) as client:
            try:
                with ProgressReporter("Pinging API..."):
                    response = await client.ping_api()
                console.print(
                    format_success(f"API is reachable at {config.get_api_url()}")
                )

                if response.get("message"):
                    console.print(f"[dim]{response['message']}[/dim]")

                return 0

            except APIError as e:
                console.print(format_error(f"API is not reachable: {e}"))
                return 1

    @staticmethod
    async def _handle_health(args: argparse.Namespace, config) -> int:
        """Is InnoDay up, and is the CLI on this machine OK? (PF-473)

        Seven rows: API, database and server version from `GET /health`; then
        this CLI's version against PyPI, any other `innoday` on PATH, sign-in,
        and the config file. Project detail is `innoday status`'s job.

        `ping` is not this command. It calls `GET /` (`ping_api`), whose
        `status` field is the string literal `"\u2705 Healthy"` -- it cannot
        report a problem. `/health` is the only route that runs `SELECT 1` and
        answers 503 when the database is gone.

        A 503 is a *verdict*, not a transport failure, so the unhealthy payload
        is reported rather than swallowed into an error string. The exit code
        is 1 only when the API or the database is unhealthy -- the local rows
        warn, they never fail the command.
        """
        print_command_header(args, config, "health")
        api_url = config.get_api_url()

        with ProgressReporter("Checking InnoDay…"):
            (api, health), latest = await asyncio.gather(
                _check_health(config), asyncio.to_thread(_fetch_pypi_latest)
            )
            sign_in = await _check_sign_in(api_url, config, api["reachable"])

        result: Dict[str, Any] = {
            # The server's own fields, verbatim and top-level, as before.
            "status": health.get("status", "unreachable"),
            "database": health.get("database", "unknown"),
            "version": health.get("version"),
            "environment": health.get("environment"),
            "api": api,
            "cli": _cli_version(get_version(), latest),
            "path": _path_installs(os.environ.get("PATH", ""), _running_innoday()),
            "sign_in": sign_in,
            "config": _config_file(Path(config.config_path)),
        }
        healthy = api["reachable"] and result["status"] == "healthy"

        if getattr(args, "format", None) == "json":
            print(json.dumps(result, indent=2))
        else:
            _display_health(result)
        return 0 if healthy else 1

    @staticmethod
    async def _handle_version(args: argparse.Namespace, config) -> int:
        print_identity()
        console.print()
        console.print("[muted]Configuration:[/muted]")
        console.print(f"  Config file: {config.config_path}")
        console.print(f"  API URL: {config.get_api_url()}")

        current_org = config.get_current_organization()
        if current_org:
            console.print(f"  Organization: {current_org}")
        else:
            console.print("  Organization: [bad]Not configured[/bad]")

        console.print()
        console.print("[muted]Service Status:[/muted]")

        async with InnoDayAPIClient(config) as client:
            try:
                await client.ping_api()
                console.print("  API: [good]✓ Online[/good]")
            except APIError:
                console.print("  API: [bad]✗ Offline[/bad]")

        return 0


# --------------------------------------------------------------------------
# `innoday health` rows (PF-473). Each gathers one row's facts; none prints.
# --------------------------------------------------------------------------


async def _check_health(config) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """The API row, and the server's `/health` body (or `{}` if unreachable)."""
    api: Dict[str, Any] = {
        "url": config.get_api_url(),
        "reachable": False,
        "latency_ms": None,
        "error": None,
    }
    health: Dict[str, Any] = {}
    start = time.monotonic()
    async with InnoDayAPIClient(config) as client:
        try:
            health = await client.get_api_health()
            api["reachable"] = True
        except APIError as e:
            # 503 is the route's own verdict and carries the same body as 200.
            # Anything else is a transport/auth failure: the server said nothing.
            if e.status_code == 503 and isinstance(e.response_data, dict):
                health = e.response_data
                api["reachable"] = True
            else:
                api["error"] = str(e)
        except httpx.HTTPError as e:
            # Connection refused / DNS / timeout arrive as httpx errors, not
            # APIError -- without this, health printed no rows at all.
            api["error"] = str(e) or type(e).__name__
    if api["reachable"]:
        api["latency_ms"] = round((time.monotonic() - start) * 1000, 1)
    return api, health


def _cli_version(installed: str, latest: Optional[str]) -> Dict[str, Any]:
    """This CLI against PyPI: current, behind, ahead (a dev build) or unknown."""
    state = "unknown"
    if latest:
        if _versions_equal(installed, latest):
            state = "current"
        else:
            try:
                state = "behind" if Version(installed) < Version(latest) else "ahead"
            except InvalidVersion:
                state = "unknown"
    return {"installed": installed, "latest": latest, "state": state}


def _running_innoday() -> Optional[Path]:
    """The `innoday` executable running now, or None when run from source
    (`python -m src.cli.main`), where there is no such file."""
    argv0 = Path(sys.argv[0]) if sys.argv and sys.argv[0] else None
    if argv0 is None or argv0.name != "innoday":
        return None
    try:
        return argv0.resolve()
    except OSError:
        return None


def _path_installs(path_env: str, running: Optional[Path]) -> Dict[str, Any]:
    """Every `innoday` on PATH, and which of them are not the one running.

    Scans each PATH directory the way `shutil.which` does, but keeps every
    match, not just the first. The same install reached twice (a symlink, a
    repeated PATH entry) counts once. Nothing found is ever executed.
    """
    found: List[str] = []
    resolved: List[Path] = []
    for directory in path_env.split(os.pathsep):
        if not directory:
            continue
        candidate = Path(directory) / "innoday"
        try:
            if not (candidate.is_file() and os.access(candidate, os.X_OK)):
                continue
            real = candidate.resolve()
        except OSError:
            continue
        if real in resolved:
            continue
        found.append(str(candidate))
        resolved.append(real)

    others = [f for f, r in zip(found, resolved) if r != running]
    # What a new shell's `innoday` would run is the first match. If that is
    # not the one running now, the two can print different things.
    shadowed = running is not None and bool(resolved) and resolved[0] != running
    return {
        "running": str(running) if running else None,
        "found": found,
        "others": others,
        "shadowed": shadowed,
    }


async def _check_sign_in(api_url: str, config, api_reachable: bool) -> Dict[str, Any]:
    """Is there a token, and does the API accept it? Signed out is not an error."""
    token = config.get_cli_token()
    block: Dict[str, Any] = {
        "signed_in": bool(token),
        "valid": None,
        "name": None,
        "email": None,
        "expires_at": None,
    }
    if not token or not api_reachable:
        return block
    me = await _fetch_me(api_url.rstrip("/"), token, config.get_team_secret())
    block["valid"] = me is not None
    if me:
        block["name"] = me.get("full_name") or me.get("name")
        block["email"] = me.get("email")
        # Imported here: status.py is a sibling command module, reused not copied.
        from src.cli.commands.status import StatusCommands

        block["expires_at"] = (await StatusCommands._token_info(api_url, config)).get(
            "expires_at"
        )
    return block


def _config_file(path: Path) -> Dict[str, Any]:
    """Can the config be read, and how many unreadable copies were set aside
    in `archive/` beside it (PF-467)."""
    readable: Optional[bool] = None
    if path.exists():
        try:
            json.loads(path.read_text())
            readable = True
        except (OSError, ValueError):
            readable = False
    archive = path.parent / "archive"
    try:
        archived = sum(1 for p in archive.glob(f"{path.name}.*") if p.is_file())
    except OSError:
        archived = 0
    return {
        "path": str(path),
        "exists": path.exists(),
        "readable": readable,
        "archived_copies": archived,
        "archive_dir": str(archive),
    }


def _home(path: str) -> str:
    home = str(Path.home())
    return "~" + path[len(home) :] if path.startswith(home) else path


def _row(mark: str, label: str, text: str, detail: str = "") -> None:
    symbol = {"good": "✓", "warn": "⚠", "bad": "✗"}[mark]
    line = f"  [{mark}]{symbol}[/{mark}] {label:<9} {text}"
    if detail:
        line += f" [muted]· {detail}[/muted]"
    console.print(line)


def _display_health(r: Dict[str, Any]) -> None:
    """Two sections, one line per row. Values are escaped: they are data."""
    api = r["api"]
    console.print()
    print_step(1, "InnoDay")
    if api["reachable"]:
        _row("good", "API", escape(api["url"]), f"{api['latency_ms']}ms")
    else:
        _row("bad", "API", escape(api["url"]), escape(f"unreachable: {api['error']}"))

    database = r["database"]
    if not api["reachable"]:
        _row("bad", "Database", "not checked", "the API did not answer")
    elif database == "connected":
        _row("good", "Database", "connected")
    else:
        _row("bad", "Database", escape(str(database)), escape(f"status {r['status']}"))

    if r["version"]:
        env = r.get("environment")
        _row(
            "good", "Server", escape(str(r["version"])), escape(str(env)) if env else ""
        )
    else:
        _row("warn", "Server", "version unknown")

    console.print()
    print_step(2, "This CLI")
    cli = r["cli"]
    installed = escape(cli["installed"])
    if cli["state"] == "current":
        _row("good", "CLI", installed, "latest on PyPI")
    elif cli["state"] == "behind":
        _row(
            "warn",
            "CLI",
            installed,
            escape(f"PyPI has {cli['latest']} — run `innoday upgrade`"),
        )
    elif cli["state"] == "ahead":
        _row("good", "CLI", installed, escape(f"ahead of PyPI {cli['latest']}"))
    else:
        _row("warn", "CLI", installed, "couldn't check PyPI")

    path = r["path"]
    # Run from source, one install on PATH is simply "the" install. Otherwise
    # any other install is one that can answer in place of this one.
    several = bool(path["others"]) and (
        path["running"] is not None or len(path["others"]) > 1
    )
    if path["shadowed"]:
        _row(
            "warn",
            "PATH",
            escape(f"`innoday` in a new shell runs {_home(path['found'][0])}"),
            "not this one",
        )
    elif several:
        _row("warn", "PATH", f"{len(path['others'])} other innoday install(s)")
    elif path["running"]:
        _row("good", "PATH", "no other innoday on PATH")
    elif path["found"]:
        _row(
            "good", "PATH", escape(_home(path["found"][0])), "the only innoday on PATH"
        )
    else:
        _row("warn", "PATH", "no innoday on PATH", "running from source")
    if path["shadowed"] or several:
        for other in path["others"]:
            console.print(f"[muted]              {escape(_home(other))}[/muted]")

    sign_in = r["sign_in"]
    if not sign_in["signed_in"]:
        _row("warn", "Sign-in", "not signed in", "run `innoday login`")
    elif sign_in["valid"] is None:
        _row("warn", "Sign-in", "token present", "not checked: the API did not answer")
    elif sign_in["valid"]:
        who = sign_in["name"] or "signed in"
        detail = sign_in["email"] or ""
        if sign_in["expires_at"]:
            expiry = format_datetime(sign_in["expires_at"])
            detail = f"{detail} · expires {expiry}" if detail else f"expires {expiry}"
        _row("good", "Sign-in", escape(who), escape(detail))
    else:
        _row("bad", "Sign-in", escape(guidance.SIGN_IN_REJECTED))

    cfg = r["config"]
    archived = cfg["archived_copies"]
    note = (
        f"{archived} archived cop{'y' if archived == 1 else 'ies'} in "
        f"{_home(cfg['archive_dir'])}"
        if archived
        else ""
    )
    if cfg["readable"] is False:
        _row("bad", "Config", escape(_home(cfg["path"])), "unreadable")
    elif not cfg["exists"]:
        _row("good", "Config", "no config file yet", escape(note) or "using defaults")
    else:
        _row("good", "Config", escape(_home(cfg["path"])), escape(note))
