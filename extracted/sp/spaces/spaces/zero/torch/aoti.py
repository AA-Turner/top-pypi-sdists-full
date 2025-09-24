"""
"""
from __future__ import annotations

import contextlib
import os
from contextvars import ContextVar
from io import BytesIO
from pathlib import Path
from typing import Any
from typing import Callable
from typing import cast
from unittest.mock import patch

import torch
from packaging import version
if version.parse(torch.__version__) < version.parse('2.8'): # pragma: no cover
    raise RuntimeError("ZeroGPU AoTI reuqires PyTorch 2.8+")

from torch._inductor.package.package import package_aoti
from torch.export.pt2_archive._package import AOTICompiledModel
from torch.export.pt2_archive._package_weights import Weights

from ..utils import register_cleanup


INDUCTOR_CONFIGS_OVERRIDES = {
    'aot_inductor.package_constants_in_so': False,
    'aot_inductor.package_constants_on_disk': True,
    'aot_inductor.package': True,
    'always_keep_tensor_constants': True,
}


ARCHIVE_SO_PATTERN = '/tmp/*/archive/data/aotinductor/model/*.wrapper.so'


@contextlib.contextmanager
def _register_aoti_cleanup():
    """
    PyTorch already cleans-up extracted archives in /tmp
    But the GPU worker never terminates gracefully in ZeroGPU so cleanup must be done manually
    """
    pid = os.getpid()
    map_files = Path(f'/proc/{pid}/map_files')
    maps_before = {f.name for f in map_files.iterdir()}
    yield
    for map_file in map_files.iterdir():
        if map_file.name not in maps_before:
            if (mapped := map_file.readlink()).match(ARCHIVE_SO_PATTERN):
                package_path = Path(*mapped.parts[:3])
                return register_cleanup(pid, package_path)


class ZeroGPUWeights:
    def __init__(self, constants_map: dict[str, torch.Tensor], to_cuda: bool = False):
        if to_cuda:
            self.constants_map = {name: tensor.to('cuda') for name, tensor in constants_map.items()}
        else:
            self.constants_map = constants_map
    def __reduce__(self):
        constants_map: dict[str, torch.Tensor] = {}
        for name, tensor in self.constants_map.items():
            tensor_ = torch.empty_like(tensor, device='cpu').pin_memory()
            constants_map[name] = tensor_.copy_(tensor).detach().share_memory_()
        return ZeroGPUWeights, (constants_map, True)


class ZeroGPUCompiledModel:
    def __init__(self, archive_file: torch.types.FileLike, weights: ZeroGPUWeights):
        self.archive_file = archive_file
        self.weights = weights
        self.compiled_model: ContextVar[AOTICompiledModel | None] = ContextVar('compiled_model', default=None)
    def __call__(self, *args, **kwargs):
        if (compiled_model := self.compiled_model.get()) is None:
            with _register_aoti_cleanup():
                compiled_model = torch._inductor.aoti_load_package(self.archive_file)
            compiled_model = cast(AOTICompiledModel, compiled_model)
            constant_map = {name: self.weights.constants_map[name] for name in compiled_model.get_constant_fqns()}
            compiled_model.load_constants(constant_map, check_full_update=True, user_managed=True)
            self.compiled_model.set(compiled_model)
        return compiled_model(*args, **kwargs)
    def __reduce__(self):
        return ZeroGPUCompiledModel, (self.archive_file, self.weights)


def aoti_compile(
    exported_program: torch.export.ExportedProgram,
    inductor_configs: dict[str, Any] | None = None,
):
    inductor_configs = {**(inductor_configs or {}), **INDUCTOR_CONFIGS_OVERRIDES}
    gm = cast(torch.fx.GraphModule, exported_program.module())
    assert exported_program.example_inputs is not None
    args, kwargs = exported_program.example_inputs
    artifacts = torch._inductor.aot_compile(gm, args, kwargs, options=inductor_configs) # pyright: ignore [reportArgumentType]
    artifacts = cast(list[str | Weights], artifacts)
    archive_file = BytesIO()
    files = (file for file in artifacts if isinstance(file, str))
    package_aoti(archive_file, list(files))
    weights, = (artifact for artifact in artifacts if isinstance(artifact, Weights))
    weights = cast(Weights, weights)
    zerogpu_weights = ZeroGPUWeights({name: weights.get_weight(name)[0] for name in weights})
    return ZeroGPUCompiledModel(archive_file, zerogpu_weights)


def aoti_apply(
    compiled: ZeroGPUCompiledModel,
    module: torch.nn.Module,
    call_method: str = 'forward',
):
    setattr(module, call_method, compiled)
    drain_module_parameters(module)


def drain_module_parameters(module: torch.nn.Module):
    state_dict_meta = {name: {'device': tensor.device, 'dtype': tensor.dtype} for name, tensor in module.state_dict().items()}
    state_dict = {name: torch.nn.Parameter(torch.empty_like(tensor, device='cpu')) for name, tensor in module.state_dict().items()}
    module.load_state_dict(state_dict, assign=True)
    for name, param in state_dict.items():
        meta = state_dict_meta[name]
        param.data = torch.Tensor([]).to(**meta)


@contextlib.contextmanager
def aoti_capture(
    module: torch.nn.Module | Callable[..., Any],
    call_method: str = 'forward',
):
    class CapturedCallException(Exception):
        def __init__(self, *args, **kwargs):
            super().__init__()
            self.args = args
            self.kwargs = kwargs

    class CapturedCall:
        def __init__(self):
            self.args: tuple[Any, ...] = ()
            self.kwargs: dict[str, Any] = {}

    captured_call = CapturedCall()

    def capture_call(*args, **kwargs):
        raise CapturedCallException(*args, **kwargs)

    with patch.object(module, call_method, new=capture_call):
        try:
            yield captured_call
        except CapturedCallException as e:
            captured_call.args = e.args
            captured_call.kwargs = e.kwargs
