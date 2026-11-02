from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ApplyDatatableAclJsonBodyChangeType2ObjectsItem")


@_attrs_define
class ApplyDatatableAclJsonBodyChangeType2ObjectsItem:
    """
    Attributes:
        name (str):
        kind (str): TABLE, SEQUENCE, FUNCTION, PROCEDURE or TYPE — what the object is. A revoke turns it into the
            keyword it takes, ROUTINE for both routine kinds; a type's grants are read only.
        args (Union[Unset, str]): identity arguments of a routine, which is what tells two of the same name apart
    """

    name: str
    kind: str
    args: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        kind = self.kind
        args = self.args

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "kind": kind,
            }
        )
        if args is not UNSET:
            field_dict["args"] = args

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        kind = d.pop("kind")

        args = d.pop("args", UNSET)

        apply_datatable_acl_json_body_change_type_2_objects_item = cls(
            name=name,
            kind=kind,
            args=args,
        )

        apply_datatable_acl_json_body_change_type_2_objects_item.additional_properties = d
        return apply_datatable_acl_json_body_change_type_2_objects_item

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
