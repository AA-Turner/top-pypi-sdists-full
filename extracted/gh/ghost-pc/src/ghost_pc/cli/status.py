"""Status display — show current config and connection state."""

from __future__ import annotations

import os
import socket

from rich.console import Console
from rich.table import Table

from ghost_pc.config.schema import CONFIG_PATH, GhostConfig

console = Console()


def show_status() -> None:
    """Print current configuration and connection state."""
    cfg = GhostConfig.load()

    table = Table(title="GhostPC Status")
    table.add_column("Setting", style="cyan")
    table.add_column("Value")

    # Config file
    if CONFIG_PATH.exists():
        table.add_row("Config File", f"[green]{CONFIG_PATH}[/]")
    else:
        table.add_row("Config File", "[yellow]Not found[/]")

    # Setup completed
    if cfg.setup_completed:
        table.add_row("Setup", "[green]Complete[/]")
    else:
        table.add_row("Setup", "[yellow]Not completed — run ghost setup[/]")

    # API key
    key = cfg.gemini_api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if key:
        table.add_row("API Key", f"[green]{key[:8]}...[/]")
    else:
        table.add_row("API Key", "[red]Not set[/]")

    # Model
    table.add_row("Model Tier", cfg.model_tier)
    table.add_row("Model", cfg.gemini_model)
    table.add_row("Browser Method", cfg.browser_method)

    # Allowed numbers
    if cfg.allowed_numbers:
        table.add_row("Allowed Numbers", ", ".join(cfg.allowed_numbers))
    else:
        table.add_row("Allowed Numbers", "[dim]None (all allowed)[/]")

    # Streaming
    table.add_row("Stream Port", str(cfg.stream_port))
    table.add_row("Screen FPS", str(cfg.screen_fps))
    table.add_row("JPEG Quality", str(cfg.jpeg_quality))

    # Bridge
    bridge_dir = cfg.get_bridge_dir()
    if (bridge_dir / "index.js").exists():
        table.add_row("Bridge", f"[green]{bridge_dir}[/]")
    else:
        table.add_row("Bridge", "[red]Not installed[/]")

    # WhatsApp auth
    creds_dir = cfg.get_credentials_dir() / "whatsapp"
    if creds_dir.is_dir() and any(creds_dir.iterdir()):
        table.add_row("WhatsApp", "[green]Paired[/]")
    else:
        table.add_row("WhatsApp", "[yellow]Not paired[/]")

    # Port status
    port = cfg.stream_port
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", port))
        table.add_row("Port Status", f"[green]{port} available[/]")
    except OSError:
        table.add_row("Port Status", f"[yellow]{port} in use[/]")

    # Extras
    if cfg.installed_extras:
        table.add_row("Extras", ", ".join(cfg.installed_extras))
    else:
        table.add_row("Extras", "[dim]None[/]")

    # Autostart
    if cfg.autostart_enabled:
        table.add_row("Autostart", "[green]Enabled[/]")
    else:
        table.add_row("Autostart", "[dim]Disabled[/]")

    console.print(table)
