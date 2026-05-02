"""Shared launcher for editable installs and checkout-backed wrappers."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Final

from apps.cli.__main__ import main as cli_main
from apps.cron_scheduler_command import command_main as cron_scheduler_command_main
from apps.cli.skills_command import command_main as skills_command_main
from apps.dashboard_command import command_main as dashboard_command_main
from apps.gateway.__main__ import command_main as gateway_command_main
from apps.runtime_layout import default_cli_state_dir, default_gateway_state_dir, default_profile_dir
from packages.state import ensure_profile_aegis_file

DEFAULT_PROFILE_MANIFEST: Final[dict[str, object]] = {
    "profile_id": "profile-local",
    "display_name": "Aegis",
    "mode": "companion",
    "preferences": [
        "tone:grounded",
        "memory:durable",
        "identity:aegis",
    ],
    "companion": {
        "personality_preset": "companion",
        "personality": [
            "warm",
            "present",
            "grounded",
        ],
        "initiative": "gentle",
        "notes": [
            "protect continuity",
            "carry the durable thread",
        ],
    },
    "enabled_capabilities": [
        "cli.primary",
    ],
}

_CORE_CLI_COMMANDS: Final[tuple[tuple[str, str], ...]] = (
    ("init", "Run first-time setup and persist identity, provider readiness, and the first clone session."),
    ("status", "Review provider, model, and security readiness before opening the wake surface."),
    ("provider", "Configure or inspect the active provider, model, reasoning effort, and context window."),
    ("clone", "Clone a fresh Aegis individual and optionally enter it immediately."),
    ("clones", "Inspect or retire existing Aegis clones."),
    ("wake", "Enter an existing Aegis clone through the branded TUI or run one provider-backed turn."),
)
_EXTRA_COMMANDS: Final[tuple[tuple[str, str], ...]] = (
    ("skills", "Inspect, search, install, and toggle skill packages without entering wake."),
    ("gateway", "Manage IM providers and accounts."),
    ("cron", "Manage the background cron scheduler."),
    ("dashboard", "Launch the local operator dashboard when frontend assets are present."),
)


def _ensure_profile_bundle(profile_dir: Path) -> None:
    profile_dir.mkdir(parents=True, exist_ok=True)
    ensure_profile_aegis_file(profile_dir)
    manifest_path = profile_dir / "profile.json"
    if not manifest_path.exists():
        manifest_path.write_text(
            json.dumps(DEFAULT_PROFILE_MANIFEST, indent=2) + "\n",
            encoding="utf-8",
        )


def _build_top_level_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="aegis",
        description=(
            "Aegis launcher with explicit init, status, provider, clone, clones, wake, "
            "skills, gateway, cron, and dashboard entrypoints."
        ),
    )
    subparsers = parser.add_subparsers(dest="command")
    for name, help_text in (*_CORE_CLI_COMMANDS, *_EXTRA_COMMANDS):
        subparsers.add_parser(name, help=help_text)
    return parser


def _forward_cli(
    argv: list[str],
    *,
    state_dir: Path,
    profile_dir: Path,
) -> int:
    forwarded = [
        "--state-dir",
        str(state_dir),
        "--profile-dir",
        str(profile_dir),
        *argv,
    ]
    return cli_main(forwarded)


def main(argv: list[str] | None = None) -> int:
    resolved_argv = list(sys.argv[1:] if argv is None else argv)
    state_dir = default_cli_state_dir()
    profile_dir = default_profile_dir()
    gateway_state_dir = default_gateway_state_dir()
    state_dir.mkdir(parents=True, exist_ok=True)
    _ensure_profile_bundle(profile_dir)
    if not resolved_argv:
        return _forward_cli([], state_dir=state_dir, profile_dir=profile_dir)

    command = resolved_argv[0]
    if command in {"-h", "--help"}:
        _build_top_level_parser().print_help()
        return 0
    if command == "gateway":
        return gateway_command_main(
            resolved_argv[1:],
            default_profile_dir=profile_dir,
            default_state_dir=gateway_state_dir,
            default_control_profile_dir=profile_dir,
            default_control_state_dir=state_dir,
        )
    if command == "cron":
        return cron_scheduler_command_main(
            resolved_argv[1:],
            default_profile_dir=profile_dir,
            default_state_dir=gateway_state_dir,
            default_control_profile_dir=profile_dir,
            default_control_state_dir=state_dir,
        )
    if command == "skills":
        return skills_command_main(
            resolved_argv[1:],
            default_state_dir=state_dir,
            default_profile_dir=profile_dir,
        )
    if command == "dashboard":
        return dashboard_command_main(
            resolved_argv[1:],
            default_state_dir=state_dir,
            default_profile_dir=profile_dir,
        )
    if command == "health":
        return _forward_cli(["status", *resolved_argv[1:]], state_dir=state_dir, profile_dir=profile_dir)
    if command in {name for name, _ in _CORE_CLI_COMMANDS}:
        return _forward_cli(resolved_argv, state_dir=state_dir, profile_dir=profile_dir)
    _build_top_level_parser().error(
        f"argument command: invalid choice: {command!r} "
        f"(choose from {', '.join(repr(name) for name, _ in (*_CORE_CLI_COMMANDS, *_EXTRA_COMMANDS))})"
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
