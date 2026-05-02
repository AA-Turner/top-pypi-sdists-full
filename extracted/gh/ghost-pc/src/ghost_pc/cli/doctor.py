"""Health checks for GhostPC installation."""

from __future__ import annotations

import socket
import subprocess
import sys

from rich.console import Console

from ghost_pc._node import find_node, find_npm
from ghost_pc.config.schema import CONFIG_PATH, GhostConfig

console = Console()


def run_doctor() -> None:
    """Run all health checks and print results."""
    console.print("[bold]GhostPC Doctor[/]\n")

    checks = [
        _check_python_version,
        _check_platform,
        _check_nodejs,
        _check_npm,
        _check_config_file,
        _check_api_key_set,
        _check_api_key_valid,
        _check_bridge_installed,
        _check_bridge_deps,
        _check_whatsapp_auth,
        _check_screen_capture,
        _check_port_available,
    ]

    passed = 0
    warned = 0
    failed = 0

    for check in checks:
        status = check()
        if status == "pass":
            passed += 1
        elif status == "warn":
            warned += 1
        else:
            failed += 1

    console.print()
    parts: list[str] = []
    if passed:
        parts.append(f"[green]{passed} passed[/]")
    if warned:
        parts.append(f"[yellow]{warned} warnings[/]")
    if failed:
        parts.append(f"[red]{failed} failed[/]")
    console.print("  ".join(parts))

    if failed:
        console.print("\nRun [bold]ghost setup[/] to fix configuration issues.")


def _check_python_version() -> str:
    v = sys.version_info
    if v >= (3, 12):
        console.print(f"  [green]PASS[/]  Python {v.major}.{v.minor}.{v.micro}")
        return "pass"
    console.print(f"  [red]FAIL[/]  Python {v.major}.{v.minor} — need 3.12+")
    return "fail"


def _check_platform() -> str:
    if sys.platform == "win32":
        console.print("  [green]PASS[/]  Windows platform")
        return "pass"
    console.print("  [yellow]WARN[/]  Not Windows — desktop control limited")
    return "warn"


def _check_nodejs() -> str:
    node = find_node()
    if not node:
        console.print("  [red]FAIL[/]  Node.js not found — install from https://nodejs.org")
        return "fail"
    try:
        result = subprocess.run([node, "--version"], capture_output=True, text=True, timeout=5)
        version = result.stdout.strip()
        console.print(f"  [green]PASS[/]  Node.js {version}")
        return "pass"
    except (subprocess.SubprocessError, OSError):
        console.print("  [yellow]WARN[/]  Node.js found but version check failed")
        return "warn"


def _check_npm() -> str:
    if find_npm():
        console.print("  [green]PASS[/]  npm available")
        return "pass"
    console.print("  [red]FAIL[/]  npm not found")
    return "fail"


def _check_config_file() -> str:
    if CONFIG_PATH.exists():
        console.print(f"  [green]PASS[/]  Config: {CONFIG_PATH}")
        return "pass"
    console.print("  [yellow]WARN[/]  No config file — run [bold]ghost setup[/]")
    return "warn"


def _check_api_key_set() -> str:
    import os

    cfg = GhostConfig.load()
    key = cfg.gemini_api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if key:
        console.print("  [green]PASS[/]  API key configured")
        return "pass"
    console.print("  [red]FAIL[/]  API key missing — run [bold]ghost setup[/]")
    return "fail"


def _check_api_key_valid() -> str:
    import os

    cfg = GhostConfig.load()
    key = cfg.gemini_api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        console.print("  [dim]SKIP[/]  API key validation (no key)")
        return "warn"
    try:
        from google import genai

        client = genai.Client(api_key=key)
        next(iter(client.models.list()))
        console.print("  [green]PASS[/]  API key valid")
        return "pass"
    except Exception:
        console.print("  [red]FAIL[/]  API key invalid — check your key")
        return "fail"


def _check_bridge_installed() -> str:
    cfg = GhostConfig.load()
    bridge_dir = cfg.get_bridge_dir()
    index_js = bridge_dir / "index.js"
    if index_js.exists():
        console.print(f"  [green]PASS[/]  Bridge: {bridge_dir}")
        return "pass"
    console.print("  [red]FAIL[/]  Bridge not installed — run [bold]ghost setup[/]")
    return "fail"


def _check_bridge_deps() -> str:
    cfg = GhostConfig.load()
    node_modules = cfg.get_bridge_dir() / "node_modules"
    if node_modules.is_dir():
        console.print("  [green]PASS[/]  Bridge dependencies installed")
        return "pass"
    console.print("  [red]FAIL[/]  Bridge node_modules missing — run npm install")
    return "fail"


def _check_whatsapp_auth() -> str:
    cfg = GhostConfig.load()
    creds_dir = cfg.get_credentials_dir() / "whatsapp"
    if creds_dir.is_dir() and any(creds_dir.iterdir()):
        console.print("  [green]PASS[/]  WhatsApp paired")
        return "pass"
    console.print("  [yellow]WARN[/]  WhatsApp not paired — run [bold]ghost setup[/]")
    return "warn"


def _check_screen_capture() -> str:
    try:
        import bettercam  # noqa: F401

        console.print("  [green]PASS[/]  bettercam available")
        return "pass"
    except ImportError:
        console.print("  [yellow]WARN[/]  bettercam not available (Windows only)")
        return "warn"


def _check_port_available() -> str:
    cfg = GhostConfig.load()
    port = cfg.stream_port
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", port))
        console.print(f"  [green]PASS[/]  Port {port} available")
        return "pass"
    except OSError:
        console.print(f"  [yellow]WARN[/]  Port {port} in use")
        return "warn"
