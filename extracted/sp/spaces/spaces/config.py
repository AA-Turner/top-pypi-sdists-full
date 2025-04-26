"""
"""
from __future__ import annotations

import os
from pathlib import Path

from .utils import boolean


ZEROGPU_OFFLOAD_DIR_DEFAULT = str(Path.home() / '.zerogpu' / 'tensors')


class Settings:
    def __init__(self):
        self.zero_gpu = boolean(
            os.getenv('SPACES_ZERO_GPU'))
        self.zero_device_api_url = (
            os.getenv('SPACES_ZERO_DEVICE_API_URL'))
        self.gradio_auto_wrap = boolean(
            os.getenv('SPACES_GRADIO_AUTO_WRAP'))
        self.zero_patch_torch_device = boolean(
            os.getenv('ZERO_GPU_PATCH_TORCH_DEVICE'))
        self.zero_gpu_v2 = boolean(
            os.getenv('ZEROGPU_V2'))
        self.zerogpu_offload_dir = (
            os.getenv('ZEROGPU_OFFLOAD_DIR', ZEROGPU_OFFLOAD_DIR_DEFAULT))
        self.zerogpu_cuda_device_name = (
            os.getenv('ZEROGPU_CUDA_DEVICE_NAME', "NVIDIA H200 MIG 3g.71gb"))
        self.zerogpu_cuda_total_memory = int(
            os.getenv('ZEROGPU_CUDA_TOTAL_MEMORY', 74625056768))
        self.zerogpu_cuda_reserved_memory = int(
            os.getenv('ZEROGPU_CUDA_RESERVED_MEMORY', 0))
        self.zerogpu_cuda_capability_major = int(
            os.getenv('ZEROGPU_CUDA_CAPABILITY_MAJOR', 9))
        self.zerogpu_cuda_capability_minor = int(
            os.getenv('ZEROGPU_CUDA_CAPABILITY_MINOR', 0))
        self.zerogpu_cuda_multi_processor_count = int(
            os.getenv('ZEROGPU_CUDA_MULTI_PROCESSOR_COUNT', 60))


Config = Settings()


if Config.zero_gpu:
    assert Config.zero_device_api_url is not None, (
        'SPACES_ZERO_DEVICE_API_URL env must be set '
        'on ZeroGPU Spaces (identified by SPACES_ZERO_GPU=true)'
    )
