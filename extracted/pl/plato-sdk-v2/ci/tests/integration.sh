#!/bin/bash
set -e
export PATH="$HOME/.local/bin:$PATH"
cd "$(dirname "$0")/../.."

echo "Running integration tests..."
echo "Note: Tests require PLATO_API_KEY environment variable"

# Always run sandbox tests
TEST_FILES="tests/integration/test_sandbox.py"

# Only run workspace tests if workspace/world core files changed
if echo "$CHANGED_FILES" | grep -qE "python-sdk/plato/(worlds|workspace)/"; then
  echo "Workspace-related changes detected, including workspace tests"
  TEST_FILES="$TEST_FILES tests/integration/test_workspace.py"
else
  echo "No workspace-related changes, skipping workspace tests"
fi

# Run FUSE correctness tests if fuse or transport code changed
if echo "$CHANGED_FILES" | grep -qE "python-sdk/(plato-fuse/|plato/agents/runtime/transport)"; then
  echo "FUSE/transport changes detected, including FUSE correctness tests"
  TEST_FILES="$TEST_FILES tests/integration/test_plato_fuse_correctness.py"
else
  echo "No FUSE/transport changes, skipping FUSE correctness tests"
fi

# -q: quiet mode for clean CI logs
# -ra: show summary of all non-passed tests
uv run --frozen pytest $TEST_FILES -q -ra
