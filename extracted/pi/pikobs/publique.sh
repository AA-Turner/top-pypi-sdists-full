#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e
. r.load.dot cmd/cmds/env/python/py310_2023.07.28_all

# Define the project directory
PROJECT_DIR="/home/dlo001/python/Pikobs"
VERSION_FILE="${PROJECT_DIR}/VERSION"
CHANGELOG_FILE="${PROJECT_DIR}/CHANGELOG.md"

echo "📈 Bumping patch version in ${VERSION_FILE}..."

# 1. Read the current version
if [[ ! -f "$VERSION_FILE" ]]; then
    echo "Error: VERSION file not found at $VERSION_FILE"
    exit 1
fi
OLD_VERSION=$(cat "$VERSION_FILE" | tr -d '[:space:]')

# 2. Split and increment the patch
IFS='.' read -r major minor patch <<< "$OLD_VERSION"
patch=$((patch + 1))
NEW_VERSION="${major}.${minor}.${patch}"

# 3. Write the new version back
echo "$NEW_VERSION" > "$VERSION_FILE"
echo "✅ Version updated: ${OLD_VERSION} -> ${NEW_VERSION}"

echo "📝 Updating ${CHANGELOG_FILE}..."

# 4. Append the new block to the bottom
DATE=$(date +'%Y-%m-%d')
{
    echo ""
    echo "## [${NEW_VERSION}] ${DATE}"
    echo "### Added"
    echo "- bugs"
} >> "$CHANGELOG_FILE"

echo "✅ Entry added to changelog."

# 5. Move to project directory for build and upload
cd "$PROJECT_DIR"

echo "🧹 Cleaning up previous builds..."
python setup.py clean --all
rm -rf dist build *.egg-info

echo "📦 Generating new distribution packages..."
python setup.py sdist bdist_wheel

echo "🚀 Uploading to PyPI..."
twine upload dist/*

echo "✅ Publishing completed successfully!"
