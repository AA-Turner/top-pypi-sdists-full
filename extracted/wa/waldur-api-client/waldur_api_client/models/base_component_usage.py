import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="BaseComponentUsage")


@_attrs_define
class BaseComponentUsage:
    """
    Attributes:
        uuid (UUID):
        created (datetime.datetime):
        type_ (str): Unique internal name of the measured unit, for example floating_ip.
        name (str): Display name for the measured unit, for example, Floating IP.
        measured_unit (str): Unit of measurement, for example, GB.
        date (datetime.datetime):
        description (Union[Unset, str]):
        usage (Union[Unset, str]):
        recurring (Union[Unset, bool]): Reported value is reused every month until changed.
    """

    uuid: UUID
    created: datetime.datetime
    type_: str
    name: str
    measured_unit: str
    date: datetime.datetime
    description: Union[Unset, str] = UNSET
    usage: Union[Unset, str] = UNSET
    recurring: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        created = self.created.isoformat()

        type_ = self.type_

        name = self.name

        measured_unit = self.measured_unit

        date = self.date.isoformat()

        description = self.description

        usage = self.usage

        recurring = self.recurring

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "created": created,
                "type": type_,
                "name": name,
                "measured_unit": measured_unit,
                "date": date,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if usage is not UNSET:
            field_dict["usage"] = usage
        if recurring is not UNSET:
            field_dict["recurring"] = recurring

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        created = isoparse(d.pop("created"))

        type_ = d.pop("type")

        name = d.pop("name")

        measured_unit = d.pop("measured_unit")

        date = isoparse(d.pop("date"))

        description = d.pop("description", UNSET)

        usage = d.pop("usage", UNSET)

        recurring = d.pop("recurring", UNSET)

        base_component_usage = cls(
            uuid=uuid,
            created=created,
            type_=type_,
            name=name,
            measured_unit=measured_unit,
            date=date,
            description=description,
            usage=usage,
            recurring=recurring,
        )

        base_component_usage.additional_properties = d
        return base_component_usage

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
