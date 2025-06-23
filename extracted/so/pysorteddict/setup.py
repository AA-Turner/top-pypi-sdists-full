import glob
import os
import sysconfig

import setuptools

# MSVC supports designated initialisers only in C++20.
cxx_standard_arg = "-std=c++14" if os.name != "nt" or sysconfig.get_platform().startswith("mingw") else "/std:c++20"

setuptools.setup(
    ext_modules=[
        setuptools.Extension("pysorteddict", glob.glob("src/pysorteddict/*.cc"), extra_compile_args=[cxx_standard_arg])
    ],
    include_package_data=False,
)
