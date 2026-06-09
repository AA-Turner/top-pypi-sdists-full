from __future__ import annotations

import os
from datetime import datetime
from typing import TYPE_CHECKING, Any

from chalk.ml.model_hooks import MODEL_REGISTRY
from chalk.ml.utils import (
    ModelClass,
    ModelEncoding,
    ModelType,
    get_model_spec,
    get_registry_metadata_file,
    model_encoding_from_proto,
    model_type_from_proto,
)

if TYPE_CHECKING:
    from chalk.features.resolver import ResourceHint


class ModelVersion:
    def __init__(
        self,
        *,
        name: str,
        version: int | None = None,
        alias: str | None = None,
        as_of_date: datetime | None = None,
        identifier: str | None = None,
        model_type: ModelType | None = None,
        model_encoding: ModelEncoding | None = None,
        model_class: ModelClass | None = None,
        filename: str | None = None,
        resource_hint: "ResourceHint | None" = None,
        resource_group: str | None = None,
        venv: str | None = None,
    ):
        """Specifies the model version that should be loaded into the deployment.

        Examples
        --------
        >>> from chalk.ml import ModelVersion
        >>> ModelVersion(
        ...     name="fraud_model",
        ...     version=1,
        ... )
        """
        super().__init__()
        self.name = name
        self.version = version
        self.alias = alias
        self.as_of_date = as_of_date
        self.identifier = identifier
        self.model_type = model_type
        self.model_encoding = model_encoding
        self.model_class = model_class
        self.filename = filename
        self.resource_hint: "ResourceHint | None" = resource_hint
        self.resource_group = resource_group
        self.venv = venv

        self._model = None
        self._predictor = None
        # Whether the model registry metadata file was present the last time
        # try_hydrate ran (i.e. a deployed environment where the model can be loaded).
        self.metadata_available = False

    def get_model_file(self) -> str | None:
        """Returns the filename of the model."""
        if self.filename is None:
            return None
        return self.filename

    @property
    def is_hydrated(self) -> bool:
        """Whether the model is hydrated and ready to be loaded/used, i.e. its
        type and encoding are known."""
        return self.model_type is not None and self.model_encoding is not None

    def try_hydrate(self) -> None:
        """Populate model_type/encoding/class/filename from the model registry
        metadata file when it is available. No-op if already hydrated or no metadata
        is available, in which case the model hydrates lazily on first use."""
        if self.is_hydrated:
            return
        registry_metadata_file = get_registry_metadata_file()
        self.metadata_available = registry_metadata_file is not None and os.path.exists(registry_metadata_file)
        if not self.metadata_available:
            return
        loaded = get_model_spec(
            model_name=self.name,
            identifier=self.identifier or "",
            registry_metadata_file=registry_metadata_file,
        )
        self.model_type = model_type_from_proto(loaded.spec.model_type)
        self.model_encoding = model_encoding_from_proto(loaded.spec.model_encoding)
        if self.model_class is None and loaded.spec.model_class:
            self.model_class = ModelClass(loaded.spec.model_class)
        if self.filename is None:
            self.filename = loaded.model_path

    def load_model(self):
        """Loads the model from the specified filename using the appropriate hook."""
        self.try_hydrate()
        if self.model_type is not None and self.model_encoding is not None:
            model = MODEL_REGISTRY.get(
                model_type=self.model_type, encoding=self.model_encoding, model_class=self.model_class
            )
            if model is not None and self.filename is not None:
                self._model = model.load_model(self.filename, resource_hint=self.resource_hint)
            else:
                raise ValueError(
                    f"No load function defined for type {self.model_type}, encoding {self.model_encoding}, and class {self.model_class}"
                )
        else:
            raise ValueError("Model type and encoding must be specified to load model.")

    def predict(self, X: Any):
        """Runs prediction using the loaded model."""
        return self.predictor.predict(self.model, X)

    @property
    def model(self) -> Any:
        """Returns the loaded model instance."""
        if self._model is None:
            self.load_model()

        return self._model

    @property
    def predictor(self) -> Any:
        """Returns the predictor instance, initializing it if needed."""
        if self._predictor is None:
            self.try_hydrate()
            if self.model_type is None or self.model_encoding is None:
                raise ValueError("Model type and encoding must be specified to use predictor.")
            self._predictor = MODEL_REGISTRY.get(
                model_type=self.model_type, encoding=self.model_encoding, model_class=self.model_class
            )
            if self._predictor is None:
                raise ValueError(f"No predictor defined for type {self.model_type} and encoding {self.model_encoding}")
        return self._predictor
