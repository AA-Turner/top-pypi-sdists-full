#!/bin/bash
# Runs INSIDE the stub image as root (driven by run_smoke_test.sh). Seeds a fake
# host passwd + bind-mounted-style home tree under /host, then exercises the
# real scan-host-users.sh entrypoint and asserts the fan-out behavior:
#   * numeric-uid setpriv drop writes as the target uid (incl. a 0700 home),
#   * all-users enumeration (root + a nologin service account are scanned),
#   * canonical-home dedupe (a shared home is scanned exactly once, first wins),
#   * the empty-RUNLAYER_API_KEY gate exits 0 without scanning anything.
#
# The container's own passwd db has NONE of these host users on purpose — that
# is the whole point of the numeric-uid drop.
set -u

ENTRYPOINT=/usr/lib/runlayer/scan-host-users.sh
PASSWD=/host/etc/passwd
export RUNLAYER_HOST_PASSWD="$PASSWD"
export RUNLAYER_HOST_HOME_PREFIX=/host

failures=0
fail() { echo "FAIL: $*" >&2; failures=$((failures + 1)); }
ok() { echo "  ok: $*"; }

# --- Seed the fake host passwd (host-absolute home paths) ---
mkdir -p /host/etc
cat >"$PASSWD" <<'EOF'
root:x:0:0:root:/root:/bin/bash
alice:x:1001:1001:Alice:/home/alice:/bin/bash
svc:x:998:998:Service Acct:/var/lib/svc:/usr/sbin/nologin
dup1:x:1002:1002:Dup One:/home/shared:/bin/bash
dup2:x:1003:1003:Dup Two:/home/shared:/bin/bash
ghost:x:1004:1004:No Home:/home/ghost:/bin/bash
EOF

# --- Seed the fake host group db: alice belongs to supplementary group 2000
# (devs). The entrypoint must restore it on the setpriv drop (runuser/initgroups
# parity) so group-readable files stay scannable. svc has no supplementary
# groups -> exercises the --clear-groups fallback path in the same pass.
cat >/host/etc/group <<'EOF'
devs:x:2000:alice,dup1
lonely:x:2001:
EOF
export RUNLAYER_HOST_GROUP=/host/etc/group

# --- Seed home dirs under the /host mount prefix ---
# root: root-owned home.
mkdir -p /host/root
# alice: 0700 home owned by a nonzero uid — proves the drop reaches a home the
# container root can't cd into.
mkdir -p /host/home/alice && chown 1001:1001 /host/home/alice && chmod 0700 /host/home/alice
# svc: nologin service account with an existing (svc-owned) home.
mkdir -p /host/var/lib/svc && chown 998:998 /host/var/lib/svc
# shared: two accounts point at it; owned by dup1 (first winner).
mkdir -p /host/home/shared && chown 1002:1002 /host/home/shared
# ghost has NO home dir seeded -> must be skipped (existing-home filter).

marker() { echo "/host$1/.runlayer/scanned"; }

# --- Gate check first (clean tree): empty key -> exit 0, no scanning ---
env -u RUNLAYER_API_KEY "$ENTRYPOINT" --once
gate_rc=$?
[ "$gate_rc" -eq 0 ] && ok "empty-key gate exited 0" || fail "empty-key gate rc=$gate_rc (want 0)"
if [ -e "$(marker /home/alice)" ] || [ -e "$(marker /root)" ]; then
    fail "gate scanned despite empty RUNLAYER_API_KEY"
else
    ok "gate produced no scan markers"
fi

# --- Configured pass: real fan-out (capture output for log assertions) ---
pass_out=$(RUNLAYER_API_KEY=stub "$ENTRYPOINT" --once 2>&1)
scan_rc=$?
printf '%s\n' "$pass_out"
[ "$scan_rc" -eq 0 ] && ok "configured --once pass exited 0" || fail "configured pass rc=$scan_rc (want 0)"

# ghost's home is in passwd but not mounted -> must be LOGGED as skipped, and
# the pass summary must count scanned vs skipped (observable coverage gap).
echo "$pass_out" | grep -q 'skipping user=ghost' \
    && ok "unmounted home logged as skipped (ghost)" || fail "no skip log for ghost"
echo "$pass_out" | grep -q 'pass summary: scanned=4 skipped_unmounted=1' \
    && ok "pass summary counts scanned=4 skipped_unmounted=1" \
    || fail "pass summary wrong: $(echo "$pass_out" | grep 'pass summary' || echo missing)"

# Heartbeat touched by the pass (liveness-probe contract).
[ -f /run/runlayer-aiwatch-heartbeat ] \
    && ok "heartbeat file touched" || fail "heartbeat file missing"

# Baked Detect-only managed config present in the image.
grep -q '"Sessions": false' /etc/runlayer/aiwatch/config.json \
    && grep -q '"Enforcement": false' /etc/runlayer/aiwatch/config.json \
    && ok "baked Detect-only config.json present (Sessions/Enforcement false)" \
    || fail "baked /etc/runlayer/aiwatch/config.json missing or wrong"

# alice: marker exists AND owned by uid 1001 (numeric drop into a 0700 home).
am="$(marker /home/alice)"
if [ -f "$am" ]; then
    owner=$(stat -c '%u' "$am")
    [ "$owner" = "1001" ] && ok "alice marker owned by uid 1001 (setpriv drop worked)" \
        || fail "alice marker owned by uid $owner (want 1001)"
    # Supplementary group 2000 (devs) restored on the drop (initgroups parity).
    if grep -q 'groups=[0-9,]*2000' "$am"; then
        ok "alice's supplementary group 2000 restored on the drop"
    else
        fail "alice's groups missing 2000: $(cat "$am")"
    fi
    # RUNLAYER_STRIP_PATH_PREFIX exported to children so submitted paths are
    # host paths, not /host/... container paths.
    if grep -q 'strip=/host ' "$am"; then
        ok "strip prefix exported to scan children"
    else
        fail "strip prefix missing from child env: $(cat "$am")"
    fi
else
    fail "alice not scanned ($am missing)"
fi

# root: scanned (all-users, no uid filter).
[ -f "$(marker /root)" ] && ok "root scanned (all-users)" || fail "root not scanned"

# svc: scanned despite nologin shell (no shell filter).
sm="$(marker /var/lib/svc)"
if [ -f "$sm" ]; then
    sowner=$(stat -c '%u' "$sm")
    [ "$sowner" = "998" ] && ok "nologin svc scanned as uid 998 (no shell filter)" \
        || fail "svc marker owned by uid $sowner (want 998)"
    # svc has no supplementary groups -> --clear-groups fallback: only gid 998.
    if grep -q 'groups=998 strip=' "$sm"; then
        ok "svc dropped with primary gid only (--clear-groups fallback)"
    else
        fail "svc groups unexpected: $(cat "$sm")"
    fi
else
    fail "nologin svc not scanned ($sm missing)"
fi

# ghost: no home -> not scanned.
[ ! -e "$(marker /home/ghost)" ] && ok "ghost (no home) skipped" || fail "ghost scanned despite no home"

# shared: scanned exactly once (dedupe), first user (dup1) wins.
shm="$(marker /home/shared)"
if [ -f "$shm" ]; then
    lines=$(wc -l <"$shm" | tr -d ' ')
    [ "$lines" = "1" ] && ok "shared home scanned exactly once (dedupe)" \
        || fail "shared home scanned $lines times (want 1)"
    grep -q 'user=dup1' "$shm" && ok "shared home first-user-wins (dup1)" \
        || fail "shared home not attributed to dup1: $(cat "$shm")"
else
    fail "shared home not scanned ($shm missing)"
fi

# --- Zero-scan misconfiguration: --once must FAIL (exit 2), not report green ---
mkdir -p /host/etc
printf 'ghost:x:1004:1004:No Home:/home/ghost:/bin/bash\n' >/host/etc/passwd-empty
RUNLAYER_API_KEY=stub RUNLAYER_HOST_PASSWD=/host/etc/passwd-empty "$ENTRYPOINT" --once
zero_rc=$?
[ "$zero_rc" -eq 2 ] && ok "zero-scan --once exited 2 (misconfig is loud)" \
    || fail "zero-scan --once rc=$zero_rc (want 2)"

echo
if [ "$failures" -gt 0 ]; then
    echo "RESULT: $failures assertion(s) failed"
    exit 1
fi
echo "RESULT: all assertions passed"
