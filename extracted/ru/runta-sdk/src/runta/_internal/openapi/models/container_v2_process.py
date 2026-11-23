from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ContainerV2Process")


@_attrs_define
class ContainerV2Process:
    """
    Attributes:
        process_id (str):
        runtime_id (str):
        terminal (bool):
        state (str):
        exit_code (int | Unset):
    """

    process_id: str
    runtime_id: str
    terminal: bool
    state: str
    exit_code: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        process_id = self.process_id

        runtime_id = self.runtime_id

        terminal = self.terminal

        state = self.state

        exit_code = self.exit_code

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "process_id": process_id,
                "runtime_id": runtime_id,
                "terminal": terminal,
                "state": state,
            }
        )
        if exit_code is not UNSET:
            field_dict["exit_code"] = exit_code

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        process_id = d.pop("process_id")

        runtime_id = d.pop("runtime_id")

        terminal = d.pop("terminal")

        state = d.pop("state")

        exit_code = d.pop("exit_code", UNSET)

        container_v2_process = cls(
            process_id=process_id,
            runtime_id=runtime_id,
            terminal=terminal,
            state=state,
            exit_code=exit_code,
        )

        container_v2_process.additional_properties = d
        return container_v2_process

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
