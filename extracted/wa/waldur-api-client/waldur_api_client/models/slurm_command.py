from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.slurm_command_parameters import SlurmCommandParameters


T = TypeVar("T", bound="SlurmCommand")


@_attrs_define
class SlurmCommand:
    """
    Attributes:
        type_ (str): Command type: fairshare, limits, qos, reset_usage
        description (str): Human-readable description
        command (str): Actual shell command
        parameters (SlurmCommandParameters): Command parameters
    """

    type_: str
    description: str
    command: str
    parameters: "SlurmCommandParameters"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        description = self.description

        command = self.command

        parameters = self.parameters.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "description": description,
                "command": command,
                "parameters": parameters,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.slurm_command_parameters import SlurmCommandParameters

        d = dict(src_dict)
        type_ = d.pop("type")

        description = d.pop("description")

        command = d.pop("command")

        parameters = SlurmCommandParameters.from_dict(d.pop("parameters"))

        slurm_command = cls(
            type_=type_,
            description=description,
            command=command,
            parameters=parameters,
        )

        slurm_command.additional_properties = d
        return slurm_command

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
