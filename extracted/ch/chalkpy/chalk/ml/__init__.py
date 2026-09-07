from __future__ import annotations

from chalk.ml.model_file_transfer import FileInfo, HFSourceConfig, LocalSourceConfig, S3SourceConfig, SourceConfig
from chalk.ml.model_handler import CHALK_HANDLER_ARTIFACT_PATH, is_model_handler, model_handler
from chalk.ml.model_reference import ModelReference
from chalk.ml.model_version import ModelVersion
from chalk.ml.utils import ModelClass, ModelEncoding, ModelRunCriterion, ModelType

__all__ = (
    "CHALK_HANDLER_ARTIFACT_PATH",
    "FileInfo",
    "HFSourceConfig",
    "LocalSourceConfig",
    "ModelClass",
    "ModelEncoding",
    "ModelReference",
    "ModelRunCriterion",
    "ModelType",
    "ModelVersion",
    "S3SourceConfig",
    "SourceConfig",
    "is_model_handler",
    "last_checkpoint_path",  # pyright: ignore[reportUnsupportedDunderAll]
    "model_handler",
)


def __getattr__(name: str):
    if name == "last_checkpoint_path":
        from chalk.ml.chalk_train import last_checkpoint_path

        return last_checkpoint_path
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
