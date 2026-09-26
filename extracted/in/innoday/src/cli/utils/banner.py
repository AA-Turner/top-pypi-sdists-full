"""
Shared banner utilities for InnoDay CLI.
"""

from rich.console import Console
from rich.panel import Panel

from src.cli.utils.messages import get_random_message
from src.cli.utils.presentation import make_console
from src.version import get_display_version


def show_welcome_banner(console: Console = None, title: str = "InnoDay"):
    """Display the welcome banner with version and tagline."""
    if console is None:
        console = make_console()

    version = get_display_version()
    tagline = get_random_message()

    banner_text = f"""[header]Welcome to {title} {version}![/header]

AI-Powered Team Orchestration Platform

[italic]{tagline}[/italic]"""

    # The rocket belongs to the command header, which is printed above
    # this panel; a second one in the title is the same mark spent twice.
    banner = Panel(banner_text, title=title, border_style="header")

    console.print(banner)
    console.print()
