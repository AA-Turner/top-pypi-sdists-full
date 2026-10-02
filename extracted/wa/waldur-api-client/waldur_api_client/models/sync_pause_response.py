from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SyncPauseResponse")


@_attrs_define
class SyncPauseResponse:
    """
    Attributes:
        paused (Union[Unset, list[str]]): List of paused items
        resumed (Union[Unset, list[str]]): List of resumed items
    """

    paused: Union[Unset, list[str]] = UNSET
    resumed: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        paused: Union[Unset, list[str]] = UNSET
        if not isinstance(self.paused, Unset):
            paused = self.paused

        resumed: Union[Unset, list[str]] = UNSET
        if not isinstance(self.resumed, Unset):
            resumed = self.resumed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if paused is not UNSET:
            field_dict["paused"] = paused
        if resumed is not UNSET:
            field_dict["resumed"] = resumed

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        paused = cast(list[str], d.pop("paused", UNSET))

        resumed = cast(list[str], d.pop("resumed", UNSET))

        sync_pause_response = cls(
            paused=paused,
            resumed=resumed,
        )

        sync_pause_response.additional_properties = d
        return sync_pause_response

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
