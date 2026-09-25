from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.facet_value import FacetValue


T = TypeVar("T", bound="RunFacets")


@_attrs_define
class RunFacets:
    """
    Attributes:
        profile (list[FacetValue]): Profiles the runs were started under.
    """

    profile: list[FacetValue]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        profile = []
        for profile_item_data in self.profile:
            profile_item = profile_item_data.to_dict()
            profile.append(profile_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "profile": profile,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.facet_value import FacetValue

        d = dict(src_dict)
        profile = []
        _profile = d.pop("profile")
        for profile_item_data in _profile:
            profile_item = FacetValue.from_dict(profile_item_data)

            profile.append(profile_item)

        run_facets = cls(
            profile=profile,
        )

        run_facets.additional_properties = d
        return run_facets

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
