"""Never print an empty error.

`str(exc)` is empty for a whole family of exceptions, and the CLI printed it raw
in sixteen places. A timed-out sync therefore reported:

    ✗ Unexpected error:

...with nothing after the colon, on a command that had usually **succeeded**
server-side. Diagnosing it needed `--verbose` to learn that the class name was
the entire message.
"""

import httpx
import pytest

from src.cli.utils.formatters import describe_error


class TestDescribeError:
    def test_an_exception_with_no_message_still_says_something(self):
        """The whole bug in one assertion."""
        assert describe_error(httpx.ReadTimeout("")) != ""
        assert "ReadTimeout" in describe_error(httpx.ReadTimeout(""))

    def test_a_timeout_says_the_work_may_have_finished_anyway(self):
        """The useful advice is not "it failed" but "it may not have" -- the
        request kept going after the client stopped waiting, which is exactly how
        a successful sync came to look like a failure."""
        message = describe_error(httpx.ReadTimeout(""))
        assert "timed out" in message
        assert "may have completed it anyway" in message

    def test_a_real_message_is_kept(self):
        assert "no space left" in describe_error(OSError("no space left"))

    def test_the_class_is_named_when_the_message_does_not_name_it(self):
        assert describe_error(ValueError("bad input")) == "ValueError: bad input"

    def test_the_class_is_not_repeated_when_the_message_already_has_it(self):
        """`RuntimeError: RuntimeError: ...` reads as a bug in the reporter."""
        out = describe_error(RuntimeError("RuntimeError while starting"))
        assert out.count("RuntimeError") == 1

    @pytest.mark.parametrize(
        "exc",
        [
            httpx.ConnectTimeout(""),
            httpx.WriteTimeout(""),
            httpx.PoolTimeout(""),
        ],
    )
    def test_every_timeout_flavour_is_recognised(self, exc):
        """Matched on the class name rather than by importing httpx types, so this
        keeps working for any client's equivalents -- and so the formatter needs no
        HTTP dependency."""
        assert "timed out" in describe_error(exc)

    def test_no_call_site_still_prints_a_bare_exception(self):
        """The fix is worthless if one of the sixteen was missed, and a missed one
        looks identical to a fixed one until it fires."""
        import pathlib

        cli = pathlib.Path(__file__).resolve().parent.parent / "src" / "cli"
        offenders = [
            f"{path.relative_to(cli.parent.parent)}:{n}"
            for path in cli.rglob("*.py")
            for n, line in enumerate(path.read_text().splitlines(), 1)
            if "Unexpected error:" in line
            and "describe_error" not in line
            # The helper's own docstring quotes the old output on purpose.
            and path.name != "formatters.py"
        ]
        assert not offenders, f"still printing a bare exception: {offenders}"
