from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DataAccessSummary")


@_attrs_define
class DataAccessSummary:
    """
    Attributes:
        total_administrative_access (Union[None, int]):
        total_organizational_access (int):
        total_provider_access (int):
    """

    total_administrative_access: Union[None, int]
    total_organizational_access: int
    total_provider_access: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total_administrative_access: Union[None, int]
        total_administrative_access = self.total_administrative_access

        total_organizational_access = self.total_organizational_access

        total_provider_access = self.total_provider_access

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total_administrative_access": total_administrative_access,
                "total_organizational_access": total_organizational_access,
                "total_provider_access": total_provider_access,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_total_administrative_access(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        total_administrative_access = _parse_total_administrative_access(d.pop("total_administrative_access"))

        total_organizational_access = d.pop("total_organizational_access")

        total_provider_access = d.pop("total_provider_access")

        data_access_summary = cls(
            total_administrative_access=total_administrative_access,
            total_organizational_access=total_organizational_access,
            total_provider_access=total_provider_access,
        )

        data_access_summary.additional_properties = d
        return data_access_summary

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
