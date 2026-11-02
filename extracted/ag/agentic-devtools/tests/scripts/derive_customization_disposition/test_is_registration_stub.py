"""Tests for is_registration_stub in derive_customization_disposition."""

from __future__ import annotations

from tests.scripts.derive_customization_disposition import derive


def test_pointer_with_empty_body_is_a_stub() -> None:
    """A stub exists only to register a name."""
    assert derive.is_registration_stub("\nagent: agdt.x\n", "\n") is True


def test_pointer_with_a_body_is_not_a_stub() -> None:
    """A prompt carrying its own body is substantive, pointer or not."""
    assert derive.is_registration_stub("\nagent: agdt.x\n", "\n# Title\n") is False


def test_no_pointer_is_not_a_stub() -> None:
    """An empty file without an ``agent:`` pointer registers nothing."""
    assert derive.is_registration_stub("\ndescription: x\n", "") is False
