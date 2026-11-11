#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0

# tag-release.sh: start the lockstep SDK release for a stable core pin.
#
# Usage: tag-release.sh [--dry-run] [--force] [--sha <commit>] [--since <commit>]
#
# Reads the pin, OPENSHELL_CORE_REF in mise.toml, at <commit> (default:
# $GITHUB_SHA, else HEAD). A pre-release pin creates nothing. Without --force,
# nothing is created either when the pin at <commit> equals the pin at --since
# (default: the parent of <commit>) or there is no pin there, so ordinary
# pushes to main and the push that adds mise.toml are no-ops.
# The release workflow passes the commit before the push as --since, which
# covers pushes of several commits. Then, each step only when missing:
#   - tag vX.Y.Z (lightweight) at <commit>; a tag at another commit fails
#   - a draft GitHub release with the merged PR's body plus
#     "Matches OpenShell core vX.Y.Z"
# Prints "tag=vX.Y.Z" when the release still has to be built and published,
# and nothing when there is nothing to release or the release is published
# already. The workflow appends the output to $GITHUB_OUTPUT.
set -euo pipefail

sdk_repo=${SDK_REPO:-ai-openshell/sdk-python}
dry=0
force=0
sha=${GITHUB_SHA:-}
since=

usage() { echo "usage: $0 [--dry-run] [--force] [--sha <commit>] [--since <commit>]" >&2; exit 2; }
while [ $# -gt 0 ]; do
  case $1 in
  --dry-run) dry=1; shift ;;
  --force) force=1; shift ;;
  --sha) sha=${2:?--sha needs a commit}; shift 2 ;;
  --since) since=${2:?--since needs a commit}; shift 2 ;;
  *) usage ;;
  esac
done
[ -n "$sha" ] || sha=$(git rev-parse HEAD)
sha=$(git rev-parse "$sha^{commit}")
short=$(git rev-parse --short "$sha")

pin_at() { git show "$1:mise.toml" 2>/dev/null | sed -n 's/^OPENSHELL_CORE_REF = "\(.*\)"$/\1/p'; }

pin=$(pin_at "$sha")
if ! [[ "$pin" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "Pin $pin is not a stable release; no SDK release." >&2
  exit 0
fi

if [ "$force" -eq 0 ]; then
  # A new branch push reports an all-zero "before"; fall back to the parent.
  if [ -z "$since" ] || ! git rev-parse --verify --quiet "$since^{commit}" >/dev/null; then
    since="$sha^"
  fi
  old=$(pin_at "$since" || true)
  if [ "$old" = "$pin" ]; then
    echo "The pin is $pin both at $short and at $(git rev-parse --short "$since"); no SDK release." >&2
    exit 0
  fi
  # No pin before means the push added mise.toml (the import), not a bump.
  if [ -z "$old" ]; then
    echo "No pin at $(git rev-parse --short "$since"); no SDK release." >&2
    exit 0
  fi
fi

# get_or_empty <api path> <jq>: the value, empty on 404, and fail on any other
# error. gh prints the error body on stdout for a 404, so stdout is only used
# after a successful call.
get_or_empty() {
  local out err
  if out=$(gh api "$1" --jq "$2" 2>"${tmp}/err"); then
    printf '%s' "$out"
  else
    err=$(cat "${tmp}/err")
    grep -q 'HTTP 404' <<<"$err" || { echo "ERROR: gh api $1 failed: $err" >&2; return 1; }
  fi
}
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

existing=$(get_or_empty "repos/$sdk_repo/git/ref/tags/$pin" '.object.sha')
if [ -n "$existing" ] && [ "$existing" != "$sha" ]; then
  echo "ERROR: tag $pin exists at $existing, not at $sha. SDK tags never move; fix this by hand." >&2
  exit 1
fi
# The tag lookup doesn't return drafts, so search the release list.
release=$(gh api --paginate "repos/$sdk_repo/releases" \
  --jq ".[] | select(.tag_name == \"$pin\") | if .draft then \"draft\" else \"published\" end" | head -1)
if [ "$release" = published ]; then
  echo "Release $pin is published already; nothing to do." >&2
  exit 0
fi

# Release notes: the body of the PR that merged this commit, then the match line.
notes="$tmp/notes.md"
pr_body=$(get_or_empty "repos/$sdk_repo/commits/$sha/pulls" '.[0].body // empty')
{
  [ -z "$pr_body" ] || printf '%s\n\n' "$pr_body"
  echo "Matches OpenShell core $pin."
} >"$notes"

if [ "$dry" -eq 1 ]; then
  if [ -n "$existing" ]; then
    echo "dry-run: tag $pin exists at $sha" >&2
  else
    echo "dry-run: would create tag $pin at $sha" >&2
  fi
  if [ "$release" = draft ]; then
    echo "dry-run: draft release $pin exists" >&2
  else
    echo "dry-run: would create draft release $pin with notes:" >&2
    sed 's/^/  | /' "$notes" >&2
  fi
  echo "tag=$pin"
  exit 0
fi

if [ -z "$existing" ]; then
  gh api -X POST "repos/$sdk_repo/git/refs" -f ref="refs/tags/$pin" -f sha="$sha" --silent
  echo "Created tag $pin at $sha." >&2
fi
if [ -z "$release" ]; then
  gh release create "$pin" -R "$sdk_repo" --draft --verify-tag --title "$pin" --notes-file "$notes" >&2
fi
echo "tag=$pin"
