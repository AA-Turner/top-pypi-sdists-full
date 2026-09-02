#!/bin/sh
# Runlayer AI Watch — container all-users shadow-AI scan (Detect only).
#
# Container analog of the .deb/.rpm cron wrapper packaging/linux/run-aiwatch-scan.sh.
# Ships as the ENTRYPOINT of the AI Watch scanner image; scans the host user
# homes that are bind-mounted into the container (standalone `docker run` today,
# a K8s DaemonSet/CronJob in a later chunk).
#
# Policy (mirrors run-aiwatch-scan.sh and the Windows all-users orchestrator in
# runlayer_cli/scan/windows_users.py):
#   * Overlap guard — never queue a second concurrent pass; skip.
#   * Unconfigured-fleet gate — without RUNLAYER_API_KEY (docker -e / K8s
#     Secret) exit 0 quietly before any scan child is spawned.
#   * Enumerate ALL passwd entries — no uid filtering and no shell filtering:
#     root, system, and service accounts are scanned too (explicit product
#     requirement). Only entries whose (bind-mounted) home exists are kept, and
#     shared homes are scanned once (dedupe by canonical path, first user wins).
#   * Each user is scanned in its own child with privileges dropped by NUMERIC
#     uid/gid (the container's passwd db has none of the host users, so setpriv
#     is driven by number, not name). One user's failure never aborts the loop;
#     the aggregate exit is non-zero if any per-user scan failed.
#   * Output goes to stdout (container-native logging) with a per-user prefix —
#     no syslog/logger dependency.
#
# Host mapping. The host's passwd is read from RUNLAYER_HOST_PASSWD (default
# /host/etc/passwd). Home paths in that passwd are host-absolute (e.g.
# /home/alice); when the host root is bind-mounted under a prefix (e.g. -v
# /:/host:ro) set RUNLAYER_HOST_HOME_PREFIX=/host so /home/alice resolves to
# /host/home/alice inside the container. Default prefix is empty (homes mounted
# at their real paths). If the host passwd is unreadable we fall back to the
# container's own `getent passwd`, so a minimal `docker run` with a single home
# mounted still works.
#
# Env knobs:
#   RUNLAYER_API_KEY          (required) org API key; empty ⇒ quiet exit 0.
#   RUNLAYER_HOST_PASSWD      host passwd file (default /host/etc/passwd).
#   RUNLAYER_HOST_GROUP       host group file (default /host/etc/group). Used to
#                             restore each user's supplementary groups on the
#                             setpriv drop (parity with runuser/initgroups in the
#                             .deb wrapper) so group-readable files — 0770 shared
#                             project dirs, group-owned homes — are still scanned.
#                             Unreadable/missing ⇒ falls back to --clear-groups
#                             (primary gid only).
#   RUNLAYER_HOST_HOME_PREFIX prefix prepended to passwd home paths (default "").
#   RUNLAYER_SCAN_INTERVAL    loop sleep seconds between passes (default 900).
#   RUNLAYER_RUN_ONCE=1       single pass then exit (also via the --once arg).
#   RUNLAYER_SCAN_TIMEOUT     per-user scan timeout seconds (default 600).
#   RUNLAYER_AIWATCH_BIN      scanner binary (default the bundled onedir exe).
#   RUNLAYER_HEARTBEAT_FILE   touched at loop start and after every pass
#                             (default /run/runlayer-aiwatch-heartbeat). A K8s
#                             exec liveness probe checks its mtime to detect a
#                             wedged loop.
#   RUNLAYER_SCAN_LOCK        overlap-guard lock file (default /run/...). The lock
#                             is container-local: it stops overlapping passes
#                             within THIS container. One-scanner-per-host comes
#                             from the deployment shape (DaemonSet = one pod per
#                             node; CronJob concurrencyPolicy: Forbid). If you
#                             run multiple standalone containers on one host,
#                             point this at a shared mounted volume.
# RUNLAYER_HOST / RUNLAYER_HOSTNAME / RUNLAYER_MACHINE_ID_PATH / RUNLAYER_DEVICE_ID
# are consumed by the scanner itself and simply passed through the env.
#
# POSIX sh only (image runtime is debian:12-slim, /bin/sh is dash) — no bashisms.

set -u

PASSWD_SRC="${RUNLAYER_HOST_PASSWD:-/host/etc/passwd}"
GROUP_SRC="${RUNLAYER_HOST_GROUP:-/host/etc/group}"
HOME_PREFIX="${RUNLAYER_HOST_HOME_PREFIX:-}"
# Scan children derive paths under the mounted prefix; the scanner strips it
# from submitted paths so findings show real HOST paths (/home/alice/...),
# identical to a native scan of the same machine.
if [ -n "$HOME_PREFIX" ]; then
    export RUNLAYER_STRIP_PATH_PREFIX="$HOME_PREFIX"
fi
INTERVAL="${RUNLAYER_SCAN_INTERVAL:-900}"
SCAN_TIMEOUT="${RUNLAYER_SCAN_TIMEOUT:-600}"
AIWATCH_BIN="${RUNLAYER_AIWATCH_BIN:-/usr/lib/runlayer/aiwatch/aiwatch}"
LOCK_FILE="${RUNLAYER_SCAN_LOCK:-/run/runlayer-aiwatch-scan.lock}"
HEARTBEAT_FILE="${RUNLAYER_HEARTBEAT_FILE:-/run/runlayer-aiwatch-heartbeat}"

heartbeat() {
    # Best-effort: a read-only /run must not kill the loop.
    touch "$HEARTBEAT_FILE" 2>/dev/null || :
}

log() {
    printf '%s %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*"
}

# --once arg or RUNLAYER_RUN_ONCE=1 ⇒ a single pass (K8s CronJob); otherwise
# loop forever (DaemonSet / plain `docker run`).
run_once=0
case "${RUNLAYER_RUN_ONCE:-}" in
1 | true | TRUE | yes | YES) run_once=1 ;;
esac
for arg in "$@"; do
    case "$arg" in
    --once) run_once=1 ;;
    esac
done

# Unconfigured-fleet gate (parity with the cron wrapper + macOS): no org API
# key means this deployment is not configured — exit quietly before any scan.
if [ -z "${RUNLAYER_API_KEY:-}" ]; then
    log "RUNLAYER_API_KEY not set — unconfigured; exiting 0 without scanning."
    exit 0
fi
export RUNLAYER_API_KEY
[ -n "${RUNLAYER_HOST:-}" ] && export RUNLAYER_HOST

# Overlap guard: hold an exclusive lock for the lifetime of this process; a
# concurrent pass (a second `docker run`, or a slow pass still in flight) skips
# instead of queueing. Pick a writable lock path without tripping `set -u` /
# killing the shell on a failed exec redirection.
for candidate in "$LOCK_FILE" /tmp/runlayer-aiwatch-scan.lock; do
    if (: >"$candidate") 2>/dev/null; then
        LOCK_FILE="$candidate"
        break
    fi
done
exec 9>"$LOCK_FILE"
flock -n 9 || {
    log "another scan pass holds $LOCK_FILE; skipping."
    exit 0
}

# Scan every existing host home once, with a per-user numeric-uid privilege
# drop. Returns non-zero if any per-user scan failed.
run_pass() {
    pass_rc=0
    seen_homes=""
    scanned_count=0
    skipped_unmounted=0

    # Snapshot passwd to a temp file: piping into `while read` runs the loop in
    # a subshell and loses pass_rc/seen_homes; `done < file` keeps them.
    passwd_list=$(mktemp) || return 1
    if [ -n "$PASSWD_SRC" ] && [ -r "$PASSWD_SRC" ]; then
        cat "$PASSWD_SRC" >"$passwd_list"
    else
        log "host passwd $PASSWD_SRC unreadable — falling back to container getent passwd."
        getent passwd >"$passwd_list" 2>/dev/null || : >"$passwd_list"
    fi

    while IFS=: read -r user _pw uid gid _gecos home _shell; do
        [ -n "$user" ] || continue
        [ -n "$uid" ] || continue
        [ -n "$gid" ] || continue
        [ -n "$home" ] || continue

        # Bind-mounted home: passwd home is host-absolute; prepend the mount
        # prefix so /home/alice ⇒ ${PREFIX}/home/alice inside the container.
        # A home that exists in the host passwd but is NOT under the mounted
        # set is a coverage gap — log it (observable, so operators know to add
        # a mount for that prefix) instead of dropping the user silently.
        resolved_home="${HOME_PREFIX}${home}"
        if [ ! -d "$resolved_home" ]; then
            # Well-known non-home sentinels (nobody, daemon, www-data, …) never
            # hold user data — skip them silently as the old behavior did, so the
            # skip log stays signal (genuine unmounted user homes) and doesn't
            # spam a line per system account every pass.
            case "$home" in
            "" | / | /nonexistent | /dev/null | /bin | /sbin | /usr/sbin | /run | /proc | /var/run)
                continue
                ;;
            esac
            log "skipping user=$user: home $home not present under the mounted set ($resolved_home missing) — add a mount for that prefix if this user should be scanned"
            skipped_unmounted=$((skipped_unmounted + 1))
            continue
        fi

        # Dedupe by canonical path so a shared home (several accounts pointing
        # at the same dir) is scanned once, first user wins. readlink -f only
        # stats via the parent, so it works even on a 0700 home the container
        # root can't cd into; fall back to the raw path rather than drop a user.
        canon_home=$(readlink -f -- "$resolved_home" 2>/dev/null) || canon_home="$resolved_home"
        if printf '%s\n' "$seen_homes" | grep -Fxq -- "$canon_home"; then
            continue
        fi
        seen_homes="$seen_homes
$canon_home"

        log "scanning user=$user uid=$uid home=$resolved_home"
        scanned_count=$((scanned_count + 1))
        # Refresh liveness before each user so a long pass (many users / slow
        # homes) can't outlive the probe's staleness window mid-scan.
        heartbeat

        # Supplementary groups from the host group db (parity with runuser's
        # initgroups in the .deb wrapper): without them, group-readable files
        # (0770 shared project dirs, group-owned homes) would be invisible to
        # the dropped child. Falls back to --clear-groups (primary gid only)
        # when the host group file isn't mounted.
        group_args="--clear-groups"
        if [ -n "$GROUP_SRC" ] && [ -r "$GROUP_SRC" ]; then
            supp_groups=$(awk -F: -v u="$user" '
                { n = split($4, m, ",")
                  for (i = 1; i <= n; i++) if (m[i] == u)
                      printf "%s%s", (out++ ? "," : ""), $3 }
            ' "$GROUP_SRC")
            if [ -n "$supp_groups" ]; then
                group_args="--groups $supp_groups"
            fi
        fi

        # Privilege drop by NUMERIC uid/gid (host users are absent from the
        # container passwd db, so a name-based drop like runuser can't work).
        # uid 0 runs directly (nothing to drop to). stdin from /dev/null so the
        # child can't consume the passwd list; timeout -k guarantees a SIGKILL
        # after the grace period so a wedged child can't hold the flock forever.
        # $group_args is intentionally unquoted: it word-splits into
        # "--groups <list>" or "--clear-groups".
        if [ "$uid" = "0" ]; then
            scan_output=$(
                timeout -k 30 "$SCAN_TIMEOUT" \
                    env HOME="$resolved_home" USER="$user" LOGNAME="$user" \
                    "$AIWATCH_BIN" scan --quiet --username "$user" \
                    </dev/null 2>&1
            )
        else
            scan_output=$(
                timeout -k 30 "$SCAN_TIMEOUT" \
                    setpriv --reuid "$uid" --regid "$gid" $group_args --inh-caps=-all \
                    env HOME="$resolved_home" USER="$user" LOGNAME="$user" \
                    "$AIWATCH_BIN" scan --quiet --username "$user" \
                    </dev/null 2>&1
            )
        fi
        scan_rc=$?

        if [ -n "$scan_output" ]; then
            printf '%s\n' "$scan_output" | sed "s/^/[aiwatch $user] /"
        fi
        if [ "$scan_rc" -ne 0 ]; then
            log "scan failed for user=$user (rc=$scan_rc)"
            pass_rc=1
        fi
    done <"$passwd_list"

    rm -f "$passwd_list"

    log "pass summary: scanned=$scanned_count skipped_unmounted=$skipped_unmounted"
    heartbeat

    # Zero scannable homes is almost always a mount/prefix mismatch, not an
    # empty host — e.g. the default RUNLAYER_HOST_PASSWD=/host/etc/passwd was
    # readable but RUNLAYER_HOST_HOME_PREFIX was left empty, so host-absolute
    # homes like /home/alice don't exist inside the container. Warn loudly
    # instead of reporting a silently green no-op pass.
    if [ "$scanned_count" -eq 0 ]; then
        log "WARNING: no scannable user homes found — check that home mounts and RUNLAYER_HOST_HOME_PREFIX pair with $PASSWD_SRC (e.g. passwd from /host/etc/passwd needs RUNLAYER_HOST_HOME_PREFIX=/host)."
        # Distinct misconfiguration code: a one-shot run (CronJob) must FAIL,
        # not report success, when it scanned nothing — zero homes on a real
        # host is a mount/prefix mismatch, not an empty machine (root's home
        # alone would match on any correctly mounted host).
        return 2
    fi
    return "$pass_rc"
}

if [ "$run_once" -eq 1 ]; then
    run_pass
    exit $?
fi

# DaemonSet / `docker run` steady state: scan, sleep, repeat. A failing pass is
# logged but never exits the container — the next pass retries.
heartbeat
while :; do
    run_pass || log "scan pass reported failures; continuing."
    log "sleeping ${INTERVAL}s until next scan pass."
    sleep "$INTERVAL"
done
