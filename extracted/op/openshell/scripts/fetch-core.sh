#!/usr/bin/env bash
# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

# fetch-core.sh: copy files from NVIDIA/OpenShell at a pinned ref.
#
# The protos come from `buf export` (mise run proto:fetch); this script fetches
# the other core files the repository checks against, such as the vendored
# conformance fixtures.
#
# Usage: fetch-core.sh <ref> <out-dir> <core-path>...
#
# Fetches only <ref> (a tag or a full commit SHA), without history or unneeded
# blobs, and copies each <core-path> (a file or directory) into <out-dir>
# under the same relative path, replacing what was there.
set -euo pipefail

if [ $# -lt 3 ]; then
  echo "usage: $0 <ref> <out-dir> <core-path>..." >&2
  exit 2
fi

ref=$1
out=$2
shift 2
remote=${OPENSHELL_CORE_REMOTE:-https://github.com/NVIDIA/OpenShell.git}
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

git -C "$work" init --quiet
git -C "$work" remote add origin "$remote"
git -C "$work" fetch --quiet --depth 1 --filter=blob:none --no-tags origin "$ref"
git -C "$work" sparse-checkout set --no-cone "$@"
git -C "$work" checkout --quiet FETCH_HEAD

for path in "$@"; do
  rm -rf "${out:?}/$path"
  mkdir -p "$out/$(dirname "$path")"
  cp -R "$work/$path" "$out/$path"
done
