#!/usr/bin/env bash
set -euo pipefail

# Fargate task volumes are attached as root-owned directories.  Bootstrap only
# their mount points as root, then restart this entrypoint as the unprivileged
# browser user.  The browser, X server, stream plane, and benchmark never run as
# root.  Do not recursively chown /profiles: the EFS access point owns that tree.
if [[ "$(id -u)" == "0" ]]; then
  install -d -m 1777 -o root -g root /tmp
  install -d -m 1777 -o root -g root /tmp/.X11-unix
  install -d -m 0750 -o browser-worker -g browser-worker /home/browser-worker
  install -d -m 0700 -o browser-worker -g browser-worker \
    "${XDG_RUNTIME_DIR:-/tmp/browser-worker-runtime}"
  exec runuser --user browser-worker --preserve-environment -- "$0" "$@"
fi

worker_display="${DISPLAY:-:99}"
worker_width="${BROWSER_WORKER_WIDTH:-1440}"
worker_height="${BROWSER_WORKER_HEIGHT:-900}"
worker_port="${BROWSER_WORKER_PORT:-8002}"
display_number="${worker_display#:}"
mkdir -p "${XDG_RUNTIME_DIR:-/tmp/browser-worker-runtime}"
chmod 700 "${XDG_RUNTIME_DIR:-/tmp/browser-worker-runtime}"

# A hard container kill can leave Xvfb's marker files in the container layer.
# This is a fresh PID namespace, so no prior display process can still own them.
rm -f "/tmp/.X${display_number}-lock" "/tmp/.X11-unix/X${display_number}"

Xvfb "${worker_display}" -screen 0 "${worker_width}x${worker_height}x24" -nolisten tcp &
xvfb_pid=$!
server_pid=""

cleanup() {
  kill "${xvfb_pid}" 2>/dev/null || true
}

terminate_server() {
  # Forward ECS shutdown to Uvicorn so FastAPI closes Chromium cleanly before
  # the task exits and does not strand profile singleton markers on EFS.
  trap - TERM INT
  if [[ -n "${server_pid}" ]]; then
    kill -TERM "${server_pid}" 2>/dev/null || true
    wait "${server_pid}" 2>/dev/null || true
  fi
  exit 0
}

trap cleanup EXIT
trap terminate_server TERM INT

for _ in $(seq 1 50); do
  if xdpyinfo -display "${worker_display}" >/dev/null 2>&1; then
    break
  fi
  sleep 0.1
done

if ! xdpyinfo -display "${worker_display}" >/dev/null 2>&1; then
  echo "Browser display failed to start" >&2
  exit 1
fi

if [[ "${P6_BENCHMARK_MODE:-0}" == "1" ]]; then
  uv run --no-sync python -m matrx_scraper.cloud_browser.worker.p6_benchmark
  exit $?
fi

uv run --no-sync uvicorn matrx_scraper.cloud_browser.worker.server:app \
  --host 0.0.0.0 --port "${worker_port}" &
server_pid=$!
wait "${server_pid}"
