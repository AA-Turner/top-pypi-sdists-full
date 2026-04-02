import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="ResourceMissingUsage")


@_attrs_define
class ResourceMissingUsage:
    """
    Attributes:
        uuid (UUID): UUID of the resource
        name (str): Name of the resource
        state (str): Current state of the resource
        created (datetime.datetime): Creation date of the resource
        offering_name (str): Name of the offering
        offering_uuid (UUID): UUID of the offering
        provider_name (str): Name of the service provider
        provider_uuid (UUID): UUID of the service provider
        customer_name (str): Name of the customer organization
        customer_uuid (UUID): UUID of the customer organization
        project_name (str): Name of the project
        project_uuid (UUID): UUID of the project
        last_usage_date (Union[None, datetime.datetime]): Date of the last usage report
        days_since_last_report (Union[None, int]): Number of days since last usage report
    """

    uuid: UUID
    name: str
    state: str
    created: datetime.datetime
    offering_name: str
    offering_uuid: UUID
    provider_name: str
    provider_uuid: UUID
    customer_name: str
    customer_uuid: UUID
    project_name: str
    project_uuid: UUID
    last_usage_date: Union[None, datetime.datetime]
    days_since_last_report: Union[None, int]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        name = self.name

        state = self.state

        created = self.created.isoformat()

        offering_name = self.offering_name

        offering_uuid = str(self.offering_uuid)

        provider_name = self.provider_name

        provider_uuid = str(self.provider_uuid)

        customer_name = self.customer_name

        customer_uuid = str(self.customer_uuid)

        project_name = self.project_name

        project_uuid = str(self.project_uuid)

        last_usage_date: Union[None, str]
        if isinstance(self.last_usage_date, datetime.datetime):
            last_usage_date = self.last_usage_date.isoformat()
        else:
            last_usage_date = self.last_usage_date

        days_since_last_report: Union[None, int]
        days_since_last_report = self.days_since_last_report

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "state": state,
                "created": created,
                "offering_name": offering_name,
                "offering_uuid": offering_uuid,
                "provider_name": provider_name,
                "provider_uuid": provider_uuid,
                "customer_name": customer_name,
                "customer_uuid": customer_uuid,
                "project_name": project_name,
                "project_uuid": project_uuid,
                "last_usage_date": last_usage_date,
                "days_since_last_report": days_since_last_report,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        state = d.pop("state")

        created = isoparse(d.pop("created"))

        offering_name = d.pop("offering_name")

        offering_uuid = UUID(d.pop("offering_uuid"))

        provider_name = d.pop("provider_name")

        provider_uuid = UUID(d.pop("provider_uuid"))

        customer_name = d.pop("customer_name")

        customer_uuid = UUID(d.pop("customer_uuid"))

        project_name = d.pop("project_name")

        project_uuid = UUID(d.pop("project_uuid"))

        def _parse_last_usage_date(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_usage_date_type_0 = isoparse(data)

                return last_usage_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        last_usage_date = _parse_last_usage_date(d.pop("last_usage_date"))

        def _parse_days_since_last_report(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        days_since_last_report = _parse_days_since_last_report(d.pop("days_since_last_report"))

        resource_missing_usage = cls(
            uuid=uuid,
            name=name,
            state=state,
            created=created,
            offering_name=offering_name,
            offering_uuid=offering_uuid,
            provider_name=provider_name,
            provider_uuid=provider_uuid,
            customer_name=customer_name,
            customer_uuid=customer_uuid,
            project_name=project_name,
            project_uuid=project_uuid,
            last_usage_date=last_usage_date,
            days_since_last_report=days_since_last_report,
        )

        resource_missing_usage.additional_properties = d
        return resource_missing_usage

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
