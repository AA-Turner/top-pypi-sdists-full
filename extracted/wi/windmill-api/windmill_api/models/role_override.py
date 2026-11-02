from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.role_override_capabilities import RoleOverrideCapabilities


T = TypeVar("T", bound="RoleOverride")


@_attrs_define
class RoleOverride:
    """
    Attributes:
        label (Union[Unset, str]):
        capabilities (Union[Unset, RoleOverrideCapabilities]): A partial RoleCapabilities; an unset key falls through to
            the layer below.
    """

    label: Union[Unset, str] = UNSET
    capabilities: Union[Unset, "RoleOverrideCapabilities"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        label = self.label
        capabilities: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.capabilities, Unset):
            capabilities = self.capabilities.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if label is not UNSET:
            field_dict["label"] = label
        if capabilities is not UNSET:
            field_dict["capabilities"] = capabilities

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.role_override_capabilities import RoleOverrideCapabilities

        d = src_dict.copy()
        label = d.pop("label", UNSET)

        _capabilities = d.pop("capabilities", UNSET)
        capabilities: Union[Unset, RoleOverrideCapabilities]
        if isinstance(_capabilities, Unset):
            capabilities = UNSET
        else:
            capabilities = RoleOverrideCapabilities.from_dict(_capabilities)

        role_override = cls(
            label=label,
            capabilities=capabilities,
        )

        role_override.additional_properties = d
        return role_override

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
