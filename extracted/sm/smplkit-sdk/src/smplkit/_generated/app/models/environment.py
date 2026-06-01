from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.environment_classification import check_environment_classification
from ..models.environment_classification import EnvironmentClassification
from dateutil.parser import isoparse
from typing import cast
import datetime


T = TypeVar("T", bound="Environment")


@_attrs_define
class Environment:
    """A named deployment context — for example, `production`, `staging`, or
    `development`. Resources scoped to an environment (such as config items
    and feature flags) are evaluated against environment-specific values.

        Example:
            {'classification': 'STANDARD', 'color': '#2ecc71', 'created_at': '2026-03-20T11:02:16.616Z', 'managed': True,
                'name': 'Production', 'updated_at': '2026-03-20T11:02:16.616Z'}

        Attributes:
            name (str): Human-readable name for the environment.
            color (None | str | Unset): Display color used by the console to badge the environment. Accepts any CSS color
                string.
            classification (EnvironmentClassification | Unset): `STANDARD` for environments deliberately created (and shown
                by default in the environment grid); `AD_HOC` for auto-discovered environments seen in SDK traffic (hidden from
                the default view). Case-insensitive on input. Independent of the `managed` flag. Default: 'STANDARD'.
            managed (bool | Unset): When `true`, per-environment resource values can be set against this environment and it
                counts toward the account's managed-environments quota. When `false`, the environment is view-only: existing
                values are displayed for comparison but no new values can be written. Promotion and demotion flip this boolean
                via `PUT /api/v1/environments/{id}`; promotion is subject to the quota. Default: False.
            created_at (datetime.datetime | None | Unset): When the environment was created.
            updated_at (datetime.datetime | None | Unset): When the environment was last modified.
    """

    name: str
    color: None | str | Unset = UNSET
    classification: EnvironmentClassification | Unset = "STANDARD"
    managed: bool | Unset = False
    created_at: datetime.datetime | None | Unset = UNSET
    updated_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        color: None | str | Unset
        if isinstance(self.color, Unset):
            color = UNSET
        else:
            color = self.color

        classification: str | Unset = UNSET
        if not isinstance(self.classification, Unset):
            classification = self.classification

        managed = self.managed

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
        if color is not UNSET:
            field_dict["color"] = color
        if classification is not UNSET:
            field_dict["classification"] = classification
        if managed is not UNSET:
            field_dict["managed"] = managed
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        def _parse_color(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        color = _parse_color(d.pop("color", UNSET))

        _classification = d.pop("classification", UNSET)
        classification: EnvironmentClassification | Unset
        if isinstance(_classification, Unset):
            classification = UNSET
        else:
            classification = check_environment_classification(_classification)

        managed = d.pop("managed", UNSET)

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

        environment = cls(
            name=name,
            color=color,
            classification=classification,
            managed=managed,
            created_at=created_at,
            updated_at=updated_at,
        )

        environment.additional_properties = d
        return environment

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
