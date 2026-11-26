import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetConcurrencyKeyStatusResponse200")


@_attrs_define
class GetConcurrencyKeyStatusResponse200:
    """
    Attributes:
        key (str):
        deferred_from (Union[Unset, None, datetime.datetime]): When the job was first due. Set the first time its
            concurrency limit held it back, and kept after it ran.
        released_at (Union[Unset, None, datetime.datetime]): When the concurrency limit let in a job it had held back,
            as the time the job was last due. The rest until it started is queue time.
    """

    key: str
    deferred_from: Union[Unset, None, datetime.datetime] = UNSET
    released_at: Union[Unset, None, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        key = self.key
        deferred_from: Union[Unset, None, str] = UNSET
        if not isinstance(self.deferred_from, Unset):
            deferred_from = self.deferred_from.isoformat() if self.deferred_from else None

        released_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.released_at, Unset):
            released_at = self.released_at.isoformat() if self.released_at else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
            }
        )
        if deferred_from is not UNSET:
            field_dict["deferred_from"] = deferred_from
        if released_at is not UNSET:
            field_dict["released_at"] = released_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        key = d.pop("key")

        _deferred_from = d.pop("deferred_from", UNSET)
        deferred_from: Union[Unset, None, datetime.datetime]
        if _deferred_from is None:
            deferred_from = None
        elif isinstance(_deferred_from, Unset):
            deferred_from = UNSET
        else:
            deferred_from = isoparse(_deferred_from)

        _released_at = d.pop("released_at", UNSET)
        released_at: Union[Unset, None, datetime.datetime]
        if _released_at is None:
            released_at = None
        elif isinstance(_released_at, Unset):
            released_at = UNSET
        else:
            released_at = isoparse(_released_at)

        get_concurrency_key_status_response_200 = cls(
            key=key,
            deferred_from=deferred_from,
            released_at=released_at,
        )

        get_concurrency_key_status_response_200.additional_properties = d
        return get_concurrency_key_status_response_200

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
