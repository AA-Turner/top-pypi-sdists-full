#!/bin/bash
set -e
export PATH="$HOME/.local/bin:$PATH"
cd "$(dirname "$0")/../.."

echo "Running unit tests..."
uv run --frozen pytest tests/test_agents.py tests/test_worlds.py tests/test_v2_imports.py -v --tb=short --ignore-glob="**/test_chronos*" -k "not ChronosCallback"
