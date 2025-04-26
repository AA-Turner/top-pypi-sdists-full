import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ExtendedJobsObscuredJobsItem")


@_attrs_define
class ExtendedJobsObscuredJobsItem:
    """
    Attributes:
        typ (Union[Unset, str]):
        started_at (Union[Unset, datetime.datetime]):
        duration_ms (Union[Unset, float]):
    """

    typ: Union[Unset, str] = UNSET
    started_at: Union[Unset, datetime.datetime] = UNSET
    duration_ms: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        typ = self.typ
        started_at: Union[Unset, str] = UNSET
        if not isinstance(self.started_at, Unset):
            started_at = self.started_at.isoformat()

        duration_ms = self.duration_ms

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if typ is not UNSET:
            field_dict["typ"] = typ
        if started_at is not UNSET:
            field_dict["started_at"] = started_at
        if duration_ms is not UNSET:
            field_dict["duration_ms"] = duration_ms

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        typ = d.pop("typ", UNSET)

        _started_at = d.pop("started_at", UNSET)
        started_at: Union[Unset, datetime.datetime]
        if isinstance(_started_at, Unset):
            started_at = UNSET
        else:
            started_at = isoparse(_started_at)

        duration_ms = d.pop("duration_ms", UNSET)

        extended_jobs_obscured_jobs_item = cls(
            typ=typ,
            started_at=started_at,
            duration_ms=duration_ms,
        )

        extended_jobs_obscured_jobs_item.additional_properties = d
        return extended_jobs_obscured_jobs_item

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
