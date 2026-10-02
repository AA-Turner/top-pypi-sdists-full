"""bitHuman platform guard — this source distribution exists to REFUSE.

`bithuman` ships pre-compiled wheels. It is a pybind11 binding over a C++
engine (ONNX Runtime, HDF5, FFmpeg, a Rust staticlib) and there is no
from-source path a `pip install` can take. Before this file existed, a
platform with no matching wheel got no error at all: pip walked backwards
through the release history until some old wheel matched its tags and
installed that, silently. This module turns that silence into the message
below.
"""
import platform
import sys

_SUPPORTED = ['Linux x86_64      (manylinux_2_28_x86_64)', 'Linux aarch64     (manylinux_2_28_aarch64)', 'macOS 14+ arm64   (macosx_14_0_arm64, Apple Silicon)']
_VERSION = '2.11.20'

_MSG = """
================================================================================
  bithuman 2.11.20 has NO WHEEL for this platform.

    you are on : {system} / {machine} / CPython {py}
    supported  : {supported}

  This package ships pre-compiled binary wheels only. It CANNOT be built from
  source: the engine needs ONNX Runtime, HDF5, FFmpeg and a Rust toolchain
  that a `pip install` cannot assemble.

  pip has NOT installed anything, and in particular it has NOT quietly
  installed an older release of bithuman in place of this one. If you have
  seen `pip install bithuman` succeed on this machine before, check what it
  actually gave you -- before this guard existed it would resolve a wheel
  from months earlier without printing a word.

  What to do:
    * Linux (x86_64 or aarch64) and Apple Silicon macOS 14+ are supported
      today -- `pip install bithuman` works there with no extra flags.
    * Windows: run it under WSL2 (Ubuntu 22.04+), which is a supported Linux.
    * Intel Macs are not supported.
    * Questions, or you need a platform that is not listed: hello@bithuman.ai
================================================================================
"""


def _refuse(*_args, **_kwargs):
    msg = _MSG.format(
        system=platform.system() or "unknown",
        machine=platform.machine() or "unknown",
        py=platform.python_version(),
        supported="\n                 ".join(_SUPPORTED),
    )
    sys.stderr.write(msg)
    sys.stderr.flush()
    raise SystemExit(msg)


# Every PEP 517 hook pip can call on the way to metadata or a wheel.
def get_requires_for_build_wheel(config_settings=None):
    _refuse()


def prepare_metadata_for_build_wheel(metadata_directory, config_settings=None):
    _refuse()


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    _refuse()


def get_requires_for_build_sdist(config_settings=None):
    _refuse()


def build_sdist(sdist_directory, config_settings=None):
    _refuse()


# PEP 660 (pip install -e).
def build_editable(wheel_directory, config_settings=None, metadata_directory=None):
    _refuse()


def get_requires_for_build_editable(config_settings=None):
    _refuse()


def prepare_metadata_for_build_editable(metadata_directory, config_settings=None):
    _refuse()
