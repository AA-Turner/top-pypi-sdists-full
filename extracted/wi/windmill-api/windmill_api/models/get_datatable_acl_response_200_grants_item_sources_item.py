from typing import Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GetDatatableAclResponse200GrantsItemSourcesItem")


@_attrs_define
class GetDatatableAclResponse200GrantsItemSourcesItem:
    """
    Attributes:
        role (str):
        privileges (List[str]): what role gave of the grant's privileges. A revoke is held back only by a source out of
            reach that gave some of what it takes back.
        reachable (bool): whether the data table's connection can take back what role gave. On an object that is the
            owner, when the connection acts for the owner, and otherwise the connection itself; for a default privilege, a
            creating role the connection acts for. What a source out of reach gave is not revocable from here; privileges
            only other sources gave still are.
    """

    role: str
    privileges: List[str]
    reachable: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        role = self.role
        privileges = self.privileges

        reachable = self.reachable

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "role": role,
                "privileges": privileges,
                "reachable": reachable,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        role = d.pop("role")

        privileges = cast(List[str], d.pop("privileges"))

        reachable = d.pop("reachable")

        get_datatable_acl_response_200_grants_item_sources_item = cls(
            role=role,
            privileges=privileges,
            reachable=reachable,
        )

        get_datatable_acl_response_200_grants_item_sources_item.additional_properties = d
        return get_datatable_acl_response_200_grants_item_sources_item

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
