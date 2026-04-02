from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="EligibilityCheck")


@_attrs_define
class EligibilityCheck:
    """
    Attributes:
        is_eligible (bool):
        restrictions (list[str]):
    """

    is_eligible: bool
    restrictions: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        is_eligible = self.is_eligible

        restrictions = self.restrictions

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "is_eligible": is_eligible,
                "restrictions": restrictions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        is_eligible = d.pop("is_eligible")

        restrictions = cast(list[str], d.pop("restrictions"))

        eligibility_check = cls(
            is_eligible=is_eligible,
            restrictions=restrictions,
        )

        eligibility_check.additional_properties = d
        return eligibility_check

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
