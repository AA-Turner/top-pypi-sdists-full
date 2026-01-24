#!/usr/bin/env bash

echo "running pybind11-stubgen $@"
pybind11-stubgen $@
if command -v ruff >/dev/null 2>&1 && [ -x "$(command -v ruff)" ]; then
  echo "ruff check and fix:"
  ruff check --fix --select I,D207,D208,D209,D212,PYI009 stubs/tango/__init__.pyi stubs/tango/_tango/__init__.pyi
  echo "ruff format:"
  ruff format stubs/tango/__init__.pyi stubs/tango/_tango/__init__.pyi
else
  echo "ruff not installed - skipping checks and fixes"
fi
