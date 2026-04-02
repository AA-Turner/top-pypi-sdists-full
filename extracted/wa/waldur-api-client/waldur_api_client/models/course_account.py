import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.course_account_state_enum import CourseAccountStateEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="CourseAccount")


@_attrs_define
class CourseAccount:
    """
    Attributes:
        url (str):
        uuid (UUID):
        created (datetime.datetime):
        modified (datetime.datetime):
        project (UUID):
        project_uuid (UUID):
        project_name (str):
        project_slug (str):
        project_start_date (datetime.date):
        project_end_date (datetime.date):
        user_uuid (UUID):
        username (str):
        customer_uuid (UUID):
        customer_name (str):
        state (CourseAccountStateEnum):
        error_message (str):
        error_traceback (str):
        email (Union[Unset, str]):
        description (Union[Unset, str]):
    """

    url: str
    uuid: UUID
    created: datetime.datetime
    modified: datetime.datetime
    project: UUID
    project_uuid: UUID
    project_name: str
    project_slug: str
    project_start_date: datetime.date
    project_end_date: datetime.date
    user_uuid: UUID
    username: str
    customer_uuid: UUID
    customer_name: str
    state: CourseAccountStateEnum
    error_message: str
    error_traceback: str
    email: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        project = str(self.project)

        project_uuid = str(self.project_uuid)

        project_name = self.project_name

        project_slug = self.project_slug

        project_start_date = self.project_start_date.isoformat()

        project_end_date = self.project_end_date.isoformat()

        user_uuid = str(self.user_uuid)

        username = self.username

        customer_uuid = str(self.customer_uuid)

        customer_name = self.customer_name

        state = self.state.value

        error_message = self.error_message

        error_traceback = self.error_traceback

        email = self.email

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "created": created,
                "modified": modified,
                "project": project,
                "project_uuid": project_uuid,
                "project_name": project_name,
                "project_slug": project_slug,
                "project_start_date": project_start_date,
                "project_end_date": project_end_date,
                "user_uuid": user_uuid,
                "username": username,
                "customer_uuid": customer_uuid,
                "customer_name": customer_name,
                "state": state,
                "error_message": error_message,
                "error_traceback": error_traceback,
            }
        )
        if email is not UNSET:
            field_dict["email"] = email
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        project = UUID(d.pop("project"))

        project_uuid = UUID(d.pop("project_uuid"))

        project_name = d.pop("project_name")

        project_slug = d.pop("project_slug")

        project_start_date = isoparse(d.pop("project_start_date")).date()

        project_end_date = isoparse(d.pop("project_end_date")).date()

        user_uuid = UUID(d.pop("user_uuid"))

        username = d.pop("username")

        customer_uuid = UUID(d.pop("customer_uuid"))

        customer_name = d.pop("customer_name")

        state = CourseAccountStateEnum(d.pop("state"))

        error_message = d.pop("error_message")

        error_traceback = d.pop("error_traceback")

        email = d.pop("email", UNSET)

        description = d.pop("description", UNSET)

        course_account = cls(
            url=url,
            uuid=uuid,
            created=created,
            modified=modified,
            project=project,
            project_uuid=project_uuid,
            project_name=project_name,
            project_slug=project_slug,
            project_start_date=project_start_date,
            project_end_date=project_end_date,
            user_uuid=user_uuid,
            username=username,
            customer_uuid=customer_uuid,
            customer_name=customer_name,
            state=state,
            error_message=error_message,
            error_traceback=error_traceback,
            email=email,
            description=description,
        )

        course_account.additional_properties = d
        return course_account

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
