#!/bin/bash
set -e
export PATH="$HOME/.local/bin:$PATH"
cd "$(dirname "$0")/.."

echo "Running ruff format..."
uv run --frozen ruff format .
echo "Running ruff check..."
uv run --frozen ruff check . --fix
echo "Running type check..."
uv run --frozen ty check plato/ --exclude 'plato/_generated/**'
