from abc import ABC, abstractmethod
from typing import Optional

from _qwak_proto.qwak.feature_store.v1.common.jfrog_artifact.jfrog_artifact_pb2 import (
    JfrogArtifact as ProtoJfrogArtifact,
)
from _qwak_proto.qwak.feature_store.v1.common.source_code.source_code_pb2 import (
    SourceCodeArtifact as ProtoSourceCodeArtifact,
    SourceCodeSpec as ProtoSourceCodeSpec,
    ZipArtifact as ProtoZipArtifact,
)
from pydantic import BaseModel, Field, model_validator
from qwak.exceptions import QwakException
from typing_extensions import Self


class JfrogArtifact(BaseModel):
    path: str

    @classmethod
    def from_proto(cls, proto: ProtoJfrogArtifact) -> "JfrogArtifact":
        return cls(path=proto.path)

    def to_proto(self) -> ProtoJfrogArtifact:
        return ProtoJfrogArtifact(path=self.path)


class SourceCodeArtifact(BaseModel, ABC):
    @abstractmethod
    def _to_proto(self) -> ProtoSourceCodeArtifact:
        pass


class ZipArtifact(SourceCodeArtifact):
    main_file: str
    qwak_artifact_path: Optional[str] = None
    jfrog_artifact_path: Optional[JfrogArtifact] = None

    @model_validator(mode="after")
    def validate_only_one_artifact_path_type_provided(self: Self) -> Self:
        """
        Ensures that either 'qwak_artifact_path' or 'jfrog_artifact_path' is provided,
        but not both.
        """
        if (self.qwak_artifact_path is None) == (self.jfrog_artifact_path is None):
            raise QwakException(
                "Either `qwak_artifact_path` or `jfrog_artifact_path` must be provided."
            )
        return self

    @classmethod
    def _from_proto(cls, proto: ProtoSourceCodeArtifact) -> "ZipArtifact":
        artifact_type: str = proto.WhichOneof("type")
        if artifact_type != "zip_artifact":
            raise QwakException(
                f"Instead of `zip_artifact` got: {artifact_type}"  # noqa
            )

        artifact_path_type: str = proto.zip_artifact.WhichOneof("path_type")
        jfrog_artifact_path: Optional[JfrogArtifact] = None
        qwak_artifact_path: Optional[str] = None

        if artifact_path_type == "jfrog_artifact_path":
            jfrog_artifact_path = JfrogArtifact.from_proto(
                proto.zip_artifact.jfrog_artifact_path
            )
        elif artifact_path_type == "path":
            qwak_artifact_path = proto.zip_artifact.path
        else:
            raise QwakException(
                "Either `path` or `jfrog_artifact_path` must be provided inside SourceCodeArtifact proto."
            )

        return cls(
            jfrog_artifact_path=jfrog_artifact_path,
            qwak_artifact_path=qwak_artifact_path,
            main_file=proto.zip_artifact.main_file,
        )

    def _to_proto(self) -> ProtoSourceCodeArtifact:
        return ProtoSourceCodeArtifact(
            zip_artifact=ProtoZipArtifact(
                jfrog_artifact_path=(
                    self.jfrog_artifact_path.to_proto()
                    if self.jfrog_artifact_path
                    else None
                ),
                path=self.qwak_artifact_path,
                main_file=self.main_file,
            )
        )


class SourceCodeSpec(BaseModel):
    artifact: Optional[SourceCodeArtifact] = Field(default=None)

    @classmethod
    def _from_proto(cls, proto: ProtoSourceCodeSpec) -> "SourceCodeSpec":
        artifact_type: str = proto.artifact.WhichOneof("type")
        if artifact_type == "zip_artifact":
            return cls(artifact=ZipArtifact._from_proto(proto.artifact))

        return cls(artifact=None)

    def _to_proto(self) -> ProtoSourceCodeSpec:
        if self.artifact:
            return ProtoSourceCodeSpec(artifact=self.artifact._to_proto())
        return ProtoSourceCodeSpec()
