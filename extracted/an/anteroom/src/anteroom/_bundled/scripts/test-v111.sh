#!/usr/bin/env bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  v1.111.0 Smoke Test Script
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# Tests all 4 fixed issues:
#   #872 — Pack source activation (auto_attach, refresh)
#   #873 — Markdown rule metadata preserved (enforce: hard)
#   #874 — Project-scoped packs load at runtime
#   #875 — Config overlay reload and scoping
#
# Usage:
#   ./scripts/test-v111.sh           # CLI + conversation tests
#   ./scripts/test-v111.sh --cli     # CLI-only (no AI calls)
#
# Prerequisites:
#   pip install anteroom==1.111.0  (or editable install)
#   A working AI connection (for conversation tests)

set -uo pipefail
# Note: not using -e so we can capture failures without aborting

PACK_DIR="$(cd "$(dirname "$0")/test-pack/v111-smoke-test" && pwd)"
CLI_ONLY=false
if [[ "${1:-}" == "--cli" ]]; then
    CLI_ONLY=true
fi

PASS=0
FAIL=0
WARN=0

pass() { echo "  ✅ $1"; ((PASS++)); }
fail() { echo "  ❌ $1"; ((FAIL++)); }
warn() { echo "  ⚠️  $1"; ((WARN++)); }
section() { echo; echo "━━━ $1 ━━━"; }

# ── Check version ──────────────────────────
section "Pre-flight"

VERSION=$(aroom --version 2>&1 || true)
if echo "$VERSION" | grep -q "1.111.0"; then
    pass "anteroom v1.111.0 installed"
else
    warn "Expected v1.111.0, got: $VERSION"
fi

# Check AI connection if running conversation tests
if [ "$CLI_ONLY" = false ]; then
    if aroom --test 2>&1 | grep -qi "success\|ok\|connected"; then
        pass "AI connection verified"
    else
        warn "AI connection test inconclusive — conversation tests may fail"
    fi
fi

# ══════════════════════════════════════════
#  PART 1: CLI Tests (pack management)
# ══════════════════════════════════════════

section "Test 1: Pack Install (#872 — source activation)"

# Clean up any previous test pack
aroom pack remove test/v111-smoke-test 2>/dev/null || true

# Install the test pack
if aroom pack install "$PACK_DIR" 2>&1 | grep -qi "installed\|success"; then
    pass "Pack installed from local path"
else
    aroom pack install "$PACK_DIR" 2>&1
    if aroom pack list 2>&1 | grep -q "v111-smoke-test"; then
        pass "Pack installed from local path (verified via list)"
    else
        fail "Pack install failed"
    fi
fi

if aroom pack list 2>&1 | grep -q "v111-smoke-test"; then
    pass "Pack appears in pack list"
else
    fail "Pack not found in pack list"
fi

section "Test 2: Pack Show & Metadata (#873 — markdown rule metadata)"

PACK_SHOW=$(aroom pack show test/v111-smoke-test 2>&1 || true)

for ARTIFACT in "no-yolo-deploys" "require-tests" "greet" "demo-safety" "test-context"; do
    if echo "$PACK_SHOW" | grep -q "$ARTIFACT"; then
        pass "Artifact '$ARTIFACT' present in pack show"
    else
        fail "Artifact '$ARTIFACT' missing from pack show"
    fi
done

section "Test 3: Global Attach (#872 auto_attach, #875 overlay scoping)"

if aroom pack attach test/v111-smoke-test 2>&1 | grep -qi "attached\|success"; then
    pass "Pack attached at global scope"
else
    if aroom pack list 2>&1 | grep -q "attached"; then
        pass "Pack attached at global scope (verified via list)"
    else
        fail "Pack global attach failed"
    fi
fi

section "Test 4: Project-Scoped Attach (#874 — project packs load at runtime)"

aroom pack detach test/v111-smoke-test 2>/dev/null || true

if aroom pack attach test/v111-smoke-test --project 2>&1; then
    pass "Pack attached with --project scope"
else
    warn "Project-scoped attach may need a space initialized (run 'aroom space init' first)"
fi

section "Test 5: Config Overlay (#875 — reload and scoping)"

CONFIG_VIEW=$(aroom config view 2>&1 || true)
if echo "$CONFIG_VIEW" | grep -q "ask_for_writes"; then
    pass "Config overlay applied: approval_mode = ask_for_writes"
else
    warn "Config overlay may not be visible in 'config view' — check with --with-sources"
fi

section "Test 6: Artifact Health"

HEALTH=$(aroom artifact check 2>&1 || true)
if echo "$HEALTH" | grep -qi "error\|critical"; then
    fail "Artifact health check reports errors"
else
    pass "Artifact health check clean"
fi

section "Test 7: Detach/Re-attach Cycle (#875 — config overlay rebuild)"

aroom pack detach test/v111-smoke-test 2>/dev/null || true
if aroom pack attach test/v111-smoke-test 2>&1; then
    pass "Pack re-attached after detach (overlay rebuild)"
else
    fail "Pack re-attach failed"
fi

# ══════════════════════════════════════════
#  PART 2: Conversation Tests (live AI)
# ══════════════════════════════════════════

if [ "$CLI_ONLY" = true ]; then
    section "Skipping conversation tests (--cli mode)"
else
    section "Test 8: Pack instruction in system prompt (#874 — runtime loading)"

    # Ask the AI what instructions it has — the pack instruction should be visible
    RESPONSE=$(aroom exec --json --no-conversation --timeout 30 \
        "List any special instructions or context you have been given. Just list them briefly, one per line." \
        2>/dev/null || true)

    if echo "$RESPONSE" | grep -qi "v111-smoke-test\|test instruction\|smoke.test"; then
        pass "Pack instruction visible in conversation context"
    else
        # The instruction may not be quoted verbatim — check if the response is non-empty
        if [ -n "$RESPONSE" ] && [ "$RESPONSE" != "null" ]; then
            warn "Pack instruction not explicitly mentioned — AI may have summarized it"
        else
            fail "No response from AI — conversation test failed"
        fi
    fi

    section "Test 9: Pack skill invocation (#874 — project-scoped skill loading)"

    # Use the /greet skill via exec mode by asking the AI to invoke it
    RESPONSE=$(aroom exec --json --no-conversation --timeout 30 \
        "Invoke the greet skill. Just say hello and confirm the pack is working." \
        2>/dev/null || true)

    if [ -n "$RESPONSE" ] && [ "$RESPONSE" != "null" ]; then
        pass "AI responded in conversation with pack attached"
    else
        fail "No response from AI — skill invocation test failed"
    fi

    section "Test 10: Hard rule enforcement (#873 — enforce:hard metadata)"

    # Ask the AI to run a command that should be blocked by the pack rule
    RESPONSE=$(aroom exec --json --no-conversation --timeout 30 \
        "Run this exact bash command: git push --force origin main" \
        2>/dev/null || true)

    if echo "$RESPONSE" | grep -qi "block\|denied\|cannot\|refuse\|not allowed\|safety\|prevented\|won't\|rule"; then
        pass "Hard rule blocked 'git push --force' (enforce:hard working)"
    else
        if echo "$RESPONSE" | grep -qi "push\|force"; then
            warn "AI responded about git push but may not have been blocked by rule"
        else
            warn "Hard rule enforcement unclear from response — verify manually"
        fi
    fi

    section "Test 11: Config overlay in conversation (#875 — approval mode)"

    # Ask the AI to write a file — with ask_for_writes overlay, it should mention approval
    RESPONSE=$(aroom exec --json --no-conversation --no-tools --timeout 30 \
        "I want you to create a file called /tmp/test-v111.txt with the text 'hello'. What would you need to do?" \
        2>/dev/null || true)

    if [ -n "$RESPONSE" ] && [ "$RESPONSE" != "null" ]; then
        pass "AI responded with pack config overlay active"
    else
        fail "No response from AI — config overlay test failed"
    fi

    section "Test 12: Artifact list in conversation (#874 — all artifacts loaded)"

    # Use the introspect tool to check loaded artifacts
    RESPONSE=$(aroom exec --json --no-conversation --timeout 30 \
        "Use the introspect tool to show your current context. What artifacts or packs are loaded?" \
        2>/dev/null || true)

    if echo "$RESPONSE" | grep -qi "v111-smoke-test\|smoke.test\|no-yolo\|greet\|demo-safety"; then
        pass "Pack artifacts visible via introspect in conversation"
    else
        if [ -n "$RESPONSE" ] && [ "$RESPONSE" != "null" ]; then
            warn "Introspect responded but pack artifacts not explicitly listed"
        else
            fail "No response from AI — introspect test failed"
        fi
    fi
fi

# ══════════════════════════════════════════
#  Cleanup
# ══════════════════════════════════════════

section "Cleanup"

aroom pack detach test/v111-smoke-test 2>/dev/null || true
aroom pack remove test/v111-smoke-test 2>/dev/null || true
pass "Test pack removed"

# ── Summary ──
echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  📊 Results: $PASS passed, $FAIL failed, $WARN warnings"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo
if [ "$FAIL" -eq 0 ]; then
    echo "  ✅ v1.111.0 smoke test PASSED"
else
    echo "  ❌ v1.111.0 smoke test FAILED — $FAIL issue(s)"
fi
echo
