from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.public_variable_type import PublicVariableType

T = TypeVar("T", bound="PublicVariable")


@_attrs_define
class PublicVariable:
    """
    Attributes:
        created_at (datetime.datetime): datetime with the constraint that the value must have timezone info
        created_by (UUID): User who created the variable
        name (str): Environment variable name
        type_ (PublicVariableType): `plain` (readable back) or `secret` (write-only)
        updated_at (datetime.datetime): datetime with the constraint that the value must have timezone info
        updated_by (UUID): User who last updated the variable
        value (None | str): Plain value as stored; always `null` for a secret
    """

    created_at: datetime.datetime
    created_by: UUID
    name: str
    type_: PublicVariableType
    updated_at: datetime.datetime
    updated_by: UUID
    value: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        created_by = str(self.created_by)

        name = self.name

        type_ = self.type_.value

        updated_at = self.updated_at.isoformat()

        updated_by = str(self.updated_by)

        value: None | str
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

        type_ = PublicVariableType(d.pop("type"))

        updated_at = isoparse(d.pop("updated_at"))

        updated_by = UUID(d.pop("updated_by"))

        def _parse_value(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        value = _parse_value(d.pop("value"))

        public_variable = cls(
            created_at=created_at,
            created_by=created_by,
            name=name,
            type_=type_,
            updated_at=updated_at,
            updated_by=updated_by,
            value=value,
        )

        public_variable.additional_properties = d
        return public_variable

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
