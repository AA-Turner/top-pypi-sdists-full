"""ASCII banner and branding for Comp-LEO CLI."""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box

BANNER = r"""
  ██████╗ ██████╗ ███╗   ███╗██████╗       ██╗     ███████╗ ██████╗ 
 ██╔════╝██╔═══██╗████╗ ████║██╔══██╗      ██║     ██╔════╝██╔═══██╗
 ██║     ██║   ██║██╔████╔██║██████╔╝█████╗██║     █████╗  ██║   ██║
 ██║     ██║   ██║██║╚██╔╝██║██╔═══╝ ╚════╝██║     ██╔══╝  ██║   ██║
 ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║           ███████╗███████╗╚██████╔╝
  ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝           ╚══════╝╚══════╝ ╚═════╝ 
"""

TAGLINE = "Compliance & Security for Leo Smart Contracts"
VERSION_INFO = "v0.3.0 | Zero-Knowledge Compliance | 100% Local | PCI-DSS"

def print_banner(console: Console = None):
    """Print the Comp-LEO banner."""
    if console is None:
        console = Console()
    
    # Create gradient effect
    banner_text = Text()
    lines = BANNER.strip().split('\n')
    
    # Gradient colors: cyan -> blue
    colors = ["cyan", "bright_cyan", "blue", "bright_blue", "blue", "cyan"]
    
    for i, line in enumerate(lines):
        color = colors[i % len(colors)]
        banner_text.append(line + "\n", style=color)
    
    console.print(banner_text)
    console.print(f"[dim]{TAGLINE}[/dim]")
    console.print(f"[dim]{VERSION_INFO}[/dim]\n")

def print_compact_banner(console: Console = None):
    """Print compact banner for non-interactive mode."""
    if console is None:
        console = Console()
    
    console.print(Panel(
        "[bold cyan]COMP-LEO SDK[/bold cyan] v0.3.0\n"
        "[dim]Compliance & Security for Leo Smart Contracts[/dim]",
        box=box.ROUNDED,
        border_style="cyan",
        padding=(0, 2)
    ))

def print_welcome_interactive():
    """Print interactive mode welcome."""
    console = Console()
    print_banner(console)
    
    console.print("━" * 70, style="dim")
    console.print("[bold green]🚀 Interactive Mode[/bold green]")
    console.print("[dim]Type 'help' for commands, 'exit' to quit[/dim]\n")
