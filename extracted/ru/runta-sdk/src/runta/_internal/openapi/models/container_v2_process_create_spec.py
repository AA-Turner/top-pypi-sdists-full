from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.container_v2_process_create_spec_environment import (
        ContainerV2ProcessCreateSpecEnvironment,
    )
    from ..models.container_v2_process_create_spec_terminal import (
        ContainerV2ProcessCreateSpecTerminal,
    )


T = TypeVar("T", bound="ContainerV2ProcessCreateSpec")


@_attrs_define
class ContainerV2ProcessCreateSpec:
    """
    Attributes:
        argv (list[str]):
        environment (ContainerV2ProcessCreateSpecEnvironment | Unset):
        working_directory (str | Unset):
        stdin (bool | Unset):  Default: True.
        terminal (ContainerV2ProcessCreateSpecTerminal | Unset):
    """

    argv: list[str]
    environment: ContainerV2ProcessCreateSpecEnvironment | Unset = UNSET
    working_directory: str | Unset = UNSET
    stdin: bool | Unset = True
    terminal: ContainerV2ProcessCreateSpecTerminal | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        argv = self.argv

        environment: dict[str, Any] | Unset = UNSET
        if not isinstance(self.environment, Unset):
            environment = self.environment.to_dict()

        working_directory = self.working_directory

        stdin = self.stdin

        terminal: dict[str, Any] | Unset = UNSET
        if not isinstance(self.terminal, Unset):
            terminal = self.terminal.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "argv": argv,
            }
        )
        if environment is not UNSET:
            field_dict["environment"] = environment
        if working_directory is not UNSET:
            field_dict["working_directory"] = working_directory
        if stdin is not UNSET:
            field_dict["stdin"] = stdin
        if terminal is not UNSET:
            field_dict["terminal"] = terminal

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.container_v2_process_create_spec_environment import (
            ContainerV2ProcessCreateSpecEnvironment,
        )
        from ..models.container_v2_process_create_spec_terminal import (
            ContainerV2ProcessCreateSpecTerminal,
        )

        d = dict(src_dict)
        argv = cast(list[str], d.pop("argv"))

        _environment = d.pop("environment", UNSET)
        environment: ContainerV2ProcessCreateSpecEnvironment | Unset
        if isinstance(_environment, Unset):
            environment = UNSET
        else:
            environment = ContainerV2ProcessCreateSpecEnvironment.from_dict(
                _environment
            )

        working_directory = d.pop("working_directory", UNSET)

        stdin = d.pop("stdin", UNSET)

        _terminal = d.pop("terminal", UNSET)
        terminal: ContainerV2ProcessCreateSpecTerminal | Unset
        if isinstance(_terminal, Unset):
            terminal = UNSET
        else:
            terminal = ContainerV2ProcessCreateSpecTerminal.from_dict(_terminal)

        container_v2_process_create_spec = cls(
            argv=argv,
            environment=environment,
            working_directory=working_directory,
            stdin=stdin,
            terminal=terminal,
        )

        container_v2_process_create_spec.additional_properties = d
        return container_v2_process_create_spec

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
