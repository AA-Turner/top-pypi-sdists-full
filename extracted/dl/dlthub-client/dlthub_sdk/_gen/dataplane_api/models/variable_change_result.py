from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.variable_change_result_status_type_0 import (
    VariableChangeResultStatusType0,
)

T = TypeVar("T", bound="VariableChangeResult")


@_attrs_define
class VariableChangeResult:
    """
    Attributes:
        name (str): Environment variable name
        status (str | VariableChangeResultStatusType0): What happened to this variable
    """

    name: str
    status: str | VariableChangeResultStatusType0
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        status: str
        if isinstance(self.status, VariableChangeResultStatusType0):
            status = self.status.value
        else:
            status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "status": status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        def _parse_status(data: object) -> str | VariableChangeResultStatusType0:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                status_type_0 = VariableChangeResultStatusType0(data)

                return status_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(str | VariableChangeResultStatusType0, data)

        status = _parse_status(d.pop("status"))

        variable_change_result = cls(
            name=name,
            status=status,
        )

        variable_change_result.additional_properties = d
        return variable_change_result

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
