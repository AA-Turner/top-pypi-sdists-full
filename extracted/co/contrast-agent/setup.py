# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys
import platform
import time
from os import environ, path
from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext
from setuptools.command.install_lib import install_lib

UNSUPPORTED_PYTHON = (3, 15) if environ.get("CONTRAST_ALLOW_PY314") else (3, 14)

root_dir = path.abspath(path.dirname(__file__))


def read(*parts):
    with open(path.join(root_dir, *parts), encoding="utf-8") as f:
        return f.read()


def is_arm():
    machine = platform.machine()
    return "arm" in machine or "aarch" in machine


version_specifier = sys.version_info[:2]
if not version_specifier < UNSUPPORTED_PYTHON:
    raise RuntimeError(
        "Fatal: Cannot install contrast-agent: Unsupported python version "
        f"({platform.python_version()})"
    )

extension_path = path.join("contrast", "assess_extensions")
extension_source_dir = path.join("src", extension_path)
common_dir = path.join(extension_source_dir, "common")

if sys.platform.startswith("darwin"):
    link_args = ["-rpath", "@loader_path"]
    platform_args = []
else:
    platform_args = ["-Wno-cast-function-type"]
    link_args = []

debug = environ.get("ASSESS_DEBUG")
debug_args = ["-g", "-O1"] if debug else []
macros = [("ASSESS_DEBUG", "1")] if debug else []
macros.append(("EXTENSION_BUILD_TIME", f'"{time.ctime()}"'))

strict_build_args = ["-Werror"] if environ.get("CONTRAST_STRICT_BUILD") else []

c_sources = [
    path.join(common_dir, name)
    for name in [
        "patches.c",
        "scope.c",
        "logging.c",
        "intern.c",
        "propagate.c",
        "repr.c",
        "repeat.c",
        "streams.c",
        "subscript.c",
        "cast.c",
        "cs_str.c",
    ]
]
libraries = []


extensions = [
    Extension(
        "contrast.assess_extensions.cs_str",
        c_sources,
        libraries=libraries,
        include_dirs=[
            extension_source_dir,
            path.join(extension_source_dir, "include"),
        ],
        library_dirs=[extension_source_dir],
        # Path relative to the .so itself (works for gnu-ld)
        runtime_library_dirs=["$ORIGIN"],
        extra_compile_args=[
            "-Wall",
            "-Wextra",
            "-Wno-unused-parameter",
            "-Wmissing-field-initializers",
        ]
        + strict_build_args
        + debug_args
        + platform_args,
        extra_link_args=link_args,
        define_macros=macros,
    )
]


class ContrastBuildExt(build_ext):
    def run(self):
        build_ext.run(self)


class ContrastInstallLib(install_lib):
    def run(self):
        install_lib.run(self)


setup(
    cmdclass=dict(build_ext=ContrastBuildExt, install_lib=ContrastInstallLib),
    ext_modules=extensions,
)
