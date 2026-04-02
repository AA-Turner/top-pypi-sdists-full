from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ServerInfo")


@_attrs_define
class ServerInfo:
    """
    Attributes:
        auth_url (str):
        identity_api_version (str):
        user_domain_name (str):
        project_name (str):
        project_id (str):
    """

    auth_url: str
    identity_api_version: str
    user_domain_name: str
    project_name: str
    project_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        auth_url = self.auth_url

        identity_api_version = self.identity_api_version

        user_domain_name = self.user_domain_name

        project_name = self.project_name

        project_id = self.project_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "auth_url": auth_url,
                "identity_api_version": identity_api_version,
                "user_domain_name": user_domain_name,
                "project_name": project_name,
                "project_id": project_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        auth_url = d.pop("auth_url")

        identity_api_version = d.pop("identity_api_version")

        user_domain_name = d.pop("user_domain_name")

        project_name = d.pop("project_name")

        project_id = d.pop("project_id")

        server_info = cls(
            auth_url=auth_url,
            identity_api_version=identity_api_version,
            user_domain_name=user_domain_name,
            project_name=project_name,
            project_id=project_id,
        )

        server_info.additional_properties = d
        return server_info

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
