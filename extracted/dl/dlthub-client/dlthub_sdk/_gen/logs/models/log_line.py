from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.log_io_stream import LogIoStream
from ..models.log_source import LogSource
from ..models.run_signal_stage import RunSignalStage

T = TypeVar("T", bound="LogLine")


@_attrs_define
class LogLine:
    """
    Attributes:
        content (str): Contents of the log message
        io_stream (LogIoStream | str): Stream the line was written to
        line_num (int): Line number of the log
        reported_at (datetime.datetime): datetime with the constraint that the value must have timezone info
        source (LogSource | str): Who emitted the line
        stage (RunSignalStage | str): Stage of the run the line belongs to
    """

    content: str
    io_stream: LogIoStream | str
    line_num: int
    reported_at: datetime.datetime
    source: LogSource | str
    stage: RunSignalStage | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        content = self.content

        io_stream: str
        if isinstance(self.io_stream, LogIoStream):
            io_stream = self.io_stream.value
        else:
            io_stream = self.io_stream

        line_num = self.line_num

        reported_at = self.reported_at.isoformat()

        source: str
        if isinstance(self.source, LogSource):
            source = self.source.value
        else:
            source = self.source

        stage: str
        if isinstance(self.stage, RunSignalStage):
            stage = self.stage.value
        else:
            stage = self.stage

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content": content,
                "io_stream": io_stream,
                "line_num": line_num,
                "reported_at": reported_at,
                "source": source,
                "stage": stage,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        content = d.pop("content")

        def _parse_io_stream(data: object) -> LogIoStream | str:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                io_stream_type_0 = LogIoStream(data)

                return io_stream_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LogIoStream | str, data)

        io_stream = _parse_io_stream(d.pop("io_stream"))

        line_num = d.pop("line_num")

        reported_at = isoparse(d.pop("reported_at"))

        def _parse_source(data: object) -> LogSource | str:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                source_type_0 = LogSource(data)

                return source_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LogSource | str, data)

        source = _parse_source(d.pop("source"))

        def _parse_stage(data: object) -> RunSignalStage | str:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                stage_type_0 = RunSignalStage(data)

                return stage_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(RunSignalStage | str, data)

        stage = _parse_stage(d.pop("stage"))

        log_line = cls(
            content=content,
            io_stream=io_stream,
            line_num=line_num,
            reported_at=reported_at,
            source=source,
            stage=stage,
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
