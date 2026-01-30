import os
from typing import List, Optional

from pydantic import ConfigDict, Field

from frogml_storage.models.entity_manifest import Artifact, Checksums, EntityManifest
from frogml_storage.models.serialization_metadata import SerializationMetadata


class ModelManifest(EntityManifest):
    """
    Represent a model manifest file

    Attributes:
        model_format: If the entity is model, holds model format information
        dependency_artifacts: If the entity is model, holds a list of files specifying the model dependencies
        code_artifacts: If the entity is model, specifies the archive file artifact
    """

    artifacts: List[Artifact] = Field(serialization_alias="model_artifacts")

    model_format: SerializationMetadata
    dependency_artifacts: Optional[List[Artifact]] = None
    code_artifacts: Optional[Artifact] = None

    # suppress warning on model_format field name.
    # if one day it collides with pydantic field, it will throw an error.
    model_config = ConfigDict(protected_namespaces=())

    def add_dependency_file(
        self, file_path: str, checksums: Checksums, rel_path: str
    ) -> None:
        if self.dependency_artifacts is None:
            self.dependency_artifacts = []
        self.dependency_artifacts.append(
            Artifact(
                artifact_path=rel_path,
                size=os.path.getsize(file_path),
                checksums=checksums,
            )
        )

    def __eq__(self, other):
        if not super.__eq__(self, other):
            return False
        if self.model_format != other.model_format:
            return False
        if self.dependency_artifacts != other.dependency_artifacts:
            return False
        if self.dependency_artifacts is not None:
            if len(self.dependency_artifacts) != len(other.dependency_artifacts):
                return False
            for self_artifact, other_artifact in zip(
                self.dependency_artifacts, other.dependency_artifacts
            ):
                if self_artifact != other_artifact:
                    return False
        if self.code_artifacts != other.code_artifacts:
            return False
        return True
