from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.forwarder_type import check_forwarder_type
from ..models.forwarder_type import ForwarderType
from dateutil.parser import isoparse
from typing import cast
from typing import Literal
import datetime

if TYPE_CHECKING:
    from ..models.forwarder_filter_type_0 import ForwarderFilterType0
    from ..models.http_configuration import HttpConfiguration


T = TypeVar("T", bound="Forwarder")


@_attrs_define
class Forwarder:
    """A destination that receives audit events recorded for the account.

    Each event recorded for the account is evaluated against every enabled
    forwarder. If the filter expression evaluates truthy — or is absent —
    the event is shaped by the configured transform and delivered to the
    destination defined by ``configuration``.

        Attributes:
            name (str): Human-readable name for the forwarder. Must contain at least one non-whitespace character.
            forwarder_type (ForwarderType): Supported forwarder destination types (ADR-050).
            configuration (HttpConfiguration): HTTP request configuration used to deliver an event to the destination.

                Used when the parent forwarder's ``forwarder_type`` is one of the
                HTTP-family destinations (``HTTP``, ``DATADOG``, ``SPLUNK_HEC``,
                ``SUMO_LOGIC``, ``NEW_RELIC``, ``HONEYCOMB``, ``ELASTIC``). When other
                transports land (``FTP``, ``SQS``, …) their own configuration schemas
                will join this one as members of a discriminated union under the
                ``configuration`` field of ``Forwarder``.
            description (None | str | Unset): Free-text description for the forwarder.
            enabled (bool | Unset): Whether the forwarder is currently delivering events. Set to `false` to pause deliveries
                without deleting the forwarder. Default: True.
            filter_ (ForwarderFilterType0 | None | Unset): JSON Logic expression evaluated against each event. The event is
                delivered only if the expression returns truthy. Omit to deliver every event.
            transform_type (Literal['JSONATA'] | None | Unset): Engine used to evaluate ``transform``. Must be set whenever
                ``transform`` is set. Today only `JSONATA` is supported.
            transform (Any | None | Unset): Template applied to each event before delivery. The shape depends on
                ``transform_type``: for `JSONATA`, a string containing a JSONata expression. Omit to deliver the event JSON
                unchanged.
            created_at (datetime.datetime | None | Unset): When the forwarder was created.
            updated_at (datetime.datetime | None | Unset): When the forwarder was last modified.
            deleted_at (datetime.datetime | None | Unset): When the forwarder was deleted. `null` for active forwarders.
            version (int | None | Unset): Monotonic counter incremented on every update, starting at 1.
    """

    name: str
    forwarder_type: ForwarderType
    configuration: HttpConfiguration
    description: None | str | Unset = UNSET
    enabled: bool | Unset = True
    filter_: ForwarderFilterType0 | None | Unset = UNSET
    transform_type: Literal["JSONATA"] | None | Unset = UNSET
    transform: Any | None | Unset = UNSET
    created_at: datetime.datetime | None | Unset = UNSET
    updated_at: datetime.datetime | None | Unset = UNSET
    deleted_at: datetime.datetime | None | Unset = UNSET
    version: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.forwarder_filter_type_0 import ForwarderFilterType0

        name = self.name

        forwarder_type: str = self.forwarder_type

        configuration = self.configuration.to_dict()

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        enabled = self.enabled

        filter_: dict[str, Any] | None | Unset
        if isinstance(self.filter_, Unset):
            filter_ = UNSET
        elif isinstance(self.filter_, ForwarderFilterType0):
            filter_ = self.filter_.to_dict()
        else:
            filter_ = self.filter_

        transform_type: Literal["JSONATA"] | None | Unset
        if isinstance(self.transform_type, Unset):
            transform_type = UNSET
        else:
            transform_type = self.transform_type

        transform: Any | None | Unset
        if isinstance(self.transform, Unset):
            transform = UNSET
        else:
            transform = self.transform

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

        deleted_at: None | str | Unset
        if isinstance(self.deleted_at, Unset):
            deleted_at = UNSET
        elif isinstance(self.deleted_at, datetime.datetime):
            deleted_at = self.deleted_at.isoformat()
        else:
            deleted_at = self.deleted_at

        version: int | None | Unset
        if isinstance(self.version, Unset):
            version = UNSET
        else:
            version = self.version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "forwarder_type": forwarder_type,
                "configuration": configuration,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if filter_ is not UNSET:
            field_dict["filter"] = filter_
        if transform_type is not UNSET:
            field_dict["transform_type"] = transform_type
        if transform is not UNSET:
            field_dict["transform"] = transform
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at
        if deleted_at is not UNSET:
            field_dict["deleted_at"] = deleted_at
        if version is not UNSET:
            field_dict["version"] = version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.forwarder_filter_type_0 import ForwarderFilterType0
        from ..models.http_configuration import HttpConfiguration

        d = dict(src_dict)
        name = d.pop("name")

        forwarder_type = check_forwarder_type(d.pop("forwarder_type"))

        configuration = HttpConfiguration.from_dict(d.pop("configuration"))

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))

        enabled = d.pop("enabled", UNSET)

        def _parse_filter_(data: object) -> ForwarderFilterType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                filter_type_0 = ForwarderFilterType0.from_dict(data)

                return filter_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ForwarderFilterType0 | None | Unset, data)

        filter_ = _parse_filter_(d.pop("filter", UNSET))

        def _parse_transform_type(data: object) -> Literal["JSONATA"] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            transform_type_type_0 = cast(Literal["JSONATA"], data)
            if transform_type_type_0 != "JSONATA":
                raise ValueError(f"transform_type_type_0 must match const 'JSONATA', got '{transform_type_type_0}'")
            return transform_type_type_0
            return cast(Literal["JSONATA"] | None | Unset, data)

        transform_type = _parse_transform_type(d.pop("transform_type", UNSET))

        def _parse_transform(data: object) -> Any | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Any | None | Unset, data)

        transform = _parse_transform(d.pop("transform", UNSET))

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

        def _parse_deleted_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                deleted_at_type_0 = isoparse(data)

                return deleted_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        deleted_at = _parse_deleted_at(d.pop("deleted_at", UNSET))

        def _parse_version(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        version = _parse_version(d.pop("version", UNSET))

        forwarder = cls(
            name=name,
            forwarder_type=forwarder_type,
            configuration=configuration,
            description=description,
            enabled=enabled,
            filter_=filter_,
            transform_type=transform_type,
            transform=transform,
            created_at=created_at,
            updated_at=updated_at,
            deleted_at=deleted_at,
            version=version,
        )

        forwarder.additional_properties = d
        return forwarder

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
