#!/bin/sh
# Run the full CLI's per-user scheduler from a root-owned cron entry.
#
# Skill sync writes user homes and refuses root, so this wrapper enumerates
# real login users (uid >= UID_MIN) with existing homes and invokes
# `runlayer schedule` through runuser. Shared homes are reconciled once, one
# child failure does not stop later users, and all output goes to syslog
# instead of cron mail.

set -u

# Cron starts in /root, which non-root children may not be able to search.
cd /

# Skip overlapping ticks. The root-only lock prevents unprivileged suppression.
umask 077
LOCK_DIR=/run/runlayer-cli
mkdir -p "$LOCK_DIR" || exit 1
chmod 0700 "$LOCK_DIR" || exit 1
exec 9>"$LOCK_DIR/schedule.lock"
chmod 0600 "$LOCK_DIR/schedule.lock" || exit 1
flock -n 9 || exit 0

# Reuse AI Watch's root-only managed credential file. A dedicated skill-sync
# key wins; existing fleets with only RUNLAYER_API_KEY use it as the fallback.
CREDENTIALS_FILE=/etc/runlayer/aiwatch/credentials
CONFIG_FILE=/etc/runlayer/aiwatch/config.json
if [ -f "$CREDENTIALS_FILE" ] && [ -r "$CREDENTIALS_FILE" ]; then
    # shellcheck source=/dev/null
    . "$CREDENTIALS_FILE"
fi
if [ -z "${RUNLAYER_SKILL_SYNC_API_KEY:-}" ]; then
    RUNLAYER_SKILL_SYNC_API_KEY=${RUNLAYER_API_KEY:-}
fi

# Unconfigured fleets are a quiet no-op. Keep the secret out of config.json;
# schedule reads Host / SyncSkills there and the key from this exported env.
if [ -z "$RUNLAYER_SKILL_SYNC_API_KEY" ]; then
    exit 0
fi
if [ ! -r "$CONFIG_FILE" ] || ! grep -Eq '"Host"[[:space:]]*:[[:space:]]*"[^"]+"' "$CONFIG_FILE"; then
    exit 0
fi
export RUNLAYER_SKILL_SYNC_API_KEY
# The cleanup task fetches the linked AI Watch config with the primary org key.
# Keep it available after runuser drops into each user's schedule process.
if [ -n "${RUNLAYER_API_KEY:-}" ]; then
    export RUNLAYER_API_KEY
fi

# Unlike the read-only scan wrapper, this fan-out WRITES each user's home, so
# it must not touch service accounts: with a managed Username override every
# passwd entry would resolve to that identity and skill trees would be written
# into homes like /usr/sbin. Gate on the distro's real-login-user boundary
# (UID_MIN from login.defs; uid, not shell — directory users can have unusual
# shells). Root is excluded by the same threshold.
uid_min=$(awk '$1 == "UID_MIN" && $2 ~ /^[0-9]+$/ { print $2 }' /etc/login.defs 2>/dev/null | tail -n 1)
case $uid_min in
    '' | *[!0-9]*) uid_min=1000 ;;
esac

rc=0
seen_homes=""

# Snapshot passwd: piping into while would hide rc/seen_homes in a subshell.
passwd_list=$(mktemp) || exit 1
trap 'rm -f "$passwd_list"' EXIT
getent passwd >"$passwd_list"

while IFS=: read -r user _pw uid _gid _gecos home _shell; do
    [ -n "$user" ] || continue
    case $uid in
        '' | *[!0-9]*) continue ;;
    esac
    [ "$uid" -ge "$uid_min" ] || continue
    [ -n "$home" ] || continue
    [ -d "$home" ] || continue

    canon_home=$(readlink -f -- "$home" 2>/dev/null) || canon_home=$home
    if printf '%s\n' "$seen_homes" | grep -Fxq -- "$canon_home"; then
        continue
    fi
    seen_homes="$seen_homes
$canon_home"

    schedule_output=$(
        timeout -k 30 600 runuser -u "$user" -- \
            env HOME="$home" USER="$user" LOGNAME="$user" \
            /usr/bin/runlayer schedule </dev/null 2>&1
    )
    schedule_rc=$?
    if [ -n "$schedule_output" ]; then
        printf '%s\n' "$schedule_output" | logger -t runlayer-cli
    fi
    if [ "$schedule_rc" -ne 0 ]; then
        logger -t runlayer-cli "schedule failed for user $user (rc=$schedule_rc)"
        rc=1
    fi
done <"$passwd_list"

exit $rc
