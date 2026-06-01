#!/usr/bin/env python3
"""
CLI Examples for typecoverage library.
Run this script to see various command-line usage examples.
"""

# Example commands - uncomment and run as needed

print("=== TYPECOVERAGE CLI EXAMPLES ===")
print()
examples = [
    # Basic usage
    ("Analyze a single file", "python -m typecoverage myfile.py"),
    ("Analyze with statistics", "python -m typecoverage --statistics myfile.py"),
    ("Show context lines", "python -m typecoverage --context-lines 3 myfile.py"),

    # Output formats
    ("JSON output", "python -m typecoverage --format json myfile.py"),
    ("Save to file", "python -m typecoverage --output report.txt myfile.py"),

    # Multiple targets
    ("Multiple files", "python -m typecoverage file1.py file2.py"),
    ("Glob patterns", "python -m typecoverage '*.py'"),
    ("Recursive directory", "python -m typecoverage --recursive src/"),

    # Filtering
    ("Exclude test files", "python -m typecoverage --exclude test_ src/"),
    ("Python files only", "python -m typecoverage --extensions .py src/"),
    ("Include hidden vars",
     "python -m typecoverage --no-ignore-underscore-vars src/"),

    # Exit behavior
    ("Exit nonzero on issues",
     "python -m typecoverage --exit-nonzero-on-issues src/"),
    ("Fail if >= 5 issues", "python -m typecoverage --fail-under 5 src/"),

    # Special modes
    ("Show version", "python -m typecoverage --version"),
    ("Run demo", "python -m typecoverage --demo"),
    ("Force colors", "python -m typecoverage --force-color src/"),
]

for description, command in examples:
    print(f"{description}:")
    print(f"  {command}")
    print()

print("=== COMMON WORKFLOWS ===")
print()
workflows = [
    ("Check entire project", "python -m typecoverage --recursive --statistics ."),
    ("CI/CD integration", "python -m typecoverage --exit-nonzero-on-issues "
     "--format json src/ > typecoverage-report.json"),
    ("Quick file check", "python -m typecoverage --context-lines 2 myfile.py"),
    ("Comprehensive analysis", "python -m typecoverage --recursive "
     "--no-ignore-underscore-vars --statistics src/"),
]
for description, command in workflows:
    print(f"{description}:")
    print(f"  {command}")
    print()
print("To run any example, copy the command and execute it in your terminal.")
