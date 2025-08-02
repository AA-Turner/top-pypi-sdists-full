from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GlobalUserUpdateJsonBody")


@_attrs_define
class GlobalUserUpdateJsonBody:
    """
    Attributes:
        is_super_admin (Union[Unset, bool]):
        is_devops (Union[Unset, bool]):
        name (Union[Unset, str]):
    """

    is_super_admin: Union[Unset, bool] = UNSET
    is_devops: Union[Unset, bool] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        is_super_admin = self.is_super_admin
        is_devops = self.is_devops
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if is_super_admin is not UNSET:
            field_dict["is_super_admin"] = is_super_admin
        if is_devops is not UNSET:
            field_dict["is_devops"] = is_devops
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        is_super_admin = d.pop("is_super_admin", UNSET)

        is_devops = d.pop("is_devops", UNSET)

        name = d.pop("name", UNSET)

        global_user_update_json_body = cls(
            is_super_admin=is_super_admin,
            is_devops=is_devops,
            name=name,
        )

        global_user_update_json_body.additional_properties = d
        return global_user_update_json_body

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
