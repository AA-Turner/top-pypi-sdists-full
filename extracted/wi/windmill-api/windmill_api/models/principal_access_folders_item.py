from typing import Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PrincipalAccessFoldersItem")


@_attrs_define
class PrincipalAccessFoldersItem:
    """
    Attributes:
        name (str):
        write (bool):
        owner (bool):
        via (List[str]): the `u/<user>` or `g/<group>` grants on the folder that reach the principal
    """

    name: str
    write: bool
    owner: bool
    via: List[str]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        write = self.write
        owner = self.owner
        via = self.via

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "write": write,
                "owner": owner,
                "via": via,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        write = d.pop("write")

        owner = d.pop("owner")

        via = cast(List[str], d.pop("via"))

        principal_access_folders_item = cls(
            name=name,
            write=write,
            owner=owner,
            via=via,
        )

        principal_access_folders_item.additional_properties = d
        return principal_access_folders_item

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
