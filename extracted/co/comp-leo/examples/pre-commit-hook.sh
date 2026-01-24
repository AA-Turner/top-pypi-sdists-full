#!/bin/bash
# Comp-LEO Pre-Commit Hook
# Place in .git/hooks/pre-commit and make executable: chmod +x .git/hooks/pre-commit

echo "🔍 Running Comp-LEO compliance checks..."

# Find all staged .leo files
staged_files=$(git diff --cached --name-only --diff-filter=ACMR | grep "\.leo$")

if [ -z "$staged_files" ]; then
    echo "No Leo files staged, skipping compliance check"
    exit 0
fi

# Run compliance check
comp-leo check programs/ --policy aleo-baseline --threshold 75 --fail-on-critical --quiet

exit_code=$?

if [ $exit_code -ne 0 ]; then
    echo ""
    echo "❌ Compliance check failed!"
    echo "Fix violations or use 'git commit --no-verify' to skip (not recommended)"
    echo ""
    echo "Run 'comp-leo check programs/' for detailed results"
    exit 1
fi

echo "✅ Compliance check passed!"
exit 0
