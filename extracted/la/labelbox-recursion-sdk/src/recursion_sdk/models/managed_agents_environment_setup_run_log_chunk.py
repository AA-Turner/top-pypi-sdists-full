from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
import datetime






T = TypeVar("T", bound="ManagedAgentsEnvironmentSetupRunLogChunk")



@_attrs_define
class ManagedAgentsEnvironmentSetupRunLogChunk:
    """ One line of a setup run's log with its stream and, when known, the script line that produced it.

        Example:
            {'at': '2026-02-18T09:30:00Z', 'line': 1, 'seq': 1, 'stream': 'example', 'text': 'example'}

        Attributes:
            at (datetime.datetime): When the line was captured.
            seq (int): Monotonic position of the line within the run. Pass the last seen seq as after to continue tailing.
            stream (str): stdout, stderr, marker (a step boundary: the script line about to run), or system (control-plane
                phase notes).
            text (str): The line, redacted, without its trailing newline.
            line (int | Unset): 1-based setup script line this output belongs to, when known from the preceding marker.
     """

    at: datetime.datetime
    seq: int
    stream: str
    text: str
    line: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        at = self.at.isoformat()

        seq = self.seq

        stream = self.stream

        text = self.text

        line = self.line


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "at": at,
            "seq": seq,
            "stream": stream,
            "text": text,
        })
        if line is not UNSET:
            field_dict["line"] = line

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        at = datetime.datetime.fromisoformat(d.pop("at"))




        seq = d.pop("seq")

        stream = d.pop("stream")

        text = d.pop("text")

        line = d.pop("line", UNSET)

        managed_agents_environment_setup_run_log_chunk = cls(
            at=at,
            seq=seq,
            stream=stream,
            text=text,
            line=line,
        )


        managed_agents_environment_setup_run_log_chunk.additional_properties = d
        return managed_agents_environment_setup_run_log_chunk

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
