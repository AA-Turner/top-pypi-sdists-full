#!/bin/bash
set -e
source pypi_build/py_versions.sh

rm wheels/* || true

sdist="--sdist"

for pyver in $PYVERS
do
  podman exec -w /workspace/dttlib dttlib uv build $sdist --wheel --python=$pyver --out-dir wheels
  sdist=""
done

