"""Tests for UserDeclinedRepairError."""

from agentic_devtools.cli.setup.doctor_repair import UserDeclinedRepairError


class TestUserDeclinedRepairError:
    """Tests for UserDeclinedRepairError exception class."""

    def test_is_exception(self) -> None:
        exc = UserDeclinedRepairError("test")
        assert isinstance(exc, Exception)

    def test_explicit_decline_message(self) -> None:
        exc = UserDeclinedRepairError("User declined destructive repair")
        assert str(exc) == "User declined destructive repair"

    def test_non_interactive_message(self) -> None:
        exc = UserDeclinedRepairError("Non-interactive environment (no TTY) — cannot confirm destructive repair")
        assert "Non-interactive" in str(exc)
        assert "no TTY" in str(exc)

    def test_distinct_messages(self) -> None:
        user_msg = "User declined destructive repair"
        tty_msg = "Non-interactive environment (no TTY) — cannot confirm destructive repair"
        assert user_msg != tty_msg
