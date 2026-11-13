"""
"""

import shutil
from pathlib import Path

from ..config import Config
from .api import GPUSize


BAD_FORK_EXCEPTION_MESSAGE = (
    "CUDA has been initialized before importing the `spaces` package. "
    "Try importing `spaces` before any other CUDA-related package."
)


_zerogpu_mode_enabled = False
_default_gpu_size: GPUSize | None = None


def zerogpu_mode_enable():
    global _zerogpu_mode_enabled
    from . import torch
    if torch.is_in_bad_fork():
        raise RuntimeError(BAD_FORK_EXCEPTION_MESSAGE)
    torch.patch()
    shutil.rmtree(Config.zerogpu_offload_dir, ignore_errors=True)
    Path(Config.zerogpu_offload_dir).mkdir(parents=True)
    _zerogpu_mode_enabled = True


def zerogpu_mode_enabled():
    return _zerogpu_mode_enabled


def zerogpu_startup():
    global _default_gpu_size
    from . import client
    from . import config
    from . import torch
    zerogpu_config = config.get_config()
    total_size = torch.pack()
    threshold = zerogpu_config['xlarge_threshold']
    if threshold is not None and total_size > threshold:
        _default_gpu_size = 'xlarge' # pragma: no cover
    client.startup_report()


def default_gpu_size():
    return _default_gpu_size
