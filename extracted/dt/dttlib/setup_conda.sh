# source this file to setup build system
#!/usr/bin/env bash

if [[ "$(basename -- "$0")" == "setup.sh" ]]; then
    >&2 echo "ERROR: Don't run $0, source it, to setup the dev environment. Ex 'source $0'"
    exit 1
fi

mamba activate dttbuild

export LIBCLANG_PATH=$CONDA_PREFIX/lib
export C_INCLUDE_PATH=$CONDA_PREFIX/include
export CPLUS_INCLUDE_PATH=$CONDA_PREFIX/include

