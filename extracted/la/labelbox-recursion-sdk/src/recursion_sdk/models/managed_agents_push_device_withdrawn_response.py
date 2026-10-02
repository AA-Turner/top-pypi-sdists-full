from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ManagedAgentsPushDeviceWithdrawnResponse")



@_attrs_define
class ManagedAgentsPushDeviceWithdrawnResponse:
    """ Response body of a device withdrawal.

        Example:
            {'deleted': True}

        Attributes:
            deleted (bool): Always true. The registration is removed, not soft deleted, and nothing more is sent to the
                device; a withdrawal that did not happen is an HTTP error instead, so this field never reports false.
     """

    deleted: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        deleted = self.deleted


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "deleted": deleted,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        deleted = d.pop("deleted")

        managed_agents_push_device_withdrawn_response = cls(
            deleted=deleted,
        )


        managed_agents_push_device_withdrawn_response.additional_properties = d
        return managed_agents_push_device_withdrawn_response

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
