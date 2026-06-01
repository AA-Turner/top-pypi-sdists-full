# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Stream schema generation utilities for live tests.

This module provides functions for inferring JSON schemas from Airbyte
record messages, useful for comparing schemas between connector versions.

Based on airbyte-ci implementation:
https://github.com/airbytehq/airbyte/blob/master/airbyte-ci/connectors/live-tests/src/live_tests/commons/models.py#L355-L366
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from airbyte_protocol.models import AirbyteMessage
from airbyte_protocol.models import Type as AirbyteMessageType
from genson import SchemaBuilder

from airbyte_ops_mcp.regression_tests.obfuscation import (
    convert_obfuscated_record_to_typed,
)

logger = logging.getLogger(__name__)


def sort_dict_keys(d: dict[str, Any]) -> dict[str, Any]:
    """Recursively sort dictionary keys for consistent output."""
    if isinstance(d, dict):
        return {k: sort_dict_keys(v) for k, v in sorted(d.items())}
    if isinstance(d, list):
        return [sort_dict_keys(item) for item in d]
    return d


def generate_schema_from_records(
    records: list[dict[str, Any]],
    obfuscated: bool = False,
) -> dict[str, Any]:
    """Generate a JSON schema from a list of record data dictionaries.

    If records are obfuscated, they are first converted to typed values
    for proper schema inference.
    """
    builder = SchemaBuilder()
    builder.add_schema({"type": "object", "properties": {}})

    for record_data in records:
        if obfuscated:
            record_data = convert_obfuscated_record_to_typed(record_data)
        builder.add_object(record_data)

    return sort_dict_keys(builder.to_schema())


def generate_stream_schemas(
    messages: list[AirbyteMessage],
    obfuscated: bool = False,
) -> dict[str, dict[str, Any]]:
    """Generate JSON schemas for each stream from Airbyte messages.

    Groups RECORD messages by stream name and infers a schema for each stream.

    Based on airbyte-ci implementation:
    https://github.com/airbytehq/airbyte/blob/master/airbyte-ci/connectors/live-tests/src/live_tests/commons/models.py#L355-L366
    """
    logger.info("Generating stream schemas")
    stream_builders: dict[str, SchemaBuilder] = {}

    for message in messages:
        if message.type != AirbyteMessageType.RECORD:
            continue
        if not message.record or not message.record.data:
            continue

        stream_name = message.record.stream
        if stream_name not in stream_builders:
            builder = SchemaBuilder()
            builder.add_schema({"type": "object", "properties": {}})
            stream_builders[stream_name] = builder

        record_data = message.record.data
        if obfuscated:
            record_data = convert_obfuscated_record_to_typed(record_data)

        stream_builders[stream_name].add_object(record_data)

    logger.info("Stream schemas generated")
    return {
        stream: sort_dict_keys(stream_builders[stream].to_schema())
        for stream in stream_builders
    }


def save_stream_schemas(
    schemas: dict[str, dict[str, Any]],
    output_dir: Path,
) -> None:
    """Save stream schemas to individual JSON files.

    Creates a directory and saves each stream's schema as a separate JSON file.

    Based on airbyte-ci implementation:
    https://github.com/airbytehq/airbyte/blob/master/airbyte-ci/connectors/live-tests/src/live_tests/commons/models.py#L456-L462
    """
    import re

    def sanitize_stream_name(stream_name: str) -> str:
        """Sanitize a stream name for use as a file name."""
        return re.sub(r"[^a-zA-Z0-9_]", "_", stream_name)

    output_dir.mkdir(parents=True, exist_ok=True)

    for stream_name, schema in schemas.items():
        file_name = f"{sanitize_stream_name(stream_name)}.json"
        file_path = output_dir / file_name
        file_path.write_text(json.dumps(schema, sort_keys=True, indent=2))

    logger.info(f"Stream schemas saved to {output_dir}")


def compare_stream_schemas(
    control_schemas: dict[str, dict[str, Any]],
    target_schemas: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Compare schemas between control and target versions.

    Returns a dictionary with differences for each stream that has schema changes.
    """
    from deepdiff import DeepDiff

    differences: dict[str, dict[str, Any]] = {}

    all_streams = set(control_schemas.keys()) | set(target_schemas.keys())

    for stream in all_streams:
        control_schema = control_schemas.get(stream, {})
        target_schema = target_schemas.get(stream, {})

        if not control_schema and target_schema:
            differences[stream] = {"status": "new_stream", "schema": target_schema}
        elif control_schema and not target_schema:
            differences[stream] = {"status": "removed_stream", "schema": control_schema}
        else:
            diff = DeepDiff(control_schema, target_schema, ignore_order=True)
            if diff:
                differences[stream] = {
                    "status": "changed",
                    "diff": diff.to_dict(),
                    "control_schema": control_schema,
                    "target_schema": target_schema,
                }

    return differences
