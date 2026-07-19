#!/bin/sh

export PREFIX=""
if [ -d 'venv' ] ; then
    export PREFIX="venv/bin/"
fi

set -ex

${PREFIX}pytest tests/unit tests/functional
