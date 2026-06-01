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
    from ..models.context_attributes import ContextAttributes


T = TypeVar("T", bound="Context")


@_attrs_define
class Context:
    """A specific instance of a context type — for example, a particular
    user, account, or device — together with the attributes observed on it.

    Context instances are addressed by a composite identifier of the form
    `context_type:key` (e.g. `user:alice-123`).

        Example:
            {'attributes': {'first_name': 'Alice', 'plan': 'enterprise'}, 'context_type': 'user', 'created_at':
                '2026-03-31T10:00:00Z', 'key': 'alice-123', 'name': 'Alice Smith', 'updated_at': '2026-03-31T10:00:00Z'}

        Attributes:
            context_type (str): Key of the context type this instance belongs to (e.g. `user`, `account`).
            key (None | str | Unset): Entity identifier within the context type (e.g. `alice-123`). Together with
                `context_type` it forms the composite `id` `context_type:key`. Always populated in responses; declared optional
                only so SDK consumers can construct a draft Context without a key. Set by the bulk-register API; not editable.
            name (None | str | Unset): Human-readable display name for the context instance.
            attributes (ContextAttributes | Unset): Observed attribute values for this context instance. The key set is
                conventionally aligned with the parent context type's known attribute keys, but additional keys are accepted.
            created_at (datetime.datetime | None | Unset): When the context instance was first registered.
            updated_at (datetime.datetime | None | Unset): When the context instance was last modified.
    """

    context_type: str
    key: None | str | Unset = UNSET
    name: None | str | Unset = UNSET
    attributes: ContextAttributes | Unset = UNSET
    created_at: datetime.datetime | None | Unset = UNSET
    updated_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        context_type = self.context_type

        key: None | str | Unset
        if isinstance(self.key, Unset):
            key = UNSET
        else:
            key = self.key

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
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
                "context_type": context_type,
            }
        )
        if key is not UNSET:
            field_dict["key"] = key
        if name is not UNSET:
            field_dict["name"] = name
        if attributes is not UNSET:
            field_dict["attributes"] = attributes
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.context_attributes import ContextAttributes

        d = dict(src_dict)
        context_type = d.pop("context_type")

        def _parse_key(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        key = _parse_key(d.pop("key", UNSET))

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        _attributes = d.pop("attributes", UNSET)
        attributes: ContextAttributes | Unset
        if isinstance(_attributes, Unset):
            attributes = UNSET
        else:
            attributes = ContextAttributes.from_dict(_attributes)

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

        context = cls(
            context_type=context_type,
            key=key,
            name=name,
            attributes=attributes,
            created_at=created_at,
            updated_at=updated_at,
        )

        context.additional_properties = d
        return context

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
