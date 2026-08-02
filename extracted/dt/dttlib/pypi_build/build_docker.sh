#!/bin/bash

PYVER=$1

docker build -t dtt-build:py${PYVER} --build-arg PYVER=${PYVER} dttbuild