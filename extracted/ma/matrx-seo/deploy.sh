#!/usr/bin/env bash
# Deploy matrx-seo to the live EC2 box behind https://seo.matrxserver.com
#
#   ./deploy.sh 0.1.0        # deploy a version (must already be on PyPI)
#   ./deploy.sh 0.0.9        # rolling back is the same command
#
# Mirrors packages/matrx-files/deploy.sh (same box, same pattern) and REFUSES
# to touch the live container until the new image is proven:
#   1. checks PyPI actually has the version (tag push publishes it)
#   2. syncs THIS directory's canonical Dockerfile to the box (kills drift)
#   3. builds matrx-seo:<version> on the box
#   4. asserts the built image really contains <version> (aborts otherwise)
#   5. swaps the container (rm + run — NEVER docker restart: --env-file is
#      read only at run time)
#   6. health-checks locally and through Cloudflare, checks the running package
#      version when exposed plus DataForSEO route inventory, verifies CORS, and proves
#      the service is inside its granted DB boundary (readiness reports service_role)
#
# Requires: `ssh matrx-sandbox` working (SSM per ~/.ssh/config; run
# `aws sso login --profile AdministratorAccess-872515272894` first if stale).
#
# The box needs /etc/matrx-seo.env (root 600) BEFORE the first deploy — see
# DEPLOY.md. It carries the ONE database's standard SUPABASE_MATRIX_* vars
# with USER/PASSWORD set to the svc_seo role, plus CREDENTIALS_ENCRYPTION_KEY.
set -euo pipefail

VERSION="${1:?usage: deploy.sh <version, e.g. 0.1.0>}"
HOST="${MATRX_SEO_HOST:-matrx-sandbox}"
PUBLIC_BASE="https://seo.matrxserver.com"
PRODUCTION_CORS_ORIGINS="https://www.aimatrx.com,https://aimatrx.com,https://demos.aimatrx.com"
PORT=8081
DIR="$(cd "$(dirname "$0")" && pwd)"

echo "==> [1/6] checking PyPI has matrx-seo==${VERSION}"
if ! curl -sf -m 15 "https://pypi.org/pypi/matrx-seo/${VERSION}/json" >/dev/null; then
  echo "ERROR: matrx-seo==${VERSION} is not on PyPI."
  echo "       Publish first: cd aidream && git tag matrx-seo/v${VERSION} && git push origin refs/tags/matrx-seo/v${VERSION}"
  exit 1
fi

echo "==> [2/6] syncing canonical Dockerfile to ${HOST}:/opt/matrx-seo/"
ssh "${HOST}" 'sudo mkdir -p /opt/matrx-seo'
scp -q "${DIR}/Dockerfile" "${HOST}:/tmp/matrx-seo.Dockerfile"
ssh "${HOST}" 'sudo mv /tmp/matrx-seo.Dockerfile /opt/matrx-seo/Dockerfile'

echo "==> [3/6] building matrx-seo:${VERSION} on ${HOST}"
ssh "${HOST}" "sudo docker build --build-arg MATRX_SEO_VERSION='==${VERSION}' -t 'matrx-seo:${VERSION}' /opt/matrx-seo"

echo "==> [4/6] verifying the image really contains ${VERSION}"
GOT="$(ssh "${HOST}" "sudo docker run --rm --entrypoint python 'matrx-seo:${VERSION}' -c 'import importlib.metadata as m; print(m.version(\"matrx-seo\"))'" | tr -d '[:space:]')"
if [ "${GOT}" != "${VERSION}" ]; then
  echo "ERROR: built image contains matrx-seo ${GOT}, expected ${VERSION} — ABORTING; live container untouched."
  exit 1
fi
echo "    image verified: ${GOT}"

echo "==> [5/6] swapping the live container (rm + run)"
# Keep manual and tag-driven deploys from interleaving their rm/run swaps on
# the one host.  The CI job acquires this same lock before it builds the image.
ssh "${HOST}" "sudo touch /var/tmp/matrx-seo-deploy.lock && sudo chmod 666 /var/tmp/matrx-seo-deploy.lock && flock -w 900 /var/tmp/matrx-seo-deploy.lock sh -c \"sudo docker rm -f matrx-seo >/dev/null 2>&1 || true; sudo docker run -d --name matrx-seo --restart unless-stopped --env-file /etc/matrx-seo.env -e 'MATRX_SEO_ALLOWED_ORIGINS=${PRODUCTION_CORS_ORIGINS}' -p 127.0.0.1:${PORT}:${PORT} 'matrx-seo:${VERSION}'\""

echo "==> [6/6] health checks"
HEALTH=""
for _ in $(seq 1 20); do
  HEALTH="$(ssh "${HOST}" "curl -sf -m 5 http://127.0.0.1:${PORT}/health" 2>/dev/null || true)"
  [ -n "${HEALTH}" ] && break
  sleep 2
done
if [ -z "${HEALTH}" ]; then
  echo "ERROR: health never came up on the box. Logs: ssh ${HOST} 'sudo docker logs --tail 50 matrx-seo'"
  echo "       Roll back: ./deploy.sh <previous-version>"
  exit 1
fi
echo "    box health: ${HEALTH}"

# Readiness proves the BOUNDARY: the service booted only because it connected
# as svc_seo and the encryption key round-tripped. A 503 here means a boot gate
# refused — read the body, it names the failed component.
READY="$(ssh "${HOST}" "curl -s -m 10 http://127.0.0.1:${PORT}/health/ready" 2>/dev/null || true)"
echo "    box readiness: ${READY}"
case "${READY}" in
  *'"service_role": true'*|*'"service_role":true'*) echo "    boundary OK: connected as svc_seo" ;;
  *) echo "ERROR: readiness does not confirm the svc_seo boundary — ABORTING the rollout check."
     echo "       Logs: ssh ${HOST} 'sudo docker logs --tail 50 matrx-seo'"
     exit 1 ;;
esac

PUBLIC_HEALTH="$(curl -sf -m 10 "${PUBLIC_BASE}/health")"
echo "    public health: ${PUBLIC_HEALTH}"
case "${PUBLIC_HEALTH}" in
  *'"version":"'"${VERSION}"'"'*) echo "    public version OK: ${VERSION}" ;;
  *'"version":'*) echo "ERROR: public health reports a different matrx-seo version than ${VERSION}."
     exit 1 ;;
  *) echo "    public version field unavailable in this pre-versioned release; verifying its route contract" ;;
esac

PUBLIC_OPENAPI="$(curl -sf -m 10 "${PUBLIC_BASE}/openapi.json")"
case "${PUBLIC_OPENAPI}" in
  *'"/providers/dataforseo/operations"'*) echo "    DataForSEO catalog route OK" ;;
  *) echo "ERROR: public OpenAPI is missing /providers/dataforseo/operations."
     echo "       The deployment is not serving the expected package contract."
     exit 1 ;;
esac
case "${PUBLIC_OPENAPI}" in
  *'"/sites/{site_id}/backlinks/refresh"'*) echo "    site backlink refresh route OK" ;;
  *) echo "ERROR: public OpenAPI is missing /sites/{site_id}/backlinks/refresh."
     echo "       The deployment is not serving the expected backlink contract."
     exit 1 ;;
esac

IFS=',' read -r -a CORS_ORIGINS <<<"${PRODUCTION_CORS_ORIGINS}"
for origin in "${CORS_ORIGINS[@]}"; do
  CORS_HEADERS="$(curl -sS -m 10 -D - -o /dev/null -X OPTIONS \
    -H "Origin: ${origin}" \
    -H 'Access-Control-Request-Method: GET' \
    -H 'Access-Control-Request-Headers: authorization' \
    "${PUBLIC_BASE}/providers/dataforseo/operations")"
  if ! grep -Fqi "access-control-allow-origin: ${origin}" <<<"${CORS_HEADERS}"; then
    echo "ERROR: public DataForSEO CORS preflight did not allow ${origin}."
    exit 1
  fi
  echo "    hosted frontend CORS OK: ${origin}"
done

ANON="$(curl -s -m 10 -o /dev/null -w '%{http_code}' "${PUBLIC_BASE}/collections?organization_id=00000000-0000-0000-0000-000000000000")"
echo "    anon /collections -> HTTP ${ANON} (expect 401)"
if [ "${ANON}" != "401" ]; then
  echo "ERROR: anonymous collection boundary returned HTTP ${ANON}, expected 401."
  exit 1
fi

echo "DONE: matrx-seo ${VERSION} is live at ${PUBLIC_BASE}. Rollback = ./deploy.sh <previous-version>"
