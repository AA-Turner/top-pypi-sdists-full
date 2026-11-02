#!/usr/bin/env bash
#
# test_check_idempotency.sh — tests for task directory ambiguity with spec context
#
# Usage: bash test_check_idempotency.sh
#
# Exit code: 0 if all tests pass, 1 if any test fails.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHECK_IDEMPOTENCY="$SCRIPT_DIR/check-idempotency.sh"
# shellcheck source=lib/spec-directory.sh
source "$SCRIPT_DIR/lib/spec-directory.sh"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

PASS=0
FAIL=0

assert_duplicate_fails() {
    local test_name="$1"
    local candidate_name="$2"
    local test_root="$TMP/$test_name"
    local specs_dir="$test_root/specs"
    local output_file="$test_root/output"
    local current_parent="$specs_dir/10-current"
    local old_parent="$specs_dir/20-old"
    local exit_code=0

    mkdir -p "$current_parent/$candidate_name" "$old_parent/$candidate_name"
    touch "$current_parent/$candidate_name/tasks.md" "$old_parent/$candidate_name/tasks.md"
    touch "$current_parent/spec.md" "$old_parent/spec.md"

    (
        cd "$test_root"
        SPEC_BASE_PATH=specs GITHUB_OUTPUT="$output_file" \
            "$CHECK_IDEMPOTENCY" 123 --phase 3 --level task \
            --spec-context specs/10-current/spec.md
    ) >/dev/null 2>&1 || exit_code=$?

    if [[ "$exit_code" -ne 0 ]] && ! grep -q '^skipped=true$' "$output_file" 2>/dev/null; then
        echo "  ✅ $test_name rejects duplicate Task directories across parent contexts"
        PASS=$((PASS + 1))
    else
        echo "  ❌ $test_name should reject duplicate Task directories across parent contexts"
        echo "     exit code: $exit_code"
        echo "     output: $(cat "$output_file" 2>/dev/null || true)"
        FAIL=$((FAIL + 1))
    fi
}

assert_flat_task_directory_proceeds_to_relocation() {
    local test_root="$TMP/flat-task"
    local specs_dir="$test_root/specs"
    local output_file="$test_root/output"
    mkdir -p "$specs_dir/10-current" "$specs_dir/123-task"
    touch "$specs_dir/10-current/spec.md" "$specs_dir/123-task/tasks.md"

    (
        cd "$test_root"
        SPEC_BASE_PATH=specs GITHUB_OUTPUT="$output_file" \
            "$CHECK_IDEMPOTENCY" 123 --phase 3 --level task \
            --spec-context specs/10-current/spec.md
    ) >/dev/null

    grep -q '^skipped=false$' "$output_file"
    echo "  ✅ flat artifact-only Task directory proceeds to relocation"
    PASS=$((PASS + 1))
}

assert_nested_task_directory_is_reused() {
    local test_root="$TMP/nested-task"
    local specs_dir="$test_root/specs"
    local output_file="$test_root/output"
    mkdir -p "$specs_dir/10-current/123"
    touch "$specs_dir/10-current/spec.md" "$specs_dir/10-current/123/tasks.md"

    (
        cd "$test_root"
        SPEC_BASE_PATH=specs GITHUB_OUTPUT="$output_file" \
            "$CHECK_IDEMPOTENCY" 123 --phase 3 --level task \
            --spec-context specs/10-current/spec.md
    ) >/dev/null

    grep -q '^skipped=true$' "$output_file"
    grep -q '^existing_spec=specs/10-current/123/tasks.md$' "$output_file"
    echo "  ✅ reuses correctly nested Task directory"
    PASS=$((PASS + 1))
}

assert_mixed_task_layout_fails() {
    local test_root="$TMP/mixed-layout"
    local specs_dir="$test_root/specs"
    local output_file="$test_root/output"
    local exit_code=0
    mkdir -p "$specs_dir/10-parent/123" "$specs_dir/10-parent/123-stale"
    touch "$specs_dir/10-parent/spec.md" "$specs_dir/10-parent/123/tasks.md"
    touch "$specs_dir/10-parent/123-stale/tasks.md"

    (
        cd "$test_root"
        SPEC_BASE_PATH=specs GITHUB_OUTPUT="$output_file" \
            "$CHECK_IDEMPOTENCY" 123 --phase 3 --level task \
            --spec-context specs/10-parent/spec.md
    ) >/dev/null 2>&1 || exit_code=$?

    if [[ "$exit_code" -ne 0 ]] && ! grep -q '^skipped=true$' "$output_file" 2>/dev/null; then
        echo "  ✅ rejects mixed numeric and issue-prefixed Task directories"
        PASS=$((PASS + 1))
    else
        echo "  ❌ should reject mixed numeric and issue-prefixed Task directories"
        echo "     exit code: $exit_code"
        echo "     output: $(cat "$output_file" 2>/dev/null || true)"
        FAIL=$((FAIL + 1))
    fi
}

assert_resolved_directory_does_not_bypass_source_ownership() {
    local test_root="$TMP/resolved-directory-ownership"
    local candidate="$test_root/specs/123-legacy"
    mkdir -p "$candidate" "$test_root/specs/10-parent"
    touch "$candidate/tasks.md" "$test_root/specs/10-parent/spec.md"

    if is_verified_inherited_task_directory \
        "$candidate" "$test_root" 123 task specs/10-parent/spec.md specs/123-legacy; then
        echo "  ❌ resolver path alone should not verify issue ownership"
        FAIL=$((FAIL + 1))
    else
        echo "  ✅ resolver path alone does not verify issue ownership"
        PASS=$((PASS + 1))
    fi

    if is_verified_inherited_task_directory \
        "$test_root/specs/10-parent/123-task" "$test_root" 123 task specs/10-parent/spec.md; then
        echo "  ✅ direct child of verified parent retains context-only exemption"
        PASS=$((PASS + 1))
    else
        echo "  ❌ direct child of verified parent should retain context-only exemption"
        FAIL=$((FAIL + 1))
    fi
}

assert_hierarchy_symlink_is_rejected() {
    local test_root="$TMP/hierarchy-symlink"
    local target="$test_root/parent-spec.md"
    local hierarchy_file="$test_root/task/hierarchy.yml"
    mkdir -p "$(dirname "$hierarchy_file")"
    printf 'parent spec remains unchanged\n' > "$target"
    ln -s "$target" "$hierarchy_file"

    if reconcile_task_parent_metadata "$hierarchy_file" 10 >/dev/null 2>&1; then
        echo "  ❌ should reject a symlinked hierarchy file"
        FAIL=$((FAIL + 1))
    elif [[ "$(cat "$target")" != "parent spec remains unchanged" ]]; then
        echo "  ❌ symlink rejection must leave the target unchanged"
        FAIL=$((FAIL + 1))
    else
        echo "  ✅ rejects symlinked hierarchy files without rewriting their targets"
        PASS=$((PASS + 1))
    fi
}

echo "=== check-idempotency.sh Task ambiguity tests ==="
assert_duplicate_fails "issue-prefixed" "123-task"
assert_duplicate_fails "numeric-fallback" "123"
assert_flat_task_directory_proceeds_to_relocation
assert_nested_task_directory_is_reused
assert_mixed_task_layout_fails
assert_resolved_directory_does_not_bypass_source_ownership
assert_hierarchy_symlink_is_rejected

echo ""
echo "=== Results: $((PASS + FAIL)) tests | $PASS passed | $FAIL failed ==="
[[ "$FAIL" -eq 0 ]]
