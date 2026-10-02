from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="EnvFormBundleResponseDtoFormType0")



@_attrs_define
class EnvFormBundleResponseDtoFormType0:
    """ A versioned structured-input form, attached to an environment or specific problem.

        Attributes:
            id (UUID): Stable form identifier (UUID). Forms are versioned structured-input schemas.
            title (None | str): Human-readable title for the bundle, surfaced in org catalog and picker UIs. Null when the
                bundle has not been named yet.
            created_at (datetime.datetime): Timestamp when the form was created (ISO-8601, UTC).
            updated_at (datetime.datetime): Timestamp when the form was last updated (ISO-8601, UTC).
     """

    id: UUID
    title: None | str
    created_at: datetime.datetime
    updated_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        title: None | str
        title = self.title

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "title": title,
            "createdAt": created_at,
            "updatedAt": updated_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        def _parse_title(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        title = _parse_title(d.pop("title"))


        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))




        env_form_bundle_response_dto_form_type_0 = cls(
            id=id,
            title=title,
            created_at=created_at,
            updated_at=updated_at,
        )

        return env_form_bundle_response_dto_form_type_0

