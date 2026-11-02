from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.effective_role_source import EffectiveRoleSource

if TYPE_CHECKING:
    from ..models.effective_role_capabilities import EffectiveRoleCapabilities


T = TypeVar("T", bound="EffectiveRole")


@_attrs_define
class EffectiveRole:
    """
    Attributes:
        name (str):
        label (str):
        capabilities (EffectiveRoleCapabilities):
        source (EffectiveRoleSource):
        overridden (bool):
    """

    name: str
    label: str
    capabilities: "EffectiveRoleCapabilities"
    source: EffectiveRoleSource
    overridden: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        label = self.label
        capabilities = self.capabilities.to_dict()

        source = self.source.value

        overridden = self.overridden

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "label": label,
                "capabilities": capabilities,
                "source": source,
                "overridden": overridden,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.effective_role_capabilities import EffectiveRoleCapabilities

        d = src_dict.copy()
        name = d.pop("name")

        label = d.pop("label")

        capabilities = EffectiveRoleCapabilities.from_dict(d.pop("capabilities"))

        source = EffectiveRoleSource(d.pop("source"))

        overridden = d.pop("overridden")

        effective_role = cls(
            name=name,
            label=label,
            capabilities=capabilities,
            source=source,
            overridden=overridden,
        )

        effective_role.additional_properties = d
        return effective_role

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
