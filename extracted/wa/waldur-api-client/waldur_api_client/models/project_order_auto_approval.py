import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectOrderAutoApproval")


@_attrs_define
class ProjectOrderAutoApproval:
    """
    Attributes:
        uuid (UUID):
        url (str):
        project (str):
        project_name (str):
        project_uuid (UUID):
        customer_name (str):
        customer_uuid (UUID):
        monthly_cost_limit (str):
        created (datetime.datetime):
        modified (datetime.datetime):
        created_by_uuid (UUID):
        created_by_username (str): Required. 128 characters or fewer. Lowercase letters, numbers and @/./+/-/_
            characters
        created_by_full_name (str):
        modified_by_uuid (UUID):
        modified_by_username (str): Required. 128 characters or fewer. Lowercase letters, numbers and @/./+/-/_
            characters
        modified_by_full_name (str):
        enabled (Union[Unset, bool]):
    """

    uuid: UUID
    url: str
    project: str
    project_name: str
    project_uuid: UUID
    customer_name: str
    customer_uuid: UUID
    monthly_cost_limit: str
    created: datetime.datetime
    modified: datetime.datetime
    created_by_uuid: UUID
    created_by_username: str
    created_by_full_name: str
    modified_by_uuid: UUID
    modified_by_username: str
    modified_by_full_name: str
    enabled: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        url = self.url

        project = self.project

        project_name = self.project_name

        project_uuid = str(self.project_uuid)

        customer_name = self.customer_name

        customer_uuid = str(self.customer_uuid)

        monthly_cost_limit = self.monthly_cost_limit

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        created_by_uuid = str(self.created_by_uuid)

        created_by_username = self.created_by_username

        created_by_full_name = self.created_by_full_name

        modified_by_uuid = str(self.modified_by_uuid)

        modified_by_username = self.modified_by_username

        modified_by_full_name = self.modified_by_full_name

        enabled = self.enabled

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "url": url,
                "project": project,
                "project_name": project_name,
                "project_uuid": project_uuid,
                "customer_name": customer_name,
                "customer_uuid": customer_uuid,
                "monthly_cost_limit": monthly_cost_limit,
                "created": created,
                "modified": modified,
                "created_by_uuid": created_by_uuid,
                "created_by_username": created_by_username,
                "created_by_full_name": created_by_full_name,
                "modified_by_uuid": modified_by_uuid,
                "modified_by_username": modified_by_username,
                "modified_by_full_name": modified_by_full_name,
            }
        )
        if enabled is not UNSET:
            field_dict["enabled"] = enabled

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        url = d.pop("url")

        project = d.pop("project")

        project_name = d.pop("project_name")

        project_uuid = UUID(d.pop("project_uuid"))

        customer_name = d.pop("customer_name")

        customer_uuid = UUID(d.pop("customer_uuid"))

        monthly_cost_limit = d.pop("monthly_cost_limit")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        created_by_uuid = UUID(d.pop("created_by_uuid"))

        created_by_username = d.pop("created_by_username")

        created_by_full_name = d.pop("created_by_full_name")

        modified_by_uuid = UUID(d.pop("modified_by_uuid"))

        modified_by_username = d.pop("modified_by_username")

        modified_by_full_name = d.pop("modified_by_full_name")

        enabled = d.pop("enabled", UNSET)

        project_order_auto_approval = cls(
            uuid=uuid,
            url=url,
            project=project,
            project_name=project_name,
            project_uuid=project_uuid,
            customer_name=customer_name,
            customer_uuid=customer_uuid,
            monthly_cost_limit=monthly_cost_limit,
            created=created,
            modified=modified,
            created_by_uuid=created_by_uuid,
            created_by_username=created_by_username,
            created_by_full_name=created_by_full_name,
            modified_by_uuid=modified_by_uuid,
            modified_by_username=modified_by_username,
            modified_by_full_name=modified_by_full_name,
            enabled=enabled,
        )

        project_order_auto_approval.additional_properties = d
        return project_order_auto_approval

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
