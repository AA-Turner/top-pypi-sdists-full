from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="SetupInstallation")



@_attrs_define
class SetupInstallation:
    """ 
        Attributes:
            id (int):
            account_login (str):
            saved (bool): Whether this installation is the one the board reads.
     """

    id: int
    account_login: str
    saved: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        account_login = self.account_login

        saved = self.saved


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "accountLogin": account_login,
            "saved": saved,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        account_login = d.pop("accountLogin")

        saved = d.pop("saved")

        setup_installation = cls(
            id=id,
            account_login=account_login,
            saved=saved,
        )


        setup_installation.additional_properties = d
        return setup_installation

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
