#!/usr/bin/env bash
#
# test_artifact_verification.sh - Unit tests for the pre-PR artifact gate wiring
#
# Tests run_artifact_verification, print_artifact_violations,
# publish_artifact_gate_outcome, run_artifact_verification_with_retry,
# write_artifact_verification_summary, _verify_retry_feedback_section, and the
# run_plan_phase prompt wiring for retry/remediation feedback. The functions are
# extracted from generate-spec-from-issue.sh and sourced in isolation, so the
# full pipeline orchestrator is never invoked.
#
# Requires the agdt-speckit-verify-artifacts entry point to be installed
# (pip install -e .).
#
# Usage: bash test_artifact_verification.sh
#
# Exit code: 0 if all tests pass, 1 if any test fails.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
export REPO_ROOT

if ! command -v agdt-speckit-verify-artifacts >/dev/null 2>&1; then
    echo "ERROR: agdt-speckit-verify-artifacts not installed (run: pip install -e .)" >&2
    exit 1
fi

# ---------------------------------------------------------------------------
# Extract the functions under test into a sourceable file.
# ---------------------------------------------------------------------------
FUNCS_FILE="$(mktemp)"
trap 'rm -f "$FUNCS_FILE"' EXIT

python3 - "$SCRIPT_DIR/generate-spec-from-issue.sh" > "$FUNCS_FILE" <<'PY'
import re
import sys

source = open(sys.argv[1], encoding="utf-8").read()
for name in (
    "run_artifact_verification",
    "print_artifact_violations",
    "publish_artifact_gate_outcome",
    "_report_artifact_gate_failure",
    "run_artifact_verification_with_retry",
    "write_artifact_verification_summary",
    "_verify_retry_feedback_section",
    "run_plan_phase",
):
    match = re.search(rf"^{re.escape(name)}\(\) \{{\n(.*?)^\}}\n", source, re.M | re.S)
    if match is None:
        raise SystemExit(f"Function not found in pipeline script: {name}")
    print(f"{name}() {{\n{match.group(1)}}}\n")
PY

# shellcheck source=/dev/null
source "$FUNCS_FILE"

# The pipeline sets these at startup; the extracted functions are sourced
# without it, so seed them here.  GITHUB_OUTPUT is always a real file so the
# gate's step outputs never leak into the assertions on captured stdout.
ARTIFACT_GATE_MODE="advisory"
ARTIFACT_GATE_STATUS=""
ARTIFACT_GATE_VIOLATIONS=""
ARTIFACT_GATE_PHASE_NUMBERS=""
ARTIFACT_GATE_PHASE_NAMES=""
ARTIFACT_GATE_PHASE_NUMBER=""
ARTIFACT_GATE_PHASE_NAME=""
GITHUB_OUTPUT="$(mktemp)"
export GITHUB_OUTPUT
trap 'rm -f "$FUNCS_FILE" "$GITHUB_OUTPUT"' EXIT

# Clears the in-memory gate state variables without touching persisted step
# outputs. Tests that need to preserve prior GITHUB_OUTPUT lines across a manual
# reconciliation rerun use this helper directly.
clear_gate_state_variables() {
    ARTIFACT_GATE_STATUS=""
    ARTIFACT_GATE_VIOLATIONS=""
    ARTIFACT_GATE_PHASE_NUMBERS=""
    ARTIFACT_GATE_PHASE_NAMES=""
    ARTIFACT_GATE_PHASE_NUMBER=""
    ARTIFACT_GATE_PHASE_NAME=""
}

# Restores the default gate mode and clears the sticky outcome + step outputs
# so each test starts from a known state.
reset_gate_state() {
    ARTIFACT_GATE_MODE="${1:-advisory}"
    clear_gate_state_variables
    : > "$GITHUB_OUTPUT"
}

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

assert_contains() {
    local description="$1"
    local needle="$2"
    local haystack="$3"
    TOTAL=$((TOTAL + 1))

    if printf '%s\n' "$haystack" | grep -qF -- "$needle"; then
        echo "  ✅ $description"
        PASS=$((PASS + 1))
    else
        echo "  ❌ $description (expected to contain '$needle')"
        FAIL=$((FAIL + 1))
    fi
}

assert_not_contains() {
    local description="$1"
    local needle="$2"
    local haystack="$3"
    TOTAL=$((TOTAL + 1))

    if printf '%s\n' "$haystack" | grep -qF -- "$needle"; then
        echo "  ❌ $description (expected NOT to contain '$needle')"
        FAIL=$((FAIL + 1))
    else
        echo "  ✅ $description"
        PASS=$((PASS + 1))
    fi
}

# Creates a spec dir whose artifacts pass every check.
make_clean_spec_dir() {
    SPEC_DIR="$(mktemp -d)"
    export SPEC_DIR
    printf '# Feature\n\n- **FR-001**: Do a thing.\n' > "$SPEC_DIR/spec.md"
    printf 'Implement the thing.\n' > "$SPEC_DIR/plan.md"
    printf -- '- [ ] T001 [P] Write unit tests for FR-001\n' > "$SPEC_DIR/tasks.md"
}

# Creates a spec dir whose plan.md references a file that does not exist.
# The sentence deliberately avoids create-intent verbs (add, create, implement,
# write, ...), otherwise the intent detector correctly treats the path as a file
# the plan intends to produce and the reference is not a violation.
make_broken_spec_dir() {
    SPEC_DIR="$(mktemp -d)"
    export SPEC_DIR
    printf '# Feature\n\n- **FR-001**: Do a thing.\n' > "$SPEC_DIR/spec.md"
    printf 'The handler lives in `pkg/definitely_absent.py` today.\n' > "$SPEC_DIR/plan.md"
}

# ---------------------------------------------------------------------------
# run_artifact_verification
# ---------------------------------------------------------------------------
test_verification_passes_on_clean_artifacts() {
    echo ""
    echo "TEST: run_artifact_verification passes on clean artifacts"
    make_clean_spec_dir

    local rc=0
    local output
    output=$(run_artifact_verification 3 2>&1) || rc=$?

    assert_eq "returns 0" "0" "$rc"
    assert_contains "reports success" "Artifact verification passed" "$output"
}
test_verification_passes_on_clean_artifacts

test_verification_reports_violations() {
    echo ""
    echo "TEST: run_artifact_verification returns 1 and names the violation"
    make_broken_spec_dir

    local rc=0
    local output
    output=$(run_artifact_verification 3 2>&1) || rc=$?

    assert_eq "returns 1" "1" "$rc"
    assert_contains "names the missing path" "pkg/definitely_absent.py" "$output"
    assert_contains "tags the check" "[referenced-path]" "$output"
}
test_verification_reports_violations

test_verification_writes_json_report() {
    echo ""
    echo "TEST: run_artifact_verification writes artifact-verification.json"
    make_broken_spec_dir
    run_artifact_verification 3 >/dev/null 2>&1 || true

    TOTAL=$((TOTAL + 1))
    if [[ -f "$SPEC_DIR/artifact-verification.json" ]]; then
        echo "  ✅ report file created"
        PASS=$((PASS + 1))
    else
        echo "  ❌ report file created (missing)"
        FAIL=$((FAIL + 1))
    fi

    assert_contains "report records the failure" '"passed": false' \
        "$(cat "$SPEC_DIR/artifact-verification.json")"
}
test_verification_writes_json_report

test_verification_unscoped_runs_all_checks() {
    echo ""
    echo "TEST: run_artifact_verification with no phase runs every check"
    SPEC_DIR="$(mktemp -d)"
    export SPEC_DIR
    printf '# Feature\n\n- **FR-001**: Do a thing.\n' > "$SPEC_DIR/spec.md"
    printf -- '- [ ] T001 Write unit tests for FR-999\n' > "$SPEC_DIR/tasks.md"

    local rc=0
    local output
    output=$(run_artifact_verification "" 2>&1) || rc=$?

    assert_eq "returns 1" "1" "$rc"
    assert_contains "labels the run as unscoped" "all checks" "$output"
    assert_contains "detects the undefined FR" "FR-999" "$output"
}
test_verification_unscoped_runs_all_checks

# ---------------------------------------------------------------------------
# run_artifact_verification_with_retry
# ---------------------------------------------------------------------------
test_retry_regenerates_then_passes() {
    echo ""
    echo "TEST: retry loop regenerates once, then passes"
    make_broken_spec_dir
    export VERIFY_MAX_RETRIES=2

    ATTEMPTS=0
    FEEDBACK_SEEN=""
    fixing_regenerator() {
        ATTEMPTS=$((ATTEMPTS + 1))
        FEEDBACK_SEEN="${SPECKIT_VERIFY_RETRY_FEEDBACK:-}"
        printf 'Implement the thing.\n' > "$SPEC_DIR/plan.md"
    }

    local rc=0
    run_artifact_verification_with_retry 3 fixing_regenerator >/dev/null 2>&1 || rc=$?

    assert_eq "returns 0" "0" "$rc"
    assert_eq "regenerated exactly once" "1" "$ATTEMPTS"
    assert_contains "violations were fed back to the generator" \
        "pkg/definitely_absent.py" "$FEEDBACK_SEEN"
}
test_retry_regenerates_then_passes

test_retry_clears_feedback_after_use() {
    echo ""
    echo "TEST: retry feedback never leaks into a later phase"
    assert_eq "SPECKIT_VERIFY_RETRY_FEEDBACK unset after retry" \
        "" "${SPECKIT_VERIFY_RETRY_FEEDBACK:-}"
}
test_retry_clears_feedback_after_use

test_retry_respects_budget() {
    echo ""
    echo "TEST: retry loop stops at VERIFY_MAX_RETRIES and reports the violations"
    make_broken_spec_dir
    export VERIFY_MAX_RETRIES=2
    reset_gate_state advisory

    stubborn_regenerator() {
        printf 'The handler still lives in `pkg/definitely_absent.py`.\n' > "$SPEC_DIR/plan.md"
    }

    local rc=0
    local output
    output=$(run_artifact_verification_with_retry 3 stubborn_regenerator 2>&1) || rc=$?

    assert_eq "returns 0 in advisory mode" "0" "$rc"
    assert_contains "first retry attempted" "Retry (1/2)" "$output"
    assert_contains "second retry attempted" "Retry (2/2)" "$output"
    assert_not_contains "does not exceed the budget" "Retry (3/2)" "$output"
    assert_contains "reports the exhausted budget" "after 2 regeneration attempt(s)" "$output"
    assert_contains "explains the advisory outcome" "still opened as a draft" "$output"
    assert_not_contains "does not claim the PR is blocked" "No pull request will be opened" "$output"

    local outputs
    outputs=$(cat "$GITHUB_OUTPUT")
    assert_contains "records the gate failure as a step output" \
        "artifact_gate_result=fail" "$outputs"
    assert_contains "records the failing internal gate phase number" \
        "artifact_gate_phase_number=3" "$outputs"
    assert_contains "records the failing internal gate phase name" \
        "artifact_gate_phase_name=plan" "$outputs"
    assert_contains "publishes the violations for the PR comment" \
        "pkg/definitely_absent.py" "$outputs"
}
test_retry_respects_budget

test_retry_blocks_when_gate_mode_is_block() {
    echo ""
    echo "TEST: block mode fails loudly so no PR is opened"
    make_broken_spec_dir
    export VERIFY_MAX_RETRIES=2
    reset_gate_state block

    stubborn_regenerator() {
        printf 'The handler still lives in `pkg/definitely_absent.py`.\n' > "$SPEC_DIR/plan.md"
    }

    local rc=0
    local output
    output=$(run_artifact_verification_with_retry 3 stubborn_regenerator 2>&1) || rc=$?

    assert_eq "returns 1" "1" "$rc"
    assert_contains "states no PR will be opened" "No pull request will be opened" "$output"
    assert_contains "reports the failure as an error" "Error: Artifact verification failed" "$output"
    reset_gate_state advisory
}
test_retry_blocks_when_gate_mode_is_block

test_regenerator_failure_reports_instead_of_aborting() {
    echo ""
    echo "TEST: a crashed regenerator does not discard the phase in advisory mode"
    make_broken_spec_dir
    export VERIFY_MAX_RETRIES=2
    reset_gate_state advisory

    failing_regenerator() { return 1; }

    local rc=0
    local output
    output=$(run_artifact_verification_with_retry 3 failing_regenerator 2>&1) || rc=$?

    assert_eq "returns 0 in advisory mode" "0" "$rc"
    assert_contains "names the failed regenerator" "failing_regenerator failed" "$output"
    assert_contains "still publishes the violations" "artifact_gate_result=fail" \
        "$(cat "$GITHUB_OUTPUT")"
}
test_regenerator_failure_reports_instead_of_aborting

test_regenerator_failure_restores_pre_retry_artifacts() {
    echo ""
    echo "TEST: a failed regenerator restores the pre-retry artifacts before reporting violations"
    make_broken_spec_dir
    export VERIFY_MAX_RETRIES=2
    reset_gate_state advisory

    rewriting_regenerator() {
        printf 'The handler lives in `pkg/rewritten_absent.py` today.\n' > "$SPEC_DIR/plan.md"
        return 1
    }

    run_artifact_verification_with_retry 3 rewriting_regenerator >/dev/null 2>&1 || true

    local published
    published="$(cat "$GITHUB_OUTPUT")"
    assert_contains "keeps pre-retry violation" "pkg/definitely_absent.py" "$published"
    assert_not_contains "does not keep rewritten partial artifact violation" "pkg/rewritten_absent.py" "$published"
}
test_regenerator_failure_restores_pre_retry_artifacts

test_regenerator_failure_aborts_in_block_mode() {
    echo ""
    echo "TEST: a crashed regenerator aborts the phase in block mode"
    make_broken_spec_dir
    export VERIFY_MAX_RETRIES=2
    reset_gate_state block

    failing_regenerator() { return 1; }

    local rc=0
    run_artifact_verification_with_retry 3 failing_regenerator >/dev/null 2>&1 || rc=$?

    assert_eq "returns 1" "1" "$rc"
    reset_gate_state advisory
}
test_regenerator_failure_aborts_in_block_mode

test_retry_without_regenerator_reports_immediately() {
    echo ""
    echo "TEST: no regenerator means a violation is reported without retrying"
    make_broken_spec_dir
    export VERIFY_MAX_RETRIES=2
    reset_gate_state advisory

    local rc=0
    local output
    output=$(run_artifact_verification_with_retry 3 "" 2>&1) || rc=$?

    assert_eq "returns 0 in advisory mode" "0" "$rc"
    assert_not_contains "no retry attempted" "Retry (1/2)" "$output"
    assert_contains "reports zero attempts" "after 0 regeneration attempt(s)" "$output"
}
test_retry_without_regenerator_reports_immediately

test_gate_outcome_failure_is_sticky() {
    echo ""
    echo "TEST: a passing phase never erases an earlier phase's failure"
    make_broken_spec_dir
    export VERIFY_MAX_RETRIES=0
    reset_gate_state advisory

    run_artifact_verification_with_retry 3 "" >/dev/null 2>&1

    make_clean_spec_dir
    run_artifact_verification_with_retry 3 "" >/dev/null 2>&1

    assert_eq "sticky status stays fail" "fail" "$ARTIFACT_GATE_STATUS"
    assert_not_contains "no pass output overwrites the failure" \
        "artifact_gate_result=pass" "$(cat "$GITHUB_OUTPUT")"
}
test_gate_outcome_failure_is_sticky

test_gate_outcome_accumulates_violations() {
    echo ""
    echo "TEST: violations from several phase-scoped gates accumulate"
    make_broken_spec_dir
    export VERIFY_MAX_RETRIES=0
    reset_gate_state advisory

    run_artifact_verification_with_retry 3 "" >/dev/null 2>&1

    SPEC_DIR="$(mktemp -d)"
    export SPEC_DIR
    printf '# Feature\n\n- **FR-001**: Do a thing.\n' > "$SPEC_DIR/spec.md"
    printf -- '- [ ] T001 Write unit tests for FR-777\n' > "$SPEC_DIR/tasks.md"
    run_artifact_verification_with_retry 4 "" >/dev/null 2>&1

    assert_contains "keeps the first phase's violation" \
        "pkg/definitely_absent.py" "$ARTIFACT_GATE_VIOLATIONS"
    assert_contains "adds the second phase's violation" \
        "FR-777" "$ARTIFACT_GATE_VIOLATIONS"
}
test_gate_outcome_accumulates_violations

test_gate_outcome_publishes_pass() {
    echo ""
    echo "TEST: a clean run publishes artifact_gate_result=pass"
    make_clean_spec_dir
    export VERIFY_MAX_RETRIES=2
    reset_gate_state advisory

    run_artifact_verification_with_retry 3 "" >/dev/null 2>&1

    local outputs
    outputs=$(cat "$GITHUB_OUTPUT")
    assert_contains "records the pass" "artifact_gate_result=pass" "$outputs"
    assert_contains "records the passing gate phase number" "artifact_gate_phase_number=3" "$outputs"
    assert_contains "records the passing gate phase name" "artifact_gate_phase_name=plan" "$outputs"
    assert_not_contains "publishes no violations" "artifact_gate_violations" "$outputs"
}
test_gate_outcome_publishes_pass

test_monolithic_reconciliation_clears_sticky_failure() {
    echo ""
    echo "TEST: final unscoped reconciliation can clear a sticky failure"
    make_broken_spec_dir
    export VERIFY_MAX_RETRIES=0
    reset_gate_state advisory

    run_artifact_verification_with_retry 3 "" >/dev/null 2>&1

    local result_lines_before phase_number_lines_before phase_name_lines_before
    result_lines_before=$(grep -c '^artifact_gate_result=' "$GITHUB_OUTPUT")
    phase_number_lines_before=$(grep -c '^artifact_gate_phase_number=' "$GITHUB_OUTPUT")
    phase_name_lines_before=$(grep -c '^artifact_gate_phase_name=' "$GITHUB_OUTPUT")

    make_clean_spec_dir
    clear_gate_state_variables
    run_artifact_verification_with_retry "" "" >/dev/null 2>&1

    assert_eq "reconciled status becomes pass" "pass" "$ARTIFACT_GATE_STATUS"
    assert_eq "final unscoped rerun appends a new gate result output" \
        "$((result_lines_before + 1))" \
        "$(grep -c '^artifact_gate_result=' "$GITHUB_OUTPUT")"
    assert_eq "final unscoped rerun appends a new phase-number output" \
        "$((phase_number_lines_before + 1))" \
        "$(grep -c '^artifact_gate_phase_number=' "$GITHUB_OUTPUT")"
    assert_eq "final unscoped rerun appends a new phase-name output" \
        "$((phase_name_lines_before + 1))" \
        "$(grep -c '^artifact_gate_phase_name=' "$GITHUB_OUTPUT")"
    assert_eq "latest published gate result is pass" \
        "artifact_gate_result=pass" \
        "$(grep '^artifact_gate_result=' "$GITHUB_OUTPUT" | tail -1)"
    assert_eq "latest published gate phase number is empty for unscoped rerun" \
        "artifact_gate_phase_number=" \
        "$(grep '^artifact_gate_phase_number=' "$GITHUB_OUTPUT" | tail -1)"
    assert_eq "latest published gate phase name is empty for unscoped rerun" \
        "artifact_gate_phase_name=" \
        "$(grep '^artifact_gate_phase_name=' "$GITHUB_OUTPUT" | tail -1)"
}
test_monolithic_reconciliation_clears_sticky_failure

test_retry_does_not_regenerate_on_operational_error() {
    echo ""
    echo "TEST: an operational error returns 2 in block mode without regenerating"
    SPEC_DIR="$(mktemp -d)/definitely-not-created"
    export SPEC_DIR
    export VERIFY_MAX_RETRIES=2
    reset_gate_state block

    ATTEMPTS=0
    counting_regenerator() { ATTEMPTS=$((ATTEMPTS + 1)); }

    local rc=0
    run_artifact_verification_with_retry 3 counting_regenerator >/dev/null 2>&1 || rc=$?

    assert_eq "returns 2" "2" "$rc"
    assert_eq "never regenerated" "0" "$ATTEMPTS"
    reset_gate_state advisory
}
test_retry_does_not_regenerate_on_operational_error

test_operational_error_is_skipped_in_advisory_mode() {
    echo ""
    echo "TEST: an operational error preserves generation and publishes fail outcome in advisory mode"
    SPEC_DIR="$(mktemp -d)/definitely-not-created"
    export SPEC_DIR
    export VERIFY_MAX_RETRIES=2
    reset_gate_state advisory

    ATTEMPTS=0
    counting_regenerator() { ATTEMPTS=$((ATTEMPTS + 1)); }

    local rc=0
    local output
    output=$(run_artifact_verification_with_retry 3 counting_regenerator 2>&1) || rc=$?

    assert_eq "returns 0 (generation preserved)" "0" "$rc"
    assert_eq "never regenerated" "0" "$ATTEMPTS"
    assert_contains "warns that the gate could not run" "generation is preserved but gate status is set to fail" "$output"
    assert_contains "records a fail outcome so the PR is drafted" \
        "artifact_gate_result=fail" "$(cat "$GITHUB_OUTPUT")"
}
test_operational_error_is_skipped_in_advisory_mode

# ---------------------------------------------------------------------------
# write_artifact_verification_summary
# ---------------------------------------------------------------------------
test_step_summary_records_violations() {
    echo ""
    echo "TEST: violations are written to GITHUB_STEP_SUMMARY"
    make_broken_spec_dir
    export VERIFY_MAX_RETRIES=2
    reset_gate_state advisory
    GITHUB_STEP_SUMMARY="$(mktemp)"
    export GITHUB_STEP_SUMMARY

    run_artifact_verification_with_retry 3 "" >/dev/null 2>&1 || true

    local summary
    summary=$(cat "$GITHUB_STEP_SUMMARY")
    assert_contains "summary has a failure heading" "artifact verification failed" "$summary"
    assert_contains "summary names the advisory mode" "advisory mode" "$summary"
    assert_contains "summary lists the violation" "pkg/definitely_absent.py" "$summary"
    unset GITHUB_STEP_SUMMARY
}
test_step_summary_records_violations

test_step_summary_reports_blocked_pr_in_block_mode() {
    echo ""
    echo "TEST: block mode summary states no PR was opened"
    make_broken_spec_dir
    export VERIFY_MAX_RETRIES=2
    reset_gate_state block
    GITHUB_STEP_SUMMARY="$(mktemp)"
    export GITHUB_STEP_SUMMARY

    run_artifact_verification_with_retry 3 "" >/dev/null 2>&1 || true

    local summary
    summary=$(cat "$GITHUB_STEP_SUMMARY")
    assert_contains "summary has a failure heading" "artifact verification failed" "$summary"
    assert_contains "summary states the PR was blocked" "No pull request was opened" "$summary"
    unset GITHUB_STEP_SUMMARY
    reset_gate_state advisory
}
test_step_summary_reports_blocked_pr_in_block_mode

test_step_summary_noop_outside_actions() {
    echo ""
    echo "TEST: summary write is a no-op outside GitHub Actions"
    unset GITHUB_STEP_SUMMARY

    local rc=0
    write_artifact_verification_summary || rc=$?
    assert_eq "returns 0 with no GITHUB_STEP_SUMMARY" "0" "$rc"
}
test_step_summary_noop_outside_actions

# ---------------------------------------------------------------------------
# _verify_retry_feedback_section
# ---------------------------------------------------------------------------
test_feedback_section_empty_without_retry() {
    echo ""
    echo "TEST: feedback section is empty when no retry is in progress"
    unset SPECKIT_VERIFY_RETRY_FEEDBACK

    local section
    section=$(_verify_retry_feedback_section)
    assert_eq "renders nothing" "" "$section"
}
test_feedback_section_empty_without_retry

test_feedback_section_appends_violations() {
    echo ""
    echo "TEST: feedback section appends violations to a prompt"
    export SPECKIT_VERIFY_RETRY_FEEDBACK="  - [fr-reference] tasks.md: FR-009 undefined."

    local prompt="BASE PROMPT"
    prompt="$prompt$(_verify_retry_feedback_section)"

    assert_contains "original prompt preserved" "BASE PROMPT" "$prompt"
    assert_contains "feedback heading added" "Artifact Verification Feedback (Retry)" "$prompt"
    assert_contains "violation included" "FR-009 undefined" "$prompt"
    unset SPECKIT_VERIFY_RETRY_FEEDBACK
}
test_feedback_section_appends_violations

test_plan_phase_appends_critical_feedback() {
    echo ""
    echo "TEST: plan phase appends CRITICAL remediation feedback to the prompt"

    local spec_dir
    spec_dir=$(mktemp -d)
    printf '# Feature Specification\n\n- FR-001: Test requirement\n' > "$spec_dir/spec.md"

    local prompt_file
    prompt_file=$(mktemp)

    strip_model_footer() { printf '%s' "$1"; }
    strip_llm_preamble() { printf '%s' "$1"; }
    _derive_plan_artifact_heading() { echo "# Implementation Plan"; }
    ensure_heading_start() { printf '%s' "$1"; }
    append_model_footer() { :; }
    call_llm() {
        printf '%s' "$1" > "$prompt_file"
        cat <<'EOF'
===ARTIFACT:plan.md===
# Implementation Plan
EOF
    }

    SPEC_DIR="$spec_dir"
    export SPEC_DIR
    export SPECKIT_CRITICAL_GATE_FEEDBACK="  - [F-01] Missing FR coverage → add the missing phase"

    local rc=0
    run_plan_phase >/dev/null 2>&1 || rc=$?
    local prompt
    prompt=$(cat "$prompt_file")

    assert_eq "plan phase succeeds" "0" "$rc"
    assert_contains "prompt includes CRITICAL heading" "CRITICAL Analysis Gate Feedback (Remediation)" "$prompt"
    assert_contains "prompt includes finding details" "Missing FR coverage" "$prompt"
    assert_contains "prompt includes remediation instruction" "You MUST address ALL findings listed above in plan.md" "$prompt"
    assert_eq "critical feedback cleared after use" "" "${SPECKIT_CRITICAL_GATE_FEEDBACK:-}"

    rm -rf "$spec_dir"
    rm -f "$prompt_file"
}
test_plan_phase_appends_critical_feedback

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
