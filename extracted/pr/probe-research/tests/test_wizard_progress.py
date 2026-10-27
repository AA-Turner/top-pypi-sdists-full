"""An install or an Update shows ONE bar with its percentage for the whole run.

The install's bar started again from empty on every coding agent's screen and
never said which agent it was on; the long wait (every agent's marketplace
refresh and installs, inside the first agent's refresh step) sat still. An
Update was a spinner with no idea of how far along it was.
"""

from __future__ import annotations

import importlib
import threading

from probe.cli import claude_cli, tui, upgrading
from probe.cli import setup as wizard
from probe.cli.capabilities import Capability

from tests.test_parallel_install_update import one_update  # noqa: F401 - fixture

main = importlib.import_module("probe.cli.main")


def test_the_percentage_reads_100_only_when_done():
    assert [tui.percent(f) for f in (0, 0.5, 0.999, 1)] == ["0%", "50%", "99%", "100%"]
    assert tui.progress_line(0.5).endswith("  50%")


class _Status:
    def __init__(self):
        self.seen: list[tuple[str, float]] = []
        self.label, self.fraction = "", None

    def set(self, *, label=None, fraction=None):
        self.label = label or self.label
        self.fraction = fraction if fraction is not None else self.fraction
        self.seen.append((self.label, self.fraction))


def test_a_working_line_inside_another_keeps_the_outer_one(monkeypatch):
    monkeypatch.setattr(tui, "interactive", lambda: True)
    monkeypatch.setattr(threading, "Thread", lambda **k: (_ for _ in ()).throw(RuntimeError("no threads")))
    monkeypatch.setattr(tui, "sys", type("S", (), {"stdout": __import__("io").StringIO()}))
    with tui.working("outer") as outer:
        outer.set(fraction=0.4)
        with tui.working("inner") as inner:
            assert inner is outer and outer.label == "outer"
        outer.set(fraction=0.2)
        assert outer.fraction == 0.4, "the bar never goes back"
    assert tui._active_status is None


def test_the_install_bar_moves_while_the_first_agent_installs_for_every_agent(monkeypatch):
    """The batch reports each agent's refresh and installs as they finish,
    from the thread that draws the screen, and the heading says whose."""
    monkeypatch.setattr(wizard, "_refresh_marketplace_now", lambda source: claude_cli.Result(ok=True))
    monkeypatch.setattr(wizard.plugin_cli, "install", lambda source, plugin_id: claude_cli.Result(ok=True))
    plan = {
        "claude_code": [(Capability.TRACKING, "probe-research"), (Capability.CAPTURE, "probe-research-tap")],
        "codex": [(Capability.TRACKING, "probe-research")],
    }
    sources = ["claude_code", "codex", "pi"]
    with wizard.marketplace_refreshes(["claude_code", "codex"], plan), wizard.install_run(sources, plan) as run:
        screen = run.for_agent("claude_code")
        headings: list[str] = []
        fractions: list[float] = []

        def render():
            heading, fraction = screen(1 / 6, 6)  # signed in, refreshing
            headings.append(heading)
            fractions.append(fraction)

        run.watch(render)
        before = screen(1 / 6, 6)[1]
        wizard.allow_batch_installs([Capability.TRACKING, Capability.CAPTURE])
        assert wizard.refresh_marketplace(source="claude_code").ok

    assert headings[0] == "Installing plugins for Claude Code and Codex"
    assert fractions == sorted(fractions) and fractions[-1] > before
    # The batch is most of the run's work: well past half once it is through.
    assert fractions[-1] > 0.5
    assert headings[-1] == "Installing for Claude Code (1 of 3)"


def test_an_install_runs_bar_reaches_100_when_every_agent_finishes():
    run = wizard.InstallRun(["claude_code", "pi"], {"claude_code": [(Capability.TRACKING, "probe-research")]})
    first, second = run.for_agent("claude_code"), run.for_agent("pi")
    assert first(0.0, 5)[1] == 0
    assert first(1.0, 5) == ("Installing for Claude Code (1 of 2)", first(1.0, 5)[1])
    halfway = second(0.5, 4)[1]
    assert 0 < halfway < 1
    assert second(1.0, 4)[1] == 1.0


def test_an_update_reports_every_part_and_ends_full(one_update):  # noqa: F811
    status = _Status()
    progress = main._UpdateProgress(["claude_code", "codex", "pi"], status)
    assert status.label == "Updating the Probe CLI" and status.fraction == 0

    with upgrading.reporting_progress(progress):
        upgrading.perform_updates(["claude_code", "codex", "pi"], base_url="https://x")

    labels = [label for label, _ in status.seen]
    assert "Updating pi's Probe package" in labels
    assert any(label.startswith("Updating the plugins for ") for label in labels)
    # CLI, pi's package and three agents' plugins: 5 of 9 before any is
    # recorded; the last is sending it all, which ends with the spinner.
    assert status.fraction == 5 / 9
    assert status.label == "Recording what is installed for Claude Code"
    for source in ("claude_code", "codex", "pi"):
        progress.recorded(source)
    assert status.fraction == 8 / 9 and status.label == "Sending the update's results to Probe"
    progress.sent()
    assert status.fraction == 1


def test_an_agent_already_set_up_still_takes_the_bar_to_100():
    """It opens no screen of its own: its turn ending counts it whole, and an
    agent listing more steps than expected never moves the bar back."""
    run = wizard.InstallRun(["claude_code", "codex"], expected={"claude_code": 2, "codex": 3})
    first = run.for_agent("claude_code")
    assert first(1.0, 9)[1] < 1  # more steps than expected, codex still to come
    shown = run.fraction()
    run.finished("claude_code")
    assert run.fraction() >= shown
    run.finished("codex")  # already set up: no screen
    assert run.fraction() == 1.0


def test_a_hook_that_raises_never_fails_the_update(one_update):  # noqa: F811
    def broken(part):
        raise RuntimeError("bar exploded")

    with upgrading.reporting_progress(broken):
        outcomes = upgrading.perform_updates(["claude_code", "codex"], base_url="https://x")
    assert all(outcome.ok for outcome in outcomes.values())


def test_a_result_with_newlines_is_measured_as_the_rows_it_draws(monkeypatch):
    """`page()` splits a line holding newlines into rows; counted as one, the
    padding above pushed the heading and percentage off a small screen."""
    monkeypatch.setattr(tui, "rows", lambda: 24)
    monkeypatch.setattr(tui, "columns", lambda: 80)
    monkeypatch.setattr(tui, "onboarding_header", lambda: None)
    progress = tui.Progress("This run will:", ["install", "rules"])
    body = progress.block() + ["What changed:", "  - " + "\n    ".join(f"line {i}" for i in range(8))]
    room = 24 - 2 * tui.safe_margin(24)
    drawn = len("\n".join(body).splitlines())
    assert progress._top(body, None) + drawn <= room
