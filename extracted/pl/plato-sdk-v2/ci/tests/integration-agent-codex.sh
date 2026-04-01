#!/bin/bash
# CI_WATCH: python-sdk/(tests/integration/test_agent_integration|tests/integration/agent_test_world/|tests/integration/configs/agent-codex)|agents/codex/
set -e
export PATH="$HOME/.local/bin:$PATH"
cd "$(dirname "$0")/../.."

# Skip unless codex agent code or codex-specific test configs changed
if ! echo "$CHANGED_FILES" | grep -qE "python-sdk/(tests/integration/test_agent_integration|tests/integration/agent_test_world/|tests/integration/configs/agent-codex)|agents/codex/"; then
  echo "No codex agent test-related changes, skipping"
  exit 0
fi

echo "Running codex agent integration tests..."
uv run --frozen pytest tests/integration/test_agent_integration.py::TestCodexAgent -q -ra --timeout=600
