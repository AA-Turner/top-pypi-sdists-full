import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.slurm_policy_date_projection_status_enum import SlurmPolicyDateProjectionStatusEnum

T = TypeVar("T", bound="SlurmPolicyDateProjection")


@_attrs_define
class SlurmPolicyDateProjection:
    """
    Attributes:
        days (Union[None, int]):
        date (Union[None, datetime.date]):
        status (SlurmPolicyDateProjectionStatusEnum):
    """

    days: Union[None, int]
    date: Union[None, datetime.date]
    status: SlurmPolicyDateProjectionStatusEnum
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        days: Union[None, int]
        days = self.days

        date: Union[None, str]
        if isinstance(self.date, datetime.date):
            date = self.date.isoformat()
        else:
            date = self.date

        status = self.status.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "days": days,
                "date": date,
                "status": status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_days(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        days = _parse_days(d.pop("days"))

        def _parse_date(data: object) -> Union[None, datetime.date]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                date_type_0 = isoparse(data).date()

                return date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.date], data)

        date = _parse_date(d.pop("date"))

        status = SlurmPolicyDateProjectionStatusEnum(d.pop("status"))

        slurm_policy_date_projection = cls(
            days=days,
            date=date,
            status=status,
        )

        slurm_policy_date_projection.additional_properties = d
        return slurm_policy_date_projection

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
