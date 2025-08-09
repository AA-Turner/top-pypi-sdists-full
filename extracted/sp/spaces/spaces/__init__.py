"""
"""
from __future__ import annotations

import sys
from typing import TYPE_CHECKING


if sys.version_info.minor < 8: # pragma: no cover
    raise RuntimeError("Importing PySpaces requires Python 3.8+")


# Prevent gradio from importing spaces
if (gr := sys.modules.get('gradio')) is not None: # pragma: no cover
    try:
        gr.Blocks
    except AttributeError:
        raise ImportError


from .zero.decorator import GPU
from .gradio import gradio_auto_wrap
from .gradio import disable_gradio_auto_wrap
from .gradio import enable_gradio_auto_wrap


def _aoti_capture(*args, **kwargs): # pragma: no cover
    from .zero.torch.aoti import aoti_capture
    return aoti_capture(*args, **kwargs)

def _aoti_compile(*args, **kwargs): # pragma: no cover
    from .zero.torch.aoti import aoti_compile
    return aoti_compile(*args, **kwargs)

def _aoti_apply(*args, **kwargs): # pragma: no cover
    from .zero.torch.aoti import aoti_apply
    return aoti_apply(*args, **kwargs)

if TYPE_CHECKING:
    from .zero.torch.aoti import aoti_capture
    from .zero.torch.aoti import aoti_compile
    from .zero.torch.aoti import aoti_apply
else:
    aoti_capture = _aoti_capture
    aoti_compile = _aoti_compile
    aoti_apply = _aoti_apply


__all__ = [
    'GPU',
    'gradio_auto_wrap',
    'disable_gradio_auto_wrap',
    'enable_gradio_auto_wrap',
    'aoti_capture',
    'aoti_compile',
    'aoti_apply',
]
