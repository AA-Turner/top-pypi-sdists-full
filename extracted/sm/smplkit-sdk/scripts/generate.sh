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

# Honor the declared attrs floor (>=21.3.0).
#
# openapi-python-client emits the Client/AuthenticatedClient attributes as e.g.
# `_base_url: str = field(alias="base_url")`. The `alias` keyword on attrs.field
# was only added in attrs 22.2.0, so its presence silently raises the floor a
# consumer must satisfy from 21.3.0 to 22.2.0. But the alias is redundant: attrs
# strips leading underscores when deriving the __init__ parameter name (since
# 20.1.0), so `_base_url = field()` already yields the `base_url` init parameter.
# Strip the redundant alias so the generated client keeps working on attrs
# 21.3.0 — fixing the code to honor the floor rather than raising the floor.
echo "Stripping redundant attrs field(alias=...) to honor the attrs>=21.3.0 floor"
find "$GENERATED_DIR" -name client.py -exec sed -i.bak -E \
    -e 's/, alias="[^"]*"//g' \
    -e 's/\(alias="[^"]*"\)/()/g' {} +
find "$GENERATED_DIR" -name 'client.py.bak' -delete

echo "Done."
