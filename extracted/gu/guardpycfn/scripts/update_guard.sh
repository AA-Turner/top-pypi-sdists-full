#!/usr/bin/env bash
set -euo pipefail

TAG="${1:-}"
if [[ -z "$TAG" ]]; then
  echo "Usage: $0 <guard-tag>"
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENDOR_DIR="$ROOT_DIR/vendor"

rm -rf "$VENDOR_DIR/cloudformation-guard" || true
git clone --depth 1 --branch "$TAG" https://github.com/aws-cloudformation/cloudformation-guard "$VENDOR_DIR/cloudformation-guard"
echo "$TAG" > "$VENDOR_DIR/UPSTREAM_GUARD_VERSION"
echo "Updated Guard to $TAG"


