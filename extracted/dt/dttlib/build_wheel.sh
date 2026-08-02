#!/bin/bash
# build wheel file in a container
# pass it a python version

pyver=$1

export CARGO_TARGET_DIR=target_wheel
uv build --wheel --python=$pyver --out-dir wheels
