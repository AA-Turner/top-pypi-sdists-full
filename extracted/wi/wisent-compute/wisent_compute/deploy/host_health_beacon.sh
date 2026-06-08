#!/bin/bash
# Out-of-band host health beacon.
#
# Writes gs://wisent-compute/host_health/<host>.json every tick with the
# fields the wisent-enterprise /jobs page surfaces:
#   - host (short hostname)
#   - reported_at (ISO8601 UTC)
#   - disk_pct, disk_avail_gb (root filesystem)
#   - units: { <unit>: {state, restart_counter, since} }
#   - last_log: tail of the agent log (truncated)
#
# Why it exists: the wisent-agent itself only publishes capacity to
# gs://wisent-compute/capacity/ AFTER it successfully starts. A unit
# stuck in a systemd restart loop (the RTX workstation went 30+ hours
# in 3,645 restart attempts on 2026-05-09 because pip self-upgrade hit
# a full disk) never publishes capacity, so the dashboard's "stale
# agents" check misses it. This beacon runs out-of-band so the
# dashboard can show the failure.
#
# Run via systemd timer (Linux) or launchd LaunchAgent (macOS); the
# tick interval should be ~60s.

set -u

PROJECT="wisent-480400"
BUCKET="wisent-compute"
UNITS_TO_WATCH="${WC_HEALTH_UNITS:-wisent-agent.service}"
LOG_PATHS="${WC_HEALTH_LOGS:-/var/log/wisent-agent.log}"
HOST_SLUG=$(/bin/hostname -s 2>/dev/null | /usr/bin/tr '[:upper:]' '[:lower:]')

# Discover gcloud (the GCP SDK is at different paths on Linux/macOS).
GCLOUD_BIN=""
for cand in /opt/homebrew/share/google-cloud-sdk/bin/gcloud \
            /usr/local/share/google-cloud-sdk/bin/gcloud \
            /home/ubuntu/google-cloud-sdk/bin/gcloud \
            "$(command -v gcloud 2>/dev/null)"; do
    if [ -n "$cand" ] && [ -x "$cand" ]; then GCLOUD_BIN="$cand"; break; fi
done
if [ -z "$GCLOUD_BIN" ]; then
    echo "host_health_beacon: no gcloud found; aborting" >&2
    exit 1
fi

reported_at=$(/bin/date -u +%Y-%m-%dT%H:%M:%SZ)

# Root fs usage
disk_line=$(/bin/df -k / 2>/dev/null | /usr/bin/awk 'NR==2 {print $3, $4, $5}')
read -r disk_used_kb disk_avail_kb disk_pct_str <<<"$disk_line"
disk_pct="${disk_pct_str%%%}"
# Avail in GB (rounded down).
disk_avail_gb=$(( ${disk_avail_kb:-0} / 1024 / 1024 ))

reread_root_disk() {
    disk_line=$(/bin/df -k / 2>/dev/null | /usr/bin/awk 'NR==2 {print $3, $4, $5}')
    read -r disk_used_kb disk_avail_kb disk_pct_str <<<"$disk_line"
    disk_pct="${disk_pct_str%%%}"
    disk_avail_gb=$(( ${disk_avail_kb:-0} / 1024 / 1024 ))
}

active_extraction_has_open_under() {
    prefix="$1"
    for p in $(/usr/bin/pgrep -f "wisent.scripts.activations.extract_and_upload" 2>/dev/null || true); do
        for fd in /proc/"$p"/fd/*; do
            target=$(/usr/bin/readlink "$fd" 2>/dev/null || true)
            case "$target" in
                "$prefix"/*) return 0 ;;
            esac
        done
    done
    return 1
}

remove_cache_if_idle() {
    target="$1"
    [ -e "$target" ] || return 0
    if ! active_extraction_has_open_under "$target"; then
        /bin/rm -rf "$target" 2>/dev/null || true
    fi
}

# Self-heal: when disk is 90%+ full AND the wisent-agent unit has been
# stuck for at least one restart, evict caches before reporting. Without
# this the agent restart-loops forever on a full disk (the workstation
# spent 30+ hours in a 3,645-restart loop on 2026-05-09 with pip-upgrade
# failing on a 46GB HF cache). The eviction targets are non-canonical
# state: HF datasets/snapshots, wheel cache, wisent corrupt pair-text
# cache. All are reproducible from the upstream source on next access.
SELF_HEAL_DISK_PCT_THRESHOLD=85
HOME_DIR="${HOME:-/home/ubuntu}"
primary_unit="${UNITS_TO_WATCH%%,*}"

# Self-heal a stopped agent even when disk is not critically full. The
# old self-heal only restarted when disk_pct >= 85, which left the box
# idle if the agent exited cleanly or got stopped while disk had already
# recovered below that threshold. This beacon is intentionally out of
# band; if it can report "inactive", it can also restart the service.
if ! /usr/bin/systemctl is-active "$primary_unit" >/dev/null 2>&1; then
    /usr/bin/systemctl restart "$primary_unit" >/dev/null 2>&1 || true
fi

if [ "${disk_pct:-0}" -ge "$SELF_HEAL_DISK_PCT_THRESHOLD" ]; then
    # Only run if wisent-agent is NOT actively serving (state != active).
    if ! /usr/bin/systemctl is-active "$primary_unit" >/dev/null 2>&1; then
        for tgt in "$HOME_DIR/.cache/huggingface/hub" \
                   "$HOME_DIR/.cache/pip" \
                   "$HOME_DIR/.wisent_cache" \
                   /root/.cache/huggingface/hub \
                   /root/.cache/pip; do
            [ -d "$tgt" ] && /bin/rm -rf "$tgt" 2>/dev/null || true
        done
        # Trigger a fresh systemd restart so the agent's pip ExecStartPre
        # runs on the now-cleaned disk.
        /usr/bin/systemctl restart "$primary_unit" >/dev/null 2>&1 || true
        # Re-read disk after eviction so the same beacon tick reports
        # the post-heal state.
        reread_root_disk
    fi
fi

# Clean known stale top-level /tmp payloads under root-disk pressure.
# Active jobs keep logs under /tmp/wc-<jid>/; do not touch those dirs.
# The stale files observed on ubuntu-server were /tmp/file* sort/tmp
# chunks and old /tmp/ZIT-*.safetensors files. If any active extraction
# process has one open, skip the cleanup and only report disk state.
if [ "${disk_pct:-0}" -ge 80 ] || [ "${disk_avail_gb:-999999}" -lt 30 ]; then
    open_tmp_junk=0
    for p in $(/usr/bin/pgrep -f "wisent.scripts.activations.extract_and_upload" 2>/dev/null || true); do
        for fd in /proc/"$p"/fd/*; do
            target=$(/usr/bin/readlink "$fd" 2>/dev/null || true)
            case "$target" in
                /tmp/file*|/tmp/ZIT-*.safetensors) open_tmp_junk=1 ;;
            esac
        done
    done
    if [ "$open_tmp_junk" -eq 0 ]; then
        /usr/bin/find /tmp -xdev -maxdepth 1 -type f \
            \( -name "file*" -o -name "ZIT-*.safetensors" \) -delete 2>/dev/null || true
        reread_root_disk
    fi
fi

# Safe cache/log cleanup for the root filesystem. These are reproducible
# caches or bounded systemd journals; active extraction open-FD checks
# prevent deleting cache trees currently being read by a running job.
if [ "${disk_pct:-0}" -ge 80 ] || [ "${disk_avail_gb:-999999}" -lt 30 ]; then
    remove_cache_if_idle "$HOME_DIR/.cache/huggingface/xet"
    remove_cache_if_idle "$HOME_DIR/.cache/pip"
    remove_cache_if_idle "$HOME_DIR/.cache/vllm"
    remove_cache_if_idle /root/.cache/huggingface/xet
    remove_cache_if_idle /root/.cache/pip
    /usr/bin/journalctl --vacuum-size=512M >/dev/null 2>&1 || true
    reread_root_disk
fi

# systemctl unit states (one entry per UNITS_TO_WATCH item, comma-sep).
units_json=""
for unit in ${UNITS_TO_WATCH//,/ }; do
    if /usr/bin/systemctl is-active "$unit" >/dev/null 2>&1; then
        state="active"
    elif /usr/bin/systemctl is-failed "$unit" >/dev/null 2>&1; then
        state="failed"
    else
        state="inactive"
    fi
    # Restart counter: parse from `systemctl show -p NRestarts`.
    n_restarts=$(/usr/bin/systemctl show -p NRestarts --value "$unit" 2>/dev/null || echo "?")
    since=$(/usr/bin/systemctl show -p ActiveEnterTimestamp --value "$unit" 2>/dev/null || echo "?")
    if [ -n "$units_json" ]; then units_json="$units_json,"; fi
    units_json="$units_json\"$unit\":{\"state\":\"$state\",\"n_restarts\":\"$n_restarts\",\"active_since\":\"$since\"}"
done

# Last log lines (truncate to 4 KB).
last_log=""
for p in ${LOG_PATHS//,/ }; do
    if [ -r "$p" ]; then
        last_log=$(/usr/bin/tail -c 4096 "$p" 2>/dev/null \
            | /usr/bin/python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))')
        break
    fi
done
[ -z "$last_log" ] && last_log='""'

# Top disk consumers under $HOME and /var, capped to 10 each, so the
# operator can see what is filling the disk without needing to SSH in.
# Only computed when disk remains tight after cleanup; avoids running du
# on every beacon tick once cleanup has restored breathing room.
top_consumers='[]'
if [ "${disk_pct:-0}" -ge 80 ] || [ "${disk_avail_gb:-999999}" -lt 15 ]; then
    top_consumers=$(
        for p in "$HOME_DIR" "$HOME_DIR/.local" "$HOME_DIR/.cache" \
                 "$HOME_DIR/.cache/huggingface" "$HOME_DIR/.cache/huggingface/xet" \
                 "$HOME_DIR/.cache/pip" "$HOME_DIR/.cache/vllm" \
                 "$HOME_DIR/.rustup" "$HOME_DIR/google-cloud-sdk" \
                 "$HOME_DIR/compute.wisent.com" "$HOME_DIR/.cargo" \
                 /var /var/log /var/log/journal /var/cache /var/lib /opt /tmp; do
            [ -e "$p" ] && /usr/bin/du -s -h "$p" 2>/dev/null
        done | /usr/bin/sort -hr \
          | /usr/bin/python3 -c '
import json, sys
out = []
for line in sys.stdin:
    parts = line.strip().split(None, 1)
    if len(parts) == 2:
        out.append({"size": parts[0], "path": parts[1]})
        if len(out) >= 20:
            break
print(json.dumps(out))
' 2>/dev/null
    )
    [ -z "$top_consumers" ] && top_consumers='[]'
fi

tmpfile=$(/usr/bin/mktemp)
cat > "$tmpfile" <<EOF
{
  "host": "${HOST_SLUG}",
  "reported_at": "${reported_at}",
  "disk_pct": ${disk_pct:-0},
  "disk_avail_gb": ${disk_avail_gb:-0},
  "units": {${units_json}},
  "top_consumers": ${top_consumers},
  "last_log": ${last_log}
}
EOF

"$GCLOUD_BIN" --quiet --project="$PROJECT" storage cp \
    "$tmpfile" "gs://$BUCKET/host_health/${HOST_SLUG}.json" >/dev/null 2>&1
rm -f "$tmpfile"
