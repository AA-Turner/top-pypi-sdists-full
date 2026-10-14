from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RelevantWhen")


@_attrs_define
class RelevantWhen:
    """
    Attributes:
        plugins (Union[Unset, list[str]]):
        feature_flags (Union[Unset, list[str]]):
        settings (Union[Unset, list[str]]):
    """

    plugins: Union[Unset, list[str]] = UNSET
    feature_flags: Union[Unset, list[str]] = UNSET
    settings: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        plugins: Union[Unset, list[str]] = UNSET
        if not isinstance(self.plugins, Unset):
            plugins = self.plugins

        feature_flags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.feature_flags, Unset):
            feature_flags = self.feature_flags

        settings: Union[Unset, list[str]] = UNSET
        if not isinstance(self.settings, Unset):
            settings = self.settings

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if plugins is not UNSET:
            field_dict["plugins"] = plugins
        if feature_flags is not UNSET:
            field_dict["feature_flags"] = feature_flags
        if settings is not UNSET:
            field_dict["settings"] = settings

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        plugins = cast(list[str], d.pop("plugins", UNSET))

        feature_flags = cast(list[str], d.pop("feature_flags", UNSET))

        settings = cast(list[str], d.pop("settings", UNSET))

        relevant_when = cls(
            plugins=plugins,
            feature_flags=feature_flags,
            settings=settings,
        )

        relevant_when.additional_properties = d
        return relevant_when

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
