import datetime
from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="SeedFullDiffScanResponse200")


@_attrs_define
class SeedFullDiffScanResponse200:
    """
    Attributes:
        candidates (int): Number of candidate items the comparison will evaluate
        scanned_at (datetime.datetime):
    """

    candidates: int
    scanned_at: datetime.datetime
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        candidates = self.candidates
        scanned_at = self.scanned_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "candidates": candidates,
                "scanned_at": scanned_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        candidates = d.pop("candidates")

        scanned_at = isoparse(d.pop("scanned_at"))

        seed_full_diff_scan_response_200 = cls(
            candidates=candidates,
            scanned_at=scanned_at,
        )

        seed_full_diff_scan_response_200.additional_properties = d
        return seed_full_diff_scan_response_200

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
