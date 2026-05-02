"""Agent start logic — refactored from the old cli.py."""

from __future__ import annotations

import asyncio
import logging
import os
import signal
import sys

from rich.console import Console
from rich.panel import Panel

from ghost_pc import __version__

console = Console()


def run_agent(
    port: int | None = None,
    fps: int | None = None,
    log_level: str | None = None,
) -> None:
    """Start the GhostPC agent with config file + env var + CLI overrides."""
    console.print(
        Panel.fit(
            "[bold cyan]GhostPC[/] — Control your PC from WhatsApp",
            subtitle=f"v{__version__}",
        )
    )

    if sys.platform != "win32":
        console.print(
            "[yellow]Warning:[/] GhostPC is designed for Windows. "
            "Screen capture and input injection won't work on this platform."
        )

    # Load .env if present (backward compat).
    # In frozen builds os.getcwd() may be System32, so check next to the exe
    # and inside GHOST_HOME first.
    from ghost_pc.config.schema import GHOST_HOME

    env_candidates: list[str] = []
    if getattr(sys, "frozen", False):
        env_candidates.append(os.path.join(os.path.dirname(sys.executable), ".env"))
    env_candidates.append(str(GHOST_HOME / ".env"))
    env_candidates.append(os.path.join(os.getcwd(), ".env"))
    for env_path in env_candidates:
        if os.path.exists(env_path):
            _load_dotenv(env_path)
            break

    # Configure logging
    effective_log_level = log_level or os.environ.get("GHOST_LOG_LEVEL", "INFO")
    logging.basicConfig(
        level=getattr(logging, effective_log_level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    # Build Settings from config file > env vars > CLI overrides
    from ghost_pc.config.settings import Settings

    try:
        settings = Settings.from_config(
            stream_port=port,
            screen_fps=fps,
            log_level=log_level,
        )
    except ValueError as exc:
        console.print(f"[red]Error:[/] {exc}")
        console.print("Run [bold]ghost setup[/] to configure, or set GEMINI_API_KEY env var.")
        sys.exit(1)

    # ADK uses GOOGLE_API_KEY internally
    if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = settings.gemini_api_key

    from ghost_pc._node import find_node

    if not find_node():
        console.print(
            "[red]Error:[/] Node.js not found.\nInstall Node.js 20+ from https://nodejs.org"
        )
        sys.exit(1)

    console.print("[dim]Starting GhostPC agent...[/]")

    try:
        asyncio.run(_async_main(settings))
    except KeyboardInterrupt:
        console.print("\n[yellow]Shutting down...[/]")


async def _async_main(settings: object) -> None:
    """Main async orchestrator — starts all subsystems."""
    from ghost_pc.agent.orchestrator import Orchestrator
    from ghost_pc.config.settings import Settings

    assert isinstance(settings, Settings)
    orchestrator = Orchestrator(settings)

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, lambda: asyncio.create_task(orchestrator.shutdown()))
        except NotImplementedError:
            pass

    await orchestrator.run()


def _load_dotenv(path: str) -> None:
    """Minimal .env loader — no external dependency needed."""
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip("'\"")
            if key and not os.environ.get(key):
                os.environ[key] = value
