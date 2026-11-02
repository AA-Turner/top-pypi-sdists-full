from typing import Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.acl_change_type_1_scope import AclChangeType1Scope
from ..models.acl_change_type_1_type import AclChangeType1Type

T = TypeVar("T", bound="AclChangeType1")


@_attrs_define
class AclChangeType1:
    """
    Attributes:
        type (AclChangeType1Type):
        role (str): a data table role of the instance, or admin
        privileges (List[str]):
        scope (AclChangeType1Scope):
    """

    type: AclChangeType1Type
    role: str
    privileges: List[str]
    scope: AclChangeType1Scope
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        role = self.role
        privileges = self.privileges

        scope = self.scope.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "role": role,
                "privileges": privileges,
                "scope": scope,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = AclChangeType1Type(d.pop("type"))

        role = d.pop("role")

        privileges = cast(List[str], d.pop("privileges"))

        scope = AclChangeType1Scope(d.pop("scope"))

        acl_change_type_1 = cls(
            type=type,
            role=role,
            privileges=privileges,
            scope=scope,
        )

        acl_change_type_1.additional_properties = d
        return acl_change_type_1

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
