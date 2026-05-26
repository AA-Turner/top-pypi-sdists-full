#!/usr/bin/env bash
# Build + run drydock install smoke tests across Linux containers.
# Windows is not run by this script — see windows/README.md for manual steps.
#
# Usage:
#   ./run_all.sh                          # all OSes
#   ./run_all.sh ubuntu                   # specific OS
#   ./run_all.sh ubuntu rocky             # multiple
#   DRYDOCK_VERSION=2.8.85 ./run_all.sh   # pin a specific drydock-cli version
#
# Env:
#   DRYDOCK_VERSION   — pip-install pin (default: latest from PyPI)
#   LLAMACPP_URL      — model endpoint inside the container (default:
#                       http://host.docker.internal:8001/v1 — host gateway)
#   LLAMACPP_MODEL    — model name (default: gemma4)
#   SMOKE_TIMEOUT_S   — per-test pexpect timeout (default: 90)
#   VERBOSE           — extra logging
#   PARALLEL          — run all containers concurrently (default: serial)
#
set -euo pipefail

cd "$(dirname "$0")"

OSES=("${@}")
if [ ${#OSES[@]} -eq 0 ]; then
    OSES=("ubuntu" "rocky")
fi

DRYDOCK_VERSION="${DRYDOCK_VERSION:-}"
LLAMACPP_URL="${LLAMACPP_URL:-http://host.docker.internal:8001/v1}"
LLAMACPP_MODEL="${LLAMACPP_MODEL:-gemma4}"
SMOKE_TIMEOUT_S="${SMOKE_TIMEOUT_S:-90}"
VERBOSE="${VERBOSE:-}"
PARALLEL="${PARALLEL:-}"

OUT_DIR="results/$(date -u +%Y%m%d_%H%M%S)"
mkdir -p "${OUT_DIR}"

run_one() {
    local os=$1
    local log_path="${OUT_DIR}/${os}.log"
    local result_path="${OUT_DIR}/${os}.result"

    echo "=== building ${os} ==="
    docker build -t "drydock-smoke-${os}" "${os}/" \
        > "${log_path}.build" 2>&1 || {
            echo "[BUILD FAIL] ${os} — see ${log_path}.build"
            echo "BUILD_FAIL" > "${result_path}"
            return 1
        }

    echo "=== running ${os} ==="
    docker run --rm \
        --add-host=host.docker.internal:host-gateway \
        -v "$(pwd)/smoke_test.py:/work/smoke_test.py:ro" \
        -e "DRYDOCK_VERSION=${DRYDOCK_VERSION}" \
        -e "LLAMACPP_URL=${LLAMACPP_URL}" \
        -e "LLAMACPP_MODEL=${LLAMACPP_MODEL}" \
        -e "SMOKE_TIMEOUT_S=${SMOKE_TIMEOUT_S}" \
        -e "VERBOSE=${VERBOSE}" \
        -e "OS_LABEL=${os}" \
        "drydock-smoke-${os}" \
        2>&1 | tee "${log_path}"

    # Capture the last [RESULT] line as the result
    grep '^\[RESULT\]' "${log_path}" | tail -1 > "${result_path}" || \
        echo "[RESULT] ${os} INCOMPLETE" > "${result_path}"
}

if [ -n "${PARALLEL}" ]; then
    pids=()
    for os in "${OSES[@]}"; do
        run_one "$os" &
        pids+=($!)
    done
    wait "${pids[@]}" || true
else
    for os in "${OSES[@]}"; do
        run_one "$os" || true
    done
fi

echo
echo "=========================================================="
echo "  SUMMARY  (logs in ${OUT_DIR}/)"
echo "=========================================================="
for os in "${OSES[@]}"; do
    if [ -f "${OUT_DIR}/${os}.result" ]; then
        cat "${OUT_DIR}/${os}.result"
    fi
done
