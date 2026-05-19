#!/usr/bin/env bash
# Babysit the TUI capture + watcher. Run as a 1-min cron job. If
# either daemon is dead, relaunch it. Cheap (just ps + maybe spawn).
#
# Cron line (commented; install manually):
#   * * * * * /data3/drydock/scripts/tui_observability_keepalive.sh
set -euo pipefail

PY=/home/bobef/miniconda3/bin/python3
SCRIPTS=/data3/drydock/scripts
LOG_DIR=/data3/drydock/.tui_observability
mkdir -p "$LOG_DIR"

_alive() {
  # Match only python-interpreter processes whose argv starts with our
  # script path. pgrep -f matches the FULL command line, which also
  # matches shells that happen to mention the script name in their
  # history — a false positive we hit on first deploy.
  local name="$1"
  local hits
  hits=$(ps -eo pid,comm,args --no-headers 2>/dev/null \
    | awk -v py="$PY" -v p="$SCRIPTS/$name" '
        $2 ~ /^python/ {
          for (i = 3; i <= NF; i++) {
            if ($i == p) { print $1; next }
          }
        }') || true
  [ -n "$hits" ]
}

_launch() {
  local name="$1"
  local out="$LOG_DIR/${name%.py}.out"
  nohup "$PY" "$SCRIPTS/$name" >>"$out" 2>&1 &
  echo "$(date -Iseconds) launched $name pid=$!" >>"$LOG_DIR/keepalive.log"
}

if [ -f /data3/drydock/.pause_tui_observability ]; then
  exit 0
fi

# Capture
if ! _alive tui_capture.py; then
  _launch tui_capture.py
fi

# Watcher
if ! _alive tui_watch.py; then
  _launch tui_watch.py
fi
