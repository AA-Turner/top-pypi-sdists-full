#!/bin/bash
set -e
export PATH="$HOME/.local/bin:$PATH"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

rm -rf dist
uv build

# Publish to CodeArtifact first (immediate availability for internal consumers)
bash "$SCRIPT_DIR/deploy-ca.sh"

# Publish to PyPI (public distribution)
uv publish

# Publish experiment templates to Chronos (only changed templates)
# Use CHANGED_FILES from CI detect-changes (git diff HEAD~1 is unreliable after version-bump commits)
CHANGED=$(echo "$CHANGED_FILES" | grep "^python-sdk/plato/cli/templates/" || true)
if echo "$CHANGED" | grep -q "env-create-launch.json"; then
  echo "Publishing env-create-launch template..."
  uv run plato pm experiment env base push
fi
if echo "$CHANGED" | grep -q "env-fix-launch.json"; then
  echo "Publishing env-fix-launch template..."
  uv run plato pm experiment env fix push
fi
if echo "$CHANGED" | grep -q "datagen-launch.json"; then
  echo "Publishing datagen-launch template..."
  uv run plato pm experiment data base push
fi
