#!/bin/bash
# The pod wrapper (plato.gpu): runs the image's own start command and adds what
# every pod session needs and no game knows about.
#
#   POD_COMMAND            JSON array: the image's start command
#   POD_MCP_PORT           where the command serves MCP; GET /health says it is up
#   PLATO_MCP_TOKEN, PLATO_MCP_ADMIN_TOKEN, VNC_PASSWORD   secrets for the command
#   RECORDING_URL          presigned PUT the recording goes to when the pod ends
#   IDLE_TERMINATE_MINUTES no MCP call for this long ends the pod
#   RESOLUTION             WxH of the X display the command draws on (default 1280x720)
#   RUNPOD_API_KEY, RUNPOD_POD_ID   set by Runpod on every pod (a pod-scoped key,
#                          not the account's): how the pod ends itself
#
# Progress goes to /var/log/pod-boot.log (served by the command's noVNC web
# root when it has one). Needs bash, curl, ffmpeg and python3 in the image.
set -euo pipefail
RESOLUTION=${RESOLUTION:-1280x720}
RECORDING=/var/lib/recording.mp4
LOG=/var/log/pod-boot.log
RUNPOD=https://rest.runpod.io/v1
# A failed boot stays up this long for someone to read the log, then ends:
# an unusable pod must not bill until a person notices.
FAILED_BOOT_GRACE_SECONDS=600
step() { echo "[$(date -u +%H:%M:%S)] $*" | tee -a "$LOG"; }

# Every request has a time limit: a peer that accepts and never answers must
# not hold the boot limit, the idle check or the shutdown.
runpod() { curl -sS --max-time 30 -H "Authorization: Bearer $RUNPOD_API_KEY" "$@"; }
pod_gone() {
  # Runpod no longer knows the pod (404) or it is ended: the delete took.
  local body code
  body=$(runpod -w '\n%{http_code}' "$RUNPOD/pods/$RUNPOD_POD_ID" 2>/dev/null) || return 1
  code=${body##*$'\n'}
  [ "$code" = 404 ] && return 0
  printf '%s' "${body%$'\n'*}" | python3 -c 'import json, sys; sys.exit(0 if json.load(sys.stdin).get("desiredStatus") in ("EXITED", "TERMINATED") else 1)' 2>/dev/null
}
self_terminate() {
  # Ends this pod. The delete is retried every minute until Runpod says the
  # pod is gone; never returns while the pod still bills. The pull credential
  # minted for the pod (stored under the pod's name) is not touched here:
  # Runpod refuses to delete a credential while a pod names it, and this
  # pod is gone the moment its delete lands. The client's terminate drops
  # it afterwards; a pod that ends itself leaves it for the sweep
  # (``plato gpu pod down`` on a pod Runpod no longer knows is a no-op).
  if [ -z "${RUNPOD_API_KEY:-}" ] || [ -z "${RUNPOD_POD_ID:-}" ]; then
    step "cannot end this pod myself: RUNPOD_API_KEY/RUNPOD_POD_ID not set"
    return 1
  fi
  until pod_gone; do
    code=$(runpod -o /dev/null -w '%{http_code}' -X DELETE "$RUNPOD/pods/$RUNPOD_POD_ID" 2>/dev/null || echo 000)
    step "pod delete answered HTTP $code; confirming"
    pod_gone && break
    # The REST delete above is what the account's key uses; the pod-scoped
    # key Runpod sets on a pod was seen looping here for over an hour
    # (the pod kept billing). The GraphQL mutation is what runpodctl uses
    # from inside a pod, so it is tried as well on every round.
    reply=$(curl -sS --max-time 30 -H "Content-Type: application/json" \
      --data '{"query":"mutation { podTerminate(input: {podId: \"'"$RUNPOD_POD_ID"'\"}) }"}' \
      "https://api.runpod.io/graphql?api_key=$RUNPOD_API_KEY" 2>/dev/null || echo "unreachable")
    step "podTerminate answered: ${reply:0:200}"
    sleep 60
  done
  step "pod $RUNPOD_POD_ID ended"
}
failed_boot() {
  step "FAILED: $*; ending this pod in ${FAILED_BOOT_GRACE_SECONDS}s"
  sleep "$FAILED_BOOT_GRACE_SECONDS"
  self_terminate
  # Only reached without the env to end the pod: nothing more this script can do.
  sleep infinity
}
trap 'failed_boot "line $LINENO"' ERR

step "starting the image's command"
# NUL-separated: an argument may hold newlines (a script handed to bash -c).
mapfile -d '' -t COMMAND < <(python3 -c 'import json, os, sys; sys.stdout.write("\0".join(json.loads(os.environ["POD_COMMAND"])))')
"${COMMAND[@]}" >>"$LOG" 2>&1 &
COMMAND_PID=$!

step "waiting for MCP on :${POD_MCP_PORT}"
for _ in $(seq 1 180); do
  curl -sf --max-time 5 "localhost:${POD_MCP_PORT}/health" >/dev/null 2>&1 && break
  kill -0 "$COMMAND_PID" 2>/dev/null || failed_boot "the image's command exited early"
  sleep 2
done
curl -sf --max-time 5 "localhost:${POD_MCP_PORT}/health" >/dev/null || failed_boot "MCP never answered on :${POD_MCP_PORT}"

# The recording: a fragmented mp4 of the X display, playable as is if the pod
# dies mid-way, uploaded every 5 minutes and when the pod ends.
export DISPLAY=:0
start_recording() {
  ffmpeg -y -loglevel error -f x11grab -framerate 10 -video_size "$RESOLUTION" -i :0 \
    -c:v libx264 -preset veryfast -pix_fmt yuv420p -movflags +frag_keyframe+empty_moov "$RECORDING" >>"$LOG" 2>&1 &
  FFMPEG=$!
}
start_recording

upload() {
  curl -fsS --max-time 600 -X PUT -H "Content-Type: video/mp4" --data-binary "@$RECORDING" "$RECORDING_URL" >/dev/null 2>&1
}
finish() {
  # Flush the recording and hand it over before the pod goes away. The
  # recording is evidence, not state: three tries, then it is logged as lost.
  trap - TERM INT
  step "ending: uploading the recording"
  kill -INT "$FFMPEG" 2>/dev/null || true
  wait "$FFMPEG" 2>/dev/null || true
  for attempt in 1 2 3; do
    if upload; then step "recording uploaded"; return 0; fi
    step "recording upload failed (attempt $attempt)"; sleep 5
  done
  step "recording LOST: upload failed three times"
}
trap 'finish; exit 0' TERM INT

step "ready: MCP on :${POD_MCP_PORT}, recording ${RESOLUTION}"
minute=0
while true; do
  # A backgrounded sleep: bash runs a trap only once the foreground command
  # ends, so a plain `sleep 60` would hold a terminate's TERM for up to a
  # minute, past the grace period, and the recording would never go.
  sleep 60 & wait $!
  minute=$((minute + 1))
  # The image's command is the session: gone means over, however /admin/state reads.
  if ! kill -0 "$COMMAND_PID" 2>/dev/null; then
    step "the image's command exited: ending this pod"
    finish
    self_terminate
    sleep infinity
  fi
  # A dead recorder is restarted (the file is rewritten: footage before this
  # minute survives only in the last periodic upload, which is logged).
  if ! kill -0 "$FFMPEG" 2>/dev/null; then
    step "ffmpeg exited at minute ${minute}: restarting the recording (earlier footage: last periodic upload)"
    start_recording
  fi
  if [ $((minute % 5)) -eq 0 ]; then upload || step "periodic recording upload failed"; fi
  # /admin/state's idle_seconds, or "-" when the server does not answer or
  # the field is missing (logged: a pod that cannot read its idle time never ends itself).
  idle=$(curl -s --max-time 10 -H "Authorization: Bearer $PLATO_MCP_ADMIN_TOKEN" "localhost:${POD_MCP_PORT}/admin/state" \
    | python3 -c 'import json, sys; print(int(json.load(sys.stdin)["idle_seconds"]))' 2>/dev/null || echo "-")
  if [ "$idle" = "-" ]; then step "idle check failed: /admin/state unreadable"; fi
  if [ "$idle" != "-" ] && [ "$idle" -ge $((IDLE_TERMINATE_MINUTES * 60)) ]; then
    step "idle for ${idle}s: terminating this pod"
    finish
    self_terminate
    # Only reached without the env to end the pod: nothing more this script can do.
    sleep infinity
  fi
done
