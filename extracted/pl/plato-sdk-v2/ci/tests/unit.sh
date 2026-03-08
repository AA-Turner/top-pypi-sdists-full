#!/bin/bash
set -e
export PATH="$HOME/.local/bin:$PATH"
cd "$(dirname "$0")/../.."

echo "Running unit tests..."

if echo "$CHANGED_FILES" | grep -qE "python-sdk/plato-fuse/"; then
  echo "plato-fuse changes detected, running Rust unit tests"
  cargo test --manifest-path plato-fuse/Cargo.toml
fi

uv run --frozen pytest tests/test_agents.py tests/test_worlds.py tests/test_v2_imports.py tests/test_transport_modes.py -v --tb=short --ignore-glob="**/test_chronos*" -k "not ChronosCallback"
