import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="SiteMaintenanceReservationRequest")


@_attrs_define
class SiteMaintenanceReservationRequest:
    """
    Attributes:
        name (str):
        start (datetime.datetime):
        end (datetime.datetime):
        partitions (Union[Unset, list[str]]): Affected partitions; empty means the whole cluster.
        node_list (Union[Unset, str]):  Default: ''.
        flags (Union[Unset, list[str]]):
    """

    name: str
    start: datetime.datetime
    end: datetime.datetime
    partitions: Union[Unset, list[str]] = UNSET
    node_list: Union[Unset, str] = ""
    flags: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        start = self.start.isoformat()

        end = self.end.isoformat()

        partitions: Union[Unset, list[str]] = UNSET
        if not isinstance(self.partitions, Unset):
            partitions = self.partitions

        node_list = self.node_list

        flags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.flags, Unset):
            flags = self.flags

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "start": start,
                "end": end,
            }
        )
        if partitions is not UNSET:
            field_dict["partitions"] = partitions
        if node_list is not UNSET:
            field_dict["node_list"] = node_list
        if flags is not UNSET:
            field_dict["flags"] = flags

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        start = isoparse(d.pop("start"))

        end = isoparse(d.pop("end"))

        partitions = cast(list[str], d.pop("partitions", UNSET))

        node_list = d.pop("node_list", UNSET)

        flags = cast(list[str], d.pop("flags", UNSET))

        site_maintenance_reservation_request = cls(
            name=name,
            start=start,
            end=end,
            partitions=partitions,
            node_list=node_list,
            flags=flags,
        )

        site_maintenance_reservation_request.additional_properties = d
        return site_maintenance_reservation_request

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
