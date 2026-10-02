from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="AttachExistingFormResponseDto")



@_attrs_define
class AttachExistingFormResponseDto:
    """ Acknowledgement response indicating an existing form was attached successfully.

        Example:
            {'ok': True}

        Attributes:
            ok (bool): Always true when the attach succeeded.
     """

    ok: bool





    def to_dict(self) -> dict[str, Any]:
        ok = self.ok


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "ok": ok,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ok = d.pop("ok")

        attach_existing_form_response_dto = cls(
            ok=ok,
        )

        return attach_existing_form_response_dto

