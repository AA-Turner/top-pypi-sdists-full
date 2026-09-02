#!/bin/bash
# Runs INSIDE a distro container as root (driven by run_smoke_tests.sh).
# Installs the runlayer-aiwatch package, then asserts install layout, perms,
# cron registration, scan/update wrapper behavior (privilege drop, credential
# gates), config|noreplace upgrade semantics, and uninstall cleanup.
#
# Usage: assert_inside_container.sh <deb|rpm> </abs/path/to/pkg>
#
# NOTE: containers have no syslogd, so nothing asserts on syslog content —
# the wrapper's `logger` calls must merely not break it.

set -u
PKG_TYPE="${1:?deb|rpm}"
PKG_PATH="${2:?package path}"

failures=0
fail() { echo "FAIL: $*" >&2; failures=$((failures + 1)); }
ok() { echo "  ok: $*"; }

assert_stat() { # <path> <expected 'mode owner:group'>
    local actual
    actual=$(stat -c '%a %U:%G' "$1" 2>/dev/null)
    if [ "$actual" = "$2" ]; then ok "$1 is $2"; else fail "$1: want '$2' got '$actual'"; fi
}

# --- Install (cron dependency must resolve from the distro repos) ---
if [ "$PKG_TYPE" = deb ]; then
    export DEBIAN_FRONTEND=noninteractive
    apt-get update -q >/dev/null
    apt-get install -y "$PKG_PATH" >/dev/null || { fail "install"; exit 1; }
else
    dnf install -y "$PKG_PATH" >/dev/null || { fail "install"; exit 1; }
fi
ok "package installed"

# --- Binary + /usr/bin symlink ---
[ -L /usr/bin/aiwatch ] && ok "/usr/bin/aiwatch is a symlink" || fail "/usr/bin/aiwatch not a symlink"
ver=$(/usr/bin/aiwatch --version) && ok "aiwatch --version: $ver" || fail "aiwatch --version failed"

# --- Layout perms ---
assert_stat /etc/cron.d/runlayer-aiwatch "644 root:root"
assert_stat /etc/runlayer/aiwatch/credentials "600 root:root"
assert_stat /etc/runlayer/aiwatch/config.json "644 root:root"
assert_stat /etc/runlayer/aiwatch/version.json "644 root:root"
[ "$(stat -c '%a' /usr/lib/runlayer/run-aiwatch-scan.sh)" = 755 ] \
    && ok "scan wrapper is 755" || fail "scan wrapper not 755"
[ "$(stat -c '%a' /usr/lib/runlayer/run-aiwatch-update.sh)" = 755 ] \
    && ok "update wrapper is 755" || fail "update wrapper not 755"

# --- Version inventory record: shape + matches aiwatch --version (ENG-4161).
# MDM reads /etc/runlayer/aiwatch/version.json without exec'ing aiwatch. ---
jsonver=$(sed -n 's/.*"Version"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' \
    /etc/runlayer/aiwatch/version.json)
[ -n "$jsonver" ] && ok "version.json Version=$jsonver" \
    || fail "version.json missing/empty Version"
case "$ver" in
*"$jsonver"*) ok "version.json matches aiwatch --version" ;;
*) fail "version.json ($jsonver) not in aiwatch --version ($ver)" ;;
esac

# --- cron.d entry: */15 scan + hourly update root lines; filename must have no dot
# (cron's run-parts-style name filter silently skips dotted files) ---
grep -q '^\*/15 \* \* \* \* root /usr/lib/runlayer/run-aiwatch-scan.sh$' /etc/cron.d/runlayer-aiwatch \
    && ok "cron.d has */15 root scan line" || fail "cron.d scan line missing"
grep -q '^7 \* \* \* \* root /usr/lib/runlayer/run-aiwatch-update.sh$' /etc/cron.d/runlayer-aiwatch \
    && ok "cron.d has hourly root update line" || fail "cron.d update line missing"
case "$(basename /etc/cron.d/runlayer-aiwatch)" in
*.*) fail "cron.d filename contains a dot" ;;
*) ok "cron.d filename has no dot" ;;
esac

# --- cron daemon pulled in by the package dependency ---
if [ "$PKG_TYPE" = deb ]; then
    { command -v cron || command -v crond; } >/dev/null \
        && ok "cron daemon installed (dep)" || fail "no cron/crond after install"
else
    command -v crond >/dev/null && ok "crond installed (dep)" || fail "no crond after install"
fi

# --- All-users wrapper: enumeration + privilege drop + configured run ---
useradd -m alice
mkdir -p /home/alice/.cursor
printf '{"mcpServers":{}}\n' >/home/alice/.cursor/mcp.json
chown -R alice:alice /home/alice/.cursor
printf 'RUNLAYER_API_KEY=stub\nRUNLAYER_HOST=http://127.0.0.1:9\n' >/etc/runlayer/aiwatch/credentials
/usr/lib/runlayer/run-aiwatch-scan.sh
[ $? -eq 0 ] && ok "configured wrapper run exited 0" || fail "configured wrapper run failed"
[ -d /home/alice/.runlayer ] && [ "$(stat -c '%U' /home/alice/.runlayer)" = alice ] \
    && ok "alice scanned with dropped privileges (alice-owned ~/.runlayer)" \
    || fail "/home/alice/.runlayer missing or not alice-owned"
# All-users means no uid filtering: root gets scanned too.
[ -d /root/.runlayer ] && ok "root scanned too (all-users)" || fail "/root/.runlayer missing"

# --- Update wrapper: root credential handoff + direct binary invocation ---
rm -f /tmp/aiwatch-update-marker
/usr/lib/runlayer/run-aiwatch-update.sh
[ $? -eq 0 ] && ok "configured update wrapper exited 0" || fail "configured update wrapper failed"
[ -e /tmp/aiwatch-update-marker ] \
    && ok "update wrapper invoked aiwatch self-update" || fail "self-update was not invoked"

# --- Unconfigured-fleet gate: empty credentials -> exit 0 before any scan ---
rm -rf /root/.runlayer
: >/etc/runlayer/aiwatch/credentials
/usr/lib/runlayer/run-aiwatch-scan.sh
[ $? -eq 0 ] && ok "unconfigured wrapper run exited 0" || fail "unconfigured run non-zero"
[ ! -d /root/.runlayer ] && ok "gate fired before any scan" || fail "scan ran while unconfigured"
rm -f /tmp/aiwatch-update-marker
/usr/lib/runlayer/run-aiwatch-update.sh
[ $? -eq 0 ] && ok "unconfigured update wrapper exited 0" || fail "unconfigured update non-zero"
[ ! -e /tmp/aiwatch-update-marker ] \
    && ok "credential gate fired before update" || fail "update ran while unconfigured"

# --- Upgrade semantics: edited config.json survives reinstall (config|noreplace).
# Same-version reinstall on deb: dpkg keeps a locally modified conffile without
# prompting (package conffile hash unchanged) — deliberately NO --force-confold,
# which would mask a regression. rpm -Uvh --replacepkgs needs no repo metadata. ---
printf '{"Host":"https://edited.example.test","Sessions":false,"Enforcement":false}\n' \
    >/etc/runlayer/aiwatch/config.json
if [ "$PKG_TYPE" = deb ]; then
    apt-get install --reinstall -y "$PKG_PATH" >/dev/null || fail "reinstall failed"
else
    rpm -Uvh --replacepkgs "$PKG_PATH" >/dev/null || fail "reinstall failed"
fi
grep -q edited.example.test /etc/runlayer/aiwatch/config.json \
    && ok "edited config.json survived reinstall" || fail "reinstall clobbered config.json"

# --- Uninstall: cron.d entry (plain content, NOT a conffile) must be GONE so
# a stale schedule never keeps firing; the edited config survives as a conffile.
# Nuance: `apt-get remove` keeps conffiles in place (only `purge` deletes them);
# rpm renames a modified %config(noreplace) file to .rpmsave on erase. ---
if [ "$PKG_TYPE" = deb ]; then
    apt-get remove -y runlayer-aiwatch >/dev/null || fail "remove failed"
    kept_config=/etc/runlayer/aiwatch/config.json
else
    dnf remove -y runlayer-aiwatch >/dev/null || fail "remove failed"
    kept_config=/etc/runlayer/aiwatch/config.json.rpmsave
fi
[ ! -e /etc/cron.d/runlayer-aiwatch ] \
    && ok "cron.d entry removed on uninstall" || fail "stale /etc/cron.d/runlayer-aiwatch left behind"
# version.json is plain content (like cron.d), so it must be gone on uninstall —
# no stale version can linger for MDM inventory (ENG-4161).
[ ! -e /etc/runlayer/aiwatch/version.json ] \
    && ok "version.json removed on uninstall" || fail "stale version.json left behind"
grep -q edited.example.test "$kept_config" 2>/dev/null \
    && ok "edited config kept on uninstall ($kept_config)" || fail "edited config lost on uninstall"
[ ! -e /usr/lib/runlayer/aiwatch/aiwatch ] \
    && ok "binary removed on uninstall" || fail "binary left behind"
[ ! -e /usr/lib/runlayer/run-aiwatch-update.sh ] \
    && ok "update wrapper removed on uninstall" || fail "update wrapper left behind"

echo
if [ "$failures" -gt 0 ]; then
    echo "RESULT: $failures assertion(s) failed"
    exit 1
fi
echo "RESULT: all assertions passed"
