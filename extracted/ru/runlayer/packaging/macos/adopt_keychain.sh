#!/bin/bash
# Recreate one legacy runlayer-cli keychain item with the packaged CLI.

set -euo pipefail

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <host-url>" >&2
    echo "Example: $0 https://app.runlayer.com" >&2
    exit 2
fi

HOST="$1"
case "$HOST" in
    https://*)
        SCHEME="https"
        AUTHORITY="${HOST#https://}"
        ;;
    http://*)
        SCHEME="http"
        AUTHORITY="${HOST#http://}"
        ;;
    *)
        echo "Error: host must be a full http(s) URL." >&2
        exit 2
        ;;
esac

AUTHORITY="${AUTHORITY%%/*}"
AUTHORITY="${AUTHORITY%%\?*}"
AUTHORITY="${AUTHORITY%%\#*}"
# Mirror url_to_host_key: hostname is lowercased, port is preserved verbatim.
HOSTNAME_PART="${AUTHORITY%%:*}"
HOSTNAME_PART="$(printf '%s' "$HOSTNAME_PART" | tr '[:upper:]' '[:lower:]')"
PORT_PART=""
case "$AUTHORITY" in
    *:*) PORT_PART="${AUTHORITY#*:}" ;;
esac
if [ "$SCHEME" = "https" ] && [ "$PORT_PART" = "443" ]; then
    PORT_PART=""
elif [ "$SCHEME" = "http" ] && [ "$PORT_PART" = "80" ]; then
    PORT_PART=""
fi
if [ -z "$HOSTNAME_PART" ]; then
    echo "Error: host URL has no hostname." >&2
    exit 2
fi
HOST_KEY="$HOSTNAME_PART"
if [ -n "$PORT_PART" ]; then
    HOST_KEY="$HOSTNAME_PART:$PORT_PART"
fi

RUNLAYER_BIN="${RUNLAYER_BIN:-/usr/local/bin/runlayer}"
if [ ! -x "$RUNLAYER_BIN" ]; then
    RUNLAYER_BIN="$(command -v runlayer || true)"
fi
if [ -z "$RUNLAYER_BIN" ] || [ ! -x "$RUNLAYER_BIN" ]; then
    echo "Error: packaged runlayer CLI not found." >&2
    exit 1
fi

SECRET=""
trap 'unset SECRET' EXIT

echo "macOS may ask once for access to the saved Runlayer credential." >&2
if ! SECRET="$(/usr/bin/security find-generic-password \
    -s runlayer-cli -a "$HOST_KEY" -w)"; then
    echo "Error: could not read the keychain credential; it was left unchanged." >&2
    exit 1
fi

if ! /usr/bin/security delete-generic-password \
    -s runlayer-cli -a "$HOST_KEY" >/dev/null; then
    echo "Error: could not delete the legacy keychain credential." >&2
    exit 1
fi

if ! RUNLAYER_API_KEY="$SECRET" "$RUNLAYER_BIN" credentials add user --host "$HOST"; then
    echo "Error: could not recreate the credential with the packaged CLI." >&2
    exit 1
fi

echo "Adopted keychain credential for $HOST_KEY." >&2
