#!/usr/bin/env bash
# Removes orphaned .prs/*.reply.md drafts whose .md review no longer exists.
set -euo pipefail

PRS_DIR="$(git rev-parse --show-toplevel)/.prs"

for reply in "$PRS_DIR"/*.reply.md; do
  [ -f "$reply" ] || continue
  review="${reply%.reply.md}.md"
  if [ ! -f "$review" ]; then
    rm "$reply"
    echo "Removed $(basename "$reply")"
  fi
done
