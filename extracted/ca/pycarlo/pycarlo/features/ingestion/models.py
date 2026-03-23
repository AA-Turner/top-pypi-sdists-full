from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum

from dataclasses_json import DataClassJsonMixin, config


def _datetime_to_iso8601(dt: datetime) -> str:
    """Serialize datetime to ISO8601 string with trailing Z for UTC."""
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _iso8601_to_datetime(s: str) -> datetime:
    """Parse ISO8601 string to datetime (handles Z suffix on Python <3.11)."""
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


_iso8601_field = config(
    encoder=_datetime_to_iso8601,
    decoder=_iso8601_to_datetime,
)


def _is_none(value: object) -> bool:
    return value is None


def _is_empty(value: object) -> bool:
    return not value


@dataclass
class Tag(DataClassJsonMixin):
    """A key-value tag attached to an asset. Value is optional for key-only tags."""

    key: str
    value: str | None = field(default=None, metadata=config(exclude=_is_none))


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
class QueryLogEntry(DataClassJsonMixin):
    """
    A single query log event for the query log ingestion API.

    :param start_time: When the query started (datetime; serialized to ISO8601).
    :param end_time: When the query finished (datetime; serialized to ISO8601).
    :param query_text: The SQL or query text that was executed.
    :param query_id: Optional identifier for the query (e.g. warehouse query ID).
    :param user: Optional user who ran the query.
    :param error_code: Optional error code (string or integer) if the query failed.
    :param error_text: Optional error message if the query failed.
    :param returned_rows: Optional number of rows returned.
    :param extra: Optional dict for additional vendor-specific fields.
    """

    start_time: datetime = field(metadata=_iso8601_field)
    end_time: datetime = field(metadata=_iso8601_field)
    query_text: str
    query_id: str | None = field(default=None, metadata=config(exclude=_is_none))
    user: str | None = field(default=None, metadata=config(exclude=_is_none))
    error_code: str | int | None = field(default=None, metadata=config(exclude=_is_none))
    error_text: str | None = field(default=None, metadata=config(exclude=_is_none))
    returned_rows: int | None = field(default=None, metadata=config(exclude=_is_none))
    extra: dict[str, object] | None = field(default=None, metadata=config(exclude=_is_none))


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


class LineageEventType(str, Enum):
    """Known event types for the lineage ingest endpoint."""

    LINEAGE = "LINEAGE"
    COLUMN_LINEAGE = "COLUMN_LINEAGE"


@dataclass
class LineageAssetRef(DataClassJsonMixin):
    """
    A reference to a table or view used in lineage events.

    :param type: Asset type, e.g. ``"TABLE"`` or ``"VIEW"`` (uppercase).
        The set of accepted values is defined by the backend and may expand
        over time (currently includes ``TABLE``, ``VIEW``, ``EXTERNAL``,
        ``WILDCARD``).
    :param name: Table or view name.
    :param database: Database name.
    :param schema: Schema name.
    :param asset_id: Optional local identifier used by column-level lineage
        ``fields`` to cross-reference this asset.

    .. note:: Field ordering
        ``name`` is declared before ``database``/``schema`` to work around
        a ``DataClassJsonMixin`` interaction where the inherited ``schema``
        classmethod causes Python's dataclasses to treat the ``schema``
        field as having a default value, which would require all subsequent
        fields to also have defaults.
    """

    type: str
    name: str
    database: str
    schema: str
    asset_id: str | None = field(default=None, metadata=config(exclude=_is_none))


@dataclass
class ColumnLineageSourceField(DataClassJsonMixin):
    """A source column reference in a column-level lineage mapping."""

    asset_id: str
    field_name: str


@dataclass
class ColumnLineageField(DataClassJsonMixin):
    """
    A column-level lineage mapping describing which source columns
    contribute to a destination column.

    :param name: Name of the destination column.
    :param source_fields: Source columns that feed into this destination column.
    """

    name: str
    source_fields: list[ColumnLineageSourceField]


@dataclass
class LineageEvent(DataClassJsonMixin):
    """
    A lineage event describing data flow from one or more source assets
    to a destination asset, with optional column-level mappings.

    :param destination: The downstream asset.
    :param sources: Upstream assets that feed into the destination.
    :param fields: Optional column-level mappings (used with
        ``COLUMN_LINEAGE`` event type).
    """

    destination: LineageAssetRef
    sources: list[LineageAssetRef]
    fields: list[ColumnLineageField] = field(
        default_factory=list, metadata=config(exclude=_is_empty)
    )


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


def build_lineage_payload(
    resource_uuid: str,
    resource_type: str,
    events: list[LineageEvent],
    event_type: LineageEventType | str | None = None,
) -> dict:
    """
    Build the full JSON payload for ``POST /ingest/v1/lineage``.

    If *event_type* is not given it is auto-detected:
    :attr:`LineageEventType.COLUMN_LINEAGE` when **any** event has
    ``fields``, otherwise :attr:`LineageEventType.LINEAGE`.

    .. note:: Mixed batches
        When a batch contains a mix of events with and without ``fields``,
        the entire payload is tagged as ``COLUMN_LINEAGE``.  The backend
        processes each event individually, so events without ``fields``
        still produce valid table-level lineage edges.
    """
    if event_type is None:
        has_fields = any(e.fields for e in events)
        event_type = LineageEventType.COLUMN_LINEAGE if has_fields else LineageEventType.LINEAGE
    resolved_type = event_type.value if isinstance(event_type, LineageEventType) else event_type
    return {
        "event_type": resolved_type,
        "resource": {
            "uuid": resource_uuid,
            "resource_type": resource_type,
        },
        "events": [e.to_dict() for e in events],
    }


def build_query_log_payload(
    resource_uuid: str,
    log_type: str,
    events: list[QueryLogEntry],
) -> dict:
    """Build the full JSON payload for ``POST /ingest/v1/querylogs``."""
    return {
        "event_type": "QUERY_LOG",
        "resource": {
            "uuid": resource_uuid,
            "log_type": log_type,
        },
        "events": [e.to_dict() for e in events],
    }
