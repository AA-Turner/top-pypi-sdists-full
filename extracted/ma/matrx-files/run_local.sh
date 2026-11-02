#!/usr/bin/env bash
# Run the matrx-files standalone microservice LOCALLY against the live DB + S3,
# so you can point the FE at http://localhost:<port> and test the exact code
# that runs in production.
#
#   From the aidream repo root:  ./packages/matrx-files/run_local.sh [port]   (default 8090)
#
# It maps the aidream .env (SUPABASE_MATRIX_* / AWS_* / CDN_*) into the variable
# names the standalone app reads (standalone/app.py::_env_config), then boots
# uvicorn. Full mode: DB pool + JWT auth + all routers. Ctrl-C to stop.
set -euo pipefail
PORT="${1:-8090}"
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
[ -f .env ] || { echo "no aidream .env at $ROOT/.env"; exit 1; }

# Map aidream env -> matrx-files env (same mapping the EC2 deploy uses).
eval "$(python3 - <<'PY'
env = {}
for line in open(".env"):
    line = line.strip()
    if not line or line.startswith("#") or "=" not in line:
        continue
    k, v = line.split("=", 1)
    env[k] = v.strip().strip('"').strip("'")
def emit(name, val):
    if val:
        print(f'export {name}={val!r}')
# DB (Supavisor pooler — same as prod)
for k in ("SUPABASE_MATRIX_HOST","SUPABASE_MATRIX_PORT","SUPABASE_MATRIX_USER",
          "SUPABASE_MATRIX_PASSWORD","SUPABASE_MATRIX_DATABASE_NAME","SUPABASE_MATRIX_URL",
          "SUPABASE_MATRIX_JWT_SECRET","AWS_S3_DEFAULT_BUCKET","AWS_ACCESS_KEY_ID",
          "AWS_SECRET_ACCESS_KEY","AWS_DEFAULT_REGION","CDN_PUBLIC_BASE_URL","AWS_S3_PUBLIC_BUCKET"):
    emit(k, env.get(k))
# names the app expects under different keys
emit("SUPABASE_URL", env.get("SUPABASE_MATRIX_URL"))
emit("SUPABASE_SECRET_KEY", env.get("SUPABASE_MATRIX_SECRET_KEY"))
emit("MATRX_FILES_BASE_DIR", "/tmp/matrx-files-local")
PY
)"

echo "▶ matrx-files standalone → http://127.0.0.1:${PORT}"
echo "  health:  curl http://127.0.0.1:${PORT}/files-service/health"
echo "  point the FE at it:  NEXT_PUBLIC_FILES_URL=http://127.0.0.1:${PORT}  (in matrx-frontend/.env.local)"
exec uv run uvicorn matrx_files.standalone.app:create_app --factory --host 127.0.0.1 --port "${PORT}"
