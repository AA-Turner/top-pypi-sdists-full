import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProviderTicket")


@_attrs_define
class ProviderTicket:
    """
    Attributes:
        url (str):
        uuid (UUID):
        key (str):
        summary (str):
        description (str):
        type_ (str):
        status (str):
        priority (str):
        created (datetime.datetime):
        modified (datetime.datetime):
        parent_issue_key (str):
        parent_issue_uuid (UUID):
        is_escalated (bool): Whether this issue has been escalated.
        provider_assignee (Union[None, UUID]):
        provider_assignee_name (str):
        first_response_deadline (Union[None, datetime.datetime]): Deadline for first response from support staff.
        resolution_deadline (Union[None, datetime.datetime]): Deadline for issue resolution.
        first_response_at (Union[None, datetime.datetime]): Timestamp of first response from support staff.
        sla_breached (bool): Whether SLA has been breached for this issue.
        customer_uuid (Union[None, UUID]):
        customer_name (Union[None, str]):
        project_uuid (Union[None, UUID]):
        project_name (Union[None, str]):
        escalated_at (Union[None, Unset, datetime.datetime]): When the issue was escalated.
        customer (Union[None, Unset, str]):
        project (Union[None, Unset, str]):
    """

    url: str
    uuid: UUID
    key: str
    summary: str
    description: str
    type_: str
    status: str
    priority: str
    created: datetime.datetime
    modified: datetime.datetime
    parent_issue_key: str
    parent_issue_uuid: UUID
    is_escalated: bool
    provider_assignee: Union[None, UUID]
    provider_assignee_name: str
    first_response_deadline: Union[None, datetime.datetime]
    resolution_deadline: Union[None, datetime.datetime]
    first_response_at: Union[None, datetime.datetime]
    sla_breached: bool
    customer_uuid: Union[None, UUID]
    customer_name: Union[None, str]
    project_uuid: Union[None, UUID]
    project_name: Union[None, str]
    escalated_at: Union[None, Unset, datetime.datetime] = UNSET
    customer: Union[None, Unset, str] = UNSET
    project: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        key = self.key

        summary = self.summary

        description = self.description

        type_ = self.type_

        status = self.status

        priority = self.priority

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        parent_issue_key = self.parent_issue_key

        parent_issue_uuid = str(self.parent_issue_uuid)

        is_escalated = self.is_escalated

        provider_assignee: Union[None, str]
        if isinstance(self.provider_assignee, UUID):
            provider_assignee = str(self.provider_assignee)
        else:
            provider_assignee = self.provider_assignee

        provider_assignee_name = self.provider_assignee_name

        first_response_deadline: Union[None, str]
        if isinstance(self.first_response_deadline, datetime.datetime):
            first_response_deadline = self.first_response_deadline.isoformat()
        else:
            first_response_deadline = self.first_response_deadline

        resolution_deadline: Union[None, str]
        if isinstance(self.resolution_deadline, datetime.datetime):
            resolution_deadline = self.resolution_deadline.isoformat()
        else:
            resolution_deadline = self.resolution_deadline

        first_response_at: Union[None, str]
        if isinstance(self.first_response_at, datetime.datetime):
            first_response_at = self.first_response_at.isoformat()
        else:
            first_response_at = self.first_response_at

        sla_breached = self.sla_breached

        customer_uuid: Union[None, str]
        if isinstance(self.customer_uuid, UUID):
            customer_uuid = str(self.customer_uuid)
        else:
            customer_uuid = self.customer_uuid

        customer_name: Union[None, str]
        customer_name = self.customer_name

        project_uuid: Union[None, str]
        if isinstance(self.project_uuid, UUID):
            project_uuid = str(self.project_uuid)
        else:
            project_uuid = self.project_uuid

        project_name: Union[None, str]
        project_name = self.project_name

        escalated_at: Union[None, Unset, str]
        if isinstance(self.escalated_at, Unset):
            escalated_at = UNSET
        elif isinstance(self.escalated_at, datetime.datetime):
            escalated_at = self.escalated_at.isoformat()
        else:
            escalated_at = self.escalated_at

        customer: Union[None, Unset, str]
        if isinstance(self.customer, Unset):
            customer = UNSET
        else:
            customer = self.customer

        project: Union[None, Unset, str]
        if isinstance(self.project, Unset):
            project = UNSET
        else:
            project = self.project

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "key": key,
                "summary": summary,
                "description": description,
                "type": type_,
                "status": status,
                "priority": priority,
                "created": created,
                "modified": modified,
                "parent_issue_key": parent_issue_key,
                "parent_issue_uuid": parent_issue_uuid,
                "is_escalated": is_escalated,
                "provider_assignee": provider_assignee,
                "provider_assignee_name": provider_assignee_name,
                "first_response_deadline": first_response_deadline,
                "resolution_deadline": resolution_deadline,
                "first_response_at": first_response_at,
                "sla_breached": sla_breached,
                "customer_uuid": customer_uuid,
                "customer_name": customer_name,
                "project_uuid": project_uuid,
                "project_name": project_name,
            }
        )
        if escalated_at is not UNSET:
            field_dict["escalated_at"] = escalated_at
        if customer is not UNSET:
            field_dict["customer"] = customer
        if project is not UNSET:
            field_dict["project"] = project

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        key = d.pop("key")

        summary = d.pop("summary")

        description = d.pop("description")

        type_ = d.pop("type")

        status = d.pop("status")

        priority = d.pop("priority")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        parent_issue_key = d.pop("parent_issue_key")

        parent_issue_uuid = UUID(d.pop("parent_issue_uuid"))

        is_escalated = d.pop("is_escalated")

        def _parse_provider_assignee(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                provider_assignee_type_0 = UUID(data)

                return provider_assignee_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        provider_assignee = _parse_provider_assignee(d.pop("provider_assignee"))

        provider_assignee_name = d.pop("provider_assignee_name")

        def _parse_first_response_deadline(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                first_response_deadline_type_0 = isoparse(data)

                return first_response_deadline_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        first_response_deadline = _parse_first_response_deadline(d.pop("first_response_deadline"))

        def _parse_resolution_deadline(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                resolution_deadline_type_0 = isoparse(data)

                return resolution_deadline_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        resolution_deadline = _parse_resolution_deadline(d.pop("resolution_deadline"))

        def _parse_first_response_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                first_response_at_type_0 = isoparse(data)

                return first_response_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        first_response_at = _parse_first_response_at(d.pop("first_response_at"))

        sla_breached = d.pop("sla_breached")

        def _parse_customer_uuid(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                customer_uuid_type_0 = UUID(data)

                return customer_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        customer_uuid = _parse_customer_uuid(d.pop("customer_uuid"))

        def _parse_customer_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        customer_name = _parse_customer_name(d.pop("customer_name"))

        def _parse_project_uuid(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                project_uuid_type_0 = UUID(data)

                return project_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        project_uuid = _parse_project_uuid(d.pop("project_uuid"))

        def _parse_project_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        project_name = _parse_project_name(d.pop("project_name"))

        def _parse_escalated_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                escalated_at_type_0 = isoparse(data)

                return escalated_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        escalated_at = _parse_escalated_at(d.pop("escalated_at", UNSET))

        def _parse_customer(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        customer = _parse_customer(d.pop("customer", UNSET))

        def _parse_project(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        project = _parse_project(d.pop("project", UNSET))

        provider_ticket = cls(
            url=url,
            uuid=uuid,
            key=key,
            summary=summary,
            description=description,
            type_=type_,
            status=status,
            priority=priority,
            created=created,
            modified=modified,
            parent_issue_key=parent_issue_key,
            parent_issue_uuid=parent_issue_uuid,
            is_escalated=is_escalated,
            provider_assignee=provider_assignee,
            provider_assignee_name=provider_assignee_name,
            first_response_deadline=first_response_deadline,
            resolution_deadline=resolution_deadline,
            first_response_at=first_response_at,
            sla_breached=sla_breached,
            customer_uuid=customer_uuid,
            customer_name=customer_name,
            project_uuid=project_uuid,
            project_name=project_name,
            escalated_at=escalated_at,
            customer=customer,
            project=project,
        )

        provider_ticket.additional_properties = d
        return provider_ticket

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
