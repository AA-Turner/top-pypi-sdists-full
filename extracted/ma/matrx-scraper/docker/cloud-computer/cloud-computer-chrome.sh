#!/usr/bin/env bash
# The desktop's Chrome icon. Every Chrome on this machine is an agent's browser,
# one window per browser profile (several named browsers share the machine,
# machine_browsers.py). The icon focuses one; each further tap moves to the
# NEXT open browser window, so a person reaches every browser from the icon.
# If a person had closed them, the icon asks the worker to open them again
# (same profiles, same window class). Never a second Chrome on one profile.
export DISPLAY="${DISPLAY:-:99}"
agent_class="matrx-agent-chrome"
worker_port="${BROWSER_WORKER_PORT:-8002}"

focus_agent_chrome() {
  local windows active window
  windows="$(xdotool search --onlyvisible --class "${agent_class}" 2>/dev/null)"
  [[ -n "${windows}" ]] || return 1
  active="$(xdotool getactivewindow 2>/dev/null || true)"
  # The window after the active one (wrapping); none active = the last one.
  window="$(printf '%s\n' "${windows}" | awk -v a="${active}" 'found{print; exit} $0==a{found=1}')"
  if [[ -z "${window}" ]]; then
    if printf '%s\n' "${windows}" | grep -qx "${active}"; then
      window="$(printf '%s\n' "${windows}" | head -n 1)"
    else
      window="$(printf '%s\n' "${windows}" | tail -n 1)"
    fi
  fi
  xdotool windowactivate "${window}" 2>/dev/null || xdotool windowmap "${window}" 2>/dev/null
  return 0
}

focus_agent_chrome && exit 0
curl -fsS -m 60 -X POST "http://127.0.0.1:${worker_port}/desktop/open-browser" >/dev/null 2>&1 || true
for _ in $(seq 1 50); do
  focus_agent_chrome && exit 0
  sleep 0.2
done
echo "the agent's Chrome did not open (no browser run on this machine?)" >&2
exit 1
