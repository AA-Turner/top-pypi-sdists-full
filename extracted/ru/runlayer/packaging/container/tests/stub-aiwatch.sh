#!/bin/sh
# Stub aiwatch for the container entrypoint smoke test — NOT the real scanner.
# Stands in for /usr/lib/runlayer/aiwatch/aiwatch. On `scan --username X` it
# appends a marker line to $HOME/.runlayer/scanned (proving which uid the drop
# landed on, and that the home was writable) and exits 0.
set -u

case "${1:-}" in
--version)
    echo "aiwatch 0.0.0-stub (container smoke-test stub)"
    ;;
scan)
    username=unknown
    while [ $# -gt 0 ]; do
        if [ "$1" = "--username" ] && [ $# -gt 1 ]; then username=$2; fi
        shift
    done
    # A home the dropped uid can't write exits 0 quietly — mirrors the real
    # scanner tolerating an unwritable ~ for accounts with root-owned homes.
    mkdir -p "$HOME/.runlayer" 2>/dev/null || exit 0
    printf 'scanned user=%s uid=%s groups=%s strip=%s home=%s\n' \
        "$username" "$(id -u)" "$(id -G | tr ' ' ',')" \
        "${RUNLAYER_STRIP_PATH_PREFIX:-none}" "$HOME" \
        >>"$HOME/.runlayer/scanned" 2>/dev/null || exit 0
    ;;
*)
    echo "stub aiwatch: unsupported args: $*" >&2
    exit 2
    ;;
esac
exit 0
