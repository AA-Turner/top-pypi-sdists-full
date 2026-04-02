from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.slurm_command_result_mode_enum import SlurmCommandResultModeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="SlurmCommandResultRequest")


@_attrs_define
class SlurmCommandResultRequest:
    """
    Attributes:
        resource_uuid (UUID): UUID of the resource the command was applied to
        success (bool): Whether the command was applied successfully
        error_message (Union[Unset, str]): Error message if the command failed Default: ''.
        mode (Union[Unset, SlurmCommandResultModeEnum]):  Default: SlurmCommandResultModeEnum.PRODUCTION.
        commands_executed (Union[Unset, list[str]]): List of shell commands actually executed by the site agent
    """

    resource_uuid: UUID
    success: bool
    error_message: Union[Unset, str] = ""
    mode: Union[Unset, SlurmCommandResultModeEnum] = SlurmCommandResultModeEnum.PRODUCTION
    commands_executed: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resource_uuid = str(self.resource_uuid)

        success = self.success

        error_message = self.error_message

        mode: Union[Unset, str] = UNSET
        if not isinstance(self.mode, Unset):
            mode = self.mode.value

        commands_executed: Union[Unset, list[str]] = UNSET
        if not isinstance(self.commands_executed, Unset):
            commands_executed = self.commands_executed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resource_uuid": resource_uuid,
                "success": success,
            }
        )
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if mode is not UNSET:
            field_dict["mode"] = mode
        if commands_executed is not UNSET:
            field_dict["commands_executed"] = commands_executed

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        resource_uuid = UUID(d.pop("resource_uuid"))

        success = d.pop("success")

        error_message = d.pop("error_message", UNSET)

        _mode = d.pop("mode", UNSET)
        mode: Union[Unset, SlurmCommandResultModeEnum]
        if isinstance(_mode, Unset):
            mode = UNSET
        else:
            mode = SlurmCommandResultModeEnum(_mode)

        commands_executed = cast(list[str], d.pop("commands_executed", UNSET))

        slurm_command_result_request = cls(
            resource_uuid=resource_uuid,
            success=success,
            error_message=error_message,
            mode=mode,
            commands_executed=commands_executed,
        )

        slurm_command_result_request.additional_properties = d
        return slurm_command_result_request

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
