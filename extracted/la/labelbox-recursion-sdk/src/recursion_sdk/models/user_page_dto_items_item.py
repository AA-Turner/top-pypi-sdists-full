from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="UserPageDtoItemsItem")



@_attrs_define
class UserPageDtoItemsItem:
    """ A user. Represents one human actor with a stable platform identity.

        Attributes:
            id (UUID): Stable user identifier (UUID).
            external_id (None | str): External user identifier from the caller's identity provider. Null for users created
                without an upstream identity link.
            name (str): Display name of the user.
            email (str): Primary contact email of the user.
            created_at (datetime.datetime): Timestamp when the user was created (ISO-8601, UTC).
            updated_at (datetime.datetime): Timestamp when the user was last updated (ISO-8601, UTC).
     """

    id: UUID
    external_id: None | str
    name: str
    email: str
    created_at: datetime.datetime
    updated_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        external_id: None | str
        external_id = self.external_id

        name = self.name

        email = self.email

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "externalId": external_id,
            "name": name,
            "email": email,
            "createdAt": created_at,
            "updatedAt": updated_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        def _parse_external_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        external_id = _parse_external_id(d.pop("externalId"))


        name = d.pop("name")

        email = d.pop("email")

        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))




        user_page_dto_items_item = cls(
            id=id,
            external_id=external_id,
            name=name,
            email=email,
            created_at=created_at,
            updated_at=updated_at,
        )

        return user_page_dto_items_item

