"""Stack implementations for Cortex."""

import importlib

from cortex.stacks.auto import build_cortex_auto_config, build_cortex_auto_stack
from cortex.stacks.base import CortexStack
from cortex.stacks.multiscale import MultiScaleStack, build_multiscale_stack, build_multiscale_stack_config


def _hf_module():
    return importlib.import_module("cortex.stacks.hf")


def build_hf_stack(*args, **kwargs):
    return _hf_module().build_hf_stack(*args, **kwargs)


def build_hf_stack_config(*args, **kwargs):
    return _hf_module().build_hf_stack_config(*args, **kwargs)


def build_llama_stack_config_from_model(*args, **kwargs):
    return _hf_module().build_llama_stack_config_from_model(*args, **kwargs)


def build_llama_stack_from_model(*args, **kwargs):
    return _hf_module().build_llama_stack_from_model(*args, **kwargs)


__all__ = [
    "CortexStack",
    "MultiScaleStack",
    "build_cortex_auto_config",
    "build_cortex_auto_stack",
    "build_hf_stack",
    "build_hf_stack_config",
    "build_llama_stack_config_from_model",
    "build_llama_stack_from_model",
    "build_multiscale_stack",
    "build_multiscale_stack_config",
]
