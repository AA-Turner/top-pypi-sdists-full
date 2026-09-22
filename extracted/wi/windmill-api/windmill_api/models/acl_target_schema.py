from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.acl_target_schema_kind import AclTargetSchemaKind

T = TypeVar("T", bound="AclTargetSchema")


@_attrs_define
class AclTargetSchema:
    """
    Attributes:
        kind (AclTargetSchemaKind):
        schema (str):
    """

    kind: AclTargetSchemaKind
    schema: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        kind = self.kind.value

        schema = self.schema

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "schema": schema,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        kind = AclTargetSchemaKind(d.pop("kind"))

        schema = d.pop("schema")

        acl_target_schema = cls(
            kind=kind,
            schema=schema,
        )

        acl_target_schema.additional_properties = d
        return acl_target_schema

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
