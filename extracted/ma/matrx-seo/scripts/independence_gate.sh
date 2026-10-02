#!/usr/bin/env bash
set -euo pipefail

package_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
repo_dir="$(cd "$package_dir/../.." && pwd)"
gate_dir="$(mktemp -d /tmp/matrx-seo-gate.XXXXXX)"

cleanup() {
    case "$gate_dir" in
        /tmp/matrx-seo-gate.*) rm -rf "$gate_dir" ;;
        *) echo "refusing to clean unexpected gate path: $gate_dir" >&2 ;;
    esac
}
trap cleanup EXIT

uv venv "$gate_dir/.venv" --python 3.13
uv pip install \
    --python "$gate_dir/.venv/bin/python" \
    -e "$repo_dir/packages/matrx-utils" \
    -e "$repo_dir/packages/matrx-orm" \
    -e "$repo_dir/packages/matrx-connect" \
    -e "$package_dir[standalone,dev]"

cd "$gate_dir"
env -u PYTHONPATH \
    -u CREDENTIALS_ENCRYPTION_KEY \
    -u SUPABASE_MATRIX_URL -u SUPABASE_URL \
    -u SUPABASE_JWT_SECRET -u SUPABASE_MATRIX_JWT_SECRET \
    -u SUPABASE_MATRIX_HOST -u SUPABASE_MATRIX_PORT -u SUPABASE_MATRIX_DATABASE_NAME \
    -u SUPABASE_MATRIX_USER -u SUPABASE_MATRIX_PASSWORD \
    "$gate_dir/.venv/bin/python" - <<'PY'
import asyncio
import os

from matrx_seo import InMemorySeoRepository, SeoCollectionService

assert InMemorySeoRepository is not None
assert SeoCollectionService is not None

# Construction needs NO environment — only lifespan startup enforces the env contract.
from matrx_seo.standalone.app import ADAPTER_FACTORIES, create_app

app = create_app()
routes = {getattr(route, "path", None) for route in app.routes}
expected = {"/health", "/health/ready", "/collections", "/collections/{run_id}"}
missing = expected - routes
assert not missing, f"standalone app is missing routes: {sorted(missing)}"
assert ADAPTER_FACTORIES, "standalone app must expose at least one provider adapter"
for name, factory in ADAPTER_FACTORIES.items():
    assert factory().provider == name


async def expect_boot_refusal(expect: str) -> None:
    application = create_app()
    try:
        async with application.router.lifespan_context(application):
            raise AssertionError("standalone startup must fail without its env contract")
    except RuntimeError as exc:
        assert expect in str(exc), f"expected {expect!r} in boot error, got: {exc}"


# No env at all -> refuses (no JWT verification material).
asyncio.run(expect_boot_refusal("JWT verification material"))

# JWT material present but no SUPABASE_MATRIX_* -> refuses at the DB gate.
os.environ["SUPABASE_JWT_SECRET"] = "gate-selftest-secret"
asyncio.run(expect_boot_refusal("SUPABASE_MATRIX"))

print("independence gate: standalone boot contract OK")
PY

env -u PYTHONPATH "$gate_dir/.venv/bin/python" -m pytest "$package_dir/tests" -q
