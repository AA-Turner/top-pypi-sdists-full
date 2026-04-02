from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.auth_type_enum import AuthTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="DiscoverVolumeAvailabilityZonesRequestRequest")


@_attrs_define
class DiscoverVolumeAvailabilityZonesRequestRequest:
    """
    Attributes:
        auth_url (str): Keystone auth URL (e.g., https://cloud.example.com:5000/v3)
        username (str):
        password (str):
        user_domain_name (Union[Unset, str]): Keystone user domain name Default: 'Default'.
        project_domain_name (Union[Unset, str]): Keystone project domain name Default: 'Default'.
        project_name (Union[Unset, str]): Keystone project (tenant) name Default: 'admin'.
        auth_type (Union[Unset, AuthTypeEnum]):  Default: AuthTypeEnum.PASSWORD.
        verify_ssl (Union[Unset, bool]):  Default: False.
        certificate (Union[Unset, str]): PEM-encoded CA certificate for SSL verification
    """

    auth_url: str
    username: str
    password: str
    user_domain_name: Union[Unset, str] = "Default"
    project_domain_name: Union[Unset, str] = "Default"
    project_name: Union[Unset, str] = "admin"
    auth_type: Union[Unset, AuthTypeEnum] = AuthTypeEnum.PASSWORD
    verify_ssl: Union[Unset, bool] = False
    certificate: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        auth_url = self.auth_url

        username = self.username

        password = self.password

        user_domain_name = self.user_domain_name

        project_domain_name = self.project_domain_name

        project_name = self.project_name

        auth_type: Union[Unset, str] = UNSET
        if not isinstance(self.auth_type, Unset):
            auth_type = self.auth_type.value

        verify_ssl = self.verify_ssl

        certificate = self.certificate

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "auth_url": auth_url,
                "username": username,
                "password": password,
            }
        )
        if user_domain_name is not UNSET:
            field_dict["user_domain_name"] = user_domain_name
        if project_domain_name is not UNSET:
            field_dict["project_domain_name"] = project_domain_name
        if project_name is not UNSET:
            field_dict["project_name"] = project_name
        if auth_type is not UNSET:
            field_dict["auth_type"] = auth_type
        if verify_ssl is not UNSET:
            field_dict["verify_ssl"] = verify_ssl
        if certificate is not UNSET:
            field_dict["certificate"] = certificate

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        auth_url = d.pop("auth_url")

        username = d.pop("username")

        password = d.pop("password")

        user_domain_name = d.pop("user_domain_name", UNSET)

        project_domain_name = d.pop("project_domain_name", UNSET)

        project_name = d.pop("project_name", UNSET)

        _auth_type = d.pop("auth_type", UNSET)
        auth_type: Union[Unset, AuthTypeEnum]
        if isinstance(_auth_type, Unset):
            auth_type = UNSET
        else:
            auth_type = AuthTypeEnum(_auth_type)

        verify_ssl = d.pop("verify_ssl", UNSET)

        certificate = d.pop("certificate", UNSET)

        discover_volume_availability_zones_request_request = cls(
            auth_url=auth_url,
            username=username,
            password=password,
            user_domain_name=user_domain_name,
            project_domain_name=project_domain_name,
            project_name=project_name,
            auth_type=auth_type,
            verify_ssl=verify_ssl,
            certificate=certificate,
        )

        discover_volume_availability_zones_request_request.additional_properties = d
        return discover_volume_availability_zones_request_request

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
