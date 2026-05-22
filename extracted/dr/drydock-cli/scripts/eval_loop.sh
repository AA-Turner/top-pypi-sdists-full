#!/usr/bin/env bash
# Real-evaluation loop. Rotates between three runners per the
# operator's 2026-05-19 spec:
#
#   lifecycle_runner.py     — 6-phase PRD→build→implement→modify→debug→expand
#   gauntlet_runner.py      — 9-level escalation from trivial to context-collapse
#   test_harness_runner.py  — operator's 52-case suite (cases.json), P1-only at v1
#
# Iters cycle modulo 3 so each runner gets equal airtime.
#
# Pause: touch /data3/drydock/.pause_eval_loop
# Single-instance via flock — cron retries this every minute and
# bails immediately if another copy is already running.

set -euo pipefail

cd /data3/drydock
LOG_DIR=/data3/drydock/.eval_loop
mkdir -p "${LOG_DIR}"
LOOP_LOG="${LOG_DIR}/loop.log"
PAUSE_FLAG="/data3/drydock/.pause_eval_loop"

exec 9>"${LOG_DIR}/loop.lock"
if ! flock -n 9; then
  exit 0
fi

echo "$(date -Iseconds) eval_loop start (pid $$)" >> "${LOOP_LOG}"
trap 'echo "$(date -Iseconds) eval_loop exit" >> "${LOOP_LOG}"; exit 0' TERM INT

iter=0
while true; do
  iter=$((iter + 1))

  if [ -f "${PAUSE_FLAG}" ]; then
    echo "$(date -Iseconds) paused" >> "${LOOP_LOG}"
    sleep 60
    continue
  fi

  # Yield when the operator's own TUI is active (avoid GPU contention).
  USER_SESSION=$(cat /home/bobef/.drydock/current_session.txt 2>/dev/null || true)
  if [ -n "${USER_SESSION}" ] && [ -f "${USER_SESSION}/messages.jsonl" ]; then
    AGE=$(($(date +%s) - $(stat -c %Y "${USER_SESSION}/messages.jsonl" 2>/dev/null || echo 0)))
    if [ "${AGE}" -lt 60 ]; then
      echo "$(date -Iseconds) iter=${iter} skip: operator TUI active (${AGE}s ago)" >> "${LOOP_LOG}"
      sleep 30
      continue
    fi
  fi

  # Rotate three runners. test_harness gets case 1 so a freshly-restarted
  # eval_loop fires it on its very first iter (operator wants real
  # cases.json scoring ASAP after restart).
  # Lifecycle ≈ 8-15 min, gauntlet ≈ 15-30 min, test-harness P1+P2 ≈ 30-50 min.
  case $((iter % 3)) in
    1) RUNNER="scripts/test_harness_runner.py"; TIMEOUT=7200; RUNNER_ARGS="" ;;
    2) RUNNER="scripts/lifecycle_runner.py"; TIMEOUT=1500; RUNNER_ARGS="" ;;
    0) RUNNER="scripts/gauntlet_runner.py"; TIMEOUT=2400; RUNNER_ARGS="" ;;
  esac

  # Real-time log for `tail -f`. Runner prints one line per phase/
  # level start + result; tee it live to live.log so the operator can
  # watch progress without parsing JSON.
  LIVE_LOG="${LOG_DIR}/live.log"
  {
    echo ""
    echo "=========================================================="
    echo "$(date -Iseconds) ITER ${iter}  ${RUNNER}"
    echo "=========================================================="
  } | tee -a "${LIVE_LOG}" >> "${LOOP_LOG}"

  set +e
  # shellcheck disable=SC2086  # we WANT word-splitting on RUNNER_ARGS
  timeout --kill-after=30 "${TIMEOUT}" /home/bobef/miniconda3/bin/python3 -u "${RUNNER}" ${RUNNER_ARGS} 2>&1 \
    | tee -a "${LIVE_LOG}" \
    | tail -60 >> "${LOOP_LOG}"
  set -e
  echo "$(date -Iseconds) iter=${iter} done" | tee -a "${LIVE_LOG}" >> "${LOOP_LOG}"
  echo "---" >> "${LOOP_LOG}"

  sleep 30
done
