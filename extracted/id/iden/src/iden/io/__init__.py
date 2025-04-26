r"""Contain data loaders and savers."""

from __future__ import annotations

__all__ = [
    "AutoFileLoader",
    "BaseFileSaver",
    "BaseLoader",
    "BaseSaver",
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
    "load_json",
    "load_pickle",
    "load_text",
    "load_torch",
    "load_yaml",
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
from iden.io.json import JsonLoader, JsonSaver, load_json, save_json
from iden.io.pickle import PickleLoader, PickleSaver, load_pickle, save_pickle
from iden.io.text import TextLoader, TextSaver, load_text, save_text
from iden.io.torch import TorchLoader, TorchSaver, load_torch, save_torch
from iden.io.yaml import YamlLoader, YamlSaver, load_yaml, save_yaml

register_auto_loaders()
