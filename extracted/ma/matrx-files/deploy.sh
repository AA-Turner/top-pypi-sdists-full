#!/usr/bin/env bash
# Deploy matrx-files to the live EC2 box behind https://files.matrxserver.com
#
#   ./deploy.sh 0.1.4        # deploy a version (must already be on PyPI)
#   ./deploy.sh 0.1.3        # rolling back is the same command
#
# What it does, in order — and it REFUSES to touch the live container until
# the new image is proven:
#   1. checks PyPI actually has the version (tag push publishes it)
#   2. syncs THIS directory's canonical Dockerfile to the box (kills drift —
#      a hand-edited on-box Dockerfile once ignored the version pin)
#   3. builds matrx-files:<version> on the box
#   4. asserts the built image really contains <version> (aborts otherwise,
#      live container untouched)
#   5. swaps the container (rm + run — NEVER docker restart: --env-file is
#      read only at run time)
#   6. health-checks locally and through Cloudflare
#
# Requires: `ssh matrx-sandbox` working (SSM per ~/.ssh/config; run
# `aws sso login --profile AdministratorAccess-872515272894` first if stale).
set -euo pipefail

VERSION="${1:?usage: deploy.sh <version, e.g. 0.1.4>}"
HOST="${MATRX_FILES_HOST:-matrx-sandbox}"
PUBLIC_BASE="https://files.matrxserver.com"
DIR="$(cd "$(dirname "$0")" && pwd)"

echo "==> [1/6] checking PyPI has matrx-files==${VERSION}"
if ! curl -sf -m 15 "https://pypi.org/pypi/matrx-files/${VERSION}/json" >/dev/null; then
  echo "ERROR: matrx-files==${VERSION} is not on PyPI."
  echo "       Publish first: cd aidream && git tag matrx-files/v${VERSION} && git push origin refs/tags/matrx-files/v${VERSION}"
  exit 1
fi

echo "==> [2/6] syncing canonical Dockerfile to ${HOST}:/opt/matrx-files/"
scp -q "${DIR}/Dockerfile" "${HOST}:/tmp/matrx-files.Dockerfile"
ssh "${HOST}" 'sudo mv /tmp/matrx-files.Dockerfile /opt/matrx-files/Dockerfile'

echo "==> [3/6] building matrx-files:${VERSION} on ${HOST}"
ssh "${HOST}" "sudo docker build --build-arg MATRX_FILES_VERSION='==${VERSION}' -t 'matrx-files:${VERSION}' /opt/matrx-files"

echo "==> [4/6] verifying the image really contains ${VERSION}"
GOT="$(ssh "${HOST}" "sudo docker run --rm --entrypoint python 'matrx-files:${VERSION}' -c 'import importlib.metadata as m; print(m.version(\"matrx-files\"))'" | tr -d '[:space:]')"
if [ "${GOT}" != "${VERSION}" ]; then
  echo "ERROR: built image contains matrx-files ${GOT}, expected ${VERSION} — ABORTING; live container untouched."
  exit 1
fi
echo "    image verified: ${GOT}"

# Run the helper FROM THE INSTALLED IMAGE, using the same config as the
# candidate/live/rollback container. Missing/old helper, missing policy,
# failed DB readiness or central refusal contracts abort before rm -f.
echo "==> preflight installed source-aware policy and authority contracts"
ssh "${HOST}" "sudo docker run --rm --env-file /etc/matrx-files.env -v /data/matrx-files:/data/matrx-files --entrypoint python 'matrx-files:${VERSION}' -m matrx_files.standalone.preflight"

echo "==> [5/6] swapping the live container (rm + run)"
# The container's json-file log dies with it, so copy it to the host first
# (best-effort: never blocks the swap), and keep 10 x 50 MB per run. Same
# commands as the Ship Manager's msRemoveContainer / msDockerRunImage.
ssh "${HOST}" "{ sudo mkdir -p /var/log/matrx-files && sudo sh -c \"docker logs --timestamps matrx-files > /var/log/matrx-files/\$(date -u +%Y%m%dT%H%M%SZ).log 2>&1\" && sudo find /var/log/matrx-files -name '*.log' -mtime +30 -delete; } >/dev/null 2>&1 || true; sudo docker rm -f matrx-files >/dev/null 2>&1 || true; sudo docker run -d --name matrx-files --restart unless-stopped --log-driver json-file --log-opt max-size=50m --log-opt max-file=10 --env-file /etc/matrx-files.env -p 127.0.0.1:8080:8080 -v /data/matrx-files:/data/matrx-files 'matrx-files:${VERSION}'"

echo "==> [6/6] health checks"
HEALTH=""
for _ in $(seq 1 20); do
  HEALTH="$(ssh "${HOST}" 'curl -sf -m 5 http://127.0.0.1:8080/files-service/health' 2>/dev/null || true)"
  [ -n "${HEALTH}" ] && break
  sleep 2
done
if [ -z "${HEALTH}" ]; then
  echo "ERROR: health never came up on the box. Logs: ssh ${HOST} 'sudo docker logs --tail 50 matrx-files'"
  echo "       Roll back: ./deploy.sh <previous-version>"
  exit 1
fi
echo "    box health:    ${HEALTH}"
echo "    public health: $(curl -sf -m 10 "${PUBLIC_BASE}/files-service/health")"
ANON="$(curl -s -m 10 -o /dev/null -w '%{http_code}' "${PUBLIC_BASE}/files/00000000-0000-0000-0000-000000000000")"
echo "    anon /files/{id} -> HTTP ${ANON} (expect 401)"

CORS_HEADERS="$(mktemp)"
trap 'rm -f "${CORS_HEADERS}"' EXIT
CORS_STATUS="$(curl -sS -m 10 -o /dev/null -D "${CORS_HEADERS}" -w '%{http_code}' \
  -X OPTIONS "${PUBLIC_BASE}/files/upload" \
  -H 'Origin: http://localhost:3000' \
  -H 'Access-Control-Request-Method: POST' \
  -H 'Access-Control-Request-Headers: authorization,content-type,x-request-id,x-idempotency-key,x-guest-fingerprint,x-cloud-files-bypass')"
CORS_ORIGIN="$(awk 'BEGIN { IGNORECASE=1 } /^access-control-allow-origin:/ { sub(/\r$/, "", $2); print $2 }' "${CORS_HEADERS}")"
if [ "${CORS_STATUS}" != "200" ] || [ "${CORS_ORIGIN}" != "http://localhost:3000" ]; then
  echo "ERROR: public CORS preflight failed: HTTP ${CORS_STATUS}, ACAO='${CORS_ORIGIN:-missing}'."
  echo "       Roll back: ./deploy.sh <previous-version>"
  exit 1
fi
echo "    CORS preflight: HTTP ${CORS_STATUS}, ACAO=${CORS_ORIGIN}"

echo "DONE: matrx-files ${VERSION} is live at ${PUBLIC_BASE}. Rollback = ./deploy.sh <previous-version>"
