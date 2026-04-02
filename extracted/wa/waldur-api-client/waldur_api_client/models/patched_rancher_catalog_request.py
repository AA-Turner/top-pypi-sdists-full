from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedRancherCatalogRequest")


@_attrs_define
class PatchedRancherCatalogRequest:
    """
    Attributes:
        name (Union[Unset, str]):
        description (Union[Unset, str]):
        catalog_url (Union[Unset, str]):
        branch (Union[Unset, str]):
        scope (Union[Unset, str]):
    """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    catalog_url: Union[Unset, str] = UNSET
    branch: Union[Unset, str] = UNSET
    scope: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        catalog_url = self.catalog_url

        branch = self.branch

        scope = self.scope

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if catalog_url is not UNSET:
            field_dict["catalog_url"] = catalog_url
        if branch is not UNSET:
            field_dict["branch"] = branch
        if scope is not UNSET:
            field_dict["scope"] = scope

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        catalog_url = d.pop("catalog_url", UNSET)

        branch = d.pop("branch", UNSET)

        scope = d.pop("scope", UNSET)

        patched_rancher_catalog_request = cls(
            name=name,
            description=description,
            catalog_url=catalog_url,
            branch=branch,
            scope=scope,
        )

        patched_rancher_catalog_request.additional_properties = d
        return patched_rancher_catalog_request

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
