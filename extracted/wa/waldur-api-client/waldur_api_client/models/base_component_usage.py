import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.missing_usage_policy_enum import MissingUsagePolicyEnum
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
        recurring (bool): Deprecated, use missing_usage_policy instead. True when the reported value is reused every
            month until changed.
        description (Union[Unset, str]):
        usage (Union[Unset, str]):
        missing_usage_policy (Union[Unset, MissingUsagePolicyEnum]):
    """

    uuid: UUID
    created: datetime.datetime
    type_: str
    name: str
    measured_unit: str
    date: datetime.datetime
    recurring: bool
    description: Union[Unset, str] = UNSET
    usage: Union[Unset, str] = UNSET
    missing_usage_policy: Union[Unset, MissingUsagePolicyEnum] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        created = self.created.isoformat()

        type_ = self.type_

        name = self.name

        measured_unit = self.measured_unit

        date = self.date.isoformat()

        recurring = self.recurring

        description = self.description

        usage = self.usage

        missing_usage_policy: Union[Unset, str] = UNSET
        if not isinstance(self.missing_usage_policy, Unset):
            missing_usage_policy = self.missing_usage_policy.value

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
                "recurring": recurring,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if usage is not UNSET:
            field_dict["usage"] = usage
        if missing_usage_policy is not UNSET:
            field_dict["missing_usage_policy"] = missing_usage_policy

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

        recurring = d.pop("recurring")

        description = d.pop("description", UNSET)

        usage = d.pop("usage", UNSET)

        _missing_usage_policy = d.pop("missing_usage_policy", UNSET)
        missing_usage_policy: Union[Unset, MissingUsagePolicyEnum]
        if isinstance(_missing_usage_policy, Unset):
            missing_usage_policy = UNSET
        else:
            missing_usage_policy = MissingUsagePolicyEnum(_missing_usage_policy)

        base_component_usage = cls(
            uuid=uuid,
            created=created,
            type_=type_,
            name=name,
            measured_unit=measured_unit,
            date=date,
            recurring=recurring,
            description=description,
            usage=usage,
            missing_usage_policy=missing_usage_policy,
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
