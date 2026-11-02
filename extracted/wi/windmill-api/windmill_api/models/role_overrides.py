from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.role_overrides_additional_property import RoleOverridesAdditionalProperty


T = TypeVar("T", bound="RoleOverrides")


@_attrs_define
class RoleOverrides:
    """A workspace's overrides keyed by role name; a name the instance does not define adds a workspace-only role (EE)."""

    additional_properties: Dict[str, "RoleOverridesAdditionalProperty"] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        pass

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.role_overrides_additional_property import RoleOverridesAdditionalProperty

        d = src_dict.copy()
        role_overrides = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = RoleOverridesAdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        role_overrides.additional_properties = additional_properties
        return role_overrides

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "RoleOverridesAdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "RoleOverridesAdditionalProperty") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
