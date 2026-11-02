"""Tests for UnresolvedRefError class."""

import pytest

from agentic_devtools.epic_tree.errors import UnresolvedRefError


class TestUnresolvedRefError:
    """Tests for the UnresolvedRefError exception class."""

    def test_inherits_from_key_error(self):
        """UnresolvedRefError is a KeyError subclass."""
        err = UnresolvedRefError(
            "msg",
            unresolved_ref="x",
            declaring_ref="y",
            direction="blocks",
        )
        assert isinstance(err, KeyError)

    def test_is_key_error_subclass(self):
        """UnresolvedRefError is a subclass of KeyError (behavior contract)."""
        assert issubclass(UnresolvedRefError, KeyError)

    def test_catchable_as_key_error(self):
        """Can be caught with except KeyError."""
        with pytest.raises(KeyError):
            raise UnresolvedRefError(
                "test message",
                unresolved_ref="bad-ref",
                declaring_ref="node-a",
                direction="blockedBy",
            )

    def test_str_returns_unquoted_message(self):
        """str(e) returns human-readable message without quotes."""
        err = UnresolvedRefError(
            "Unresolved ref 'bad-ref' in blocks of 'node-a'",
            unresolved_ref="bad-ref",
            declaring_ref="node-a",
            direction="blocks",
        )
        # KeyError normally wraps string args in quotes; we override that
        assert str(err) == "Unresolved ref 'bad-ref' in blocks of 'node-a'"
        assert not str(err).startswith('"')

    def test_error_payload_contains_required_fields(self):
        """error_payload contains all required fields."""
        err = UnresolvedRefError(
            "msg",
            unresolved_ref="missing",
            declaring_ref="node-x",
            direction="blockedBy",
        )
        payload = err.error_payload
        assert payload["unresolved_ref"] == "missing"
        assert payload["declaring_ref"] == "node-x"
        assert payload["direction"] == "blockedBy"
        assert payload["scope"] == "intra_epic_v1"
        assert payload["category"] == "unresolved_reference"

    def test_error_payload_blocks_direction(self):
        """error_payload correctly stores blocks direction."""
        err = UnresolvedRefError(
            "msg",
            unresolved_ref="target",
            declaring_ref="source",
            direction="blocks",
        )
        assert err.error_payload["direction"] == "blocks"

    def test_str_empty_args_returns_empty_string(self):
        """__str__ returns empty string when args is empty (defensive guard)."""
        err = UnresolvedRefError.__new__(UnresolvedRefError)
        # BaseException.__new__ leaves args=(); __init__ was never called
        assert str(err) == ""
