from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ContainerV2WaitResponse")


@_attrs_define
class ContainerV2WaitResponse:
    """
    Attributes:
        exit_code (int):
        exited_at_unix_millis (int):
    """

    exit_code: int
    exited_at_unix_millis: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        exit_code = self.exit_code

        exited_at_unix_millis = self.exited_at_unix_millis

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "exit_code": exit_code,
                "exited_at_unix_millis": exited_at_unix_millis,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        exit_code = d.pop("exit_code")

        exited_at_unix_millis = d.pop("exited_at_unix_millis")

        container_v2_wait_response = cls(
            exit_code=exit_code,
            exited_at_unix_millis=exited_at_unix_millis,
        )

        container_v2_wait_response.additional_properties = d
        return container_v2_wait_response

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
