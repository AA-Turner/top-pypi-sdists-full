from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ComponentActivity")


@_attrs_define
class ComponentActivity:
    """
    Attributes:
        commits_since_base (Union[Unset, int]):
        commits_since_previous (Union[Unset, int]):
        compare_url_base (Union[Unset, str]):
        compare_url_previous (Union[Unset, str]):
    """

    commits_since_base: Union[Unset, int] = UNSET
    commits_since_previous: Union[Unset, int] = UNSET
    compare_url_base: Union[Unset, str] = UNSET
    compare_url_previous: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        commits_since_base = self.commits_since_base

        commits_since_previous = self.commits_since_previous

        compare_url_base = self.compare_url_base

        compare_url_previous = self.compare_url_previous

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if commits_since_base is not UNSET:
            field_dict["commits_since_base"] = commits_since_base
        if commits_since_previous is not UNSET:
            field_dict["commits_since_previous"] = commits_since_previous
        if compare_url_base is not UNSET:
            field_dict["compare_url_base"] = compare_url_base
        if compare_url_previous is not UNSET:
            field_dict["compare_url_previous"] = compare_url_previous

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        commits_since_base = d.pop("commits_since_base", UNSET)

        commits_since_previous = d.pop("commits_since_previous", UNSET)

        compare_url_base = d.pop("compare_url_base", UNSET)

        compare_url_previous = d.pop("compare_url_previous", UNSET)

        component_activity = cls(
            commits_since_base=commits_since_base,
            commits_since_previous=commits_since_previous,
            compare_url_base=compare_url_base,
            compare_url_previous=compare_url_previous,
        )

        component_activity.additional_properties = d
        return component_activity

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
