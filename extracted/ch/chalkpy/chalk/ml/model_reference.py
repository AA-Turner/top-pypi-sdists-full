from __future__ import annotations

import inspect
import os
from datetime import datetime
from typing import TYPE_CHECKING

from chalk.ml.model_version import ModelVersion
from chalk.ml.utils import (
    ModelClass,
    get_model_spec,
    get_registry_metadata_file,
    model_encoding_from_proto,
    model_type_from_proto,
)
from chalk.utils.object_inspect import get_source_object_starting
from chalk.utils.source_parsing import should_skip_source_code_parsing

if TYPE_CHECKING:
    from chalk.features.resolver import ResourceHint


class ModelReference:
    def __init__(
        self,
        *,
        name: str,
        version: int | None = None,
        alias: str | None = None,
        as_of_date: datetime | None = None,
        resource_hint: "ResourceHint | None" = None,
        resource_group: str | None = None,
    ):
        """Specifies the model version that should be loaded into the deployment.

        Examples
        --------
        >>> from chalk import ModelReference
        >>> ModelReference(
        ...     name="fraud_model",
        ...     version=1,
        ... )
        """
        super().__init__()
        self.errors = []

        filename = None
        source_line_start = None
        source_line_end = None
        source_code = None

        if not should_skip_source_code_parsing():
            try:
                internal_frame = inspect.currentframe()
                if internal_frame is not None:
                    definition_frame = internal_frame.f_back
                    if definition_frame is not None:
                        calling_frame = definition_frame.f_back
                        if calling_frame is not None:
                            filename = calling_frame.f_code.co_filename
                            source_line_start = calling_frame.f_lineno
                            source_code, source_line_start, source_line_end = get_source_object_starting(calling_frame)
                    del internal_frame
            except Exception:
                pass

        if sum([v is not None for v in [version, alias, as_of_date]]) != 1:
            self.errors.append(("ModelReference must be specified with only one of version, alias, or as_of_date."))

        identifier = ""
        if version is not None:
            identifier = f"version_{version}"
        elif alias is not None:
            identifier = f"alias_{alias}"
        elif as_of_date is not None:
            identifier = f"asof_{int(as_of_date.timestamp())}"

        self.name = name
        self.version = version
        self.as_of_date = as_of_date
        self.alias = alias
        self.identifier = identifier
        self.resource_hint = resource_hint
        self.resource_group = resource_group

        self.filename = filename
        self.source_line_start = source_line_start
        self.code = source_code
        self.source_line_end = source_line_end

        self.relations: list[tuple[list[str], str]] = []
        self.resolvers: list[str] = []

        dup_mr = MODEL_REFERENCE_REGISTRY.get((name, identifier), None)
        if dup_mr is not None:
            self.errors.append(
                (
                    "Model Reference must be distinct on name and identifier, but found two model bundles with name "
                    f"'{name}' and identifier '{identifier}' in files '{dup_mr.filename}' and '{filename}'."
                )
            )

        MODEL_REFERENCE_REGISTRY[(name, identifier)] = self

        # Only load model if the metadata file exists, which only happens in deployed environments
        registry_metadata_file = get_registry_metadata_file()
        if registry_metadata_file is not None and os.path.exists(registry_metadata_file):
            model_artifact_metadata = get_model_spec(model_name=name, identifier=identifier)

            mv = ModelVersion(
                filename=model_artifact_metadata.model_path,
                name=name,
                version=version,
                as_of_date=as_of_date,
                identifier=identifier,
                model_type=model_type_from_proto(model_artifact_metadata.spec.model_type),
                model_encoding=model_encoding_from_proto(model_artifact_metadata.spec.model_encoding),
                model_class=ModelClass(model_artifact_metadata.spec.model_class)
                if model_artifact_metadata.spec.model_class
                else None,
                resource_hint=resource_hint,
                resource_group=resource_group,
            )

            from chalk.features.hooks import before_all

            def hook():
                mv.load_model()

            before_all(hook, resource_hint=resource_hint, resource_group=resource_group)

            self.model_version = mv
        else:
            self.model_version = ModelVersion(
                name=name, identifier=identifier, resource_hint=resource_hint, resource_group=resource_group
            )

    @classmethod
    def as_of(
        cls,
        name: str,
        when: datetime,
        resource_hint: "ResourceHint | None" = None,
        resource_group: str | None = None,
    ) -> ModelVersion:
        """Creates a ModelReference for a specific point in time.

        Parameters
        ----------
        name
            The name of the model.
        when
            The datetime to use for creating the model version identifier.
        resource_hint
            Whether this model loading is bound by CPU, I/O, or GPU.
        resource_group
            The resource group for the model: this is used to isolate execution
            onto a separate pod (or set of nodes), such as on a GPU-enabled node.

        Returns
        -------
        ModelReference
            A new ModelReference instance with a time-based identifier.

        Examples
        --------
        >>> import datetime
        >>> timestamp = datetime.datetime(2023, 10, 15, 14, 30, 0)
        >>> model = ModelReference.as_of("fraud_model", timestamp)
        >>> model = ModelReference.as_of("fraud_model", timestamp, resource_hint="gpu", resource_group="gpu-group")
        """

        mr = ModelReference(name=name, as_of_date=when, resource_hint=resource_hint, resource_group=resource_group)
        return mr.model_version

    @classmethod
    def from_version(
        cls,
        name: str,
        version: int,
        resource_hint: "ResourceHint | None" = None,
        resource_group: str | None = None,
    ) -> ModelVersion:
        """Creates a ModelReference using a numeric version identifier.

        Parameters
        ----------
        name
            The name of the model.
        version
            The version number. Must be a non-negative integer.
        resource_hint
            Whether this model loading is bound by CPU, I/O, or GPU.
        resource_group
            The resource group for the model: this is used to isolate execution
            onto a separate pod (or set of nodes), such as on a GPU-enabled node.

        Returns
        -------
        ModelReference
            A new ModelReference instance with a version-based identifier.

        Raises
        ------
        ValueError
            If version is negative.

        Examples
        --------
        >>> model = ModelReference.from_version("fraud_model", 1)
        >>> model = ModelReference.from_version("fraud_model", 1, resource_hint="gpu", resource_group="gpu-group")
        """
        if version < 0:
            raise ValueError("Version number must be a non-negative integer.")

        mr = ModelReference(name=name, version=version, resource_hint=resource_hint, resource_group=resource_group)
        return mr.model_version

    @classmethod
    def from_alias(
        cls,
        name: str,
        alias: str,
        resource_hint: "ResourceHint | None" = None,
        resource_group: str | None = None,
    ) -> ModelVersion:
        """Creates a ModelReference using an alias identifier.

        Parameters
        ----------
        name
            The name of the model.
        alias
            The alias string. Must be non-empty.
        resource_hint
            Whether this model loading is bound by CPU, I/O, or GPU.
        resource_group
            The resource group for the model: this is used to isolate execution
            onto a separate pod (or set of nodes), such as on a GPU-enabled node.

        Returns
        -------
        ModelReference
            A new ModelReference instance with an alias-based identifier.

        Raises
        ------
        ValueError
            If alias is empty.

        Examples
        --------
        >>> model = ModelReference.from_alias("fraud_model", "latest")
        >>> model = ModelReference.from_alias("fraud_model", "latest", resource_hint="gpu", resource_group="gpu-group")
        """
        if not alias:
            raise ValueError("Alias must be a non-empty string.")

        mr = ModelReference(name=name, alias=alias, resource_hint=resource_hint, resource_group=resource_group)
        return mr.model_version


MODEL_REFERENCE_REGISTRY: dict[tuple[str, str], ModelReference] = {}
