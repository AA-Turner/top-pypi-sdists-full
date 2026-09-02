#!/bin/bash
# uninstall-runlayer.sh — remove the full Runlayer CLI from a macOS device
# (run as root). Companion to uninstall.sh (AI Watch); the two packages share
# /usr/local/lib/runlayer but own separate bundles, jobs, and receipts.
#
# Best-effort throughout: every step tolerates already-removed state, so
# re-runs and partial installs both exit 0.
#
# Removes everything build_pkg_runlayer.sh lays down: the scheduler
# LaunchAgent (booted out of the console user's GUI domain), the update
# LaunchDaemon, the binary symlink + onedir bundle, and the pkg receipt.
#
# Does NOT remove the MDM-pushed deployment profile
# (com.runlayer.cli.mobileconfig: tenant config + Managed Login Items) —
# unscope that from the device group / Blueprint separately. Leaves the
# AI Watch install untouched.

AGENT_LABELS=(
    com.runlayer.cli.schedule
)
DAEMON_LABELS=(
    com.runlayer.cli.update
)

# Bootout agents from the console user's GUI domain (no-op at loginwindow).
CONSOLE_UID=$(stat -f %u /dev/console 2>/dev/null || echo "")
if [ -n "$CONSOLE_UID" ] && [ "$CONSOLE_UID" != "0" ]; then
    for label in "${AGENT_LABELS[@]}"; do
        launchctl bootout "gui/${CONSOLE_UID}/${label}" 2>/dev/null || true
    done
fi

# Bootout the daemon(s) from the system domain.
for label in "${DAEMON_LABELS[@]}"; do
    launchctl bootout "system/${label}" 2>/dev/null || true
done

# Binary symlink + onedir bundle (AI Watch's sibling bundle stays).
rm -f /usr/local/bin/runlayer
rm -rf /usr/local/lib/runlayer/runlayer

# LaunchAgents + LaunchDaemons.
rm -f /Library/LaunchAgents/com.runlayer.cli.schedule.plist
rm -f /Library/LaunchDaemons/com.runlayer.cli.update.plist

# Optional package-only Test Device config. This is deliberately limited to
# /Library/Preferences; MDM-owned /Library/Managed Preferences stays untouched.
defaults delete /Library/Preferences/com.runlayer.cli 2>/dev/null || true
rm -f /Library/Preferences/com.runlayer.cli.plist

# Forget the pkg receipt so a future install is a clean first-install.
pkgutil --forget com.runlayer.cli 2>/dev/null || true

exit 0
