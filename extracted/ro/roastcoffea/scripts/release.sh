#!/usr/bin/env bash
set -euo pipefail

# Usage: ./scripts/release.sh <version>
# Example: ./scripts/release.sh 0.1.1

VERSION="${1:-}"

if [[ -z "$VERSION" ]]; then
    echo "Usage: $0 <version>"
    echo "Example: $0 0.1.1"
    exit 1
fi

echo "=== Releasing roastcoffea $VERSION ==="

# Pre-flight checks
echo ""
echo "=== Pre-flight checks ==="

# Check if tag already exists
if git rev-parse "$VERSION" >/dev/null 2>&1; then
    echo "ERROR: Tag $VERSION already exists!"
    echo "If this is a retry, you may need to:"
    echo "  git tag -d $VERSION              # delete local tag"
    echo "  git push origin :refs/tags/$VERSION  # delete remote tag"
    exit 1
fi

# Check for uncommitted changes (excluding untracked)
if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "ERROR: You have uncommitted changes. Commit or stash them first."
    git status --short
    exit 1
fi

# Check we're on main branch
BRANCH=$(git branch --show-current)
if [[ "$BRANCH" != "main" ]]; then
    echo "ERROR: Not on main branch (currently on '$BRANCH')"
    exit 1
fi

# Check gh CLI is available
if ! command -v gh &> /dev/null; then
    echo "ERROR: gh CLI not found. Install from https://cli.github.com/"
    exit 1
fi

# Check twine is available
if ! pixi run -e dev twine --version &> /dev/null; then
    echo "ERROR: twine not available in dev environment"
    exit 1
fi

echo "All pre-flight checks passed!"
echo ""

# Confirm with user
read -p "Ready to release $VERSION. Continue? [y/N] " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 1
fi

# 1. Run tests FIRST (before any changes)
echo ""
echo "=== Step 1/10: Running tests ==="
pixi run -e dev pytest -v -m "not slow"

# 2. Run pre-commit BEFORE making changes
echo ""
echo "=== Step 2/10: Running pre-commit checks ==="
pixi run -e dev pre-commit run --all-files


# 3. Update version in __init__.py
echo ""
echo "=== Step 3/10: Updating version to $VERSION ==="
sed -i '' "s/__version__ = \".*\"/__version__ = \"$VERSION\"/" src/roastcoffea/__init__.py
echo "Updated src/roastcoffea/__init__.py"

# 4. Commit version bump
echo ""
echo "=== Step 4/10: Committing version bump ==="
git add src/roastcoffea/__init__.py
git commit -m "chore: bump version to $VERSION"

# 5. Create tag
echo ""
echo "=== Step 5/10: Creating tag $VERSION ==="
git tag -a "$VERSION" -m "Release $VERSION"

# 6. Build distribution (before push, so we can verify)
echo ""
echo "=== Step 6/10: Building distribution ==="
rm -rf dist/
pixi run -e dev python -m build

# 7. Verify build
echo ""
echo "=== Step 7/10: Verifying build ==="
pixi run -e dev twine check dist/*

# 8. Push to GitHub (only after build verified)
echo ""
echo "=== Step 8/10: Pushing to GitHub ==="
git push origin main
git push origin "$VERSION"

# 9. Create GitHub release
echo ""
echo "=== Step 9/10: Creating GitHub release ==="
gh release create "$VERSION" \
    --title "v$VERSION" \
    --generate-notes

# 10. Publish to PyPI
echo ""
echo "=== Step 10/10: Publishing to PyPI ==="
pixi run -e dev twine upload dist/*

echo ""
echo "=== Release $VERSION complete! ==="
echo ""
echo "Published:"
echo "  - GitHub: https://github.com/MoAly98/roastcoffea/releases/tag/$VERSION"
echo "  - PyPI:   https://pypi.org/project/roastcoffea/$VERSION/"
