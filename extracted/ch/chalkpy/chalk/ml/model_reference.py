from __future__ import annotations

import inspect
import os
from datetime import datetime

from chalk.utils.object_inspect import get_source_object_starting
from chalk.utils.source_parsing import should_skip_source_code_parsing

DEFAULT_MODEL_PATH = os.getenv("CHALK_MODEL_REGISTRY_ROOT", "/models")


class ModelReference:
    def __init__(
        self,
        *,
        name: str,
        version: int | None = None,
        alias: str | None = None,
        as_of_date: datetime | None = None,
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
            identifier = f"version/{version}"
        elif alias is not None:
            identifier = f"alias/{alias}"
        elif as_of_date is not None:
            identifier = f"asof/{as_of_date.strftime('%Y-%m-%dT%H-%M-%S')}"

        self.name = name
        self.version = version
        self.as_of_date = as_of_date
        self.alias = alias
        self.identifier = identifier

        self.filename = filename
        self.source_line_start = source_line_start
        self.code = source_code
        self.source_line_end = source_line_end

        dup_mv = MODEL_REFERENCE_REGISTRY.get((name, identifier), None)
        if dup_mv is not None:
            self.errors.append(
                (
                    "Model Reference must be distinct on name and identifier, but found two model bundles with name "
                    f"'{name}' and identifier '{identifier}' in files '{dup_mv.filename}' and '{filename}'."
                )
            )

        MODEL_REFERENCE_REGISTRY[(name, identifier)] = self

    @classmethod
    def as_of(cls, name: str, when: datetime):
        """Creates a ModelReference for a specific point in time.

        Parameters
        ----------
        name
            The name of the model.
        when
            The datetime to use for creating the model version identifier.

        Returns
        -------
        ModelReference
            A new ModelReference instance with a time-based identifier.

        Examples
        --------
        >>> import datetime
        >>> timestamp = datetime.datetime(2023, 10, 15, 14, 30, 0)
        >>> model = ModelReference.as_of("fraud_model", timestamp)
        """
        return ModelReference(name=name, as_of_date=when)

    @classmethod
    def from_version(cls, name: str, version: int):
        """Creates a ModelReference using a numeric version identifier.

        Parameters
        ----------
        name
            The name of the model.
        version
            The version number. Must be a non-negative integer.

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
        """
        if version < 0:
            raise ValueError("Version number must be a non-negative integer.")

        return ModelReference(name=name, version=version)

    @classmethod
    def from_alias(cls, name: str, alias: str):
        """Creates a ModelReference using an alias identifier.

        Parameters
        ----------
        name
            The name of the model.
        alias
            The alias string. Must be non-empty.

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
        """
        if not alias:
            raise ValueError("Alias must be a non-empty string.")

        return ModelReference(name=name, alias=alias)

    def get_file(self, file_name: str) -> str:
        """Returns the file path of the model version.

        Parameters
        ----------
        file_name (str):
            The name of the file to retrieve.

        Returns
        -------
        file_path: The file path of the specified file in the model version.

        Examples
        --------
        >>> model_version = ModelReference.from_version(name="fraud_model", version=1)
        >>> file_path = model_version.get_file("model.pkl")
        """
        return os.path.join(DEFAULT_MODEL_PATH, self.name, self.identifier, file_name)


MODEL_REFERENCE_REGISTRY: dict[tuple[str, str], ModelReference] = {}
