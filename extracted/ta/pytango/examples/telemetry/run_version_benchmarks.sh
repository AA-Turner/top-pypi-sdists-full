#!/usr/bin/env bash
# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

set -euo pipefail

READS_PER_ITERATION="${READS_PER_ITERATION:-300}"
ITERATIONS="${ITERATIONS:-100}"
SERVER_START_TIMEOUT="${SERVER_START_TIMEOUT:-60}"
TOPICS="${TOPICS:-all}"
EMIT_KERNEL_SPANS="${EMIT_KERNEL_SPANS:-off}"
PIXI_CACHE_DIR="${PIXI_CACHE_DIR:-/tmp/pixi-cache}"
RATTLER_CACHE_DIR="${RATTLER_CACHE_DIR:-/tmp/rattler-cache}"

PYTANGO_100_DIR="/tmp/pytango-100"
PYTANGO_101_DIR="/tmp/pytango-101"
CURRENT_REPO_MANIFEST="../.."

export PIXI_CACHE_DIR
export RATTLER_CACHE_DIR

write_env_manifest() {
    local env_dir="$1"
    local pytango_version="$2"
    local omniorb_spec="$3"

    mkdir -p "${env_dir}"
    cat >"${env_dir}/pixi.toml" <<EOF
[workspace]
channels = ["conda-forge"]
platforms = ["osx-arm64"]

[dependencies]
pytango = "==${pytango_version}"
tango-test = "*"
cxx-compiler = "*"
cmake = ">=3.18"
ninja = ">=1.11"
cppzmq = ">=4.10.0"
omniorb = "${omniorb_spec}"
zeromq = ">=4.0.5"
libjpeg-turbo = ">=1.5.2"
tango-idl = "==6.0.2"
libopentelemetry-cpp = ">=1.11.0"
EOF
}

install_env() {
    local env_dir="$1"
    pixi install --manifest-path "${env_dir}"
}

warn_if_current_repo_debug_build_type() {
    local pixi_toml="${CURRENT_REPO_MANIFEST}/pixi.toml"

    if [[ ! -f "${pixi_toml}" ]]; then
        return
    fi

    if grep -q 'cmake\.build-type.*Debug' "${pixi_toml}"; then
        cat >&2 <<EOF
WARNING: ${pixi_toml} contains a cmake.build-type set to Debug.
Benchmark timings from a Debug build can be misleading. Use RelWithDebInfo or Release instead.
EOF
    fi
}

run_benchmarks() {
    local label="$1"
    local manifest_path="$2"
    local telemetry_env_vars="$3"
    local kernel_span_args=()

    case "${EMIT_KERNEL_SPANS}" in
        1 | true | TRUE | yes | YES | on | ON)
            kernel_span_args+=(--emit-kernel-spans)
            ;;
    esac

    echo
    echo "=== ${label} ==="
    pixi run --manifest-path "${CURRENT_REPO_MANIFEST}" python run_benchmarks.py \
        --pixi-manifest-path "${manifest_path}" \
        --telemetry-env-vars "${telemetry_env_vars}" \
        --iterations "${ITERATIONS}" \
        --reads-per-iteration "${READS_PER_ITERATION}" \
        --telemetry-topics "${TOPICS}" \
        --server-start-timeout "${SERVER_START_TIMEOUT}" \
        "${kernel_span_args[@]}"
}

write_env_manifest "${PYTANGO_100_DIR}" "10.0" "==4.3.2"
write_env_manifest "${PYTANGO_101_DIR}" "10.1" ">=4.3.0"

warn_if_current_repo_debug_build_type

install_env "${PYTANGO_100_DIR}"
install_env "${PYTANGO_101_DIR}"

run_benchmarks "PyTango 10.0" "${PYTANGO_100_DIR}" "singular"
run_benchmarks "PyTango 10.1" "${PYTANGO_101_DIR}" "singular"
run_benchmarks "Current repo" "${CURRENT_REPO_MANIFEST}" "plural"
