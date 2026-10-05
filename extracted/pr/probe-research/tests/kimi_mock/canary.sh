#!/usr/bin/env bash
# The Kimi Code canary: does the newest Kimi still work with Probe's plugins?
#
#   agent/tests/kimi_mock/canary.sh            # uses `kimi` on PATH
#
# Kimi Code ships about daily, auto-updates by default, and Probe relies on its
# internal plugin list and its hook protocol (agent/docs/adding-a-harness.md).
# This runs the real CLI against the scripted mock model (no account, no
# spend) with Probe's Kimi plugins installed the way `probe wizard` installs
# them, and fails loudly on the first thing that no longer holds:
#
#   1. Kimi is at least the registry's floor version;
#   2. the wizard can install into Kimi's plugin list (its layout is unchanged);
#   3. Kimi loads the plugins and runs their hooks: the session-start hook
#      records the Kimi process (how `probe` finds its session);
#   4. the guard's PreToolUse deny still stops a Write into the approvals folder;
#   5. the transcript is where Probe looks, in the protocol Probe parses.
#
# Everything lives in a scratch folder; nothing outside it is read or written.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
AGENT="$(cd "$HERE/../.." && pwd)"
PY="${PYTHON:-python3}"
EXPECTED_PROTOCOL="${KIMI_EXPECTED_PROTOCOL:-1.5}"

SCRATCH="$(mktemp -d)"
MOCK_PID=""
cleanup() { [ -n "$MOCK_PID" ] && kill "$MOCK_PID" 2>/dev/null || true; rm -rf "$SCRATCH"; }
trap cleanup EXIT
fail() { echo "KIMI CANARY FAILED: $*" >&2; exit 1; }

PORT="$("$PY" -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1", 0)); print(s.getsockname()[1])')"
MOCK_PORT="$PORT" node "$HERE/server.mjs" >"$SCRATCH/mock.log" 2>&1 &
MOCK_PID=$!

export HOME="$SCRATCH/home" KIMI_CODE_HOME="$SCRATCH/kimi"
export XDG_CONFIG_HOME="$SCRATCH/xdg/config" XDG_STATE_HOME="$SCRATCH/xdg/state" XDG_CACHE_HOME="$SCRATCH/xdg/cache"
export KIMI_CODE_NO_AUTO_UPDATE=1 KIMI_MODEL_NAME=mock-model KIMI_MODEL_API_KEY=canary
export KIMI_MODEL_PROVIDER_TYPE=openai KIMI_MODEL_BASE_URL="http://127.0.0.1:$PORT/v1"
export PROBE_KIMI_PLUGIN_SOURCE="$AGENT" PROBE_TELEMETRY=off PYTHONPATH="$AGENT/src"
mkdir -p "$HOME" "$SCRATCH/proj" "$XDG_STATE_HOME"

echo "kimi $(kimi --version </dev/null)"

# 1 + 2: the floor and the install the wizard performs.
"$PY" - <<'EOF' || fail "install into Kimi's plugin list"
import sys
from probe.cli import kimi_config
problem = kimi_config.version_floor_problem()
if problem:
    sys.exit(problem)
for plugin in ("probe-research", "probe-research-tap"):
    result = kimi_config.install_plugin(plugin)
    print(result.detail)
    if not result.ok:
        sys.exit(1)
EOF

# 3 + 4: one print-mode session: a Bash call, then a Write aimed at the
# approvals folder (the guard must deny it).
FORGED="$XDG_STATE_HOME/probe/approvals/answers/canary.json"
for _ in $(seq 1 50); do (exec 3<>/dev/tcp/127.0.0.1/"$PORT") 2>/dev/null && break; sleep 0.1; done
(cd "$SCRATCH/proj" && kimi -p "RUN: echo canary
WRITE: allowed.txt :: an ordinary file
WRITE: $FORGED :: {\"answer\": \"yes\"}
SAY: done" --output-format stream-json </dev/null >"$SCRATCH/run.jsonl" 2>"$SCRATCH/run.err") \
  || fail "kimi -p exited non-zero: $(tail -5 "$SCRATCH/run.err")"

ls "$XDG_STATE_HOME/probe/harness-processes/"*.json >/dev/null 2>&1 \
  || fail "no harness-process record: Kimi did not run the plugin's session-start hook"
[ ! -e "$FORGED" ] || fail "the guard let a Write into the approvals folder through"
grep -q "where the Probe daemon keeps the questions it holds" "$SCRATCH/run.jsonl" \
  || fail "the forged Write was not refused by Probe's guard (Kimi no longer honours the PreToolUse deny?)"
[ -f "$SCRATCH/proj/allowed.txt" ] || fail "an ordinary Write did not land: the guard refuses too much"

# 5: the transcript Probe captures, in the protocol Probe parses.
WIRE="$(ls "$KIMI_CODE_HOME"/sessions/*/session_*/agents/main/wire.jsonl 2>/dev/null | head -1)"
[ -n "$WIRE" ] || fail "no transcript at sessions/<wd>/session_<id>/agents/main/wire.jsonl"
PROTOCOL="$("$PY" -c 'import json,sys; print(json.loads(open(sys.argv[1]).readline()).get("protocol_version"))' "$WIRE")"
[ "$PROTOCOL" = "$EXPECTED_PROTOCOL" ] \
  || fail "Kimi's transcript protocol is $PROTOCOL, Probe parses $EXPECTED_PROTOCOL: a resumed older session is now rewritten in place, and capture stops for it (see the Kimi harness doc)"

echo "kimi canary: ok (protocol $PROTOCOL)"
