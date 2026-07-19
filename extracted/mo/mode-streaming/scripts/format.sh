#!/bin/sh -e

set -x

ruff format mode tests
ruff check mode tests --fix
