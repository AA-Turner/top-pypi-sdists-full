# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Catalog overrides for regression tests.

This module provides functions for filtering catalog streams to control
the data volume during regression test reads. This is particularly
useful for connectors with large numbers of streams that would
otherwise cause timeouts.

It also builds the catalogs for streams a connection does not sync yet --
typically a stream the PR under test adds -- from the connector's own
DISCOVER output, so those streams can be read at all.

See: https://github.com/airbytehq/airbyte-internal-issues/issues/15844
See: https://github.com/airbytehq/airbyte-internal-issues/issues/17919
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

logger = logging.getLogger(__name__)


def filter_configured_catalog(
    catalog: dict[str, Any],
    selected_streams: set[str],
) -> dict[str, Any]:
    """Filter a configured catalog to only include the specified streams.

    Args:
        catalog: The configured catalog dict (Airbyte protocol format
            with a "streams" key containing configured stream objects).
        selected_streams: Set of stream names to include.

    Returns:
        A new catalog dict containing only the selected streams.

    Raises:
        ValueError: If none of the selected streams are found in the catalog.
    """
    original_streams = catalog.get("streams", [])
    filtered_streams = [
        stream
        for stream in original_streams
        if _get_stream_name(stream) in selected_streams
    ]

    if not filtered_streams:
        available = {_get_stream_name(s) for s in original_streams}
        raise ValueError(
            f"None of the selected streams {selected_streams} were found in the catalog. "
            f"Available streams: {available}"
        )

    matched_names = {_get_stream_name(s) for s in filtered_streams}
    unmatched = selected_streams - matched_names
    if unmatched:
        logger.warning(
            f"Some selected streams were not found in the catalog: {unmatched}"
        )

    logger.info(
        f"Filtered catalog from {len(original_streams)} to {len(filtered_streams)} streams"
    )

    return {"streams": filtered_streams}


def filter_configured_catalog_file(
    catalog_path: Path,
    selected_streams: set[str],
) -> Path:
    """Filter a configured catalog JSON file in-place.

    Args:
        catalog_path: Path to the configured catalog JSON file.
        selected_streams: Set of stream names to include.

    Returns:
        The same catalog_path (modified in-place).
    """
    catalog = json.loads(catalog_path.read_text())
    filtered_catalog = filter_configured_catalog(catalog, selected_streams)
    catalog_path.write_text(json.dumps(filtered_catalog, indent=2))
    return catalog_path


def _get_stream_name(configured_stream: dict[str, Any]) -> str:
    """Extract stream name from a configured stream object.

    Handles both flat format ({"name": "..."}) and nested format
    ({"stream": {"name": "..."}}).
    """
    stream_info = configured_stream.get("stream", configured_stream)
    return stream_info.get("name", "")


InjectedSyncMode = Literal["full_refresh", "incremental"]


class StreamsNotDiscoveredError(ValueError):
    """Streams asked for by name that the version under test does not discover.

    A setup error, not a connector failure: a typo in the stream name, a test
    image that is not the PR's, or a stream the config gates off. Reading on
    would only hand the connector a stream it does not define, which the CDK
    reports as a lone INCOMPLETE status and exits 0 -- a run that reads
    nothing and passes.
    """

    def __init__(self, missing: set[str], discovered: set[str]) -> None:
        self.missing = tuple(sorted(missing))
        self.discovered = tuple(sorted(discovered))
        super().__init__(
            f"Stream(s) not discovered by the version under test: "
            f"{', '.join(self.missing)}. Check the stream name, the test image and "
            f"any config option that gates the stream. Discovered: "
            f"{', '.join(self.discovered) or 'none'}"
        )


@dataclass(frozen=True)
class InjectedCatalogs:
    """The configured catalogs for a read that includes streams the connection lacks.

    The two versions get different catalogs. A stream the reference version
    (the released connector) does not discover has no control side, so it goes
    to the target only: handing it to a control that does not define it would
    read nothing there and make the comparison look covered. A stream both
    versions discover is not new -- it is only unselected on this connection --
    so it goes to both and is compared like any other.

    Attributes:
        target_catalog: The configured catalog for the version under test.
        control_catalog: The configured catalog for the control version.
        new_streams: Discovered by the target, not by the reference version.
        shared_streams: Discovered by both versions, absent from the connection.
        unknown_streams: Discovered by the target; whether the reference version
            has them is unknown, because its DISCOVER was unavailable. Treated
            like new streams, target only, and reported as such.
        kept_target_only: Selected streams already in the configured catalog
            that the reference version does not discover, so they are kept from
            the control. A run without a connection gets its catalog from the
            target's DISCOVER, which holds the PR's new streams already.
        sync_modes: The sync mode each injected stream was configured with,
            and each kept target-only stream when a sync mode was asked for.
        notes: Anything a reviewer should know about how a stream was
            configured, such as an incremental request that fell back.
    """

    target_catalog: dict[str, Any]
    control_catalog: dict[str, Any]
    new_streams: tuple[str, ...] = ()
    shared_streams: tuple[str, ...] = ()
    unknown_streams: tuple[str, ...] = ()
    kept_target_only: tuple[str, ...] = ()
    sync_modes: dict[str, str] = field(default_factory=dict)
    notes: tuple[str, ...] = ()

    @property
    def injected_streams(self) -> tuple[str, ...]:
        """Every stream added to a catalog, whatever its novelty."""
        return tuple(
            sorted((*self.new_streams, *self.shared_streams, *self.unknown_streams))
        )

    @property
    def target_only_streams(self) -> tuple[str, ...]:
        """The streams with no control side: new, kept or of unknown novelty."""
        return tuple(
            sorted((*self.new_streams, *self.unknown_streams, *self.kept_target_only))
        )

    @property
    def changes_anything(self) -> bool:
        """Whether either catalog differs from the configured one, filtered as usual."""
        return bool(self.injected_streams or self.kept_target_only)

    def to_dict(self) -> dict[str, Any]:
        """The bounded summary for the run's payload and artifact: names only."""
        return {
            "new_streams": list(self.new_streams),
            "shared_streams": list(self.shared_streams),
            "unknown_streams": list(self.unknown_streams),
            "kept_target_only": list(self.kept_target_only),
            "sync_modes": dict(self.sync_modes),
            "notes": list(self.notes),
        }


def build_injected_catalogs(
    configured_catalog: dict[str, Any] | None,
    selected_streams: set[str],
    target_discovered: dict[str, Any],
    reference_discovered: dict[str, Any] | None,
    *,
    sync_mode: InjectedSyncMode | None = None,
) -> InjectedCatalogs:
    """Build the control and target catalogs for streams the connection lacks.

    Selected streams the connection already syncs keep their configured entry,
    so their sync mode, cursor and primary key stay the customer's. Selected
    streams it lacks are configured from the target's discovered catalog and
    sorted by novelty against the reference version's discovered catalog. A
    kept entry the reference version does not discover stays in the target's
    catalog only, as a new stream would.

    Args:
        configured_catalog: The connection's configured catalog, or `None` when
            the run has none.
        selected_streams: The stream names to read. Names the connection does
            not sync are the ones injected.
        target_discovered: The catalog the version under test discovered, as a
            protocol `AirbyteCatalog` dict.
        reference_discovered: The catalog the control version discovered, or
            `None` when its DISCOVER was not available.
        sync_mode: The sync mode for injected streams. `None` prefers full
            refresh. `incremental` falls back to full refresh, with a note, for
            a stream that cannot be read incrementally.

    Returns:
        The two catalogs and how each injected stream was classified.

    Raises:
        StreamsNotDiscoveredError: A selected stream is neither on the
            connection nor in the target's discovered catalog.
    """
    configured = list((configured_catalog or {}).get("streams", []))
    kept = [s for s in configured if _get_stream_name(s) in selected_streams]
    missing = selected_streams - {_get_stream_name(s) for s in configured}

    discovered = {
        stream.get("name", ""): stream
        for stream in target_discovered.get("streams", [])
    }
    not_discovered = missing - discovered.keys()
    if not_discovered:
        raise StreamsNotDiscoveredError(not_discovered, set(discovered))

    reference_names = (
        {stream.get("name", "") for stream in reference_discovered.get("streams", [])}
        if reference_discovered is not None
        else None
    )

    kept_target_only = sorted(
        name
        for name in (_get_stream_name(s) for s in kept)
        if reference_names is not None and name not in reference_names
    )

    new: list[str] = []
    shared: list[str] = []
    unknown: list[str] = []
    for name in sorted(missing):
        if reference_names is None:
            unknown.append(name)
        elif name in reference_names:
            shared.append(name)
        else:
            new.append(name)

    # A kept target-only stream is reconfigured only when a sync mode was asked
    # for: on a run without a connection its entry is the generated one, so the
    # requested mode would otherwise be dropped without a word.
    configure = sorted(missing)
    if sync_mode is not None:
        configure += [name for name in kept_target_only if name in discovered]
    sync_modes: dict[str, str] = {}
    notes: list[str] = []
    entries: dict[str, dict[str, Any]] = {}
    for name in configure:
        entry, note = _configure_discovered_stream(discovered[name], sync_mode)
        entries[name] = entry
        sync_modes[name] = entry["sync_mode"]
        if note:
            notes.append(note)

    return InjectedCatalogs(
        target_catalog={
            "streams": [
                *(entries.get(_get_stream_name(s), s) for s in kept),
                *(entries[n] for n in sorted(missing)),
            ]
        },
        control_catalog={
            "streams": [
                *(s for s in kept if _get_stream_name(s) not in kept_target_only),
                *(entries[n] for n in shared),
            ]
        },
        new_streams=tuple(new),
        shared_streams=tuple(shared),
        unknown_streams=tuple(unknown),
        kept_target_only=tuple(kept_target_only),
        sync_modes=sync_modes,
        notes=tuple(notes),
    )


def _configure_discovered_stream(
    stream: dict[str, Any], sync_mode: InjectedSyncMode | None
) -> tuple[dict[str, Any], str | None]:
    """Configure one discovered stream the way a new connection would.

    Incremental needs a cursor: the source-defined one, or the stream's
    `default_cursor_field`. A stream with neither cannot be read
    incrementally, so it falls back to full refresh when it supports it.

    Returns:
        The configured stream and, when the requested mode was not used, why.
    """
    name = stream.get("name", "")
    supported = stream.get("supported_sync_modes") or ["full_refresh"]
    cursor = stream.get("default_cursor_field") or []
    can_incremental = "incremental" in supported and bool(
        cursor or stream.get("source_defined_cursor")
    )
    note: str | None = None

    if sync_mode == "incremental" and can_incremental:
        chosen = "incremental"
    elif "full_refresh" in supported:
        chosen = "full_refresh"
        if sync_mode == "incremental":
            note = (
                f"{name}: read in full refresh, because it cannot be read "
                "incrementally (no incremental support or no cursor)"
            )
    else:
        chosen = "incremental"

    configured: dict[str, Any] = {
        "stream": stream,
        "sync_mode": chosen,
        "destination_sync_mode": "append" if chosen == "incremental" else "overwrite",
    }
    if chosen == "incremental" and cursor:
        configured["cursor_field"] = list(cursor)
    primary_key = stream.get("source_defined_primary_key")
    if primary_key:
        configured["primary_key"] = primary_key
    return configured, note
