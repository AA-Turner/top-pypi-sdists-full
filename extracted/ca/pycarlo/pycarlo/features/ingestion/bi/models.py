from __future__ import annotations

from dataclasses import dataclass, field

from dataclasses_json import DataClassJsonMixin, config

from pycarlo.features.ingestion.models import (
    AssetRef,
    Tag,
    _check_batch_size,
    _is_empty,
    _is_none,
)

# Allowed values for ``BiAssetRef.relationship_type`` (uppercase). A semantic
# label on a BI→BI reference; the backend stores it as an edge property.
BI_RELATIONSHIP_TYPE_VALUES: frozenset[str] = frozenset(
    {"DERIVES_FROM", "CONTAINED_IN", "REFERENCES"}
)


@dataclass
class BiOwner(DataClassJsonMixin):
    """
    Owner of a BI asset (producer subset).

    ``email`` is strongly preferred — it resolves to a Monte Carlo user. A
    producer that only exposes a vendor user id should resolve it to an email
    where possible, falling back to ``source_id``.

    :param email: Owner's email (preferred identifier).
    :param name: Owner's display name.
    :param source_id: Owner's identifier in the source system.
    """

    email: str | None = field(default=None, metadata=config(exclude=_is_none))
    name: str | None = field(default=None, metadata=config(exclude=_is_none))
    source_id: str | None = field(default=None, metadata=config(exclude=_is_none))


@dataclass
class BiAssetRef(DataClassJsonMixin):
    """
    A BI→BI lineage reference to another BI asset by its ``asset_source_id``,
    used on :attr:`BiAsset.upstream_assets` / :attr:`BiAsset.downstream_assets`.

    :param asset_source_id: The referenced asset's vendor-stable source id
        (within the same container). Required.
    :param relationship_type: Optional semantic edge label; one of
        :data:`BI_RELATIONSHIP_TYPE_VALUES`. Untyped references default to a
        generic downstream edge on the backend.

    .. note:: ``container_source_id`` (cross-container references) is
        intentionally omitted — the v1 normalizer rejects it, so exposing it
        would let a caller build a reference that silently never resolves. It
        will be added when cross-container lineage is supported.
    """

    asset_source_id: str
    relationship_type: str | None = field(default=None, metadata=config(exclude=_is_none))

    def __post_init__(self) -> None:
        if (
            self.relationship_type is not None
            and self.relationship_type not in BI_RELATIONSHIP_TYPE_VALUES
        ):
            raise ValueError(
                f"BiAssetRef.relationship_type must be one of "
                f"{sorted(BI_RELATIONSHIP_TYPE_VALUES)} (or None); got {self.relationship_type!r}."
            )


@dataclass
class BiAsset(DataClassJsonMixin):
    """
    A BI asset (dashboard, report, dataset, …) as a producer pushes it to
    ``POST /ingest/v1/bi/metadata``.

    ``asset_source_id``, ``name``, and ``asset_type`` are required; everything
    else is optional and stripped from the serialized dict when unset. The
    owning ``custom-bi-connector`` container's Monte Carlo UUID is carried in
    the top-level ``resource.uuid`` of the request, not per-asset.

    :param asset_source_id: Vendor-stable id, unique within the container. Must
        be the vendor's stable id, not a display name.
    :param name: Display name; the lineage-node label and search title.
    :param asset_type: Free-form type label in the producer's vocabulary
        (``"dashboard"``, ``"Look"``, ``"semantic model"``, …). Rendered
        verbatim; never validated.
    :param description: Optional human-readable description.
    :param asset_url: Optional URL to view the asset in the source system.
    :param folder: Optional folder / namespace string.
    :param owner: Optional :class:`BiOwner`.
    :param created_time: Optional ISO8601 creation time.
    :param last_modified_time: Optional ISO8601 last-modified time.
    :param last_viewed_time: Optional ISO8601 last-viewed time.
    :param view_count: Optional view count.
    :param is_certified: Optional certification flag.
    :param certification_note: Optional certification note.
    :param is_archived: Optional archived flag.
    :param upstream_assets: BI→BI references this asset derives from.
    :param downstream_assets: BI→BI references that derive from this asset.
    :param inputs: Warehouse-table references upstream of this asset, via the
        shared :class:`AssetRef` (mcon / fully-qualified name + ``asset_type`` +
        ``role``). A BI asset always *reads from* these tables, so ``role``
        should always be ``"INPUT"``. ``role`` is UPPERCASE on the wire and the
        normalizer lowercases it to the canonical model.
    :param properties: Searchable key/value tags (:class:`Tag`).
    :param attributes: Free-form vendor-specific attributes.
    """

    asset_source_id: str
    name: str
    asset_type: str
    description: str | None = field(default=None, metadata=config(exclude=_is_none))
    asset_url: str | None = field(default=None, metadata=config(exclude=_is_none))
    folder: str | None = field(default=None, metadata=config(exclude=_is_none))
    owner: BiOwner | None = field(default=None, metadata=config(exclude=_is_none))
    created_time: str | None = field(default=None, metadata=config(exclude=_is_none))
    last_modified_time: str | None = field(default=None, metadata=config(exclude=_is_none))
    last_viewed_time: str | None = field(default=None, metadata=config(exclude=_is_none))
    view_count: int | None = field(default=None, metadata=config(exclude=_is_none))
    is_certified: bool | None = field(default=None, metadata=config(exclude=_is_none))
    certification_note: str | None = field(default=None, metadata=config(exclude=_is_none))
    is_archived: bool | None = field(default=None, metadata=config(exclude=_is_none))
    upstream_assets: list[BiAssetRef] = field(
        default_factory=list, metadata=config(exclude=_is_empty)
    )
    downstream_assets: list[BiAssetRef] = field(
        default_factory=list, metadata=config(exclude=_is_empty)
    )
    inputs: list[AssetRef] = field(default_factory=list, metadata=config(exclude=_is_empty))
    properties: list[Tag] = field(default_factory=list, metadata=config(exclude=_is_empty))
    attributes: dict | None = field(default=None, metadata=config(exclude=_is_none))


def build_bi_metadata_payload(
    resource_uuid: str,
    resource_type: str,
    events: list[BiAsset],
) -> dict:
    """Build the full JSON payload for ``POST /ingest/v1/bi/metadata``.

    Events are flat :class:`BiAsset` dicts — there is no per-event wrapper
    (unlike ETL's ``etl_asset``), matching the common ``BiMetadataRequest``
    contract. Batch size must be 1–100.

    :param resource_uuid: UUID of the ``custom-bi-connector`` container.
    :param resource_type: Resource type identifier (e.g. ``"custom-bi-connector"``).
    :param events: One or more :class:`BiAsset` objects. Batch size: 1–100.
    :raises ValueError: If the batch is empty or exceeds 100 events.
    """
    _check_batch_size(events, "build_bi_metadata_payload")
    return {
        "event_type": "BI_METADATA",
        "resource": {
            "uuid": resource_uuid,
            "resource_type": resource_type,
        },
        "events": [e.to_dict() for e in events],
    }
