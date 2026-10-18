"""Integer-limit compatibility on supported interpreters."""

from __future__ import annotations

import runpy
import sys

import pytest

from nab_markersets import _compat
from nab_markersets.markersets import MarkerSet, _markersets


def test_missing_integer_limit_is_unlimited(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delattr(sys, "get_int_max_str_digits", raising=False)
    namespace = runpy.run_path(_compat.__file__)
    get_limit = namespace["get_int_max_str_digits"]
    assert get_limit() == 0
    monkeypatch.setattr(_markersets, "get_int_max_str_digits", get_limit)
    assert MarkerSet.from_marker('python_version >= "3.9"').evaluate(
        {"python_version": "3.11"}
    )


@pytest.mark.parametrize("limit", [0, 640])
def test_available_integer_limit_is_preserved(
    monkeypatch: pytest.MonkeyPatch, limit: int
) -> None:
    monkeypatch.setattr(sys, "get_int_max_str_digits", lambda: limit, raising=False)
    namespace = runpy.run_path(_compat.__file__)
    assert namespace["get_int_max_str_digits"]() == limit


@pytest.mark.skipif(
    _compat.get_int_max_str_digits() != 0,
    reason="requires unlimited native integer conversion",
)
def test_unlimited_interpreter_accepts_large_version_literal() -> None:
    literal = "9" * 5000
    marker = MarkerSet.from_marker(f'python_full_version < "{literal}"')
    assert marker.evaluate({"python_full_version": "3.11"})
