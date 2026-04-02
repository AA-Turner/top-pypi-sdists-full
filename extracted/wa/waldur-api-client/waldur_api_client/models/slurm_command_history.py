import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.execution_mode_enum import ExecutionModeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="SlurmCommandHistory")


@_attrs_define
class SlurmCommandHistory:
    """
    Attributes:
        uuid (UUID):
        command_type (str): Type of command: fairshare, limits, qos, reset_usage
        description (str): Human-readable description of what the command does
        shell_command (str): Actual shell command that was/would be executed
        executed_at (datetime.datetime):
        parameters (Union[Unset, Any]): Command parameters as key-value pairs
        execution_mode (Union[Unset, ExecutionModeEnum]):
        success (Union[Unset, bool]): Whether the command execution was successful
        error_message (Union[Unset, str]): Error message if command execution failed
    """

    uuid: UUID
    command_type: str
    description: str
    shell_command: str
    executed_at: datetime.datetime
    parameters: Union[Unset, Any] = UNSET
    execution_mode: Union[Unset, ExecutionModeEnum] = UNSET
    success: Union[Unset, bool] = UNSET
    error_message: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        command_type = self.command_type

        description = self.description

        shell_command = self.shell_command

        executed_at = self.executed_at.isoformat()

        parameters = self.parameters

        execution_mode: Union[Unset, str] = UNSET
        if not isinstance(self.execution_mode, Unset):
            execution_mode = self.execution_mode.value

        success = self.success

        error_message = self.error_message

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "command_type": command_type,
                "description": description,
                "shell_command": shell_command,
                "executed_at": executed_at,
            }
        )
        if parameters is not UNSET:
            field_dict["parameters"] = parameters
        if execution_mode is not UNSET:
            field_dict["execution_mode"] = execution_mode
        if success is not UNSET:
            field_dict["success"] = success
        if error_message is not UNSET:
            field_dict["error_message"] = error_message

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        command_type = d.pop("command_type")

        description = d.pop("description")

        shell_command = d.pop("shell_command")

        executed_at = isoparse(d.pop("executed_at"))

        parameters = d.pop("parameters", UNSET)

        _execution_mode = d.pop("execution_mode", UNSET)
        execution_mode: Union[Unset, ExecutionModeEnum]
        if isinstance(_execution_mode, Unset):
            execution_mode = UNSET
        else:
            execution_mode = ExecutionModeEnum(_execution_mode)

        success = d.pop("success", UNSET)

        error_message = d.pop("error_message", UNSET)

        slurm_command_history = cls(
            uuid=uuid,
            command_type=command_type,
            description=description,
            shell_command=shell_command,
            executed_at=executed_at,
            parameters=parameters,
            execution_mode=execution_mode,
            success=success,
            error_message=error_message,
        )

        slurm_command_history.additional_properties = d
        return slurm_command_history

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
