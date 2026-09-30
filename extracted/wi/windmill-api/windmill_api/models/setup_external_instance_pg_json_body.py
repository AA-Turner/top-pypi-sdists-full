from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SetupExternalInstancePgJsonBody")


@_attrs_define
class SetupExternalInstancePgJsonBody:
    """
    Attributes:
        rotate_passwords (Union[Unset, bool]):
    """

    rotate_passwords: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        rotate_passwords = self.rotate_passwords

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if rotate_passwords is not UNSET:
            field_dict["rotate_passwords"] = rotate_passwords

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        rotate_passwords = d.pop("rotate_passwords", UNSET)

        setup_external_instance_pg_json_body = cls(
            rotate_passwords=rotate_passwords,
        )

        setup_external_instance_pg_json_body.additional_properties = d
        return setup_external_instance_pg_json_body

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
