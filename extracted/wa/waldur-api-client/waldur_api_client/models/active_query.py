from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ActiveQuery")


@_attrs_define
class ActiveQuery:
    """
    Attributes:
        pid (int): Process ID
        duration_seconds (float): Query duration in seconds
        state (str): Query state
        wait_event_type (Union[None, str]): Type of event the query is waiting for
        query_preview (str): First 100 characters of the query
    """

    pid: int
    duration_seconds: float
    state: str
    wait_event_type: Union[None, str]
    query_preview: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pid = self.pid

        duration_seconds = self.duration_seconds

        state = self.state

        wait_event_type: Union[None, str]
        wait_event_type = self.wait_event_type

        query_preview = self.query_preview

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pid": pid,
                "duration_seconds": duration_seconds,
                "state": state,
                "wait_event_type": wait_event_type,
                "query_preview": query_preview,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        pid = d.pop("pid")

        duration_seconds = d.pop("duration_seconds")

        state = d.pop("state")

        def _parse_wait_event_type(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        wait_event_type = _parse_wait_event_type(d.pop("wait_event_type"))

        query_preview = d.pop("query_preview")

        active_query = cls(
            pid=pid,
            duration_seconds=duration_seconds,
            state=state,
            wait_event_type=wait_event_type,
            query_preview=query_preview,
        )

        active_query.additional_properties = d
        return active_query

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
