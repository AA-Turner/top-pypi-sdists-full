from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RancherCatalogCreateRequest")


@_attrs_define
class RancherCatalogCreateRequest:
    """
    Attributes:
        name (str):
        catalog_url (str):
        branch (str):
        scope (str):
        description (Union[Unset, str]):
        username (Union[Unset, str]):
        password (Union[Unset, str]):
    """

    name: str
    catalog_url: str
    branch: str
    scope: str
    description: Union[Unset, str] = UNSET
    username: Union[Unset, str] = UNSET
    password: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        catalog_url = self.catalog_url

        branch = self.branch

        scope = self.scope

        description = self.description

        username = self.username

        password = self.password

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "catalog_url": catalog_url,
                "branch": branch,
                "scope": scope,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if username is not UNSET:
            field_dict["username"] = username
        if password is not UNSET:
            field_dict["password"] = password

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        catalog_url = d.pop("catalog_url")

        branch = d.pop("branch")

        scope = d.pop("scope")

        description = d.pop("description", UNSET)

        username = d.pop("username", UNSET)

        password = d.pop("password", UNSET)

        rancher_catalog_create_request = cls(
            name=name,
            catalog_url=catalog_url,
            branch=branch,
            scope=scope,
            description=description,
            username=username,
            password=password,
        )

        rancher_catalog_create_request.additional_properties = d
        return rancher_catalog_create_request

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
