#!/usr/bin/env bash
# The desktop session of one Cloud Computer, started by the browser-worker
# entrypoint (as browser-worker) once the X display answers. Openbox manages
# windows; tint2 is the taskbar with terminal / files / Chrome launchers.
set -u

export DISPLAY="${DISPLAY:-:99}"
xsetroot -solid "#1f2937" 2>/dev/null || true
openbox --sm-disable >/tmp/openbox.log 2>&1 &

for _ in $(seq 1 50); do
  if xprop -root _NET_SUPPORTING_WM_CHECK 2>/dev/null | grep -q "window id"; then
    break
  fi
  sleep 0.1
done

tint2 -c /etc/xdg/cloud-computer/tint2rc >/tmp/tint2.log 2>&1 &

if xprop -root _NET_SUPPORTING_WM_CHECK 2>/dev/null | grep -q "window id"; then
  echo "cloud-computer desktop ready epoch_ms=$(date +%s%3N) wm=openbox"
else
  echo "cloud-computer desktop FAILED: window manager did not start" >&2
fi
wait
