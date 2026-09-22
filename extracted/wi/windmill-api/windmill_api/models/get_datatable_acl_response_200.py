from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.get_datatable_acl_response_200_grants_item import GetDatatableAclResponse200GrantsItem


T = TypeVar("T", bound="GetDatatableAclResponse200")


@_attrs_define
class GetDatatableAclResponse200:
    """
    Attributes:
        owner (str):
        roles (List[str]): the roles a change may name; empty unless the caller may change anything
        editable (bool): whether the caller may plan and apply changes
        clone (bool): whether this is a clone, whose grants stay as they were copied
        supports_maintain (bool): whether the server is Postgres 17+, which added the MAINTAIN table privilege
        dbname (str): the database the target lives in
        grants (List['GetDatatableAclResponse200GrantsItem']):
        children (List[str]): a database's schemas, or a schema's tables
    """

    owner: str
    roles: List[str]
    editable: bool
    clone: bool
    supports_maintain: bool
    dbname: str
    grants: List["GetDatatableAclResponse200GrantsItem"]
    children: List[str]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        owner = self.owner
        roles = self.roles

        editable = self.editable
        clone = self.clone
        supports_maintain = self.supports_maintain
        dbname = self.dbname
        grants = []
        for grants_item_data in self.grants:
            grants_item = grants_item_data.to_dict()

            grants.append(grants_item)

        children = self.children

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "owner": owner,
                "roles": roles,
                "editable": editable,
                "clone": clone,
                "supports_maintain": supports_maintain,
                "dbname": dbname,
                "grants": grants,
                "children": children,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_datatable_acl_response_200_grants_item import GetDatatableAclResponse200GrantsItem

        d = src_dict.copy()
        owner = d.pop("owner")

        roles = cast(List[str], d.pop("roles"))

        editable = d.pop("editable")

        clone = d.pop("clone")

        supports_maintain = d.pop("supports_maintain")

        dbname = d.pop("dbname")

        grants = []
        _grants = d.pop("grants")
        for grants_item_data in _grants:
            grants_item = GetDatatableAclResponse200GrantsItem.from_dict(grants_item_data)

            grants.append(grants_item)

        children = cast(List[str], d.pop("children"))

        get_datatable_acl_response_200 = cls(
            owner=owner,
            roles=roles,
            editable=editable,
            clone=clone,
            supports_maintain=supports_maintain,
            dbname=dbname,
            grants=grants,
            children=children,
        )

        get_datatable_acl_response_200.additional_properties = d
        return get_datatable_acl_response_200

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
