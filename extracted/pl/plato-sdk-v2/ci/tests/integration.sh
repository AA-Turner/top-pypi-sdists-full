#!/bin/bash
# CI_WATCH: python-sdk/(plato/(worlds/(base|workspace|durable|checkpoint|runner|verifier)|workspace|sandbox)/|tests/integration/test_(sandbox|workspace))
set -e
export PATH="$HOME/.local/bin:$PATH"
cd "$(dirname "$0")/../.."

echo "Running integration tests (non-VM)..."
echo "Note: Tests require PLATO_API_KEY environment variable"

# Always run sandbox tests
TEST_FILES="tests/integration/test_sandbox.py"

# Only run workspace tests if workspace/world core files changed (not review models, config, etc.)
if echo "$CHANGED_FILES" | grep -qE "python-sdk/plato/(worlds/(base|workspace|durable|checkpoint|runner|verifier)|workspace)/"; then
  echo "Workspace-related changes detected, including workspace tests"
  TEST_FILES="$TEST_FILES tests/integration/test_workspace.py"
else
  echo "No workspace-related changes, skipping workspace tests"
fi

uv run --frozen pytest $TEST_FILES -q -ra
