#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
S3_BUCKET="plato-public-static"
S3_KEY="plato-fuse"
AWS_REGION="us-west-1"
SKIP_UPLOAD="${SKIP_UPLOAD:-0}"

# Build the binary
"$SCRIPT_DIR/build.sh"

BINARY="$SCRIPT_DIR/target/x86_64-unknown-linux-gnu/release/plato-fuse"

if [[ "$SKIP_UPLOAD" == "1" ]]; then
    echo "Skipping upload because SKIP_UPLOAD=1"
    exit 0
fi

echo "Uploading to s3://$S3_BUCKET/$S3_KEY ..."
aws s3 cp "$BINARY" "s3://$S3_BUCKET/$S3_KEY" --region "$AWS_REGION"

echo "Done. Published to https://$S3_BUCKET.s3.$AWS_REGION.amazonaws.com/$S3_KEY"
