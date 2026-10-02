from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ManagedAgentsSessionMetadataValuesResponse")



@_attrs_define
class ManagedAgentsSessionMetadataValuesResponse:
    """ Response body of GET /v1/sessions/metadata-values: the distinct values one caller-defined metadata key takes across
    the sessions the caller may list.

        Example:
            {'truncated': True, 'values': ['example']}

        Attributes:
            values (list[str]): Distinct values the key takes on sessions the caller may list, sorted, narrowed to the q
                prefix when one was given. Always an array; empty when nothing matches.
            truncated (bool | Unset): True when more distinct values match than limit allowed. The list is sorted, so narrow
                with a longer q prefix rather than paging.
     """

    values: list[str]
    truncated: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        values = self.values



        truncated = self.truncated


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "values": values,
        })
        if truncated is not UNSET:
            field_dict["truncated"] = truncated

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        values = cast(list[str], d.pop("values"))


        truncated = d.pop("truncated", UNSET)

        managed_agents_session_metadata_values_response = cls(
            values=values,
            truncated=truncated,
        )


        managed_agents_session_metadata_values_response.additional_properties = d
        return managed_agents_session_metadata_values_response

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
