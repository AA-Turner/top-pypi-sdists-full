#!/usr/bin/env python3
# Copyright 2021 Quansight, LLC
# Copyright 2021 Filipe Laíns
# Copyright 2022 Collabora Ltd.
# SPDX-License-Identifier: MIT

# Generate a PKG-INFO file using a very small subset of meson-python.

import sys
from pathlib import Path

import pyproject_metadata
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

if __name__ == '__main__':
    top_srcdir = Path(__file__).parent.parent

    with open(top_srcdir / 'pyproject.toml') as reader:
        conf = tomllib.loads(reader.read())

    meta = pyproject_metadata.StandardMetadata.from_pyproject(conf, top_srcdir)
    meta.version = sys.argv[1]
    core_metadata = meta.as_rfc822()

    with open(sys.argv[2], 'wb') as writer:
        writer.write(bytes(core_metadata))
