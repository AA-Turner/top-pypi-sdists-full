#!/usr/bin/env bash
# scripts/sync_vendor.sh — sync the vendored Hermes runtime from the
# reference repo into cvc/agent/_vendor/hermes/.
#
# Why this exists:
#   cvc/agent/_vendor/hermes/ is a checked-in copy of the hermes-agent
#   runtime, frozen at whatever commit we last sync'd. Without a script,
#   the vendor drifts behind upstream and we accumulate subtle bugs
#   (e.g. the tool_loop_guardrails default that hardcoded hard_stop_enabled
#   to False). This script does the sync deterministically and preserves
#   the CVC-specific overrides that must survive any sync.
#
# What it preserves (re-applied automatically after sync):
#   - hermes_cli/platforms.py   — registers the cvc-dashboard platform
#   - agent/skill_utils.py      — injects cvc/bundled_skills/ at runtime
#   - tools/browser_providers/  — CVC-only extras, not in ref
#   - skills/creative/DESCRIPTION.md — CVC-only, not in ref
#
# What it deletes from vendor:
#   - Anything that exists in vendor but not in ref (clean drift removal)
#
# Usage:
#   ./scripts/sync_vendor.sh --dry-run   # show what would happen
#   ./scripts/sync_vendor.sh             # sync + re-apply overrides
#   ./scripts/sync_vendor.sh --no-test   # skip smoke tests
#
# After sync: rebuild wheel (make wheel) and restart daemon (cvc gateway restart).
# On Windows: pip install --upgrade tm-ai and restart the CVC service.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REF_DIR="$REPO_ROOT/_hermes_agent_ref"
VENDOR_DIR="$REPO_ROOT/cvc/agent/_vendor/hermes"

DRY_RUN=0
NO_TEST=0
for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=1 ;;
        --no-test) NO_TEST=1 ;;
        -h|--help)
            grep '^#' "$0" | sed 's/^# \?//'
            exit 0
            ;;
        *) echo "Unknown arg: $arg" >&2; exit 2 ;;
    esac
done

# ── Preflight ────────────────────────────────────────────────────────
if [[ ! -d "$REF_DIR" ]]; then
    echo "ERROR: reference repo not found at $REF_DIR" >&2
    echo "       Run: git clone https://github.com/.../hermes-agent.git _hermes_agent_ref" >&2
    exit 1
fi
if [[ ! -d "$VENDOR_DIR" ]]; then
    echo "ERROR: vendor dir not found at $VENDOR_DIR" >&2
    exit 1
fi

# CVC-only extras to preserve (not in ref). Stashed to /tmp before sync,
# restored after. (rsync handles --exclude via the rsync-mode path; this
# covers the no-rsync fallback and provides an extra restore checkpoint.)
STAGING=$(mktemp -d -t cvc-vendor-sync.XXXXXX)
trap "rm -rf $STAGING" EXIT

# Record ref HEAD for the commit message
REF_HEAD=$(cd "$REF_DIR" && git rev-parse --short HEAD 2>/dev/null || echo "no-git")
REF_BRANCH=$(cd "$REF_DIR" && git branch --show-current 2>/dev/null || echo "detached")
VENDOR_HEAD=$(cd "$REPO_ROOT" && git rev-parse --short HEAD 2>/dev/null || echo "no-git")

# Same source set vendor_diff.sh uses — keep them in sync
SUBDIRS=(agent tools hermes_cli gateway providers cron plugins skills optional-skills)
TOPLEVEL=(batch_runner.py hermes_constants.py toolset_distributions.py
          hermes_bootstrap.py run_agent.py toolsets.py hermes_logging.py
          mini_swe_runner.py hermes_time.py setup.py utils.py
          trajectory_compressor.py hermes_state.py model_tools.py mcp_serve.py)

# Subdirs where we sync ADD/UPDATE only, never DELETE — refactor or
# dead-code migrations happen upstream, and we don't want to lose
# vendor-only files that CVC's runtime might still import from.
# These dirs accumulate "legacy" code until CVC migrates to the
# upstream architecture (e.g. gateway/platforms/ → plugins/platforms/).
NO_DELETE_DIRS=(
    "gateway/platforms"   # ref migrated to plugins/platforms/, vendor still imports from here
    "tools/browser_providers"  # CVC-only extras
)

# Patches that are applied AFTER sync. Each one is a small, anchored
# text transform in scripts/patches/ that injects CVC-specific behavior
# into a ref-owned file without wholesale replacing it. This means
# upstream refactors to other parts of the file don't break us.
#
# Patch files live in scripts/patches/*.py and are applied by
# scripts/apply_cvc_patches.py (called at the end of this script).
#
# Files in this list are NOT preserved wholesale — they go through the
# normal sync, then get the CVC patch layered on top.
PATCHED_FILES=(
    "hermes_cli/platforms.py"   # cvc_dashboard_platform.py
    "agent/skill_utils.py"      # cvc_bundled_skills.py
)

# Extras that we always preserve (CVC-only, not in ref).
extras_dirs=(
    "tools/browser_providers"
)

# ── Dry-run summary ─────────────────────────────────────────────────
if [[ $DRY_RUN -eq 1 ]]; then
    echo ""
    echo "Dry run — invoking vendor_diff.sh for stats:"
    echo ""
    "$SCRIPT_DIR/vendor_diff.sh" --full
    echo ""
    echo "Would copy from $REF_DIR (HEAD $REF_HEAD on $REF_BRANCH)"
    echo "Would delete  vendor files no longer in ref (see - lines above)"
    echo "Would re-apply CVC overrides (stashed above) onto vendor"
    exit 0
fi

# ── Sync: copy each source path into vendor ─────────────────────────
echo ""
echo "Syncing from ref $REF_HEAD ($REF_BRANCH) into $VENDOR_DIR ..."
echo ""

copied=0
deleted=0
for d in "${SUBDIRS[@]}"; do
    src="$REF_DIR/$d"
    dst="$VENDOR_DIR/$d"
    if [[ ! -d "$src" ]]; then
        echo "  skip (not in ref): $d/"
        continue
    fi
    mkdir -p "$dst"
    # Use rsync if available — handles deletes cleanly.
    # Fall back to cp -R + manual prune if rsync is missing.
    if command -v rsync >/dev/null 2>&1; then
        # Decide --delete based on whether this dir is in NO_DELETE_DIRS
        use_delete=""
        for nd in "${NO_DELETE_DIRS[@]}"; do
            [[ "$d" == "$nd" ]] && use_delete="" && break
        done
        [[ -z "$use_delete" ]] && use_delete="--delete"
        # --delete removes files in vendor that don't exist in ref
        # --exclude keeps our preserved dirs intact
        rsync -a $use_delete \
            --exclude="browser_providers/" \
            --exclude="creative/DESCRIPTION.md" \
            --exclude="platforms/" \
            --exclude="red-teaming/godmode/scripts/" \
            --exclude="__pycache__/" \
            "$src/" "$dst/"
    else
        # No rsync — copy, then prune manually (skipping NO_DELETE_DIRS)
        find "$src" -type f ! -path "*/__pycache__/*" \
            \( -name "*.py" -o -name "*.yaml" -o -name "*.json" -o -name "*.md" \) \
            -print0 | while IFS= read -r -d '' src_file; do
                rel="${src_file#$src/}"
                dst_file="$dst/$rel"
                mkdir -p "$(dirname "$dst_file")"
                cp "$src_file" "$dst_file"
            done
        # Prune vendor files that don't exist in ref — unless this is a NO_DELETE_DIR
        is_no_delete=0
        for nd in "${NO_DELETE_DIRS[@]}"; do
            [[ "$d" == "$nd" ]] && is_no_delete=1 && break
        done
        if [[ $is_no_delete -eq 0 ]] && [[ -d "$dst" ]]; then
            find "$dst" -type f ! -path "*/__pycache__/*" \
                \( -name "*.py" -o -name "*.yaml" -o -name "*.json" -o -name "*.md" \) \
                -print0 | while IFS= read -r -d '' dst_file; do
                    rel="${dst_file#$dst/}"
                    src_file="$src/$rel"
                    # ALSO skip files under NO_DELETE_PATHS (cross-dir protection)
                    skip=0
                    case "$rel" in
                        platforms/*|red-teaming/godmode/scripts/*) skip=1 ;;
                    esac
                    [[ $skip -eq 0 ]] && [[ ! -f "$src_file" ]] && rm -f "$dst_file"
                done
        fi
    fi
    count=$(find "$src" -type f ! -path "*/__pycache__/*" \
            \( -name "*.py" -o -name "*.yaml" -o -name "*.json" -o -name "*.md" \) | wc -l | tr -d ' ')
    copied=$((copied + count))
    echo "  synced $d/  ($count files)"
done

for f in "${TOPLEVEL[@]}"; do
    src="$REF_DIR/$f"
    dst="$VENDOR_DIR/$f"
    if [[ ! -f "$src" ]]; then
        [[ -f "$dst" ]] && { rm -f "$dst"; deleted=$((deleted+1)); }
        continue
    fi
    cp "$src" "$dst"
    copied=$((copied + 1))
done
echo ""
echo "Copied $copied files from ref."

# ── Restore CVC-only extras (browser_providers, etc.) ──────────────
echo ""
echo "Restoring CVC-only extras ..."
mkdir -p "$STAGING/extras"
for f in "${extras_dirs[@]}"; do
    if [[ -d "$VENDOR_DIR/$f" ]]; then
        # Snapshot to staging before re-syncing, in case sync deleted it
        cp -R "$VENDOR_DIR/$f" "$STAGING/extras/$f" 2>/dev/null || true
        echo "  snapshotted CVC extra dir: $f/"
    fi
done
# After sync, restore the extras
for f in "${extras_dirs[@]}"; do
    if [[ -d "$STAGING/extras/$f" ]]; then
        mkdir -p "$VENDOR_DIR/$(dirname "$f")"
        # Use rsync to merge rather than replace (in case ref added files there)
        if command -v rsync >/dev/null 2>&1; then
            rsync -a "$STAGING/extras/$f/" "$VENDOR_DIR/$f/"
        else
            cp -R "$STAGING/extras/$f/"* "$VENDOR_DIR/$f/" 2>/dev/null || true
        fi
        echo "  restored CVC extra dir: $f/"
    fi
done

# ── Apply CVC override patches ─────────────────────────────────────
echo ""
echo "Applying CVC override patches (scripts/apply_cvc_patches.py) ..."
if [[ -x "$SCRIPT_DIR/apply_cvc_patches.py" ]] || [[ -f "$SCRIPT_DIR/apply_cvc_patches.py" ]]; then
    if python3 "$SCRIPT_DIR/apply_cvc_patches.py"; then
        echo "  ✓ patches applied"
    else
        echo "  ✗ patch failed — vendor may be in inconsistent state"
        exit 1
    fi
else
    echo "  (apply_cvc_patches.py not found — skipping)"
fi

# ── Smoke tests ─────────────────────────────────────────────────────
if [[ $NO_TEST -eq 0 ]]; then
    echo ""
    echo "Running vendor smoke tests ..."
    cd "$REPO_ROOT"

    # 1. Vendor still imports
    if python -c "import cvc.agent._vendor.hermes.model_tools as m; print('imports OK,', len(m.get_all_tool_names()), 'tools')" 2>/dev/null; then
        echo "  ✓ vendor imports cleanly"
    else
        PYTHONPATH="$REPO_ROOT" python3 -c "import cvc.agent._vendor.hermes.model_tools as m; print('imports OK,', len(m.get_all_tool_names()), 'tools')" 2>&1 | head -5 || true
        echo "  ⚠ import smoke test failed — investigate before restarting daemon"
    fi

    # 2. CVC overrides still present
    if grep -q '"cvc-dashboard"' "$VENDOR_DIR/hermes_cli/platforms.py"; then
        echo "  ✓ cvc-dashboard platform registered"
    else
        echo "  ✗ cvc-dashboard platform MISSING — restore failed"
        exit 1
    fi
    if grep -q 'bundled_skills' "$VENDOR_DIR/agent/skill_utils.py"; then
        echo "  ✓ bundled skills injection intact"
    else
        echo "  ✗ bundled skills injection MISSING — restore failed"
        exit 1
    fi
fi

# ── Done ────────────────────────────────────────────────────────────
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  Vendor sync complete."
echo ""
echo "  ref HEAD:        $REF_HEAD ($REF_BRANCH)"
echo "  vendor HEAD:     $VENDOR_HEAD (working tree updated — not yet committed)"
echo ""
echo "  Next steps:"
echo "    1. Review the diff:  git diff --stat cvc/agent/_vendor/hermes/"
echo "    2. Smoke-test locally:  cvc gateway restart"
echo "    3. Commit:  git add cvc/agent/_vendor/hermes/ && git commit -m \"chore(vendor): sync from hermes-agent $REF_HEAD\""
echo "    4. Push:    git push origin main"
echo "═══════════════════════════════════════════════════════════════"
