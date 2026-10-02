from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.grading_config_input_compute_exec_output_format import GradingConfigInputComputeExecOutputFormat
from ..models.grading_config_input_compute_exec_type import GradingConfigInputComputeExecType
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.grading_config_input_compute_exec_mounts_item import GradingConfigInputComputeExecMountsItem





T = TypeVar("T", bound="GradingConfigInputComputeExec")



@_attrs_define
class GradingConfigInputComputeExec:
    """ Grading config leaf that grades a snapshot run by executing a command against its persistent compute, mounting
    optional files, and parsing the grade-output file.

        Attributes:
            type_ (GradingConfigInputComputeExecType): Discriminator: grade by executing a command against the solver’s
                persistent compute (no separate grader container).
            command (str): Command executed against the persistent compute to start grading.
            output_format (GradingConfigInputComputeExecOutputFormat): Format the grade command writes to the grade-output
                file, used to parse the score.
            poll_command (str | Unset): Optional command polled repeatedly until the grade result is ready or failed.
            mounts (list[GradingConfigInputComputeExecMountsItem] | Unset): Files copied into the compute (at their
                mountPath) before the grade command runs.
     """

    type_: GradingConfigInputComputeExecType
    command: str
    output_format: GradingConfigInputComputeExecOutputFormat
    poll_command: str | Unset = UNSET
    mounts: list[GradingConfigInputComputeExecMountsItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.grading_config_input_compute_exec_mounts_item import GradingConfigInputComputeExecMountsItem # noqa: PLC0415
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
        field_dict.update(self.additional_properties)
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
        from ..models.grading_config_input_compute_exec_mounts_item import GradingConfigInputComputeExecMountsItem # noqa: PLC0415
        d = dict(src_dict)
        type_ = GradingConfigInputComputeExecType(d.pop("type"))




        command = d.pop("command")

        output_format = GradingConfigInputComputeExecOutputFormat(d.pop("outputFormat"))




        poll_command = d.pop("pollCommand", UNSET)

        _mounts = d.pop("mounts", UNSET)
        mounts: list[GradingConfigInputComputeExecMountsItem] | Unset = UNSET
        if _mounts is not UNSET:
            mounts = []
            for mounts_item_data in _mounts:
                mounts_item = GradingConfigInputComputeExecMountsItem.from_dict(mounts_item_data)



                mounts.append(mounts_item)


        grading_config_input_compute_exec = cls(
            type_=type_,
            command=command,
            output_format=output_format,
            poll_command=poll_command,
            mounts=mounts,
        )


        grading_config_input_compute_exec.additional_properties = d
        return grading_config_input_compute_exec

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
