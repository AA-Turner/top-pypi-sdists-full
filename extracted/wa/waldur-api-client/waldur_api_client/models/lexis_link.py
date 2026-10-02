import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="LexisLink")


@_attrs_define
class LexisLink:
    """
    Attributes:
        url (str):
        uuid (UUID):
        created (datetime.datetime):
        modified (datetime.datetime):
        robot_account (str):
        robot_account_username (str):
        robot_account_type (str):
        state (str):
        resource_uuid (UUID):
        resource_name (str):
        resource_type (str):
        resource_backend_id (str):
        resource_end_date (datetime.datetime):
        project_uuid (UUID):
        project_name (str):
        customer_uuid (UUID):
        customer_name (str):
        heappe_project_id (Union[None, Unset, int]):
    """

    url: str
    uuid: UUID
    created: datetime.datetime
    modified: datetime.datetime
    robot_account: str
    robot_account_username: str
    robot_account_type: str
    state: str
    resource_uuid: UUID
    resource_name: str
    resource_type: str
    resource_backend_id: str
    resource_end_date: datetime.datetime
    project_uuid: UUID
    project_name: str
    customer_uuid: UUID
    customer_name: str
    heappe_project_id: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        robot_account = self.robot_account

        robot_account_username = self.robot_account_username

        robot_account_type = self.robot_account_type

        state = self.state

        resource_uuid = str(self.resource_uuid)

        resource_name = self.resource_name

        resource_type = self.resource_type

        resource_backend_id = self.resource_backend_id

        resource_end_date = self.resource_end_date.isoformat()

        project_uuid = str(self.project_uuid)

        project_name = self.project_name

        customer_uuid = str(self.customer_uuid)

        customer_name = self.customer_name

        heappe_project_id: Union[None, Unset, int]
        if isinstance(self.heappe_project_id, Unset):
            heappe_project_id = UNSET
        else:
            heappe_project_id = self.heappe_project_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "created": created,
                "modified": modified,
                "robot_account": robot_account,
                "robot_account_username": robot_account_username,
                "robot_account_type": robot_account_type,
                "state": state,
                "resource_uuid": resource_uuid,
                "resource_name": resource_name,
                "resource_type": resource_type,
                "resource_backend_id": resource_backend_id,
                "resource_end_date": resource_end_date,
                "project_uuid": project_uuid,
                "project_name": project_name,
                "customer_uuid": customer_uuid,
                "customer_name": customer_name,
            }
        )
        if heappe_project_id is not UNSET:
            field_dict["heappe_project_id"] = heappe_project_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        robot_account = d.pop("robot_account")

        robot_account_username = d.pop("robot_account_username")

        robot_account_type = d.pop("robot_account_type")

        state = d.pop("state")

        resource_uuid = UUID(d.pop("resource_uuid"))

        resource_name = d.pop("resource_name")

        resource_type = d.pop("resource_type")

        resource_backend_id = d.pop("resource_backend_id")

        resource_end_date = isoparse(d.pop("resource_end_date"))

        project_uuid = UUID(d.pop("project_uuid"))

        project_name = d.pop("project_name")

        customer_uuid = UUID(d.pop("customer_uuid"))

        customer_name = d.pop("customer_name")

        def _parse_heappe_project_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        heappe_project_id = _parse_heappe_project_id(d.pop("heappe_project_id", UNSET))

        lexis_link = cls(
            url=url,
            uuid=uuid,
            created=created,
            modified=modified,
            robot_account=robot_account,
            robot_account_username=robot_account_username,
            robot_account_type=robot_account_type,
            state=state,
            resource_uuid=resource_uuid,
            resource_name=resource_name,
            resource_type=resource_type,
            resource_backend_id=resource_backend_id,
            resource_end_date=resource_end_date,
            project_uuid=project_uuid,
            project_name=project_name,
            customer_uuid=customer_uuid,
            customer_name=customer_name,
            heappe_project_id=heappe_project_id,
        )

        lexis_link.additional_properties = d
        return lexis_link

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
