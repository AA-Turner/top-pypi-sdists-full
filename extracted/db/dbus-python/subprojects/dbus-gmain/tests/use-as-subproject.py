#!/usr/bin/env python3
# Copyright 2022 Collabora Ltd.
# SPDX-License-Identifier: MIT

import os
import shutil
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    if shutil.which('meson') is None:
        print('SKIP: meson not found in PATH')
        raise SystemExit(0)

    with tempfile.TemporaryDirectory() as temp:
        shutil.copytree(
            os.path.join(HERE, 'use-as-subproject'),
            os.path.join(temp, 'src'),
        )
        os.makedirs(os.path.join(temp, 'src', 'subprojects'), exist_ok=True)
        os.symlink(
            os.path.dirname(HERE),
            os.path.join(temp, 'src', 'subprojects', 'dbus-gmain'),
        )
        subprocess.run(
            ['meson', os.path.join(temp, 'src'), os.path.join(temp, 'build')],
            check=True,
        )
        subprocess.run(
            ['meson', 'compile', '-C', os.path.join(temp, 'build')],
            check=True,
        )
