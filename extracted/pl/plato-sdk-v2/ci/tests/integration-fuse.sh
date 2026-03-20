#!/bin/bash
# CI_WATCH: python-sdk/(plato/(cli/chronos/test/|transport/|fuse/)|tests/integration/test_plato_fuse|tests/integration/fuse_correctness_world/)
set -e
export PATH="$HOME/.local/bin:$PATH"
cd "$(dirname "$0")/../.."

# Skip unless fuse/transport or test runner code changed
if ! echo "$CHANGED_FILES" | grep -qE "python-sdk/(plato/(cli/chronos/test/|transport/|fuse/)|tests/integration/test_plato_fuse|tests/integration/fuse_correctness_world/)"; then
  echo "No FUSE-related changes, skipping"
  exit 0
fi

echo "Running FUSE correctness integration tests..."
uv run --frozen pytest tests/integration/test_plato_fuse_correctness.py -q -ra
