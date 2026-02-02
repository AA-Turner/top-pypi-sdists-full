#!/usr/bin/python3 

import os
import sys
from setuptools import setup, find_packages, Extension
try:
    from Cython.Build import cythonize
except ImportError:
    cythonize = None


if 'sdist' in sys.argv and "CYTHONIZE" not in os.environ:
    raise Exception("Please use supplied makefile to build the package.")

# https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html#distributing-cython-modules
def no_cythonize(extensions, **_ignore):
    for extension in extensions:
        sources = []
        for sfile in extension.sources:
            path, ext = os.path.splitext(sfile)
            if ext in (".pyx", ".py"):
                if extension.language == "c++":
                    ext = ".cpp"
                else:
                    ext = ".c"
                sfile = path + ext
            sources.append(sfile)
        extension.sources[:] = sources
    return extensions


extensions = [
    Extension("wrapper", ["fatfs/wrapper.pyx", "fatfs/diskiocheck.c", "foreign/fatfs/source/ff.c", "foreign/fatfs/source/ffsystem.c", "foreign/fatfs/source/ffunicode.c"], include_dirs=["foreign/fatfs/source"]),
]

cythonize_env = bool(int(os.getenv("CYTHONIZE", 0)))

if cythonize_env and cythonize_env is None:
    raise Exception("Cython needs to be installed for CYTHONIZE=1")

CYTHONIZE = cythonize_env and cythonize is not None

if CYTHONIZE:
    compiler_directives = {"language_level": 3, "embedsignature": True}
    extensions = cythonize(extensions, compiler_directives=compiler_directives)
else:
    extensions = no_cythonize(extensions)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='fatfs-ng',
    version="0.1.15",
    author="Johann Obermeier",
    author_email="obermeier.johann@googlemail.com",
    description="Enhanced Python wrapper around ChaN's FatFS library - Fork of fatfs-python with extended features.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    ext_package='fatfs',
    ext_modules=extensions,
    url="https://github.com/Jason2866/pyfatfs",
    project_urls={
        "Original Project": "https://github.com/krakonos/fatfs-python",
        "Bug Tracker": "https://github.com/Jason2866/pyfatfs/issues",
        "Documentation": "https://github.com/Jason2866/pyfatfs",
    },
    packages=find_packages(),
    setup_requires=['cython'],
    zip_safe=False,
    python_requires='>=3.8',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Programming Language :: Cython",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Embedded Systems",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Filesystems",
    ],
    keywords="fatfs fat filesystem embedded esp32 platformio",
)
