#!/bin/bash
# Prepare Comp-LEO SDK for release

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Comp-LEO SDK - Release Preparation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Get current version
current_version=$(python3 -c "import comp_leo; print(comp_leo.__version__)")
echo "Current version: $current_version"
echo ""

# Ask for new version
read -p "New version (e.g., 0.2.0): " new_version

if [ -z "$new_version" ]; then
    echo "❌ Version required"
    exit 1
fi

echo ""
echo "📝 Preparing release v$new_version..."
echo ""

# Update version in __init__.py
echo "1️⃣  Updating version in __init__.py..."
sed -i '' "s/__version__ = \"$current_version\"/__version__ = \"$new_version\"/" comp_leo/__init__.py

# Update version in pyproject.toml
echo "2️⃣  Updating version in pyproject.toml..."
sed -i '' "s/version = \"$current_version\"/version = \"$new_version\"/" pyproject.toml

# Update CHANGELOG
echo "3️⃣  Updating CHANGELOG.md..."
if [ ! -f CHANGELOG.md ]; then
    cat > CHANGELOG.md << EOF
# Changelog

All notable changes to Comp-LEO SDK will be documented in this file.

## [Unreleased]

## [$new_version] - $(date +%Y-%m-%d)

### Added
- 

### Changed
- 

### Fixed
- 

EOF
else
    # Add new version section
    sed -i '' "s/## \[Unreleased\]/## [Unreleased]\n\n## [$new_version] - $(date +%Y-%m-%d)\n\n### Added\n- \n\n### Changed\n- \n\n### Fixed\n- \n/" CHANGELOG.md
fi

echo "✅ Updated to v$new_version"
echo ""
echo "Next steps:"
echo "  1. Edit CHANGELOG.md with release notes"
echo "  2. Commit changes: git add . && git commit -m 'chore: bump version to $new_version'"
echo "  3. Run tests: make test"
echo "  4. Publish: ./scripts/publish.sh"
echo ""
