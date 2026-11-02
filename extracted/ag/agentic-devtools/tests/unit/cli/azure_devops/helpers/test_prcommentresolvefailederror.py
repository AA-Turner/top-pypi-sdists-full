"""Tests for the PrCommentResolveFailedError exception class."""

from agentic_devtools.cli.azure_devops.helpers import PrCommentResolveFailedError


class TestPrCommentResolveFailedError:
    """Tests for PrCommentResolveFailedError's constructor/thread-ID contract."""

    def test_stores_thread_id(self) -> None:
        """The thread_id attribute is set from the constructor argument."""
        error = PrCommentResolveFailedError(thread_id=55, message="resolve failed")

        assert error.thread_id == 55

    def test_message_is_preserved(self) -> None:
        """The message argument is preserved as the exception's string representation."""
        error = PrCommentResolveFailedError(thread_id=1, message="Comment posted (thread 1) but resolving it failed")

        assert str(error) == "Comment posted (thread 1) but resolving it failed"

    def test_is_a_runtime_error(self) -> None:
        """The exception subclasses RuntimeError so untyped callers still catch it."""
        error = PrCommentResolveFailedError(thread_id=1, message="boom")

        assert isinstance(error, RuntimeError)

    def test_raises_and_is_catchable(self) -> None:
        """The exception can be raised and caught, exposing thread_id on the instance."""
        try:
            raise PrCommentResolveFailedError(thread_id=99, message="resolve failed")
        except PrCommentResolveFailedError as error:
            assert error.thread_id == 99
