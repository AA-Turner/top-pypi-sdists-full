#!/usr/bin/env bash

set -euo pipefail

ISSUE_NUMBER="${1:-}"
SPEC_DIR="${2:-}"
BRANCH_NAME="${3:-}"

if [[ -z "$ISSUE_NUMBER" ]]; then
    echo "Error: issue number is required" >&2
    exit 1
fi

if [[ -z "$SPEC_DIR" ]]; then
    echo "Error: spec directory is required" >&2
    exit 1
fi

if [[ -z "$BRANCH_NAME" ]]; then
    echo "Error: branch name is required" >&2
    exit 1
fi

git config user.name "github-actions[bot]"
git config user.email "github-actions[bot]@users.noreply.github.com"

if git ls-remote --exit-code --heads origin "$BRANCH_NAME" >/dev/null 2>&1; then
    echo "Branch '$BRANCH_NAME' already exists on remote — fetching and resetting"
    git fetch origin "refs/heads/$BRANCH_NAME:refs/remotes/origin/$BRANCH_NAME"
    git checkout -B "$BRANCH_NAME"
else
    git checkout -b "$BRANCH_NAME"
fi

git add "$SPEC_DIR"
COMMIT_CREATED="false"
if git diff --cached --quiet; then
    echo "No staged changes after migration — nothing to commit."
else
    git commit -m "chore(#${ISSUE_NUMBER}): migrate legacy Phase 3 diagnostics to generated/

Relocates fr-coverage.json, test-coverage.json, and analysis-report.md from the
spec root into the generated/ subdirectory to keep machine-generated diagnostics
out of Copilot Code Review's diff surface.  Phase 3 generation was skipped
(artifacts already present), so migration is applied here instead.

#${ISSUE_NUMBER}"
    COMMIT_CREATED="true"
fi

if [[ -n "${GITHUB_OUTPUT:-}" ]]; then
    echo "branch_name=$BRANCH_NAME" >> "$GITHUB_OUTPUT"
    echo "spec_dir=$SPEC_DIR" >> "$GITHUB_OUTPUT"
    echo "commit_created=$COMMIT_CREATED" >> "$GITHUB_OUTPUT"
fi
