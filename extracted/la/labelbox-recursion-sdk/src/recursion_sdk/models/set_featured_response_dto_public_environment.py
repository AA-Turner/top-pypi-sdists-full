from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="SetFeaturedResponseDtoPublicEnvironment")



@_attrs_define
class SetFeaturedResponseDtoPublicEnvironment:
    """ Updated public-environment record after the featured flag was toggled.

        Attributes:
            id (UUID): Stable public-environment identifier (UUID).
            environment_id (UUID): Underlying environment this public listing surfaces.
            environment_name (str): Display name of the environment shown in the public catalog.
            description (str): Marketing-friendly description shown in the public catalog.
            image_url (str): Cover image URL displayed alongside the public listing.
            is_featured (bool): True when this environment is currently featured on the public landing page.
            featured_at (datetime.datetime | None): Timestamp when the environment was most recently featured (ISO-8601,
                UTC). Null if never featured.
            created_at (datetime.datetime): Timestamp when the public-environment record was created (ISO-8601, UTC).
            updated_at (datetime.datetime): Timestamp when the public-environment record was last updated (ISO-8601, UTC).
            preview_filename (None | str): Output filename resolved as a thumbnail on each problem card, or null when
                preview is not configured.
     """

    id: UUID
    environment_id: UUID
    environment_name: str
    description: str
    image_url: str
    is_featured: bool
    featured_at: datetime.datetime | None
    created_at: datetime.datetime
    updated_at: datetime.datetime
    preview_filename: None | str





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        environment_id = str(self.environment_id)

        environment_name = self.environment_name

        description = self.description

        image_url = self.image_url

        is_featured = self.is_featured

        featured_at: None | str
        if isinstance(self.featured_at, datetime.datetime):
            featured_at = self.featured_at.isoformat()
        else:
            featured_at = self.featured_at

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        preview_filename: None | str
        preview_filename = self.preview_filename


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "environmentId": environment_id,
            "environmentName": environment_name,
            "description": description,
            "imageUrl": image_url,
            "isFeatured": is_featured,
            "featuredAt": featured_at,
            "createdAt": created_at,
            "updatedAt": updated_at,
            "previewFilename": preview_filename,
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

        def _parse_featured_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                featured_at_type_0 = datetime.datetime.fromisoformat(data)



                return featured_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        featured_at = _parse_featured_at(d.pop("featuredAt"))


        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))




        def _parse_preview_filename(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        preview_filename = _parse_preview_filename(d.pop("previewFilename"))


        set_featured_response_dto_public_environment = cls(
            id=id,
            environment_id=environment_id,
            environment_name=environment_name,
            description=description,
            image_url=image_url,
            is_featured=is_featured,
            featured_at=featured_at,
            created_at=created_at,
            updated_at=updated_at,
            preview_filename=preview_filename,
        )

        return set_featured_response_dto_public_environment

