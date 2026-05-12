"""
"""

from ..config import Config


default_gpu_size: 'api.GPUSize | None' = None


if Config.zero_gpu:

    from . import api
    from . import client
    from . import config
    from . import decorator
    from . import gradio
    from . import torch

    if torch.is_in_bad_fork():
        raise RuntimeError(
            "CUDA has been initialized before importing the `spaces` package. "
            "Try importing `spaces` before any other CUDA-related package."
        )

    def startup():
        global default_gpu_size
        zerogpu_config = config.get_config()
        total_size = torch.pack()
        threshold = zerogpu_config['xlarge_threshold']
        if threshold is not None and total_size > threshold:
            default_gpu_size = 'xlarge' # pragma: no cover
        if len(decorator.decorated_cache) == 0:
            return # pragma: no cover
        client.startup_report()

    torch.patch()
    gradio.one_launch(startup)
