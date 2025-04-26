from dataclasses import dataclass, field
from typing import Optional, Union

from anyscale._private.models.model_base import ModelBase, ModelEnum


class ImageBuildStatus(ModelEnum):
    IN_PROGRESS = "IN_PROGRESS"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"

    def __str__(self):
        return self.name

    __docstrings__ = {
        IN_PROGRESS: "The image build is in progress.",
        SUCCEEDED: "The image build succeeded.",
        FAILED: "The image build failed.",
        UNKNOWN: "The CLI/SDK received an unexpected state from the API server. In most cases, this means you need to update the CLI.",
    }


@dataclass(frozen=True)
class ImageBuild(ModelBase):
    __doc_py_example__ = """\
import anyscale
from anyscale.models import ImageBuild, ImageBuildStatus

image_build: ImageBuild = anyscale.image.get("image-name")
"""
    __doc_cli_example__ = """\
$ anyscale image get -n my-image
uri: anyscale/image/my-image:2
status: SUCCEEDED
"""

    uri: str = field(metadata={"docstring": "The URI of the image for the build."},)

    def _validate_uri(self, uri: str):
        if uri is None or not isinstance(uri, str):
            raise ValueError("The URI of the image must be a string.")

    status: Union[str, ImageBuildStatus] = field(
        metadata={"docstring": "The status of the image build."},
    )

    def _validate_status(self, status: Union[str, ImageBuildStatus]):
        return ImageBuildStatus.validate(status)

    ray_version: Optional[str] = field(
        metadata={"docstring": "The Ray version used for the image build."},
    )

    def _validate_ray_version(self, ray_version: Optional[str]):
        if ray_version is not None and not isinstance(ray_version, str):
            raise ValueError("The Ray version must be a string.")
