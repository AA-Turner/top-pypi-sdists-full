import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="RemoteProjectAllocationEntry")


@_attrs_define
class RemoteProjectAllocationEntry:
    """
    Attributes:
        id (int):
        allocation (str): New total allocation (credits) after this change.
        delta (str):
        source_project_name (str):
        source_project_uuid (UUID):
        submitted_at (datetime.datetime):
        is_confirmed (bool):
        previous_allocation (Union[None, Unset, str]): Total allocation before this change.  Null for the first entry.
        confirmed_at (Union[None, Unset, datetime.datetime]): When the remote portal confirmed this allocation.  Null if
            pending.
        note (Union[Unset, str]): Optional comment, e.g. 'carrying over 20 unused credits from previous award'.
    """

    id: int
    allocation: str
    delta: str
    source_project_name: str
    source_project_uuid: UUID
    submitted_at: datetime.datetime
    is_confirmed: bool
    previous_allocation: Union[None, Unset, str] = UNSET
    confirmed_at: Union[None, Unset, datetime.datetime] = UNSET
    note: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        allocation = self.allocation

        delta = self.delta

        source_project_name = self.source_project_name

        source_project_uuid = str(self.source_project_uuid)

        submitted_at = self.submitted_at.isoformat()

        is_confirmed = self.is_confirmed

        previous_allocation: Union[None, Unset, str]
        if isinstance(self.previous_allocation, Unset):
            previous_allocation = UNSET
        else:
            previous_allocation = self.previous_allocation

        confirmed_at: Union[None, Unset, str]
        if isinstance(self.confirmed_at, Unset):
            confirmed_at = UNSET
        elif isinstance(self.confirmed_at, datetime.datetime):
            confirmed_at = self.confirmed_at.isoformat()
        else:
            confirmed_at = self.confirmed_at

        note = self.note

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "allocation": allocation,
                "delta": delta,
                "source_project_name": source_project_name,
                "source_project_uuid": source_project_uuid,
                "submitted_at": submitted_at,
                "is_confirmed": is_confirmed,
            }
        )
        if previous_allocation is not UNSET:
            field_dict["previous_allocation"] = previous_allocation
        if confirmed_at is not UNSET:
            field_dict["confirmed_at"] = confirmed_at
        if note is not UNSET:
            field_dict["note"] = note

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        allocation = d.pop("allocation")

        delta = d.pop("delta")

        source_project_name = d.pop("source_project_name")

        source_project_uuid = UUID(d.pop("source_project_uuid"))

        submitted_at = isoparse(d.pop("submitted_at"))

        is_confirmed = d.pop("is_confirmed")

        def _parse_previous_allocation(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        previous_allocation = _parse_previous_allocation(d.pop("previous_allocation", UNSET))

        def _parse_confirmed_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                confirmed_at_type_0 = isoparse(data)

                return confirmed_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        confirmed_at = _parse_confirmed_at(d.pop("confirmed_at", UNSET))

        note = d.pop("note", UNSET)

        remote_project_allocation_entry = cls(
            id=id,
            allocation=allocation,
            delta=delta,
            source_project_name=source_project_name,
            source_project_uuid=source_project_uuid,
            submitted_at=submitted_at,
            is_confirmed=is_confirmed,
            previous_allocation=previous_allocation,
            confirmed_at=confirmed_at,
            note=note,
        )

        remote_project_allocation_entry.additional_properties = d
        return remote_project_allocation_entry

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
