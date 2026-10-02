from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.grading_config_compute_exec_output_format import GradingConfigComputeExecOutputFormat
from ..models.grading_config_compute_exec_type import GradingConfigComputeExecType
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.grading_config_compute_exec_mounts_item import GradingConfigComputeExecMountsItem





T = TypeVar("T", bound="GradingConfigComputeExec")



@_attrs_define
class GradingConfigComputeExec:
    """ Grading config leaf that grades a snapshot run by executing a command against its persistent compute, mounting
    optional files, and parsing the grade-output file.

        Attributes:
            type_ (GradingConfigComputeExecType): Discriminator: grade by executing a command against the solver’s
                persistent compute (no separate grader container).
            command (str): Command executed against the persistent compute to start grading.
            output_format (GradingConfigComputeExecOutputFormat): Format the grade command writes to the grade-output file,
                used to parse the score.
            poll_command (str | Unset): Optional command polled repeatedly until the grade result is ready or failed.
            mounts (list[GradingConfigComputeExecMountsItem] | Unset): Files copied into the compute (at their mountPath)
                before the grade command runs.
     """

    type_: GradingConfigComputeExecType
    command: str
    output_format: GradingConfigComputeExecOutputFormat
    poll_command: str | Unset = UNSET
    mounts: list[GradingConfigComputeExecMountsItem] | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.grading_config_compute_exec_mounts_item import GradingConfigComputeExecMountsItem # noqa: PLC0415
        type_ = self.type_.value

        command = self.command

        output_format = self.output_format.value

        poll_command = self.poll_command

        mounts: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.mounts, Unset):
            mounts = []
            for mounts_item_data in self.mounts:
                mounts_item = mounts_item_data.to_dict()
                mounts.append(mounts_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "type": type_,
            "command": command,
            "outputFormat": output_format,
        })
        if poll_command is not UNSET:
            field_dict["pollCommand"] = poll_command
        if mounts is not UNSET:
            field_dict["mounts"] = mounts

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.grading_config_compute_exec_mounts_item import GradingConfigComputeExecMountsItem # noqa: PLC0415
        d = dict(src_dict)
        type_ = GradingConfigComputeExecType(d.pop("type"))




        command = d.pop("command")

        output_format = GradingConfigComputeExecOutputFormat(d.pop("outputFormat"))




        poll_command = d.pop("pollCommand", UNSET)

        _mounts = d.pop("mounts", UNSET)
        mounts: list[GradingConfigComputeExecMountsItem] | Unset = UNSET
        if _mounts is not UNSET:
            mounts = []
            for mounts_item_data in _mounts:
                mounts_item = GradingConfigComputeExecMountsItem.from_dict(mounts_item_data)



                mounts.append(mounts_item)


        grading_config_compute_exec = cls(
            type_=type_,
            command=command,
            output_format=output_format,
            poll_command=poll_command,
            mounts=mounts,
        )

        return grading_config_compute_exec

