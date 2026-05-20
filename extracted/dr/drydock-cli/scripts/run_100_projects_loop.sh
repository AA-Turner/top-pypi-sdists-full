#!/usr/bin/env bash
# Continuous loop: drive drydock TUI against random 100-projects entries.
# One run at a time. JSON results land in
# /data3/drydock/.100_projects/runs/. The 30-min Claude wakeup reads
# those and fixes bugs it sees.
#
# Pause: `touch /data3/drydock/.pause_100_projects`
set -euo pipefail

cd /data3/drydock
LOG_DIR=/data3/drydock/.100_projects
mkdir -p "${LOG_DIR}"
LOOP_LOG="${LOG_DIR}/loop.log"
PAUSE_FLAG="/data3/drydock/.pause_100_projects"

# Single-instance lock so multiple invocations don't race.
exec 9>"${LOG_DIR}/loop.lock"
if ! flock -n 9; then
  echo "$(date -Iseconds) another instance is already running; exiting" >> "${LOOP_LOG}"
  exit 0
fi

echo "$(date -Iseconds) loop start (pid $$)" >> "${LOOP_LOG}"

trap 'echo "$(date -Iseconds) loop received SIGTERM, exiting" >> "${LOOP_LOG}"; exit 0' TERM INT

iter=0
while true; do
  iter=$((iter + 1))

  if [ -f "${PAUSE_FLAG}" ]; then
    echo "$(date -Iseconds) paused (flag=${PAUSE_FLAG})" >> "${LOOP_LOG}"
    sleep 60
    continue
  fi

  # Skip when the user's own drydock TUI is busy (active session log
  # modified in the last 60s). Multi-drydock is supported but we don't
  # want to fight the operator for GPU time.
  USER_SESSION=$(cat /home/bobef/.drydock/current_session.txt 2>/dev/null || true)
  if [ -n "${USER_SESSION}" ] && [ -f "${USER_SESSION}/messages.jsonl" ]; then
    AGE=$(($(date +%s) - $(stat -c %Y "${USER_SESSION}/messages.jsonl" 2>/dev/null || echo 0)))
    if [ "${AGE}" -lt 60 ]; then
      echo "$(date -Iseconds) iter=${iter} skip: operator TUI active (last write ${AGE}s ago)" >> "${LOOP_LOG}"
      sleep 30
      continue
    fi
  fi

  echo "$(date -Iseconds) iter=${iter} starting run" >> "${LOOP_LOG}"
  # 5-prompt iterative sequence (read→edit→run→debug→re-edit) needs
  # much longer than the prior 2-prompt 240s budget. Cap at ~15 min
  # per run; wrapper kill at 16 min so a hung iter doesn't stall the
  # loop.
  RUN_OUT=$(timeout 960 /home/bobef/miniconda3/bin/python3 scripts/run_100_projects.py --timeout-sec 900 2>&1 || true)
  echo "$(date -Iseconds) iter=${iter} done" >> "${LOOP_LOG}"
  echo "${RUN_OUT}" >> "${LOOP_LOG}"
  echo "---" >> "${LOOP_LOG}"

  # Brief pause so the next iteration doesn't immediately monopolize
  # the model server.
  sleep 30
done
