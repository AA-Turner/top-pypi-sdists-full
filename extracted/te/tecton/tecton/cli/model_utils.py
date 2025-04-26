import importlib
from pathlib import Path
from typing import List

from tecton.framework import model_config
from tecton.framework.model_config import ModelConfig


def get_custom_models(model_config_file_path: Path) -> List[ModelConfig]:
    spec = importlib.util.spec_from_file_location(model_config_file_path.stem, model_config_file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return list(model_config._CUSTOM_MODELS)
