from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from uuid import UUID






T = TypeVar("T", bound="PublicEnvironmentListItemPageDtoItemsItem")



@_attrs_define
class PublicEnvironmentListItemPageDtoItemsItem:
    """ A public-catalog entry exposing one environment to unauthenticated visitors.

        Attributes:
            id (UUID): Stable public-environment identifier (UUID).
            environment_id (UUID): Underlying environment this public listing surfaces.
            environment_name (str): Display name of the environment shown in the public catalog.
            description (str): Marketing-friendly description shown in the public catalog.
            image_url (str): Cover image URL displayed alongside the public listing.
            is_featured (bool): True when this environment is currently featured on the public landing page.
     """

    id: UUID
    environment_id: UUID
    environment_name: str
    description: str
    image_url: str
    is_featured: bool





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        environment_id = str(self.environment_id)

        environment_name = self.environment_name

        description = self.description

        image_url = self.image_url

        is_featured = self.is_featured


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "environmentId": environment_id,
            "environmentName": environment_name,
            "description": description,
            "imageUrl": image_url,
            "isFeatured": is_featured,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        environment_id = UUID(d.pop("environmentId"))




        environment_name = d.pop("environmentName")

        description = d.pop("description")

        image_url = d.pop("imageUrl")

        is_featured = d.pop("isFeatured")

        public_environment_list_item_page_dto_items_item = cls(
            id=id,
            environment_id=environment_id,
            environment_name=environment_name,
            description=description,
            image_url=image_url,
            is_featured=is_featured,
        )

        return public_environment_list_item_page_dto_items_item

