"""
"""

import shutil

from pathlib import Path

from .. import utils
from ..config import Config


if Config.zero_gpu:

    from . import client
    from . import decorator
    from . import gradio
    from . import torch

    if torch.is_in_bad_fork():
        raise RuntimeError(
            "CUDA has been initialized before importing the `spaces` package"
        )

    def startup():
        total_size = torch.pack()
        if len(decorator.decorated_cache) == 0:
            return # pragma: no cover
        if Config.zerogpu_size == 'auto':
            gpu_size = 'medium' if total_size < Config.zerogpu_medium_size_threshold else 'large'
        else:
            gpu_size = Config.zerogpu_size
        client.startup_report(utils.self_cgroup_device_path(), gpu_size)

    torch.patch()
    gradio.one_launch(startup)

    # Cleanup offload directory
    shutil.rmtree(Config.zerogpu_offload_dir, ignore_errors=True)
    Path(Config.zerogpu_offload_dir).mkdir(parents=True)
