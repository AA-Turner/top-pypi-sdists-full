#!/bin/sh
set -eu

BASE_VERSION="$(poetry version -s)"
PIPELINE_NUMBER="${CI_PIPELINE_IID:-${CI_PIPELINE_ID:-}}"

if [ -z "${PIPELINE_NUMBER}" ]; then
    echo "CI_PIPELINE_IID or CI_PIPELINE_ID must be set for TestPyPI branch publishes."
    exit 1
fi

case "${BASE_VERSION}" in
    *.dev*)
        echo "Base version ${BASE_VERSION} already includes a .dev suffix; refusing to stack another dev release."
        exit 1
        ;;
esac

TESTPYPI_VERSION="${BASE_VERSION}.dev${PIPELINE_NUMBER}"

echo "🔧 Preparing TestPyPI version from base version ${BASE_VERSION}..."
poetry version "${TESTPYPI_VERSION}" >/dev/null
echo "📦 TestPyPI version: $(poetry version -s)"
