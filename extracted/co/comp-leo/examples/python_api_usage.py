"""
Example: Using Comp-LEO SDK from Python

Demonstrates various ways to use the SDK programmatically.
"""

from comp_leo import ComplianceChecker, LeoParser
from comp_leo.core.models import Severity
import json

print("=" * 60)
print("Comp-LEO SDK: Python API Examples")
print("=" * 60)

# ============================================================================
# Example 1: Basic Compliance Check
# ============================================================================

print("\n[Example 1] Basic Compliance Check")
print("-" * 60)

leo_code = """
program example.aleo {
    mapping balances: address => u64;
    
    transition transfer(public recipient: address, public amount: u64) {
        // Missing validation!
        Mapping::set(balances, recipient, amount);
    }
}
"""

checker = ComplianceChecker(policy_pack="aleo-baseline")
program = checker.parser.parse_source(leo_code, "example.leo")
result = checker.check_file("example.leo") if False else checker._run_checks(program)

print(f"Violations found: {len(result)}")
for v in result[:3]:  # Show first 3
    print(f"  - {v.severity.value.upper()}: {v.rule_name}")
    print(f"    {v.message}")

# ============================================================================
# Example 2: Parse and Analyze Leo Structure
# ============================================================================

print("\n[Example 2] Parse Leo Structure")
print("-" * 60)

parser = LeoParser()
program = parser.parse_source(leo_code, "example.leo")

print(f"Program: {program.name}")
print(f"Transitions: {[t.name for t in program.transitions]}")
print(f"Mappings: {[m.name for m in program.mappings]}")

for transition in program.transitions:
    print(f"\nTransition: {transition.name}")
    print(f"  - Parameters: {len(transition.parameters)}")
    print(f"  - Has assertions: {transition.has_assertions}")
    print(f"  - Modifies state: {transition.modifies_state}")
    print(f"  - Has mappings: {transition.has_mappings}")

# ============================================================================
# Example 3: Custom Filtering and Analysis
# ============================================================================

print("\n[Example 3] Filter Critical Issues")
print("-" * 60)

checker = ComplianceChecker(policy_pack="aleo-baseline")
program = checker.parser.parse_source(leo_code, "example.leo")
violations = checker._run_checks(program)

critical = [v for v in violations if v.severity == Severity.CRITICAL]
high = [v for v in violations if v.severity == Severity.HIGH]

print(f"Critical violations: {len(critical)}")
print(f"High severity violations: {len(high)}")

if critical:
    print("\n⚠️  CRITICAL ISSUES MUST BE FIXED:")
    for v in critical:
        print(f"  → {v.file_path}:{v.line_number}")
        print(f"    {v.message}")
        if v.remediation:
            print(f"    💡 Fix: {v.remediation.description}")

# ============================================================================
# Example 4: Export Results
# ============================================================================

print("\n[Example 4] Export to JSON")
print("-" * 60)

# Create a proper check result
checker = ComplianceChecker(policy_pack="aleo-baseline")

# Write source to temp file for full check
import tempfile
from pathlib import Path

with tempfile.NamedTemporaryFile(mode='w', suffix='.leo', delete=False) as f:
    f.write(leo_code)
    temp_path = f.name

try:
    result = checker.check_file(temp_path, threshold=70)
    
    print(f"Check complete:")
    print(f"  - Score: {result.score}/100")
    print(f"  - Passed: {result.passed}")
    print(f"  - Violations: {len(result.violations)}")
    
    # Export to JSON
    output = {
        "summary": {
            "score": result.score,
            "passed": result.passed,
            "total_checks": result.total_checks
        },
        "violations": [
            {
                "rule": v.rule_name,
                "severity": v.severity.value,
                "message": v.message,
                "location": f"{v.file_path}:{v.line_number}"
            }
            for v in result.violations
        ]
    }
    
    print("\nExported JSON (first 500 chars):")
    json_str = json.dumps(output, indent=2)
    print(json_str[:500] + "..." if len(json_str) > 500 else json_str)

finally:
    Path(temp_path).unlink(missing_ok=True)

# ============================================================================
# Example 5: Batch Processing
# ============================================================================

print("\n[Example 5] Batch Processing Multiple Files")
print("-" * 60)

programs = [
    ("safe.leo", """
program safe.aleo {
    transition hello(public name: address) -> u64 {
        assert_eq(self.caller, name);
        return 42u64;
    }
}
"""),
    ("unsafe.leo", """
program unsafe.aleo {
    mapping data: field => u64;
    
    transition update(key: field, value: u64) {
        Mapping::set(data, key, value);  // No access control!
    }
}
""")
]

results = {}

for filename, code in programs:
    with tempfile.NamedTemporaryFile(mode='w', suffix='.leo', delete=False) as f:
        f.write(code)
        temp_path = f.name
    
    try:
        checker = ComplianceChecker(policy_pack="aleo-baseline")
        result = checker.check_file(temp_path, threshold=75)
        results[filename] = result
        
        status = "✅ PASS" if result.passed else "❌ FAIL"
        print(f"{filename}: {status} (Score: {result.score}/100, Violations: {len(result.violations)})")
    finally:
        Path(temp_path).unlink(missing_ok=True)

# Summary
total_violations = sum(len(r.violations) for r in results.values())
avg_score = sum(r.score for r in results.values()) / len(results)

print(f"\nBatch Summary:")
print(f"  - Files checked: {len(results)}")
print(f"  - Total violations: {total_violations}")
print(f"  - Average score: {avg_score:.1f}/100")

print("\n" + "=" * 60)
print("Examples complete!")
print("=" * 60)
