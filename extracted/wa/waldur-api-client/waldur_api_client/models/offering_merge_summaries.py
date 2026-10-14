from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="OfferingMergeSummaries")


@_attrs_define
class OfferingMergeSummaries:
    """
    Attributes:
        components (int): Components whose monthly usage summaries are recomputed.
        periods (list[str]): Months recomputed, as YYYY-MM.
    """

    components: int
    periods: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        components = self.components

        periods = self.periods

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "components": components,
                "periods": periods,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        components = d.pop("components")

        periods = cast(list[str], d.pop("periods"))

        offering_merge_summaries = cls(
            components=components,
            periods=periods,
        )

        offering_merge_summaries.additional_properties = d
        return offering_merge_summaries

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
