#!/bin/bash

set -x -e

PYVER=$1

source /opt/conda/etc/profile.d/conda.sh
conda activate dttbuild
micromamba install --yes python==$PYVER