"""Generate CI/CD configuration files."""

from pathlib import Path
from rich.console import Console

console = Console()

GITHUB_ACTIONS_TEMPLATE = """name: Compliance Check

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main, develop]

jobs:
  compliance:
    name: Leo Compliance Check
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install Comp-LEO
        run: pip install comp-leo
      
      - name: Run compliance checks
        run: |
          comp-leo check programs/ \\
            --policy aleo-baseline \\
            --threshold 75 \\
            --fail-on-critical \\
            --output compliance-report.json
      
      - name: Upload report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: compliance-report
          path: compliance-report.json
"""

GITLAB_CI_TEMPLATE = """compliance_check:
  stage: test
  image: python:3.10
  
  before_script:
    - pip install comp-leo
  
  script:
    - |
      comp-leo check programs/ \\
        --policy aleo-baseline \\
        --threshold 75 \\
        --fail-on-critical \\
        --output compliance-report.json
  
  artifacts:
    when: always
    paths:
      - compliance-report.json
    reports:
      junit: compliance-report.json
"""

PRE_COMMIT_TEMPLATE = """#!/bin/bash
# Comp-LEO Pre-Commit Hook

echo "🔍 Running Comp-LEO compliance checks..."

# Find staged .leo files
staged_files=$(git diff --cached --name-only --diff-filter=ACMR | grep "\\.leo$")

if [ -z "$staged_files" ]; then
    echo "No Leo files staged, skipping"
    exit 0
fi

# Run check
comp-leo check programs/ --policy aleo-baseline --threshold 75 --fail-on-critical --quiet

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Compliance check failed!"
    echo "Fix violations or use 'git commit --no-verify' to skip"
    exit 1
fi

echo "✅ Compliance check passed!"
exit 0
"""

def generate_github_actions(output_dir: str = "."):
    """Generate GitHub Actions workflow."""
    output_path = Path(output_dir) / ".github" / "workflows" / "compliance.yml"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        f.write(GITHUB_ACTIONS_TEMPLATE)
    
    console.print(f"[green]✓[/green] Generated: {output_path}")
    return str(output_path)

def generate_gitlab_ci(output_dir: str = "."):
    """Generate GitLab CI configuration."""
    output_path = Path(output_dir) / ".gitlab-ci.yml"
    
    # Append to existing or create new
    mode = 'a' if output_path.exists() else 'w'
    
    with open(output_path, mode) as f:
        if mode == 'a':
            f.write("\n\n# Comp-LEO Compliance Check\n")
        f.write(GITLAB_CI_TEMPLATE)
    
    console.print(f"[green]✓[/green] {'Updated' if mode == 'a' else 'Generated'}: {output_path}")
    return str(output_path)

def generate_pre_commit_hook(output_dir: str = "."):
    """Generate pre-commit hook."""
    output_path = Path(output_dir) / ".git" / "hooks" / "pre-commit"
    
    if not output_path.parent.exists():
        console.print("[yellow]⚠️  No .git directory found. Initialize git first.[/yellow]")
        # Create in examples instead
        output_path = Path(output_dir) / "pre-commit"
    
    with open(output_path, 'w') as f:
        f.write(PRE_COMMIT_TEMPLATE)
    
    # Make executable
    output_path.chmod(0o755)
    
    console.print(f"[green]✓[/green] Generated: {output_path}")
    console.print(f"[dim]Run: chmod +x {output_path}[/dim]")
    return str(output_path)

def generate_all(output_dir: str = "."):
    """Generate all CI/CD files."""
    console.print("\n[bold]Generating CI/CD configurations...[/bold]\n")
    
    files = []
    files.append(generate_github_actions(output_dir))
    files.append(generate_gitlab_ci(output_dir))
    files.append(generate_pre_commit_hook(output_dir))
    
    console.print(f"\n[green]✓ Generated {len(files)} CI/CD files[/green]")
    return files
