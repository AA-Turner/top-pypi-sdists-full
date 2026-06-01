#!/usr/bin/env bash
set -euo pipefail

PYPROJECT="$(dirname "$0")/../pyproject.toml"
PYPROJECT="$(realpath "$PYPROJECT")"

# ── helpers ──────────────────────────────────────────────────────────────────

current_version() {
  grep '^version' "$PYPROJECT" | sed 's/version = "\(.*\)"/\1/'
}

bump_version() {
  local part="${1:-patch}"   # major | minor | patch
  local ver
  ver="$(current_version)"
  IFS='.' read -r major minor patch <<< "$ver"
  case "$part" in
    major) major=$((major + 1)); minor=0; patch=0 ;;
    minor) minor=$((minor + 1)); patch=0 ;;
    patch) patch=$((patch + 1)) ;;
    *) echo "Unknown part: $part (use major|minor|patch)"; exit 1 ;;
  esac
  echo "${major}.${minor}.${patch}"
}

set_version() {
  local new="$1"
  sed -i '' "s/^version = \".*\"/version = \"${new}\"/" "$PYPROJECT"
  echo "Version set to ${new}"
}

# ── main ─────────────────────────────────────────────────────────────────────

PART="${1:-}"        # first arg: major | minor | patch | exact:<x.y.z> (optional)
SKIP_PUBLISH="${2:-}"

CURRENT="$(current_version)"

if [[ -z "$PART" ]]; then
  echo "Current version: ${CURRENT}"
  echo "Increment:  [1] patch  [2] minor  [3] major"
  read -r -p "Choice [1]: " choice
  case "${choice:-1}" in
    1|patch) PART="patch" ;;
    2|minor) PART="minor" ;;
    3|major) PART="major" ;;
    *) echo "Invalid choice."; exit 1 ;;
  esac
fi

if [[ "$PART" == exact:* ]]; then
  NEW_VERSION="${PART#exact:}"
else
  NEW_VERSION="$(bump_version "$PART")"
fi

echo "Current: ${CURRENT}  →  New: ${NEW_VERSION}  (${PART})"
read -r -p "Continue? [y/N] " confirm
[[ "$confirm" =~ ^[Yy]$ ]] || { echo "Aborted."; exit 0; }

set_version "$NEW_VERSION"

echo ""
echo "▶ uv build"
uv build --project "$(dirname "$PYPROJECT")"

if [[ "$SKIP_PUBLISH" != "--no-publish" ]]; then
  echo ""
  echo "▶ uv publish"
  uv publish dist/atlasdocs_theme-"${NEW_VERSION}"*.whl dist/atlasdocs_theme-"${NEW_VERSION}".tar.gz
fi

echo ""
echo "▶ git add + commit"
REPO_ROOT="$(dirname "$PYPROJECT")"
git -C "$REPO_ROOT" add -A
git -C "$REPO_ROOT" commit -m "chore: release ${NEW_VERSION}"

echo ""
echo "✓ Released ${NEW_VERSION}"
