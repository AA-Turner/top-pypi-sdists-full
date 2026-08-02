#!/bin/bash

source ~/.bashrc
source ../ndscope/.venv_bullseye/bin/activate
source ~/fakeroot_bullseye/fakeroot.sh
maturin $1 --features all --target-dir target_bullseye --release
