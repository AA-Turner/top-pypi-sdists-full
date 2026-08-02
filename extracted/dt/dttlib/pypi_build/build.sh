#!/bin/sh
set -e -x
cd /build

sdist=$1

source /opt/conda/bin/activate
#eval $(conda shell.bash hook)
conda activate dttbuild
export LIBCLANG_PATH=$CONDA_PREFIX/lib
export C_INCLUDE_PATH=$CONDA_PREFIX/include
export CPLUS_INCLUDE_PATH=$CONDA_PREFIX/include

maturin build $sdist --target-dir pypi_build/target_pypi --out wheels --release  --interpreter "python${pyver}" --features python,python-pipe,nds,pyo3/extension-module