# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Catalog validation functions for discovered catalogs.

Based on airbyte-ci validation tests:
https://github.com/airbytehq/airbyte/blob/master/airbyte-ci/connectors/live-tests/src/live_tests/validation_tests/test_discover.py
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import dpath.util
import jsonschema
from airbyte_protocol.models import AirbyteCatalog, AirbyteStream


@dataclass
class ValidationResult:
    """Result of a validation check."""

    passed: bool
    message: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @classmethod
    def success(cls, message: str = "Validation passed") -> ValidationResult:
        return cls(passed=True, message=message)

    @classmethod
    def failure(cls, message: str, errors: list[str] | None = None) -> ValidationResult:
        return cls(passed=False, message=message, errors=errors or [])


def validate_catalog_has_streams(catalog: AirbyteCatalog) -> ValidationResult:
    """Validate that the catalog has at least one stream.

    Args:
        catalog: The discovered catalog to validate.

    Returns:
        ValidationResult indicating success or failure.
    """
    if not catalog.streams:
        return ValidationResult.failure(
            "Catalog should contain at least one stream",
            errors=["No streams found in catalog"],
        )
    return ValidationResult.success(f"Catalog contains {len(catalog.streams)} streams")


def validate_no_duplicate_stream_names(catalog: AirbyteCatalog) -> ValidationResult:
    """Validate that all stream names in the catalog are unique.

    Args:
        catalog: The discovered catalog to validate.

    Returns:
        ValidationResult indicating success or failure.
    """
    name_counts: dict[str, int] = {}
    for stream in catalog.streams:
        count = name_counts.get(stream.name, 0)
        name_counts[stream.name] = count + 1

    duplicates = [name for name, count in name_counts.items() if count > 1]
    if duplicates:
        return ValidationResult.failure(
            f"Catalog has duplicate stream names: {duplicates}",
            errors=[f"Stream '{name}' appears multiple times" for name in duplicates],
        )
    return ValidationResult.success("All stream names are unique")


def validate_schemas_are_valid_json_schema(catalog: AirbyteCatalog) -> ValidationResult:
    """Validate that all stream schemas are valid JSON Schema Draft 7.

    Args:
        catalog: The discovered catalog to validate.

    Returns:
        ValidationResult indicating success or failure.
    """
    errors = []
    for stream in catalog.streams:
        try:
            jsonschema.Draft7Validator.check_schema(stream.json_schema)
        except jsonschema.exceptions.SchemaError as e:
            errors.append(
                f"Stream '{stream.name}' has invalid JSON schema: {e.message}"
            )

    if errors:
        return ValidationResult.failure(
            "Some streams have invalid JSON schemas",
            errors=errors,
        )
    return ValidationResult.success("All stream schemas are valid JSON Schema Draft 7")


def validate_cursors_exist_in_schema(catalog: AirbyteCatalog) -> ValidationResult:
    """Validate that all defined cursor fields exist in their stream schemas.

    Args:
        catalog: The discovered catalog to validate.

    Returns:
        ValidationResult indicating success or failure.
    """
    errors = []
    for stream in catalog.streams:
        if not stream.default_cursor_field:
            continue

        schema = stream.json_schema
        if "properties" not in schema:
            errors.append(
                f"Stream '{stream.name}' has cursor field but no 'properties' in schema"
            )
            continue

        cursor_path = "/properties/".join(stream.default_cursor_field)
        cursor_field_location = dpath.util.search(schema["properties"], cursor_path)
        if not cursor_field_location:
            errors.append(
                f"Stream '{stream.name}': cursor field {stream.default_cursor_field} "
                "not found in schema properties"
            )

    if errors:
        return ValidationResult.failure(
            "Some cursor fields are not defined in their schemas",
            errors=errors,
        )
    return ValidationResult.success("All cursor fields exist in their schemas")


def _find_all_values_for_key(
    schema: dict[str, Any] | list[Any] | Any,
    key: str,
) -> list[Any]:
    """Find all values for a given key in a nested structure.

    Args:
        schema: The schema or nested structure to search.
        key: The key to search for.

    Returns:
        List of all values found for the key.
    """
    results = []
    if isinstance(schema, dict):
        for k, v in schema.items():
            if k == key:
                results.append(v)
            results.extend(_find_all_values_for_key(v, key))
    elif isinstance(schema, list):
        for item in schema:
            results.extend(_find_all_values_for_key(item, key))
    return results


def validate_no_unresolved_refs(catalog: AirbyteCatalog) -> ValidationResult:
    """Validate that no stream schemas contain unresolved $ref values.

    Args:
        catalog: The discovered catalog to validate.

    Returns:
        ValidationResult indicating success or failure.
    """
    errors = []
    for stream in catalog.streams:
        refs = _find_all_values_for_key(stream.json_schema, "$ref")
        if refs:
            errors.append(f"Stream '{stream.name}' has unresolved $ref values: {refs}")

    if errors:
        return ValidationResult.failure(
            "Some streams have unresolved $ref values",
            errors=errors,
        )
    return ValidationResult.success("No unresolved $ref values found")


def _find_keyword_in_schema(
    schema: dict[str, Any] | list[Any] | str,
    keyword: str,
) -> bool:
    """Find if a keyword exists in a schema, skipping object properties.

    Args:
        schema: The schema to search.
        keyword: The keyword to find.

    Returns:
        True if keyword is found, False otherwise.
    """

    def _find_keyword(
        schema: dict[str, Any] | list[Any] | str,
        key: str,
        skip: bool = False,
    ) -> None:
        if isinstance(schema, list):
            for v in schema:
                _find_keyword(v, key)
        elif isinstance(schema, dict):
            for k, v in schema.items():
                if k == key and not skip:
                    raise StopIteration
                rec_skip = k == "properties" and schema.get("type") == "object"
                _find_keyword(v, key, rec_skip)

    try:
        _find_keyword(schema, keyword)
    except StopIteration:
        return True
    return False


def validate_no_disallowed_keywords(
    catalog: AirbyteCatalog,
    keywords: list[str] | None = None,
) -> ValidationResult:
    """Validate that no stream schemas contain disallowed keywords.

    Args:
        catalog: The discovered catalog to validate.
        keywords: List of disallowed keywords. Defaults to ["allOf", "not"].

    Returns:
        ValidationResult indicating success or failure.
    """
    if keywords is None:
        keywords = ["allOf", "not"]

    errors = []
    for stream in catalog.streams:
        for keyword in keywords:
            if _find_keyword_in_schema(stream.json_schema, keyword):
                errors.append(
                    f"Stream '{stream.name}' contains disallowed keyword '{keyword}'"
                )

    if errors:
        return ValidationResult.failure(
            f"Some streams contain disallowed keywords: {keywords}",
            errors=errors,
        )
    return ValidationResult.success("No disallowed keywords found in schemas")


def validate_primary_keys_exist_in_schema(catalog: AirbyteCatalog) -> ValidationResult:
    """Validate that all primary keys are present in their stream schemas.

    Args:
        catalog: The discovered catalog to validate.

    Returns:
        ValidationResult indicating success or failure.
    """
    errors = []
    for stream in catalog.streams:
        for pk in stream.source_defined_primary_key or []:
            schema = stream.json_schema
            if "properties" not in schema:
                errors.append(
                    f"Stream '{stream.name}' has primary key but no 'properties' in schema"
                )
                continue

            pk_path = "/properties/".join(pk)
            pk_field_location = dpath.util.search(schema["properties"], pk_path)
            if not pk_field_location:
                errors.append(
                    f"Stream '{stream.name}': primary key {pk} not found in schema"
                )

    if errors:
        return ValidationResult.failure(
            "Some primary keys are not defined in their schemas",
            errors=errors,
        )
    return ValidationResult.success("All primary keys exist in their schemas")


def validate_streams_have_sync_modes(catalog: AirbyteCatalog) -> ValidationResult:
    """Validate that all streams have supported_sync_modes defined.

    Args:
        catalog: The discovered catalog to validate.

    Returns:
        ValidationResult indicating success or failure.
    """
    errors = []
    for stream in catalog.streams:
        if stream.supported_sync_modes is None:
            errors.append(
                f"Stream '{stream.name}' is missing supported_sync_modes field"
            )
        elif len(stream.supported_sync_modes) == 0:
            errors.append(f"Stream '{stream.name}' has empty supported_sync_modes list")

    if errors:
        return ValidationResult.failure(
            "Some streams are missing sync mode declarations",
            errors=errors,
        )
    return ValidationResult.success("All streams have sync modes defined")


def validate_additional_properties_is_true(catalog: AirbyteCatalog) -> ValidationResult:
    """Validate that additionalProperties is always true when set.

    Setting additionalProperties to false introduces risk of breaking changes
    when removing properties from the schema.

    Args:
        catalog: The discovered catalog to validate.

    Returns:
        ValidationResult indicating success or failure.
    """
    errors = []
    for stream in catalog.streams:
        additional_props = _find_all_values_for_key(
            stream.json_schema, "additionalProperties"
        )
        for value in additional_props:
            if value is not True:
                errors.append(
                    f"Stream '{stream.name}' has additionalProperties={value}, "
                    "should be true for backward compatibility"
                )

    if errors:
        return ValidationResult.failure(
            "Some streams have additionalProperties set to false",
            errors=errors,
        )
    return ValidationResult.success(
        "All additionalProperties values are true (or not set)"
    )


def validate_stream(stream: AirbyteStream) -> list[ValidationResult]:
    """Run all validations on a single stream.

    Args:
        stream: The stream to validate.

    Returns:
        List of ValidationResult objects.
    """
    catalog = AirbyteCatalog(streams=[stream])
    return [
        validate_schemas_are_valid_json_schema(catalog),
        validate_cursors_exist_in_schema(catalog),
        validate_no_unresolved_refs(catalog),
        validate_no_disallowed_keywords(catalog),
        validate_primary_keys_exist_in_schema(catalog),
        validate_streams_have_sync_modes(catalog),
        validate_additional_properties_is_true(catalog),
    ]


def validate_catalog(catalog: AirbyteCatalog) -> list[ValidationResult]:
    """Run all catalog validations.

    Args:
        catalog: The catalog to validate.

    Returns:
        List of ValidationResult objects.
    """
    return [
        validate_catalog_has_streams(catalog),
        validate_no_duplicate_stream_names(catalog),
        validate_schemas_are_valid_json_schema(catalog),
        validate_cursors_exist_in_schema(catalog),
        validate_no_unresolved_refs(catalog),
        validate_no_disallowed_keywords(catalog),
        validate_primary_keys_exist_in_schema(catalog),
        validate_streams_have_sync_modes(catalog),
        validate_additional_properties_is_true(catalog),
    ]
