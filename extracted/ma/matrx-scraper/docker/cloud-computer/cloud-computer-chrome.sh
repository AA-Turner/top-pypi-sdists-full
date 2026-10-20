#!/usr/bin/env bash
# The desktop's Chrome icon. There is ONE Chrome on this machine: the agent's,
# on the person's profile. The icon focuses its window; if a person had closed
# it, the icon asks the worker to open it again (same profile, same window
# class) and focuses it once it appears. Never a second Chrome on one profile.
export DISPLAY="${DISPLAY:-:99}"
agent_class="matrx-agent-chrome"
worker_port="${BROWSER_WORKER_PORT:-8002}"

focus_agent_chrome() {
  local window
  window="$(xdotool search --onlyvisible --class "${agent_class}" 2>/dev/null | tail -n 1)"
  [[ -n "${window}" ]] || return 1
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
