#!/usr/bin/env bash

VERSION=${1:+@${1}}

TMP=/tmp
PKG_DATA=$(
  npm pack --json --pack-destination "${TMP}" --ignore-scripts \
    --registry=https://registry.npmjs.org "axe-core${VERSION}"
)

TARFILE=$(jq -r '.[].filename' <<< "${PKG_DATA}")
DISTFILE=$(
  jq -r '.[].files[].path | select(test("axe\\.min\\.js$"))' \
    <<< "${PKG_DATA}"
)
tar -Oxzf "${TMP}/${TARFILE}" "package/${DISTFILE}" > \
  axe_playwright_python/axe.min.js

rm -f "${TMP}/${TARFILE}"
