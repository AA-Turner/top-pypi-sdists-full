from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.apply_datatable_acl_json_body_target_type_2_kind import ApplyDatatableAclJsonBodyTargetType2Kind

T = TypeVar("T", bound="ApplyDatatableAclJsonBodyTargetType2")


@_attrs_define
class ApplyDatatableAclJsonBodyTargetType2:
    """
    Attributes:
        kind (ApplyDatatableAclJsonBodyTargetType2Kind):
        schema (str):
        table (str):
    """

    kind: ApplyDatatableAclJsonBodyTargetType2Kind
    schema: str
    table: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        kind = self.kind.value

        schema = self.schema
        table = self.table

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "schema": schema,
                "table": table,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        kind = ApplyDatatableAclJsonBodyTargetType2Kind(d.pop("kind"))

        schema = d.pop("schema")

        table = d.pop("table")

        apply_datatable_acl_json_body_target_type_2 = cls(
            kind=kind,
            schema=schema,
            table=table,
        )

        apply_datatable_acl_json_body_target_type_2.additional_properties = d
        return apply_datatable_acl_json_body_target_type_2

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
