from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="PlatformConfigResponseDto")



@_attrs_define
class PlatformConfigResponseDto:
    """ Platform-level configuration values exposed to clients.

        Attributes:
            grader_base_image (str): Container image reference used as the base for grader execution environments.
     """

    grader_base_image: str





    def to_dict(self) -> dict[str, Any]:
        grader_base_image = self.grader_base_image


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "graderBaseImage": grader_base_image,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        grader_base_image = d.pop("graderBaseImage")

        platform_config_response_dto = cls(
            grader_base_image=grader_base_image,
        )

        return platform_config_response_dto

