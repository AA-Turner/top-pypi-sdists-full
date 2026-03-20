#!/bin/bash
# CI_WATCH: python-sdk/(plato/(worlds/(base|workspace|durable|checkpoint|runner|verifier)|workspace)/|plato/cli/chronos/test/|tests/integration/test_workspace_vm|tests/integration/workspace_test_world/)
set -e
export PATH="$HOME/.local/bin:$PATH"
cd "$(dirname "$0")/../.."

# Skip unless workspace/world core files or test runner code changed
if ! echo "$CHANGED_FILES" | grep -qE "python-sdk/(plato/(worlds/(base|workspace|durable|checkpoint|runner|verifier)|workspace)/|plato/cli/chronos/test/|tests/integration/test_workspace_vm|tests/integration/workspace_test_world/)"; then
  echo "No workspace VM-related changes, skipping"
  exit 0
fi

echo "Running workspace VM integration tests..."
uv run --frozen pytest tests/integration/test_workspace_vm.py -q -ra
