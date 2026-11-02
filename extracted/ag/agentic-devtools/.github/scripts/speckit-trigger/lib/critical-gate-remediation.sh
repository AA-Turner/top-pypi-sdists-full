#!/usr/bin/env bash
#
# critical-gate-remediation.sh - Library for CRITICAL analysis gate remediation
#
# This is a **library** script — it defines functions only and has no
# top-level side effects.  It is sourced by generate-spec-from-issue.sh
# and test_critical_gate_remediation.sh.
#
# Dependencies (must be defined by the sourcing script):
#   Functions: run_tasks_phase, run_plan_phase, run_analyze_phase, call_llm,
#              strip_model_footer, strip_llm_preamble, ensure_heading_start,
#              append_model_footer, check_analysis_gate,
#              run_artifact_verification, publish_artifact_gate_outcome,
#              run_fr_validation_with_retry, run_test_coverage_validation,
#              resolve_generated_artifact (lib/generated-artifacts.sh)
#   Variables: SPECKIT_CRITICAL_GATE_MAX_RETRIES (env, default: 2)
#
# Caller-visible variables set on return:
#   critical_gate_remediation_layer = "layer1" | "layer2"

# ---------------------------------------------------------------------------
# _rerun_artifact_gate_check <layer_label> <phase_num> <artifact_label>
#
# Re-runs the artifact verification gate for the given pipeline phase and
# publishes the outcome via publish_artifact_gate_outcome.
#
# Called after each remediation rewrite (Layer 1 and Layer 2) to ensure that
# structural violations (missing-path, FR-reference, unmapped-test) introduced
# by the rewrite are reflected in artifact_gate_result rather than being silently
# absorbed into the earlier passing result.
#
# Returns:
#   0  — gate passed; caller may proceed to run_analyze_phase
#   1  — any non-pass outcome (violations or operational error); caller should
#        retry or abort the current attempt before analyze runs
#   Operational errors are recorded as a synthetic fail outcome so downstream
#   workflow logic cannot treat an unverified rewrite as gate-passing.
# ---------------------------------------------------------------------------
_rerun_artifact_gate_check() {
    local layer_label="$1"
    local phase_num="$2"
    local artifact_label="$3"

    local _saved_gate_phase="${ARTIFACT_GATE_PHASE_NUMBER:-}"
    ARTIFACT_GATE_PHASE_NUMBER="$phase_num"
    local _verify_rc=0
    run_artifact_verification "$phase_num" || _verify_rc=$?
    ARTIFACT_GATE_PHASE_NUMBER="$_saved_gate_phase"

    if [[ "$_verify_rc" -eq 0 ]]; then
        publish_artifact_gate_outcome pass
        return 0
    fi

    if [[ "$_verify_rc" -eq 1 ]]; then
        echo "[CRITICAL Gate] $layer_label: Warning: Artifact gate violations after ${artifact_label} phase rewrite" >&2
    else
        echo "[CRITICAL Gate] $layer_label: Warning: Artifact gate could not run after ${artifact_label} phase rewrite (rc=$_verify_rc)" >&2
        local _operational_message="(operational gate error after ${artifact_label} rewrite — verification could not run; exit code $_verify_rc)"
        if [[ -z "${ARTIFACT_GATE_VIOLATIONS:-}" ]]; then
            ARTIFACT_GATE_VIOLATIONS="$_operational_message"
        else
            ARTIFACT_GATE_VIOLATIONS="${ARTIFACT_GATE_VIOLATIONS}"$'\n'"$_operational_message"
        fi
    fi
    publish_artifact_gate_outcome fail
    return 1
}

# ---------------------------------------------------------------------------
# _refresh_derived_coverage <hierarchy_level>
#
# Refreshes fr-coverage.json and test-coverage.json after tasks.md has been
# rewritten (Layer 1 or Layer 2 remediation for feature-level specs).
#
# Must be called before run_artifact_verification and run_analyze_phase so that
# those steps see data consistent with the new tasks.md rather than the
# pre-remediation state.  Without this refresh, run_analyze_phase labels the
# old coverage files as "Pre-Validated" even though the task set has changed.
#
# Skipped for:
#   "epic"  — plan.md is the primary artifact; no tasks.md/fr-coverage exist.
#   "task"  — inherits coverage from parent feature; local files are not updated.
# ---------------------------------------------------------------------------
_refresh_derived_coverage() {
    local level="$1"
    if [[ "$level" == "epic" || "$level" == "task" ]]; then
        return 0
    fi

    local fr_rc=0
    run_fr_validation_with_retry || fr_rc=$?
    if [[ "$fr_rc" -ne 0 ]]; then
        echo "[CRITICAL Gate] FR coverage validation failed during derived-data refresh (rc=$fr_rc) — aborting attempt" >&2
        return "$fr_rc"
    fi
    run_test_coverage_validation
}

# ---------------------------------------------------------------------------
# _run_critical_gate_remediation <spec_dir> <findings_json> [hierarchy_level]
#
# Multi-layer LLM remediation for unresolved CRITICAL analysis findings.
# Called when check_analysis_gate returns code 10 (unresolved CRITICALs).
#
# hierarchy_level (optional, default "feature"):
#   "epic"    — tasks step is intentionally skipped; Layer 1 re-runs plan phase
#               and Layer 2 patches plan.md instead of tasks.md.
#   "feature" / "task" / (any other) — standard behavior (tasks phase / tasks.md).
#
# Recovery layers:
#   Layer 1: Standard LLM remediation — re-run the primary artifact phase
#            (tasks for feature/task, plan for epic) with findings as feedback,
#            then re-run analyze phase and re-check gate.  Bounded by
#            SPECKIT_CRITICAL_GATE_MAX_RETRIES (default: 2).
#   Layer 2: Alternate LLM remediation — use a distinct prompt strategy
#            (focused on self-validation) to directly patch the primary artifact
#            (tasks.md for feature/task, plan.md for epic) via call_llm, then
#            re-run analyze phase and re-check gate.  Up to 2 attempts.
#
# Returns 0 if all CRITICALs are resolved, 1 otherwise.
# Sets caller-visible: critical_gate_remediation_layer ("layer1" or "layer2")
# ---------------------------------------------------------------------------
_run_critical_gate_remediation() {
    local spec_dir="$1"
    local findings_json_input="$2"
    local hierarchy_level="${3:-feature}"

    # For epics the tasks step is intentionally absent; remediation must operate
    # on plan.md instead of tasks.md to avoid creating an artifact that should
    # not exist at this hierarchy level.
    local _primary_artifact_file _primary_artifact_label
    # Artifact verification phase number: step 3 verified plan.md (epic), step 4 verified
    # tasks.md (feature/task).  Re-running the same step after a remediation rewrite catches
    # structural violations (missing-path, FR-reference, unmapped-test) that the rewrite may
    # have introduced before those defects can escape into a passing artifact_gate_result.
    local _artifact_phase_num
    if [[ "$hierarchy_level" == "epic" ]]; then
        _primary_artifact_file="plan.md"
        _primary_artifact_label="plan"
        _artifact_phase_num="3"
    else
        _primary_artifact_file="tasks.md"
        _primary_artifact_label="tasks"
        _artifact_phase_num="4"
    fi

    # Save and override SPEC_DIR so run_tasks_phase/run_plan_phase/run_analyze_phase
    # operate on the correct directory regardless of the caller's SPEC_DIR value.
    local _saved_spec_dir="${SPEC_DIR:-}"
    SPEC_DIR="$spec_dir"

    # Sanitize max_retries: default to 2 on invalid/non-integer input, allow 0
    local max_retries="${SPECKIT_CRITICAL_GATE_MAX_RETRIES:-2}"
    if ! [[ "$max_retries" =~ ^[0-9]+$ ]]; then
        echo "[CRITICAL Gate] Warning: Invalid SPECKIT_CRITICAL_GATE_MAX_RETRIES='$max_retries', defaulting to 2" >&2
        max_retries=2
    fi
    local attempt

    # Initialize caller-visible variable to avoid stale values across calls
    critical_gate_remediation_layer=""

    # ── Layer 1: Standard LLM remediation ───────────────────────────────
    if [[ "$max_retries" -gt 0 ]]; then
        echo "[CRITICAL Gate] Layer 1: Standard LLM remediation (max $max_retries retries)" >&2

        for (( attempt=1; attempt<=max_retries; attempt++ )); do
            echo "[CRITICAL Gate] Layer 1: Attempt $attempt/$max_retries" >&2

            # Build feedback from findings JSON
            local feedback=""
            feedback=$(python3 -c "
import json, sys
findings = json.loads(sys.argv[1])
lines = ['The following CRITICAL findings MUST be resolved in ${_primary_artifact_label}.md:']
for f in findings:
    lines.append(f\"  - [{f['id']}] {f['summary']} → {f['recommendation']}\")
lines.append('')
lines.append('Ensure every requirement in spec.md has at least one corresponding entry in ${_primary_artifact_label}.md.')
print('\n'.join(lines))
" "$findings_json_input" 2>/dev/null) || {
                echo "[CRITICAL Gate] Layer 1: Warning: Failed to parse findings JSON in attempt $attempt" >&2
                continue
            }

            # Re-run the primary artifact phase (plan for epic, tasks for feature/task)
            # with the CRITICAL findings as structured feedback.
            # Use an explicit conditional rather than indirect invocation via a variable so
            # that the dispatch is readable and the per-command env assignment is unambiguous.
            export SPECKIT_CRITICAL_GATE_FEEDBACK="$feedback"
            local _layer1_phase_ok=true
            if [[ "$hierarchy_level" == "epic" ]]; then
                COPILOT_TIMEOUT=900 run_plan_phase || _layer1_phase_ok=false
            else
                COPILOT_TIMEOUT=900 run_tasks_phase || _layer1_phase_ok=false
            fi
            if [[ "$_layer1_phase_ok" == "false" ]]; then
                echo "[CRITICAL Gate] Layer 1: Warning: ${_primary_artifact_label^} phase failed in attempt $attempt" >&2
                unset SPECKIT_CRITICAL_GATE_FEEDBACK
                continue
            fi
            unset SPECKIT_CRITICAL_GATE_FEEDBACK

            # Refresh derived coverage (fr-coverage.json, test-coverage.json) so that the
            # subsequent artifact verification and analyze phase see data consistent with the
            # regenerated tasks.md rather than the pre-remediation state.
            local _refresh_rc=0
            _refresh_derived_coverage "$hierarchy_level" || _refresh_rc=$?
            if [[ "$_refresh_rc" -ne 0 ]]; then
                echo "[CRITICAL Gate] Layer 1: FR coverage refresh failed in attempt $attempt (rc=$_refresh_rc) — retrying" >&2
                continue
            fi

            # Re-run the artifact verification gate on the regenerated artifact.
            # The original step-3/step-4 gate passed before remediation; a regenerated
            # artifact can introduce missing-path, FR-reference, or unmapped-test violations
            # that would otherwise escape into an already-passing artifact_gate_result.
            local _l1_gate_rc=0
            _rerun_artifact_gate_check "Layer 1" "$_artifact_phase_num" "$_primary_artifact_label" || _l1_gate_rc=$?
            if [[ "$_l1_gate_rc" -eq 1 ]]; then
                echo "[CRITICAL Gate] Layer 1: Artifact gate violations in attempt $attempt — retrying" >&2
                continue
            fi

            # Re-run analyze phase
            if ! COPILOT_TIMEOUT=900 run_analyze_phase; then
                echo "[CRITICAL Gate] Layer 1: Warning: Analyze phase failed in attempt $attempt" >&2
                continue
            fi

            # Re-check gate
            local gate_rc=0
            check_analysis_gate "$(resolve_generated_artifact "$spec_dir" "analysis-report.md")" "block" false || gate_rc=$?

            if [[ "$gate_rc" -eq 0 ]]; then
                echo "[CRITICAL Gate] Layer 1: ✓ All CRITICALs resolved after attempt $attempt" >&2
                critical_gate_remediation_layer="layer1"
                SPEC_DIR="$_saved_spec_dir"
                return 0
            elif [[ "$gate_rc" -eq 20 ]]; then
                echo "[CRITICAL Gate] Layer 1: Warning: Report malformed after attempt $attempt" >&2
                continue
            fi
            # gate_rc=10: CRITICALs remain, update findings for next iteration
            findings_json_input="$critical_findings_json"
            echo "[CRITICAL Gate] Layer 1: CRITICALs remain after attempt $attempt" >&2
        done

        echo "[CRITICAL Gate] Layer 1: Exhausted ($max_retries attempts)" >&2
    else
        echo "[CRITICAL Gate] Layer 1: Skipped (SPECKIT_CRITICAL_GATE_MAX_RETRIES=0)" >&2
    fi

    # ── Layer 2: Alternate LLM remediation ──────────────────────────────
    local layer2_max=2
    echo "[CRITICAL Gate] Layer 2: Alternate LLM remediation (max $layer2_max attempts)" >&2

    for (( attempt=1; attempt<=layer2_max; attempt++ )); do
        echo "[CRITICAL Gate] Layer 2: Attempt $attempt/$layer2_max" >&2

        # Read current artifacts (guard against missing files)
        local primary_content spec_content
        if [[ ! -r "$spec_dir/$_primary_artifact_file" || ! -r "$spec_dir/spec.md" ]]; then
            echo "[CRITICAL Gate] Layer 2: Warning: Required artifact missing or unreadable ($_primary_artifact_file or spec.md) in attempt $attempt" >&2
            SPEC_DIR="$_saved_spec_dir"
            return 1
        fi
        primary_content=$(strip_model_footer "$(cat "$spec_dir/$_primary_artifact_file")") || {
            echo "[CRITICAL Gate] Layer 2: Warning: Failed to read $_primary_artifact_file in attempt $attempt" >&2
            SPEC_DIR="$_saved_spec_dir"
            return 1
        }
        spec_content=$(strip_model_footer "$(cat "$spec_dir/spec.md")") || {
            echo "[CRITICAL Gate] Layer 2: Warning: Failed to read spec.md in attempt $attempt" >&2
            SPEC_DIR="$_saved_spec_dir"
            return 1
        }

        # Build alternate prompt with self-validation instructions
        local alt_prompt="You are a ${_primary_artifact_label}-list specialist performing self-validation and correction.

## Current ${_primary_artifact_label}.md
$primary_content

## Feature Specification (spec.md)
$spec_content

## Unresolved CRITICAL Findings
$(python3 -c "
import json, sys
findings = json.loads(sys.argv[1])
for f in findings:
    print(f\"- [{f['id']}] {f['summary']}: {f['recommendation']}\")
" "$findings_json_input" 2>/dev/null || echo "$findings_json_input")

## Instructions
1. You MUST verify that EVERY functional requirement (FR-XXX) in spec.md has at least one corresponding entry in ${_primary_artifact_label}.md.
2. You MUST address each CRITICAL finding listed above by adding, modifying, or reorganizing entries.
3. Output the COMPLETE corrected ${_primary_artifact_label}.md content.
4. Do NOT remove existing valid content — only add missing entries or fix incorrect ones.
5. Maintain the exact same format: phases, IDs, labels, dependencies.
6. Start your response with the markdown heading (e.g., '# ${_primary_artifact_label^}: ...').

CRITICAL: Your output MUST begin with a markdown heading on the very first line.
Do NOT include any conversational preamble before the heading."

        local result=""
        if ! result=$(call_llm "$alt_prompt"); then
            echo "[CRITICAL Gate] Layer 2: Warning: LLM call failed in attempt $attempt" >&2
            continue
        fi

        if [[ -z "$result" ]]; then
            echo "[CRITICAL Gate] Layer 2: Warning: LLM returned empty response in attempt $attempt" >&2
            continue
        fi

        # Write result to the primary artifact file (tasks.md for feature/task, plan.md for epic)
        result=$(strip_llm_preamble "$result" "# ")
        if [[ -z "${result//[[:space:]]/}" ]]; then
            echo "[CRITICAL Gate] Layer 2: Warning: LLM returned blank content after sanitization" >&2
            continue
        fi
        result=$(ensure_heading_start "$result" "# ${_primary_artifact_label^} List")
        printf '%s\n' "$result" > "$spec_dir/$_primary_artifact_file"
        append_model_footer "$spec_dir/$_primary_artifact_file"

        # Refresh derived coverage (fr-coverage.json, test-coverage.json) so that the
        # subsequent artifact verification and analyze phase see data consistent with the
        # directly patched tasks.md rather than the pre-remediation state.
        local _l2_refresh_rc=0
        _refresh_derived_coverage "$hierarchy_level" || _l2_refresh_rc=$?
        if [[ "$_l2_refresh_rc" -ne 0 ]]; then
            echo "[CRITICAL Gate] Layer 2: FR coverage refresh failed in attempt $attempt (rc=$_l2_refresh_rc) — retrying" >&2
            continue
        fi

        # Re-run the artifact verification gate on the directly patched artifact.
        # Same rationale as Layer 1: the patch can introduce structural violations that
        # must be published before analysis runs so artifact_gate_result stays accurate.
        local _l2_gate_rc=0
        _rerun_artifact_gate_check "Layer 2" "$_artifact_phase_num" "$_primary_artifact_label" || _l2_gate_rc=$?
        if [[ "$_l2_gate_rc" -eq 1 ]]; then
            echo "[CRITICAL Gate] Layer 2: Artifact gate violations in attempt $attempt — retrying" >&2
            continue
        fi

        # Re-run analyze phase
        if ! COPILOT_TIMEOUT=900 run_analyze_phase; then
            echo "[CRITICAL Gate] Layer 2: Warning: Analyze phase failed in attempt $attempt" >&2
            continue
        fi

        # Re-check gate
        local gate_rc=0
        check_analysis_gate "$(resolve_generated_artifact "$spec_dir" "analysis-report.md")" "block" false || gate_rc=$?

        if [[ "$gate_rc" -eq 0 ]]; then
            echo "[CRITICAL Gate] Layer 2: ✓ All CRITICALs resolved after attempt $attempt" >&2
            critical_gate_remediation_layer="layer2"
            SPEC_DIR="$_saved_spec_dir"
            return 0
        elif [[ "$gate_rc" -eq 20 ]]; then
            echo "[CRITICAL Gate] Layer 2: Warning: Report malformed after attempt $attempt" >&2
            continue
        fi
        # Update findings for next iteration
        findings_json_input="$critical_findings_json"
        echo "[CRITICAL Gate] Layer 2: CRITICALs remain after attempt $attempt" >&2
    done

    echo "[CRITICAL Gate] Layer 2: Exhausted ($layer2_max attempts)" >&2
    echo "[CRITICAL Gate] ✗ Remediation failed — all layers exhausted" >&2
    SPEC_DIR="$_saved_spec_dir"
    return 1
}
