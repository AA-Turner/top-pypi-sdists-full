#!/usr/bin/env bash
# cloud-files: the Cloud folder's helper on a Cloud Computer.
#   cloud-files fetch <path>   download the real file behind a placeholder (stub)
#   cloud-files status         what is synced, stubbed, and the last error
#   cloud-files sync           sync both ways now
#   cloud-files restore-held   put back the files whose deletes the sync is holding
#   (deleting held files in the cloud is confirmed by the person in the AI Matrx app)
set -euo pipefail
port="${BROWSER_WORKER_PORT:-8002}"
base="http://127.0.0.1:${port}/machine/cloud-files"
case "${1:-status}" in
  fetch)
    shift
    [[ $# -ge 1 ]] || { echo "usage: cloud-files fetch <path>" >&2; exit 2; }
    for p in "$@"; do
      abs="$(realpath -m -- "$p")"
      curl -fsS -X POST --get --data-urlencode "path=${abs}" "${base}/fetch"; echo
    done ;;
  status) curl -fsS "${base}/status"; echo ;;
  sync) curl -fsS -X POST "${base}/sync-now"; echo ;;
  restore-held)
    hold="$(curl -fsS "${base}/status" | python3 -c 'import json,sys; h=(json.load(sys.stdin).get("sync") or {}).get("halt") or {}; print(h.get("hold_id") or "")')"
    [[ -n "$hold" ]] || { echo "nothing is held"; exit 0; }
    curl -fsS -X POST -H 'content-type: application/json' \
      -d "{\"hold_id\":\"${hold}\",\"action\":\"restore\"}" "${base}/resolve-held"; echo ;;
  confirm-deletes)
    echo "Deleting held files in the cloud is confirmed in the AI Matrx app (Computer tab)." >&2
    echo "To put them back here instead: cloud-files restore-held" >&2; exit 1 ;;
  *) echo "usage: cloud-files fetch <path> | status | sync | restore-held" >&2; exit 2 ;;
esac
