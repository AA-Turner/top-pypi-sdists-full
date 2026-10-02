from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.set_featured_response_dto_public_environment import SetFeaturedResponseDtoPublicEnvironment





T = TypeVar("T", bound="SetFeaturedResponseDto")



@_attrs_define
class SetFeaturedResponseDto:
    """ Response payload returned after toggling the featured status of a public environment.

        Attributes:
            public_environment (SetFeaturedResponseDtoPublicEnvironment): Updated public-environment record after the
                featured flag was toggled.
            featured_count (int): Total number of environments currently featured after the update.
     """

    public_environment: SetFeaturedResponseDtoPublicEnvironment
    featured_count: int





    def to_dict(self) -> dict[str, Any]:
        from ..models.set_featured_response_dto_public_environment import SetFeaturedResponseDtoPublicEnvironment # noqa: PLC0415
        public_environment = self.public_environment.to_dict()

        featured_count = self.featured_count


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "publicEnvironment": public_environment,
            "featuredCount": featured_count,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.set_featured_response_dto_public_environment import SetFeaturedResponseDtoPublicEnvironment # noqa: PLC0415
        d = dict(src_dict)
        public_environment = SetFeaturedResponseDtoPublicEnvironment.from_dict(d.pop("publicEnvironment"))




        featured_count = d.pop("featuredCount")

        set_featured_response_dto = cls(
            public_environment=public_environment,
            featured_count=featured_count,
        )

        return set_featured_response_dto

