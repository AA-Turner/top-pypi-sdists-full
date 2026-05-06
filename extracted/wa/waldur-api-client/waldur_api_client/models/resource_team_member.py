import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.nested_resource_project_permission import NestedResourceProjectPermission


T = TypeVar("T", bound="ResourceTeamMember")


@_attrs_define
class ResourceTeamMember:
    """
    Attributes:
        url (str):
        uuid (UUID):
        username (str): Required. 128 characters or fewer. Lowercase letters, numbers and @/./+/-/_ characters
        full_name (str):
        role_name (Union[None, str]):
        role_uuid (Union[None, str]):
        expiration_time (Union[None, datetime.datetime]):
        resource_projects (list['NestedResourceProjectPermission']):
        email (Union[Unset, str]):
        image (Union[None, Unset, str]):
    """

    url: str
    uuid: UUID
    username: str
    full_name: str
    role_name: Union[None, str]
    role_uuid: Union[None, str]
    expiration_time: Union[None, datetime.datetime]
    resource_projects: list["NestedResourceProjectPermission"]
    email: Union[Unset, str] = UNSET
    image: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        username = self.username

        full_name = self.full_name

        role_name: Union[None, str]
        role_name = self.role_name

        role_uuid: Union[None, str]
        role_uuid = self.role_uuid

        expiration_time: Union[None, str]
        if isinstance(self.expiration_time, datetime.datetime):
            expiration_time = self.expiration_time.isoformat()
        else:
            expiration_time = self.expiration_time

        resource_projects = []
        for resource_projects_item_data in self.resource_projects:
            resource_projects_item = resource_projects_item_data.to_dict()
            resource_projects.append(resource_projects_item)

        email = self.email

        image: Union[None, Unset, str]
        if isinstance(self.image, Unset):
            image = UNSET
        else:
            image = self.image

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "username": username,
                "full_name": full_name,
                "role_name": role_name,
                "role_uuid": role_uuid,
                "expiration_time": expiration_time,
                "resource_projects": resource_projects,
            }
        )
        if email is not UNSET:
            field_dict["email"] = email
        if image is not UNSET:
            field_dict["image"] = image

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.nested_resource_project_permission import NestedResourceProjectPermission

        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        username = d.pop("username")

        full_name = d.pop("full_name")

        def _parse_role_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        role_name = _parse_role_name(d.pop("role_name"))

        def _parse_role_uuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        role_uuid = _parse_role_uuid(d.pop("role_uuid"))

        def _parse_expiration_time(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expiration_time_type_0 = isoparse(data)

                return expiration_time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        expiration_time = _parse_expiration_time(d.pop("expiration_time"))

        resource_projects = []
        _resource_projects = d.pop("resource_projects")
        for resource_projects_item_data in _resource_projects:
            resource_projects_item = NestedResourceProjectPermission.from_dict(resource_projects_item_data)

            resource_projects.append(resource_projects_item)

        email = d.pop("email", UNSET)

        def _parse_image(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        image = _parse_image(d.pop("image", UNSET))

        resource_team_member = cls(
            url=url,
            uuid=uuid,
            username=username,
            full_name=full_name,
            role_name=role_name,
            role_uuid=role_uuid,
            expiration_time=expiration_time,
            resource_projects=resource_projects,
            email=email,
            image=image,
        )

        resource_team_member.additional_properties = d
        return resource_team_member

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
