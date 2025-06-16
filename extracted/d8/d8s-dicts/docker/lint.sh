#!/usr/bin/env bash

set -euxo pipefail

echo "Running linters and formatters..."

isort d8s_dicts/ tests/

black d8s_dicts/ tests/

mypy d8s_dicts/ tests/

pylint --fail-under 9 d8s_dicts/*.py

flake8 d8s_dicts/ tests/

bandit -r d8s_dicts/

# we run black again at the end to undo any odd changes made by any of the linters above
black d8s_dicts/ tests/
