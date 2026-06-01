from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.flag_source_declared_type_type_0 import check_flag_source_declared_type_type_0
from ..models.flag_source_declared_type_type_0 import FlagSourceDeclaredTypeType0
from dateutil.parser import isoparse
from typing import cast
import datetime


T = TypeVar("T", bound="FlagSource")


@_attrs_define
class FlagSource:
    """A record of an SDK observing a feature flag from a particular
    service and environment.

    The flags service auto-registers a source the first time an SDK
    reports a flag from a given service/environment pair and refreshes
    `last_seen` on every subsequent report. Each source captures the
    value type and default value the SDK declared in source code at
    that location, which makes it possible to detect when service code
    has drifted from the flag's authoritative configuration.

        Attributes:
            service (None | str | Unset): Service that declared the flag.
            environment (None | str | Unset): Environment in which the service declared the flag.
            declared_type (FlagSourceDeclaredTypeType0 | None | Unset): Value type the SDK reported when registering the
                flag from this service/environment. May differ from the flag's authoritative `type` if the service is running
                stale code.
            declared_default (Any | Unset): Default value the SDK reported when registering the flag from this
                service/environment. May differ from the flag's authoritative `default` if the service is running stale code.
            first_observed (datetime.datetime | None | Unset): When this source was first observed.
            last_seen (datetime.datetime | None | Unset): Most recent time the SDK re-registered this source.
            created_at (datetime.datetime | None | Unset): When the source record was created.
            updated_at (datetime.datetime | None | Unset): When the source record was last modified.
    """

    service: None | str | Unset = UNSET
    environment: None | str | Unset = UNSET
    declared_type: FlagSourceDeclaredTypeType0 | None | Unset = UNSET
    declared_default: Any | Unset = UNSET
    first_observed: datetime.datetime | None | Unset = UNSET
    last_seen: datetime.datetime | None | Unset = UNSET
    created_at: datetime.datetime | None | Unset = UNSET
    updated_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        service: None | str | Unset
        if isinstance(self.service, Unset):
            service = UNSET
        else:
            service = self.service

        environment: None | str | Unset
        if isinstance(self.environment, Unset):
            environment = UNSET
        else:
            environment = self.environment

        declared_type: None | str | Unset
        if isinstance(self.declared_type, Unset):
            declared_type = UNSET
        elif isinstance(self.declared_type, str):
            declared_type = self.declared_type
        else:
            declared_type = self.declared_type

        declared_default = self.declared_default

        first_observed: None | str | Unset
        if isinstance(self.first_observed, Unset):
            first_observed = UNSET
        elif isinstance(self.first_observed, datetime.datetime):
            first_observed = self.first_observed.isoformat()
        else:
            first_observed = self.first_observed

        last_seen: None | str | Unset
        if isinstance(self.last_seen, Unset):
            last_seen = UNSET
        elif isinstance(self.last_seen, datetime.datetime):
            last_seen = self.last_seen.isoformat()
        else:
            last_seen = self.last_seen

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
        field_dict.update({})
        if service is not UNSET:
            field_dict["service"] = service
        if environment is not UNSET:
            field_dict["environment"] = environment
        if declared_type is not UNSET:
            field_dict["declared_type"] = declared_type
        if declared_default is not UNSET:
            field_dict["declared_default"] = declared_default
        if first_observed is not UNSET:
            field_dict["first_observed"] = first_observed
        if last_seen is not UNSET:
            field_dict["last_seen"] = last_seen
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_service(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        service = _parse_service(d.pop("service", UNSET))

        def _parse_environment(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        environment = _parse_environment(d.pop("environment", UNSET))

        def _parse_declared_type(data: object) -> FlagSourceDeclaredTypeType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                declared_type_type_0 = check_flag_source_declared_type_type_0(data)

                return declared_type_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(FlagSourceDeclaredTypeType0 | None | Unset, data)

        declared_type = _parse_declared_type(d.pop("declared_type", UNSET))

        declared_default = d.pop("declared_default", UNSET)

        def _parse_first_observed(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                first_observed_type_0 = isoparse(data)

                return first_observed_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        first_observed = _parse_first_observed(d.pop("first_observed", UNSET))

        def _parse_last_seen(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_seen_type_0 = isoparse(data)

                return last_seen_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        last_seen = _parse_last_seen(d.pop("last_seen", UNSET))

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

        flag_source = cls(
            service=service,
            environment=environment,
            declared_type=declared_type,
            declared_default=declared_default,
            first_observed=first_observed,
            last_seen=last_seen,
            created_at=created_at,
            updated_at=updated_at,
        )

        flag_source.additional_properties = d
        return flag_source

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
