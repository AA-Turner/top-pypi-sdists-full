#!/usr/bin/env bash
#
# test_resolve_cascade_target.sh — tests for resolve-cascade-target.sh
#
# Usage: test_resolve_cascade_target.sh
#
# Exit code: 0 if all tests pass, 1 if any test fails.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESOLVE="$SCRIPT_DIR/resolve-cascade-target.sh"
chmod +x "$RESOLVE"

PASS=0
FAIL=0

assert_eq() {
  local test_name="$1" expected="$2" actual="$3"
  if [[ "$actual" == "$expected" ]]; then
    echo "  ✅ $test_name"
    PASS=$((PASS + 1))
  else
    echo "  ❌ $test_name"
    echo "     expected: $expected"
    echo "     actual:   $actual"
    FAIL=$((FAIL + 1))
  fi
}

assert_exit() {
  local test_name="$1" expected_exit="$2"
  shift 2
  local actual_exit=0
  "$@" >/dev/null 2>&1 || actual_exit=$?
  assert_eq "$test_name" "$expected_exit" "$actual_exit"
}

# ── Fixture helpers ──────────────────────────────────────────────────────────

make_hierarchy_yml() {
  local path="$1" level="$2"
  shift 2
  mkdir -p "$(dirname "$path")"
  {
    echo "level: $level"
    if [[ $# -gt 0 ]]; then
      echo "$@"
    fi
  } > "$path"
}

# ── Tests ────────────────────────────────────────────────────────────────────

echo "=== resolve-cascade-target.sh tests ==="
echo ""

# ── Test: missing --issue exits with code 1 ──────────────────────────────────
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

echo "--- argument validation ---"
exit_code=0
"$RESOLVE" --spec-base-path "$TMP/specs" 2>/dev/null || exit_code=$?
assert_eq "missing --issue exits 1" "1" "$exit_code"

exit_code=0
"$RESOLVE" --issue 42 2>/dev/null || exit_code=$?
assert_eq "missing --spec-base-path exits 1" "1" "$exit_code"

exit_code=0
"$RESOLVE" --issue 42 --spec-base-path "$TMP/nonexistent" 2>/dev/null || exit_code=$?
assert_eq "nonexistent SPEC_BASE_PATH exits 1" "1" "$exit_code"

# ── Test: standalone issue (no hierarchy.yml) exits 2 ────────────────────────
echo "--- standalone issue ---"
mkdir -p "$TMP/specs"
exit_code=0
"$RESOLVE" --issue 99 --spec-base-path "$TMP/specs" 2>/dev/null || exit_code=$?
assert_eq "no hierarchy.yml exits 2" "2" "$exit_code"

# ── Test: epic issue → first-child ───────────────────────────────────────────
echo "--- epic issue ---"
make_hierarchy_yml "$TMP/specs/1/hierarchy.yml" "epic"
OUTPUT=$("$RESOLVE" --issue 1 --spec-base-path "$TMP/specs" 2>/dev/null)
eval "$OUTPUT"
assert_eq "epic: MODE=first-child" "first-child" "$MODE"
assert_eq "epic: HIERARCHY_YML correct" "$TMP/specs/1/hierarchy.yml" "$HIERARCHY_YML"

# ── Test: feature issue → first-child ────────────────────────────────────────
echo "--- feature issue ---"
make_hierarchy_yml "$TMP/specs/1/2/hierarchy.yml" "feature"
OUTPUT=$("$RESOLVE" --issue 2 --spec-base-path "$TMP/specs" 2>/dev/null)
eval "$OUTPUT"
assert_eq "feature: MODE=first-child" "first-child" "$MODE"
assert_eq "feature: HIERARCHY_YML correct" "$TMP/specs/1/2/hierarchy.yml" "$HIERARCHY_YML"

# ── Test: task issue (hierarchical path) → next-sibling ──────────────────────
echo "--- task issue (hierarchical path) ---"
make_hierarchy_yml "$TMP/specs/1/2/3/hierarchy.yml" "task"
# parent yml is already at $TMP/specs/1/2/hierarchy.yml (feature)
OUTPUT=$("$RESOLVE" --issue 3 --spec-base-path "$TMP/specs" 2>/dev/null)
eval "$OUTPUT"
assert_eq "task(nested): MODE=next-sibling" "next-sibling" "$MODE"
assert_eq "task(nested): HIERARCHY_YML is parent" "$TMP/specs/1/2/hierarchy.yml" "$HIERARCHY_YML"

# ── Test: task issue (legacy flat layout) → next-sibling ─────────────────────
echo "--- task issue (legacy flat layout) ---"
FLAT="$TMP/flat-specs"
mkdir -p "$FLAT"
PARENT_NUMBER=200
make_hierarchy_yml "$FLAT/${PARENT_NUMBER}-my-feature/hierarchy.yml" "feature"
make_hierarchy_yml "$FLAT/201-my-task/hierarchy.yml" "task" "parent: $PARENT_NUMBER"
OUTPUT=$("$RESOLVE" --issue 201 --spec-base-path "$FLAT" 2>/dev/null)
eval "$OUTPUT"
assert_eq "task(legacy): MODE=next-sibling" "next-sibling" "$MODE"
assert_eq "task(legacy): HIERARCHY_YML is parent" "$FLAT/${PARENT_NUMBER}-my-feature/hierarchy.yml" "$HIERARCHY_YML"

# ── Test: task without a parent exits 2 ──────────────────────────────────────
echo "--- task without parent ---"
NOPARENT="$TMP/noparent"
mkdir -p "$NOPARENT"
make_hierarchy_yml "$NOPARENT/300-orphan-task/hierarchy.yml" "task" "parent: 999"
exit_code=0
"$RESOLVE" --issue 300 --spec-base-path "$NOPARENT" 2>/dev/null || exit_code=$?
assert_eq "task with missing parent exits 2" "2" "$exit_code"

# ── Test: task without parent field exits 2 ──────────────────────────────────
echo "--- task without parent field ---"
NOPARENTFIELD="$TMP/noparentfield"
mkdir -p "$NOPARENTFIELD"
make_hierarchy_yml "$NOPARENTFIELD/301-orphan-task/hierarchy.yml" "task"
exit_code=0
"$RESOLVE" --issue 301 --spec-base-path "$NOPARENTFIELD" 2>/dev/null || exit_code=$?
assert_eq "task without parent field exits 2" "2" "$exit_code"

# ── Test: unknown level exits 1 ───────────────────────────────────────────────
echo "--- unknown hierarchy level ---"
UNKNOWN="$TMP/unknown"
mkdir -p "$UNKNOWN"
make_hierarchy_yml "$UNKNOWN/400/hierarchy.yml" "story"
exit_code=0
"$RESOLVE" --issue 400 --spec-base-path "$UNKNOWN" 2>/dev/null || exit_code=$?
assert_eq "unknown level exits 1" "1" "$exit_code"

# ── Test: missing level entry exits 1 ─────────────────────────────────────────
echo "--- missing hierarchy level ---"
NOLEVEL="$TMP/nolevel"
mkdir -p "$NOLEVEL/401"
cat > "$NOLEVEL/401/hierarchy.yml" <<EOF
name: no-level
EOF
exit_code=0
"$RESOLVE" --issue 401 --spec-base-path "$NOLEVEL" 2>/dev/null || exit_code=$?
assert_eq "missing level exits 1" "1" "$exit_code"

# ── Test: --level flag overrides yaml-parsed level ───────────────────────────
echo "--- --level flag ---"
# Issue 1 has an "epic" hierarchy.yml; pass --level feature to override
OUTPUT=$("$RESOLVE" --issue 1 --spec-base-path "$TMP/specs" --level feature 2>/dev/null)
eval "$OUTPUT"
assert_eq "--level override: MODE=first-child" "first-child" "$MODE"

# ── Test: legacy flat path match ─────────────────────────────────────────────
echo "--- legacy flat path ---"
LEGACY="$TMP/legacy"
mkdir -p "$LEGACY"
make_hierarchy_yml "$LEGACY/500-my-epic/hierarchy.yml" "epic"
OUTPUT=$("$RESOLVE" --issue 500 --spec-base-path "$LEGACY" 2>/dev/null)
eval "$OUTPUT"
assert_eq "legacy flat: MODE=first-child" "first-child" "$MODE"
assert_eq "legacy flat: HIERARCHY_YML correct" "$LEGACY/500-my-epic/hierarchy.yml" "$HIERARCHY_YML"

# ── Summary ───────────────────────────────────────────────────────────────────
echo ""
TOTAL=$((PASS + FAIL))
echo "=== Results: $TOTAL tests | $PASS passed | $FAIL failed ==="

[[ "$FAIL" -eq 0 ]]
