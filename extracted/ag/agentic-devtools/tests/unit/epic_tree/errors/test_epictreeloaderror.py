"""Tests for EpicTreeLoadError exception."""

from agentic_devtools.epic_tree.errors import EpicTreeLoadError, EpicTreeValidationError


class TestEpicTreeLoadError:
    """Tests for the EpicTreeLoadError exception class."""

    def test_errors_property_returns_tuple(self):
        """errors property returns a tuple of EpicTreeValidationError."""
        errs = [
            EpicTreeValidationError(path="/ref", message="required", keyword="required"),
            EpicTreeValidationError(path="/title", message="required", keyword="required"),
        ]
        exc = EpicTreeLoadError(errs)
        assert isinstance(exc.errors, tuple)
        assert len(exc.errors) == 2
        assert exc.errors[0].path == "/ref"
        assert exc.errors[1].path == "/title"

    def test_inherits_from_exception(self):
        """EpicTreeLoadError inherits from Exception, not ValueError."""
        exc = EpicTreeLoadError([])
        assert isinstance(exc, Exception)
        assert not isinstance(exc, ValueError)

    def test_str_with_le_5_errors_shows_all(self):
        """__str__ shows all errors when count <= 5."""
        errs = [EpicTreeValidationError(path=f"/field{i}", message=f"error {i}", keyword="required") for i in range(3)]
        exc = EpicTreeLoadError(errs)
        s = str(exc)
        assert "3 validation error(s)" in s
        assert "/field0" in s
        assert "/field1" in s
        assert "/field2" in s
        assert "... and" not in s

    def test_str_with_gt_5_errors_truncates(self):
        """__str__ truncates to 5 errors and shows count of remaining."""
        errs = [EpicTreeValidationError(path=f"/field{i}", message=f"error {i}", keyword="required") for i in range(8)]
        exc = EpicTreeLoadError(errs)
        s = str(exc)
        assert "8 validation error(s)" in s
        assert "/field4" in s  # 5th error shown
        assert "/field5" not in s  # 6th error not shown
        assert "... and 3 more" in s

    def test_empty_errors_tuple(self):
        """EpicTreeLoadError can be constructed with empty errors list."""
        exc = EpicTreeLoadError([])
        assert exc.errors == ()
        assert "0 validation error(s)" in str(exc)
