from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.provider_summary_resources import ProviderSummaryResources


T = TypeVar("T", bound="ProviderSummary")


@_attrs_define
class ProviderSummary:
    """
    Attributes:
        resources (ProviderSummaryResources):
        traits (list[str]):
    """

    resources: "ProviderSummaryResources"
    traits: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resources = self.resources.to_dict()

        traits = self.traits

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resources": resources,
                "traits": traits,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.provider_summary_resources import ProviderSummaryResources

        d = dict(src_dict)
        resources = ProviderSummaryResources.from_dict(d.pop("resources"))

        traits = cast(list[str], d.pop("traits"))

        provider_summary = cls(
            resources=resources,
            traits=traits,
        )

        provider_summary.additional_properties = d
        return provider_summary

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
