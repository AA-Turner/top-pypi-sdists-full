# SPDX-License-Identifier: BSD-2-Clause

# Copyright (c) 2025 Phil Thompson <phil@riverbankcomputing.com>


import glob

from setuptools import Extension, setup


# Build the extension module.
module_src = sorted(glob.glob('*.c'))

module = Extension('PyQt5.sip', module_src)

# Do the setup.
setup(
        name='PyQt5_sip',
        version='12.17.0',
        license='BSD-2-Clause',
        python_requires='>=3.9',
        ext_modules=[module]
     )
