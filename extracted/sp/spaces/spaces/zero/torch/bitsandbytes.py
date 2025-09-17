"""
"""
# pyright: reportPrivateImportUsage=false

from __future__ import annotations

from contextlib import contextmanager
from importlib import metadata
from types import ModuleType

from packaging import version


@contextmanager
def cuda_unavailable(torch: ModuleType): # pragma: no cover
    _is_available = torch.cuda.is_available
    torch.cuda.is_available = lambda: False
    try:
        yield
    finally:
        torch.cuda.is_available = _is_available


def maybe_import_bitsandbytes():
    try:
        import torch
    except ImportError: # pragma: no cover
        return None
    try:
        bnb_version = version.parse(metadata.version('bitsandbytes'))
    except ImportError: # pragma: no cover
        return None
    if bnb_version < version.parse('0.46.0'): # pragma: no cover
        print(f"ZeroGPU highly recommends bitsandbytes > `0.46.0` (`{bnb_version}` installed). Falling back to legacy support")
        return bnb_version
    with cuda_unavailable(torch):
        try:
            import bitsandbytes
        except ImportError:
            return None
        print("↑ Those bitsandbytes warnings are expected on ZeroGPU ↑")
    return bnb_version


if (bnb_version := maybe_import_bitsandbytes()) is not None and bnb_version > version.parse('0.46.0'):

    def _patch():
        pass

    def _unpatch():
        pass

    def _move():
        import bitsandbytes as bnb
        from bitsandbytes import cextension
        from bitsandbytes.backends.cuda import ops
        bnb.cuda_ops = ops
        cextension.lib._lib = cextension.get_native_library()._lib

elif bnb_version is not None: # pragma: no cover

    from . import bitsandbytes_legacy

    _patch = bitsandbytes_legacy.patch
    _unpatch = bitsandbytes_legacy.unpatch
    _move = bitsandbytes_legacy.move

else:

    _patch = lambda: None
    _unpatch = lambda: None
    _move = lambda: None


patch = _patch
unpatch = _unpatch
move = _move
