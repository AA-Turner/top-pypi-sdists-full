from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.role_definition_capabilities import RoleDefinitionCapabilities


T = TypeVar("T", bound="RoleDefinition")


@_attrs_define
class RoleDefinition:
    """One entry of the `workspace_roles` instance setting.

    Attributes:
        name (str):
        label (Union[Unset, str]):
        capabilities (Union[Unset, RoleDefinitionCapabilities]): A partial RoleCapabilities; an unset key falls through
            to the layer below.
    """

    name: str
    label: Union[Unset, str] = UNSET
    capabilities: Union[Unset, "RoleDefinitionCapabilities"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        label = self.label
        capabilities: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.capabilities, Unset):
            capabilities = self.capabilities.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if label is not UNSET:
            field_dict["label"] = label
        if capabilities is not UNSET:
            field_dict["capabilities"] = capabilities

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.role_definition_capabilities import RoleDefinitionCapabilities

        d = src_dict.copy()
        name = d.pop("name")

        label = d.pop("label", UNSET)

        _capabilities = d.pop("capabilities", UNSET)
        capabilities: Union[Unset, RoleDefinitionCapabilities]
        if isinstance(_capabilities, Unset):
            capabilities = UNSET
        else:
            capabilities = RoleDefinitionCapabilities.from_dict(_capabilities)

        role_definition = cls(
            name=name,
            label=label,
            capabilities=capabilities,
        )

        role_definition.additional_properties = d
        return role_definition

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
