#!/usr/bin/env bash
# Chrome as a person on the desktop opens it. Basic password store keeps saved
# logins portable across machines (no keyring on the box).
exec /opt/google/chrome/chrome \
  --password-store=basic \
  --no-sandbox \
  --disable-dev-shm-usage \
  --no-first-run \
  --no-default-browser-check \
  "$@"
