#!/usr/bin/env bash
# Publish a single workspace package to npm, skipping it (rather than failing)
# if this exact version is already on the registry. Reads $TAG and $PUBLISH
# ("true" for a real publish, anything else for a dry run).
set -euo pipefail

pkg="$1"
cd "$pkg"

name=$(pnpm pkg get name | tr -d '"')
version=$(pnpm pkg get version | tr -d '"')

# `pnpm view <name>@<version> version` prints the version when it is already
# published and nothing otherwise, so a non-empty result is an unambiguous
# "already exists". This runs in dry-run mode too: an authenticated
# `pnpm publish --dry-run` still hits the registry's "cannot publish over the
# previously published versions" error, so we have to skip before reaching it.
if [ -n "$(pnpm view "$name@$version" version 2>/dev/null)" ]; then
  echo "::warning title=Skipped $name::$name@$version is already published, skipping"
  exit 0
fi

args=(--access public --tag "${TAG:-latest}" --no-git-checks)
[ "${PUBLISH:-false}" = "true" ] || args+=(--dry-run)

pnpm publish "${args[@]}"
