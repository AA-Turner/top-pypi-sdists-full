"""Labqoat starter SDK and CLI.

Each public name and subpackage loads on first use, so a process that only supervises workers or runs one
command never imports the authoring API it does not touch.
"""

from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from labqoat._generated.hugging_face_source import HuggingFaceSource
    from labqoat._generated.new_dataset_import import NewDatasetImport
    from labqoat.authoring import Resources
    from labqoat.client import Client
    from labqoat.compute.app import App
    from labqoat.compute.image import Image
    from labqoat.compute.secret import Secret
    from labqoat.compute.volume import Volume
    from labqoat.coordination.dict import Dict
    from labqoat.coordination.queue import Queue
    from labqoat.dataset import Dataset
    from labqoat.evaluation_case import EvaluationCase
    from labqoat.evaluation_report import EvaluationReport
    from labqoat.references import AssetRef as Artifact
    from labqoat.references import CheckpointRef as Checkpoint
    from labqoat.references import DatasetRef, ResolvedDatasetRef, ResourceId, Sha256
    from labqoat.run_context import RunContext
    from labqoat.runs.run_handle import RunHandle
    from labqoat.sandbox.sandbox import Sandbox

__version__ = "0.2.144"

_EXPORTS = {
    "App": ("labqoat.compute.app", "App"),
    "Image": ("labqoat.compute.image", "Image"),
    "Volume": ("labqoat.compute.volume", "Volume"),
    "Client": ("labqoat.client", "Client"),
    "Dict": ("labqoat.coordination.dict", "Dict"),
    "Queue": ("labqoat.coordination.queue", "Queue"),
    "Secret": ("labqoat.compute.secret", "Secret"),
    "EvaluationCase": ("labqoat.evaluation_case", "EvaluationCase"),
    "EvaluationReport": ("labqoat.evaluation_report", "EvaluationReport"),
    "RunContext": ("labqoat.run_context", "RunContext"),
    "RunHandle": ("labqoat.runs.run_handle", "RunHandle"),
    "Sandbox": ("labqoat.sandbox.sandbox", "Sandbox"),
    "Artifact": ("labqoat.references", "AssetRef"),
    "Dataset": ("labqoat.dataset", "Dataset"),
    "Checkpoint": ("labqoat.references", "CheckpointRef"),
    "DatasetRef": ("labqoat.references", "DatasetRef"),
    "ResolvedDatasetRef": ("labqoat.references", "ResolvedDatasetRef"),
    "ResourceId": ("labqoat.references", "ResourceId"),
    "Sha256": ("labqoat.references", "Sha256"),
    "Resources": ("labqoat.authoring", "Resources"),
    "HuggingFaceSource": ("labqoat._generated.hugging_face_source", "HuggingFaceSource"),
    "NewDatasetImport": ("labqoat._generated.new_dataset_import", "NewDatasetImport"),
}

__all__ = [
    "App",
    "Image",
    "Volume",
    "Client",
    "Dict",
    "Queue",
    "Secret",
    "EvaluationCase",
    "EvaluationReport",
    "RunContext",
    "RunHandle",
    "Sandbox",
    "Artifact",
    "Dataset",
    "Checkpoint",
    "DatasetRef",
    "ResolvedDatasetRef",
    "ResourceId",
    "Sha256",
    "Resources",
    "HuggingFaceSource",
    "NewDatasetImport",
    "__version__",
]


def __getattr__(name: str) -> object:
    """Load a public name, or a subpackage such as ``compute``, the first time it is read."""
    if name in _EXPORTS:
        module, attribute = _EXPORTS[name]
        value = getattr(import_module(module), attribute)
    elif name.startswith("_"):
        raise AttributeError(f"module 'labqoat' has no attribute {name!r}")
    else:
        try:
            value = import_module(f"labqoat.{name}")
        except ModuleNotFoundError as error:
            if error.name != f"labqoat.{name}":
                raise
            raise AttributeError(f"module 'labqoat' has no attribute {name!r}") from error
    globals()[name] = value
    return value
