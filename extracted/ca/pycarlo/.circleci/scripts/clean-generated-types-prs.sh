#!/bin/bash
set -euo pipefail

# Colors for output
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;36m'  # Light cyan/blue
NC='\033[0m' # No Color

# Print functions
info() {
    echo -e "${BLUE}$1${NC}" >&2
}

success() {
    echo -e "${GREEN}$1${NC}" >&2
}

warn() {
    echo -e "${YELLOW}[WARNING]${NC} $1" >&2
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

# Function to trigger type generation workflow for a given monolith PR
rerun_generation() {
    local monolith_pr=$1
    info "Triggering type generation workflow for monolith PR #$monolith_pr..."

    # Get the branch name for the monolith PR
    local monolith_branch
    monolith_branch=$(gh pr view "$monolith_pr" --repo monte-carlo-data/monolith-django --json headRefName --jq '.headRefName' 2>/dev/null)

    if [ -z "$monolith_branch" ]; then
        error "Failed to get branch name for monolith PR #$monolith_pr"
        return 1
    fi

    info "Found monolith branch: $monolith_branch"

    # Get the latest workflow run for this branch
    local run_id
    run_id=$(gh run list --repo monte-carlo-data/monolith-django \
        --workflow handle-pycarlo-schema-changes.yml \
        --branch "$monolith_branch" \
        --limit 1 \
        --json databaseId \
        --jq '.[0].databaseId' 2>/dev/null)

    if [ -z "$run_id" ]; then
        error "No workflow runs found for monolith PR #$monolith_pr (branch: $monolith_branch)"
        return 1
    fi

    info "Found workflow run ID: $run_id"

    # Rerun the workflow
    if gh run rerun "$run_id" --repo monte-carlo-data/monolith-django; then
        success "Successfully triggered workflow rerun for monolith PR #$monolith_pr"
        return 0
    else
        error "Failed to rerun workflow for monolith PR #$monolith_pr"
        return 1
    fi
}

info "Checking for existing PRs with same changes as main..."

# Check for clean working directory
if ! git diff --quiet || ! git diff --cached --quiet; then
  error "Working directory has uncommitted changes. Please commit or stash them before running this script."
  exit 1
fi

# Get all open PRs that match our branch naming pattern
OPEN_PRS=$(gh pr list --base main --search "update-types-from-monolith- in:title is:open" --json number,headRefName,url --jq '.[]')

git fetch -q origin main
for pr in $(echo "${OPEN_PRS}" | jq -c '.'); do
  PR_NUMBER=$(echo "$pr" | jq -r '.number')
  PR_BRANCH=$(echo "$pr" | jq -r '.headRefName')
  PR_URL=$(echo "$pr" | jq -r '.url')
  MONOLITH_PR=$(echo "$PR_BRANCH" | sed -n 's/.*update-types-from-monolith-\([0-9]*\).*/\1/p')

  info "Comparing current branch with PR #$PR_NUMBER (branch: $PR_BRANCH)..."

  # Check if the related monolith PR is closed/merged
  # If so, we will go ahead and close the SDK PR because
  # it's more likely than not no longer needed and any changes
  # should already be in main or will get into main via one of the open ones
  if [ -n "$MONOLITH_PR" ]; then
    info "Checking status of monolith PR #$MONOLITH_PR..."
    MONOLITH_STATUS=$(gh pr view "$MONOLITH_PR" --repo monte-carlo-data/monolith-django --json state --jq '.state' 2>/dev/null || echo "NOT_FOUND")

    if [ "$MONOLITH_STATUS" = "CLOSED" ] || [ "$MONOLITH_STATUS" = "MERGED" ]; then
      warn "Monolith PR #$MONOLITH_PR is $MONOLITH_STATUS. Closing SDK PR #$PR_NUMBER..."
      gh pr close "$PR_NUMBER" --delete-branch --comment "Closing this PR as the related monolith PR #$MONOLITH_PR has been $MONOLITH_STATUS."
      echo
      continue
    elif [ "$MONOLITH_STATUS" = "NOT_FOUND" ]; then
      warn "Could not find monolith PR #$MONOLITH_PR"
    else
      info "Monolith PR #$MONOLITH_PR is still open ($MONOLITH_STATUS)"
    fi
  fi

  # Fetch the PR branch and main
  git fetch -q origin "$PR_BRANCH"

  # Track whether PR should be closed
  is_same_as_main=false

  # Fetch the PR branch
  if ! git fetch -q origin "$PR_BRANCH"; then
    error "Failed to fetch branch $PR_BRANCH for PR #$PR_NUMBER. Skipping..."
    continue
  fi

  # Compare PR branch with main
  if git diff --quiet origin/"$PR_BRANCH" origin/main; then
    info "Existing PR #$PR_NUMBER is same as main: $PR_URL"
    is_same_as_main=true
  else
    # Create a temporary branch from the PR branch
    if ! git checkout -q -b temp_"$PR_BRANCH" origin/"$PR_BRANCH" 2>/dev/null; then
      error "Failed to checkout branch $PR_BRANCH for PR #$PR_NUMBER. Skipping..."
      continue
    fi

    # Attempt to merge latest from main into the temporary branch
    if git merge --quiet origin/main --no-ff -m "Merging latest from main" > /dev/null 2>&1; then
      # Now compare with main
      if git diff --quiet origin/main; then
        info "PR #$PR_NUMBER is now same as main after merging: $PR_URL"
        is_same_as_main=true
      else
        info "PR #$PR_NUMBER still has changes compared to main: $PR_URL"
      fi
    else
      warn "Merge conflict detected for PR #$PR_NUMBER. Closing to allow fresh regeneration..."
      # Clean up: abort the merge
      git merge --abort
      # Switch back to original branch and delete the temporary branch
      git checkout -q -
      git branch -q -D temp_"$PR_BRANCH"
      # Close the PR
      info "API repo PR: https://github.com/monte-carlo-data/monolith-django/pull/$MONOLITH_PR"
      gh pr close "$PR_NUMBER" --delete-branch --comment "Closing this PR due to merge conflicts with main. Types will be regenerated on the next update."

      # Rerun the workflow for the monolith PR
      rerun_generation "$MONOLITH_PR"

      continue
    fi

    # Switch back to original branch and delete the temporary branch
    git checkout -q -
    git branch -q -D temp_"$PR_BRANCH"
  fi

  # Close PR if it's the same as main
  if [ "$is_same_as_main" = true ]; then
    info "API repo PR: https://github.com/monte-carlo-data/monolith-django/pull/$MONOLITH_PR"
    warn "Closing PR #$PR_NUMBER..."
    gh pr close "$PR_NUMBER" --delete-branch --comment "Closing this PR as there are no remaining changes compared to current main."
  fi
  echo
done
