#!/usr/bin/env bash
# Syncs .prs/ against open PRs, then prints a verdict-grouped summary table.
# Pass --no-sync to skip the sync step and only render existing review files.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ "${1:-}" != "--no-sync" ]; then
  bash "$HERE/../review-prs/sync.sh" >&2
fi

python3 "$HERE/summarise.py"
