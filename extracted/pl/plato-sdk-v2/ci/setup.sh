#!/bin/bash
set -e

if ! command -v uv &> /dev/null; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi
export PATH="$HOME/.local/bin:$PATH"

cd "$(dirname "$0")/.."
uv sync --extra dev
