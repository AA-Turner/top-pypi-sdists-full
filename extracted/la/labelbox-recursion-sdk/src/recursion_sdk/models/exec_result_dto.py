from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="ExecResultDto")



@_attrs_define
class ExecResultDto:
    """ Result of executing a one-off command inside a compute.

        Example:
            {'stdout': '==== 14 passed in 3.21s ====\\n', 'stderr': '', 'exitCode': 0}

        Attributes:
            stdout (str): Captured standard output emitted by the command.
            stderr (str): Captured standard error emitted by the command.
            exit_code (int | None): Process exit code, or null when the command was terminated before exiting.
     """

    stdout: str
    stderr: str
    exit_code: int | None





    def to_dict(self) -> dict[str, Any]:
        stdout = self.stdout

        stderr = self.stderr

        exit_code: int | None
        exit_code = self.exit_code


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "stdout": stdout,
            "stderr": stderr,
            "exitCode": exit_code,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        stdout = d.pop("stdout")

        stderr = d.pop("stderr")

        def _parse_exit_code(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        exit_code = _parse_exit_code(d.pop("exitCode"))


        exec_result_dto = cls(
            stdout=stdout,
            stderr=stderr,
            exit_code=exit_code,
        )

        return exec_result_dto

