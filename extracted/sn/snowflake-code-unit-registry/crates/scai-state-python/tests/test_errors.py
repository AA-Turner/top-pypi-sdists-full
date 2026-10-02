"""Error code contract integrity tests.

Validates that ScaiError carries the correct error_code attribute
across the FFI boundary for each error variant, and that the Python
ErrorCode IntEnum stays in sync with the Rust Error enum.
"""

from __future__ import annotations

import re

import pytest

from snowflake_code_unit_registry import CodeUnitRegistry, ErrorCode, list_error_codes
from snowflake_code_unit_registry._native import ScaiError


def _pascal_to_upper_snake(name: str) -> str:
    """Convert PascalCase to UPPER_SNAKE_CASE."""
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name).upper()


def test_error_propagation(registry_dir: str):
    """Verify ScaiError carries the correct error_code attribute across FFI."""

    # RegistryNotFound
    with pytest.raises(ScaiError) as exc_info:
        CodeUnitRegistry.open("/nonexistent/path/that/does/not/exist")
    assert exc_info.value.error_code == ErrorCode.REGISTRY_NOT_FOUND

    # CodeUnitNotFound
    registry = CodeUnitRegistry.init(registry_dir)
    with pytest.raises(ScaiError) as exc_info:
        registry.get_by_id("nonexistent-id")
    assert exc_info.value.error_code == ErrorCode.CODE_UNIT_NOT_FOUND


def test_error_info_on_thrown_exception(registry_dir: str):
    """Verify ScaiError carries a structured .info attribute with code, message,
    and that it round-trips correctly through the FFI boundary."""

    registry = CodeUnitRegistry.init(registry_dir)

    with pytest.raises(ScaiError) as exc_info:
        registry.get_by_id("nonexistent-id")

    info = exc_info.value.info
    assert isinstance(info, dict)
    assert info["code"] == ErrorCode.CODE_UNIT_NOT_FOUND
    assert "nonexistent-id" in info["message"]


def test_error_info_trace_is_populated(registry_dir: str):
    """Verify ErrorInfo.trace contains at least one entry with location and message."""

    registry = CodeUnitRegistry.init(registry_dir)

    with pytest.raises(ScaiError) as exc_info:
        registry.get_by_id("nonexistent-id")

    info = exc_info.value.info
    trace = info.get("trace")
    assert isinstance(trace, list)
    assert len(trace) >= 1, "trace should contain at least one entry"
    assert "nonexistent-id" in trace[0]["message"]
    assert len(trace[0]["location"]) > 0, "trace entry location should not be empty"


def test_all_rust_error_codes_have_matching_python_enum():
    """Cross-language contract: every Rust error code must have a Python ErrorCode member."""
    rust_codes = list_error_codes()
    assert len(rust_codes) > 0, "Rust returned no error codes"

    for name, code in rust_codes:
        expected_member = _pascal_to_upper_snake(name)
        assert code in ErrorCode._value2member_map_, (
            f"Rust error '{name}' (code {code}) has no matching "
            f"Python ErrorCode member (expected ErrorCode.{expected_member})"
        )
        actual_member = ErrorCode(code)
        assert actual_member.name == expected_member, (
            f"Python enum member name for code {code} is "
            f"'{actual_member.name}', expected '{expected_member}'"
        )

    assert len(ErrorCode) == len(rust_codes), (
        f"Python ErrorCode has {len(ErrorCode)} members but "
        f"Rust has {len(rust_codes)} variants — enums are out of sync"
    )
