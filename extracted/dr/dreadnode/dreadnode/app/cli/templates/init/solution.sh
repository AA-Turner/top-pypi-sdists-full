#!/bin/bash
# Solution script — reference implementation that solves the task.
# See: https://docs.dreadnode.io/evaluations/tasks/
#
# Contract (TSK-SOL-001..002):
#   - Used by `dn task validate --smoke` to prove the task is solvable.
#   - Never exposed to agents during evaluation.
#   - Should leave the task in a "solved" state — verify.sh must pass after
#     this script runs.
#
# The smoke test lifecycle:
#   1. Boot compose
#   2. Run verify.sh — must FAIL (unsolved task must not pass)
#   3. Run solution.sh
#   4. Run verify.sh — must PASS (solution must produce a passing state)

set -euo pipefail

# TODO: replace with your reference solution.
echo "solution.sh: not implemented yet" >&2
exit 1
