import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.cadence_enum import CadenceEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="BulkRoundCreateRequestRequest")


@_attrs_define
class BulkRoundCreateRequestRequest:
    """
    Attributes:
        start_time (datetime.datetime):
        cadence (CadenceEnum):
        submission_window_days (int):
        number_of_rounds (int):
        review_duration_in_days (Union[None, Unset, int]):
        custom_interval_months (Union[None, Unset, int]):
    """

    start_time: datetime.datetime
    cadence: CadenceEnum
    submission_window_days: int
    number_of_rounds: int
    review_duration_in_days: Union[None, Unset, int] = UNSET
    custom_interval_months: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        start_time = self.start_time.isoformat()

        cadence = self.cadence.value

        submission_window_days = self.submission_window_days

        number_of_rounds = self.number_of_rounds

        review_duration_in_days: Union[None, Unset, int]
        if isinstance(self.review_duration_in_days, Unset):
            review_duration_in_days = UNSET
        else:
            review_duration_in_days = self.review_duration_in_days

        custom_interval_months: Union[None, Unset, int]
        if isinstance(self.custom_interval_months, Unset):
            custom_interval_months = UNSET
        else:
            custom_interval_months = self.custom_interval_months

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "start_time": start_time,
                "cadence": cadence,
                "submission_window_days": submission_window_days,
                "number_of_rounds": number_of_rounds,
            }
        )
        if review_duration_in_days is not UNSET:
            field_dict["review_duration_in_days"] = review_duration_in_days
        if custom_interval_months is not UNSET:
            field_dict["custom_interval_months"] = custom_interval_months

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        start_time = isoparse(d.pop("start_time"))

        cadence = CadenceEnum(d.pop("cadence"))

        submission_window_days = d.pop("submission_window_days")

        number_of_rounds = d.pop("number_of_rounds")

        def _parse_review_duration_in_days(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        review_duration_in_days = _parse_review_duration_in_days(d.pop("review_duration_in_days", UNSET))

        def _parse_custom_interval_months(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        custom_interval_months = _parse_custom_interval_months(d.pop("custom_interval_months", UNSET))

        bulk_round_create_request_request = cls(
            start_time=start_time,
            cadence=cadence,
            submission_window_days=submission_window_days,
            number_of_rounds=number_of_rounds,
            review_duration_in_days=review_duration_in_days,
            custom_interval_months=custom_interval_months,
        )

        bulk_round_create_request_request.additional_properties = d
        return bulk_round_create_request_request

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
