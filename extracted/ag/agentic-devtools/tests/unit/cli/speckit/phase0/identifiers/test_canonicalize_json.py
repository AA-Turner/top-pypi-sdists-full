"""Tests for canonicalize_json in speckit/phase0/identifiers.py."""

from __future__ import annotations

import math

import pytest

from agentic_devtools.cli.speckit.phase0.identifiers import canonicalize_json


class TestCanonicalizeJson:
    """Tests for the canonicalize_json function."""

    def test_sorts_object_keys(self) -> None:
        assert canonicalize_json({"b": 1, "a": 2}) == b'{"a":2,"b":1}'

    def test_preserves_array_order(self) -> None:
        assert canonicalize_json([3, 1, 2]) == b"[3,1,2]"

    def test_no_insignificant_whitespace(self) -> None:
        result = canonicalize_json({"a": [1, 2], "b": "x"})
        assert b" " not in result

    def test_nested_structures_are_sorted_recursively(self) -> None:
        payload = {"outer": {"z": 1, "a": {"y": 2, "x": 3}}}
        assert canonicalize_json(payload) == b'{"outer":{"a":{"x":3,"y":2},"z":1}}'

    def test_is_deterministic(self) -> None:
        assert canonicalize_json({"a": 1, "b": 2}) == canonicalize_json({"b": 2, "a": 1})

    def test_supports_scalars(self) -> None:
        assert canonicalize_json(None) == b"null"
        assert canonicalize_json(True) == b"true"
        assert canonicalize_json(False) == b"false"
        assert canonicalize_json(1.5) == b"1.5"
        assert canonicalize_json("text") == b'"text"'

    def test_rejects_non_finite_float(self) -> None:
        with pytest.raises(TypeError):
            canonicalize_json(math.nan)

    def test_rejects_non_string_keys(self) -> None:
        with pytest.raises(TypeError):
            canonicalize_json({1: "a"})  # type: ignore[dict-item]

    def test_rejects_unsupported_value_types(self) -> None:
        with pytest.raises(TypeError):
            canonicalize_json({"a", "b"})  # a set is not JSON-compatible

    def test_rejects_lone_surrogate_string_values(self) -> None:
        with pytest.raises(TypeError, match="UTF-8 encodable strings"):
            canonicalize_json("\ud800")

    def test_rejects_lone_surrogate_object_member_names(self) -> None:
        with pytest.raises(TypeError, match="UTF-8 encodable object member names"):
            canonicalize_json({"\ud800": "value"})

    # RFC 8785 §3.2.2 number normalization
    def test_negative_zero_serializes_as_zero(self) -> None:
        # JCS requires -0.0 → "0", not "-0.0"
        assert canonicalize_json(-0.0) == b"0"

    def test_positive_zero_serializes_as_zero(self) -> None:
        assert canonicalize_json(0.0) == b"0"

    def test_small_float_exponent_uses_minimal_digits(self) -> None:
        # Python emits "1e-07"; JCS requires "1e-7"
        result = canonicalize_json(1e-7)
        assert result == b"1e-7"

    def test_large_float_decimal_notation_below_1e21(self) -> None:
        # RFC 8785 / ECMAScript: k ≤ n ≤ 21 uses decimal form, not exponential.
        # 1e20 → "100000000000000000000" (21 digits, all zeros after 1).
        assert canonicalize_json(1e20) == b"100000000000000000000"

    def test_large_float_exponential_notation_at_1e21(self) -> None:
        # n = 22 > 21, so exponential form is required.
        assert canonicalize_json(1e21) == b"1e+21"

    def test_small_float_decimal_notation_at_boundary(self) -> None:
        # -6 < n ≤ 0: 1e-6 (n = -5) uses "0.000001", not exponential.
        assert canonicalize_json(1e-6) == b"0.000001"

    def test_integer_zero_unchanged(self) -> None:
        assert canonicalize_json(0) == b"0"

    def test_negative_float_serializes_with_sign(self) -> None:
        # Negative values must carry their sign through _jcs_float.
        assert canonicalize_json(-1.5) == b"-1.5"

    def test_negative_float_large_decimal_form(self) -> None:
        # Negative large value in the k ≤ n ≤ 21 range.
        assert canonicalize_json(-1e20) == b"-100000000000000000000"

    def test_fixed_form_fraction_below_point_one(self) -> None:
        # 0.001 → int_part="0" → exercises the leading-zeros path in _jcs_float.
        assert canonicalize_json(0.001) == b"0.001"

    def test_large_integer_uses_jcs_exponential_notation(self) -> None:
        # int 10**21 must follow ECMAScript §7.1.12.1 just like float 1e21.
        assert canonicalize_json(10**21) == b"1e+21"

    def test_rejects_integer_not_exactly_representable_as_ieee754(self) -> None:
        # 10**21 + 1 cannot be distinguished from 10**21 as a float, so it
        # must be rejected rather than silently losing precision.
        with pytest.raises(TypeError, match="IEEE-754"):
            canonicalize_json(10**21 + 1)
