"""
"""

from importlib import metadata

from packaging.version import Version

from ..config import Config
from .context import ZeroGPULog
from .errors import ZeroGPUClientError
from .errors import ZeroGPUError
from .errors import ZeroGPUException
from .errors import ZeroGPUIllegalDuration
from .errors import ZeroGPUPendingCreditsExceeded
from .errors import ZeroGPUQueueTimeout
from .errors import ZeroGPUQuotaExceeded
from .errors import ZeroGPUTaskAborted
from .errors import ZeroGPUTaskException
from .errors import ZeroGPUWorkerError
from .middleware import ZeroGPUMiddleware
from .lifecycle import default_gpu_size
from .lifecycle import zerogpu_mode_enable
from .lifecycle import zerogpu_mode_enabled
from .lifecycle import zerogpu_startup


def _maybe_enable_gradio_compat():
    try:
        gradio_version = metadata.version('gradio')
    except metadata.PackageNotFoundError: # pragma: no cover
        pass
    else:
        if Version(gradio_version) < Version('7.0.0.dev0'):
            from . import gradio
            gradio.patch()


if Config.zero_gpu:
    zerogpu_mode_enable()
    _maybe_enable_gradio_compat()


# Compat
startup = zerogpu_startup


__all__ = [
    'ZeroGPUError',
    'ZeroGPUException',
    'ZeroGPUClientError',
    'ZeroGPUIllegalDuration',
    'ZeroGPUPendingCreditsExceeded',
    'ZeroGPUQueueTimeout',
    'ZeroGPUQuotaExceeded',
    'ZeroGPUTaskAborted',
    'ZeroGPUTaskException',
    'ZeroGPUWorkerError',
    'ZeroGPULog',
    'ZeroGPUMiddleware',
    'default_gpu_size',
    'zerogpu_mode_enable',
    'zerogpu_mode_enabled',
    'zerogpu_startup',
]
