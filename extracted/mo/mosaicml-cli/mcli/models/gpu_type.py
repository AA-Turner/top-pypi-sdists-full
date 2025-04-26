""" Defines a GPU Type """
from __future__ import annotations

from enum import Enum
from typing import List


class GPUType(Enum):
    """ The Type of GPU to use in a job """
    NONE = 'None'
    A100_80GB = 'a100_80gb'
    A100_40GB = 'a100_40gb'
    V100_32GB = 'v100_32gb'
    V100_16GB = 'v100_16gb'
    T4 = 't4'
    K80 = 'k80'
    RTX3080 = '3080'
    RTX3090 = '3090'
    TPUv2 = 'tpuv2'  # pylint: disable=invalid-name
    TPUv3 = 'tpuv3'  # pylint: disable=invalid-name

    @staticmethod
    def get_available_gpu_types() -> List[str]:
        return [x.value for x in GPUType]

    @classmethod
    def from_string(cls, gpu_type: str) -> GPUType:
        if isinstance(gpu_type, int):
            # Secondary catch for gpu_type for 30 series enums
            gpu_type = str(gpu_type)
        try:
            for e in GPUType:
                if e.value.lower() == gpu_type.lower():
                    return e
            return cls[gpu_type.lower()]
        except Exception as e:  # pylint: disable=broad-except
            gpu_types_str = ', '.join(GPUType.get_available_gpu_types())
            raise ValueError(
                f'Unable to convert type: {gpu_type} into an available gpu type\n'
                f'Available GPU Types: {gpu_types_str}',) from e

    def __str__(self) -> str:
        return self.value

    def __lt__(self, other) -> bool:
        """ Implemented for choosing the best instance as defaults """
        if not isinstance(other, GPUType):
            # Does not matter if not a GPUType
            return False

        def get_rating(gpu_type: GPUType) -> int:
            ordering = [
                GPUType.A100_80GB,
                GPUType.A100_40GB,
                GPUType.V100_32GB,
                GPUType.V100_16GB,
                GPUType.T4,
                GPUType.RTX3090,
                GPUType.RTX3080,
                GPUType.NONE,
            ]
            try:
                return ordering.index(gpu_type)
            except ValueError:
                return len(ordering)

        return get_rating(self) < get_rating(other)
