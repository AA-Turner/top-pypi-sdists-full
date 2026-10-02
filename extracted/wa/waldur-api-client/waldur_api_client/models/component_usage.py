import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ComponentUsage")


@_attrs_define
class ComponentUsage:
    """
    Attributes:
        uuid (Union[Unset, UUID]):
        created (Union[Unset, datetime.datetime]):
        description (Union[Unset, str]):
        type_ (Union[Unset, str]): Unique internal name of the measured unit, for example floating_ip.
        name (Union[Unset, str]): Display name for the measured unit, for example, Floating IP.
        measured_unit (Union[Unset, str]): Unit of measurement, for example, GB.
        usage (Union[Unset, int]):
        date (Union[Unset, datetime.datetime]):
        recurring (Union[Unset, bool]): Reported value is reused every month until changed.
        resource_name (Union[Unset, str]):
        resource_uuid (Union[Unset, UUID]):
        offering_name (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        project_name (Union[Unset, str]):
        project_uuid (Union[Unset, str]):
        customer_name (Union[Unset, str]):
        customer_uuid (Union[Unset, str]):
        billing_period (Union[Unset, datetime.date]):
        modified_by (Union[None, Unset, int]):
    """

    uuid: Union[Unset, UUID] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    description: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    measured_unit: Union[Unset, str] = UNSET
    usage: Union[Unset, int] = UNSET
    date: Union[Unset, datetime.datetime] = UNSET
    recurring: Union[Unset, bool] = UNSET
    resource_name: Union[Unset, str] = UNSET
    resource_uuid: Union[Unset, UUID] = UNSET
    offering_name: Union[Unset, str] = UNSET
    offering_uuid: Union[Unset, UUID] = UNSET
    project_name: Union[Unset, str] = UNSET
    project_uuid: Union[Unset, str] = UNSET
    customer_name: Union[Unset, str] = UNSET
    customer_uuid: Union[Unset, str] = UNSET
    billing_period: Union[Unset, datetime.date] = UNSET
    modified_by: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        description = self.description

        type_ = self.type_

        name = self.name

        measured_unit = self.measured_unit

        usage = self.usage

        date: Union[Unset, str] = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.isoformat()

        recurring = self.recurring

        resource_name = self.resource_name

        resource_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.resource_uuid, Unset):
            resource_uuid = str(self.resource_uuid)

        offering_name = self.offering_name

        offering_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.offering_uuid, Unset):
            offering_uuid = str(self.offering_uuid)

        project_name = self.project_name

        project_uuid = self.project_uuid

        customer_name = self.customer_name

        customer_uuid = self.customer_uuid

        billing_period: Union[Unset, str] = UNSET
        if not isinstance(self.billing_period, Unset):
            billing_period = self.billing_period.isoformat()

        modified_by: Union[None, Unset, int]
        if isinstance(self.modified_by, Unset):
            modified_by = UNSET
        else:
            modified_by = self.modified_by

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if created is not UNSET:
            field_dict["created"] = created
        if description is not UNSET:
            field_dict["description"] = description
        if type_ is not UNSET:
            field_dict["type"] = type_
        if name is not UNSET:
            field_dict["name"] = name
        if measured_unit is not UNSET:
            field_dict["measured_unit"] = measured_unit
        if usage is not UNSET:
            field_dict["usage"] = usage
        if date is not UNSET:
            field_dict["date"] = date
        if recurring is not UNSET:
            field_dict["recurring"] = recurring
        if resource_name is not UNSET:
            field_dict["resource_name"] = resource_name
        if resource_uuid is not UNSET:
            field_dict["resource_uuid"] = resource_uuid
        if offering_name is not UNSET:
            field_dict["offering_name"] = offering_name
        if offering_uuid is not UNSET:
            field_dict["offering_uuid"] = offering_uuid
        if project_name is not UNSET:
            field_dict["project_name"] = project_name
        if project_uuid is not UNSET:
            field_dict["project_uuid"] = project_uuid
        if customer_name is not UNSET:
            field_dict["customer_name"] = customer_name
        if customer_uuid is not UNSET:
            field_dict["customer_uuid"] = customer_uuid
        if billing_period is not UNSET:
            field_dict["billing_period"] = billing_period
        if modified_by is not UNSET:
            field_dict["modified_by"] = modified_by

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        description = d.pop("description", UNSET)

        type_ = d.pop("type", UNSET)

        name = d.pop("name", UNSET)

        measured_unit = d.pop("measured_unit", UNSET)

        usage = d.pop("usage", UNSET)

        _date = d.pop("date", UNSET)
        date: Union[Unset, datetime.datetime]
        if isinstance(_date, Unset):
            date = UNSET
        else:
            date = isoparse(_date)

        recurring = d.pop("recurring", UNSET)

        resource_name = d.pop("resource_name", UNSET)

        _resource_uuid = d.pop("resource_uuid", UNSET)
        resource_uuid: Union[Unset, UUID]
        if isinstance(_resource_uuid, Unset):
            resource_uuid = UNSET
        else:
            resource_uuid = UUID(_resource_uuid)

        offering_name = d.pop("offering_name", UNSET)

        _offering_uuid = d.pop("offering_uuid", UNSET)
        offering_uuid: Union[Unset, UUID]
        if isinstance(_offering_uuid, Unset):
            offering_uuid = UNSET
        else:
            offering_uuid = UUID(_offering_uuid)

        project_name = d.pop("project_name", UNSET)

        project_uuid = d.pop("project_uuid", UNSET)

        customer_name = d.pop("customer_name", UNSET)

        customer_uuid = d.pop("customer_uuid", UNSET)

        _billing_period = d.pop("billing_period", UNSET)
        billing_period: Union[Unset, datetime.date]
        if isinstance(_billing_period, Unset):
            billing_period = UNSET
        else:
            billing_period = isoparse(_billing_period).date()

        def _parse_modified_by(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        modified_by = _parse_modified_by(d.pop("modified_by", UNSET))

        component_usage = cls(
            uuid=uuid,
            created=created,
            description=description,
            type_=type_,
            name=name,
            measured_unit=measured_unit,
            usage=usage,
            date=date,
            recurring=recurring,
            resource_name=resource_name,
            resource_uuid=resource_uuid,
            offering_name=offering_name,
            offering_uuid=offering_uuid,
            project_name=project_name,
            project_uuid=project_uuid,
            customer_name=customer_name,
            customer_uuid=customer_uuid,
            billing_period=billing_period,
            modified_by=modified_by,
        )

        component_usage.additional_properties = d
        return component_usage

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
