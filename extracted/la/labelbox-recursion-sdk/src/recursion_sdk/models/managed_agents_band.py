from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ManagedAgentsBand")



@_attrs_define
class ManagedAgentsBand:
    """ Low, typical and high values: the 25th, 50th and 75th percentiles.

        Example:
            {'high': 1.5, 'low': 1.5, 'typical': 1.5}

        Attributes:
            high (float): 75th percentile.
            low (float): 25th percentile.
            typical (float): 50th percentile, the median.
     """

    high: float
    low: float
    typical: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        high = self.high

        low = self.low

        typical = self.typical


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "high": high,
            "low": low,
            "typical": typical,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        high = d.pop("high")

        low = d.pop("low")

        typical = d.pop("typical")

        managed_agents_band = cls(
            high=high,
            low=low,
            typical=typical,
        )


        managed_agents_band.additional_properties = d
        return managed_agents_band

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
