"""Comp-LEO CLI - Command-line interface for compliance checks."""

import sys
import json
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.syntax import Syntax

from comp_leo import __version__
from comp_leo.analyzer.checker import ComplianceChecker
from comp_leo.cli.formatters import format_violations, format_summary, format_report
from comp_leo.cli.banner import print_banner, print_compact_banner
from comp_leo.cli.interactive import start_interactive
from comp_leo.core.models import CheckResult, Severity


console = Console()


@click.group(invoke_without_command=True)
@click.version_option(version="0.1.2")
@click.option('--interactive', '-i', is_flag=True, help='Start interactive menu mode')
@click.option('--classic', is_flag=True, help='Use classic command-based interactive mode')
@click.pass_context
def cli(ctx, interactive, classic):
    """Comp-LEO: Compliance & Security SDK for Leo Smart Contracts."""
    if interactive:
        # Try menu mode first, fall back to classic
        try:
            from comp_leo.cli.interactive_menu import start_interactive_menu
            start_interactive_menu()
        except ImportError:
            start_interactive()
        ctx.exit()
    elif classic:
        start_interactive()
        ctx.exit()
    elif ctx.invoked_subcommand is None:
        print_banner()
        click.echo("Use --help for available commands or --interactive for interactive mode")
    pass


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--policy', '-p', default='aleo-baseline', help='Policy pack to use')
@click.option('--threshold', '-t', default=75, type=int, help='Minimum passing score (0-100)')
@click.option('--fail-on-high', is_flag=True, help='Fail if any HIGH severity violations found')
@click.option('--fail-on-critical', is_flag=True, default=True, help='Fail if any CRITICAL violations found (default: true)')
@click.option('--output', '-o', type=click.Path(), help='Write results to JSON file')
@click.option('--quiet', '-q', is_flag=True, help='Only show summary')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed output')
def check(
    path: str,
    policy: str,
    threshold: int,
    fail_on_high: bool,
    fail_on_critical: bool,
    output: Optional[str],
    quiet: bool,
    verbose: bool
):
    """
    Run compliance checks on Leo source code.
    
    PATH can be a .leo file or directory containing Leo programs.
    
    Examples:
    
        # Check a single file
        comp-leo check programs/my_contract/src/main.leo
        
        # Check entire directory with PCI-DSS policy
        comp-leo check programs/payment/ --policy pci-dss
        
        # Fail on any HIGH severity issues
        comp-leo check programs/ --fail-on-high
        
        # Generate JSON report
        comp-leo check programs/ --output report.json
    """
    
    print_compact_banner(console)
    console.print(f"Policy: [cyan]{policy}[/cyan] | Threshold: [cyan]{threshold}[/cyan]\n")
    
    # Initialize checker
    try:
        checker = ComplianceChecker(policy_pack=policy)
    except Exception as e:
        console.print(f"[bold red]Error loading policy pack:[/bold red] {e}", style="red")
        sys.exit(1)
    
    # Run checks
    path_obj = Path(path)
    
    try:
        with console.status("[bold green]Analyzing Leo code..."):
            if path_obj.is_file():
                result = checker.check_file(str(path_obj), threshold=threshold)
            else:
                result = checker.check_directory(str(path_obj), threshold=threshold)
    except Exception as e:
        console.print(f"[bold red]Analysis failed:[/bold red] {e}", style="red")
        if verbose:
            import traceback
            console.print(traceback.format_exc())
        sys.exit(1)
    
    # Display results
    if not quiet:
        _display_results(result, verbose)
    else:
        _display_summary(result)
    
    # Write output file
    if output:
        with open(output, 'w') as f:
            json.dump(result.model_dump(mode='json'), f, indent=2, default=str)
        console.print(f"\n[dim]Results written to {output}[/dim]")
    
    # Determine exit code
    should_fail = False
    
    if not result.passed:
        should_fail = True
    
    if fail_on_critical and result.critical_count > 0:
        should_fail = True
    
    if fail_on_high and result.high_count > 0:
        should_fail = True
    
    if should_fail:
        sys.exit(1)
    else:
        sys.exit(0)


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--policy', '-p', default='aleo-baseline', help='Policy pack to use')
@click.option('--format', '-f', type=click.Choice(['json', 'html', 'markdown']), default='json', help='Report format')
@click.option('--output', '-o', type=click.Path(), required=True, help='Output file path')
def report(path: str, policy: str, format: str, output: str):
    """
    Generate compliance audit report.
    
    Creates a comprehensive audit report with evidence artifacts
    for regulatory reviews and partner due diligence.
    
    Examples:
    
        # Generate JSON audit report
        comp-leo report programs/ -o audit-report.json
        
        # Generate HTML report for stakeholders
        comp-leo report programs/ --format html -o report.html
    """
    
    console.print(f"\n[bold cyan]Generating Audit Report[/bold cyan]")
    console.print(f"Policy: [cyan]{policy}[/cyan] | Format: [cyan]{format}[/cyan]\n")
    
    # Run checks
    checker = ComplianceChecker(policy_pack=policy)
    
    path_obj = Path(path)
    
    with console.status("[bold green]Analyzing and generating report..."):
        if path_obj.is_file():
            result = checker.check_file(str(path_obj))
        else:
            result = checker.check_directory(str(path_obj))
    
    # Generate report based on format
    if format == 'json':
        _generate_json_report(result, output)
    elif format == 'html':
        _generate_html_report(result, output)
    elif format == 'markdown':
        _generate_markdown_report(result, output)
    
    console.print(f"\n[bold green]✓[/bold green] Report generated: [cyan]{output}[/cyan]")


@cli.command()
def list_policies():
    """List available policy packs."""
    
    policies_dir = Path(__file__).parent.parent / "policies"
    policy_files = list(policies_dir.glob("*.json"))
    
    if not policy_files:
        console.print("[yellow]No policy packs found[/yellow]")
        return
    
    table = Table(title="Available Policy Packs", box=box.ROUNDED)
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="green")
    table.add_column("Frameworks", style="yellow")
    
    for policy_file in policy_files:
        with open(policy_file, 'r') as f:
            policy_data = json.load(f)
        
        table.add_row(
            policy_data.get("id", ""),
            policy_data.get("name", ""),
            ", ".join(policy_data.get("frameworks", []))
        )
    
    console.print(table)


def _display_results(result: CheckResult, verbose: bool):
    """Display check results with Rich formatting."""
    
    # Violations
    if result.violations:
        console.print(format_violations(result.violations, verbose))
    else:
        console.print(Panel(
            "[bold green]✓ No violations found![/bold green]",
            box=box.ROUNDED,
            style="green"
        ))
    
    # Summary
    console.print(format_summary(result))


def _display_summary(result: CheckResult):
    """Display compact summary."""
    
    if result.passed:
        icon = "✅"
        color = "green"
        status = "PASSED"
    else:
        icon = "❌"
        color = "red"
        status = "FAILED"
    
    console.print(
        f"\n{icon} [bold {color}]{status}[/bold {color}] | "
        f"Score: {result.score}/{result.threshold} | "
        f"Violations: {len(result.violations)} "
        f"(🔴 {result.critical_count} ⚠️ {result.high_count})"
    )


def _generate_json_report(result: CheckResult, output_path: str):
    """Generate JSON audit report."""
    
    from comp_leo.core.models import AuditReport
    import uuid
    
    report = AuditReport(
        report_id=str(uuid.uuid4()),
        project_name=Path(result.scanned_files[0]).parent.name if result.scanned_files else "unknown",
        policy_pack=result.policy_pack,
        results=result,
        sdk_version=__version__
    )
    
    with open(output_path, 'w') as f:
        json.dump(report.model_dump(mode='json'), f, indent=2, default=str)


def _generate_html_report(result: CheckResult, output_path: str):
    """Generate HTML audit report."""
    
    html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Comp-LEO Audit Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .header {{ background: #1e3a8a; color: white; padding: 20px; border-radius: 8px; }}
        .summary {{ display: flex; gap: 20px; margin: 20px 0; }}
        .metric {{ background: #f3f4f6; padding: 15px; border-radius: 8px; flex: 1; }}
        .violation {{ border-left: 4px solid #ef4444; padding: 15px; margin: 10px 0; background: #fef2f2; }}
        .critical {{ border-color: #dc2626; background: #fee2e2; }}
        .high {{ border-color: #f59e0b; background: #fef3c7; }}
        .medium {{ border-color: #3b82f6; background: #dbeafe; }}
        .low {{ border-color: #10b981; background: #d1fae5; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Compliance Audit Report</h1>
        <p>Policy: {result.policy_pack} | Score: {result.score}/100</p>
    </div>
    
    <div class="summary">
        <div class="metric">
            <h3>Total Checks</h3>
            <p style="font-size: 2em;">{result.total_checks}</p>
        </div>
        <div class="metric">
            <h3>Violations</h3>
            <p style="font-size: 2em;">{len(result.violations)}</p>
        </div>
        <div class="metric">
            <h3>Pass Rate</h3>
            <p style="font-size: 2em;">{int((result.passed_checks / result.total_checks) * 100) if result.total_checks > 0 else 0}%</p>
        </div>
    </div>
    
    <h2>Violations</h2>
"""
    
    for v in result.violations:
        html_template += f"""
    <div class="violation {v.severity.value}">
        <h3>{v.rule_name}</h3>
        <p><strong>Severity:</strong> {v.severity.value.upper()}</p>
        <p><strong>File:</strong> {v.file_path}:{v.line_number}</p>
        <p>{v.message}</p>
    </div>
"""
    
    html_template += """
</body>
</html>
"""
    
    with open(output_path, 'w') as f:
        f.write(html_template)


def _generate_markdown_report(result: CheckResult, output_path: str):
    """Generate Markdown audit report."""
    
    md = f"""# Compliance Audit Report

**Policy Pack:** {result.policy_pack}  
**Score:** {result.score}/100  
**Status:** {"✅ PASSED" if result.passed else "❌ FAILED"}

## Summary

- **Total Checks:** {result.total_checks}
- **Passed:** {result.passed_checks}
- **Failed:** {result.failed_checks}
- **Critical:** {result.critical_count}
- **High:** {result.high_count}
- **Medium:** {result.medium_count}
- **Low:** {result.low_count}

## Violations

"""
    
    for v in result.violations:
        md += f"""### {v.rule_name}

**Severity:** {v.severity.value.upper()}  
**Location:** `{v.file_path}:{v.line_number}`  
**Message:** {v.message}

"""
        
        if v.remediation:
            md += f"**Remediation:** {v.remediation.description}\n\n"
    
    with open(output_path, 'w') as f:
        f.write(md)


@cli.command(name='init-ci')
@click.option('--provider', type=click.Choice(['github', 'gitlab', 'all']), default='all', help='CI/CD provider')
@click.option('--output-dir', default='.', help='Output directory')
def init_ci(provider, output_dir):
    """
    Generate CI/CD configuration files.
    
    Examples:
        comp-leo init-ci
        comp-leo init-ci --provider github
    """
    from comp_leo.cli.ci_generator import generate_github_actions, generate_gitlab_ci, generate_pre_commit_hook, generate_all
    
    console.print("\n[bold cyan]🔧 Generating CI/CD Configuration[/bold cyan]\n")
    
    if provider == 'github':
        generate_github_actions(output_dir)
    elif provider == 'gitlab':
        generate_gitlab_ci(output_dir)
    else:
        generate_all(output_dir)
    
    console.print("\n[green]✅ CI/CD configuration generated![/green]")
    console.print("[dim]Commit these files to enable automated compliance checks[/dim]\n")


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--policy', '-p', default='aleo-baseline', help='Policy pack to use')
def watch(path, policy):
    """
    Watch Leo files for changes and run checks automatically.
    
    Examples:
        comp-leo watch programs/
        comp-leo watch main.leo --policy nist-800-53
    """
    try:
        from comp_leo.cli.watch import watch_directory
    except ImportError:
        console.print("[red]Watch mode requires 'watchdog' package[/red]")
        console.print("[dim]Install: pip install comp-leo[watch][/dim]")
        sys.exit(1)
    
    watch_directory(path, policy)


@cli.command()
@click.argument('violation_id', required=False)
def fix(violation_id):
    """
    Preview auto-fix suggestions for violations.
    
    Examples:
        comp-leo fix                    # Show all fixable violations
        comp-leo fix input-validation   # Preview specific fix
    """
    from comp_leo.cli.autofix import batch_fix_suggestions, get_fix_confidence
    
    console.print("\n[bold yellow]🔧 Auto-Fix Preview (Template-based)[/bold yellow]")
    console.print("[dim]AI-powered fixes coming in v0.4.0+[/dim]\n")
    
    # This is a placeholder - in real use, would load violations from last check
    console.print("[yellow]Run 'comp-leo check' first to detect violations[/yellow]")
    console.print("[dim]Then use 'comp-leo fix' to preview fixes[/dim]\n")


if __name__ == '__main__':
    cli()
