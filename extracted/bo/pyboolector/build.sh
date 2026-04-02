#!/usr/bin/env bash
set -e -o pipefail

log() { echo "[INFO] $*"; }

# Enable xtrace for easier debugging of failures
set -x

log "Creating /build and entering it"
mkdir -p /build
cd /build

log "Start PyPI build.sh"

BUILD_DIR=`pwd`
N_CORES=`nproc`

test -n "$PYTHON_VERSIONS" || { echo PYTHON_VERSIONS must be set.; exit 1; }
log "PYTHON_VERSIONS=$PYTHON_VERSIONS"

cp -r /boolector .

# Setup dependencies
cd boolector
log "Running contrib/setup-btor2tools.sh"
/bin/bash -x ./contrib/setup-btor2tools.sh
log "Running contrib/setup-cadical.sh"
/bin/bash -x ./contrib/setup-cadical.sh
log "Running contrib/setup-lingeling.sh"
/bin/bash -x ./contrib/setup-lingeling.sh

#********************************************************************
#* boolector
#********************************************************************
cd ${BUILD_DIR}

cd boolector

log "Configuring Boolector"
./configure.sh --shared --prefix /usr

cd build

log "Building Boolector with ${N_CORES} cores"
make -j${N_CORES}

log "Installing Boolector"
make install

#********************************************************************
#* pyboolector
#********************************************************************

cd ${BUILD_DIR}
rm -rf pyboolector

# Specify path to CmakeLists.txt so setup.py can extract the version
export CMAKELISTS_TXT=/boolector/CMakeLists.txt

log "Copying Python package template"
cp -r /boolector/pypi pyboolector

# Prepare the artifact directory.
log "Preparing artifact directory at /boolector/result"
rm -rf /boolector/result
mkdir -p /boolector/result

# Grab the main license file
log "Copying license file"
cp /boolector/COPYING pyboolector/LICENSE

log "Entering pyboolector directory"
cd pyboolector

for py in $PYTHON_VERSIONS; do
  python=/opt/python/${py}-${py}/bin/python
  log "Building for ABI ${py} using interpreter ${python}"
  log "Installing Python build dependencies"
  ${python} -m pip install cython wheel setuptools
  cd ${BUILD_DIR}/pyboolector
  rm -rf src
  log "Copying Python bindings and headers"
  cp -r ${BUILD_DIR}/boolector/src/api/python src
  sed -i -e 's/override//g' \
     -e 's/noexcept/_GLIBCXX_USE_NOEXCEPT/g' \
     -e 's/\(BoolectorException (const.*\)/\1\n    virtual ~BoolectorException() _GLIBCXX_USE_NOEXCEPT {}/' \
       src/pyboolector_abort.cpp
  mkdir -p src/utils
  cp ${BUILD_DIR}/boolector/src/*.h src
  cp ${BUILD_DIR}/boolector/src/utils/*.h src/utils
  log "Generating enums with $python"
  $python ./src/mkenums.py ./src/btortypes.h ./src/pyboolector_enums.pxd
  cat src/pyboolector_enums.pxd
  log "Building sdist and wheel with $python"
  $python setup.py sdist bdist_wheel
done

# Copy the source distribution into the artifact directory.
log "Copying source distributions to /boolector/result"
cp dist/*.tar.gz /boolector/result

# Repair wheels and place them into the artifact directory.
log "Repairing wheels with auditwheel"
for whl in dist/*.whl; do
  log "auditwheel repair $whl"
  auditwheel repair --wheel-dir /boolector/result/dist $whl
done
