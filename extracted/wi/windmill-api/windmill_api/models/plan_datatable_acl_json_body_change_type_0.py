from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.plan_datatable_acl_json_body_change_type_0_type import PlanDatatableAclJsonBodyChangeType0Type

T = TypeVar("T", bound="PlanDatatableAclJsonBodyChangeType0")


@_attrs_define
class PlanDatatableAclJsonBodyChangeType0:
    """hands the target to role — for a schema, with everything already in it but an extension's members, which stay with
    the extension

        Attributes:
            type (PlanDatatableAclJsonBodyChangeType0Type):
            role (str): a data table role of the instance, or admin
    """

    type: PlanDatatableAclJsonBodyChangeType0Type
    role: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        role = self.role

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "role": role,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = PlanDatatableAclJsonBodyChangeType0Type(d.pop("type"))

        role = d.pop("role")

        plan_datatable_acl_json_body_change_type_0 = cls(
            type=type,
            role=role,
        )

        plan_datatable_acl_json_body_change_type_0.additional_properties = d
        return plan_datatable_acl_json_body_change_type_0

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
