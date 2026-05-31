#!/usr/bin/env bash
# Harbor run watchdog. Detects stuck `harbor run` processes that have
# stopped making trial-level progress and kills them so the next
# operator-initiated run isn't blocked on a dead-but-not-dead process.
#
# Triggered every 10 minutes by cron (see scripts/install_cron.sh
# tail). Pause via: touch /data3/drydock/.pause_harbor_watchdog
#
# Definition of "stuck": there's a `harbor run` process older than
# STALL_MIN minutes whose job-output directory has NOT had a new
# `result.json` appear in the last STALL_MIN minutes. Use
# trial-result granularity rather than process CPU because harbor
# legitimately sits on a single trial for up to 15 min of agent time
# plus up to 30 min of env build for heavy task images (build-pmars,
# build-pov-ray, etc.) — but a SINGLE trial taking 2+ hours is the
# bug we're catching.
#
# Logs: /data3/drydock/logs/harbor_watchdog.log
# Telegram: same BOT_TOKEN / CHAT_ID as scripts/telegram_bot.py.

set -euo pipefail

PAUSE_FLAG=/data3/drydock/.pause_harbor_watchdog
LOG=/data3/drydock/logs/harbor_watchdog.log
JOBS_DIR=/data3/tbench_local/jobs
STALL_MIN=${HARBOR_WATCHDOG_STALL_MIN:-45}
PROC_MIN_AGE_MIN=${HARBOR_WATCHDOG_PROC_MIN_AGE_MIN:-30}

# Telegram (same creds as scripts/telegram_bot.py — repo-internal,
# not user-facing; rotation is on the operator's TODO).
BOT_TOKEN="8488479213:AAGd2tMUrqc-Xse14IQ6yfoMudAAal7odio"
CHAT_ID=8431425848

mkdir -p "$(dirname "$LOG")"

ts() { date -Iseconds; }
log() { echo "$(ts) $*" >> "$LOG"; }

[ -f "$PAUSE_FLAG" ] && { log "paused"; exit 0; }

telegram() {
    local msg="$1"
    curl -sS -X POST \
        --data-urlencode "chat_id=$CHAT_ID" \
        --data-urlencode "text=$msg" \
        "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
        > /dev/null 2>> "$LOG" || true
}

# Find harbor run processes (the inner python invocation, not the
# bash wrapper — that one's PID has a longer lineage).
mapfile -t harbor_pids < <(
    pgrep -af "harbor run" 2>/dev/null \
        | grep -E "python3?.*harbor.*run" \
        | awk '{print $1}'
)

if [ "${#harbor_pids[@]}" -eq 0 ]; then
    # Nothing to do — common case, no log line to keep the log small.
    exit 0
fi

for pid in "${harbor_pids[@]}"; do
    # Skip kernel-reaped or already-exiting PIDs.
    [ -d "/proc/$pid" ] || continue

    # How long has this process been alive?
    age_sec=$(awk '{print $1}' /proc/uptime | xargs -I{} bash -c "echo \$(({} - \$(awk '{print \$22/100}' /proc/$pid/stat 2>/dev/null || echo 999999)))" 2>/dev/null)
    if ! [[ "$age_sec" =~ ^[0-9]+$ ]]; then
        # Fallback: read etimes from ps.
        age_sec=$(ps -p "$pid" -o etimes= 2>/dev/null | xargs || echo 0)
    fi
    age_min=$((age_sec / 60))

    if [ "$age_min" -lt "$PROC_MIN_AGE_MIN" ]; then
        # Too young to be considered stuck — even heavy env builds
        # legitimately take 20-30 min.
        log "pid=$pid age=${age_min}m — under threshold ${PROC_MIN_AGE_MIN}m, skipping"
        continue
    fi

    # Find which --job-name this process is running. Job dirs live
    # under JOBS_DIR. We pull --job-name from the command line.
    job_name=$(tr '\0' ' ' < "/proc/$pid/cmdline" 2>/dev/null \
        | grep -oP -- '--job-name\s+\S+' \
        | awk '{print $2}' | head -1)
    if [ -z "$job_name" ]; then
        log "pid=$pid no --job-name in cmdline, skipping"
        continue
    fi

    job_dir="$JOBS_DIR/$job_name"
    if [ ! -d "$job_dir" ]; then
        log "pid=$pid job_dir missing: $job_dir"
        continue
    fi

    # How long since the last `result.json` (trial completion) landed?
    # find -mmin returns paths modified in the last N minutes; we
    # invert to detect "nothing new in last STALL_MIN minutes".
    recent_result=$(find "$job_dir" -mindepth 2 -maxdepth 3 \
        -name "result.json" -mmin -"$STALL_MIN" 2>/dev/null | head -1)

    trial_count=$(find "$job_dir" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)
    done_count=$(find "$job_dir" -mindepth 2 -maxdepth 3 -name "result.json" 2>/dev/null | wc -l)

    if [ -n "$recent_result" ]; then
        log "pid=$pid job=$job_name healthy: trials=$trial_count done=$done_count recent_result=$recent_result"
        continue
    fi

    log "STALL pid=$pid age=${age_min}m job=$job_name trials=$trial_count done=$done_count — no new result.json in ${STALL_MIN}m, killing"

    # Kill the harbor run process tree. Use -TERM first for a clean
    # shutdown (harbor cleans up Docker containers on SIGTERM); fall
    # back to -KILL after 30s if it's still alive.
    pkill -TERM -P "$pid" 2>/dev/null || true
    kill -TERM "$pid" 2>/dev/null || true
    for _ in $(seq 1 30); do
        [ -d "/proc/$pid" ] || break
        sleep 1
    done
    if [ -d "/proc/$pid" ]; then
        log "pid=$pid still alive after SIGTERM, sending SIGKILL"
        pkill -KILL -P "$pid" 2>/dev/null || true
        kill -KILL "$pid" 2>/dev/null || true
    fi

    telegram "🚨 harbor watchdog killed stuck run: $job_name
elapsed=${age_min}min, trials=$trial_count, done=$done_count.
No new result.json in ${STALL_MIN}min.
job dir: $job_dir"
done
