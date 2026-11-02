#!/usr/bin/env bash
#
# test_critical_gate_remediation.sh - Integration tests for CRITICAL gate remediation
#
# Tests the _run_critical_gate_remediation function with mocked LLM/phase calls.
#
# Usage: test_critical_gate_remediation.sh
#
# Exit code: 0 if all tests pass, 1 if any test fails.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FIXTURES_DIR="$SCRIPT_DIR/fixtures"

# Source the gate library
# shellcheck source=check-analysis-gate.sh
source "$SCRIPT_DIR/check-analysis-gate.sh"

# Source generated-diagnostics path helpers (used by the remediation library)
# shellcheck source=lib/generated-artifacts.sh
source "$SCRIPT_DIR/lib/generated-artifacts.sh"

# Source the remediation library (tests the real implementation)
# shellcheck source=lib/critical-gate-remediation.sh
source "$SCRIPT_DIR/lib/critical-gate-remediation.sh"

PASS=0
FAIL=0
TOTAL=0

# ---------------------------------------------------------------------------
# Test helpers
# ---------------------------------------------------------------------------

assert_eq() {
    local description="$1"
    local expected="$2"
    local actual="$3"
    TOTAL=$((TOTAL + 1))

    if [[ "$actual" == "$expected" ]]; then
        echo "  ✅ $description"
        PASS=$((PASS + 1))
    else
        echo "  ❌ $description (expected='$expected', got='$actual')"
        FAIL=$((FAIL + 1))
    fi
}

assert_exit_code() {
    local description="$1"
    local expected_exit="$2"
    shift 2
    TOTAL=$((TOTAL + 1))

    local actual_exit=0
    "$@" || actual_exit=$?

    if [[ "$actual_exit" -eq "$expected_exit" ]]; then
        echo "  ✅ $description"
        PASS=$((PASS + 1))
    else
        echo "  ❌ $description (expected exit=$expected_exit, got exit=$actual_exit)"
        FAIL=$((FAIL + 1))
    fi
}

# ---------------------------------------------------------------------------
# Setup: Create a temp directory with test artifacts
# ---------------------------------------------------------------------------
setup_spec_dir() {
    local tmp_dir
    tmp_dir=$(mktemp -d)

    # Minimal spec.md
    cat > "$tmp_dir/spec.md" << 'EOF'
# Feature Specification: Test Feature

## Requirements

- FR-001: User login
- FR-005: User dashboard
EOF

    # Minimal tasks.md (missing coverage for FR-001 and FR-005)
    cat > "$tmp_dir/tasks.md" << 'EOF'
# Tasks: Test Feature

## Phase 1: Setup

- [ ] T001 Initialize project structure
EOF

    # Copy the criticals fixture as the analysis report
    cp "$FIXTURES_DIR/analysis-report-with-criticals.md" "$tmp_dir/analysis-report.md"

    echo "$tmp_dir"
}

# ---------------------------------------------------------------------------
# Test: critical_findings_json is set by check_analysis_gate on rc=10
# ---------------------------------------------------------------------------
echo ""
echo "=== Test: critical_findings_json caller-visible variable ==="

test_critical_findings_json_set() {
    critical_findings_json=""
    gate_result=""
    critical_count=""
    check_analysis_gate "$FIXTURES_DIR/analysis-report-with-criticals.md" "block" "false" >/dev/null 2>&1 || true
    assert_eq "critical_findings_json is non-empty on rc=10" "true" "$([[ -n "$critical_findings_json" && "$critical_findings_json" != "[]" ]] && echo true || echo false)"
    assert_eq "critical_count is 2" "2" "$critical_count"
}
test_critical_findings_json_set

test_critical_findings_json_empty_on_pass() {
    critical_findings_json="should-be-cleared"
    check_analysis_gate "$FIXTURES_DIR/analysis-report-no-criticals.md" "block" "false" >/dev/null 2>&1 || true
    assert_eq "critical_findings_json is [] on pass" "[]" "$critical_findings_json"
}
test_critical_findings_json_empty_on_pass

test_critical_findings_json_empty_on_malformed() {
    critical_findings_json="should-be-cleared"
    check_analysis_gate "$FIXTURES_DIR/analysis-report-malformed-no-table.md" "block" "false" >/dev/null 2>&1 || true
    assert_eq "critical_findings_json is [] on malformed report" "[]" "$critical_findings_json"
}
test_critical_findings_json_empty_on_malformed

# ---------------------------------------------------------------------------
# Test: remediated report passes the gate
# ---------------------------------------------------------------------------
echo ""
echo "=== Test: Remediated report passes gate ==="

test_remediated_report_passes() {
    local rc=0
    check_analysis_gate "$FIXTURES_DIR/analysis-report-remediated.md" "block" "false" >/dev/null 2>&1 || rc=$?
    assert_eq "Remediated report passes gate (rc=0)" "0" "$rc"
    assert_eq "gate_result is pass" "pass" "$gate_result"
    assert_eq "critical_count is 0" "0" "$critical_count"
}
test_remediated_report_passes

# ---------------------------------------------------------------------------
# Test: _run_critical_gate_remediation with mocked functions
# ---------------------------------------------------------------------------
echo ""
echo "=== Test: _run_critical_gate_remediation ==="

# The real _run_critical_gate_remediation is sourced from lib/critical-gate-remediation.sh.
# We define minimal mocks for its dependencies so the tests exercise the shipped logic.

# Mock helpers needed by _run_critical_gate_remediation
strip_model_footer() { echo "$1"; }
strip_llm_preamble() { echo "$1"; }
ensure_heading_start() { echo "$1"; }
append_model_footer() { true; }
run_artifact_verification() { return 0; }
publish_artifact_gate_outcome() { true; }
run_fr_validation_with_retry() { return 0; }
run_test_coverage_validation() { true; }

# Track call counts
_mock_reset() {
    MOCK_RUN_TASKS_CALLS=0
    MOCK_RUN_ANALYZE_CALLS=0
    MOCK_CALL_LLM_CALLS=0
    MOCK_GATE_PASS_AFTER=0
}

# --- Test: Layer 1 succeeds on first attempt ---
test_layer1_success() {
    _mock_reset
    local tmp_dir
    tmp_dir=$(setup_spec_dir)

    # Mock: tasks phase succeeds, analyze phase succeeds, then gate passes
    run_tasks_phase() { return 0; }
    run_analyze_phase() {
        # Replace with remediated report on first analyze call
        cp "$FIXTURES_DIR/analysis-report-remediated.md" "$tmp_dir/analysis-report.md"
        return 0
    }
    call_llm() { echo "# Tasks: Test"; }

    local rc=0
    _run_critical_gate_remediation "$tmp_dir" '[{"id":"F-01","summary":"test","recommendation":"fix"}]' 2>/dev/null || rc=$?
    assert_eq "Layer 1 success returns 0" "0" "$rc"
    assert_eq "Layer set to layer1" "layer1" "$critical_gate_remediation_layer"

    rm -rf "$tmp_dir"
}
test_layer1_success

# --- Test: Layer 1 fails, Layer 2 succeeds ---
test_layer2_success() {
    _mock_reset
    local tmp_dir
    tmp_dir=$(setup_spec_dir)

    local analyze_call_count=0

    # Mock: tasks phase fails all Layer 1 attempts
    run_tasks_phase() { return 1; }
    run_analyze_phase() {
        analyze_call_count=$((analyze_call_count + 1))
        # Layer 2 analyze call replaces report with remediated
        cp "$FIXTURES_DIR/analysis-report-remediated.md" "$tmp_dir/analysis-report.md"
        return 0
    }
    call_llm() { echo "# Tasks: Test Remediated"; }

    SPECKIT_CRITICAL_GATE_MAX_RETRIES=2
    local rc=0
    _run_critical_gate_remediation "$tmp_dir" '[{"id":"F-01","summary":"test","recommendation":"fix"}]' 2>/dev/null || rc=$?
    assert_eq "Layer 2 success returns 0" "0" "$rc"
    assert_eq "Layer set to layer2" "layer2" "$critical_gate_remediation_layer"

    # Verify tasks.md was patched with the mocked LLM output (call_llm is invoked in a
    # command-substitution subshell, so a counter variable cannot propagate back; assert
    # on the produced artifact instead).
    local tasks_content
    tasks_content=$(cat "$tmp_dir/tasks.md")
    assert_eq "tasks.md contains mocked LLM output (Layer 2 invoked call_llm)" "true" "$( [[ "$tasks_content" == *"Tasks: Test Remediated"* ]] && echo true || echo false )"

    rm -rf "$tmp_dir"
}
test_layer2_success

# --- Test: Both layers fail → returns 1 ---
test_both_layers_fail() {
    _mock_reset
    local tmp_dir
    tmp_dir=$(setup_spec_dir)

    # Mock: everything fails (report never changes)
    run_tasks_phase() { return 1; }
    run_analyze_phase() { return 0; }  # analyze succeeds but report stays with criticals
    call_llm() { echo "# Tasks: Broken"; }

    SPECKIT_CRITICAL_GATE_MAX_RETRIES=2
    local rc=0
    _run_critical_gate_remediation "$tmp_dir" '[{"id":"F-01","summary":"test","recommendation":"fix"}]' 2>/dev/null || rc=$?
    assert_eq "Both layers fail returns 1" "1" "$rc"

    rm -rf "$tmp_dir"
}
test_both_layers_fail

# --- Test: SPECKIT_CRITICAL_GATE_MAX_RETRIES=0 skips Layer 1 ---
test_max_retries_zero() {
    _mock_reset
    local tmp_dir
    tmp_dir=$(setup_spec_dir)

    run_tasks_phase() { MOCK_RUN_TASKS_CALLS=$((MOCK_RUN_TASKS_CALLS + 1)); return 0; }
    run_analyze_phase() {
        cp "$FIXTURES_DIR/analysis-report-remediated.md" "$tmp_dir/analysis-report.md"
        return 0
    }
    call_llm() { echo "# Tasks: Test"; }

    SPECKIT_CRITICAL_GATE_MAX_RETRIES=0
    local rc=0
    _run_critical_gate_remediation "$tmp_dir" '[{"id":"F-01","summary":"test","recommendation":"fix"}]' 2>/dev/null || rc=$?
    assert_eq "MAX_RETRIES=0 skips Layer 1, Layer 2 succeeds" "0" "$rc"
    assert_eq "Layer set to layer2" "layer2" "$critical_gate_remediation_layer"

    rm -rf "$tmp_dir"
}
test_max_retries_zero

# --- Test: SPECKIT_CRITICAL_GATE_REMEDIATION=false skips all ---
echo ""
echo "=== Test: Remediation disabled ==="

test_remediation_disabled() {
    local tmp_output
    tmp_output=$(mktemp)

    SPECKIT_CRITICAL_GATE_REMEDIATION="false"
    GITHUB_OUTPUT="$tmp_output"

    # Simulate what the gate block does
    local gate_mode="draft"
    local gate_rc=0
    check_analysis_gate "$FIXTURES_DIR/analysis-report-with-criticals.md" "$gate_mode" true >/dev/null 2>&1 || gate_rc=$?

    local status_emitted=""
    if [[ "$gate_rc" -eq 10 ]]; then
        if [[ "${SPECKIT_CRITICAL_GATE_REMEDIATION:-true}" == "true" ]]; then
            status_emitted="should-not-reach"
        else
            echo "critical_gate_remediation_status=skipped" >> "$tmp_output"
            status_emitted="skipped"
        fi
    fi

    local actual_status
    actual_status=$(grep "critical_gate_remediation_status=" "$tmp_output" | sed 's/critical_gate_remediation_status=//' | tail -1)
    assert_eq "Remediation disabled emits skipped" "skipped" "$actual_status"

    rm -f "$tmp_output"
    unset SPECKIT_CRITICAL_GATE_REMEDIATION
    unset GITHUB_OUTPUT
}
test_remediation_disabled

# ---------------------------------------------------------------------------
# Test: epic hierarchy — Layer 1 uses run_plan_phase, Layer 2 patches plan.md
# ---------------------------------------------------------------------------
echo ""
echo "=== Test: Epic hierarchy — remediation uses plan.md, not tasks.md ==="

setup_epic_spec_dir() {
    local tmp_dir
    tmp_dir=$(mktemp -d)

    cat > "$tmp_dir/spec.md" << 'EOF'
# Epic Specification: Test Epic

## Requirements

- FR-001: Sub-feature A
- FR-002: Sub-feature B
EOF

    cat > "$tmp_dir/plan.md" << 'EOF'
# Plan: Test Epic

## Phase 1: Foundation

- Establish architecture
EOF

    # No tasks.md — intentionally absent for epics
    cp "$FIXTURES_DIR/analysis-report-with-criticals.md" "$tmp_dir/analysis-report.md"

    echo "$tmp_dir"
}

# Test: epic Layer 1 calls run_plan_phase, not run_tasks_phase
test_epic_layer1_uses_plan_phase() {
    local tmp_dir
    tmp_dir=$(setup_epic_spec_dir)

    local plan_phase_calls=0
    local tasks_phase_calls=0

    run_plan_phase() {
        plan_phase_calls=$((plan_phase_calls + 1))
        return 0
    }
    run_tasks_phase() {
        tasks_phase_calls=$((tasks_phase_calls + 1))
        return 0
    }
    run_analyze_phase() {
        cp "$FIXTURES_DIR/analysis-report-remediated.md" "$tmp_dir/analysis-report.md"
        return 0
    }
    call_llm() { echo "# Plan: Test"; }

    SPECKIT_CRITICAL_GATE_MAX_RETRIES=2
    local rc=0
    _run_critical_gate_remediation "$tmp_dir" '[{"id":"F-01","summary":"test","recommendation":"fix"}]' "epic" 2>/dev/null || rc=$?
    assert_eq "Epic Layer 1 returns 0" "0" "$rc"
    # run_plan_phase/run_tasks_phase are called directly (not in a subshell), so the
    # counters propagate back to this shell — unlike call_llm which runs in $().
    assert_eq "Epic Layer 1 calls run_plan_phase" "true" "$([[ $plan_phase_calls -ge 1 ]] && echo true || echo false)"
    assert_eq "Epic Layer 1 does NOT call run_tasks_phase" "0" "$tasks_phase_calls"
    assert_eq "Layer set to layer1" "layer1" "$critical_gate_remediation_layer"
    assert_eq "tasks.md not created for epic" "false" "$([[ -f "$tmp_dir/tasks.md" ]] && echo true || echo false)"

    rm -rf "$tmp_dir"
}
test_epic_layer1_uses_plan_phase

# Test: epic Layer 2 patches plan.md, not tasks.md
test_epic_layer2_patches_plan_md() {
    local tmp_dir
    tmp_dir=$(setup_epic_spec_dir)

    run_plan_phase() { return 1; }  # Layer 1 fails → falls to Layer 2
    run_tasks_phase() { return 1; }
    run_analyze_phase() {
        cp "$FIXTURES_DIR/analysis-report-remediated.md" "$tmp_dir/analysis-report.md"
        return 0
    }
    call_llm() { echo "# Plan: Test Remediated"; }

    SPECKIT_CRITICAL_GATE_MAX_RETRIES=2
    local rc=0
    _run_critical_gate_remediation "$tmp_dir" '[{"id":"F-01","summary":"test","recommendation":"fix"}]' "epic" 2>/dev/null || rc=$?
    assert_eq "Epic Layer 2 returns 0" "0" "$rc"
    assert_eq "Layer set to layer2" "layer2" "$critical_gate_remediation_layer"
    assert_eq "Epic Layer 2 patched plan.md" "true" "$([[ "$(cat "$tmp_dir/plan.md")" == *"Test Remediated"* ]] && echo true || echo false)"
    assert_eq "tasks.md not created for epic" "false" "$([[ -f "$tmp_dir/tasks.md" ]] && echo true || echo false)"

    rm -rf "$tmp_dir"
}
test_epic_layer2_patches_plan_md

# Test: default (no hierarchy arg) still uses tasks.md — backward-compat
test_default_hierarchy_still_uses_tasks_md() {
    local tmp_dir
    tmp_dir=$(setup_spec_dir)

    run_tasks_phase() { return 0; }
    run_analyze_phase() {
        cp "$FIXTURES_DIR/analysis-report-remediated.md" "$tmp_dir/analysis-report.md"
        return 0
    }
    call_llm() { echo "# Tasks: Test"; }

    SPECKIT_CRITICAL_GATE_MAX_RETRIES=2
    local rc=0
    _run_critical_gate_remediation "$tmp_dir" '[{"id":"F-01","summary":"test","recommendation":"fix"}]' 2>/dev/null || rc=$?
    assert_eq "Default (no level arg) returns 0" "0" "$rc"
    assert_eq "Layer set to layer1 (default path)" "layer1" "$critical_gate_remediation_layer"

    rm -rf "$tmp_dir"
}
test_default_hierarchy_still_uses_tasks_md

# ---------------------------------------------------------------------------
# Test: artifact verification is re-run after each remediation rewrite
# ---------------------------------------------------------------------------
echo ""
echo "=== Test: Artifact verification re-run after remediation rewrites ==="

# Test: Layer 1 (feature) calls run_artifact_verification with phase 4
test_layer1_reruns_artifact_verification() {
    local tmp_dir
    tmp_dir=$(setup_spec_dir)

    local art_verify_calls=0
    local art_verify_phase=""
    local publish_calls=0
    local publish_status=""

    run_tasks_phase() { return 0; }
    run_analyze_phase() {
        cp "$FIXTURES_DIR/analysis-report-remediated.md" "$tmp_dir/analysis-report.md"
        return 0
    }
    run_artifact_verification() {
        art_verify_calls=$((art_verify_calls + 1))
        art_verify_phase="$1"
        return 0
    }
    publish_artifact_gate_outcome() {
        publish_calls=$((publish_calls + 1))
        publish_status="$1"
    }
    call_llm() { echo "# Tasks: Test"; }

    SPECKIT_CRITICAL_GATE_MAX_RETRIES=1
    local rc=0
    _run_critical_gate_remediation "$tmp_dir" '[{"id":"F-01","summary":"test","recommendation":"fix"}]' "feature" 2>/dev/null || rc=$?
    assert_eq "Layer 1 (feature) returns 0" "0" "$rc"
    assert_eq "Layer 1 (feature) calls run_artifact_verification" "true" "$([[ $art_verify_calls -ge 1 ]] && echo true || echo false)"
    assert_eq "Layer 1 (feature) passes phase 4 to run_artifact_verification" "4" "$art_verify_phase"
    assert_eq "Layer 1 (feature) calls publish_artifact_gate_outcome pass" "pass" "$publish_status"

    rm -rf "$tmp_dir"
}
test_layer1_reruns_artifact_verification

# Test: Layer 1 (epic) calls run_artifact_verification with phase 3
test_layer1_epic_reruns_artifact_verification() {
    local tmp_dir
    tmp_dir=$(setup_epic_spec_dir)

    local art_verify_phase=""

    run_plan_phase() { return 0; }
    run_tasks_phase() { return 1; }
    run_analyze_phase() {
        cp "$FIXTURES_DIR/analysis-report-remediated.md" "$tmp_dir/analysis-report.md"
        return 0
    }
    run_artifact_verification() {
        art_verify_phase="$1"
        return 0
    }
    publish_artifact_gate_outcome() { true; }
    call_llm() { echo "# Plan: Test"; }

    SPECKIT_CRITICAL_GATE_MAX_RETRIES=1
    local rc=0
    _run_critical_gate_remediation "$tmp_dir" '[{"id":"F-01","summary":"test","recommendation":"fix"}]' "epic" 2>/dev/null || rc=$?
    assert_eq "Layer 1 (epic) passes phase 3 to run_artifact_verification" "3" "$art_verify_phase"

    rm -rf "$tmp_dir"
}
test_layer1_epic_reruns_artifact_verification

# Test: Layer 1 aborts the current attempt when run_artifact_verification reports violations
test_layer1_aborts_on_artifact_violations() {
    local tmp_dir
    tmp_dir=$(setup_spec_dir)

    local published_statuses=()

    run_tasks_phase() { return 0; }
    run_analyze_phase() {
        # analyze is never called because the artifact gate failure causes continue
        cp "$FIXTURES_DIR/analysis-report-remediated.md" "$tmp_dir/analysis-report.md"
        return 0
    }
    run_artifact_verification() { return 1; }   # violations found — every attempt
    publish_artifact_gate_outcome() {
        published_statuses+=("$1")
    }
    call_llm() { echo "# Tasks: Test"; }

    # Layer 1 exhausts retries (artifact gate always fails), Layer 2 also fails
    # (artifact gate still returns 1), so the function returns 1.
    SPECKIT_CRITICAL_GATE_MAX_RETRIES=1
    local rc=0
    _run_critical_gate_remediation "$tmp_dir" '[{"id":"F-01","summary":"test","recommendation":"fix"}]' "feature" 2>/dev/null || rc=$?
    assert_eq "Artifact violations: returns 1 (remediation aborted)" "1" "$rc"
    local has_fail="false"
    for s in "${published_statuses[@]:-}"; do
        [[ "$s" == "fail" ]] && has_fail="true"
    done
    assert_eq "Artifact violations: publish_artifact_gate_outcome called with fail" "true" "$has_fail"

    rm -rf "$tmp_dir"
}
test_layer1_aborts_on_artifact_violations

# Test: Layer 2 calls run_artifact_verification after patching the artifact
test_layer2_reruns_artifact_verification() {
    local tmp_dir
    tmp_dir=$(setup_spec_dir)

    local art_verify_calls=0
    local art_verify_phase=""

    run_tasks_phase() { return 1; }   # Layer 1 always fails
    run_analyze_phase() {
        cp "$FIXTURES_DIR/analysis-report-remediated.md" "$tmp_dir/analysis-report.md"
        return 0
    }
    run_artifact_verification() {
        art_verify_calls=$((art_verify_calls + 1))
        art_verify_phase="$1"
        return 0
    }
    publish_artifact_gate_outcome() { true; }
    call_llm() { echo "# Tasks: Layer2 Test"; }

    SPECKIT_CRITICAL_GATE_MAX_RETRIES=2
    local rc=0
    _run_critical_gate_remediation "$tmp_dir" '[{"id":"F-01","summary":"test","recommendation":"fix"}]' "feature" 2>/dev/null || rc=$?
    assert_eq "Layer 2 (feature) returns 0" "0" "$rc"
    assert_eq "Layer 2 (feature) calls run_artifact_verification" "true" "$([[ $art_verify_calls -ge 1 ]] && echo true || echo false)"
    assert_eq "Layer 2 (feature) passes phase 4 to run_artifact_verification" "4" "$art_verify_phase"

    rm -rf "$tmp_dir"
}
test_layer2_reruns_artifact_verification

# Test: Layer 1 retries and succeeds on second attempt when artifact gate initially fails
test_layer1_retries_after_artifact_gate_failure() {
    local tmp_dir
    tmp_dir=$(setup_spec_dir)

    local art_verify_call_count=0

    run_tasks_phase() { return 0; }
    run_analyze_phase() {
        cp "$FIXTURES_DIR/analysis-report-remediated.md" "$tmp_dir/analysis-report.md"
        return 0
    }
    run_artifact_verification() {
        art_verify_call_count=$((art_verify_call_count + 1))
        # Fail on first attempt, pass on second
        if [[ "$art_verify_call_count" -eq 1 ]]; then
            return 1
        fi
        return 0
    }
    publish_artifact_gate_outcome() { true; }
    call_llm() { echo "# Tasks: Test"; }

    SPECKIT_CRITICAL_GATE_MAX_RETRIES=2
    local rc=0
    _run_critical_gate_remediation "$tmp_dir" '[{"id":"F-01","summary":"test","recommendation":"fix"}]' "feature" 2>/dev/null || rc=$?
    assert_eq "Layer 1 retries after artifact gate failure and succeeds" "0" "$rc"
    assert_eq "Layer set to layer1" "layer1" "$critical_gate_remediation_layer"
    assert_eq "run_artifact_verification called at least twice" "true" "$([[ $art_verify_call_count -ge 2 ]] && echo true || echo false)"

    rm -rf "$tmp_dir"
}
test_layer1_retries_after_artifact_gate_failure

test_layer1_retries_after_artifact_gate_operational_error() {
    local tmp_dir
    tmp_dir=$(setup_spec_dir)

    local art_verify_call_count=0
    local analyze_call_count=0
    local published_statuses=()

    run_tasks_phase() { return 0; }
    run_analyze_phase() {
        analyze_call_count=$((analyze_call_count + 1))
        cp "$FIXTURES_DIR/analysis-report-remediated.md" "$tmp_dir/analysis-report.md"
        return 0
    }
    run_artifact_verification() {
        art_verify_call_count=$((art_verify_call_count + 1))
        if [[ "$art_verify_call_count" -eq 1 ]]; then
            return 2
        fi
        return 0
    }
    publish_artifact_gate_outcome() {
        published_statuses+=("$1")
    }
    call_llm() { echo "# Tasks: Test"; }

    SPECKIT_CRITICAL_GATE_MAX_RETRIES=2
    local rc=0
    _run_critical_gate_remediation "$tmp_dir" '[{"id":"F-01","summary":"test","recommendation":"fix"}]' "feature" 2>/dev/null || rc=$?
    assert_eq "Artifact operational error: retries and succeeds" "0" "$rc"
    assert_eq "Artifact operational error: analyze skipped on failed first attempt" "1" "$analyze_call_count"
    assert_eq "Artifact operational error: publish_artifact_gate_outcome records fail" "true" "$(
        [[ " ${published_statuses[*]:-} " == *" fail "* ]] && echo true || echo false
    )"

    rm -rf "$tmp_dir"
}
test_layer1_retries_after_artifact_gate_operational_error

# ---------------------------------------------------------------------------
# Test: derived coverage refresh is called in Layer 1 and Layer 2 for feature level,
#       but NOT for epic level
# ---------------------------------------------------------------------------
echo ""
echo "=== Test: Derived coverage refresh ==="

test_layer1_refreshes_coverage_for_feature() {
    local tmp_dir
    tmp_dir=$(setup_spec_dir)

    local fr_refresh_calls=0
    local tc_refresh_calls=0

    run_tasks_phase() { return 0; }
    run_analyze_phase() {
        cp "$FIXTURES_DIR/analysis-report-remediated.md" "$tmp_dir/analysis-report.md"
        return 0
    }
    run_artifact_verification() { return 0; }
    publish_artifact_gate_outcome() { true; }
    run_fr_validation_with_retry() { fr_refresh_calls=$((fr_refresh_calls + 1)); return 0; }
    run_test_coverage_validation() { tc_refresh_calls=$((tc_refresh_calls + 1)); }
    call_llm() { echo "# Tasks: Test"; }

    SPECKIT_CRITICAL_GATE_MAX_RETRIES=1
    _run_critical_gate_remediation "$tmp_dir" '[{"id":"F-01","summary":"test","recommendation":"fix"}]' "feature" 2>/dev/null || true
    assert_eq "Layer 1 (feature) calls run_fr_validation_with_retry" "true" "$([[ $fr_refresh_calls -ge 1 ]] && echo true || echo false)"
    assert_eq "Layer 1 (feature) calls run_test_coverage_validation" "true" "$([[ $tc_refresh_calls -ge 1 ]] && echo true || echo false)"

    rm -rf "$tmp_dir"
}
test_layer1_refreshes_coverage_for_feature

test_layer1_skips_coverage_refresh_for_epic() {
    local tmp_dir
    tmp_dir=$(setup_epic_spec_dir)

    local fr_refresh_calls=0
    local tc_refresh_calls=0

    run_plan_phase() { return 0; }
    run_tasks_phase() { return 1; }
    run_analyze_phase() {
        cp "$FIXTURES_DIR/analysis-report-remediated.md" "$tmp_dir/analysis-report.md"
        return 0
    }
    run_artifact_verification() { return 0; }
    publish_artifact_gate_outcome() { true; }
    run_fr_validation_with_retry() { fr_refresh_calls=$((fr_refresh_calls + 1)); return 0; }
    run_test_coverage_validation() { tc_refresh_calls=$((tc_refresh_calls + 1)); }
    call_llm() { echo "# Plan: Test"; }

    SPECKIT_CRITICAL_GATE_MAX_RETRIES=1
    _run_critical_gate_remediation "$tmp_dir" '[{"id":"F-01","summary":"test","recommendation":"fix"}]' "epic" 2>/dev/null || true
    assert_eq "Layer 1 (epic) does NOT call run_fr_validation_with_retry" "0" "$fr_refresh_calls"
    assert_eq "Layer 1 (epic) does NOT call run_test_coverage_validation" "0" "$tc_refresh_calls"

    rm -rf "$tmp_dir"
}
test_layer1_skips_coverage_refresh_for_epic

test_layer2_refreshes_coverage_for_feature() {
    local tmp_dir
    tmp_dir=$(setup_spec_dir)

    local fr_refresh_calls=0
    local tc_refresh_calls=0

    run_tasks_phase() { return 1; }   # Layer 1 always fails → falls to Layer 2
    run_analyze_phase() {
        cp "$FIXTURES_DIR/analysis-report-remediated.md" "$tmp_dir/analysis-report.md"
        return 0
    }
    run_artifact_verification() { return 0; }
    publish_artifact_gate_outcome() { true; }
    run_fr_validation_with_retry() { fr_refresh_calls=$((fr_refresh_calls + 1)); return 0; }
    run_test_coverage_validation() { tc_refresh_calls=$((tc_refresh_calls + 1)); }
    call_llm() { echo "# Tasks: Layer2 Test"; }

    SPECKIT_CRITICAL_GATE_MAX_RETRIES=2
    _run_critical_gate_remediation "$tmp_dir" '[{"id":"F-01","summary":"test","recommendation":"fix"}]' "feature" 2>/dev/null || true
    assert_eq "Layer 2 (feature) calls run_fr_validation_with_retry" "true" "$([[ $fr_refresh_calls -ge 1 ]] && echo true || echo false)"
    assert_eq "Layer 2 (feature) calls run_test_coverage_validation" "true" "$([[ $tc_refresh_calls -ge 1 ]] && echo true || echo false)"

    rm -rf "$tmp_dir"
}
test_layer2_refreshes_coverage_for_feature

# ---------------------------------------------------------------------------
# Test: Layer 1 retries when FR coverage refresh fails, then succeeds on retry
# ---------------------------------------------------------------------------
echo ""
echo "=== Test: FR coverage refresh failure triggers retry ==="

test_layer1_retries_after_fr_coverage_failure() {
    local tmp_dir
    tmp_dir=$(setup_spec_dir)

    local tasks_call_count=0
    local fr_call_count=0

    run_tasks_phase() { tasks_call_count=$((tasks_call_count + 1)); return 0; }
    run_analyze_phase() {
        cp "$FIXTURES_DIR/analysis-report-remediated.md" "$tmp_dir/analysis-report.md"
        return 0
    }
    run_artifact_verification() { return 0; }
    publish_artifact_gate_outcome() { true; }
    run_fr_validation_with_retry() {
        fr_call_count=$((fr_call_count + 1))
        # Fail on first attempt, pass on second
        if [[ "$fr_call_count" -eq 1 ]]; then
            return 1
        fi
        return 0
    }
    run_test_coverage_validation() { true; }
    call_llm() { echo "# Tasks: Test"; }

    SPECKIT_CRITICAL_GATE_MAX_RETRIES=2
    local rc=0
    _run_critical_gate_remediation "$tmp_dir" '[{"id":"F-01","summary":"test","recommendation":"fix"}]' "feature" 2>/dev/null || rc=$?
    assert_eq "Layer 1 retries after FR coverage refresh failure and succeeds" "0" "$rc"
    assert_eq "Layer set to layer1" "layer1" "$critical_gate_remediation_layer"
    assert_eq "run_tasks_phase called at least twice" "true" "$([[ $tasks_call_count -ge 2 ]] && echo true || echo false)"

    rm -rf "$tmp_dir"
}
test_layer1_retries_after_fr_coverage_failure

test_layer2_retries_after_fr_coverage_failure() {
    local tmp_dir
    tmp_dir=$(setup_spec_dir)

    local fr_call_count=0

    run_tasks_phase() { return 1; }  # Layer 1 always fails → falls to Layer 2
    run_analyze_phase() {
        cp "$FIXTURES_DIR/analysis-report-remediated.md" "$tmp_dir/analysis-report.md"
        return 0
    }
    run_artifact_verification() { return 0; }
    publish_artifact_gate_outcome() { true; }
    run_fr_validation_with_retry() {
        fr_call_count=$((fr_call_count + 1))
        # Fail on first Layer 2 attempt, pass on second
        if [[ "$fr_call_count" -eq 1 ]]; then
            return 1
        fi
        return 0
    }
    run_test_coverage_validation() { true; }
    call_llm() { echo "# Tasks: Layer2 Test"; }

    SPECKIT_CRITICAL_GATE_MAX_RETRIES=2
    local rc=0
    _run_critical_gate_remediation "$tmp_dir" '[{"id":"F-01","summary":"test","recommendation":"fix"}]' "feature" 2>/dev/null || rc=$?
    assert_eq "Layer 2 retries after FR coverage refresh failure and succeeds" "0" "$rc"
    assert_eq "Layer set to layer2" "layer2" "$critical_gate_remediation_layer"
    assert_eq "run_fr_validation_with_retry called at least twice in Layer 2" "true" "$([[ $fr_call_count -ge 2 ]] && echo true || echo false)"

    rm -rf "$tmp_dir"
}
test_layer2_retries_after_fr_coverage_failure

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
echo ""
echo "========================================"
echo "Results: $PASS passed, $FAIL failed (total: $TOTAL)"
echo "========================================"

if [[ "$FAIL" -gt 0 ]]; then
    exit 1
fi
exit 0
