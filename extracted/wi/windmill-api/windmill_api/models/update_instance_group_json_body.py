from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateInstanceGroupJsonBody")


@_attrs_define
class UpdateInstanceGroupJsonBody:
    """
    Attributes:
        new_summary (str):
        instance_role (Union[Unset, None, str]): Instance-level role for group members. 'superadmin', 'devops', 'user'
            or empty to clear.
    """

    new_summary: str
    instance_role: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        new_summary = self.new_summary
        instance_role = self.instance_role

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "new_summary": new_summary,
            }
        )
        if instance_role is not UNSET:
            field_dict["instance_role"] = instance_role

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        new_summary = d.pop("new_summary")

        instance_role = d.pop("instance_role", UNSET)

        update_instance_group_json_body = cls(
            new_summary=new_summary,
            instance_role=instance_role,
        )

        update_instance_group_json_body.additional_properties = d
        return update_instance_group_json_body

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
