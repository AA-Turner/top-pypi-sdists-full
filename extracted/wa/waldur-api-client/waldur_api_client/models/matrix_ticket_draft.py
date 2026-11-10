import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.matrix_ticket_draft_state_enum import MatrixTicketDraftStateEnum

T = TypeVar("T", bound="MatrixTicketDraft")


@_attrs_define
class MatrixTicketDraft:
    """
    Attributes:
        uuid (str):
        state (MatrixTicketDraftStateEnum):
        title (str):
        description (str):
        request_type (str):
        priority (str):
        project_uuid (str):
        project_name (str):
        customer_uuid (str):
        customer_name (str):
        resource_uuid (Union[None, str]):
        resource_name (str):
        resource_offering_name (str):
        helpdesk (str):
        expires_at (datetime.datetime):
        issue_uuid (Union[None, str]):
        issue_key (Union[None, str]):
        issue_url (Union[None, str]):
    """

    uuid: str
    state: MatrixTicketDraftStateEnum
    title: str
    description: str
    request_type: str
    priority: str
    project_uuid: str
    project_name: str
    customer_uuid: str
    customer_name: str
    resource_uuid: Union[None, str]
    resource_name: str
    resource_offering_name: str
    helpdesk: str
    expires_at: datetime.datetime
    issue_uuid: Union[None, str]
    issue_key: Union[None, str]
    issue_url: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = self.uuid

        state = self.state.value

        title = self.title

        description = self.description

        request_type = self.request_type

        priority = self.priority

        project_uuid = self.project_uuid

        project_name = self.project_name

        customer_uuid = self.customer_uuid

        customer_name = self.customer_name

        resource_uuid: Union[None, str]
        resource_uuid = self.resource_uuid

        resource_name = self.resource_name

        resource_offering_name = self.resource_offering_name

        helpdesk = self.helpdesk

        expires_at = self.expires_at.isoformat()

        issue_uuid: Union[None, str]
        issue_uuid = self.issue_uuid

        issue_key: Union[None, str]
        issue_key = self.issue_key

        issue_url: Union[None, str]
        issue_url = self.issue_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "state": state,
                "title": title,
                "description": description,
                "request_type": request_type,
                "priority": priority,
                "project_uuid": project_uuid,
                "project_name": project_name,
                "customer_uuid": customer_uuid,
                "customer_name": customer_name,
                "resource_uuid": resource_uuid,
                "resource_name": resource_name,
                "resource_offering_name": resource_offering_name,
                "helpdesk": helpdesk,
                "expires_at": expires_at,
                "issue_uuid": issue_uuid,
                "issue_key": issue_key,
                "issue_url": issue_url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = d.pop("uuid")

        state = MatrixTicketDraftStateEnum(d.pop("state"))

        title = d.pop("title")

        description = d.pop("description")

        request_type = d.pop("request_type")

        priority = d.pop("priority")

        project_uuid = d.pop("project_uuid")

        project_name = d.pop("project_name")

        customer_uuid = d.pop("customer_uuid")

        customer_name = d.pop("customer_name")

        def _parse_resource_uuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        resource_uuid = _parse_resource_uuid(d.pop("resource_uuid"))

        resource_name = d.pop("resource_name")

        resource_offering_name = d.pop("resource_offering_name")

        helpdesk = d.pop("helpdesk")

        expires_at = isoparse(d.pop("expires_at"))

        def _parse_issue_uuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        issue_uuid = _parse_issue_uuid(d.pop("issue_uuid"))

        def _parse_issue_key(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        issue_key = _parse_issue_key(d.pop("issue_key"))

        def _parse_issue_url(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        issue_url = _parse_issue_url(d.pop("issue_url"))

        matrix_ticket_draft = cls(
            uuid=uuid,
            state=state,
            title=title,
            description=description,
            request_type=request_type,
            priority=priority,
            project_uuid=project_uuid,
            project_name=project_name,
            customer_uuid=customer_uuid,
            customer_name=customer_name,
            resource_uuid=resource_uuid,
            resource_name=resource_name,
            resource_offering_name=resource_offering_name,
            helpdesk=helpdesk,
            expires_at=expires_at,
            issue_uuid=issue_uuid,
            issue_key=issue_key,
            issue_url=issue_url,
        )

        matrix_ticket_draft.additional_properties = d
        return matrix_ticket_draft

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
