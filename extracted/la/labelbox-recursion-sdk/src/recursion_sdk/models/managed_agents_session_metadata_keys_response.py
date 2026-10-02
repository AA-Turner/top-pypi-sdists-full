from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ManagedAgentsSessionMetadataKeysResponse")



@_attrs_define
class ManagedAgentsSessionMetadataKeysResponse:
    """ Response body of GET /v1/sessions/metadata-keys: the distinct caller-defined metadata keys across the sessions the
    caller may list.

        Example:
            {'keys': ['example'], 'truncated': True}

        Attributes:
            keys (list[str]): Distinct caller-defined metadata keys carried by sessions the caller may list, sorted. Always
                an array; empty when no listed session carries metadata.
            truncated (bool | Unset): True when the organization carries more distinct keys than the response holds. The
                list is sorted, so the missing keys sort after the last one returned.
     """

    keys: list[str]
    truncated: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        keys = self.keys



        truncated = self.truncated


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "keys": keys,
        })
        if truncated is not UNSET:
            field_dict["truncated"] = truncated

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        keys = cast(list[str], d.pop("keys"))


        truncated = d.pop("truncated", UNSET)

        managed_agents_session_metadata_keys_response = cls(
            keys=keys,
            truncated=truncated,
        )


        managed_agents_session_metadata_keys_response.additional_properties = d
        return managed_agents_session_metadata_keys_response

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
