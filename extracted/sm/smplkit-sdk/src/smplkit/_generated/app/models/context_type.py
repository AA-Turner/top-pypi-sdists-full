from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import cast
import datetime

if TYPE_CHECKING:
    from ..models.context_type_attributes import ContextTypeAttributes


T = TypeVar("T", bound="ContextType")


@_attrs_define
class ContextType:
    """A kind of context — for example, `user`, `account`, or `device` — that
    groups together context instances sharing a common set of attributes.

    The known attribute keys for the type accumulate as instances are
    registered; each key carries an optional metadata object describing it.

        Example:
            {'attributes': {'beta_tester': {}, 'first_name': {}, 'plan': {}}, 'created_at': '2026-03-31T10:00:00Z', 'name':
                'User', 'updated_at': '2026-03-31T10:00:00Z'}

        Attributes:
            name (str): Display label for the context type, e.g. `User`, `Account`, or `Device`.
            attributes (ContextTypeAttributes | Unset): Map of known attribute key to per-attribute metadata. The metadata
                object is free-form and may be empty. Keys grow as new attributes are observed on context instances of this
                type.
            created_at (datetime.datetime | None | Unset): When the context type was created.
            updated_at (datetime.datetime | None | Unset): When the context type was last modified.
    """

    name: str
    attributes: ContextTypeAttributes | Unset = UNSET
    created_at: datetime.datetime | None | Unset = UNSET
    updated_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        attributes: dict[str, Any] | Unset = UNSET
        if not isinstance(self.attributes, Unset):
            attributes = self.attributes.to_dict()

        created_at: None | str | Unset
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        updated_at: None | str | Unset
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        elif isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if attributes is not UNSET:
            field_dict["attributes"] = attributes
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.context_type_attributes import ContextTypeAttributes

        d = dict(src_dict)
        name = d.pop("name")

        _attributes = d.pop("attributes", UNSET)
        attributes: ContextTypeAttributes | Unset
        if isinstance(_attributes, Unset):
            attributes = UNSET
        else:
            attributes = ContextTypeAttributes.from_dict(_attributes)

        def _parse_created_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = isoparse(data)

                return created_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        created_at = _parse_created_at(d.pop("created_at", UNSET))

        def _parse_updated_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                updated_at_type_0 = isoparse(data)

                return updated_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        updated_at = _parse_updated_at(d.pop("updated_at", UNSET))

        context_type = cls(
            name=name,
            attributes=attributes,
            created_at=created_at,
            updated_at=updated_at,
        )

        context_type.additional_properties = d
        return context_type

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
