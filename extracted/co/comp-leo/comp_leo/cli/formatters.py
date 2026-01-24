"""Output formatters for CLI display."""

from typing import List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from rich import box

from comp_leo.core.models import Violation, CheckResult, Severity


def format_violations(violations: List[Violation], verbose: bool = False) -> Panel:
    """Format violations for display."""
    
    # Group by severity
    by_severity = {
        Severity.CRITICAL: [],
        Severity.HIGH: [],
        Severity.MEDIUM: [],
        Severity.LOW: [],
        Severity.INFO: []
    }
    
    for v in violations:
        by_severity[v.severity].append(v)
    
    output_lines = []
    
    # Show violations by severity
    for severity in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW, Severity.INFO]:
        viols = by_severity[severity]
        if not viols:
            continue
        
        icon = _get_severity_icon(severity)
        color = _get_severity_color(severity)
        
        output_lines.append(f"\n[bold {color}]{icon} {severity.value.upper()}: {len(viols)} issue(s)[/bold {color}]")
        
        for v in viols:
            output_lines.append(f"\n  [bold]{v.rule_name}[/bold] [{v.violation_type.value}]")
            output_lines.append(f"  → {v.file_path}:{v.line_number}")
            output_lines.append(f"  {v.message}")
            
            # Show controls
            if verbose and v.controls:
                controls = ", ".join([f"{c.framework}:{c.control_id}" for c in v.controls])
                output_lines.append(f"  [dim]Controls: {controls}[/dim]")
            
            # Show remediation
            if v.remediation:
                output_lines.append(f"  [cyan]💡 {v.remediation.description}[/cyan]")
                if verbose and v.remediation.code_example:
                    output_lines.append(f"  [dim]{v.remediation.code_example}[/dim]")
    
    content = "\n".join(output_lines)
    
    return Panel(
        content,
        title=f"[bold red]⚠️  {len(violations)} Violation(s) Found[/bold red]",
        box=box.ROUNDED,
        border_style="red"
    )


def format_summary(result: CheckResult) -> Panel:
    """Format summary statistics."""
    
    # Build summary table
    table = Table(box=None, show_header=False, padding=(0, 2))
    
    table.add_row("✅ Passed", f"[green]{result.passed_checks}[/green]")
    table.add_row("⚠️  Failed", f"[red]{result.failed_checks}[/red]")
    table.add_row("", "")
    table.add_row("🔴 Critical", f"[bold red]{result.critical_count}[/bold red]")
    table.add_row("⚠️  High", f"[yellow]{result.high_count}[/yellow]")
    table.add_row("ℹ️  Medium", f"[cyan]{result.medium_count}[/cyan]")
    table.add_row("💬 Low", f"[dim]{result.low_count}[/dim]")
    table.add_row("", "")
    table.add_row("Score", f"[bold]{result.score}/100[/bold] (Threshold: {result.threshold})")
    
    if result.scan_duration_ms:
        table.add_row("Duration", f"{result.scan_duration_ms:.1f}ms")
    
    border_color = "green" if result.passed else "red"
    title = "[bold green]✓ PASSED[/bold green]" if result.passed else "[bold red]✗ FAILED[/bold red]"
    
    return Panel(
        table,
        title=title,
        box=box.DOUBLE,
        border_style=border_color
    )


def _get_severity_icon(severity: Severity) -> str:
    """Get icon for severity level."""
    icons = {
        Severity.CRITICAL: "🔴",
        Severity.HIGH: "⚠️ ",
        Severity.MEDIUM: "ℹ️ ",
        Severity.LOW: "💬",
        Severity.INFO: "📝"
    }
    return icons.get(severity, "•")


def _get_severity_color(severity: Severity) -> str:
    """Get color for severity level."""
    colors = {
        Severity.CRITICAL: "bold red",
        Severity.HIGH: "yellow",
        Severity.MEDIUM: "cyan",
        Severity.LOW: "white",
        Severity.INFO: "dim"
    }
    return colors.get(severity, "white")


def format_report(result: CheckResult, format: str = "json") -> str:
    """
    Format check result for export.
    
    Args:
        result: Check result to format
        format: Output format (json, html, markdown)
    
    Returns:
        Formatted report as string
    """
    if format == "json":
        import json
        return json.dumps(result.model_dump(mode='json'), indent=2, default=str)
    
    elif format == "html":
        return _format_html_report(result)
    
    elif format == "markdown":
        return _format_markdown_report(result)
    
    else:
        raise ValueError(f"Unsupported format: {format}")


def _format_html_report(result: CheckResult) -> str:
    """Generate HTML report."""
    status_color = "green" if result.passed else "red"
    status_text = "PASSED" if result.passed else "FAILED"
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Compliance Report</title>
    <style>
        body {{ font-family: system-ui, -apple-system, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; margin-bottom: 30px; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 40px; }}
        .stat-card {{ background: #f8f9fa; padding: 20px; border-radius: 6px; border-left: 4px solid #007bff; }}
        .stat-value {{ font-size: 32px; font-weight: bold; color: #333; }}
        .stat-label {{ color: #666; font-size: 14px; }}
        .status-{status_color} {{ background: #{status_color}; color: white; padding: 8px 16px; border-radius: 4px; display: inline-block; }}
        .violation {{ border-left: 4px solid #dc3545; padding: 15px; margin-bottom: 15px; background: #fff5f5; }}
        .violation.high {{ border-color: #ffc107; background: #fffbeb; }}
        .violation.medium {{ border-color: #17a2b8; background: #f0f9ff; }}
        .violation.low {{ border-color: #6c757d; background: #f8f9fa; }}
        .violation-title {{ font-weight: bold; color: #333; margin-bottom: 8px; }}
        .violation-location {{ color: #666; font-size: 14px; font-family: monospace; }}
        .remediation {{ background: #e7f3ff; padding: 10px; border-radius: 4px; margin-top: 10px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Compliance Report</h1>
        
        <div class="summary">
            <div class="stat-card">
                <div class="stat-value" style="color: {status_color};">{result.score}</div>
                <div class="stat-label">Score (Threshold: {result.threshold})</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{result.total_checks}</div>
                <div class="stat-label">Total Checks</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" style="color: red;">{result.critical_count}</div>
                <div class="stat-label">Critical Issues</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" style="color: orange;">{result.high_count}</div>
                <div class="stat-label">High Issues</div>
            </div>
        </div>
        
        <p><strong>Status:</strong> <span class="status-{status_color}">{status_text}</span></p>
        <p><strong>Policy Pack:</strong> {result.policy_pack}</p>
        <p><strong>Scanned At:</strong> {result.timestamp}</p>
        
        <h2>Violations ({len(result.violations)})</h2>
"""
    
    for v in result.violations:
        severity_class = v.severity.value.lower()
        html += f"""
        <div class="violation {severity_class}">
            <div class="violation-title">{v.severity.value.upper()}: {v.rule_name}</div>
            <div class="violation-location">{v.file_path}:{v.line_number}</div>
            <p>{v.message}</p>
"""
        if v.remediation:
            html += f"""
            <div class="remediation">
                <strong>💡 Remediation:</strong> {v.remediation.description}
            </div>
"""
        html += "        </div>\n"
    
    html += """
    </div>
</body>
</html>
"""
    return html


def _format_markdown_report(result: CheckResult) -> str:
    """Generate Markdown report."""
    status = "✅ PASSED" if result.passed else "❌ FAILED"
    
    md = f"""# Compliance Audit Report

**Policy Pack:** {result.policy_pack}  
**Score:** {result.score}/100  
**Status:** {status}

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
    
    return md
