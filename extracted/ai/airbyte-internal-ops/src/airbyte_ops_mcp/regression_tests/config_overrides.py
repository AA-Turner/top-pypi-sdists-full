# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Catalog overrides for regression tests.

This module provides functions for filtering catalog streams to control
the data volume during regression test reads. This is particularly
useful for connectors with large numbers of streams that would
otherwise cause timeouts.

See: https://github.com/airbytehq/airbyte-internal-issues/issues/15844
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

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
