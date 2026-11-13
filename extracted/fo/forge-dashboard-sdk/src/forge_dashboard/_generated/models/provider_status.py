from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.provider_status_indicator import ProviderStatusIndicator
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ProviderStatus")



@_attrs_define
class ProviderStatus:
    """ 
        Attributes:
            indicator (ProviderStatusIndicator): The status page's overall level. It covers every GitHub component,
                including ones the dashboard doesn't use, so read incidents and components for what concerns this service.
            components (list[str] | Unset): The affected components the dashboard uses, as the page names them ("Pull
                Requests").
            incidents (list[str] | Unset): Titles of the open incidents on those components.
     """

    indicator: ProviderStatusIndicator
    components: list[str] | Unset = UNSET
    incidents: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        indicator = self.indicator.value

        components: list[str] | Unset = UNSET
        if not isinstance(self.components, Unset):
            components = self.components



        incidents: list[str] | Unset = UNSET
        if not isinstance(self.incidents, Unset):
            incidents = self.incidents




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "indicator": indicator,
        })
        if components is not UNSET:
            field_dict["components"] = components
        if incidents is not UNSET:
            field_dict["incidents"] = incidents

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        indicator = ProviderStatusIndicator(d.pop("indicator"))




        components = cast(list[str], d.pop("components", UNSET))


        incidents = cast(list[str], d.pop("incidents", UNSET))


        provider_status = cls(
            indicator=indicator,
            components=components,
            incidents=incidents,
        )


        provider_status.additional_properties = d
        return provider_status

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
