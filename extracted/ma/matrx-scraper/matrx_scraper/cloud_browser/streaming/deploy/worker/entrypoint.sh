#!/usr/bin/env bash
# Cloud Browser streaming worker entrypoint (WS-4 reference).
# Launches Xvfb + headed Chromium on a private display. The Selkies ENCODER is
# NOT started here — nothing streams by default (D-8). A control-plane signal
# (claimed takeover) starts capture/input; return/cancel stops it.
set -euo pipefail

DISPLAY="${DISPLAY:-:99}"
XVFB_W="${XVFB_W:-1280}"
XVFB_H="${XVFB_H:-800}"

echo "[worker] starting Xvfb on ${DISPLAY} at ${XVFB_W}x${XVFB_H}x24 (private, -nolisten tcp)"
Xvfb "${DISPLAY}" -screen 0 "${XVFB_W}x${XVFB_H}x24" -nolisten tcp &
XVFB_PID=$!

# Wait for the display.
for _ in $(seq 1 50); do
  if xdpyinfo -display "${DISPLAY}" >/dev/null 2>&1; then break; fi
  sleep 0.1
done

# The matrx-scraper Cloud Browser worker (WS-2/WS-5) launches and owns headed
# Chromium via Playwright launch_persistent_context against this DISPLAY, and
# runs the ordered command queue + the worker_input XTEST channel. It is invoked
# by the platform, not hardcoded here; for the standalone proof, any headed
# Chromium on ${DISPLAY} suffices.
echo "[worker] display ready; Chromium is launched by the Cloud Browser worker."
echo "[worker] Selkies encoder is ASLEEP until a takeover is claimed (D-8)."

# Keep the container alive; the control plane drives capture/input lifecycle.
wait "${XVFB_PID}"
