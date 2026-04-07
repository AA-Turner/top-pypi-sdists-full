#!/usr/bin/env bash
set -eux

# shellcheck source=../activate_venv.sh
. ./scripts/activate_venv.sh

python -m mypy src scripts
python -m ruff check
python -m ruff format --check
