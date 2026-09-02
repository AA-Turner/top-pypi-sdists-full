"""Tests for EpicTreeValidationError dataclass."""

from agentic_devtools.epic_tree.errors import EpicTreeValidationError


class TestEpicTreeValidationError:
    """Tests for the EpicTreeValidationError dataclass."""

    def test_create_with_all_fields(self):
        """Error can be created with all fields including property_name."""
        error = EpicTreeValidationError(
            path="/features/0",
            message="'ref' is a required property",
            keyword="required",
            property_name="ref",
        )
        assert error.path == "/features/0"
        assert error.message == "'ref' is a required property"
        assert error.keyword == "required"
        assert error.property_name == "ref"

    def test_create_without_property_name(self):
        """Error can be created without property_name (defaults to None)."""
        error = EpicTreeValidationError(
            path="",
            message="Some error",
            keyword="type",
        )
        assert error.property_name is None

    def test_frozen_dataclass(self):
        """EpicTreeValidationError is immutable."""
        error = EpicTreeValidationError(
            path="/features/0",
            message="test",
            keyword="required",
        )
        try:
            error.path = "/other"  # type: ignore[misc]
            raise AssertionError("Should have raised FrozenInstanceError")
        except AttributeError:
            pass

    def test_equality(self):
        """Two errors with identical fields are equal."""
        e1 = EpicTreeValidationError(path="/a", message="m", keyword="k", property_name="p")
        e2 = EpicTreeValidationError(path="/a", message="m", keyword="k", property_name="p")
        assert e1 == e2

    def test_inequality(self):
        """Two errors with different fields are not equal."""
        e1 = EpicTreeValidationError(path="/a", message="m", keyword="k")
        e2 = EpicTreeValidationError(path="/b", message="m", keyword="k")
        assert e1 != e2
