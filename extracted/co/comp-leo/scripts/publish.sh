#!/bin/bash
# Publish Comp-LEO SDK to PyPI

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Comp-LEO SDK - Publishing to PyPI"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if on main branch
current_branch=$(git branch --show-current)
if [ "$current_branch" != "main" ]; then
    echo "❌ Must be on 'main' branch to publish"
    echo "Current branch: $current_branch"
    exit 1
fi

# Check for uncommitted changes
if [[ -n $(git status -s) ]]; then
    echo "❌ Uncommitted changes detected"
    echo "Commit or stash changes before publishing"
    git status -s
    exit 1
fi

# Get version
version=$(python3 -c "import comp_leo; print(comp_leo.__version__)")
echo "📦 Publishing version: $version"
echo ""

# Confirm
read -p "Publish v$version to PyPI? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled"
    exit 1
fi

echo ""
echo "1️⃣  Running tests..."
pytest tests/ -v || { echo "❌ Tests failed"; exit 1; }

echo ""
echo "2️⃣  Running linters..."
ruff check comp_leo/ || { echo "❌ Linting failed"; exit 1; }

echo ""
echo "3️⃣  Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info

echo ""
echo "4️⃣  Building distribution..."
python3 -m build

echo ""
echo "5️⃣  Checking package..."
twine check dist/*

echo ""
echo "6️⃣  Uploading to PyPI..."
twine upload dist/*

echo ""
echo "7️⃣  Creating git tag..."
git tag "v$version"
git push origin "v$version"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✅ Published v$version to PyPI!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Next steps:"
echo "  • Verify: pip install comp-leo==$version"
echo "  • Create GitHub release"
echo "  • Announce on Aleo Forum"
echo "  • Tweet announcement"
echo ""
