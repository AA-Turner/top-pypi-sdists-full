#!/bin/bash
# CI_WATCH: python-sdk/(plato/(utils/audit|utils/tool_execution|agents/runtime/transport|worlds/workspace)|tests/(test_audit|integration/agent_audit_test_world|integration/configs/.*audit))
set -e
export PATH="$HOME/.local/bin:$PATH"
cd "$(dirname "$0")/../.."

# Skip unless audit-related code changed
if [ -n "$CHANGED_FILES" ] && ! echo "$CHANGED_FILES" | grep -qE "python-sdk/(plato/(utils/audit|utils/tool_execution|agents/runtime/transport|worlds/workspace)|tests/(test_audit|integration/agent_audit_test_world|integration/configs/.*audit))"; then
  echo "No audit-related changes, skipping"
  exit 0
fi

echo "Running audit attribution integration tests (all agents)..."

uv run plato chronos test tests/integration/configs/agent-audit-claude-code-test.json --verbose
