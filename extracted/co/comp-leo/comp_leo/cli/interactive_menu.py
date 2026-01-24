"""Menu-based interactive CLI mode for Comp-LEO."""

import os
import sys
from pathlib import Path
from typing import Optional

try:
    import questionary
    from questionary import Style
    HAS_QUESTIONARY = True
    
    # Custom style for menu (only if questionary is available)
    custom_style = Style([
        ('qmark', 'fg:#673ab7 bold'),       # Question mark
        ('question', 'bold'),                # Question text
        ('answer', 'fg:#00bcd4 bold'),      # Selected answer
        ('pointer', 'fg:#673ab7 bold'),     # Pointer
        ('highlighted', 'fg:#00bcd4 bold'), # Highlighted choice
        ('selected', 'fg:#00bcd4'),         # Selected choice
        ('separator', 'fg:#cc5454'),        # Separator
        ('instruction', ''),                 # Instructions
        ('text', ''),                        # Plain text
        ('disabled', 'fg:#858585 italic')   # Disabled choices
    ])
except ImportError:
    HAS_QUESTIONARY = False
    custom_style = None

from rich.console import Console
from rich.panel import Panel
from rich import box

from comp_leo.analyzer.checker import ComplianceChecker
from comp_leo.cli.formatters import format_violations, format_summary
from comp_leo.cli.banner import print_banner

console = Console()


def scan_for_leo_files(max_depth=3):
    """Scan for Leo files in current and nearby directories."""
    leo_files = []
    search_paths = [
        Path.cwd(),
        Path.cwd().parent,
        Path.cwd() / "programs",
        Path.cwd().parent / "programs",
    ]
    
    for search_path in search_paths:
        if not search_path.exists():
            continue
        
        try:
            # Find .leo files (limited depth to avoid huge scans)
            for leo_file in search_path.rglob("*.leo"):
                # Skip if too deep
                try:
                    relative = leo_file.relative_to(Path.cwd())
                    depth = len(relative.parents)
                    if depth <= max_depth:
                        leo_files.append(leo_file)
                except ValueError:
                    # File is outside cwd, use absolute path
                    try:
                        relative = leo_file.relative_to(search_path)
                        if len(relative.parents) <= 2:
                            leo_files.append(leo_file)
                    except:
                        pass
        except:
            continue
    
    # Remove duplicates and sort
    unique_files = list(set(leo_files))
    unique_files.sort()
    
    return unique_files[:50]  # Limit to 50 files


def quick_check_file(checker, file_path):
    """Quickly check a file and display results."""
    console.print(f"\n[cyan]🔍 Checking {file_path.name}...[/cyan]\n")
    
    try:
        result = checker.check_file(str(file_path))
        
        if result.violations:
            console.print(format_violations(result.violations[:5], verbose=False))
            if len(result.violations) > 5:
                console.print(f"[dim]... and {len(result.violations) - 5} more. Select 'View Last Results' to see all.[/dim]\n")
        else:
            console.print("[green]✓ No violations found![/green]\n")
        
        console.print(format_summary(result))
        console.print()
        
        return result
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]\n")
        return None


def check_from_scanned_files(checker, leo_files):
    """Let user select from all scanned files."""
    if not leo_files:
        console.print("[yellow]No Leo files found. Use 'Browse & Check File' to specify path.[/yellow]\n")
        return None
    
    # Create display names
    choices = []
    for f in leo_files:
        try:
            display = str(f.relative_to(Path.cwd()))
        except ValueError:
            display = str(f)
        
        if len(display) > 70:
            display = "..." + display[-67:]
        
        choices.append(display)
    
    choices.append("← Back")
    
    selected = questionary.select(
        f"Select a Leo file to check ({len(leo_files)} files):",
        choices=choices,
        style=custom_style
    ).ask()
    
    if not selected or selected == "← Back":
        return None
    
    # Find the actual file
    selected_clean = selected.replace("...", "")
    matching = [f for f in leo_files if str(f).endswith(selected_clean.strip())]
    
    if matching:
        return quick_check_file(checker, matching[0])
    
    return None


def start_interactive_menu():
    """Start menu-based interactive mode."""
    
    if not HAS_QUESTIONARY:
        console.print("[yellow]Menu mode requires 'questionary' package[/yellow]")
        console.print("[dim]Install: pip install questionary[/dim]")
        console.print("\n[cyan]Falling back to command mode. Type 'help' for commands.[/cyan]")
        from comp_leo.cli.interactive import start_interactive
        start_interactive()
        return
    
    print_banner()
    console.print("━" * 70, style="dim")
    console.print("[bold green]📋 Interactive Menu Mode[/bold green]")
    console.print("[dim]Use arrow keys to navigate, Enter to select[/dim]\n")
    
    # Scan for Leo files in current directory and parent
    console.print("[dim]🔍 Scanning for Leo files...[/dim]")
    leo_files = scan_for_leo_files()
    
    if leo_files:
        console.print(f"[dim]✓ Found {len(leo_files)} Leo file(s)[/dim]\n")
    else:
        console.print("[dim]No Leo files found in current directory[/dim]\n")
    
    checker = ComplianceChecker(policy_pack="aleo-baseline")
    current_file = None
    last_result = None
    
    while True:
        try:
            # Build dynamic menu based on available files
            menu_choices = []
            
            # Add quick access to found Leo files
            if leo_files:
                menu_choices.append("─── Quick Check ───")
                for f in leo_files[:5]:  # Show top 5
                    display_path = str(f)
                    if len(display_path) > 50:
                        display_path = "..." + display_path[-47:]
                    menu_choices.append(f"  ✓ {display_path}")
                
                if len(leo_files) > 5:
                    menu_choices.append(f"  ... and {len(leo_files) - 5} more files")
                
                menu_choices.append("─── More Options ───")
            
            # Standard options
            menu_choices.extend([
                "🔍 Browse & Check File",
                "📁 Check Directory",
                "🔄 Rescan for Leo Files",
            ])
            
            if last_result:
                menu_choices.extend([
                    "📊 View Last Results",
                    "📈 Show Statistics",
                    "💾 Export Report",
                ])
            
            menu_choices.extend([
                "📋 List Available Policies",
                "🔧 Change Policy Pack",
                "❓ Help",
                "❌ Exit"
            ])
            
            # Main menu
            action = questionary.select(
                "What would you like to do?",
                choices=menu_choices,
                style=custom_style,
                qmark="›",
                pointer="▸"
            ).ask()
            
            if action is None or "Exit" in action:
                console.print("\n[yellow]👋 Goodbye![/yellow]\n")
                break
            
            # Handle separator lines
            elif action.startswith("───"):
                continue
            
            # Quick check from scanned files
            elif action.startswith("  ✓ "):
                file_path = action.replace("  ✓ ", "").replace("...", "")
                # Find matching file
                matching = [f for f in leo_files if str(f).endswith(file_path.strip())]
                if matching:
                    result = quick_check_file(checker, matching[0])
                    if result:
                        last_result = result
                        current_file = str(matching[0])
            
            elif "... and" in action:
                # Show all files for selection
                result = check_from_scanned_files(checker, leo_files)
                if result:
                    last_result = result
            
            elif "Browse & Check File" in action:
                result = check_file_menu(checker)
                if result:
                    last_result = result
                
            elif "Check Directory" in action:
                result = check_directory_menu(checker)
                if result:
                    last_result = result
            
            elif "Rescan for Leo Files" in action:
                console.print("\n[dim]🔍 Rescanning...[/dim]")
                leo_files = scan_for_leo_files()
                console.print(f"[green]✓ Found {len(leo_files)} Leo file(s)[/green]\n")
                
            elif "View Last Results" in action:
                show_last_results(last_result)
                
            elif "Show Statistics" in action:
                show_statistics(last_result)
                
            elif "List Available Policies" in action:
                list_policies()
                
            elif "Change Policy Pack" in action:
                checker = change_policy_menu(checker)
                
            elif "Export Report" in action:
                export_report_menu(last_result)
                
            elif "Show Current File Info" in action:
                show_current_file_info(current_file, checker)
                
            elif "Help" in action:
                show_help()
                
        except KeyboardInterrupt:
            console.print("\n[yellow]Use Exit option to quit[/yellow]")
            continue
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            continue


def check_file_menu(checker):
    """Check a single Leo file."""
    path = questionary.text(
        "Enter path to Leo file or directory:",
        default=".",
        style=custom_style
    ).ask()
    
    if not path:
        return None
    
    path_obj = Path(path)
    
    if not path_obj.exists():
        console.print(f"[red]File not found: {path}[/red]\n")
        return None
    
    # If directory, list files
    if path_obj.is_dir():
        leo_files = list(path_obj.rglob("*.leo"))
        if not leo_files:
            console.print(f"[yellow]No .leo files found in {path}[/yellow]\n")
            return None
        
        file_choices = []
        for f in leo_files[:30]:
            try:
                display = str(f.relative_to(path_obj))
            except ValueError:
                display = f.name
            file_choices.append(display)
        
        if len(leo_files) > 30:
            file_choices.append(f"← Show all {len(leo_files)} files")
        
        file_choices.append("← Back")
        
        selected = questionary.select(
            f"Select a file to check ({len(leo_files)} files found):",
            choices=file_choices,
            style=custom_style
        ).ask()
        
        if not selected or selected == "← Back":
            return None
        elif selected.startswith("← Show all"):
            return check_from_scanned_files(checker, leo_files)
        else:
            path_obj = path_obj / selected
    
    return quick_check_file(checker, path_obj)


def check_directory_menu(checker):
    """Check all Leo files in directory."""
    path = questionary.text(
        "Enter directory path:",
        default=".",
        style=custom_style
    ).ask()
    
    if not path:
        return None
    
    path_obj = Path(path)
    
    if not path_obj.exists() or not path_obj.is_dir():
        console.print(f"[red]Directory not found: {path}[/red]\n")
        return None
    
    console.print(f"\n[cyan]🔍 Scanning {path}...[/cyan]\n")
    
    try:
        result = checker.check_directory(str(path_obj))
        
        if result.violations:
            console.print(format_violations(result.violations[:10], verbose=False))
            if len(result.violations) > 10:
                console.print(f"[dim]... and {len(result.violations) - 10} more. Select 'View Last Results' to see all.[/dim]\n")
        else:
            console.print("[green]✓ No violations found![/green]\n")
        
        console.print(format_summary(result))
        console.print()
        
        return result
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]\n")
        return None


def show_last_results(last_result):
    """Show violations from last check."""
    if not last_result:
        console.print("[yellow]No previous check results. Run a check first.[/yellow]\n")
        return
    
    if not last_result.violations:
        console.print("[green]✓ No violations in last check![/green]\n")
        return
    
    console.print(format_violations(last_result.violations, verbose=True))
    console.print()


def show_statistics(last_result):
    """Show detailed statistics."""
    if not last_result:
        console.print("[yellow]No previous check results. Run a check first.[/yellow]\n")
        return
    
    from rich.table import Table
    
    table = Table(title="Check Statistics", box=box.ROUNDED, border_style="cyan")
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value", style="white", justify="right")
    
    table.add_row("Score", f"{last_result.score}/100")
    table.add_row("Total Checks", str(last_result.total_checks))
    table.add_row("Passed", str(last_result.passed_checks))
    table.add_row("Failed", str(last_result.failed_checks))
    table.add_row("", "")
    table.add_row("Critical", str(last_result.critical_count), style="red" if last_result.critical_count > 0 else "white")
    table.add_row("High", str(last_result.high_count), style="yellow" if last_result.high_count > 0 else "white")
    table.add_row("Medium", str(last_result.medium_count))
    table.add_row("Low", str(last_result.low_count))
    table.add_row("", "")
    table.add_row("Duration", f"{last_result.scan_duration_ms:.1f}ms")
    
    console.print(table)
    console.print()


def list_policies():
    """List available policy packs."""
    from rich.table import Table
    
    policies = [
        ("aleo-baseline", "Core Leo security best practices", "✓ Available"),
        ("nist-800-53", "Federal security controls", "Coming in v0.2"),
        ("iso-27001", "Information security", "Coming in v0.2"),
        ("pci-dss", "Payment card security", "Coming in v0.3"),
        ("gdpr", "Data protection & privacy", "Coming in v0.3"),
    ]
    
    table = Table(title="Policy Packs", box=box.ROUNDED, border_style="cyan")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")
    table.add_column("Status", style="dim")
    
    for policy_id, desc, status in policies:
        table.add_row(policy_id, desc, status)
    
    console.print(table)
    console.print()


def change_policy_menu(checker):
    """Change the active policy pack."""
    policy = questionary.select(
        "Select policy pack:",
        choices=[
            "aleo-baseline (Default)",
            "nist-800-53 (Coming soon)",
            "iso-27001 (Coming soon)",
            "pci-dss (Coming soon)",
            "gdpr (Coming soon)"
        ],
        style=custom_style
    ).ask()
    
    if policy and "aleo-baseline" in policy:
        checker = ComplianceChecker(policy_pack="aleo-baseline")
        console.print(f"[green]✓ Switched to policy: aleo-baseline[/green]\n")
    else:
        console.print(f"[yellow]Policy not yet available. Using 'aleo-baseline'[/yellow]\n")
    
    return checker


def export_report_menu(last_result):
    """Export report in various formats."""
    if not last_result:
        console.print("[yellow]No results to export. Run a check first.[/yellow]\n")
        return
    
    format_choice = questionary.select(
        "Select export format:",
        choices=["JSON", "HTML", "Markdown", "Cancel"],
        style=custom_style
    ).ask()
    
    if not format_choice or format_choice == "Cancel":
        return
    
    format_map = {
        "JSON": "json",
        "HTML": "html",
        "Markdown": "markdown"
    }
    
    ext_map = {
        "JSON": ".json",
        "HTML": ".html",
        "Markdown": ".md"
    }
    
    default_name = f"compliance-report{ext_map[format_choice]}"
    
    filename = questionary.text(
        f"Save as:",
        default=default_name,
        style=custom_style
    ).ask()
    
    if not filename:
        return
    
    try:
        from comp_leo.cli.formatters import format_report
        content = format_report(last_result, format_map[format_choice])
        
        with open(filename, 'w') as f:
            f.write(content)
        
        console.print(f"[green]✓ Report saved to {filename}[/green]\n")
        
    except Exception as e:
        console.print(f"[red]Error saving report: {e}[/red]\n")


def show_current_file_info(current_file, checker):
    """Show information about current file."""
    if not current_file:
        console.print("[yellow]No file loaded. Check a file first.[/yellow]\n")
        return
    
    try:
        program = checker.parser.parse_file(current_file)
        
        console.print(Panel(
            f"[bold]Loaded: {program.name}.aleo[/bold]\n"
            f"Lines: {program.end_line}\n"
            f"Transitions: {len(program.transitions)}\n"
            f"Functions: {len(program.functions)}\n"
            f"Structs: {len(program.structs)}\n"
            f"Mappings: {len(program.mappings)}",
            title="📄 Program Info",
            border_style="green",
            box=box.ROUNDED
        ))
        console.print()
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]\n")


def show_help():
    """Show help information."""
    console.print(Panel(
        "[bold cyan]Comp-LEO Interactive Menu[/bold cyan]\n\n"
        "[bold]Navigation:[/bold]\n"
        "  • Use ↑↓ arrow keys to navigate menu\n"
        "  • Press Enter to select\n"
        "  • Press Ctrl+C to cancel\n\n"
        "[bold]Features:[/bold]\n"
        "  • Check individual Leo files\n"
        "  • Scan entire directories\n"
        "  • View detailed violation reports\n"
        "  • Export compliance reports\n"
        "  • Switch policy packs\n\n"
        "[bold]Commands:[/bold]\n"
        "  • comp-leo --interactive    (Menu mode)\n"
        "  • comp-leo check <path>     (Direct check)\n"
        "  • comp-leo --help           (Full help)",
        title="Help",
        border_style="cyan",
        box=box.ROUNDED
    ))
    console.print()
