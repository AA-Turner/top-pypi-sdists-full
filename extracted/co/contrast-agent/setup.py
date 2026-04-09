# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

import platform
import sys
import time
from os import environ, path

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext
from setuptools.command.install_lib import install_lib

UNSUPPORTED_PYTHON = (3, 15)

root_dir = path.abspath(path.dirname(__file__))


def read(*parts):
    with open(path.join(root_dir, *parts), encoding="utf-8") as f:
        return f.read()


def is_arm():
    machine = platform.machine()
    return "arm" in machine or "aarch" in machine


is_windows = sys.platform == "win32"

version_specifier = sys.version_info[:2]
if not version_specifier < UNSUPPORTED_PYTHON:
    raise RuntimeError(
        "Fatal: Cannot install contrast-agent: Unsupported python version "
        f"({platform.python_version()})"
    )

if is_windows and not environ.get("CONTRAST_ALLOW_WINDOWS"):
    raise RuntimeError(
        f"Fatal: Cannot install contrast-agent: Unsupported platform {sys.platform}"
    )

extensions_dir = path.join("src", "contrast", "extensions")

debug = environ.get("ASSESS_DEBUG")
macros: list[tuple[str, str | None]] = [("ASSESS_DEBUG", "1")] if debug else []
macros.append(("EXTENSION_BUILD_TIME", f'"{time.ctime()}"'))

if is_windows:
    # https://learn.microsoft.com/en-us/cpp/build/reference/compiler-options-listed-by-category
    extra_link_args = []
    platform_args = []
    compile_args = ["/W3"]
    debug_args = ["/Z7", "/Od"] if debug else []
    strict_build_args = ["/WX"] if environ.get("CONTRAST_STRICT_BUILD") else []
    runtime_lib_dirs = []
else:
    is_darwin = sys.platform.startswith("darwin")
    extra_link_args = ["-rpath", "@loader_path"] if is_darwin else []
    platform_args = [] if is_darwin else ["-Wno-cast-function-type"]
    compile_args = [
        "-Wall",
        "-Wextra",
        "-Wno-unused-parameter",
        "-Wmissing-field-initializers",
    ]
    debug_args = ["-g", "-O1"] if debug else []
    strict_build_args = ["-Werror"] if environ.get("CONTRAST_STRICT_BUILD") else []
    runtime_lib_dirs = ["$ORIGIN"]

c_sources = [
    path.join(extensions_dir, "common", name)
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
        "_c_ext.c",
    ]
]

extensions = [
    Extension(
        "contrast.extensions._c_ext",
        c_sources,
        include_dirs=[
            extensions_dir,
            path.join(extensions_dir, "include"),
        ],
        library_dirs=[extensions_dir],
        runtime_library_dirs=runtime_lib_dirs,
        extra_compile_args=compile_args
        + strict_build_args
        + debug_args
        + platform_args,
        extra_link_args=extra_link_args,
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
