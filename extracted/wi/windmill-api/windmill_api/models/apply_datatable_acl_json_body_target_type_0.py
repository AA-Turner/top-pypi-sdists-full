from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.apply_datatable_acl_json_body_target_type_0_kind import ApplyDatatableAclJsonBodyTargetType0Kind

T = TypeVar("T", bound="ApplyDatatableAclJsonBodyTargetType0")


@_attrs_define
class ApplyDatatableAclJsonBodyTargetType0:
    """
    Attributes:
        kind (ApplyDatatableAclJsonBodyTargetType0Kind):
    """

    kind: ApplyDatatableAclJsonBodyTargetType0Kind
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        kind = self.kind.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        kind = ApplyDatatableAclJsonBodyTargetType0Kind(d.pop("kind"))

        apply_datatable_acl_json_body_target_type_0 = cls(
            kind=kind,
        )

        apply_datatable_acl_json_body_target_type_0.additional_properties = d
        return apply_datatable_acl_json_body_target_type_0

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
