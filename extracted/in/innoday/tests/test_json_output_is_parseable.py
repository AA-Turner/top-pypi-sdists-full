"""`--format json` has to survive `json.loads`. It did not.

Three different ways, all of them rich:

* **`Syntax(...)`** in the shared formatter pads every line out to the console
  width and hard-wraps anything longer. Broken always.
* **`Console.print(json.dumps(...))`** in three commands is the worst of them:
  printing a *string* applies rich's markup parsing as well as word-wrap, so a
  value containing something like `[bold]` has it **silently deleted**. Wrong
  data, no error.
* **`Console.print_json(...)`** in eight commands breaks only when the console
  is a terminal -- which includes any run with `FORCE_COLOR` set, and Claude
  Code exports `FORCE_COLOR=3`. Piped to a file it happens to be fine, which is
  exactly why this survived so long: it looked correct in CI and failed for a
  person.

The output looked right in a terminal and was not JSON: parsing raised
`Invalid control character`, and the only way to get a clean stream was for the
caller to guess a console width wide enough that nothing wrapped. A contract
that holds only at 100,000 columns is not a contract.

These tests read the bytes the way a script would: narrow terminal, colour on,
then parse.
"""

from __future__ import annotations

import json

import pytest

from src.cli.utils.formatters import OutputFormatter

WIDE_ENOUGH_TO_WRAP = "x" * 300


@pytest.fixture(autouse=True)
def narrow_terminal(monkeypatch):
    """The condition the bug needed. 80 columns is also the default when piped."""
    monkeypatch.setenv("COLUMNS", "80")
    monkeypatch.setenv("LINES", "24")


def _emitted(capsys):
    """Only stdout, parsed. Anything on stderr is a person's business."""
    return json.loads(capsys.readouterr().out)


class TestItParses:
    @pytest.mark.parametrize("color", [True, False])
    def test_a_long_value_is_not_wrapped_into_invalid_json(self, capsys, color):
        """Colour was the trigger: it chose the rich path over a plain print."""
        formatter = OutputFormatter("json", color_enabled=color)
        formatter.format_ticket({"id": 1, "summary": WIDE_ENOUGH_TO_WRAP})
        assert _emitted(capsys)["summary"] == WIDE_ENOUGH_TO_WRAP

    def test_a_list_of_tickets_parses(self, capsys):
        formatter = OutputFormatter("json", color_enabled=True)
        formatter.format_tickets(
            [{"id": n, "summary": WIDE_ENOUGH_TO_WRAP} for n in range(3)]
        )
        assert [t["id"] for t in _emitted(capsys)] == [0, 1, 2]

    def test_the_bytes_are_exactly_json_dumps(self, capsys):
        """Byte-for-byte, not merely parseable.

        Replaces an earlier assertion that no ANSI escape reached stdout, which
        could not fail: `tests/conftest.py` sets `NO_COLOR=1` and `TERM=dumb`
        before anything is imported, so `color_enabled=True` produced no colour
        even on the broken code. Comparing against `json.dumps` catches padding,
        wrapping, markup stripping and colour in one assertion, and none of them
        depend on how the test environment feels about terminals.
        """
        payload = {"id": 1, "note": "see [bold] docs", "long": WIDE_ENOUGH_TO_WRAP}
        OutputFormatter("json", color_enabled=True).format_ticket(payload)
        assert capsys.readouterr().out == json.dumps(payload, indent=2) + "\n"

    def test_markup_in_a_value_is_not_eaten(self, capsys):
        """The silent half of the bug, and the dangerous one.

        `Console.print` on a string parses rich markup, so `[bold]` inside a
        value simply vanished. The document still parsed; it just no longer said
        what the server said.
        """
        OutputFormatter("json", color_enabled=True).format_ticket(
            {"note": "see [bold] docs"}
        )
        assert _emitted(capsys)["note"] == "see [bold] docs"


class TestAnEmptyAnswerIsStillJson:
    """`[]`, not prose. A caller parsing this crashed on "No tickets found"."""

    def test_no_tickets_emits_an_empty_array(self, capsys):
        OutputFormatter("json", color_enabled=True).format_tickets([])
        assert _emitted(capsys) == []

    def test_no_comments_emits_an_empty_array(self, capsys):
        OutputFormatter("json", color_enabled=True).format_comments([])
        assert _emitted(capsys) == []

    def test_a_table_still_says_it_in_words(self, capsys):
        """The human path is unchanged -- prose is right when a person is reading."""
        OutputFormatter("table", color_enabled=False).format_tickets([])
        assert "No tickets found" in capsys.readouterr().out


class TestEveryEmptyListSaysSoInJson:
    """Two of roughly six places were fixed the first time.

    `orgs list` and `projects list` are run by the check and register-project
    skills with `--format json`, so a fresh account -- exactly the case those
    skills exist for -- returned prose and crashed them.
    """

    def test_no_organizations_emits_an_empty_array(self, capsys):
        OutputFormatter("json", color_enabled=True).format_organizations([])
        assert _emitted(capsys) == []

    def test_no_projects_emits_an_empty_array(self, capsys):
        OutputFormatter("json", color_enabled=True).format_projects([])
        assert _emitted(capsys) == []


class TestAdvisoriesStayOffStdout:
    def test_the_advisory_console_writes_to_stderr(self, capsys):
        """A scope note printed to stdout lands immediately before the JSON.

        This is the other half of the same break: even with the payload fixed, a
        line of prose in front of it makes the stream unparseable.
        """
        from src.cli.utils.formatters import advisory_console

        advisory_console.print("scoped to something")
        captured = capsys.readouterr()
        assert captured.out == ""
        assert "scoped to something" in captured.err


class TestNothingRendersJsonThroughRich:
    """A source gate, because reviewing this by eye already failed once.

    Five call sites were fixed by hand and three more in `releases.py` were
    missed -- the grep that found them had been truncated by `head`. Every one
    of them was on a `--format json` path, so each was a silently unparseable
    payload. An inventory kept by a person is exactly the thing that goes stale;
    this one is kept by the test run.
    """

    def test_no_cli_module_calls_print_json_or_syntax(self):
        import pathlib
        import re

        cli = pathlib.Path(__file__).resolve().parents[1] / "src" / "cli"
        offenders = []
        for path in sorted(cli.rglob("*.py")):
            for lineno, line in enumerate(path.read_text().splitlines(), 1):
                if re.search(r"\bprint_json\s*\(", line) and "_print_json" not in line:
                    offenders.append(f"{path.name}:{lineno} print_json")
                if re.search(r"\bSyntax\s*\(", line):
                    offenders.append(f"{path.name}:{lineno} Syntax")
                # The pattern the first version of this gate missed entirely:
                # three sites passed `json.dumps(...)` straight to
                # `Console.print`, which is worse than `print_json` because it
                # also strips markup out of the values.
                if re.search(r"\.print\(\s*_?json\.dumps", line):
                    offenders.append(f"{path.name}:{lineno} Console.print(json.dumps)")
        assert not offenders, (
            "rich renders JSON padded to the console width and wraps long lines, "
            "which is not JSON. Use `print(json.dumps(...))`. Offenders: "
            + ", ".join(offenders)
        )


class TestTheSpinnerStopsBeforeAnythingIsPrinted:
    """A spinner that spans a whole command has to be put away before output.

    It now starts before the first network call — three round trips used to run
    ahead of it in silence, which reads as a command that did not launch. That
    fix only works if it also stops before the report and the confirmation
    prompt, so `stop()` is explicit and has to survive the `with` block exiting
    on top of it.
    """

    def test_stop_is_safe_to_call_twice(self):
        from src.cli.utils.formatters import ProgressReporter

        reporter = ProgressReporter("working")
        with reporter:
            reporter.stop()
            reporter.stop()

    def test_update_after_stop_does_not_raise(self):
        """The caller holds one reporter across several stages and may not know
        which of them the spinner outlived."""
        from src.cli.utils.formatters import ProgressReporter

        reporter = ProgressReporter("working")
        with reporter:
            reporter.stop()
            reporter.update("later stage")
