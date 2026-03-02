#!/bin/bash
set -e
export PATH="$HOME/.local/bin:$PATH"
cd "$(dirname "$0")/.."

# DEV_FLAG is set by CI (empty for release, --dev for dev branches)
../.github/bump_version.sh VERSION $DEV_FLAG --mode VERSION

git add VERSION
