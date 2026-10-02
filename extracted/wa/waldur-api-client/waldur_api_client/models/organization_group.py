from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OrganizationGroup")


@_attrs_define
class OrganizationGroup:
    """
    Attributes:
        uuid (Union[Unset, UUID]):
        url (Union[Unset, str]):
        name (Union[Unset, str]):
        parent_uuid (Union[Unset, UUID]): UUID of the parent organization group
        parent_name (Union[Unset, str]): Name of the parent organization group
        parent (Union[None, Unset, str]):
        customers_count (Union[Unset, int]): Number of customers in this organization group
    """

    uuid: Union[Unset, UUID] = UNSET
    url: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    parent_uuid: Union[Unset, UUID] = UNSET
    parent_name: Union[Unset, str] = UNSET
    parent: Union[None, Unset, str] = UNSET
    customers_count: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        url = self.url

        name = self.name

        parent_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.parent_uuid, Unset):
            parent_uuid = str(self.parent_uuid)

        parent_name = self.parent_name

        parent: Union[None, Unset, str]
        if isinstance(self.parent, Unset):
            parent = UNSET
        else:
            parent = self.parent

        customers_count = self.customers_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if url is not UNSET:
            field_dict["url"] = url
        if name is not UNSET:
            field_dict["name"] = name
        if parent_uuid is not UNSET:
            field_dict["parent_uuid"] = parent_uuid
        if parent_name is not UNSET:
            field_dict["parent_name"] = parent_name
        if parent is not UNSET:
            field_dict["parent"] = parent
        if customers_count is not UNSET:
            field_dict["customers_count"] = customers_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        url = d.pop("url", UNSET)

        name = d.pop("name", UNSET)

        _parent_uuid = d.pop("parent_uuid", UNSET)
        parent_uuid: Union[Unset, UUID]
        if isinstance(_parent_uuid, Unset):
            parent_uuid = UNSET
        else:
            parent_uuid = UUID(_parent_uuid)

        parent_name = d.pop("parent_name", UNSET)

        def _parse_parent(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        parent = _parse_parent(d.pop("parent", UNSET))

        customers_count = d.pop("customers_count", UNSET)

        organization_group = cls(
            uuid=uuid,
            url=url,
            name=name,
            parent_uuid=parent_uuid,
            parent_name=parent_name,
            parent=parent,
            customers_count=customers_count,
        )

        organization_group.additional_properties = d
        return organization_group

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
