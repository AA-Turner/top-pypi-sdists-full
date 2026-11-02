from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
import datetime






T = TypeVar("T", bound="APITokenCreateRequest")



@_attrs_define
class APITokenCreateRequest:
    """ 
        Attributes:
            label (str):
            expires_at (datetime.datetime): Must be in the future and no more than 366 days out (matching
                GitHub's own fine-grained-token maximum) — the
                Settings UI offers 7/30/60/90-day presets (30 pre-selected)
                or a custom date within that same cap, never an option for
                no expiration at all.
     """

    label: str
    expires_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        label = self.label

        expires_at = self.expires_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "label": label,
            "expiresAt": expires_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        label = d.pop("label")

        expires_at = datetime.datetime.fromisoformat(d.pop("expiresAt"))




        api_token_create_request = cls(
            label=label,
            expires_at=expires_at,
        )


        api_token_create_request.additional_properties = d
        return api_token_create_request

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
