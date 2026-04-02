from collections.abc import Mapping
from io import BytesIO
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from .. import types
from ..types import UNSET, File, Unset

T = TypeVar("T", bound="MarketplaceCategoryRequest")


@_attrs_define
class MarketplaceCategoryRequest:
    """
    Attributes:
        title (str):
        description (Union[Unset, str]):
        icon (Union[File, None, Unset]):
        default_vm_category (Union[Unset, bool]): Set to "true" if this category is for OpenStack VM. Only one category
            can have "true" value.
        default_volume_category (Union[Unset, bool]): Set to true if this category is for OpenStack Volume. Only one
            category can have "true" value.
        default_tenant_category (Union[Unset, bool]): Set to true if this category is for OpenStack Tenant. Only one
            category can have "true" value.
        group (Union[None, Unset, str]):
    """

    title: str
    description: Union[Unset, str] = UNSET
    icon: Union[File, None, Unset] = UNSET
    default_vm_category: Union[Unset, bool] = UNSET
    default_volume_category: Union[Unset, bool] = UNSET
    default_tenant_category: Union[Unset, bool] = UNSET
    group: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        description = self.description

        icon: Union[None, Unset, types.FileTypes]
        if isinstance(self.icon, Unset):
            icon = UNSET
        elif isinstance(self.icon, File):
            icon = self.icon.to_tuple()

        else:
            icon = self.icon

        default_vm_category = self.default_vm_category

        default_volume_category = self.default_volume_category

        default_tenant_category = self.default_tenant_category

        group: Union[None, Unset, str]
        if isinstance(self.group, Unset):
            group = UNSET
        else:
            group = self.group

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if icon is not UNSET:
            field_dict["icon"] = icon
        if default_vm_category is not UNSET:
            field_dict["default_vm_category"] = default_vm_category
        if default_volume_category is not UNSET:
            field_dict["default_volume_category"] = default_volume_category
        if default_tenant_category is not UNSET:
            field_dict["default_tenant_category"] = default_tenant_category
        if group is not UNSET:
            field_dict["group"] = group

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        title = d.pop("title")

        description = d.pop("description", UNSET)

        def _parse_icon(data: object) -> Union[File, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, bytes):
                    raise TypeError()
                icon_type_0 = File(payload=BytesIO(data))

                return icon_type_0
            except:  # noqa: E722
                pass
            return cast(Union[File, None, Unset], data)

        icon = _parse_icon(d.pop("icon", UNSET))

        default_vm_category = d.pop("default_vm_category", UNSET)

        default_volume_category = d.pop("default_volume_category", UNSET)

        default_tenant_category = d.pop("default_tenant_category", UNSET)

        def _parse_group(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        group = _parse_group(d.pop("group", UNSET))

        marketplace_category_request = cls(
            title=title,
            description=description,
            icon=icon,
            default_vm_category=default_vm_category,
            default_volume_category=default_volume_category,
            default_tenant_category=default_tenant_category,
            group=group,
        )

        marketplace_category_request.additional_properties = d
        return marketplace_category_request

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
