from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ManagedAgentsNextAction")



@_attrs_define
class ManagedAgentsNextAction:
    """ The literal next API call to make. Included on errors and results whose resolution is one known call, so a caller
    need not infer it.

        Example:
            {'method': 'example', 'operation_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'path': 'example'}

        Attributes:
            method (str): HTTP method of that call.
            operation_id (str): OpenAPI operation id of the call to make next, e.g. createEnvironmentSetupRun.
            path (str): Path of that call with path parameters already filled in.
     """

    method: str
    operation_id: str
    path: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        method = self.method

        operation_id = self.operation_id

        path = self.path


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "method": method,
            "operation_id": operation_id,
            "path": path,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        method = d.pop("method")

        operation_id = d.pop("operation_id")

        path = d.pop("path")

        managed_agents_next_action = cls(
            method=method,
            operation_id=operation_id,
            path=path,
        )


        managed_agents_next_action.additional_properties = d
        return managed_agents_next_action

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
