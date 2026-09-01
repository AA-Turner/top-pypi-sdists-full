from __future__ import annotations

from collections.abc import Mapping
from typing import (
    Any,
    Literal,
    TypeVar,
    cast,
)

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SecretVariableUpsert")


@_attrs_define
class SecretVariableUpsert:
    """
    Attributes:
        name (str): Environment variable name. Names the runtime sets are rejected on write:
            DASHBOARD__SYNC_FROM_RUNTIME, HOME, PATH, PORT, PYTHONHOME, PYTHONPATH, PYTHONUNBUFFERED, RUNTIME__RUN_ID,
            RUNTIME__WORKSPACE_ID, WORKSPACE__PROFILE, and anything starting with SEND__ARTIFACTS__, SYNC__ARTIFACTS__,
            DESTINATION__PLAYGROUND__, RUNTIME__DLTHUB_
        type_ (Literal['secret']): Write-only, never shown again
        value (str): Value exported into the run environment; must not be empty
    """

    name: str
    type_: Literal["secret"]
    value: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        type_ = self.type_

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "type": type_,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        type_ = cast(Literal["secret"], d.pop("type"))
        if type_ != "secret":
            raise ValueError(f"type must match const 'secret', got '{type_}'")

        value = d.pop("value")

        secret_variable_upsert = cls(
            name=name,
            type_=type_,
            value=value,
        )

        secret_variable_upsert.additional_properties = d
        return secret_variable_upsert

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
