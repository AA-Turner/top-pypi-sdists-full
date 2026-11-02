from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="EditAddAdminsAndDevelopersToForksJsonBody")


@_attrs_define
class EditAddAdminsAndDevelopersToForksJsonBody:
    """
    Attributes:
        add_admins_and_developers_to_forks (bool):
    """

    add_admins_and_developers_to_forks: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        add_admins_and_developers_to_forks = self.add_admins_and_developers_to_forks

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "add_admins_and_developers_to_forks": add_admins_and_developers_to_forks,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        add_admins_and_developers_to_forks = d.pop("add_admins_and_developers_to_forks")

        edit_add_admins_and_developers_to_forks_json_body = cls(
            add_admins_and_developers_to_forks=add_admins_and_developers_to_forks,
        )

        edit_add_admins_and_developers_to_forks_json_body.additional_properties = d
        return edit_add_admins_and_developers_to_forks_json_body

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
