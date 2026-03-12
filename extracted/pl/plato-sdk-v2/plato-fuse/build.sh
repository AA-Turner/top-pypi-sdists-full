#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
IMAGE_NAME="plato-fuse-builder"
TARGET_GLIBC="2.34"
TARGET_TRIPLE="x86_64-unknown-linux-gnu.${TARGET_GLIBC}"
TARGET_DIR="$SCRIPT_DIR/target"
TARGET_BINARY_DIR="$TARGET_DIR/x86_64-unknown-linux-gnu/release"
DOCKER_PLATFORM="${DOCKER_PLATFORM:-}"

echo "Building $IMAGE_NAME image..."
DOCKER_BUILD_ARGS=()
if [[ -n "$DOCKER_PLATFORM" ]]; then
    DOCKER_BUILD_ARGS+=(--platform "$DOCKER_PLATFORM")
fi
docker build "${DOCKER_BUILD_ARGS[@]}" -t "$IMAGE_NAME" -f "$SCRIPT_DIR/Dockerfile.builder" "$SCRIPT_DIR"

echo "Building plato-fuse binary..."
DOCKER_RUN_ARGS=()
if [[ -n "$DOCKER_PLATFORM" ]]; then
    DOCKER_RUN_ARGS+=(--platform "$DOCKER_PLATFORM")
fi
docker run --rm \
    "${DOCKER_RUN_ARGS[@]}" \
    -v "$SCRIPT_DIR":/src \
    -v "$TARGET_DIR":/src/target \
    -v plato-fuse-cargo-registry:/root/.cargo/registry \
    -v plato-fuse-cargo-git:/root/.cargo/git \
    -w /src \
    "$IMAGE_NAME" \
    bash -lc "rustup target add x86_64-unknown-linux-gnu && cargo zigbuild --release --target \"$TARGET_TRIPLE\""

BINARY="$TARGET_BINARY_DIR/plato-fuse"
if [[ ! -f "$BINARY" ]]; then
    echo "ERROR: Binary not found at $BINARY"
    exit 1
fi

echo "Binary built: $BINARY ($(du -h "$BINARY" | cut -f1))"
if command -v objdump &>/dev/null; then
    MAX_GLIBC="$(
        objdump -T "$BINARY" \
        | grep -o 'GLIBC_[0-9]\+\.[0-9]\+' \
        | sed 's/GLIBC_//' \
        | sort -V \
        | tail -n1
    )"
    echo "Binary max GLIBC requirement: ${MAX_GLIBC:-unknown}"
fi
