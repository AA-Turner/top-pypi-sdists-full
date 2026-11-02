from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetOfflineLicenseStatusResponse200")


@_attrs_define
class GetOfflineLicenseStatusResponse200:
    """
    Attributes:
        seats_used (Union[Unset, float]): Author-equivalent seats consumed (authors + 0.5 × operators)
        seats_cap (Union[Unset, int]):
        author_count (Union[Unset, int]):
        operator_count (Union[Unset, int]):
        current_cu (Union[Unset, float]): Sum of CU rate across workers that pinged in the last 2 minutes.
        cu_cap (Union[Unset, float]):
        cu_over_cap (Union[Unset, bool]):
    """

    seats_used: Union[Unset, float] = UNSET
    seats_cap: Union[Unset, int] = UNSET
    author_count: Union[Unset, int] = UNSET
    operator_count: Union[Unset, int] = UNSET
    current_cu: Union[Unset, float] = UNSET
    cu_cap: Union[Unset, float] = UNSET
    cu_over_cap: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        seats_used = self.seats_used
        seats_cap = self.seats_cap
        author_count = self.author_count
        operator_count = self.operator_count
        current_cu = self.current_cu
        cu_cap = self.cu_cap
        cu_over_cap = self.cu_over_cap

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if seats_used is not UNSET:
            field_dict["seats_used"] = seats_used
        if seats_cap is not UNSET:
            field_dict["seats_cap"] = seats_cap
        if author_count is not UNSET:
            field_dict["author_count"] = author_count
        if operator_count is not UNSET:
            field_dict["operator_count"] = operator_count
        if current_cu is not UNSET:
            field_dict["current_cu"] = current_cu
        if cu_cap is not UNSET:
            field_dict["cu_cap"] = cu_cap
        if cu_over_cap is not UNSET:
            field_dict["cu_over_cap"] = cu_over_cap

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        seats_used = d.pop("seats_used", UNSET)

        seats_cap = d.pop("seats_cap", UNSET)

        author_count = d.pop("author_count", UNSET)

        operator_count = d.pop("operator_count", UNSET)

        current_cu = d.pop("current_cu", UNSET)

        cu_cap = d.pop("cu_cap", UNSET)

        cu_over_cap = d.pop("cu_over_cap", UNSET)

        get_offline_license_status_response_200 = cls(
            seats_used=seats_used,
            seats_cap=seats_cap,
            author_count=author_count,
            operator_count=operator_count,
            current_cu=current_cu,
            cu_cap=cu_cap,
            cu_over_cap=cu_over_cap,
        )

        get_offline_license_status_response_200.additional_properties = d
        return get_offline_license_status_response_200

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
