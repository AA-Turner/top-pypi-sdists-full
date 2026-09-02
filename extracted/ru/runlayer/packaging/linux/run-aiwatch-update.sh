#!/bin/sh
# Runlayer AI Watch — apply the backend-selected package as root.

set -u

# Deduplicate hourly updater invocations, then wait for the scan wrapper's
# package lock without abandoning the attempt behind a long all-user scan.
# Locks live in a root-only runtime directory so an unprivileged user cannot
# hold flock and suppress security updates.
# Contention on the updater lock exits EX_TEMPFAIL (75), not 0: `aiwatch
# update-now` invokes this wrapper and must not report success when another
# update cycle already runs. Cron ignores the exit code.
EX_TEMPFAIL=75
umask 077
LOCK_DIR=/run/runlayer-aiwatch
mkdir -p "$LOCK_DIR" || exit 1
chmod 0700 "$LOCK_DIR" || exit 1
exec 9>"$LOCK_DIR/update.lock"
chmod 0600 "$LOCK_DIR/update.lock" || exit 1
flock -n 9 || exit $EX_TEMPFAIL
exec 8>"$LOCK_DIR/package.lock"
chmod 0600 "$LOCK_DIR/package.lock" || exit 1
flock 8 || exit 1

# Root-only credentials (0600): RUNLAYER_API_KEY, optional RUNLAYER_HOST.
CREDENTIALS_FILE=/etc/runlayer/aiwatch/credentials
if [ -f "$CREDENTIALS_FILE" ] && [ -r "$CREDENTIALS_FILE" ]; then
    . "$CREDENTIALS_FILE"
fi

# Unconfigured devices have no authenticated update target to resolve.
if [ -z "${RUNLAYER_API_KEY:-}" ]; then
    exit 0
fi
export RUNLAYER_API_KEY
if [ -n "${RUNLAYER_HOST:-}" ]; then
    export RUNLAYER_HOST
fi

# Managed opt-out policy stays inside the binary; cron owns cadence only.
update_output=$(/usr/lib/runlayer/aiwatch/aiwatch self-update 2>&1)
update_rc=$?
if [ -n "$update_output" ]; then
    printf '%s\n' "$update_output" | logger -t runlayer-aiwatch
fi
if [ "$update_rc" -ne 0 ]; then
    logger -t runlayer-aiwatch "update failed (rc=$update_rc)"
fi

exit $update_rc
