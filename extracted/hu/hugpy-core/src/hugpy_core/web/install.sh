#!/usr/bin/env bash
# Served by /api/fleet/workers/install.sh: makes this box a worker of the Core at CENTRAL (Core fills it in).
# The console's Settings -> Boxes gives the whole line:
#   curl -fsSL <core>/api/fleet/workers/install.sh | sudo bash -s -- --name NAME --token T --core-key K
#        [--worker DIR] [--central DIR]
#   1. the signed hugpy APT repository, the Wrapper (with its llama.cpp engine) and Discovery;
#   2. this box enrolled through Core (single-use token T, when given);
#   3. the Wrapper on this box's network address, with every engine (--engines all) and its model drives entered
#      in Discovery (the worker drive DIR, default /srv/MODELS/worker as on ae; a central drive when given),
#      connected to this Core with the key K, then restarted.
# 2026-11-14 (a clean VM, the operator: "every single time i install a wrapper anywhere its this"): without the
# engines and a declared drive a new box's Discovery never started and its Wrapper had no engine, unlike ae.
# 2026-11-14: replaces the fitevict-era worker installer (hugpy-wrapper>=0.1.59 + hugpy-worker + `fitevict install`).
set -euo pipefail

CENTRAL=""
NAME="${HUGPY_WORKER_NAME:-$(hostname -s)}"
TOKEN=""
CORE_KEY=""
WORKER_DIR="${HUGPY_WORKER_DIR:-/srv/MODELS/worker}"
CENTRAL_DIR=""
while (( $# )); do
  case "$1" in
    --name|--token|--core-key|--worker|--central)
      if (( $# < 2 )); then echo "$1 needs a value" >&2; exit 2; fi
      case "$1" in --name) NAME="$2" ;; --token) TOKEN="$2" ;; --core-key) CORE_KEY="$2" ;;
                   --worker) WORKER_DIR="$2" ;; --central) CENTRAL_DIR="$2" ;; esac
      shift 2 ;;
    *) echo "Unknown install option: $1" >&2; exit 2 ;;
  esac
done

if [[ ! "$CENTRAL" =~ ^https?://[A-Za-z0-9._:-]+$ ]]; then
  echo "Install URL has no valid Core address: $CENTRAL" >&2; exit 2
fi
if [[ ! "$NAME" =~ ^[A-Za-z0-9._-]+$ ]]; then
  echo "The worker name must use letters, digits, dot, underscore or dash" >&2; exit 2
fi
[[ $EUID == 0 ]] || { echo "Run it as root: curl -fsSL $CENTRAL/api/fleet/workers/install.sh | sudo bash -s -- ..." >&2; exit 1; }

echo "== 1/3 the hugpy APT repository, the Wrapper (with its llama.cpp engine) and Discovery"
curl -fsSL --proto '=https' https://hugpy.ai/apt/setup.sh | bash -s -- --install wrapper
apt-get install -y hugpy-discovery

if [[ -n "$TOKEN" ]]; then
  echo "== 2/3 enrolling $NAME through $CENTRAL"
  install -d -m 0755 /etc/hugpy
  payload=$(python3 -c 'import json, socket, sys; print(json.dumps({"enroll_token": sys.argv[1], "name": sys.argv[2], "info": {"host": socket.gethostname()}}))' "$TOKEN" "$NAME")
  (umask 077; curl -fsS -X POST "$CENTRAL/api/boxes/enroll" -H 'Content-Type: application/json' -d "$payload" > /etc/hugpy/box-enrollment.json)
  chmod 0600 /etc/hugpy/box-enrollment.json
else
  echo "== 2/3 no enrollment token given: enrollment skipped"
fi

for dir in "$WORKER_DIR" $CENTRAL_DIR; do
  [[ "$dir" == /* ]] || { echo "A model drive is an absolute path: $dir" >&2; exit 2; }
done
echo "== 3/3 the Wrapper on this box's network address, every engine, drives entered, connected to $CENTRAL"
# --link: the Wrapper connects out to this Core, which then needs no way in to this box (any network)
wrapper_args=(--host auto --engines all --worker "$WORKER_DIR" --core "$CENTRAL" --link)
[[ -n "$CENTRAL_DIR" ]] && wrapper_args+=(--central "$CENTRAL_DIR")
[[ -n "$CORE_KEY" ]] && wrapper_args+=(--core-key "$CORE_KEY")
hugpy-wrapper system install "${wrapper_args[@]}"
systemctl restart hugpy-wrapper.service || true
echo "Done: $NAME is installed and connected to $CENTRAL (worker drive $WORKER_DIR${CENTRAL_DIR:+, central drive $CENTRAL_DIR})."
