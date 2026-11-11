#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0

# stop-gateway.sh: stop the E2E gateway started by start-gateway.sh, save its
# log, remove the sandbox containers, and remove the "e2e" gateway
# registration (and the active-gateway pointer when it still names "e2e").
#
# Usage: stop-gateway.sh [--state-dir <dir>]
#
# Writes <state-dir>/gateway.log. Safe to run when nothing is running. Runs
# every cleanup step even when one fails, then exits nonzero if any failed.
set -uo pipefail

state=${OPENSHELL_E2E_STATE:-${RUNNER_TEMP:-/tmp}/openshell-e2e}
[ "${1:-}" != --state-dir ] || state=${2:?--state-dir needs a path}
[ -f "$state/docker-compose.yml" ] || { echo "No E2E gateway state in $state."; exit 0; }

semver=$(sed 's/^v//' "$state/core-version" 2>/dev/null || echo latest)
compose() { IMAGE_TAG=$semver docker compose -p openshell-e2e -f "$state/docker-compose.yml" "$@"; }

failed=0
fail() { echo "stop-gateway: $*" >&2; failed=1; }

if compose logs --no-color --timestamps >"$state/gateway.log" 2>&1; then
  echo "Gateway log: $state/gateway.log"
else
  fail "could not save the gateway log; see $state/gateway.log"
fi

# The Docker driver labels sandbox and supervisor containers with core's
# openshell.ai/managed-by and openshell.ai/sandbox-namespace labels. Compose
# doesn't know about them, so remove them before taking the project down.
if ids=$(docker ps -aq \
  --filter label=openshell.ai/managed-by=openshell \
  --filter label=openshell.ai/sandbox-namespace=openshell); then
  # shellcheck disable=SC2086 # one container ID per word
  [ -z "$ids" ] || docker rm -f $ids >/dev/null || fail "could not remove sandbox containers"
else
  fail "could not list sandbox containers"
fi
compose down --volumes --remove-orphans >/dev/null || fail "docker compose down failed"

config_home=${XDG_CONFIG_HOME:-$HOME/.config}
rm -rf "$config_home/openshell/gateways/e2e" || fail "could not remove the e2e gateway registration"
if [ "$(cat "$config_home/openshell/active_gateway" 2>/dev/null)" = e2e ]; then
  rm -f "$config_home/openshell/active_gateway" || fail "could not remove the active-gateway pointer"
fi

if [ "$failed" -ne 0 ]; then
  echo "Gateway cleanup failed; the gateway or its sandboxes may still be running." >&2
  exit 1
fi
echo "Gateway stopped."
