#!/usr/bin/env bash
set -euo pipefail

SELF=$(readlink -f "${BASH_SOURCE[0]}")
DIR=${SELF%/*/*}

cd -- "$DIR"
if [[ ! -e ./venv ]]
then
  ./scripts/install_in_venv.sh
fi
source ./venv/bin/activate
python -m unittest discover -v ./test
