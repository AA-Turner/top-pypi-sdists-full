"""Tests for derive_operation_id_from_delivery in speckit/phase0/identifiers.py (FR-001)."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.speckit.phase0.identifiers import derive_operation_id_from_delivery


class TestDeriveOperationIdFromDelivery:
    """Tests for the derive_operation_id_from_delivery function."""

    def test_valid_delivery_id(self) -> None:
        assert derive_operation_id_from_delivery("abc-123") == "gh-event:abc-123"

    def test_uuid_style_delivery_id(self) -> None:
        delivery_id = "72d3162e-cc78-11e3-81ab-4c9367dc0958"
        assert derive_operation_id_from_delivery(delivery_id) == f"gh-event:{delivery_id}"

    def test_rejects_empty_delivery_id(self) -> None:
        with pytest.raises(ValueError):
            derive_operation_id_from_delivery("")

    def test_rejects_non_string_delivery_id(self) -> None:
        with pytest.raises(ValueError):
            derive_operation_id_from_delivery(123)  # type: ignore[arg-type]

    def test_rejects_delivery_id_with_disallowed_characters(self) -> None:
        with pytest.raises(ValueError):
            derive_operation_id_from_delivery("has space")
