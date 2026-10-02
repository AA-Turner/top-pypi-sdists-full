"""Exercise the real review layout and key bindings without a server or agent."""

import asyncio
from contextlib import nullcontext

import pytest
from prompt_toolkit.application import create_app_session
from prompt_toolkit.data_structures import Size
from prompt_toolkit.input import create_pipe_input
from prompt_toolkit.output import DummyOutput

from probe.cli import tui

# Every test here drives a prompt_toolkit app session and asserts on the frames
# it rendered. That is a finished-render measurement, so it belongs in the serial
# lane with the pty tests -- see the `tui` marker in agent/pyproject.toml.
pytestmark = pytest.mark.tui


def _run(
    monkeypatch, keys, *, lines=None, choices=None, width=80, height=24, text=False,
    onboarding=None, render=None, invalidate_changes=True,
):
    class Output(DummyOutput):
        def get_size(self):
            return Size(rows=height, columns=width)

    monkeypatch.setattr(tui, "interactive", lambda: True)
    monkeypatch.setattr(tui, "columns", lambda: width)
    monkeypatch.setattr(tui, "rows", lambda: height)
    frames = []
    ask = tui.ask

    with (
        create_pipe_input() as pipe,
        create_app_session(input=pipe, output=Output()),
        tui.onboarding(onboarding) if onboarding is not None else nullcontext(),
    ):
        def run(question, **kwargs):
            app = question.application

            def snapshot():
                screen = app.renderer._last_screen
                return [
                    "".join(screen.data_buffer[y][x].char for x in range(width)).rstrip()
                    for y in range(height)
                ]

            async def drawn(previous):
                """The next frame the app actually draws, not whatever is there.

                This used to be `sleep(0.03)` and read `_last_screen` -- a fixed
                wait standing in for "the render finished". When the box is busy
                the render has not finished in 30ms, so the capture is the frame
                BEFORE the key, and the test fails asserting that a page-down
                changed the view. It reads as a bug in whatever else was in that
                commit, which is how it keeps costing someone an afternoon.

                So wait for the frame to CHANGE. A key that legitimately redraws
                nothing falls through the deadline and returns what is there,
                which is what the fixed sleep did on its good days.
                """
                loop = asyncio.get_running_loop()
                deadline = loop.time() + 2.0
                while loop.time() < deadline:
                    await asyncio.sleep(0.01)
                    current = snapshot()
                    if current != previous:
                        return current
                return snapshot()

            async def drive():
                previous = None
                for key in keys:
                    if callable(key):
                        key()
                        if invalidate_changes:
                            app.invalidate()
                    previous = await drawn(previous)
                    frames.append(previous)
                    if not callable(key):
                        pipe.send_text(key)
                await asyncio.sleep(app.ttimeoutlen + 0.1)
                if not app.is_done:
                    app.exit(exception=AssertionError("review did not handle the final key"))

            app.pre_run_callables.append(lambda: app.create_background_task(drive()))
            return ask(question, **kwargs)

        monkeypatch.setattr(tui, "ask", run)
        if render is not None:
            answer = render()
        elif text:
            answer = tui.text("Change the plan", ["Escape returns to the plan."], "What should change?")
        else:
            answer = tui.review(
                "Review the import plan", lines or [f"File {n:03d}" for n in range(100)],
                choices or [("Import files", "import"), ("Change the plan", "revise"), ("Cancel import", "cancel")],
            )
    return answer, frames


def _row(frame, text):
    return next(index for index, line in enumerate(frame) if text in line)


def test_enter_in_document_returns_to_actions_without_approving(monkeypatch):
    answer, _ = _run(monkeypatch, ["\t", "\x1b[B", "\r", "\x1b[B", "\r"])
    assert answer == "revise"


@pytest.mark.parametrize("key,expected", [("\x1b", tui.BACK), ("\x03", None)])
def test_cancellation_is_distinct_from_approval(monkeypatch, key, expected):
    answer, _ = _run(monkeypatch, [key])
    assert answer is expected


@pytest.mark.parametrize("keys,expected", [
    (["\r"], False),
    (["\x1b[B", "\r"], True),
    (["\x1b"], tui.BACK),
    (["\x03"], None),
])
def test_account_switch_requires_an_explicit_choice_in_the_shared_frame(monkeypatch, keys, expected):
    from probe.cli import setup

    answer, frames = _run(
        monkeypatch, keys,
        render=lambda: setup.run_confirm_account_switch("previous.researcher@example.test"),
    )
    assert answer is expected
    screen = "\n".join(frames[0])
    assert "previous.researcher@example.test" in screen
    assert "the account saved here and releases this device" in screen
    assert "Keep current account" in screen
    assert "Continue with website code" in screen
    assert _row(frames[0], "This device is already signed in.") == 3


def test_review_cannot_approve_from_a_pipe(monkeypatch, capsys):
    monkeypatch.setattr(tui, "interactive", lambda: False)
    assert tui.review("Review", ["A proposal"], [("Import", True)]) is None
    assert tui.text("Change", [], "Correction?") is None
    assert "A proposal" in capsys.readouterr().out
