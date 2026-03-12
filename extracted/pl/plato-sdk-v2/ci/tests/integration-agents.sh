#!/bin/bash
set -e
export PATH="$HOME/.local/bin:$PATH"
cd "$(dirname "$0")/../.."

# Skip unless agent test code or test runner changed
if ! echo "$CHANGED_FILES" | grep -qE "python-sdk/(plato/(cli/chronos/test/|agents/)|tests/integration/test_agent_integration|tests/integration/agent_test_world/)"; then
  echo "No agent test-related changes, skipping"
  exit 0
fi

echo "Running agent integration tests..."
uv run --frozen pytest tests/integration/test_agent_integration.py -q -ra
