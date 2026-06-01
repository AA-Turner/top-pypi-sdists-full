"""Tests for PathValue dict wrapper."""

import pytest

from csrd.context._models import PathValue


class TestPathValue:
    def test_dict_access(self):
        pv = PathValue({"user_id": "123", "org": "acme"})
        assert pv["user_id"] == "123"

    def test_dot_notation(self):
        pv = PathValue({"user_id": "123"})
        assert pv.user_id == "123"

    def test_dot_notation_missing_raises_attribute_error(self):
        pv = PathValue()
        with pytest.raises(AttributeError, match="no key"):
            _ = pv.missing_key

    def test_set_via_dot_notation(self):
        pv = PathValue()
        pv.name = "Alice"
        assert pv["name"] == "Alice"

    def test_del_via_dot_notation(self):
        pv = PathValue({"key": "val"})
        del pv.key
        assert "key" not in pv

    def test_del_missing_raises(self):
        pv = PathValue()
        with pytest.raises(AttributeError):
            del pv.nope

    def test_dunder_attrs_use_regular_path(self):
        pv = PathValue()
        with pytest.raises(AttributeError):
            _ = pv.__nonexistent__

    def test_empty_defaults(self):
        pv = PathValue()
        assert len(pv) == 0
        assert dict(pv) == {}
