#!/usr/bin/env bash
# Hotfix: Upload all connector icon.svg files to GCS directories.
#
# Background:
#   The legacy metadata_service pipeline stored icon.svg directly in latest/
#   directories but NOT in versioned directories. When Registry 2.0's compile
#   step re-syncs latest/ from versioned directories, icons are lost because
#   the versioned directories don't contain them.
#
#   This script reads icon.svg files from the airbyte repo and uploads them
#   to GCS, restoring the missing icons. It can target either the latest/
#   directory or the latest semver directory (read from metadata.yaml).
#
# Usage:
#   ./scripts/hotfix_publish_icons.sh <path-to-airbyte-repo> [OPTIONS]
#
# Options:
#   --target TARGET   Where to upload: "latest" or "versioned" (default: latest)
#   --dry-run         Print what would be uploaded without uploading
#   --force           Upload icons even if they already exist in GCS
#   --bucket NAME     GCS bucket (default: prod-airbyte-cloud-connector-metadata-service)
#   --connector NAME  Only process a single connector (e.g. source-faker)
#
# Targets:
#   latest     Upload icon.svg to <connector>/latest/icon.svg
#   versioned  Read the dockerImageTag from <connector>/latest/metadata.yaml
#              and upload icon.svg to <connector>/<version>/icon.svg
#   both       Upload to both latest/ and the versioned directory
#
# Examples:
#   ./scripts/hotfix_publish_icons.sh /path/to/airbyte --dry-run
#   ./scripts/hotfix_publish_icons.sh /path/to/airbyte --target versioned --dry-run
#   ./scripts/hotfix_publish_icons.sh /path/to/airbyte --target both
#   ./scripts/hotfix_publish_icons.sh /path/to/airbyte --connector source-hubspot

set -euo pipefail

AIRBYTE_REPO=""
DRY_RUN=false
BUCKET="prod-airbyte-cloud-connector-metadata-service"
CONNECTOR_FILTER=""
TARGET="latest"
FORCE=false

print_usage() {
    echo "Usage: $0 <path-to-airbyte-repo> [--target latest|versioned|both] [--dry-run] [--force] [--bucket NAME] [--connector NAME]" >&2
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run)
            DRY_RUN=true; shift ;;
        --force)
            FORCE=true; shift ;;
        --target)
            if [[ $# -lt 2 || "$2" == -* ]]; then
                echo "ERROR: --target requires a value (latest, versioned, or both)." >&2; print_usage; exit 1
            fi
            TARGET="$2"
            if [[ "$TARGET" != "latest" && "$TARGET" != "versioned" && "$TARGET" != "both" ]]; then
                echo "ERROR: --target must be 'latest', 'versioned', or 'both' (got '$TARGET')." >&2; exit 1
            fi
            shift 2 ;;
        --bucket)
            if [[ $# -lt 2 || "$2" == -* ]]; then
                echo "ERROR: --bucket requires a value." >&2; print_usage; exit 1
            fi
            BUCKET="$2"; shift 2 ;;
        --connector)
            if [[ $# -lt 2 || "$2" == -* ]]; then
                echo "ERROR: --connector requires a value." >&2; print_usage; exit 1
            fi
            CONNECTOR_FILTER="$2"; shift 2 ;;
        -h|--help)       sed -n '2,/^$/p' "$0"; exit 0 ;;
        *)
            if [[ -z "$AIRBYTE_REPO" ]]; then
                AIRBYTE_REPO="$1"
            else
                echo "ERROR: Unknown argument: $1" >&2; exit 1
            fi
            shift ;;
    esac
done

if [[ -z "$AIRBYTE_REPO" ]]; then
    print_usage; exit 1
fi

# Ensure gsutil is available
if ! command -v gsutil >/dev/null 2>&1; then
    echo "ERROR: gsutil is not installed or not in PATH." >&2
    exit 1
fi

CONNECTORS_DIR="$AIRBYTE_REPO/airbyte-integrations/connectors"

if [[ ! -d "$CONNECTORS_DIR" ]]; then
    echo "ERROR: Connectors directory not found: $CONNECTORS_DIR" >&2
    exit 1
fi

# --- Collect icon files ---

ICON_LIST=$(mktemp -t airbyte_icons.XXXXXX)
trap 'rm -f "$ICON_LIST"' EXIT

if [[ -n "$CONNECTOR_FILTER" ]]; then
    icon="$CONNECTORS_DIR/$CONNECTOR_FILTER/icon.svg"
    if [[ -f "$icon" ]]; then
        echo "$icon" > "$ICON_LIST"
    else
        echo "ERROR: No icon.svg found at $icon" >&2; exit 1
    fi
else
    find "$CONNECTORS_DIR" -maxdepth 2 -name "icon.svg" | sort > "$ICON_LIST"
fi

TOTAL=$(wc -l < "$ICON_LIST")

if [[ "$TOTAL" -eq 0 ]]; then
    echo "ERROR: No icon.svg files found in $CONNECTORS_DIR" >&2
    exit 1
fi

START_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
START_EPOCH=$(date +%s)

echo "========================================"
echo "Registry Icons Hotfix"
echo "========================================"
echo "Started:     $START_TIME"
echo "Repo:        $AIRBYTE_REPO"
echo "Bucket:      $BUCKET"
echo "Target:      $TARGET"
echo "Dry run:     $DRY_RUN"
echo "Force:       $FORCE"
echo "Connector:   ${CONNECTOR_FILTER:-all}"
echo "Icons found: $TOTAL"
echo "========================================"

# --- Pre-fetch connectors that have metadata.yaml in GCS (single call) ---
echo "Fetching published connector list from GCS..."
GCS_METADATA_LIST=$(mktemp -t airbyte_gcs_metadata.XXXXXX)
trap 'rm -f "$ICON_LIST" "$GCS_METADATA_LIST"' EXIT

if [[ -n "$CONNECTOR_FILTER" ]]; then
    # Single connector: just check that one
    if gsutil -q stat "gs://$BUCKET/metadata/airbyte/$CONNECTOR_FILTER/latest/metadata.yaml" 2>/dev/null; then
        echo "$CONNECTOR_FILTER" > "$GCS_METADATA_LIST"
    fi
else
    gsutil ls "gs://$BUCKET/metadata/airbyte/*/latest/metadata.yaml" 2>/dev/null \
        | sed 's|.*/metadata/airbyte/||; s|/latest/metadata.yaml||' \
        | sort > "$GCS_METADATA_LIST" || true
fi

GCS_COUNT=$(wc -l < "$GCS_METADATA_LIST")
echo "Found $GCS_COUNT connectors with metadata.yaml in GCS."

# --- Pre-fetch connectors that already have icon.svg in GCS (single call) ---
echo "Fetching existing icon list from GCS..."
GCS_ICON_LIST=$(mktemp -t airbyte_gcs_icons.XXXXXX)
trap 'rm -f "$ICON_LIST" "$GCS_METADATA_LIST" "$GCS_ICON_LIST"' EXIT

if [[ -n "$CONNECTOR_FILTER" ]]; then
    if gsutil -q stat "gs://$BUCKET/metadata/airbyte/$CONNECTOR_FILTER/latest/icon.svg" 2>/dev/null; then
        echo "$CONNECTOR_FILTER" > "$GCS_ICON_LIST"
    fi
else
    gsutil ls "gs://$BUCKET/metadata/airbyte/*/latest/icon.svg" 2>/dev/null \
        | sed 's|.*/metadata/airbyte/||; s|/latest/icon.svg||' \
        | sort > "$GCS_ICON_LIST" || true
fi

GCS_ICON_COUNT=$(wc -l < "$GCS_ICON_LIST")
echo "Found $GCS_ICON_COUNT connectors with existing icon.svg in GCS."

# upload_icon <local_path> <gcs_dest>
upload_icon() {
    local local_path="$1"
    local gcs_dest="$2"

    if [[ "$DRY_RUN" == "true" ]]; then
        return 0
    fi

    if gsutil -h "Content-Type:image/svg+xml" -h "Cache-Control:no-cache" \
        cp "$local_path" "$gcs_dest" 2>&1; then
        return 0
    else
        return 1
    fi
}

uploaded=0
skipped=0
failed=0

while IFS= read -r icon_path; do
    connector_name=$(basename "$(dirname "$icon_path")")
    gcs_base="gs://$BUCKET/metadata/airbyte/$connector_name"
    metadata_blob="$gcs_base/latest/metadata.yaml"

    # Skip connectors that don't have a metadata.yaml in GCS latest/
    if ! grep -qx "$connector_name" "$GCS_METADATA_LIST"; then
        skipped=$((skipped + 1))
        if [[ "$DRY_RUN" == "true" ]]; then
            echo "  [SKIP] $connector_name (no metadata.yaml in GCS)"
        fi
        continue
    fi

    # Skip connectors that already have an icon.svg in GCS (unless --force)
    if [[ "$FORCE" != "true" ]] && grep -qx "$connector_name" "$GCS_ICON_LIST"; then
        skipped=$((skipped + 1))
        if [[ "$DRY_RUN" == "true" ]]; then
            echo "  [SKIP] $connector_name (icon.svg already exists in GCS)"
        fi
        continue
    fi

    # Read the version from metadata.yaml if we need the versioned path
    version=""
    if [[ "$TARGET" == "versioned" || "$TARGET" == "both" ]]; then
        version=$(gsutil cat "$metadata_blob" 2>/dev/null | grep '^\s*dockerImageTag:' | head -1 | sed 's/.*dockerImageTag:\s*//' | tr -d '[:space:]"'"'") || true
        if [[ -z "$version" ]]; then
            echo "  [SKIP] $connector_name (could not read dockerImageTag from metadata.yaml)" >&2
            skipped=$((skipped + 1))
            continue
        fi
    fi

    connector_ok=true

    # Upload to latest/
    if [[ "$TARGET" == "latest" || "$TARGET" == "both" ]]; then
        dest="$gcs_base/latest/icon.svg"
        echo "  Copying to: $dest"
        if [[ "$DRY_RUN" == "true" ]]; then
            echo "  [DRY RUN] skipped"
        elif ! upload_icon "$icon_path" "$dest"; then
            echo "  FAILED: $dest" >&2
            connector_ok=false
        fi
    fi

    # Upload to versioned dir
    if [[ "$TARGET" == "versioned" || "$TARGET" == "both" ]]; then
        dest="$gcs_base/$version/icon.svg"
        echo "  Copying to: $dest"
        if [[ "$DRY_RUN" == "true" ]]; then
            echo "  [DRY RUN] skipped"
        elif ! upload_icon "$icon_path" "$dest"; then
            echo "  FAILED: $dest" >&2
            connector_ok=false
        fi
    fi

    if [[ "$connector_ok" == "true" ]]; then
        uploaded=$((uploaded + 1))
        if [[ "$DRY_RUN" != "true" ]] && (( uploaded % 50 == 0 )); then
            echo "  ... $uploaded/$TOTAL uploaded ..."
        fi
    else
        failed=$((failed + 1))
    fi
done < "$ICON_LIST"

END_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
END_EPOCH=$(date +%s)
ELAPSED=$(( END_EPOCH - START_EPOCH ))

echo ""
echo "========================================"
echo "Done: $uploaded uploaded, $skipped skipped, $failed failed (of $TOTAL total)"
[[ "$DRY_RUN" == "true" ]] && echo "(DRY RUN — nothing was uploaded)"
echo "Started:  $START_TIME"
echo "Finished: $END_TIME"
echo "Elapsed:  ${ELAPSED}s"
echo "========================================"

[[ $failed -gt 0 ]] && exit 1
exit 0
