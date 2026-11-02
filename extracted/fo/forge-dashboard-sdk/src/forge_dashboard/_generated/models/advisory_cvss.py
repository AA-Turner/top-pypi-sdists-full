from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="AdvisoryCVSS")



@_attrs_define
class AdvisoryCVSS:
    """ 
        Attributes:
            score (float): The CVSS base score, 0 to 10.
            vector (str | Unset): The CVSS vector string.
     """

    score: float
    vector: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        score = self.score

        vector = self.vector


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "score": score,
        })
        if vector is not UNSET:
            field_dict["vector"] = vector

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        score = d.pop("score")

        vector = d.pop("vector", UNSET)

        advisory_cvss = cls(
            score=score,
            vector=vector,
        )


        advisory_cvss.additional_properties = d
        return advisory_cvss

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
