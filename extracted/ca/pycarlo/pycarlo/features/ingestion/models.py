from __future__ import annotations

from dataclasses import dataclass, field

from dataclasses_json import DataClassJsonMixin, config


def _is_none(value: object) -> bool:
    return value is None


def _is_empty(value: object) -> bool:
    return not value


@dataclass
class Tag(DataClassJsonMixin):
    """A key-value tag attached to an asset."""

    key: str
    value: str


@dataclass
class AssetField(DataClassJsonMixin):
    """A column/field definition for a relational asset."""

    name: str
    type: str
    description: str | None = field(default=None, metadata=config(exclude=_is_none))


@dataclass
class AssetMetadata(DataClassJsonMixin):
    """Core metadata describing a relational asset (table or view)."""

    name: str
    database: str
    schema: str
    description: str | None = field(default=None, metadata=config(exclude=_is_none))
    view_query: str | None = field(default=None, metadata=config(exclude=_is_none))
    created_on: str | None = field(default=None, metadata=config(exclude=_is_none))


@dataclass
class AssetVolume(DataClassJsonMixin):
    """Volume (size) information for a relational asset."""

    row_count: int | None = field(default=None, metadata=config(exclude=_is_none))
    byte_count: int | None = field(default=None, metadata=config(exclude=_is_none))


@dataclass
class AssetFreshness(DataClassJsonMixin):
    """Freshness (recency) information for a relational asset."""

    last_update_time: str | None = field(default=None, metadata=config(exclude=_is_none))


@dataclass
class RelationalAsset(DataClassJsonMixin):
    """
    A relational asset (table or view) with its metadata, schema, volume,
    and freshness information.

    :param type: Asset type, e.g. ``"TABLE"`` or ``"VIEW"`` (uppercase).
    :param metadata: Core metadata (name, database, schema, etc.).
    :param tags: Optional key-value tags.
    :param fields: Optional list of columns/fields.
    :param volume: Optional volume (row/byte counts).
    :param freshness: Optional freshness (last update time).
    """

    type: str
    metadata: AssetMetadata
    tags: list[Tag] = field(default_factory=list, metadata=config(exclude=_is_empty))
    fields: list[AssetField] = field(default_factory=list, metadata=config(exclude=_is_empty))
    volume: AssetVolume | None = field(default=None, metadata=config(exclude=_is_none))
    freshness: AssetFreshness | None = field(default=None, metadata=config(exclude=_is_none))


def build_metadata_payload(
    resource_uuid: str,
    resource_type: str,
    events: list[RelationalAsset],
) -> dict:
    """Build the full JSON payload for ``POST /ingest/v1/metadata``."""
    return {
        "event_type": "METADATA",
        "resource": {
            "uuid": resource_uuid,
            "resource_type": resource_type,
        },
        "events": [{"relational_asset": e.to_dict()} for e in events],
    }
