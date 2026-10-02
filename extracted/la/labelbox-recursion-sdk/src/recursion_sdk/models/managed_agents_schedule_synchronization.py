from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_schedule_synchronization_status import ManagedAgentsScheduleSynchronizationStatus
from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsScheduleSynchronization")



@_attrs_define
class ManagedAgentsScheduleSynchronization:
    """ Delivery status of saved schedule configuration, independent of run outcomes.

        Example:
            {'error': 'example', 'status': 'pending'}

        Attributes:
            status (ManagedAgentsScheduleSynchronizationStatus): Whether the saved configuration has reached Temporal.
            error (str | Unset): Safe synchronization failure summary; synchronization is retried automatically.
     """

    status: ManagedAgentsScheduleSynchronizationStatus
    error: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        error = self.error


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "status": status,
        })
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = ManagedAgentsScheduleSynchronizationStatus(d.pop("status"))




        error = d.pop("error", UNSET)

        managed_agents_schedule_synchronization = cls(
            status=status,
            error=error,
        )


        managed_agents_schedule_synchronization.additional_properties = d
        return managed_agents_schedule_synchronization

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
