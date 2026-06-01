from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import cast
import datetime


T = TypeVar("T", bound="Group")


@_attrs_define
class Group:
    """An Environment Access Group: a named bundle of standard
    environments its members may manage.

    A user's effective managed-environment set is the union across all
    their groups (or "all" if any of their groups grants ``["*"]``).
    Roles answer *what* a user may do; groups answer *which environments*
    that capability reaches.

        Example:
            {'created_at': '2026-05-26T11:02:16.616Z', 'description': 'Senior engineers who may change production.',
                'managed_environments': ['production'], 'name': 'Production Stewards', 'system': False, 'updated_at':
                '2026-05-26T11:02:16.616Z'}

        Attributes:
            name (str): Human-readable name for the group.
            description (None | str | Unset): Free-text description shown on the group's detail page.
            managed_environments (list[str] | Unset): The set of environments members of this group may manage. Either the
                exact value `["*"]` to grant every standard environment, or an explicit array of standard environment keys. Ad-
                hoc environments are never listed here — they are exempt from group governance and remain manageable by every
                member of the account.
            system (bool | Unset): True for built-in groups the platform reserves. The `default` group has `system=true`; it
                cannot be deleted or renamed, though its `managed_environments` may be narrowed. Default: False.
            created_at (datetime.datetime | None | Unset): When the group was created.
            updated_at (datetime.datetime | None | Unset): When the group was last modified.
    """

    name: str
    description: None | str | Unset = UNSET
    managed_environments: list[str] | Unset = UNSET
    system: bool | Unset = False
    created_at: datetime.datetime | None | Unset = UNSET
    updated_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        managed_environments: list[str] | Unset = UNSET
        if not isinstance(self.managed_environments, Unset):
            managed_environments = self.managed_environments

        system = self.system

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
        if description is not UNSET:
            field_dict["description"] = description
        if managed_environments is not UNSET:
            field_dict["managed_environments"] = managed_environments
        if system is not UNSET:
            field_dict["system"] = system
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        managed_environments = cast(list[str], d.pop("managed_environments", UNSET))

        system = d.pop("system", UNSET)

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

        group = cls(
            name=name,
            description=description,
            managed_environments=managed_environments,
            system=system,
            created_at=created_at,
            updated_at=updated_at,
        )

        group.additional_properties = d
        return group

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
