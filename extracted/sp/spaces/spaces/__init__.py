"""
"""
import sys
from types import FunctionType
from typing import TYPE_CHECKING
from typing import Callable


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


class LazyImported:
    def __init__(self, import_fn: Callable[[], FunctionType]):
        self.import_fn = import_fn
    def __call__(self, *args, **kwargs):
        return self.import_fn()(*args, **kwargs)
    @property
    def __wrapped__(self):
        return self.import_fn()
    @property
    def __doc__(self): # pyright: ignore[reportIncompatibleVariableOverride]
        return self.import_fn().__doc__
    @property
    def __code__(self):
        return self.import_fn.__code__
    @property
    def __class__(self): # pyright: ignore[reportIncompatibleMethodOverride]
        return FunctionType
    @property
    def __name__(self):
        return self.import_fn.__name__.removeprefix('_')


def _aoti_capture():
    from .zero.torch.aoti import aoti_capture
    return aoti_capture

def _aoti_compile():
    from .zero.torch.aoti import aoti_compile
    return aoti_compile

def _aoti_compile_and_save(): # pragma: no cover
    from .zero.torch.aoti import aoti_compile_and_save
    return aoti_compile_and_save

def _aoti_apply():
    from .zero.torch.aoti import aoti_apply
    return aoti_apply

def _aoti_patch(): # pragma: no cover
    from .zero.torch.aoti import aoti_patch
    return aoti_patch

def _aoti_load(): # pragma: no cover
    from .zero.torch.aoti import aoti_load
    return aoti_load

def _aoti_load_call_source(): # pragma: no cover
    from .zero.torch.aoti import aoti_load_call_source
    return aoti_load_call_source

def _aoti_load_from_package_dir(): # pragma: no cover
    from .zero.torch.aoti import aoti_load_from_package_dir
    return aoti_load_from_package_dir

def _aoti_blocks_load():
    from .zero.torch.aoti import aoti_blocks_load
    return aoti_blocks_load


aoti_capture = LazyImported(_aoti_capture)
aoti_compile = LazyImported(_aoti_compile)
aoti_compile_and_save = LazyImported(_aoti_compile_and_save)
aoti_apply = LazyImported(_aoti_apply)
aoti_patch = LazyImported(_aoti_patch)
aoti_load = LazyImported(_aoti_load)
aoti_load_call_source = LazyImported(_aoti_load_call_source)
aoti_load_from_package_dir = LazyImported(_aoti_load_from_package_dir)
aoti_blocks_load = LazyImported(_aoti_blocks_load)


if TYPE_CHECKING:
    from .zero.torch.aoti import aoti_capture
    from .zero.torch.aoti import aoti_compile
    from .zero.torch.aoti import aoti_compile_and_save
    from .zero.torch.aoti import aoti_apply
    from .zero.torch.aoti import aoti_patch
    from .zero.torch.aoti import aoti_load
    from .zero.torch.aoti import aoti_load_call_source
    from .zero.torch.aoti import aoti_load_from_package_dir
    from .zero.torch.aoti import aoti_blocks_load


__all__ = [
    'GPU',
    'gradio_auto_wrap',
    'disable_gradio_auto_wrap',
    'enable_gradio_auto_wrap',
    'aoti_capture',
    'aoti_compile',
    'aoti_compile_and_save',
    'aoti_apply',
    'aoti_patch',
    'aoti_load',
    'aoti_load_call_source',
    'aoti_load_from_package_dir',
    'aoti_blocks_load',
]
