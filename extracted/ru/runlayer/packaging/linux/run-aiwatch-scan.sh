#!/bin/sh
# Runlayer AI Watch — all-users shadow-AI scan (Detect only).
#
# Installed at /usr/lib/runlayer/run-aiwatch-scan.sh (0755) and run as root
# every 15 minutes from /etc/cron.d/runlayer-aiwatch (parity with the macOS
# LaunchAgent StartInterval=900 and the Windows AIWatchScan task).
#
# Policy (mirrors the Windows all-users orchestrator in
# runlayer_cli/scan/windows_users.py):
#   * Overlap guard — cron stacks runs; skip, never queue.
#   * Unconfigured-fleet gate — without RUNLAYER_API_KEY, exit 0 quietly
#     before any scan child is spawned (no churn on unconfigured devices).
#   * Enumerate ALL passwd entries — no uid filtering and no shell filtering:
#     root, system, and service accounts are scanned too (explicit product
#     requirement). Only entries whose home directory exists are kept, and
#     shared homes are scanned once (dedupe by canonical path, first user wins).
#   * Each user is scanned in its own child process with dropped privileges;
#     one user's failure never aborts the loop, but the aggregate exit is
#     non-zero if any per-user scan failed.
#   * Child output is routed to syslog so cron never emails root.
#   * The org API key is exported into each scan child's environment — the
#     child needs it to submit findings. Each user can read the key from
#     their own child's /proc/<pid>/environ (owner-only) during the scan
#     window; that is the same exposure class as the user-readable managed
#     prefs (macOS) / HKLM value (Windows) that carry this key today. At
#     rest the key stays in the 0600 root-only credentials file.
#
# POSIX sh only (/bin/sh is dash on Debian) — no bashisms.

set -u

# Scan children inherit our cwd through runuser. Cron runs us with cwd=/root,
# which non-root users can't search, so any relative-path stat in a child
# fails EACCES. Run from / so every child starts in a world-searchable cwd.
cd /

# Overlap/update guard: hold one package-wide exclusive lock for this shell's
# lifetime. Keep locks under a root-only runtime directory so an unprivileged
# user cannot hold flock and suppress scans or security updates.
# Lock contention exits EX_TEMPFAIL (75), not 0: `aiwatch config sync` invokes
# this wrapper and must not report success when nothing ran. Cron ignores the
# exit code (output goes to syslog, so no cron mail either way).
EX_TEMPFAIL=75
umask 077
LOCK_DIR=/run/runlayer-aiwatch
mkdir -p "$LOCK_DIR" || exit 1
chmod 0700 "$LOCK_DIR" || exit 1
exec 9>"$LOCK_DIR/package.lock"
chmod 0600 "$LOCK_DIR/package.lock" || exit 1
flock -n 9 || exit $EX_TEMPFAIL

# Root-only credentials (0600): RUNLAYER_API_KEY, optional RUNLAYER_HOST.
# The API key must never live in the world-readable config.json.
CREDENTIALS_FILE=/etc/runlayer/aiwatch/credentials
if [ -f "$CREDENTIALS_FILE" ] && [ -r "$CREDENTIALS_FILE" ]; then
    . "$CREDENTIALS_FILE"
fi

# Unconfigured-fleet gate (parity with macOS): no org API key means this
# device has not been configured yet — exit quietly, before any scan runs.
if [ -z "${RUNLAYER_API_KEY:-}" ]; then
    exit 0
fi
export RUNLAYER_API_KEY
if [ -n "${RUNLAYER_HOST:-}" ]; then
    export RUNLAYER_HOST
fi

# Backend settings snapshot: as root (the cache is root-written), pull the
# dashboard-managed Detect settings into /var/lib/runlayer/aiwatch before the
# per-user fan-out so this run's scan children already see them. Best-effort:
# a refresh failure keeps the last-known-good snapshot and never blocks scans.
refresh_output=$(
    timeout -k 30 120 /usr/lib/runlayer/aiwatch/aiwatch config refresh 2>&1
)
if [ -n "$refresh_output" ]; then
    printf '%s\n' "$refresh_output" | logger -t runlayer-aiwatch
fi

rc=0
seen_homes=""

# Snapshot passwd to a temp file: `getent passwd | while read` would run the
# loop body in a subshell and lose rc/seen_homes; `done < file` does not.
passwd_list=$(mktemp) || exit 1
trap 'rm -f "$passwd_list"' EXIT
getent passwd >"$passwd_list"

while IFS=: read -r user _pw _uid _gid _gecos home _shell; do
    [ -n "$user" ] || continue
    [ -n "$home" ] || continue
    [ -d "$home" ] || continue

    # Dedupe by canonical home path: shared homes (e.g. several service
    # accounts pointing at /bin) are scanned once, first user wins.
    # readlink -f, not `cd && pwd -P`: cd needs execute on the home itself,
    # which fails for root on a 0700 root_squash NFS home — silently skipping
    # exactly the users the privilege-drop scan is meant to reach. readlink
    # only stats the entry via the (typically 755) parent. If even that fails,
    # fall back to the raw path — never silently exclude a user.
    canon_home=$(readlink -f -- "$home" 2>/dev/null) || canon_home=$home
    if printf '%s\n' "$seen_homes" | grep -Fxq -- "$canon_home"; then
        continue
    fi
    seen_homes="$seen_homes
$canon_home"

    # Privilege drop + per-user env; own child per user so one failure can't
    # poison the rest. stdin from /dev/null so the child can't consume the
    # passwd list this loop is reading. timeout -k guarantees a SIGKILL 30s
    # after the TERM so a wedged child can't hold the flock forever. runuser
    # opens a PAM session per user (one auth-log line each per run — same
    # class of noise as cron's own per-job session line); switch to setpriv
    # if a fleet finds that too chatty.
    scan_output=$(
        timeout -k 30 600 runuser -u "$user" -- \
            env HOME="$home" USER="$user" LOGNAME="$user" \
            /usr/lib/runlayer/aiwatch/aiwatch scan --quiet --username "$user" \
            </dev/null 2>&1
    )
    scan_rc=$?
    if [ -n "$scan_output" ]; then
        printf '%s\n' "$scan_output" | logger -t runlayer-aiwatch
    fi
    if [ "$scan_rc" -ne 0 ]; then
        logger -t runlayer-aiwatch "scan failed for user $user (rc=$scan_rc)"
        rc=1
    fi
done <"$passwd_list"

exit $rc
