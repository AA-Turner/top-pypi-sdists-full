from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.auth_type_enum import AuthTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="PreviewServiceAttributesRequestRequest")


@_attrs_define
class PreviewServiceAttributesRequestRequest:
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
        external_network_id (Union[Unset, str]): Selected external network ID Default: ''.
        instance_availability_zone (Union[Unset, str]): Selected instance availability zone name Default: ''.
        volume_availability_zone (Union[Unset, str]): Selected volume availability zone name Default: ''.
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
    external_network_id: Union[Unset, str] = ""
    instance_availability_zone: Union[Unset, str] = ""
    volume_availability_zone: Union[Unset, str] = ""
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

        external_network_id = self.external_network_id

        instance_availability_zone = self.instance_availability_zone

        volume_availability_zone = self.volume_availability_zone

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
        if external_network_id is not UNSET:
            field_dict["external_network_id"] = external_network_id
        if instance_availability_zone is not UNSET:
            field_dict["instance_availability_zone"] = instance_availability_zone
        if volume_availability_zone is not UNSET:
            field_dict["volume_availability_zone"] = volume_availability_zone

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

        external_network_id = d.pop("external_network_id", UNSET)

        instance_availability_zone = d.pop("instance_availability_zone", UNSET)

        volume_availability_zone = d.pop("volume_availability_zone", UNSET)

        preview_service_attributes_request_request = cls(
            auth_url=auth_url,
            username=username,
            password=password,
            user_domain_name=user_domain_name,
            project_domain_name=project_domain_name,
            project_name=project_name,
            auth_type=auth_type,
            verify_ssl=verify_ssl,
            certificate=certificate,
            external_network_id=external_network_id,
            instance_availability_zone=instance_availability_zone,
            volume_availability_zone=volume_availability_zone,
        )

        preview_service_attributes_request_request.additional_properties = d
        return preview_service_attributes_request_request

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
