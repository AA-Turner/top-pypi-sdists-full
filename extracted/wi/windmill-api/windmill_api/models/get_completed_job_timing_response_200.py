import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetCompletedJobTimingResponse200")


@_attrs_define
class GetCompletedJobTimingResponse200:
    """
    Attributes:
        created_at (datetime.datetime):
        started_at (Union[Unset, datetime.datetime]):
        duration_ms (Union[Unset, int]):
    """

    created_at: datetime.datetime
    started_at: Union[Unset, datetime.datetime] = UNSET
    duration_ms: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        created_at = self.created_at.isoformat()

        started_at: Union[Unset, str] = UNSET
        if not isinstance(self.started_at, Unset):
            started_at = self.started_at.isoformat()

        duration_ms = self.duration_ms

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_at": created_at,
            }
        )
        if started_at is not UNSET:
            field_dict["started_at"] = started_at
        if duration_ms is not UNSET:
            field_dict["duration_ms"] = duration_ms

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        created_at = isoparse(d.pop("created_at"))

        _started_at = d.pop("started_at", UNSET)
        started_at: Union[Unset, datetime.datetime]
        if isinstance(_started_at, Unset):
            started_at = UNSET
        else:
            started_at = isoparse(_started_at)

        duration_ms = d.pop("duration_ms", UNSET)

        get_completed_job_timing_response_200 = cls(
            created_at=created_at,
            started_at=started_at,
            duration_ms=duration_ms,
        )

        get_completed_job_timing_response_200.additional_properties = d
        return get_completed_job_timing_response_200

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
