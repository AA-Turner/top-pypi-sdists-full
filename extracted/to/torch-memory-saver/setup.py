import logging
import os
import shutil
from pathlib import Path

import setuptools
from setuptools import setup

logger = logging.getLogger(__name__)


# copy & modify from torch/utils/cpp_extension.py
def _find_cuda_home():
    """Find the CUDA install path."""
    # Guess #1
    cuda_home = os.environ.get('CUDA_HOME') or os.environ.get('CUDA_PATH')
    if cuda_home is None:
        # Guess #2
        nvcc_path = shutil.which("nvcc")
        if nvcc_path is not None:
            cuda_home = os.path.dirname(os.path.dirname(nvcc_path))
        else:
            # Guess #3
            cuda_home = '/usr/local/cuda'
    return cuda_home


cuda_home = Path(_find_cuda_home())
include_dirs = [
    str(cuda_home.resolve() / 'targets/x86_64-linux/include'),
]
library_dirs = [
    str(cuda_home.resolve() / 'lib64'),
    str(cuda_home.resolve() / 'lib64/stubs'),
]

setup(
    name='torch_memory_saver',
    version='0.0.6',
    ext_modules=[setuptools.Extension(
        'torch_memory_saver_cpp',
        ['csrc/torch_memory_saver.cpp'],
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        libraries=['cuda']
    )],
    python_requires=">=3.9",
    packages=['torch_memory_saver'],
)
