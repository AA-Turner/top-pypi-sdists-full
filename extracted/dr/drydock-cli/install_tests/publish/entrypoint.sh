#!/usr/bin/env bash
# Container entrypoint: ensures a sensible default drydock config
# exists, then execs the requested command (default: drydock).
#
# If the user mounts their own ~/.drydock as a volume, this script
# detects the existing config.toml and skips the default.
set -euo pipefail

CONFIG_DIR="${HOME}/.drydock"
CONFIG_PATH="${CONFIG_DIR}/config.toml"

mkdir -p "${CONFIG_DIR}"

if [ ! -f "${CONFIG_PATH}" ]; then
    LLAMACPP_URL="${LLAMACPP_URL:-http://host.docker.internal:8001/v1}"
    LLAMACPP_MODEL="${LLAMACPP_MODEL:-gemma4}"
    cat > "${CONFIG_PATH}" <<EOF
# Default drydock config — written by container entrypoint on first run.
# Override by mounting your own ~/.drydock:/root/.drydock volume.

active_model = "local"
auto_approve = false
enable_telemetry = false
enable_update_checks = false
enable_auto_update = false
disable_welcome_banner_animation = false
api_timeout = 60.0

[[providers]]
name = "llamacpp"
api_base = "${LLAMACPP_URL}"
api_key_env_var = ""
api_style = "openai"
backend = "generic"

[[models]]
name = "${LLAMACPP_MODEL}"
provider = "llamacpp"
alias = "local"
EOF
fi

# Pre-trust the working directory (drydock pops a Trust dialog on
# unfamiliar dirs; not ergonomic in a container).
TRUSTED="${CONFIG_DIR}/trusted_folders.toml"
if [ ! -f "${TRUSTED}" ]; then
    cat > "${TRUSTED}" <<EOF
trusted = ["${PWD}", "/work"]
EOF
fi

exec "$@"
