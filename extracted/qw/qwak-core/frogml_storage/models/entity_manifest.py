import os
from abc import ABC
from typing import List, Optional

from pydantic import BaseModel

from frogml_storage.utils import calc_content_sha2, calculate_sha2


class Checksums(BaseModel):
    sha2: str

    @classmethod
    def calc_checksums(cls, file_path: str) -> "Checksums":
        return cls(sha2=calculate_sha2(file_path))

    @classmethod
    def calc_content_checksums(cls, content: str) -> "Checksums":
        return cls(sha2=calc_content_sha2(content))


class Artifact(BaseModel):
    artifact_path: str
    size: int
    checksums: Checksums

    def __eq__(self, other):
        if not isinstance(other, Artifact):
            return False
        return (
            self.artifact_path == other.artifact_path
            and self.size == other.size
            and self.checksums == other.checksums
        )


class EntityManifest(BaseModel, ABC):
    """
    Represent an entity manifest file

    Attributes:
        created_date: The date the model | dataset were uploaded to Artifactory
        artifacts: A list of artifacts that belong to the model | dataset
        id: <organization>/<entity_name> - exists only for downloaded EntityInfo
        version: The entity version - exists only for downloaded EntityInfo
    """

    created_date: str
    artifacts: List[Artifact]
    id: Optional[str] = None
    version: Optional[str] = None

    def add_file(self, file_path: str, checksums: Checksums, rel_path: str) -> None:
        self.artifacts.append(
            Artifact(
                artifact_path=rel_path,
                size=os.path.getsize(file_path),
                checksums=checksums,
            )
        )

    def add_content_file(self, rel_path: str, content: str) -> None:
        checksums = Checksums.calc_content_checksums(content)
        self.artifacts.append(
            Artifact(
                artifact_path=rel_path,
                size=len((content, "utf-8")),
                checksums=checksums,
            )
        )

    @classmethod
    def from_json(cls, json_str: str) -> "EntityManifest":
        return cls.model_validate_json(json_str)

    def to_json(self) -> str:
        return self.model_dump_json(by_alias=True, exclude_none=True)

    def __eq__(self, other):
        if not isinstance(other, EntityManifest):
            return False
        if self.id != other.id:
            return False
        if self.version != other.version:
            return False
        if self.created_date != other.created_date:
            return False
        if len(self.artifacts) != len(other.artifacts):
            return False
        for self_artifact, other_artifact in zip(self.artifacts, other.artifacts):
            if self_artifact != other_artifact:
                return False
        return True
