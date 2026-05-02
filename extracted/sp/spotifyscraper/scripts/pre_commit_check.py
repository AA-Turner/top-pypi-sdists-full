#!/usr/bin/env python3
"""
Pre-commit check script to ensure all linters pass.
Run this before committing to avoid CI failures.
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd):
    """Run a command and return success status."""
    print(f"\n🔍 Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Failed: {cmd}")
        print(result.stdout)
        print(result.stderr)
        return False
    print(f"✅ Passed: {cmd}")
    return True

def main():
    """Run all pre-commit checks."""
    project_root = Path(__file__).parent.parent
    
    checks = [
        ("Black", f"cd {project_root} && black --check src/ tests/"),
        ("isort", f"cd {project_root} && isort --check-only src/ tests/"),
        ("Flake8", f"cd {project_root} && flake8 src/ tests/"),
        ("Pylint", f"cd {project_root} && pylint src/"),
    ]
    
    all_passed = True
    
    print("🚀 Running pre-commit checks...")
    
    for name, cmd in checks:
        if not run_command(cmd):
            all_passed = False
            
            # Offer to fix automatically
            if name == "Black":
                if input("\nRun black to fix? (y/n): ").lower() == 'y':
                    subprocess.run(f"cd {project_root} && black src/ tests/", shell=True)
                    print("✅ Black formatting applied")
            elif name == "isort":
                if input("\nRun isort to fix? (y/n): ").lower() == 'y':
                    subprocess.run(f"cd {project_root} && isort src/ tests/", shell=True)
                    print("✅ Import sorting applied")
    
    if all_passed:
        print("\n🎉 All checks passed! Safe to commit.")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please fix before committing.")
        return 1

if __name__ == "__main__":
    sys.exit(main())