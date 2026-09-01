from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import (
    Any,
    Literal,
    TypeVar,
    cast,
)
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="PlainPublicVariable")


@_attrs_define
class PlainPublicVariable:
    """
    Attributes:
        created_at (datetime.datetime): datetime with the constraint that the value must have timezone info
        created_by (UUID): User who created the variable
        name (str): Environment variable name
        type_ (Literal['plain']): Readable back
        updated_at (datetime.datetime): datetime with the constraint that the value must have timezone info
        updated_by (UUID): User who last updated the variable
        value (str): Value as stored
    """

    created_at: datetime.datetime
    created_by: UUID
    name: str
    type_: Literal["plain"]
    updated_at: datetime.datetime
    updated_by: UUID
    value: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        created_by = str(self.created_by)

        name = self.name

        type_ = self.type_

        updated_at = self.updated_at.isoformat()

        updated_by = str(self.updated_by)

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "created_at": created_at,
                "created_by": created_by,
                "name": name,
                "type": type_,
                "updated_at": updated_at,
                "updated_by": updated_by,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created_at = isoparse(d.pop("created_at"))

        created_by = UUID(d.pop("created_by"))

        name = d.pop("name")

        type_ = cast(Literal["plain"], d.pop("type"))
        if type_ != "plain":
            raise ValueError(f"type must match const 'plain', got '{type_}'")

        updated_at = isoparse(d.pop("updated_at"))

        updated_by = UUID(d.pop("updated_by"))

        value = d.pop("value")

        plain_public_variable = cls(
            created_at=created_at,
            created_by=created_by,
            name=name,
            type_=type_,
            updated_at=updated_at,
            updated_by=updated_by,
            value=value,
        )

        plain_public_variable.additional_properties = d
        return plain_public_variable

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
