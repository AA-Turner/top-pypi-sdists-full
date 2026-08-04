#!/bin/bash
set -e
export PATH="$HOME/.local/bin:$PATH"
cd "$(dirname "$0")/.."

# DEV_FLAG is set by CI (empty for release, --dev for dev branches)
../.github/bump_version.sh VERSION $DEV_FLAG --mode VERSION

# Bump plato-fuse's Cargo version (patch) whenever its Rust source changed, so
# every published binary is attributable: the binary prints it via --version
# and plato-fuse/deploy.sh stamps it into the release notes on upload.
if echo "${CHANGED_FILES:-}" | grep -q "python-sdk/plato-fuse/"; then
  fuse_toml="plato-fuse/Cargo.toml"
  current=$(grep -m1 '^version = ' "$fuse_toml" | sed 's/version = "\(.*\)"/\1/')
  IFS=. read -r major minor patch <<< "$current"
  next="$major.$minor.$((patch + 1))"
  sed -i "0,/^version = \"$current\"/s//version = \"$next\"/" "$fuse_toml"
  # Keep Cargo.lock's own package entry in sync without needing cargo here.
  sed -i "/^name = \"plato-fuse\"$/{n;s/version = \"$current\"/version = \"$next\"/}" plato-fuse/Cargo.lock
  echo "Bumped plato-fuse: $current -> $next"
fi

# Re-lock worlds that depend on the SDK so their uv.lock stays in sync
failed_worlds=()
for world in ../worlds/*/; do
  [ ! -f "${world}pyproject.toml" ] && continue
  grep -q "plato-sdk-v2" "${world}pyproject.toml" || continue
  if uv lock --directory "$world"; then
    echo "Re-locked $(basename "$world")"
  else
    echo "Failed to re-lock $(basename "$world")" >&2
    failed_worlds+=("$world")
  fi
done

if ((${#failed_worlds[@]} > 0)); then
  echo "Error: Failed to re-lock the following worlds:" >&2
  for world in "${failed_worlds[@]}"; do
    echo "  - $(basename "$world")" >&2
  done
  exit 1
fi

git add VERSION ../worlds/*/uv.lock plato-fuse/Cargo.toml plato-fuse/Cargo.lock
