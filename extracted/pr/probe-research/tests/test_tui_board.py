"""The board that concurrent agents share.

The bug it exists for: three import units each repainting `\\r` on "the" status
line. That is not three progress indicators, it is one row with three writers --
whichever ticked last wins, the other two are invisible, and the count on screen
belongs to whichever unit happened to interrupt. On screen it read as a backfill
that kept restarting.

So the property under test is INDEPENDENCE: writing row 1 must not disturb row
0. That only holds while every row is addressed absolutely, which is what these
assert -- against the escape codes, because that is where the guarantee lives.
"""

from __future__ import annotations

import io
import threading

from probe.cli import tui


class _Screen(io.StringIO):
    """A TTY as far as the code under test can tell."""

    def isatty(self) -> bool:
        return True


# --- the between-screens spinner -------------------------------------------


def test_working_is_silent_into_a_pipe(monkeypatch, capsys):
    """`\\r` repaints into a pipe are log garbage, so a pipe gets NOTHING --
    not even a static line. Same split Progress documents."""
    monkeypatch.setattr(tui, "interactive", lambda: False)
    with tui.working("collecting"):
        pass
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_working_runs_the_body_even_if_the_spinner_cannot_start(monkeypatch):
    """No spinner beats no work: a thread that cannot start must not take the
    actual collection down with it."""

    monkeypatch.setattr(tui, "interactive", lambda: True)

    class _NoThread:
        def __init__(self, *a, **k):
            raise RuntimeError("thread limit")

    monkeypatch.setattr(threading, "Thread", _NoThread)
    ran = []
    with tui.working("collecting"):
        ran.append(True)
    assert ran == [True]


