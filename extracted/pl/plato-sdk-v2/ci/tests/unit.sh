#!/bin/bash
set -e
export PATH="$HOME/.local/bin:$PATH"
cd "$(dirname "$0")/../.."

echo "Running unit tests..."

if echo "$CHANGED_FILES" | grep -qE "python-sdk/plato-fuse/"; then
  echo "plato-fuse changes detected, running Rust unit tests"
  cargo test --manifest-path plato-fuse/Cargo.toml
fi

uv run --frozen pytest tests -v --tb=short -m "not integration" --ignore=tests/integration --ignore=tests/test_tools_openhands_integration.py -n 8 --dist=loadfile
