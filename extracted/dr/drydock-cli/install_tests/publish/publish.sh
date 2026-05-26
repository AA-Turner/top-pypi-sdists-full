#!/usr/bin/env bash
# Build + push the public drydock-cli image to Docker Hub.
#
# Auth: Set DOCKER_HUB_USERNAME + DOCKER_HUB_PASSWORD env vars
# (or use an existing `docker login` session). The script uses
# --password-stdin so credentials never appear in process listings,
# shell history, or command-line argv.
#
# Usage:
#   DOCKER_HUB_USERNAME=fbobe3 \
#   DOCKER_HUB_PASSWORD=... \
#       ./publish.sh                   # publishes :latest + :<pypi version>
#
#   ./publish.sh --version 2.8.85      # publish a specific pinned version
#   ./publish.sh --dry-run             # build but don't push
#
set -euo pipefail
cd "$(dirname "$0")"

REPO="${REPO:-fbobe3/drydock}"
DRYDOCK_VERSION=""
DRY_RUN=""

while [ $# -gt 0 ]; do
    case "$1" in
        --version) DRYDOCK_VERSION="$2"; shift 2 ;;
        --dry-run) DRY_RUN=1; shift ;;
        --help)
            sed -n '/^# /,/^$/p' "$0" | sed 's/^# \?//'
            exit 0 ;;
        *) echo "unknown arg: $1" >&2; exit 1 ;;
    esac
done

# Auto-detect latest drydock-cli version from PyPI if not pinned
if [ -z "$DRYDOCK_VERSION" ]; then
    DRYDOCK_VERSION=$(pip index versions drydock-cli 2>&1 \
        | grep -m1 'drydock-cli' \
        | sed -E 's/^drydock-cli \(([^)]+)\).*/\1/')
    if [ -z "$DRYDOCK_VERSION" ]; then
        echo "Could not auto-detect drydock-cli version" >&2
        exit 1
    fi
fi
echo "Building drydock image for version: ${DRYDOCK_VERSION}"

# Login if credentials provided (skip if already logged in)
if [ -n "${DOCKER_HUB_PASSWORD:-}" ] && [ -n "${DOCKER_HUB_USERNAME:-}" ]; then
    echo "Logging into Docker Hub as ${DOCKER_HUB_USERNAME}..."
    echo "${DOCKER_HUB_PASSWORD}" | docker login -u "${DOCKER_HUB_USERNAME}" --password-stdin
    unset DOCKER_HUB_PASSWORD
fi

VERSIONED_TAG="${REPO}:${DRYDOCK_VERSION}"
LATEST_TAG="${REPO}:latest"

echo
echo "=== building ${VERSIONED_TAG} ==="
docker build \
    --build-arg "DRYDOCK_VERSION=${DRYDOCK_VERSION}" \
    -t "${VERSIONED_TAG}" \
    -t "${LATEST_TAG}" \
    .

if [ -n "${DRY_RUN}" ]; then
    echo
    echo "=== dry run — not pushing ==="
    docker image ls "${REPO}"
    exit 0
fi

echo
echo "=== pushing ${VERSIONED_TAG} ==="
docker push "${VERSIONED_TAG}"
echo "=== pushing ${LATEST_TAG} ==="
docker push "${LATEST_TAG}"

echo
echo "=== published ==="
echo "  ${VERSIONED_TAG}"
echo "  ${LATEST_TAG}"
echo
echo "Pull from another host:"
echo "  docker pull ${LATEST_TAG}"
