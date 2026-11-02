#!/usr/bin/env bash
#
# Wrapper for the speckit nest command.
#
# Migrates flat specs/{number}-{slug}/ directories into the nested
# specs/{epic}/{feature}/{task}/ hierarchy. Defaults to a plan-only preview;
# pass --execute to perform the migration.

set -e

usage() {
    echo "Usage: $0 [--dry-run] [--execute] [--scope N | --issue N] [--owner OWNER] [--repo REPO] [--specs-root PATH]"
    echo "  --dry-run          Compute and display the plan without writing anything"
    echo "  --execute          Perform the migration and create a single commit"
    echo "  --scope N          Limit migration to issue N and its descendants"
    echo "  --issue N          Alias for --scope N"
    echo "  --owner OWNER      GitHub owner (auto-detected from the git remote)"
    echo "  --repo REPO        GitHub repository (auto-detected from the git remote)"
    echo "  --specs-root PATH  Path to the specs directory (defaults to ./specs)"
    echo "  --help             Show this help message"
}

for arg in "$@"; do
    case "$arg" in
        --help|-h)
            usage
            exit 0
            ;;
    esac
done

if ! command -v agdt-speckit-nest >/dev/null 2>&1; then
    echo "Error: agdt-speckit-nest is not installed. Install agentic-devtools first." >&2
    exit 1
fi

exec agdt-speckit-nest "$@"
