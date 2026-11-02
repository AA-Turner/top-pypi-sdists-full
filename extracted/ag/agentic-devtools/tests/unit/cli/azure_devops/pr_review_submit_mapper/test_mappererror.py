"""Tests for the MapperError class."""

from agentic_devtools.cli.azure_devops.pr_review_submit_mapper import MapperError


class TestMapperError:
    def test_is_value_error_subclass(self):
        assert issubclass(MapperError, ValueError)

    def test_carries_message(self):
        err = MapperError("boom")
        assert str(err) == "boom"
