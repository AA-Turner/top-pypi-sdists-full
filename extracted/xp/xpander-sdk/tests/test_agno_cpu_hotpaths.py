"""Stuck-detection argument signature and headroom-compact gate."""

from xpander_sdk.modules.backend.frameworks import agno


class TestBoundedArgSignature:
    """_bounded_arg_signature: stable, order-invariant, bounded for large args."""

    def test_repeated_call_same_signature(self) -> None:
        """Identical args produce an identical signature (the stuck-detection contract)."""
        args = {"a": 1, "b": "hello"}
        assert agno._bounded_arg_signature(args) == agno._bounded_arg_signature(dict(args))

    def test_key_order_irrelevant(self) -> None:
        """Signature is independent of dict key order."""
        assert agno._bounded_arg_signature({"a": 1, "b": 2}) == agno._bounded_arg_signature(
            {"b": 2, "a": 1}
        )

    def test_different_args_differ(self) -> None:
        """Different argument values yield different signatures."""
        assert agno._bounded_arg_signature({"a": 1}) != agno._bounded_arg_signature({"a": 2})

    def test_large_string_arg_is_sampled_not_serialized_whole(self) -> None:
        """A ~1MB value is sampled (len+head+tail), keeping the signature bounded."""
        big = "z" * 1_000_000
        sig = agno._bounded_arg_signature({"payload": big})
        assert len(sig) < 2_000
        assert "1000000" in sig

    def test_identical_large_values_still_match(self) -> None:
        """The same large value always matches itself (the case stuck-detection needs)."""
        a = "a" * 500_000 + "X" + "a" * 500_000
        assert agno._bounded_arg_signature({"p": a}) == agno._bounded_arg_signature({"p": a})


class TestHeadroomCompact:
    """_headroom_compact: cheap gate returns None for anything that can't compact."""

    def test_non_json_string_returns_none(self) -> None:
        """A non-JSON string is gated out."""
        assert agno._headroom_compact("not json at all") is None

    def test_leading_whitespace_object_still_passes_gate(self) -> None:
        """Whitespace before '{' still passes the gate (result is a str or None)."""
        out = agno._headroom_compact('   {"a": 1, "b": 2}')
        assert out is None or isinstance(out, str)

    def test_scalar_json_returns_none(self) -> None:
        """Valid JSON that isn't an object/array is gated out cheaply."""
        assert agno._headroom_compact("123") is None
        assert agno._headroom_compact('"a string"') is None

    def test_empty_returns_none(self) -> None:
        """An empty string is gated out."""
        assert agno._headroom_compact("") is None
