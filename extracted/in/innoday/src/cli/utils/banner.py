"""
Shared banner utilities for InnoDay CLI.
"""

from rich.console import Console
from rich.panel import Panel

from src.cli.utils.messages import get_random_message
from src.version import get_display_version


def show_welcome_banner(console: Console = None, title: str = "InnoDay"):
    """Display the welcome banner with version and tagline."""
    if console is None:
        console = Console()

    version = get_display_version()
    tagline = get_random_message()

    banner_text = f"""[bold cyan]Welcome to {title} {version}![/bold cyan]

AI-Powered Team Orchestration Platform

[italic]{tagline}[/italic]"""

    banner = Panel(banner_text, title=f"🚀 {title}", border_style="cyan")

    console.print(banner)
    console.print()
