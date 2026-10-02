from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.glauth_tree_scope_type_enum import GlauthTreeScopeTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="GlauthTreeScope")


@_attrs_define
class GlauthTreeScope:
    """
    Attributes:
        type_ (GlauthTreeScopeTypeEnum):
        uuid (str):
        name (Union[None, str]):
        slug (Union[None, Unset, str]):
        resource_uuid (Union[None, Unset, str]):
    """

    type_: GlauthTreeScopeTypeEnum
    uuid: str
    name: Union[None, str]
    slug: Union[None, Unset, str] = UNSET
    resource_uuid: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        uuid = self.uuid

        name: Union[None, str]
        name = self.name

        slug: Union[None, Unset, str]
        if isinstance(self.slug, Unset):
            slug = UNSET
        else:
            slug = self.slug

        resource_uuid: Union[None, Unset, str]
        if isinstance(self.resource_uuid, Unset):
            resource_uuid = UNSET
        else:
            resource_uuid = self.resource_uuid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "uuid": uuid,
                "name": name,
            }
        )
        if slug is not UNSET:
            field_dict["slug"] = slug
        if resource_uuid is not UNSET:
            field_dict["resource_uuid"] = resource_uuid

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = GlauthTreeScopeTypeEnum(d.pop("type"))

        uuid = d.pop("uuid")

        def _parse_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        name = _parse_name(d.pop("name"))

        def _parse_slug(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        slug = _parse_slug(d.pop("slug", UNSET))

        def _parse_resource_uuid(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        resource_uuid = _parse_resource_uuid(d.pop("resource_uuid", UNSET))

        glauth_tree_scope = cls(
            type_=type_,
            uuid=uuid,
            name=name,
            slug=slug,
            resource_uuid=resource_uuid,
        )

        glauth_tree_scope.additional_properties = d
        return glauth_tree_scope

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
