r"""Contain data loaders and savers."""

from __future__ import annotations

__all__ = [
    "AutoFileLoader",
    "BaseFileSaver",
    "BaseLoader",
    "BaseSaver",
    "CloudpickleLoader",
    "CloudpickleSaver",
    "JoblibLoader",
    "JoblibSaver",
    "JsonLoader",
    "JsonSaver",
    "PickleLoader",
    "PickleSaver",
    "TextLoader",
    "TextSaver",
    "TorchLoader",
    "TorchSaver",
    "YamlLoader",
    "YamlSaver",
    "is_loader_config",
    "is_saver_config",
    "load_cloudpickle",
    "load_joblib",
    "load_json",
    "load_pickle",
    "load_text",
    "load_torch",
    "load_yaml",
    "save_cloudpickle",
    "save_joblib",
    "save_json",
    "save_pickle",
    "save_text",
    "save_torch",
    "save_yaml",
    "setup_loader",
    "setup_saver",
]

from iden.io.auto import AutoFileLoader, register_auto_loaders
from iden.io.base import (
    BaseFileSaver,
    BaseLoader,
    BaseSaver,
    is_loader_config,
    is_saver_config,
    setup_loader,
    setup_saver,
)
from iden.io.cloudpickle import (
    CloudpickleLoader,
    CloudpickleSaver,
    load_cloudpickle,
    save_cloudpickle,
)
from iden.io.joblib import JoblibLoader, JoblibSaver, load_joblib, save_joblib
from iden.io.json import JsonLoader, JsonSaver, load_json, save_json
from iden.io.pickle import PickleLoader, PickleSaver, load_pickle, save_pickle
from iden.io.text import TextLoader, TextSaver, load_text, save_text
from iden.io.torch import TorchLoader, TorchSaver, load_torch, save_torch
from iden.io.yaml import YamlLoader, YamlSaver, load_yaml, save_yaml

register_auto_loaders()
