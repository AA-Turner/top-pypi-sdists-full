#!/bin/bash
set -e

# Upload to PyPI using API token
# Usage: ./scripts/upload-to-pypi.sh
#
# Requires: PYPI_API_TOKEN environment variable

if [ -z "$PYPI_API_TOKEN" ]; then
    echo "Error: PYPI_API_TOKEN environment variable is not set"
    exit 1
fi

VERSION=$(poetry version -s)
WHEEL="dist/sprig_config-${VERSION}-py3-none-any.whl"
SDIST="dist/sprig_config-${VERSION}.tar.gz"

echo "Building distribution..."
poetry build

echo "Uploading to PyPI..."
poetry run twine upload -u __token__ -p "$PYPI_API_TOKEN" "$WHEEL" "$SDIST"

echo "Upload complete!"
