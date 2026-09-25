from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.facet_value import FacetValue


T = TypeVar("T", bound="ScriptFacets")


@_attrs_define
class ScriptFacets:
    """
    Attributes:
        pipeline_name (list[FacetValue]): Pipeline names the jobs deliver to.
        profile (list[FacetValue]): Profiles the jobs run under.
        tags (list[FacetValue]): Tags the jobs declare, prefix removed.
    """

    pipeline_name: list[FacetValue]
    profile: list[FacetValue]
    tags: list[FacetValue]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pipeline_name = []
        for pipeline_name_item_data in self.pipeline_name:
            pipeline_name_item = pipeline_name_item_data.to_dict()
            pipeline_name.append(pipeline_name_item)

        profile = []
        for profile_item_data in self.profile:
            profile_item = profile_item_data.to_dict()
            profile.append(profile_item)

        tags = []
        for tags_item_data in self.tags:
            tags_item = tags_item_data.to_dict()
            tags.append(tags_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pipeline_name": pipeline_name,
                "profile": profile,
                "tags": tags,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.facet_value import FacetValue

        d = dict(src_dict)
        pipeline_name = []
        _pipeline_name = d.pop("pipeline_name")
        for pipeline_name_item_data in _pipeline_name:
            pipeline_name_item = FacetValue.from_dict(pipeline_name_item_data)

            pipeline_name.append(pipeline_name_item)

        profile = []
        _profile = d.pop("profile")
        for profile_item_data in _profile:
            profile_item = FacetValue.from_dict(profile_item_data)

            profile.append(profile_item)

        tags = []
        _tags = d.pop("tags")
        for tags_item_data in _tags:
            tags_item = FacetValue.from_dict(tags_item_data)

            tags.append(tags_item)

        script_facets = cls(
            pipeline_name=pipeline_name,
            profile=profile,
            tags=tags,
        )

        script_facets.additional_properties = d
        return script_facets

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
