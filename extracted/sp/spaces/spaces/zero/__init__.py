"""
"""

from ..config import Config


if Config.zero_gpu:

    from . import client
    from . import decorator
    from . import gradio
    from . import torch
    from . import utils

    if torch.is_in_bad_fork():
        raise RuntimeError(
            "CUDA has been initialized before importing the `spaces` package. "
            "Try importing `spaces` before any other CUDA-related package."
        )

    def startup():
        torch.pack()
        if len(decorator.decorated_cache) == 0:
            return # pragma: no cover
        client.startup_report()

    torch.patch()
    gradio.one_launch(startup)
