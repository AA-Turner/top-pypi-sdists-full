from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="ImageDetailDto")



@_attrs_define
class ImageDetailDto:
    """ Detailed view of a runtime image including its compatible models.

        Example:
            {'id': 'claude-code', 'displayName': 'Claude Code', 'version': 'latest', 'defaultImage': 'us-
                docker.pkg.dev/example-project/recursion-images/claude-code:latest', 'models': ['claude-sonnet-4-6', 'claude-
                opus-4-6']}

        Attributes:
            id (str): Stable identifier for a runtime container image.
            display_name (str): Human-readable name of the image shown in selection UIs.
            version (str): Image version tag identifying the published build.
            default_image (str): Fully-qualified default container image reference used when this image is selected.
            models (list[str]): Models compatible with this image.
     """

    id: str
    display_name: str
    version: str
    default_image: str
    models: list[str]





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        display_name = self.display_name

        version = self.version

        default_image = self.default_image

        models = self.models




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "displayName": display_name,
            "version": version,
            "defaultImage": default_image,
            "models": models,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        display_name = d.pop("displayName")

        version = d.pop("version")

        default_image = d.pop("defaultImage")

        models = cast(list[str], d.pop("models"))


        image_detail_dto = cls(
            id=id,
            display_name=display_name,
            version=version,
            default_image=default_image,
            models=models,
        )

        return image_detail_dto

