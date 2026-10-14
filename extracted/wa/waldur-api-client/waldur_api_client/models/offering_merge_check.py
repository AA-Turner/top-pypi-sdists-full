from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.offering_merge_check_details import OfferingMergeCheckDetails


T = TypeVar("T", bound="OfferingMergeCheck")


@_attrs_define
class OfferingMergeCheck:
    """
    Attributes:
        code (str):
        passed (bool):
        details (OfferingMergeCheckDetails):
    """

    code: str
    passed: bool
    details: "OfferingMergeCheckDetails"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        code = self.code

        passed = self.passed

        details = self.details.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "passed": passed,
                "details": details,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.offering_merge_check_details import OfferingMergeCheckDetails

        d = dict(src_dict)
        code = d.pop("code")

        passed = d.pop("passed")

        details = OfferingMergeCheckDetails.from_dict(d.pop("details"))

        offering_merge_check = cls(
            code=code,
            passed=passed,
            details=details,
        )

        offering_merge_check.additional_properties = d
        return offering_merge_check

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
