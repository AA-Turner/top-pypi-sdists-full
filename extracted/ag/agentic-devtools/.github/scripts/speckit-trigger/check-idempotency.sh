#!/usr/bin/env bash
#
# check-idempotency.sh - Check if specification already exists for an issue
#
# Usage: check-idempotency.sh <issue_number> [--phase <1-3>] [--level <level>]
#
# Arguments:
#   issue_number - The GitHub issue number
#   --phase N    - (optional) Check idempotency for a specific phase:
#                    1: skip if spec.md exists
#                    2: skip if spec.md contains ## Clarifications section
#                       AND checklists/requirements.md exists
#                    3: skip if the terminal artifact of the merged planning
#                       phase exists — generated/analysis-report.md, or
#                       tasks.md when --level task (analyze is not run for
#                       task-level issues)
#                  When omitted, uses the original full-pipeline check.
#   --level L    - (optional) Hierarchy level (epic|feature|task|unknown); defaults
#                  to feature.  Only affects the phase-3 terminal artifact.
#                  'unknown' (fail-closed hierarchy resolution, #3931) is treated
#                  like 'feature' for artifact-detection purposes so generation
#                  is never silently skipped.
#
# Outputs:
#   GITHUB_OUTPUT: skipped=true|false, existing_spec=<path>
#
# Checks (without --phase):
#   1. Search specs/ directory for spec.md files containing "Source Issue: #N"
#   2. Search specs/ directory for spec.md files containing the issue URL
#   3. Checks for spec.md AND at least one full-pipeline artifact
#      (plan.md, tasks.md, analysis-report.md). Legacy spec-only runs
#      do NOT block re-generation with the full pipeline.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source generated-diagnostics path helpers
# shellcheck source=lib/generated-artifacts.sh
source "$SCRIPT_DIR/lib/generated-artifacts.sh"

ISSUE_NUMBER="${1:-}"

if [[ -z "$ISSUE_NUMBER" ]]; then
    echo "Error: Issue number is required" >&2
    exit 1
fi

shift  # consume issue_number

# Parse optional --phase and --level arguments
PHASE=""
HIERARCHY_LEVEL="feature"
while [[ $# -gt 0 ]]; do
    case "$1" in
        --phase)
            PHASE="${2:-}"
            if [[ -z "$PHASE" ]]; then
                echo "Error: --phase requires a value (1-3)" >&2
                exit 1
            fi
            if [[ ! "$PHASE" =~ ^[1-3]$ ]]; then
                echo "Error: --phase must be 1-3 (got '$PHASE')" >&2
                exit 1
            fi
            shift 2
            ;;
        --level)
            HIERARCHY_LEVEL="${2:-}"
            if [[ ! "$HIERARCHY_LEVEL" =~ ^(epic|feature|task|unknown)$ ]]; then
                echo "Error: --level must be one of epic, feature, task, unknown (got '${HIERARCHY_LEVEL}')" >&2
                exit 1
            fi
            if [[ "$HIERARCHY_LEVEL" == "unknown" ]]; then
                # Fail-closed hierarchy resolution (#3931): treat as 'feature' for
                # artifact-detection purposes only, matching generate-spec-from-issue.sh's
                # own fallback. This never affects the speckit:needs-implementation gate,
                # which is applied by the caller based on the ungated 'unknown' level.
                HIERARCHY_LEVEL="feature"
            fi
            shift 2
            ;;
        *)
            echo "Error: Unknown argument '$1'" >&2
            exit 1
            ;;
    esac
done

SPECS_DIR="${SPEC_BASE_PATH:-specs}"

validate_single_line_output_value() {
    local name="$1"
    local value="$2"
    # Fail closed: reject CR/LF outright instead of silently rewriting values.
    if [[ "$value" == *$'\n'* || "$value" == *$'\r'* ]]; then
        echo "Error: refusing to write multi-line value for output '$name'" >&2
        exit 1
    fi
}

write_output_value() {
    local name="$1"
    local value="$2"
    validate_single_line_output_value "$name" "$value"
    printf '%s=%s\n' "$name" "$value" >> "${GITHUB_OUTPUT:-/dev/stdout}"
}

# Check if specs directory exists
if [[ ! -d "$SPECS_DIR" ]]; then
    echo "No specs directory found, proceeding with generation"
    write_output_value "skipped" "false"
    exit 0
fi

# ---------------------------------------------------------------------------
# Per-phase idempotency check (when --phase is provided)
# ---------------------------------------------------------------------------
if [[ -n "$PHASE" ]]; then
    # Find the spec directory for this issue.
    # Collect ALL prefix-based matches and fail if >1, mirroring the safeguard in
    # generate-spec-from-issue.sh to avoid non-deterministic directory selection.
    MATCHING_DIRS=()
    shopt -s nullglob
    for dir in "$SPECS_DIR"/${ISSUE_NUMBER}-*; do
        if [[ -d "$dir" ]]; then
            MATCHING_DIRS+=("$dir")
        fi
    done
    shopt -u nullglob

    if (( ${#MATCHING_DIRS[@]} > 1 )); then
        echo "Error: Found multiple spec directories for issue #$ISSUE_NUMBER:" >&2
        for dir in "${MATCHING_DIRS[@]}"; do
            echo "  - $(basename "$dir")" >&2
        done
        echo "Refusing to choose one directory non-deterministically. Remove or rename the extra directories and retry." >&2
        exit 1
    fi

    SPEC_DIR=""
    if (( ${#MATCHING_DIRS[@]} == 1 )); then
        SPEC_DIR="${MATCHING_DIRS[0]}"
    fi

    # Fallback: grep for "Source Issue.*#N" inside spec.md files (handles legacy naming)
    if [[ -z "$SPEC_DIR" ]]; then
        SEARCH_PATTERN="Source Issue.*#${ISSUE_NUMBER}([^0-9]|$)"
        SPEC_FILE=$(grep -Erl --include='spec.md' "$SEARCH_PATTERN" "$SPECS_DIR" 2>/dev/null | head -1 || echo "")
        if [[ -n "$SPEC_FILE" ]]; then
            SPEC_DIR="$(dirname "$SPEC_FILE")"
        fi
    fi

    # Fallback: nested numeric layout — specs/{epic}/{feature}/{task} directories have
    # no spec.md, so the grep above never finds them.  Search for a directory whose
    # name is exactly the issue number at any depth inside the specs tree.
    if [[ -z "$SPEC_DIR" ]]; then
        mapfile -t NESTED_MATCHING_DIRS < <(find "$SPECS_DIR" -type d -name "${ISSUE_NUMBER}" | sort)
        if (( ${#NESTED_MATCHING_DIRS[@]} > 1 )); then
            echo "Error: Found multiple nested spec directories for issue #$ISSUE_NUMBER:" >&2
            for dir in "${NESTED_MATCHING_DIRS[@]}"; do
                echo "  - $dir" >&2
            done
            echo "Refusing to choose one directory non-deterministically. Remove or rename the extra directories and retry." >&2
            exit 1
        fi
        if (( ${#NESTED_MATCHING_DIRS[@]} == 1 )); then
            SPEC_DIR="${NESTED_MATCHING_DIRS[0]}"
        fi
    fi

    if [[ -z "$SPEC_DIR" ]]; then
        echo "✓ No spec directory found for issue #$ISSUE_NUMBER — proceeding"
        write_output_value "skipped" "false"
        exit 0
    fi
    case "$PHASE" in
        1)
            # Phase 1: skip if spec.md exists (same as original full-pipeline check
            # but without requiring plan/tasks/analysis artifacts)
            if [[ -f "$SPEC_DIR/spec.md" ]]; then
                echo "✗ Phase 1 artifact already exists: $SPEC_DIR/spec.md"
                write_output_value "skipped" "true"
                write_output_value "existing_spec" "$SPEC_DIR/spec.md"
                exit 0
            fi
            ;;
        2)
            # Phase 2: skip only if BOTH clarifications marker AND checklist exist.
            # Checking only the heading would incorrectly skip when a previous run
            # updated spec.md but failed before generating checklists/requirements.md.
            if [[ -f "$SPEC_DIR/spec.md" ]] && grep -q '## Clarifications' "$SPEC_DIR/spec.md" \
               && [[ -f "$SPEC_DIR/checklists/requirements.md" ]]; then
                echo "✗ Phase 2 artifacts already exist: spec.md contains Clarifications section and checklists/requirements.md present"
                write_output_value "skipped" "true"
                write_output_value "existing_spec" "$SPEC_DIR/spec.md"
                exit 0
            fi
            ;;
        3)
            # Phase 3 (plan + tasks + analyze): skip only when the terminal
            # artifact of the merged planning phase already exists.  A partially
            # complete directory (for example plan.md without tasks.md) must
            # re-run so the remaining artifacts are produced.
            if [[ "$HIERARCHY_LEVEL" == "task" ]]; then
                # Task-level issues generate tasks only — analyze never runs.
                TERMINAL_ARTIFACT="$SPEC_DIR/tasks.md"
            else
                TERMINAL_ARTIFACT="$(resolve_generated_artifact "$SPEC_DIR" "analysis-report.md")"
            fi

            if [[ -f "$TERMINAL_ARTIFACT" ]]; then
                if [[ "$HIERARCHY_LEVEL" != "task" ]]; then
                    MISSING_PHASE3_PREREQUISITES=()
                    [[ -f "$SPEC_DIR/spec.md" ]] || MISSING_PHASE3_PREREQUISITES+=("$SPEC_DIR/spec.md")
                    [[ -f "$SPEC_DIR/plan.md" ]] || MISSING_PHASE3_PREREQUISITES+=("$SPEC_DIR/plan.md")
                    if (( ${#MISSING_PHASE3_PREREQUISITES[@]} > 0 )); then
                        echo "Error: Phase 3 artifact ($TERMINAL_ARTIFACT) exists but prerequisite artifacts are missing:" >&2
                        for missing_artifact in "${MISSING_PHASE3_PREREQUISITES[@]}"; do
                            echo "  - Missing: $missing_artifact" >&2
                        done
                        echo "Spec directory is in an inconsistent state. Restore missing artifacts or remove $TERMINAL_ARTIFACT and retry." >&2
                        exit 1
                    fi
                fi

                # For feature-level runs, analysis-report.md is only complete after
                # tasks.md has been produced.  If the report exists but tasks.md is
                # absent the directory is partially complete — skip would mis-label the
                # PR as implementation-ready without the required task breakdown.
                if [[ "$HIERARCHY_LEVEL" == "feature" && ! -f "$SPEC_DIR/tasks.md" ]]; then
                    echo "Error: Phase 3 analysis artifact ($TERMINAL_ARTIFACT) exists but required artifact is missing:" >&2
                    echo "  - Missing: $SPEC_DIR/tasks.md" >&2
                    echo "Spec directory is in an inconsistent state. Restore missing artifacts or remove $TERMINAL_ARTIFACT and retry." >&2
                    exit 1
                fi

                if [[ "$HIERARCHY_LEVEL" == "task" ]]; then
                    write_output_value "migration_done" "false"
                else
                    # If the diagnostics are still at the legacy spec root, migrate
                    # them to generated/ before the idempotency short-circuit.  The
                    # workflow stages any resulting changes in the commit-migration
                    # step, so completed legacy spec directories are relocated on the
                    # very next pipeline run even when generation is skipped.
                    LEGACY_GENERATED_ARTIFACTS=(
                        "$SPEC_DIR/fr-coverage.json"
                        "$SPEC_DIR/test-coverage.json"
                        "$SPEC_DIR/analysis-report.md"
                    )
                    NEEDS_MIGRATION=false
                    for legacy_artifact in "${LEGACY_GENERATED_ARTIFACTS[@]}"; do
                        if [[ -f "$legacy_artifact" ]]; then
                            NEEDS_MIGRATION=true
                            break
                        fi
                    done
                    if [[ "$NEEDS_MIGRATION" == "true" ]]; then
                        migrate_legacy_generated_artifacts "$SPEC_DIR" \
                            "fr-coverage.json" "test-coverage.json" "analysis-report.md"
                        write_output_value "migration_done" "true"
                    else
                        write_output_value "migration_done" "false"
                    fi
                    TERMINAL_ARTIFACT="$(resolve_generated_artifact "$SPEC_DIR" "analysis-report.md")"
                fi

                echo "✗ Phase 3 artifact already exists: $TERMINAL_ARTIFACT"
                write_output_value "skipped" "true"
                write_output_value "existing_spec" "$TERMINAL_ARTIFACT"
                write_output_value "spec_dir" "$SPEC_DIR"
                exit 0
            fi
            ;;
    esac

    echo "✓ Phase $PHASE artifacts not found for issue #$ISSUE_NUMBER — proceeding"
    write_output_value "skipped" "false"
    exit 0
fi

# ---------------------------------------------------------------------------
# Original full-pipeline idempotency check (when --phase is NOT provided)
# ---------------------------------------------------------------------------

# Helper: check whether the full planning pipeline artifacts exist alongside a spec.
# Returns 0 (true) if at least one of plan.md, tasks.md, analysis-report.md is present.
# Returns 1 (false) if none are found (legacy spec-only run).
check_full_pipeline_artifacts() {
    local spec_file="$1"
    local spec_dir
    spec_dir="$(dirname "$spec_file")"

    if [[ -f "$spec_dir/plan.md" ]] || [[ -f "$spec_dir/tasks.md" ]] ||
       [[ -f "$(resolve_generated_artifact "$spec_dir" "analysis-report.md")" ]]; then
        return 0
    fi
    return 1
}

# Search for existing spec with this issue reference.
# The pattern requires the issue number to be followed by a non-digit or end-of-line
# to prevent prefix false-positives (e.g. #12 matching #123).
SEARCH_PATTERN="Source Issue.*#${ISSUE_NUMBER}([^0-9]|$)"
LEGACY_SPEC_FOUND=false

# Restrict search to spec.md files only — other artifacts (e.g. checklists/requirements.md)
# may also contain "Source Issue" and would produce false positives.
# Scan ALL matching spec.md files (not just the first) so a legacy match can't hide
# a full-pipeline match in another directory.
while IFS= read -r spec_match; do
    [[ -z "$spec_match" ]] && continue
    if check_full_pipeline_artifacts "$spec_match"; then
        echo "✗ Found existing specification for issue #$ISSUE_NUMBER: $spec_match"
        write_output_value "skipped" "true"
        write_output_value "existing_spec" "$spec_match"
        exit 0
    else
        echo "⚠ Found spec.md but full pipeline artifacts missing — allowing re-run"
        LEGACY_SPEC_FOUND=true
    fi
done < <(grep -Erl --include='spec.md' "$SEARCH_PATTERN" "$SPECS_DIR" 2>/dev/null || true)

# Also check for issue URL pattern — same all-matches scan as above.
if [[ -n "${GITHUB_REPOSITORY:-}" ]]; then
    URL_PATTERN="github.com/${GITHUB_REPOSITORY}/issues/${ISSUE_NUMBER}([^0-9]|$)"

    while IFS= read -r spec_match; do
        [[ -z "$spec_match" ]] && continue
        if check_full_pipeline_artifacts "$spec_match"; then
            echo "✗ Found existing specification for issue #$ISSUE_NUMBER: $spec_match"
            write_output_value "skipped" "true"
            write_output_value "existing_spec" "$spec_match"
            exit 0
        else
            echo "⚠ Found spec.md but full pipeline artifacts missing — allowing re-run"
            LEGACY_SPEC_FOUND=true
        fi
    done < <(grep -Erl --include='spec.md' "$URL_PATTERN" "$SPECS_DIR" 2>/dev/null || true)
fi

if [[ "$LEGACY_SPEC_FOUND" == "true" ]]; then
    echo "✓ Legacy spec-only directory found for issue #$ISSUE_NUMBER — proceeding with full pipeline generation"
else
    echo "✓ No existing specification found for issue #$ISSUE_NUMBER"
fi
write_output_value "skipped" "false"
