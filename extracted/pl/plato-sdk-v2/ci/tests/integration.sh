#!/bin/bash
set -e
export PATH="$HOME/.local/bin:$PATH"
cd "$(dirname "$0")/../.."

echo "Running integration tests..."
echo "Note: Tests require PLATO_API_KEY environment variable"

# Run integration tests
# -q: quiet mode for clean CI logs
# -ra: show summary of all non-passed tests
uv run --frozen pytest tests/integration/test_sandbox.py -q -ra
