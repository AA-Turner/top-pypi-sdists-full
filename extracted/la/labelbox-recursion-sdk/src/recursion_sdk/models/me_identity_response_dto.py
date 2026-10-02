from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from uuid import UUID






T = TypeVar("T", bound="MeIdentityResponseDto")



@_attrs_define
class MeIdentityResponseDto:
    """ Identity payload for the currently-authenticated caller.

        Example:
            {'id': '49dea803-7390-49c4-abb1-5629718fc9cd'}

        Attributes:
            id (UUID): Stable identifier of the authenticated user.
     """

    id: UUID





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        me_identity_response_dto = cls(
            id=id,
        )

        return me_identity_response_dto

