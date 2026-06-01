# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Record obfuscation utilities for live tests.

This module provides functions for obfuscating sensitive data in Airbyte
records while preserving type and length information for schema inference.

Based on airbyte-ci implementation:
https://github.com/airbytehq/airbyte/blob/master/tools/bin/record_obfuscator.py
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

from airbyte_protocol.models import AirbyteMessage
from airbyte_protocol.models import Type as AirbyteMessageType


def _generate_hash(value: Any) -> str:
    """Generate a SHA256 hash of the value."""
    return hashlib.sha256(str(value).encode()).hexdigest()[:16]


def obfuscate_value(value: Any) -> str:
    """Obfuscate a value while retaining type and length information.

    The obfuscated value encodes:
    - The original type (string, integer, number, boolean, null, array, object)
    - The length/size of the original value
    - A hash for uniqueness (truncated for readability)

    This allows schema inference to work correctly on obfuscated data.
    """
    if isinstance(value, str):
        return f"string_len-{len(value)}_{_generate_hash(value)}"
    if isinstance(value, bool):  # Must check bool before int (bool is subclass of int)
        return f"boolean_{_generate_hash(value)}"
    if isinstance(value, int):
        return f"integer_len-{len(str(value))}_{_generate_hash(value)}"
    if isinstance(value, float):
        return f"number_len-{len(str(value))}_{_generate_hash(value)}"
    if value is None:
        return f"null_{_generate_hash(value)}"
    if isinstance(value, list):
        return f"array_len-{len(value)}_{_generate_hash(json.dumps(value, sort_keys=True))}"
    if isinstance(value, dict):
        return f"object_len-{len(value.keys())}_{_generate_hash(json.dumps(value, sort_keys=True))}"
    # Fallback for unknown types
    return f"unknown_{_generate_hash(value)}"


def obfuscate_record_data(data: dict[str, Any]) -> dict[str, str]:
    """Obfuscate all values in a record's data dictionary.

    Preserves the keys but replaces all values with obfuscated versions.
    """
    return {key: obfuscate_value(value) for key, value in data.items()}


def obfuscate_message(message: AirbyteMessage) -> AirbyteMessage:
    """Obfuscate an Airbyte message if it's a RECORD type.

    Non-RECORD messages are returned unchanged.
    RECORD messages have their data field obfuscated.
    """
    if message.type != AirbyteMessageType.RECORD:
        return message

    if not message.record or not message.record.data:
        return message

    # Create a copy with obfuscated data
    obfuscated_data = obfuscate_record_data(message.record.data)

    # Create new message with obfuscated data
    message_dict = message.dict()
    message_dict["record"]["data"] = obfuscated_data
    return AirbyteMessage.parse_obj(message_dict)


def obfuscate_messages(
    messages: list[AirbyteMessage],
) -> list[AirbyteMessage]:
    """Obfuscate a list of Airbyte messages.

    RECORD messages have their data obfuscated; other messages pass through unchanged.
    """
    return [obfuscate_message(msg) for msg in messages]


def get_type_from_obfuscated_value(obfuscated: str) -> Any:
    """Convert an obfuscated value back to a representative value of the original type.

    This is useful for schema inference on obfuscated data.

    Based on airbyte-ci implementation:
    https://github.com/airbytehq/airbyte/blob/master/airbyte-ci/connectors/live-tests/src/live_tests/commons/models.py#L369-L390
    """
    if obfuscated.startswith("string_"):
        return "a"
    if obfuscated.startswith("integer_"):
        return 0
    if obfuscated.startswith("number_"):
        return 0.1
    if obfuscated.startswith("boolean_"):
        return True
    if obfuscated.startswith("null_"):
        return None
    if obfuscated.startswith("array_"):
        return []
    if obfuscated.startswith("object_"):
        return {}
    # Unknown type, return as string
    return "unknown"


def convert_obfuscated_record_to_typed(
    obfuscated_data: dict[str, str],
) -> dict[str, Any]:
    """Convert obfuscated record data to typed values for schema inference."""
    return {
        key: get_type_from_obfuscated_value(value)
        for key, value in obfuscated_data.items()
    }
