"""
Test Comp-LEO SDK on existing Leo programs.

This script demonstrates running compliance checks on the CompliLedger
Leo programs in the parent repository.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from comp_leo.analyzer.checker import ComplianceChecker
from comp_leo.cli.formatters import format_violations, format_summary
from rich.console import Console

console = Console()

def test_sbom_registry():
    """Test the sbom_registry program."""
    console.print("\n[bold cyan]Testing: sbom_registry.aleo[/bold cyan]\n")
    
    file_path = "../../compliedger-aleo/programs/sbom_registry/src/main.leo"
    
    checker = ComplianceChecker(policy_pack="aleo-baseline")
    result = checker.check_file(file_path, threshold=70)
    
    if result.violations:
        console.print(format_violations(result.violations, verbose=True))
    else:
        console.print("[green]✓ No violations found![/green]")
    
    console.print(format_summary(result))
    
    return result


def test_compliance_oracle():
    """Test the compliance_oracle program."""
    console.print("\n[bold cyan]Testing: compliance_oracle.aleo[/bold cyan]\n")
    
    file_path = "../../compliedger-aleo/programs/compliance_oracle/src/main.leo"
    
    checker = ComplianceChecker(policy_pack="aleo-baseline")
    result = checker.check_file(file_path, threshold=70)
    
    if result.violations:
        console.print(format_violations(result.violations, verbose=True))
    else:
        console.print("[green]✓ No violations found![/green]")
    
    console.print(format_summary(result))
    
    return result


if __name__ == "__main__":
    console.print("[bold]Comp-LEO SDK: Testing Existing Code[/bold]\n")
    
    try:
        # Test both programs
        sbom_result = test_sbom_registry()
        oracle_result = test_compliance_oracle()
        
        # Overall summary
        console.print("\n" + "="*60)
        console.print("[bold]Overall Results[/bold]")
        console.print("="*60)
        console.print(f"SBOM Registry: {'✅ PASSED' if sbom_result.passed else '❌ FAILED'} (Score: {sbom_result.score}/100)")
        console.print(f"Compliance Oracle: {'✅ PASSED' if oracle_result.passed else '❌ FAILED'} (Score: {oracle_result.score}/100)")
        
    except FileNotFoundError as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print("[yellow]Make sure you run this from the comp-leo-sdk/examples directory[/yellow]")
