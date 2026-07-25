#!/usr/bin/env bash

RLS=$(
  curl -sf "https://api.github.com/repos/dequelabs/axe-core/releases?per_page=3"
)

COOLDOWN=$(( 5*24*3600 ))
CANDIDATE=$(
  jq -r '[.[] | select(.published_at | fromdate < now - '"${COOLDOWN}"')] | first' \
   <<< "${RLS}"
)

CUR=$(
  sed -n 's/^\/\*! axe \(v[0-9.]*\)/\1/p;q' \
    axe_playwright_python/axe.min.js
)
CAND=$(jq -r '.tag_name' <<< "${CANDIDATE}")

[[ "${CUR}" == "${CAND}" ]] || echo "${CAND#v}"
