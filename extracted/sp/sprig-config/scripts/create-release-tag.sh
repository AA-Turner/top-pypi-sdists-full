#!/usr/bin/env bash
set -euo pipefail

# ==========================================
# Release Tag Creation Script
# ==========================================
# This script:
# 1. Extracts the latest version from CHANGELOG.md
# 2. Verifies it matches pyproject.toml version
# 3. Validates semantic version progression:
#    - Prevents skipping versions (e.g., 1.2.4 -> 1.2.7)
#    - Ensures proper major/minor/patch increments
#    - Supports RC versions (e.g., 1.2.5-RC1, 1.2.5-RC2)
# 4. Checks if the tag already exists
# 5. Creates an annotated git tag with changelog entry
# ==========================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODULE_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
MONOREPO_ROOT="$(cd "${MODULE_DIR}/.." && pwd)"
CHANGELOG_FILE="${MONOREPO_ROOT}/CHANGELOG.md"
PYPROJECT_FILE="${MODULE_DIR}/pyproject.toml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
error() {
    echo -e "${RED}❌ Error: $1${NC}" >&2
    exit 1
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

warn() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Parse semantic version into components
# Returns: MAJOR MINOR PATCH RC (RC will be empty if not an RC version)
parse_version() {
    local version="$1"
    local major minor patch rc

    # Handle RC versions (e.g., 1.2.5-RC1)
    if [[ $version =~ ^([0-9]+)\.([0-9]+)\.([0-9]+)-RC([0-9]+)$ ]]; then
        major="${BASH_REMATCH[1]}"
        minor="${BASH_REMATCH[2]}"
        patch="${BASH_REMATCH[3]}"
        rc="${BASH_REMATCH[4]}"
    # Handle normal versions (e.g., 1.2.5)
    elif [[ $version =~ ^([0-9]+)\.([0-9]+)\.([0-9]+)$ ]]; then
        major="${BASH_REMATCH[1]}"
        minor="${BASH_REMATCH[2]}"
        patch="${BASH_REMATCH[3]}"
        rc=""
    else
        echo "INVALID"
        return 1
    fi

    echo "${major} ${minor} ${patch} ${rc}"
}

# Validate version progression
validate_version_increment() {
    local prev_version="$1"
    local new_version="$2"

    # Parse versions
    local prev_parsed new_parsed
    prev_parsed=$(parse_version "${prev_version}")
    new_parsed=$(parse_version "${new_version}")

    if [[ "$prev_parsed" == "INVALID" ]] || [[ "$new_parsed" == "INVALID" ]]; then
        error "Invalid version format"
    fi

    read -r prev_major prev_minor prev_patch prev_rc <<< "$prev_parsed"
    read -r new_major new_minor new_patch new_rc <<< "$new_parsed"

    # Check if versions are identical (only RC changes)
    if [[ $new_major -eq $prev_major ]] && [[ $new_minor -eq $prev_minor ]] && [[ $new_patch -eq $prev_patch ]]; then
        # Same base version - check RC progression or final release
        if [[ -n "$prev_rc" ]] && [[ -z "$new_rc" ]]; then
            # Going from RC to final release (e.g., 1.2.5-RC2 -> 1.2.5)
            success "Valid progression: RC to final release (${prev_version} -> ${new_version})"
            return 0
        elif [[ -n "$prev_rc" ]] && [[ -n "$new_rc" ]]; then
            # Both are RC - check increment
            if [[ $new_rc -eq $((prev_rc + 1)) ]]; then
                success "Valid progression: RC increment (${prev_version} -> ${new_version})"
                return 0
            else
                error "Invalid RC progression: ${prev_version} -> ${new_version}\n  RC must increment by 1 (expected: ${prev_major}.${prev_minor}.${prev_patch}-RC$((prev_rc + 1)))"
            fi
        else
            error "Cannot create duplicate version: ${prev_version} -> ${new_version}"
        fi
    fi

    # Check patch increment (e.g., 1.2.4 -> 1.2.5 or 1.2.5-RC1)
    if [[ $new_major -eq $prev_major ]] && [[ $new_minor -eq $prev_minor ]] && [[ $new_patch -eq $((prev_patch + 1)) ]]; then
        success "Valid progression: Patch increment (${prev_version} -> ${new_version})"
        return 0
    fi

    # Check minor increment (e.g., 1.2.4 -> 1.3.0)
    if [[ $new_major -eq $prev_major ]] && [[ $new_minor -eq $((prev_minor + 1)) ]] && [[ $new_patch -eq 0 ]]; then
        if [[ -z "$new_rc" ]]; then
            success "Valid progression: Minor increment (${prev_version} -> ${new_version})"
            return 0
        else
            warn "Minor increment with RC (${prev_version} -> ${new_version})"
            return 0
        fi
    fi

    # Check major increment (e.g., 1.2.4 -> 2.0.0)
    if [[ $new_major -eq $((prev_major + 1)) ]] && [[ $new_minor -eq 0 ]] && [[ $new_patch -eq 0 ]]; then
        if [[ -z "$new_rc" ]]; then
            success "Valid progression: Major increment (${prev_version} -> ${new_version})"
            return 0
        else
            warn "Major increment with RC (${prev_version} -> ${new_version})"
            return 0
        fi
    fi

    # If we got here, it's an invalid increment
    local suggestion=""
    if [[ $new_major -eq $prev_major ]] && [[ $new_minor -eq $prev_minor ]]; then
        suggestion="  Expected: ${prev_major}.${prev_minor}.$((prev_patch + 1))"
    elif [[ $new_major -eq $prev_major ]]; then
        suggestion="  Expected: ${prev_major}.$((prev_minor + 1)).0"
    else
        suggestion="  Expected: $((prev_major + 1)).0.0"
    fi

    error "Invalid version progression: ${prev_version} -> ${new_version}\n${suggestion}\n\nYou cannot skip versions. Please use proper semantic versioning."
}

# Change to module directory
cd "${MODULE_DIR}"

# Check if files exist
[[ -f "${CHANGELOG_FILE}" ]] || error "CHANGELOG.md not found at ${CHANGELOG_FILE}"
[[ -f "${PYPROJECT_FILE}" ]] || error "pyproject.toml not found at ${PYPROJECT_FILE}"

info "Extracting latest version from CHANGELOG.md..."

# Extract the first version from CHANGELOG.md (format: ## [1.2.5] — 2026-01-08)
CHANGELOG_VERSION=$(grep -m 1 '^## \[' "${CHANGELOG_FILE}" | sed -E 's/^## \[([0-9]+\.[0-9]+\.[0-9]+(-RC[0-9]+)?)\].*/\1/')

if [[ -z "${CHANGELOG_VERSION}" ]]; then
    error "Could not extract version from CHANGELOG.md"
fi

info "Found changelog version: ${CHANGELOG_VERSION}"

# Extract version from pyproject.toml
info "Extracting version from pyproject.toml..."
PYPROJECT_VERSION=$(grep '^version = ' "${PYPROJECT_FILE}" | head -1 | sed -E 's/version = "([^"]+)"/\1/')

if [[ -z "${PYPROJECT_VERSION}" ]]; then
    error "Could not extract version from pyproject.toml"
fi

info "Found pyproject.toml version: ${PYPROJECT_VERSION}"

# Compare versions (case-insensitive)
CHANGELOG_VERSION_LOWER=$(echo "${CHANGELOG_VERSION}" | tr '[:upper:]' '[:lower:]')
PYPROJECT_VERSION_LOWER=$(echo "${PYPROJECT_VERSION}" | tr '[:upper:]' '[:lower:]')
if [[ "${CHANGELOG_VERSION_LOWER}" != "${PYPROJECT_VERSION_LOWER}" ]]; then
    error "Version mismatch!\n  CHANGELOG.md: ${CHANGELOG_VERSION}\n  pyproject.toml: ${PYPROJECT_VERSION}\n\nPlease ensure both files have the same version."
fi

success "Version matches in both files: ${CHANGELOG_VERSION}"

# Get latest git tag to validate version progression
info "Checking version progression against latest git tag..."

# Get all tags matching V*.*.* or v*.*.* pattern, strip prefix, sort by version, get the latest
LATEST_TAG=$(git tag -l "[Vv]*.*.*" | grep -E '^[Vv][0-9]+\.[0-9]+\.[0-9]+(-RC[0-9]+)?$' | \
    sed 's/^[Vv]//' | sort -V | tail -n 1)

# If we found a version, prepend V to reconstruct the tag format
if [[ -n "${LATEST_TAG}" ]]; then
    LATEST_VERSION="${LATEST_TAG}"
    # Find the actual tag name (could be V or v prefix)
    ACTUAL_TAG=$(git tag -l "[Vv]${LATEST_VERSION}" | head -n 1)
    LATEST_TAG="${ACTUAL_TAG}"
else
    LATEST_TAG=""
fi

if [[ -n "${LATEST_TAG}" ]]; then
    # Strip the V/v prefix from tag
    LATEST_VERSION="${LATEST_TAG#[Vv]}"
    info "Latest tag: ${LATEST_TAG} (version: ${LATEST_VERSION})"

    # Validate version progression
    validate_version_increment "${LATEST_VERSION}" "${CHANGELOG_VERSION}"
else
    warn "No previous version tags found - this appears to be the first release"
    info "Creating initial release tag for version ${CHANGELOG_VERSION}"
fi

# Construct tag name (V prefix, case-preserved from changelog)
TAG_NAME="V${CHANGELOG_VERSION}"

# Check if tag already exists (case-insensitive check)
info "Checking if tag ${TAG_NAME} already exists..."

if git rev-parse "${TAG_NAME}" >/dev/null 2>&1; then
    error "Tag ${TAG_NAME} already exists!\n\nUse 'git tag -d ${TAG_NAME}' to delete it locally if you need to recreate it.\nUse 'git push origin :refs/tags/${TAG_NAME}' to delete it remotely."
fi

# Also check lowercase version
TAG_NAME_LOWER="v${CHANGELOG_VERSION}"
if [[ "${TAG_NAME}" != "${TAG_NAME_LOWER}" ]] && git rev-parse "${TAG_NAME_LOWER}" >/dev/null 2>&1; then
    error "Tag ${TAG_NAME_LOWER} already exists!\n\nUse 'git tag -d ${TAG_NAME_LOWER}' to delete it locally if you need to recreate it."
fi

success "Tag ${TAG_NAME} does not exist"

# Extract the changelog entry for this version
info "Extracting changelog entry for annotation..."

# Get all lines between the first ## [version] and the next ## [
CHANGELOG_ENTRY=$(awk '/^## \['"${CHANGELOG_VERSION}"'\]/{flag=1; next} /^## \[/{flag=0} flag' "${CHANGELOG_FILE}")

if [[ -z "${CHANGELOG_ENTRY}" ]]; then
    error "Could not extract changelog entry for version ${CHANGELOG_VERSION}"
fi

# Preview the tag
echo ""
info "Ready to create tag: ${TAG_NAME}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Tag Annotation Preview:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Release ${CHANGELOG_VERSION}"
echo ""
echo "${CHANGELOG_ENTRY}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Prompt for confirmation
read -p "Create tag ${TAG_NAME}? [y/N] " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    warn "Tag creation cancelled"
    exit 0
fi

# Create annotated tag with changelog entry
info "Creating annotated tag ${TAG_NAME}..."

TAG_MESSAGE="Release ${CHANGELOG_VERSION}

${CHANGELOG_ENTRY}"

git tag -a "${TAG_NAME}" -m "${TAG_MESSAGE}"

success "Tag ${TAG_NAME} created successfully!"

echo ""
info "Next steps:"
echo "  1. Verify the tag: git show ${TAG_NAME}"
echo "  2. Push the tag:   git push origin ${TAG_NAME}"
echo "  3. GitLab CI will trigger deployment jobs for version tags"
echo ""
info "To undo (if needed):"
echo "  - Delete local tag:  git tag -d ${TAG_NAME}"
echo "  - Delete remote tag: git push origin :refs/tags/${TAG_NAME}"
