"""Tests for omit_none_values helper."""

from agentic_devtools.orchestration.llm.base_provider import omit_none_values


class TestOmitNoneValues:
    """Tests for omit_none_values."""

    def test_removes_only_none_values(self):
        values = {"temperature": None, "max_tokens": 100, "stream": False}

        assert omit_none_values(values) == {"max_tokens": 100, "stream": False}

    def test_returns_new_dict(self):
        values = {"response_format": {"type": "json_object"}}

        result = omit_none_values(values)

        assert result == values
        assert result is not values
