#!/usr/bin/env bash
# scripts/vendor_diff.sh — show what scripts/sync_vendor.sh would change
# without actually writing anything. Safe to run any time.
#
# Usage:
#   ./scripts/vendor_diff.sh                 # human-readable summary
#   ./scripts/vendor_diff.sh --full          # per-file list
#   ./scripts/vendor_diff.sh --files-only    # paths only (for piping)

set -euo pipefail

# Resolve repo root from this script's location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REF_DIR="$REPO_ROOT/_hermes_agent_ref"
VENDOR_DIR="$REPO_ROOT/cvc/agent/_vendor/hermes"

if [[ ! -d "$REF_DIR" ]]; then
    echo "ERROR: reference repo not found at $REF_DIR" >&2
    echo "       clone hermes-agent there before running this." >&2
    exit 1
fi
if [[ ! -d "$VENDOR_DIR" ]]; then
    echo "ERROR: vendor dir not found at $VENDOR_DIR" >&2
    exit 1
fi

# Same source set the sync script uses — keep in sync with sync_vendor.sh
SUBDIRS=(agent tools hermes_cli gateway providers cron plugins skills optional-skills)
TOPLEVEL=(batch_runner.py hermes_constants.py toolset_distributions.py
          hermes_bootstrap.py run_agent.py toolsets.py hermes_logging.py
          mini_swe_runner.py hermes_time.py setup.py utils.py
          trajectory_compressor.py hermes_state.py model_tools.py mcp_serve.py)

mode="${1:-summary}"
added=0
modified=0
deleted=0
unchanged=0

declare -a report_added
declare -a report_modified
declare -a report_deleted

# Subdirectories
for d in "${SUBDIRS[@]}"; do
    src="$REF_DIR/$d"
    dst="$VENDOR_DIR/$d"
    [[ -d "$src" ]] || continue

    while IFS= read -r src_file; do
        rel="${src_file#$src/}"
        dst_file="$dst/$rel"
        if [[ ! -f "$dst_file" ]]; then
            added=$((added+1))
            report_added+=("$d/$rel  (new in ref)")
        elif ! diff -q "$src_file" "$dst_file" >/dev/null 2>&1; then
            modified=$((modified+1))
            report_modified+=("$d/$rel")
        else
            unchanged=$((unchanged+1))
        fi
    done < <(find "$src" -type f \( -name "*.py" -o -name "*.yaml" -o -name "*.json" -o -name "*.md" \) ! -path "*/__pycache__/*")

    # Files in vendor but not in ref (will be deleted by sync)
    if [[ -d "$dst" ]]; then
        while IFS= read -r dst_file; do
            rel="${dst_file#$dst/}"
            src_file="$src/$rel"
            if [[ ! -f "$src_file" ]]; then
                # NO_DELETE check: skip files under paths we protect
                # from sync-driven deletion (refactor migrations, CVC extras).
                skip=0
                case "$rel" in
                    platforms/*|browser_providers*|red-teaming/godmode/scripts/*)
                        skip=1 ;;
                esac
                if [[ $skip -eq 0 ]]; then
                    deleted=$((deleted+1))
                    report_deleted+=("$d/$rel")
                fi
            fi
        done < <(find "$dst" -type f \( -name "*.py" -o -name "*.yaml" -o -name "*.json" -o -name "*.md" \) ! -path "*/__pycache__/*")
    fi
done

# Top-level files
for f in "${TOPLEVEL[@]}"; do
    src="$REF_DIR/$f"
    dst="$VENDOR_DIR/$f"
    [[ -f "$src" ]] || continue
    if [[ ! -f "$dst" ]]; then
        added=$((added+1))
        report_added+=("$f  (new in ref)")
    elif ! diff -q "$src" "$dst" >/dev/null 2>&1; then
        modified=$((modified+1))
        report_modified+=("$f")
    else
        unchanged=$((unchanged+1))
    fi
done

# Skip files we deliberately preserve (CVC overrides + extras)
is_cvc_override() {
    case "$1" in
        # CVC registers its own platform
        hermes_cli/platforms.py) return 0 ;;
        # CVC injects bundled skills tree
        agent/skill_utils.py) return 0 ;;
        # CVC extras — only in vendor
        tools/browser_providers/*) return 0 ;;
        skills/creative/DESCRIPTION.md) return 0 ;;
        *) return 1 ;;
    esac
}

if [[ "$mode" == "--files-only" ]]; then
    printf '%s\n' "${report_added[@]}"
    printf '%s\n' "${report_modified[@]}"
    printf '%s\n' "${report_deleted[@]}"
    exit 0
fi

echo "═══════════════════════════════════════════════════════════════"
echo "  Vendor sync diff — _hermes_agent_ref → cvc/agent/_vendor/hermes"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "  Added in ref (vendor missing):   $added"
echo "  Modified (drift):                $modified"
echo "  Deleted (only in vendor):        $deleted"
echo "  Unchanged:                       $unchanged"
echo ""

if [[ "$mode" == "--full" ]]; then
    if [[ ${#report_added[@]} -gt 0 ]]; then
        echo "─── Added (${#report_added[@]}) ───"
        printf '  + %s\n' "${report_added[@]}"
    fi
    if [[ ${#report_modified[@]} -gt 0 ]]; then
        echo "─── Modified (${#report_modified[@]}) ───"
        printf '  ~ %s\n' "${report_modified[@]}"
    fi
    if [[ ${#report_deleted[@]} -gt 0 ]]; then
        echo "─── Deleted (${#report_deleted[@]}) ───"
        printf '  - %s\n' "${report_deleted[@]}"
    fi
fi

echo ""
echo "Files preserved by sync (CVC overrides — re-applied automatically):"
echo "  hermes_cli/platforms.py    (registers cvc-dashboard platform)"
echo "  agent/skill_utils.py       (bundled skills tree injection)"
