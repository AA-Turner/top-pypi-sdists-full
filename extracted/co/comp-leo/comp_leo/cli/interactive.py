"""Interactive CLI mode for Comp-LEO."""

import os
import sys
from pathlib import Path
from typing import Optional
import readline  # For input history

from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.panel import Panel
from rich import box

from comp_leo.analyzer.checker import ComplianceChecker
from comp_leo.cli.formatters import format_violations, format_summary
from comp_leo.cli.banner import print_welcome_interactive

console = Console()

class InteractiveSession:
    """Interactive CLI session manager."""
    
    def __init__(self):
        self.checker = ComplianceChecker(policy_pack="aleo-baseline")
        self.current_file = None
        self.last_result = None
        self.history = []
        
    def run(self):
        """Start interactive session."""
        print_welcome_interactive()
        
        while True:
            try:
                command = Prompt.ask("[bold cyan]comp-leo[/bold cyan]", default="help")
                command = command.strip()
                
                if not command:
                    continue
                
                self.history.append(command)
                
                if command in ["exit", "quit", "q"]:
                    console.print("[yellow]👋 Goodbye![/yellow]")
                    break
                elif command == "help":
                    self.show_help()
                elif command.startswith("check "):
                    path = command[6:].strip()
                    self.check_file(path)
                elif command.startswith("load "):
                    path = command[5:].strip()
                    self.load_file(path)
                elif command == "info":
                    self.show_info()
                elif command == "violations":
                    self.show_violations()
                elif command == "stats":
                    self.show_stats()
                elif command == "policies":
                    self.list_policies()
                elif command.startswith("policy "):
                    policy = command[7:].strip()
                    self.set_policy(policy)
                elif command == "clear":
                    os.system('clear' if os.name != 'nt' else 'cls')
                    print_welcome_interactive()
                elif command == "history":
                    self.show_history()
                else:
                    console.print(f"[red]Unknown command: {command}[/red]")
                    console.print("[dim]Type 'help' for available commands[/dim]")
                    
            except KeyboardInterrupt:
                console.print("\n[yellow]Use 'exit' to quit[/yellow]")
            except EOFError:
                break
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
    
    def show_help(self):
        """Show help menu."""
        table = Table(title="Available Commands", box=box.ROUNDED, border_style="cyan")
        table.add_column("Command", style="cyan", no_wrap=True)
        table.add_column("Description", style="white")
        table.add_column("Example", style="dim")
        
        commands = [
            ("check <path>", "Check Leo file or directory", "check main.leo"),
            ("load <path>", "Load file for inspection", "load program.leo"),
            ("info", "Show current file info", "info"),
            ("violations", "Show violations from last check", "violations"),
            ("stats", "Show statistics", "stats"),
            ("policies", "List available policy packs", "policies"),
            ("policy <name>", "Switch policy pack", "policy nist-800-53"),
            ("history", "Show command history", "history"),
            ("clear", "Clear screen", "clear"),
            ("help", "Show this help", "help"),
            ("exit", "Exit interactive mode", "exit"),
        ]
        
        for cmd, desc, example in commands:
            table.add_row(cmd, desc, example)
        
        console.print(table)
        console.print()
    
    def check_file(self, path: str):
        """Check a Leo file."""
        path_obj = Path(path)
        
        if not path_obj.exists():
            console.print(f"[red]File not found: {path}[/red]")
            return
        
        console.print(f"[cyan]🔍 Checking {path}...[/cyan]\n")
        
        try:
            result = self.checker.check_file(str(path_obj))
            self.last_result = result
            self.current_file = path
            
            if result.violations:
                console.print(format_violations(result.violations[:10], verbose=False))
                if len(result.violations) > 10:
                    console.print(f"[dim]... and {len(result.violations) - 10} more. Type 'violations' to see all.[/dim]\n")
            
            console.print(format_summary(result))
            
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
    
    def load_file(self, path: str):
        """Load a file for inspection."""
        path_obj = Path(path)
        
        if not path_obj.exists():
            console.print(f"[red]File not found: {path}[/red]")
            return
        
        try:
            program = self.checker.parser.parse_file(str(path_obj))
            self.current_file = path
            
            console.print(Panel(
                f"[bold]Loaded: {program.name}.aleo[/bold]\n"
                f"Lines: {program.end_line}\n"
                f"Transitions: {len(program.transitions)}\n"
                f"Functions: {len(program.functions)}\n"
                f"Structs: {len(program.structs)}\n"
                f"Mappings: {len(program.mappings)}",
                title="📄 Program Info",
                border_style="green"
            ))
            
        except Exception as e:
            console.print(f"[red]Error loading file: {e}[/red]")
    
    def show_info(self):
        """Show current file info."""
        if not self.current_file:
            console.print("[yellow]No file loaded. Use 'load <path>' or 'check <path>'[/yellow]")
            return
        
        try:
            program = self.checker.parser.parse_file(self.current_file)
            
            console.print(f"\n[bold cyan]Current File:[/bold cyan] {self.current_file}")
            console.print(f"[bold]Program:[/bold] {program.name}.aleo")
            console.print(f"[bold]Lines:[/bold] {program.end_line}\n")
            
            # Transitions
            if program.transitions:
                console.print("[bold]Transitions:[/bold]")
                for t in program.transitions:
                    console.print(f"  • {t.name} ({len(t.parameters)} params)")
            
            # Structs
            if program.structs:
                console.print("\n[bold]Structs:[/bold]")
                for s in program.structs:
                    console.print(f"  • {s.name} ({len(s.fields)} fields)")
            
            # Mappings
            if program.mappings:
                console.print("\n[bold]Mappings:[/bold]")
                for m in program.mappings:
                    console.print(f"  • {m.name}: {m.key_type} => {m.value_type}")
            
            console.print()
            
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
    
    def show_violations(self):
        """Show all violations from last check."""
        if not self.last_result:
            console.print("[yellow]No check results. Use 'check <path>' first[/yellow]")
            return
        
        if not self.last_result.violations:
            console.print("[green]✓ No violations found![/green]")
            return
        
        console.print(format_violations(self.last_result.violations, verbose=True))
    
    def show_stats(self):
        """Show statistics."""
        if not self.last_result:
            console.print("[yellow]No check results. Use 'check <path>' first[/yellow]")
            return
        
        table = Table(title="Check Statistics", box=box.ROUNDED)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="white", justify="right")
        
        table.add_row("Score", f"{self.last_result.score}/100")
        table.add_row("Total Checks", str(self.last_result.total_checks))
        table.add_row("Passed", str(self.last_result.total_checks - len(self.last_result.violations)))
        table.add_row("Failed", str(len(self.last_result.violations)))
        table.add_row("Critical", str(self.last_result.critical_count), style="red" if self.last_result.critical_count > 0 else "white")
        table.add_row("High", str(self.last_result.high_count), style="yellow" if self.last_result.high_count > 0 else "white")
        table.add_row("Medium", str(self.last_result.medium_count))
        table.add_row("Low", str(self.last_result.low_count))
        
        console.print(table)
        console.print()
    
    def list_policies(self):
        """List available policy packs."""
        policies = [
            ("aleo-baseline", "Core Leo security best practices", "✓ Active" if self.checker.policy_pack == "aleo-baseline" else ""),
            ("nist-800-53", "Federal security controls", "Coming soon"),
            ("iso-27001", "Information security", "Coming soon"),
            ("pci-dss", "Payment card security", "Coming soon"),
            ("gdpr", "Data protection & privacy", "Coming soon"),
        ]
        
        table = Table(title="Policy Packs", box=box.ROUNDED)
        table.add_column("ID", style="cyan")
        table.add_column("Description", style="white")
        table.add_column("Status", style="dim")
        
        for policy_id, desc, status in policies:
            table.add_row(policy_id, desc, status)
        
        console.print(table)
        console.print()
    
    def set_policy(self, policy: str):
        """Set active policy pack."""
        if policy == "aleo-baseline":
            self.checker = ComplianceChecker(policy_pack=policy)
            console.print(f"[green]✓ Switched to policy: {policy}[/green]")
        else:
            console.print(f"[yellow]Policy '{policy}' not yet implemented. Using 'aleo-baseline'[/yellow]")
    
    def show_history(self):
        """Show command history."""
        if not self.history:
            console.print("[dim]No command history yet[/dim]")
            return
        
        console.print("[bold]Command History:[/bold]")
        for i, cmd in enumerate(self.history[-20:], 1):  # Last 20
            console.print(f"  {i}. {cmd}")
        console.print()

def start_interactive():
    """Start interactive mode."""
    session = InteractiveSession()
    session.run()
