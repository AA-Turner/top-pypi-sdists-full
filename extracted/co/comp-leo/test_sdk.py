#!/usr/bin/env python3
"""
Quick test script for Comp-LEO SDK
Run: python3 test_sdk.py
"""

import sys
from pathlib import Path

# Add SDK to path
sys.path.insert(0, str(Path(__file__).parent))

from comp_leo.analyzer.checker import ComplianceChecker
from comp_leo.analyzer.parser import LeoParser
from rich.console import Console
from rich.panel import Panel
from rich import box

console = Console()

def print_header(title):
    console.print(f"\n{'='*60}")
    console.print(f"  {title}", style="bold cyan")
    console.print(f"{'='*60}\n")

def test_parser():
    """Test 1: Leo Parser"""
    print_header("Test 1: Leo Parser")
    
    # Test parsing simple Leo code
    test_code = """
program test.aleo {
    mapping balances: address => u64;
    
    struct Entry {
        hash: field,
        value: u64,
    }
    
    transition transfer(public recipient: address, public amount: u64) {
        assert(amount > 0u64);
        Mapping::set(balances, recipient, amount);
    }
}
"""
    
    try:
        parser = LeoParser()
        program = parser.parse_source(test_code, "test.leo")
        
        console.print("✅ Parser working!", style="green")
        console.print(f"  • Program: {program.name}")
        console.print(f"  • Transitions: {[t.name for t in program.transitions]}")
        console.print(f"  • Mappings: {[m.name for m in program.mappings]}")
        console.print(f"  • Structs: {[s.name for s in program.structs]}")
        return True
    except Exception as e:
        console.print(f"❌ Parser error: {e}", style="red")
        return False

def test_checker():
    """Test 2: Compliance Checker"""
    print_header("Test 2: Compliance Checker")
    
    # Test with code that has violations
    unsafe_code = """
program unsafe.aleo {
    mapping data: field => u64;
    
    transition update(key: field, value: u64) {
        // No validation!
        // No access control!
        Mapping::set(data, key, value);
    }
}
"""
    
    try:
        checker = ComplianceChecker(policy_pack="aleo-baseline")
        program = checker.parser.parse_source(unsafe_code, "unsafe.leo")
        violations = checker._run_checks(program)
        
        console.print("✅ Checker working!", style="green")
        console.print(f"  • Violations found: {len(violations)}")
        
        for v in violations[:3]:  # Show first 3
            console.print(f"  • {v.severity.value.upper()}: {v.rule_name}")
        
        return True
    except Exception as e:
        console.print(f"❌ Checker error: {e}", style="red")
        import traceback
        console.print(traceback.format_exc())
        return False

def test_existing_leo_files():
    """Test 3: Real Leo Files"""
    print_header("Test 3: Your Existing Leo Programs")
    
    # Paths to your Leo files
    files = [
        "../compliedger-aleo/programs/sbom_registry/src/main.leo",
        "../compliedger-aleo/programs/compliance_oracle/src/main.leo"
    ]
    
    results = {}
    
    for file_path in files:
        path = Path(file_path)
        
        if not path.exists():
            console.print(f"⚠️  Skipping {path.name} (not found)", style="yellow")
            continue
        
        try:
            console.print(f"\n📝 Analyzing: [cyan]{path.name}[/cyan]")
            
            checker = ComplianceChecker(policy_pack="aleo-baseline")
            
            # Parse and analyze
            program = checker.parser.parse_file(str(path))
            violations = checker._run_checks(program)
            score = checker._compute_score(violations, 10)  # 10 enabled rules
            
            results[path.name] = {
                "score": score,
                "violations": len(violations),
                "critical": len([v for v in violations if v.severity.value == "critical"]),
                "high": len([v for v in violations if v.severity.value == "high"])
            }
            
            # Display results
            status = "✅ PASS" if score >= 70 else "⚠️  REVIEW"
            console.print(f"{status} Score: {score}/100 | Violations: {len(violations)}")
            
            # Show violations
            if violations:
                for v in violations[:5]:  # First 5
                    console.print(f"  • {v.severity.value.upper()}: {v.message}", style="yellow")
                    if v.remediation:
                        console.print(f"    💡 {v.remediation.description}", style="dim")
        
        except Exception as e:
            console.print(f"❌ Error analyzing {path.name}: {e}", style="red")
    
    return results

def main():
    console.print(Panel.fit(
        "[bold cyan]Comp-LEO SDK Test Suite[/bold cyan]\n"
        "Testing parser, checker, and your Leo programs",
        box=box.DOUBLE,
        border_style="cyan"
    ))
    
    # Run tests
    test1_ok = test_parser()
    test2_ok = test_checker()
    results = test_existing_leo_files()
    
    # Summary
    print_header("Test Summary")
    
    console.print(f"Parser Test: {'✅' if test1_ok else '❌'}")
    console.print(f"Checker Test: {'✅' if test2_ok else '❌'}")
    console.print(f"\nYour Programs:")
    
    for name, data in results.items():
        console.print(f"  • {name}")
        console.print(f"    Score: {data['score']}/100")
        console.print(f"    Violations: {data['violations']} (🔴 {data['critical']} ⚠️ {data['high']})")
    
    if all([test1_ok, test2_ok, results]):
        console.print(f"\n[bold green]✅ All tests passed![/bold green]")
        console.print("\n[dim]Next steps:[/dim]")
        console.print("  • Review violations above")
        console.print("  • Try: python3 -m comp_leo.cli.main check ../compliedger-aleo/programs/")
        console.print("  • Try: python3 examples/python_api_usage.py")
    else:
        console.print(f"\n[bold yellow]⚠️  Some tests need attention[/bold yellow]")
    
    console.print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Interrupted by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[bold red]Error: {e}[/bold red]")
        import traceback
        console.print(traceback.format_exc())
        sys.exit(1)
