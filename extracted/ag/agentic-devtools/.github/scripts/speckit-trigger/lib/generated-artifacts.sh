#!/usr/bin/env bash
#
# generated-artifacts.sh - Path helpers for machine-generated spec diagnostics
#
# This is a **library** script — it defines functions/constants only and has no
# top-level side effects.  It is sourced by generate-spec-from-issue.sh,
# check-idempotency.sh and their test harnesses.
#
# The SpecKit pipeline writes three machine-generated diagnostics into every
# spec directory: `fr-coverage.json`, `test-coverage.json` and
# `analysis-report.md`.  They are analyser output, not authored planning prose,
# yet they were previously committed alongside `spec.md`/`plan.md`/`tasks.md`
# and therefore entered the pull-request review surface as reviewable content.
#
# They are now written under `<spec_dir>/generated/`, which matches the
# `**/generated/**/*` pattern on GitHub's published Copilot code review
# exclusion list, so the diagnostics still run, still gate the phase and are
# still committed (preserving the audit trail) without being reviewed as
# content.
#
# See: https://docs.github.com/en/copilot/reference/review-excluded-files
#
# Spec directories generated before this change keep the diagnostics at the
# spec-directory root; `resolve_generated_artifact` falls back to that legacy
# location so existing directories continue to work unchanged.

# Sourcing guard — safe to source multiple times
if [[ -n "${_GENERATED_ARTIFACTS_LIB_LOADED:-}" ]]; then
    return 0 2>/dev/null || true
fi
_GENERATED_ARTIFACTS_LIB_LOADED=1

# Subdirectory of a spec directory that holds machine-generated diagnostics.
GENERATED_ARTIFACT_SUBDIR="generated"

# ---------------------------------------------------------------------------
# generated_artifact_path <spec_dir> <filename>
#
# Prints the path a newly generated diagnostic must be written to.  The caller
# is responsible for creating the directory (see ensure_generated_dir).
# ---------------------------------------------------------------------------
generated_artifact_path() {
    printf '%s/%s/%s\n' "${1%/}" "$GENERATED_ARTIFACT_SUBDIR" "$2"
}

# ---------------------------------------------------------------------------
# ensure_generated_dir <spec_dir>
#
# Creates the generated-diagnostics directory for a spec directory.
# ---------------------------------------------------------------------------
ensure_generated_dir() {
    mkdir -p "${1%/}/$GENERATED_ARTIFACT_SUBDIR"
}

# ---------------------------------------------------------------------------
# resolve_generated_artifact <spec_dir> <filename>
#
# Prints the path of an existing diagnostic, preferring the current
# `generated/` location and falling back to the legacy spec-directory root used
# by spec directories created before the relocation.  When the file exists in
# neither place, the current (`generated/`) path is printed so that callers can
# report a stable, forward-looking path in their error messages.
# ---------------------------------------------------------------------------
resolve_generated_artifact() {
    local spec_dir="${1%/}"
    local filename="$2"
    local current="$spec_dir/$GENERATED_ARTIFACT_SUBDIR/$filename"
    local legacy="$spec_dir/$filename"

    if [[ -f "$current" ]]; then
        printf '%s\n' "$current"
    elif [[ -f "$legacy" ]]; then
        printf '%s\n' "$legacy"
    else
        printf '%s\n' "$current"
    fi
}

# ---------------------------------------------------------------------------
# migrate_legacy_generated_artifacts <spec_dir> <filename...>
#
# Moves diagnostics left at the legacy spec-directory root by an earlier
# pipeline run into `generated/`, so a spec directory that is picked up again
# by a later phase keeps working and stops publishing the diagnostic as
# reviewable content.  Files already present at the current location win; the
# stale legacy copy is discarded.
# ---------------------------------------------------------------------------
migrate_legacy_generated_artifacts() {
    local spec_dir="${1%/}"
    shift
    ensure_generated_dir "$spec_dir"

    local filename legacy current
    for filename in "$@"; do
        legacy="$spec_dir/$filename"
        current="$spec_dir/$GENERATED_ARTIFACT_SUBDIR/$filename"
        [[ -f "$legacy" ]] || continue
        if [[ -f "$current" ]]; then
            rm -f "$legacy"
        else
            mv "$legacy" "$current"
        fi
        echo "Relocated generated diagnostic to $current" >&2
    done
}
