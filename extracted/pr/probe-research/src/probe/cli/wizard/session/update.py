"""the wizard's Update: what asked for it, its hand-off argv, and its progress bar across agents."""

from __future__ import annotations

import contextlib
import sys

import typer


def _update_action_trigger(yes: bool):
    """What asked for an Update the wizard (or `probe update`) is running.

    The plugin's SessionStart hook spawns `probe wizard --action update --yes`
    (older plugins: `probe update --yes`) with no terminal on either end, and is
    the only thing that does; a person at Update has one. A spawner that names
    itself in `TRIGGER_ENV` wins over both readings."""
    from probe.shared.updates import update_report

    unattended = yes and not (sys.stdin.isatty() and sys.stdout.isatty())
    return update_report.trigger_from_env(
        update_report.Trigger.SESSION_START if unattended else update_report.Trigger.MANUAL
    )


def _hand_off_update(trigger, argv: list[str], *, json_output: bool = False, before_exec=None) -> None:
    """An Update's first step (`probe.core.adopt.begin`), before anything else
    of it runs: with a newer release out, it is installed beside this one and
    this process becomes the new release's `probe <argv>`, which switches the
    CLI and runs the rest of the update in its own code. Returns to go on
    here; an update that must end now (its adopt waits for a quiet machine, or
    the new release cannot run it) exits with that status, said."""
    from probe.core import adopt

    ending = adopt.begin(trigger.value, argv=["-m", "probe.cli", *_root_options(), *argv], before_exec=before_exec)
    if ending is None:
        return
    if json_output:
        from probe.core import events as json_events

        json_events.done_events(
            code=json_events.ErrorCode.BUSY if ending.status == adopt.DEFERRED_EXIT else json_events.ErrorCode.FAILED,
            message=ending.message,
            exit_code=ending.status,
        )
    print(f"probe update: {ending.message}", file=sys.stderr)
    raise typer.Exit(ending.status)


def _root_options() -> list[str]:
    """The root options this `probe` was started with (`--base-url`,
    `--spool-dir`), for the newest release to run the update with the same."""
    options: list[str] = []
    if _conn.base_url:
        options += ["--base-url", _conn.base_url]
    if _conn.spool_dir:
        options += ["--spool-dir", _conn.spool_dir]
    return options


def _update_argv(*, yes: bool, json_output: bool = False, agent=None) -> list[str]:
    """`probe wizard --action update` as this run was asked for it (the agents
    named or picked), for the newest release to run in its place
    (`_hand_off_update`)."""
    argv = ["wizard", "--action", "update"]
    for value in _agent_values(agent):
        argv += ["--agent", value]
    if yes:
        argv.append("--yes")
    if json_output:
        argv.append("--json")
    return argv


class _UpdateProgress:
    """The wizard's Update as a bar with its percentage under the spinner: the
    CLI and pi's package once, every agent's plugins (at once), then what is
    installed recorded for each agent, in that order, the label naming what
    is running. `upgrading.reporting_progress`'s hook: called from the agents'
    update threads too. `status` None (no spinner) shows nothing."""

    def __init__(self, sources, status) -> None:
        import threading

        from probe.cli.install.upgrade.upgrade import UpdatePart

        self._sources = list(sources)
        self._status = status
        self._core = [UpdatePart.CLI, UpdatePart.PI_PACKAGE]
        self._plugins = list(self._sources)
        self._recording = list(self._sources)
        # One more for sending it all (`sent`): only then is it 100%.
        self._sending = True
        self._total = len(self._core) + 2 * len(self._sources) + 1
        self._lock = threading.Lock()
        self._show()

    def __call__(self, part: str) -> None:
        with self._lock:
            for left in (self._core, self._plugins):
                if part in left:
                    left.remove(part)
                    break
            self._show()

    def recorded(self, source: str) -> None:
        with self._lock:
            if source in self._recording:
                self._recording.remove(source)
            self._show()

    def sent(self) -> None:
        """The merged registration and report went out: the update is done."""
        with self._lock:
            self._sending = False
            self._show()

    def _label(self) -> str:
        from probe.cli import wizard as wizard
        from probe.cli.install.upgrade.upgrade import UpdatePart
        from probe.cli.install.upgrade.package_step import package_harness

        if UpdatePart.CLI in self._core:
            return "Updating the Probe CLI"
        # pi's package moves above, once: its own pass has nothing to wait on.
        package = package_harness()
        updating = [wizard.agent_label(s) for s in self._plugins if s != package]
        if UpdatePart.PI_PACKAGE in self._core and package in self._sources:
            return f"Updating {wizard.agent_label(package)}'s Probe package"
        if updating:
            return f"Updating the plugins for {wizard.spoken_list(updating)}"
        if self._recording:
            return f"Recording what is installed for {wizard.agent_label(self._recording[0])}"
        return "Sending the update's results to Probe"

    def _show(self) -> None:
        if self._status is None:
            return
        left = len(self._core) + len(self._plugins) + len(self._recording) + self._sending
        self._status.set(label=self._label(), fraction=(self._total - left) / self._total)


def _update_agents(sources, *, base_now: str, yes: bool, progress: "_UpdateProgress | None" = None) -> dict:
    """The Update action for several agents (`upgrading.perform_updates`):
    each agent's answer, which its own pass then reports (`_run_wizard_action`)."""
    from probe.cli.install.upgrade.upgrade import perform_updates, reporting_progress

    with reporting_progress(progress) if progress is not None else contextlib.nullcontext():
        return perform_updates(
            list(sources), base_url=base_now, include_plugin=True, trigger=_update_action_trigger(yes)
        )
from probe.cli.commands.machine.wizard import wizard  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _conn  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.agent_flags import _agent_values  # noqa: E402 -- pieces need each other; the front door loads this one first
