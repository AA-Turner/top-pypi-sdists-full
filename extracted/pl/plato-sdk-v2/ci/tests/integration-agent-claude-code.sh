#!/bin/bash
# CI_WATCH: python-sdk/(plato/(cli/chronos/test/|agents/)|tests/integration/test_agent_integration|tests/integration/agent_test_world/|tests/integration/configs/agent-claude-code)|agents/claude-code/
set -e
export PATH="$HOME/.local/bin:$PATH"
cd "$(dirname "$0")/../.."

# Skip unless agent test code, test runner, SDK agent code, or claude-code agent changed
if ! echo "$CHANGED_FILES" | grep -qE "python-sdk/(plato/(cli/chronos/test/|agents/)|tests/integration/test_agent_integration|tests/integration/agent_test_world/|tests/integration/configs/agent-claude-code)|agents/claude-code/"; then
  echo "No claude-code agent test-related changes, skipping"
  exit 0
fi

echo "Running claude-code agent integration tests..."
uv run --frozen pytest tests/integration/test_agent_integration.py::TestClaudeCodeAgent -q -ra --timeout=600
