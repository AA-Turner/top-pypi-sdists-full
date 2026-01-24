"""Watch mode for continuous compliance checking."""

import time
from pathlib import Path
from typing import Set
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent

from rich.console import Console
from rich.live import Live
from rich.panel import Panel

from comp_leo.analyzer.checker import ComplianceChecker
from comp_leo.cli.formatters import format_summary

console = Console()

class LeoFileHandler(FileSystemEventHandler):
    """Handler for Leo file changes."""
    
    def __init__(self, checker: ComplianceChecker, paths: Set[str]):
        self.checker = checker
        self.paths = paths
        self.last_check = {}
        
    def on_modified(self, event):
        """Handle file modification."""
        if event.is_directory:
            return
        
        path = Path(event.src_path)
        if path.suffix == '.leo':
            # Debounce: check if enough time has passed
            now = time.time()
            if path in self.last_check and now - self.last_check[path] < 2:
                return
            
            self.last_check[path] = now
            self.check_file(path)
    
    def check_file(self, path: Path):
        """Check a single file."""
        console.print(f"\n[cyan]🔍 Checking {path.name}...[/cyan]")
        
        try:
            result = self.checker.check_file(str(path))
            console.print(format_summary(result))
            
            if result.critical_count > 0:
                console.print("[red]⚠️  Critical issues found![/red]")
            elif result.passed:
                console.print("[green]✅ All checks passed[/green]")
            
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

def watch_directory(path: str, policy: str = "aleo-baseline"):
    """Watch directory for Leo file changes."""
    path_obj = Path(path)
    
    if not path_obj.exists():
        console.print(f"[red]Path not found: {path}[/red]")
        return
    
    checker = ComplianceChecker(policy_pack=policy)
    
    # Find all Leo files
    if path_obj.is_file():
        files = {path_obj}
    else:
        files = set(path_obj.rglob("*.leo"))
    
    console.print(Panel(
        f"[bold]👀 Watching {len(files)} Leo file(s)[/bold]\n"
        f"[dim]Path: {path}[/dim]\n"
        f"[dim]Press Ctrl+C to stop[/dim]",
        title="Watch Mode",
        border_style="cyan"
    ))
    
    # Create handler and observer
    event_handler = LeoFileHandler(checker, files)
    observer = Observer()
    observer.schedule(event_handler, str(path_obj), recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        console.print("\n[yellow]👋 Watch mode stopped[/yellow]")
    
    observer.join()
