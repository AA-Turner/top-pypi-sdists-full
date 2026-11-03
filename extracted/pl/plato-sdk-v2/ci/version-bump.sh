#!/bin/bash
set -e
export PATH="$HOME/.local/bin:$PATH"
cd "$(dirname "$0")/.."

# DEV_FLAG is set by CI (empty for release, --dev for dev branches)
../.github/bump_version.sh VERSION $DEV_FLAG --mode VERSION

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

git add VERSION ../worlds/*/uv.lock
