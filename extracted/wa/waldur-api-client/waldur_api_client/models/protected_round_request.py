import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProtectedRoundRequest")


@_attrs_define
class ProtectedRoundRequest:
    """
    Attributes:
        start_time (datetime.datetime):
        cutoff_time (datetime.datetime):
        allocation_date (Union[None, Unset, datetime.datetime]):
        review_duration_in_days (Union[Unset, int]):
    """

    start_time: datetime.datetime
    cutoff_time: datetime.datetime
    allocation_date: Union[None, Unset, datetime.datetime] = UNSET
    review_duration_in_days: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        start_time = self.start_time.isoformat()

        cutoff_time = self.cutoff_time.isoformat()

        allocation_date: Union[None, Unset, str]
        if isinstance(self.allocation_date, Unset):
            allocation_date = UNSET
        elif isinstance(self.allocation_date, datetime.datetime):
            allocation_date = self.allocation_date.isoformat()
        else:
            allocation_date = self.allocation_date

        review_duration_in_days = self.review_duration_in_days

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "start_time": start_time,
                "cutoff_time": cutoff_time,
            }
        )
        if allocation_date is not UNSET:
            field_dict["allocation_date"] = allocation_date
        if review_duration_in_days is not UNSET:
            field_dict["review_duration_in_days"] = review_duration_in_days

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        start_time = isoparse(d.pop("start_time"))

        cutoff_time = isoparse(d.pop("cutoff_time"))

        def _parse_allocation_date(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                allocation_date_type_0 = isoparse(data)

                return allocation_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        allocation_date = _parse_allocation_date(d.pop("allocation_date", UNSET))

        review_duration_in_days = d.pop("review_duration_in_days", UNSET)

        protected_round_request = cls(
            start_time=start_time,
            cutoff_time=cutoff_time,
            allocation_date=allocation_date,
            review_duration_in_days=review_duration_in_days,
        )

        protected_round_request.additional_properties = d
        return protected_round_request

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
