#!/bin/bash
# uninstall.sh — remove AI Watch from a macOS device (run as root).
#
# Consolidates the teardown that packaging/DEPLOYMENT.md §9 previously spelled
# out inline, so MDM admins ship one Run-Once script instead of hand-maintaining
# the block. Best-effort throughout: every step tolerates already-removed state,
# so re-runs and partial installs both exit 0.
#
# Removes everything the .pkg lays down: all LaunchAgents + LaunchDaemons
# (booted out first), the daemon endpoint, the binary + onedir bundle, the Chrome
# native-messaging host, the install-window stamp, the MDM version-inventory
# record, and the pkg receipt.
#
# Does NOT remove the MDM-pushed Configuration Profiles (tenant config, PPPC,
# Login Items) — unscope those from the device group / Blueprint separately.

AGENT_LABELS=(
    com.runlayer.aiwatch
    com.runlayer.aiwatch.enroll
    com.runlayer.aiwatch.daemon
)
DAEMON_LABELS=(
    com.runlayer.aiwatch.bootstrap
    com.runlayer.aiwatch.update
)

# Stop every discovered user's loaded agents and remove the daemon endpoint.
# Console + who cover logged-in directory users; local dscl records provide a
# final best-effort pass for background sessions.
CLEANED_UIDS=""
cleanup_user() {
    local user_name="$1"
    local user_uid="$2"
    case "$user_uid" in
        ""|*[!0-9]*) return ;;
    esac
    if [ "$user_uid" = "0" ] || [ -z "$user_name" ] || [ "$user_name" = "root" ]; then
        return
    fi
    case " $CLEANED_UIDS " in
        *" $user_uid "*) return ;;
    esac

    for label in "${AGENT_LABELS[@]}"; do
        launchctl bootout "gui/${user_uid}/${label}" 2>/dev/null || true
    done

    USER_HOME=$(
        /usr/bin/dscl /Search -read "/Users/${user_name}" NFSHomeDirectory 2>/dev/null \
            | /usr/bin/cut -d ' ' -f 2-
    )
    case "$USER_HOME" in
        /*)
        DAEMON_DIR="$USER_HOME/Library/Application Support/Runlayer"
        rm -f "$DAEMON_DIR/aiwatch.sock" "$DAEMON_DIR/aiwatch.sock.lock"
        CLEANED_UIDS="$CLEANED_UIDS $user_uid"
        ;;
    esac
}

CONSOLE_UID=$(stat -f %u /dev/console 2>/dev/null || echo "")
CONSOLE_USER=$(stat -f %Su /dev/console 2>/dev/null || echo "")
cleanup_user "$CONSOLE_USER" "$CONSOLE_UID"

while read -r ACTIVE_USER _; do
    ACTIVE_UID=$(/usr/bin/id -u "$ACTIVE_USER" 2>/dev/null || echo "")
    cleanup_user "$ACTIVE_USER" "$ACTIVE_UID"
done < <(/usr/bin/who 2>/dev/null)

while read -r USER_NAME USER_UID; do
    case "$USER_UID" in
        ""|*[!0-9]*) continue ;;
    esac
    if [ "$USER_UID" -ge 500 ]; then
        cleanup_user "$USER_NAME" "$USER_UID"
    fi
done < <(/usr/bin/dscl . -list /Users UniqueID 2>/dev/null)

# Bootout the daemon(s) from the system domain.
for label in "${DAEMON_LABELS[@]}"; do
    launchctl bootout "system/${label}" 2>/dev/null || true
done

# Binary + onedir bundle.
rm -f /usr/local/bin/aiwatch
rm -rf /usr/local/lib/runlayer/aiwatch

# LaunchAgents + LaunchDaemons.
rm -f /Library/LaunchAgents/com.runlayer.aiwatch.plist
rm -f /Library/LaunchAgents/com.runlayer.aiwatch.enroll.plist
rm -f /Library/LaunchAgents/com.runlayer.aiwatch.daemon.plist
rm -f /Library/LaunchDaemons/com.runlayer.aiwatch.bootstrap.plist
rm -f /Library/LaunchDaemons/com.runlayer.aiwatch.update.plist

# Browser native-messaging hosts installed by the .pkg.
rm -f /Library/Google/Chrome/NativeMessagingHosts/com.runlayer.aiwatch.json
rm -f "/Library/Application Support/Mozilla/NativeMessagingHosts/com.runlayer.aiwatch.json"

# Install-window stamp dir (see runlayer_cli/install_window.py).
rm -rf /var/db/com.runlayer.aiwatch

# Optional package-only Test Device config. This is deliberately limited to
# /Library/Preferences; MDM-owned /Library/Managed Preferences stays untouched.
defaults delete /Library/Preferences/com.runlayer.aiwatch 2>/dev/null || true
rm -f /Library/Preferences/com.runlayer.aiwatch.plist

# MDM version-inventory record (dedicated com.runlayer.aiwatch.version domain):
# rm the plist, then defaults delete to drop the cfprefsd cache so a stale value
# can't be read back after uninstall.
rm -f /Library/Preferences/com.runlayer.aiwatch.version.plist
defaults delete com.runlayer.aiwatch.version 2>/dev/null || true

# Forget the pkg receipt so a future install is a clean first-install.
pkgutil --forget com.runlayer.aiwatch 2>/dev/null || true

exit 0
