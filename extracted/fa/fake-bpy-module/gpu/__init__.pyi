"""
This module provides Python wrappers for the GPU implementation in Blender.
Some higher level functions can be found in the gpu_extras module.

gpu.types.rst
gpu.matrix.rst
gpu.select.rst
gpu.shader.rst
gpu.state.rst
gpu.texture.rst
gpu.platform.rst
gpu.capabilities.rst

:maxdepth: 1
:caption: Submodules

"""

import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
from . import capabilities as capabilities
from . import matrix as matrix
from . import platform as platform
from . import select as select
from . import shader as shader
from . import state as state
from . import texture as texture
from . import types as types
