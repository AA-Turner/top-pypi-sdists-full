#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
IMAGE_NAME="plato-fuse-builder"
S3_BUCKET="plato-public-static"
S3_KEY="plato-fuse"
AWS_REGION="us-west-1"
TARGET_GLIBC="2.34"
TARGET_TRIPLE="x86_64-unknown-linux-gnu.${TARGET_GLIBC}"
TARGET_DIR="$SCRIPT_DIR/target"
TARGET_BINARY_DIR="$TARGET_DIR/x86_64-unknown-linux-gnu/release"

echo "Building $IMAGE_NAME image..."
docker build -t "$IMAGE_NAME" -f "$SCRIPT_DIR/Dockerfile.builder" "$SCRIPT_DIR"

echo "Building plato-fuse binary..."
docker run --rm \
    -v "$SCRIPT_DIR":/src \
    -v "$TARGET_DIR":/src/target \
    -v plato-fuse-cargo-registry:/root/.cargo/registry \
    -v plato-fuse-cargo-git:/root/.cargo/git \
    -w /src \
    "$IMAGE_NAME" cargo zigbuild --release --target "$TARGET_TRIPLE"

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

echo "Uploading to s3://$S3_BUCKET/$S3_KEY ..."
aws s3 cp "$BINARY" "s3://$S3_BUCKET/$S3_KEY" --region "$AWS_REGION"

echo "Done. Published to https://$S3_BUCKET.s3.$AWS_REGION.amazonaws.com/$S3_KEY"
