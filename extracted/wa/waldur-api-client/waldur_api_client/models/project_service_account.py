import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.service_account_state import ServiceAccountState
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectServiceAccount")


@_attrs_define
class ProjectServiceAccount:
    """
    Attributes:
        url (str):
        uuid (UUID):
        created (datetime.datetime):
        modified (datetime.datetime):
        error_message (str):
        state (ServiceAccountState):
        token (Union[None, str]):
        expires_at (Union[None, str]):
        project (UUID):
        project_uuid (UUID):
        project_name (str):
        customer_uuid (UUID):
        customer_name (str):
        customer_abbreviation (str):
        username (Union[Unset, str]):
        description (Union[Unset, str]):
        error_traceback (Union[Unset, str]):
        email (Union[Unset, str]):
        preferred_identifier (Union[Unset, str]):
    """

    url: str
    uuid: UUID
    created: datetime.datetime
    modified: datetime.datetime
    error_message: str
    state: ServiceAccountState
    token: Union[None, str]
    expires_at: Union[None, str]
    project: UUID
    project_uuid: UUID
    project_name: str
    customer_uuid: UUID
    customer_name: str
    customer_abbreviation: str
    username: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    error_traceback: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    preferred_identifier: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        error_message = self.error_message

        state = self.state.value

        token: Union[None, str]
        token = self.token

        expires_at: Union[None, str]
        expires_at = self.expires_at

        project = str(self.project)

        project_uuid = str(self.project_uuid)

        project_name = self.project_name

        customer_uuid = str(self.customer_uuid)

        customer_name = self.customer_name

        customer_abbreviation = self.customer_abbreviation

        username = self.username

        description = self.description

        error_traceback = self.error_traceback

        email = self.email

        preferred_identifier = self.preferred_identifier

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "created": created,
                "modified": modified,
                "error_message": error_message,
                "state": state,
                "token": token,
                "expires_at": expires_at,
                "project": project,
                "project_uuid": project_uuid,
                "project_name": project_name,
                "customer_uuid": customer_uuid,
                "customer_name": customer_name,
                "customer_abbreviation": customer_abbreviation,
            }
        )
        if username is not UNSET:
            field_dict["username"] = username
        if description is not UNSET:
            field_dict["description"] = description
        if error_traceback is not UNSET:
            field_dict["error_traceback"] = error_traceback
        if email is not UNSET:
            field_dict["email"] = email
        if preferred_identifier is not UNSET:
            field_dict["preferred_identifier"] = preferred_identifier

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        error_message = d.pop("error_message")

        state = ServiceAccountState(d.pop("state"))

        def _parse_token(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        token = _parse_token(d.pop("token"))

        def _parse_expires_at(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        expires_at = _parse_expires_at(d.pop("expires_at"))

        project = UUID(d.pop("project"))

        project_uuid = UUID(d.pop("project_uuid"))

        project_name = d.pop("project_name")

        customer_uuid = UUID(d.pop("customer_uuid"))

        customer_name = d.pop("customer_name")

        customer_abbreviation = d.pop("customer_abbreviation")

        username = d.pop("username", UNSET)

        description = d.pop("description", UNSET)

        error_traceback = d.pop("error_traceback", UNSET)

        email = d.pop("email", UNSET)

        preferred_identifier = d.pop("preferred_identifier", UNSET)

        project_service_account = cls(
            url=url,
            uuid=uuid,
            created=created,
            modified=modified,
            error_message=error_message,
            state=state,
            token=token,
            expires_at=expires_at,
            project=project,
            project_uuid=project_uuid,
            project_name=project_name,
            customer_uuid=customer_uuid,
            customer_name=customer_name,
            customer_abbreviation=customer_abbreviation,
            username=username,
            description=description,
            error_traceback=error_traceback,
            email=email,
            preferred_identifier=preferred_identifier,
        )

        project_service_account.additional_properties = d
        return project_service_account

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
