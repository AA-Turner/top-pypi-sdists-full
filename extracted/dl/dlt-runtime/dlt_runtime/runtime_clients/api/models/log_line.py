import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.log_phase import LogPhase

T = TypeVar("T", bound="LogLine")


@_attrs_define
class LogLine:
    """
    Attributes:
        content (str): Contents of the log message
        line_num (int): Line number of the log
        phase (LogPhase): The phase of execution this log line belongs to
        reported_at (datetime.datetime): Timestamp when the log was reported
    """

    content: str
    line_num: int
    phase: LogPhase
    reported_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        content = self.content

        line_num = self.line_num

        phase = self.phase.value

        reported_at = self.reported_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content": content,
                "line_num": line_num,
                "phase": phase,
                "reported_at": reported_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        content = d.pop("content")

        line_num = d.pop("line_num")

        phase = LogPhase(d.pop("phase"))

        reported_at = isoparse(d.pop("reported_at"))

        log_line = cls(
            content=content,
            line_num=line_num,
            phase=phase,
            reported_at=reported_at,
        )

        log_line.additional_properties = d
        return log_line

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
