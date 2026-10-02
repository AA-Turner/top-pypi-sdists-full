import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ComponentUserUsage")


@_attrs_define
class ComponentUserUsage:
    """
    Attributes:
        uuid (Union[Unset, UUID]):
        user (Union[Unset, str]):
        username (Union[Unset, str]):
        component_usage (Union[Unset, str]):
        usage (Union[Unset, int]):
        measured_unit (Union[Unset, str]): Unit of measurement, for example, GB.
        description (Union[Unset, str]):
        created (Union[Unset, datetime.datetime]):
        modified (Union[Unset, datetime.datetime]):
        backend_id (Union[Unset, str]):
        resource_name (Union[Unset, str]):
        resource_uuid (Union[Unset, UUID]):
        offering_name (Union[Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        project_name (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        customer_name (Union[Unset, str]):
        customer_uuid (Union[Unset, UUID]):
        component_type (Union[Unset, str]): Unique internal name of the measured unit, for example floating_ip.
        date (Union[Unset, datetime.datetime]):
        billing_period (Union[Unset, datetime.date]):
    """

    uuid: Union[Unset, UUID] = UNSET
    user: Union[Unset, str] = UNSET
    username: Union[Unset, str] = UNSET
    component_usage: Union[Unset, str] = UNSET
    usage: Union[Unset, int] = UNSET
    measured_unit: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    modified: Union[Unset, datetime.datetime] = UNSET
    backend_id: Union[Unset, str] = UNSET
    resource_name: Union[Unset, str] = UNSET
    resource_uuid: Union[Unset, UUID] = UNSET
    offering_name: Union[Unset, str] = UNSET
    offering_uuid: Union[Unset, UUID] = UNSET
    project_name: Union[Unset, str] = UNSET
    project_uuid: Union[Unset, UUID] = UNSET
    customer_name: Union[Unset, str] = UNSET
    customer_uuid: Union[Unset, UUID] = UNSET
    component_type: Union[Unset, str] = UNSET
    date: Union[Unset, datetime.datetime] = UNSET
    billing_period: Union[Unset, datetime.date] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        user = self.user

        username = self.username

        component_usage = self.component_usage

        usage = self.usage

        measured_unit = self.measured_unit

        description = self.description

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        modified: Union[Unset, str] = UNSET
        if not isinstance(self.modified, Unset):
            modified = self.modified.isoformat()

        backend_id = self.backend_id

        resource_name = self.resource_name

        resource_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.resource_uuid, Unset):
            resource_uuid = str(self.resource_uuid)

        offering_name = self.offering_name

        offering_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.offering_uuid, Unset):
            offering_uuid = str(self.offering_uuid)

        project_name = self.project_name

        project_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.project_uuid, Unset):
            project_uuid = str(self.project_uuid)

        customer_name = self.customer_name

        customer_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.customer_uuid, Unset):
            customer_uuid = str(self.customer_uuid)

        component_type = self.component_type

        date: Union[Unset, str] = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.isoformat()

        billing_period: Union[Unset, str] = UNSET
        if not isinstance(self.billing_period, Unset):
            billing_period = self.billing_period.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if user is not UNSET:
            field_dict["user"] = user
        if username is not UNSET:
            field_dict["username"] = username
        if component_usage is not UNSET:
            field_dict["component_usage"] = component_usage
        if usage is not UNSET:
            field_dict["usage"] = usage
        if measured_unit is not UNSET:
            field_dict["measured_unit"] = measured_unit
        if description is not UNSET:
            field_dict["description"] = description
        if created is not UNSET:
            field_dict["created"] = created
        if modified is not UNSET:
            field_dict["modified"] = modified
        if backend_id is not UNSET:
            field_dict["backend_id"] = backend_id
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
        if component_type is not UNSET:
            field_dict["component_type"] = component_type
        if date is not UNSET:
            field_dict["date"] = date
        if billing_period is not UNSET:
            field_dict["billing_period"] = billing_period

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

        user = d.pop("user", UNSET)

        username = d.pop("username", UNSET)

        component_usage = d.pop("component_usage", UNSET)

        usage = d.pop("usage", UNSET)

        measured_unit = d.pop("measured_unit", UNSET)

        description = d.pop("description", UNSET)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        _modified = d.pop("modified", UNSET)
        modified: Union[Unset, datetime.datetime]
        if isinstance(_modified, Unset):
            modified = UNSET
        else:
            modified = isoparse(_modified)

        backend_id = d.pop("backend_id", UNSET)

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

        _project_uuid = d.pop("project_uuid", UNSET)
        project_uuid: Union[Unset, UUID]
        if isinstance(_project_uuid, Unset):
            project_uuid = UNSET
        else:
            project_uuid = UUID(_project_uuid)

        customer_name = d.pop("customer_name", UNSET)

        _customer_uuid = d.pop("customer_uuid", UNSET)
        customer_uuid: Union[Unset, UUID]
        if isinstance(_customer_uuid, Unset):
            customer_uuid = UNSET
        else:
            customer_uuid = UUID(_customer_uuid)

        component_type = d.pop("component_type", UNSET)

        _date = d.pop("date", UNSET)
        date: Union[Unset, datetime.datetime]
        if isinstance(_date, Unset):
            date = UNSET
        else:
            date = isoparse(_date)

        _billing_period = d.pop("billing_period", UNSET)
        billing_period: Union[Unset, datetime.date]
        if isinstance(_billing_period, Unset):
            billing_period = UNSET
        else:
            billing_period = isoparse(_billing_period).date()

        component_user_usage = cls(
            uuid=uuid,
            user=user,
            username=username,
            component_usage=component_usage,
            usage=usage,
            measured_unit=measured_unit,
            description=description,
            created=created,
            modified=modified,
            backend_id=backend_id,
            resource_name=resource_name,
            resource_uuid=resource_uuid,
            offering_name=offering_name,
            offering_uuid=offering_uuid,
            project_name=project_name,
            project_uuid=project_uuid,
            customer_name=customer_name,
            customer_uuid=customer_uuid,
            component_type=component_type,
            date=date,
            billing_period=billing_period,
        )

        component_user_usage.additional_properties = d
        return component_user_usage

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
