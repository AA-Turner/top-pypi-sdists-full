"""A blocking wait paints one centered status and leaves no stale spinner."""

import io
import threading
from types import SimpleNamespace

import pytest

from probe.cli import tui
from tests.test_setup_wizard import _Screen

pytestmark = pytest.mark.tui
_LABEL = "Checking connected agents"
_HEADER = ["Install Probe · Step 3 of 4", "━" * 30 + "─" * 10]


class _Ticks:
    """Run exactly one iteration of the real spinner loop on demand."""

    def __init__(self):
        self.remaining = 0
        self.stopped = False
        self.target = None
        self.joined = False

    def wait(self, _timeout):
        if self.stopped or not self.remaining:
            return True
        self.remaining -= 1
        return False

    def set(self):
        self.stopped = True

    def thread(self, *, target, daemon):
        assert daemon
        self.target = target
        return self

    def start(self):
        pass

    def join(self, timeout):
        self.joined = True

    def tick(self):
        assert self.target is not None and not self.stopped
        self.remaining = 1
        self.target()


@pytest.fixture
def spinner(monkeypatch):
    dimensions = [80, 24]
    output = io.StringIO()
    ticks = _Ticks()
    monkeypatch.setattr(tui, "interactive", lambda: True)
    monkeypatch.setattr(tui, "columns", lambda: dimensions[0])
    monkeypatch.setattr(tui, "rows", lambda: dimensions[1])
    # pytest replaces process stdout between fixture setup and the test call.
    # Patch this module's stream reference so both phases use the same buffer.
    monkeypatch.setattr(tui, "sys", SimpleNamespace(stdout=output))
    monkeypatch.setattr(threading, "Event", lambda: ticks)
    monkeypatch.setattr(threading, "Thread", ticks.thread)

    def screen():
        width, height = dimensions
        return _Screen(height, width).feed(output.getvalue().encode())

    return dimensions, ticks, screen


def _assert_running(screen, *, header):
    lines = screen.lines()
    text = "\n".join(lines)
    assert text.count(_LABEL) == 1, screen.dump()
    assert "Preparing…" not in text, screen.dump()
    assert screen.cursor_visible is False, screen.dump()
    margin = tui.safe_margin(screen.h)
    assert not any(lines[:margin]) and not any(lines[-margin:]), screen.dump()
    if header:
        for index, label in enumerate(_HEADER):
            assert lines[margin + index].strip() == label, screen.dump()
        assert text.count(_HEADER[0]) == 1, screen.dump()
    row = next(index for index, line in enumerate(lines) if _LABEL in line)
    first = margin + (len(_HEADER) + 1 if header else 0)
    last = screen.h - margin - 1
    assert abs(row - (first + last) / 2) <= 0.5, screen.dump()
    line = lines[row]
    left = len(line) - len(line.lstrip())
    right = screen.w - len(line)
    assert abs(left - right) <= 1, screen.dump()
    assert len([line for line in lines if line.strip()]) == (3 if header else 1), screen.dump()
    return row, line.strip()


def _assert_cleaned(screen, *, header):
    lines = screen.lines()
    assert _LABEL not in "\n".join(lines), screen.dump()
    assert screen.cursor_visible is True, screen.dump()
    assert [line.strip() for line in lines if line.strip()] == (_HEADER if header else []), screen.dump()


@pytest.mark.parametrize("failure", [RuntimeError, KeyboardInterrupt])
def test_working_erases_status_and_restores_cursor_when_work_raises(spinner, failure):
    _dimensions, ticks, screen = spinner
    with tui.onboarding(lambda: _HEADER):
        with pytest.raises(failure):
            with tui.working(_LABEL):
                ticks.tick()
                _assert_running(screen(), header=True)
                raise failure("work interrupted")
        _assert_cleaned(screen(), header=True)
    assert ticks.stopped and ticks.joined


@pytest.mark.parametrize("phase", ["start", "join"])
def test_working_restores_the_cursor_when_thread_lifecycle_is_interrupted(spinner, monkeypatch, phase):
    _dimensions, ticks, screen = spinner
    interrupted = []
    entered = []

    def interrupt(*args, **kwargs):
        _assert_running(screen(), header=True)
        interrupted.append(phase)
        raise KeyboardInterrupt("spinner lifecycle interrupted")

    monkeypatch.setattr(ticks, phase, interrupt)
    with tui.onboarding(lambda: _HEADER):
        with pytest.raises(KeyboardInterrupt):
            with tui.working(_LABEL):
                entered.append(True)
                ticks.tick()
        _assert_cleaned(screen(), header=True)
    assert interrupted == [phase]
    assert bool(entered) is (phase == "join")
    assert ticks.stopped


