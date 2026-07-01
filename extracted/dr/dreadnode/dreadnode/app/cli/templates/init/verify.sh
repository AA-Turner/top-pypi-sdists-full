#!/bin/bash
# Verification script — exit 0 if the challenge is solved, non-zero otherwise.
# See: https://docs.dreadnode.io/evaluations/verification/
#
# This script runs after the agent finishes. The `where` field in task.yaml
# controls where it runs:
#   - where: environment (default) — runs alongside task services. Use this to
#     check server-side state: query a database, curl a service, exec into a
#     container, inspect files on the service host.
#   - where: agent — runs on the machine where the agent ran. Use this to
#     validate what the agent produced (output files, JSON structure, results).
#
# Examples:
#
# # where: environment — check server-side state
# curl -sf http://localhost:8080/admin | grep -q "FLAG{" && exit 0
# exit 1
#
# # where: agent — check what the agent wrote
# RESULT=$(cat /tmp/result.txt 2>/dev/null)
# [[ "$RESULT" == "FLAG{expected}" ]] && exit 0
# exit 1

set -euo pipefail

# TODO: replace with your verification logic.
echo "verify.sh: not implemented yet" >&2
exit 1
