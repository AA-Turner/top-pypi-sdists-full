from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="AdvisoryEPSS")



@_attrs_define
class AdvisoryEPSS:
    """ The Exploit Prediction Scoring System's reading, as GitHub sends it. Absent when GitHub sent none.

        Attributes:
            percentage (float): The probability of exploitation in the next 30 days, as a fraction from 0 to 1.
            percentile (float): How the score ranks among all scored flaws, as a fraction from 0 to 1.
     """

    percentage: float
    percentile: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        percentage = self.percentage

        percentile = self.percentile


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "percentage": percentage,
            "percentile": percentile,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        percentage = d.pop("percentage")

        percentile = d.pop("percentile")

        advisory_epss = cls(
            percentage=percentage,
            percentile=percentile,
        )


        advisory_epss.additional_properties = d
        return advisory_epss

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
