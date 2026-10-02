#!/usr/bin/env bash
# Run one environment of the opt-in environment suite against the RELEASED SDK.
#
#   agent/tests/environments/run.sh <env> [pytest args...]   one environment
#   agent/tests/environments/run.sh all   [pytest args...]   every environment, one venv
#
# The venv: $PROBE_ENV_VENV if set (reused as is -- several environments can
# share one), else agent/tests/environments/.venvs/<env>, built on first use
# with uv from <env>/requirements.txt (torch from the CPU wheel index) plus
# pytest. It holds `probe-research` from PyPI: that is what the customer's
# scripts import. The test harness itself imports this checkout's agent/src.
#
# Server: the agent suite's fake, served on loopback, unless PROBE_BASE_URL +
# PROBE_TOKEN + PROBE_E2E_PROJECT are exported (a real deployment).
# PROBE_ENV_CLOSE_WAIT_SEC (real server only) waits that long for a run whose
# lease was killed to be closed by the server (lease expiry is >= 180 s).
# PROBE_ENV_SDK_SRC=<tree>/agent/src runs the children on that SDK source
# instead of the released one (to check an unreleased fix).
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
agent="$(cd "$here/../.." && pwd)"
name="${1:?usage: run.sh <env|all> [pytest args...]}"
shift

if [ "$name" = "all" ]; then
  targets=()
  for d in "$here"/*/; do
    [ -f "$d/requirements.txt" ] && targets+=("tests/environments/$(basename "$d")")
  done
  reqs=$(cat "$here"/*/requirements.txt | sort -u)
else
  [ -f "$here/$name/requirements.txt" ] || {
    echo "no environment '$name'; have: $(cd "$here" && ls -d */requirements.txt | cut -d/ -f1 | tr '\n' ' ')" >&2
    exit 2
  }
  targets=("tests/environments/$name")
  reqs=$(cat "$here/$name/requirements.txt")
fi

venv="${PROBE_ENV_VENV:-$here/.venvs/$name}"
if [ ! -x "$venv/bin/python" ]; then
  uv venv "$venv" --python 3.12 -q
  if grep -qE '^torch([^a-zA-Z_]|$)' <<<"$reqs"; then
    VIRTUAL_ENV="$venv" uv pip install -q --index-url https://download.pytorch.org/whl/cpu torch
  fi
  mapfile -t pkgs <<<"$reqs"  # an array: `jax[cpu]` must not glob
  VIRTUAL_ENV="$venv" uv pip install -q "${pkgs[@]}" pytest pytest-timeout
fi

"$venv/bin/python" - <<'PY'
from importlib.metadata import version
print("probe-research", version("probe-research"), "(the SDK under test)")
PY

cd "$agent"
PROBE_ENV_TESTS=1 PROBE_ENV_PYTHON="$venv/bin/python" PYTHONPATH="$agent/src" \
  exec "$venv/bin/python" -m pytest "${targets[@]}" -p no:cacheprovider -p no:xdist "$@"
