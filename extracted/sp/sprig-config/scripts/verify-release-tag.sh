#!/bin/sh
set -eu

if [ -z "${CI_COMMIT_TAG:-}" ]; then
    echo "CI_COMMIT_TAG is not set."
    exit 1
fi

echo "🔍 Checking release tag against pyproject.toml..."
PYPROJECT_VERSION="$(poetry version -s)"
TAG_VERSION="$(printf '%s' "${CI_COMMIT_TAG}" | sed -E 's/^[Vv]//')"
NORMALIZED_PYPROJECT_VERSION="$(printf '%s' "${PYPROJECT_VERSION}" | tr '[:upper:]' '[:lower:]')"
NORMALIZED_TAG_VERSION="$(printf '%s' "${TAG_VERSION}" | tr '[:upper:]' '[:lower:]')"

echo "📦 pyproject.toml version: ${PYPROJECT_VERSION}"
echo "🏷️ Git tag: ${CI_COMMIT_TAG}"

if [ "${NORMALIZED_PYPROJECT_VERSION}" != "${NORMALIZED_TAG_VERSION}" ]; then
    echo "❌ Version mismatch: expected v${PYPROJECT_VERSION}, got ${CI_COMMIT_TAG}"
    exit 1
fi
