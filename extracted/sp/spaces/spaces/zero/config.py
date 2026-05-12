"""
"""

import json
import warnings
from importlib.resources import files
from functools import cache
from pathlib import Path
from typing import TypedDict


CONFIGS_FILENAME = 'configs.json'


class ZeroGPUConfig(TypedDict):
    model: str
    memory: int
    sm_major: int
    sm_minor: int
    sm_count: int
    xlarge_threshold: int | None
    duration_factor: float


@cache
def get_config():
    configs_raw = files('spaces.zero').joinpath(CONFIGS_FILENAME).read_text()
    configs: list[ZeroGPUConfig] = json.loads(configs_raw)
    default = configs[0]
    try:
        information = _read_gpu_information()
    except Exception: # pragma: no cover
        warnings.warn("Error while reading infos from Nvidia driver FS")
    else:
        model = _get_model(information) if information is not None else None
        for config in configs:
            if config['model'] == model:
                return config # pragma: no cover
    return default


def _read_gpu_information():
    for dir_path in Path('/proc/driver/nvidia/gpus').iterdir():
        if dir_path.is_dir():
            if (info_path := dir_path / 'information').is_file():
                return info_path.read_text()


def _get_model(information: str):
    for line in information.splitlines():
        if line.startswith('Model:'):
            return line.split('Model:')[1].strip()
