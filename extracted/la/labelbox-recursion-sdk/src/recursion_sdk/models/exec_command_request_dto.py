from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ExecCommandRequestDto")



@_attrs_define
class ExecCommandRequestDto:
    """ Request body to execute a one-off command inside a running compute.

        Example:
            {'command': 'pytest', 'args': ['-q', 'tests/test_agent.py'], 'timeoutSeconds': 120}

        Attributes:
            command (str): Executable to run inside the compute container.
            args (list[str] | Unset): Positional arguments passed to the command.
            stdin (str | Unset): Optional standard-input payload streamed to the command (max 65536 code points).
            timeout_seconds (int | Unset): Maximum execution time before the long-poll returns and the command is killed.
     """

    command: str
    args: list[str] | Unset = UNSET
    stdin: str | Unset = UNSET
    timeout_seconds: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        command = self.command

        args: list[str] | Unset = UNSET
        if not isinstance(self.args, Unset):
            args = self.args



        stdin = self.stdin

        timeout_seconds = self.timeout_seconds


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "command": command,
        })
        if args is not UNSET:
            field_dict["args"] = args
        if stdin is not UNSET:
            field_dict["stdin"] = stdin
        if timeout_seconds is not UNSET:
            field_dict["timeoutSeconds"] = timeout_seconds

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        command = d.pop("command")

        args = cast(list[str], d.pop("args", UNSET))


        stdin = d.pop("stdin", UNSET)

        timeout_seconds = d.pop("timeoutSeconds", UNSET)

        exec_command_request_dto = cls(
            command=command,
            args=args,
            stdin=stdin,
            timeout_seconds=timeout_seconds,
        )


        exec_command_request_dto.additional_properties = d
        return exec_command_request_dto

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
