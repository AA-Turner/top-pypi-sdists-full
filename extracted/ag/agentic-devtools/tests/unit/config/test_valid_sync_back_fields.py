"""Tests for VALID_SYNC_BACK_FIELDS constant in agentic_devtools.config."""

from agentic_devtools.config import _VALID_SYNC_BACK_FIELDS_SET, VALID_SYNC_BACK_FIELDS


class TestValidSyncBackFields:
    """Tests for the VALID_SYNC_BACK_FIELDS constant."""

    def test_is_tuple(self):
        """VALID_SYNC_BACK_FIELDS is a tuple (immutable, ordered)."""
        assert isinstance(VALID_SYNC_BACK_FIELDS, tuple)

    def test_canonical_order(self):
        """Fields are in canonical order: comment, label, status."""
        assert VALID_SYNC_BACK_FIELDS == ("comment", "label", "status")

    def test_importable_from_config(self):
        """Constant is importable from agentic_devtools.config."""
        from agentic_devtools.config import VALID_SYNC_BACK_FIELDS as imported

        assert imported is VALID_SYNC_BACK_FIELDS

    def test_frozenset_companion_matches(self):
        """The _VALID_SYNC_BACK_FIELDS_SET frozenset matches the tuple contents."""
        assert isinstance(_VALID_SYNC_BACK_FIELDS_SET, frozenset)
        assert _VALID_SYNC_BACK_FIELDS_SET == frozenset(VALID_SYNC_BACK_FIELDS)
