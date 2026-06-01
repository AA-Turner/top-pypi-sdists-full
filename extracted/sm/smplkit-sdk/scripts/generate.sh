#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OPENAPI_DIR="$REPO_ROOT/openapi"
GENERATED_DIR="$REPO_ROOT/src/smplkit/_generated"
CONFIG="$REPO_ROOT/generator/config.yaml"

for spec in "$OPENAPI_DIR"/*.json; do
    [ -f "$spec" ] || continue

    service="$(basename "$spec" .json)"
    output_dir="$GENERATED_DIR/$service"

    echo "Generating client for service: $service"

    # Remove existing generated code for idempotency
    rm -rf "$output_dir"

    python3 -m openapi_python_client generate \
        --path "$spec" \
        --config "$CONFIG" \
        --output-path "$output_dir" \
        --meta none

    echo "Generated client at: $output_dir"
done

echo "Done."
