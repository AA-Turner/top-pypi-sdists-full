#!/usr/bin/env bash
# Convenience wrapper — delegates to the monorepo publish script.
# Usage: ./scripts/release.sh [--patch|--minor|--major] [--message "..."] [--dry-run]
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$SCRIPT_DIR/../../../scripts/publish-package.sh" matrx-scraper "$@"
