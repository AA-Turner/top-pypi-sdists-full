"""Shared analyzer-result guards for Appium query helpers."""

_NOT_VISIBLE = "__not_visible__"


def is_not_visible(value) -> bool:
    """Whether the analyzer explicitly abstained instead of returning a value."""
    return isinstance(value, str) and value.strip().lower() == _NOT_VISIBLE
