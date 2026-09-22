from typing import Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.plan_datatable_acl_json_body_change_type_1_scope import PlanDatatableAclJsonBodyChangeType1Scope
from ..models.plan_datatable_acl_json_body_change_type_1_type import PlanDatatableAclJsonBodyChangeType1Type

T = TypeVar("T", bound="PlanDatatableAclJsonBodyChangeType1")


@_attrs_define
class PlanDatatableAclJsonBodyChangeType1:
    """
    Attributes:
        type (PlanDatatableAclJsonBodyChangeType1Type):
        role (str): a data table role of the instance, or admin
        privileges (List[str]):
        scope (PlanDatatableAclJsonBodyChangeType1Scope):
    """

    type: PlanDatatableAclJsonBodyChangeType1Type
    role: str
    privileges: List[str]
    scope: PlanDatatableAclJsonBodyChangeType1Scope
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
        type = PlanDatatableAclJsonBodyChangeType1Type(d.pop("type"))

        role = d.pop("role")

        privileges = cast(List[str], d.pop("privileges"))

        scope = PlanDatatableAclJsonBodyChangeType1Scope(d.pop("scope"))

        plan_datatable_acl_json_body_change_type_1 = cls(
            type=type,
            role=role,
            privileges=privileges,
            scope=scope,
        )

        plan_datatable_acl_json_body_change_type_1.additional_properties = d
        return plan_datatable_acl_json_body_change_type_1

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
