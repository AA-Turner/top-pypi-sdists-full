#!/usr/bin/env bash

set -e
set -x

# mypy mode
ruff check mode tests
ruff format mode tests --check
