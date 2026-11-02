from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.auto_update_unavailable_code import AutoUpdateUnavailableCode






T = TypeVar("T", bound="AutoUpdateUnavailable")



@_attrs_define
class AutoUpdateUnavailable:
    """ 
        Attributes:
            code (AutoUpdateUnavailableCode):
            reason (str): A sentence a client can show as it is.
     """

    code: AutoUpdateUnavailableCode
    reason: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        code = self.code.value

        reason = self.reason


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "code": code,
            "reason": reason,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        code = AutoUpdateUnavailableCode(d.pop("code"))




        reason = d.pop("reason")

        auto_update_unavailable = cls(
            code=code,
            reason=reason,
        )


        auto_update_unavailable.additional_properties = d
        return auto_update_unavailable

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
