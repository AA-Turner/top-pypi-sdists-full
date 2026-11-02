#!/usr/bin/env bash
# Served by /api/fleet/workers/install.sh. Core fills CENTRAL with its public URL.
set -euo pipefail

CENTRAL=""
WORKER_NAME="${HUGPY_WORKER_NAME:-$(hostname -s)}"
WORKER_PORT="${HUGPY_WORKER_PORT:-9100}"
WRAPPER_PORT="${HUGPY_WRAPPER_PORT:-7302}"
NODE_PORT="${HUGPY_NODE_PORT:-7300}"
WORKER_VENV="${HUGPY_WORKER_VENV:-$HOME/.local/share/hugpy/worker-venv}"

# The console supplies these with `bash -s -- --name ... --token ...`.
while (( $# )); do
  case "$1" in
    --name|--token)
      if (( $# < 2 )); then echo "$1 needs a value" >&2; exit 2; fi
      if [[ "$1" == --name ]]; then WORKER_NAME="$2"; else HUGPY_ENROLL_TOKEN="$2"; fi
      shift 2 ;;
    *) echo "Unknown install option: $1" >&2; exit 2 ;;
  esac
done

if [[ ! "$CENTRAL" =~ ^https?://[A-Za-z0-9._:-]+$ ]]; then
  echo "Install URL has no valid central address: $CENTRAL" >&2; exit 2
fi
if [[ ! "$WORKER_NAME" =~ ^[A-Za-z0-9._-]+$ ]]; then
  echo "HUGPY_WORKER_NAME must use letters, digits, dot, underscore or dash" >&2; exit 2
fi
for port in "$WORKER_PORT" "$WRAPPER_PORT" "$NODE_PORT"; do
  if [[ ! "$port" =~ ^[0-9]+$ ]] || (( port < 1024 || port > 65535 )); then
    echo "Worker, wrapper and node ports must be 1024–65535" >&2; exit 2
  fi
done
if [[ "$WORKER_PORT" == "$WRAPPER_PORT" || "$WORKER_PORT" == "$NODE_PORT" || "$WRAPPER_PORT" == "$NODE_PORT" ]]; then
  echo "Worker, wrapper and node ports must differ" >&2; exit 2
fi

python3 -m venv "$WORKER_VENV"
"$WORKER_VENV/bin/python" -m pip install --disable-pip-version-check --upgrade \
  'hugpy-wrapper>=0.1.59' 'hugpy-worker>=0.1.16' 'abstract_toolserver[server,db]>=0.0.95'

wrapper_args=(--user --port "$WRAPPER_PORT" --yes --tf)
if [[ -n "${HUGPY_MODELS_HOME:-}" ]]; then
  wrapper_args+=(--models "$HUGPY_MODELS_HOME")
fi
"$WORKER_VENV/bin/fitevict" install "${wrapper_args[@]}"

# The account node is separate from core's orbit toolserver. The supported
# method provisions its own DB, identity and system unit, retaining them on rerun.
if ! command -v sudo >/dev/null; then
  echo "sudo is required once for abstract-toolserver node install" >&2; exit 2
fi
sudo "$WORKER_VENV/bin/abstract-toolserver" node install --user "$(id -un)" \
  --port "$NODE_PORT" --db own

if [[ ! -s "$HOME/.config/hugpy/box.cred" && -z "${HUGPY_ENROLL_TOKEN:-}" ]]; then
  if [[ ! -r /dev/tty ]]; then
    echo "Set HUGPY_ENROLL_TOKEN to a single-use token from central Settings → Boxes" >&2; exit 2
  fi
  read -rsp 'Single-use Hugpy box enrollment token: ' HUGPY_ENROLL_TOKEN </dev/tty
  echo >/dev/tty
fi
export HUGPY_ENROLL_TOKEN="${HUGPY_ENROLL_TOKEN:-}"
"$WORKER_VENV/bin/hugpy-worker-enroll" --central "$CENTRAL" --name "$WORKER_NAME"
unset HUGPY_ENROLL_TOKEN

config_dir="$HOME/.config/hugpy"
unit_dir="$HOME/.config/systemd/user"
mkdir -p "$config_dir" "$unit_dir"
chmod 700 "$config_dir"
env_file="$config_dir/worker.env"
unit_file="$unit_dir/hugpy-worker.service"
cat >"$env_file" <<EOF
WORKER_CENTRAL_URL=$CENTRAL
WORKER_NAME=$WORKER_NAME
WORKER_PORT=$WORKER_PORT
HUGPY_WORKER_FRONT_DOOR=http://127.0.0.1:$WRAPPER_PORT
EOF
chmod 600 "$env_file"
cat >"$unit_file" <<EOF
[Unit]
Description=Hugpy worker attached to $CENTRAL
After=network-online.target hugpy-wrapper.service
Wants=network-online.target

[Service]
Type=simple
EnvironmentFile=$env_file
ExecStart=$WORKER_VENV/bin/hugpy-worker
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
EOF
systemctl --user daemon-reload
systemctl --user enable --now hugpy-worker.service
for attempt in {1..20}; do
  if curl -fsS "http://127.0.0.1:$WORKER_PORT/health" >/dev/null; then
    echo "Worker $WORKER_NAME attached to $CENTRAL on port $WORKER_PORT"
    exit 0
  fi
  sleep 1
done
echo "Worker service did not become healthy; inspect journalctl --user -u hugpy-worker" >&2
exit 1
