#!/usr/bin/env bash
# fleet-console installer — fetch the latest staged .deb from the hugpy central
# and install it. Served publicly at GET /agent/console/install.sh (no secret
# embedded — same rule as /agent/client.sh); the member/operator credential is
# read from the CALLER's environment at run time:
#
#   curl -fsSL https://dev.hugpy.ai/api/agent/console/install.sh | HUGPY_TOKEN=<token> bash
#
# Env:
#   HUGPY_TOKEN or HUGPY_OPERATOR_TOKEN   credential (required) — sent as a bearer
#   HUGPY_CENTRAL                         API base (default https://dev.hugpy.ai/api)
#
# The download is verified against the sha256 sidecar surfaced by
# /agent/console/info when one is staged. Install prefers `apt-get install`
# (resolves the deb's dependencies); root or sudo is required for that step.
set -euo pipefail

CENTRAL="${HUGPY_CENTRAL:-https://dev.hugpy.ai/api}"
CENTRAL="${CENTRAL%/}"
TOKEN="${HUGPY_TOKEN:-${HUGPY_OPERATOR_TOKEN:-}}"
[ -n "$TOKEN" ] || {
  echo "error: no credential. Set HUGPY_TOKEN (or HUGPY_OPERATOR_TOKEN) — the" >&2
  echo "       console artifacts are member-gated, e.g.:" >&2
  echo "       curl -fsSL $CENTRAL/agent/console/install.sh | HUGPY_TOKEN=xxx bash" >&2
  exit 1
}
command -v curl >/dev/null || { echo "error: curl is required" >&2; exit 1; }

auth=(-H "Authorization: Bearer $TOKEN")
info="$(curl -fsSL "${auth[@]}" "$CENTRAL/agent/console/info")" || {
  echo "error: $CENTRAL/agent/console/info unreachable or credential rejected" >&2
  exit 1
}

# Parse {deb:{filename,sha256}} — python3 when present, sed as a last resort.
if command -v python3 >/dev/null; then
  fname="$(printf '%s' "$info" | python3 -c \
    'import json,sys; d=json.load(sys.stdin).get("deb") or {}; print(d.get("filename",""))')"
  sha="$(printf '%s' "$info" | python3 -c \
    'import json,sys; d=json.load(sys.stdin).get("deb") or {}; print(d.get("sha256",""))')"
else
  fname="$(printf '%s' "$info" | sed -n 's/.*"filename"[[:space:]]*:[[:space:]]*"\(fleet-console_[^"]*\.deb\)".*/\1/p' | head -1)"
  sha="$(printf '%s' "$info" | sed -n 's/.*"sha256"[[:space:]]*:[[:space:]]*"\([0-9a-f]\{64\}\)".*/\1/p' | head -1)"
fi
[ -n "$fname" ] || { echo "error: no fleet-console .deb staged on the central" >&2; exit 1; }

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
echo "downloading $fname ..."
curl -fSL "${auth[@]}" -o "$TMP/$fname" "$CENTRAL/agent/console/$fname"

if [ -n "$sha" ] && command -v sha256sum >/dev/null; then
  echo "$sha  $TMP/$fname" | sha256sum -c - >/dev/null \
    || { echo "error: sha256 mismatch — refusing to install" >&2; exit 1; }
  echo "sha256 verified"
fi

SUDO=""
[ "$(id -u)" = 0 ] || SUDO="sudo"
echo "installing (apt resolves the deb's dependencies) ..."
if $SUDO apt-get install -y "$TMP/$fname"; then
  :
else
  # older apt without local-deb support
  $SUDO dpkg -i "$TMP/$fname" || $SUDO apt-get install -y -f
fi
echo "ok: $fname installed — launch 'fleet-console'"
