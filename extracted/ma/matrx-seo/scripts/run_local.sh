#!/usr/bin/env bash
set -euo pipefail

package_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
repo_dir="$(cd "${package_dir}/../.." && pwd)"
env_file="${MATRX_SEO_ENV_FILE:-${repo_dir}/.env}"
port="${MATRX_SEO_LOCAL_PORT:-8081}"

if [[ ! -f "${env_file}" ]]; then
  echo "ERROR: matrx-seo local env file not found: ${env_file}" >&2
  echo "Set MATRX_SEO_ENV_FILE to an env file containing the SUPABASE_MATRIX_* and encryption/JWT values." >&2
  exit 1
fi

echo "Starting matrx-seo at http://127.0.0.1:${port}"
echo "Using ${env_file}; MATRX_SEO_LOCAL_DEV=1 permits its non-svc_seo database role on localhost only."

cd "${repo_dir}"
MATRX_SEO_LOCAL_DEV=1 exec uv run \
  --env-file "${env_file}" \
  --package matrx-seo \
  uvicorn matrx_seo.standalone.app:create_app \
  --factory \
  --host 127.0.0.1 \
  --port "${port}" \
  --reload \
  --reload-dir "${package_dir}"
