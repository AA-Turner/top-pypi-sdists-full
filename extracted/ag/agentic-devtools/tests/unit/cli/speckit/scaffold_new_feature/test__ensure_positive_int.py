"""Tests for ``_ensure_positive_int``."""

import argparse

import pytest

from agentic_devtools.cli.speckit.scaffold_new_feature import _ensure_positive_int


def test_ensure_positive_int_rejects_non_positive_values() -> None:
    with pytest.raises(argparse.ArgumentTypeError):
        _ensure_positive_int("0")
    with pytest.raises(argparse.ArgumentTypeError):
        _ensure_positive_int("abc")


@pytest.mark.parametrize("value", ["+1", "01", "1_000"])
def test_ensure_positive_int_rejects_non_legacy_tokens(value: str) -> None:
    with pytest.raises(argparse.ArgumentTypeError):
        _ensure_positive_int(value)
