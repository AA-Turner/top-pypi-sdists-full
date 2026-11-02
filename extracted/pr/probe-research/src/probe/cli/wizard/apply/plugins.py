"""install and uninstall Probe's plugins through each harness's PluginInstaller, refreshing a marketplace once per run (batched across agents)."""

from __future__ import annotations

import contextlib
import threading
from concurrent.futures import FIRST_COMPLETED, Future
from concurrent.futures import wait as wait_for_futures
import contextvars
from contextvars import ContextVar
from collections.abc import Iterable, Mapping, Sequence
from probe.shared.harness.harnesses.claude_code import binary as claude_cli
from probe.shared.harness.harnesses import pi as pi_config
from probe.shared.harness import plugins as plugin_cli
from probe.cli.wizard.state.state import (
    DAEMON_PLUGIN_NAME,
    MARKETPLACE,
    MARKETPLACE_REPO,
    TAP_PLUGIN_NAME,
    TRACKING_PLUGIN_NAME,
    Capability)
from probe.cli.wizard.state.agent_identity import agent_source


#: The refreshes and installs `marketplace_refreshes` runs together: the
#: sources still to take theirs, each one's answer once run (its refresh and
#: the installs after it), the installs each source asked for, which of their
#: capabilities the run may install (`allow_batch_installs`), and the installs
#: already taken. None outside one.
_refresh_batch: ContextVar[dict | None] = ContextVar("probe_marketplace_refreshes", default=None)


@contextlib.contextmanager
def marketplace_refreshes(
    sources: Iterable[str], installs: Mapping[str, Sequence[tuple[Capability, str]]] | None = None
):
    """In this block, the first `refresh_marketplace` of any of `sources`
    refreshes all of them at once, one thread each, then installs each one's
    `installs` (capability, plugin name), in order, on the same thread, and
    returns once every one has answered; each source's own first refresh and
    its installs (`install_plugin`) then take their answers instead of running
    again (a second one, an install's retry, runs for real).

    An install for several agents refreshed and installed one agent after
    another, a git clone or fetch (~2.5 s on a first install) and a plugin
    install or two each. Here they overlap. The first refresh is an install
    step, after the sign-in: nothing is written while a person approves
    (`sdk.settings.device`), and a first `add` writes Claude Code's settings or Codex's
    config.toml. Only plugins whose credential the sign-in got are installed
    (`allow_batch_installs`). Every one answers before the first refresh
    returns, so none runs beside another agent's install steps."""
    token = _refresh_batch.set({
        "pending": set(sources), "answers": {}, "installed": {}, "installs": dict(installs or {}),
        "allowed": frozenset(), "taken": set(),
    })
    try:
        yield
    finally:
        _refresh_batch.reset(token)


def allow_batch_installs(capabilities: Iterable[Capability]) -> None:
    """The capabilities whose plugins the open batch may install with its
    refreshes: those the run holds a credential for, set at the install's
    refresh step. Unset, the batch installs nothing: each agent installs at
    its own step, as before."""
    batch = _refresh_batch.get()
    if batch is not None and not batch["answers"]:
        batch["allowed"] = frozenset(capabilities)


def _taken_install(name: str, source: str) -> "claude_cli.Result | None":
    """The open batch's install of `name` for `source`, once, if it ran."""
    batch = _refresh_batch.get()
    future = batch["installed"].get(source) if batch is not None else None
    if future is None or not future.done() or future.exception() is not None:
        return None
    installed = future.result()
    if name not in installed or (source, name) in batch["taken"]:
        return None
    batch["taken"].add((source, name))
    return installed[name]


def _refresh_together(batch: dict) -> None:
    """Start every refresh in `batch` on its own thread and wait for them all.
    A daemon thread each, and an interrupted wait is not resumed: a cancelled
    wizard exits now (a terminal's Ctrl-C stops the agents' CLIs with it). A
    source whose thread cannot start (a process limit) refreshes on its own, at
    its own step, as it did before the batch."""
    answers: dict[str, Future] = batch["answers"]
    #: Each future's source and how many of its units it finishes.
    units: dict[Future, tuple[str, int]] = {}
    for each in sorted(batch["pending"]):
        refreshed: Future = Future()
        installed: Future = Future()
        plan = [name for capability, name in batch["installs"].get(each, ()) if capability in batch["allowed"]]

        def run(each=each, refreshed=refreshed, installed=installed, plan=plan) -> None:
            try:
                refreshed.set_result(_refresh_marketplace_now(each))
            except BaseException as exc:  # noqa: BLE001 - re-raised to its source's refresh
                refreshed.set_exception(exc)
            try:
                retried: list[bool] = []
                # One retry for the agent, as `_run_wizard_action`'s budget allows.
                installed.set_result({
                    name: install_plugin(
                        name, source=each, on_retry=lambda: not retried and not retried.append(True)
                    )
                    for name in plan
                })
            except BaseException as exc:  # noqa: BLE001 - the agent's own step installs again
                installed.set_exception(exc)

        try:
            # An empty context: a thread that saw this batch (a free-threaded
            # build copies the caller's) would wait on itself from a retry.
            threading.Thread(
                target=contextvars.Context().run, args=(run,), name=f"probe-marketplace-{each}", daemon=True
            ).start()
        except RuntimeError:
            break
        answers[each] = refreshed
        batch["installed"][each] = installed
        units[refreshed] = (each, 1)
        units[installed] = (each, len(plan))
    batch["pending"].intersection_update(answers)
    run = _install_run.get()
    # Waited for HERE, the thread that draws the screen: the run's bar moves
    # as each agent's refresh and installs finish.
    if run is not None:
        run.batch_started(answers)
    waiting = set(units)
    while waiting:
        finished, waiting = wait_for_futures(waiting, return_when=FIRST_COMPLETED)
        for future in finished:
            if run is not None:
                run.batch_progress(*units[future])


def refresh_marketplace(*, source: str | None = None) -> claude_cli.Result:
    """Bring the local marketplace copy up to date. ONCE per wizard run.

    `marketplace add` on an already-added marketplace does NOT refresh it, so
    without the update a fresh wizard run happily installs a stale plugin
    version -- which is exactly how a newly published plugin appears to be
    missing. The dashboard's pairing modal ships `add` and `update` as separate
    commands for the same reason.

    Hoisted OUT of install_plugin, which used to do it per plugin: a run that
    installs both plugins refreshed the same marketplace twice, and threw both
    results away. Discarding them is why a failed refresh surfaced as Claude's
    downstream "not found in marketplace" -- an error whose suggested fix is
    the very command the wizard had just silently failed at.

    `add` failing is NOT fatal and is not reported: the common case is "already
    on disk", which exits non-zero on some versions. `update` is the one whose
    success decides whether the catalog we install from is current, except
    after an `add` that cloned the marketplace just now: that copy is current,
    and its answer is the refresh's (`_refresh_marketplace_now`). Inside
    `marketplace_refreshes`, several agents' refreshes run at once.

    pi has no marketplace to refresh -- `install_plugin`/`uninstall_plugin`
    route it through `pi_config`'s settings.json entry instead (see
    `INSTALLABLE_AGENT_SOURCES`), which needs no separate refresh step.
    Checked explicitly, not folded into the (now pi-inclusive)
    `INSTALLABLE_AGENT_SOURCES` membership test below, because pi IS
    installable through this wizard now -- just not through a marketplace.
    Reported as a no-op SUCCESS, not a failure: main.py's `_refresh()` step
    turns any non-`ok` Result here into a printed "! could not refresh..."
    line, and a pi capture install's own step label now legitimately starts
    with "install" (pi is no longer excluded from that check either), which
    schedules this step for a pi run exactly like it does for claude_code/
    codex. A failure-shaped no-op would paint a real success red.
    """
    selected = source or agent_source()
    batch = _refresh_batch.get()
    if batch is not None and selected in batch["pending"] and not batch["answers"]:
        _refresh_together(batch)
    if batch is None or selected not in batch["pending"]:
        return _refresh_marketplace_now(selected)
    batch["pending"].discard(selected)
    return batch["answers"][selected].result()


def _refresh_marketplace_now(selected: str) -> claude_cli.Result:
    """`refresh_marketplace` for `selected`, run now."""
    if selected == "pi":
        return claude_cli.Result(ok=True, detail=f"{selected} has no plugin marketplace to refresh")
    if selected not in INSTALLABLE_AGENT_SOURCES:
        return claude_cli.Result(
            ok=False, detail=f"{selected} has no plugin marketplace", reachable=False
        )
    checkout = plugin_cli.marketplace_checkout(selected, MARKETPLACE)
    cloning = checkout is not None and not checkout.exists()
    added = plugin_cli.add_marketplace(selected, MARKETPLACE_REPO, name=MARKETPLACE)
    if cloning and added.ok and checkout.exists():
        # This `add` cloned it just now, so the copy is current: an `update`
        # would fetch the same repository again, ~2 s of a first install.
        return added
    refreshed = plugin_cli.refresh_marketplace(selected, MARKETPLACE)
    if not refreshed.ok and not added.ok:
        from probe.cli.install import updater

        # On a machine that never added the marketplace, `add` is the clone
        # that hits a Mac's blocked git, and `update` then fails as "not
        # found": report the cause, not the symptom.
        if updater.git_blocker(added.detail):
            return added
        # Otherwise say BOTH. `add` alone can be the harmless "already
        # added", but when the refresh then fails too, `add`'s refusal is
        # usually the cause: Codex's "not configured as a Git marketplace"
        # was all a researcher saw of an add that had been refused.
        return claude_cli.Result(
            ok=False,
            detail=f"`{added.command}` failed: {added.detail}\n"
            f"`{refreshed.command}` failed: {refreshed.detail}",
            reachable=refreshed.reachable,
            command=refreshed.command,
        )
    return refreshed


def install_plugin(name: str, *, source: str | None = None, on_retry=None) -> claude_cli.Result:
    """Install one plugin. Retries ONCE, after a refresh, on ANY failure.

    Deliberately NOT gated on matching Claude's error text. A retry that fires
    only when the message contains "not found in marketplace" is a guard that
    certifies its own rot: Anthropic rewords the string, the retry silently
    stops firing, and every test stays green. One plain rule instead -- it
    failed, so refresh and try once more -- costs one extra attempt on a
    genuinely broken machine and cannot fall out of sync with anyone's prose.

    `on_retry` is the caller's retry BUDGET, not a notification: it returns
    False once the run has already spent its single retry, so two plugins
    failing cannot cost two refreshes and two reinstalls.

    pi has NO marketplace at all, so `name` is ignored on that branch (see
    `_install_pi_package`): one settings.json `packages` entry is the whole
    install, for every capability that reaches this function -- both
    `apply_tracking`'s and `apply_capture`'s calls converge on the same
    idempotent write. Retrying is meaningless there too (a failed write is
    not repaired by trying the identical write again), so `on_retry` is
    never consulted on that branch.
    """
    # Installing Probe again after an Uninstall: the OS keeper may come back (D35).
    with contextlib.suppress(Exception):
        from probe.service import keeper

        keeper.allow()
    selected = source or agent_source()
    taken = _taken_install(name, selected)
    if taken is not None:
        return taken  # installed with its marketplace's refresh (`marketplace_refreshes`)
    if selected not in INSTALLABLE_AGENT_SOURCES:
        return claude_cli.Result(
            ok=False, detail=f"{selected} has no plugin marketplace", reachable=False
        )
    if selected == "pi":
        # One package, two halves: only the tracking half's install (either
        # profile's name) brings Probe's skills and MCP on a FRESH entry; the
        # capture half arrives as `pi_config.PACKAGE_NAME` (CAPTURE_PLUGIN_LABEL).
        return _install_pi_package(tracking=name in _TRACKING_NAMES)
    result = plugin_cli.install(selected, f"{name}@{MARKETPLACE}")
    if result.ok or on_retry is None or not on_retry():
        return result
    refresh_marketplace(source=selected)
    return plugin_cli.install(selected, f"{name}@{MARKETPLACE}")


#: The tracking half's plugin names (either profile). For pi, whose one package
#: carries both halves, these decide which half an install or uninstall means.
_TRACKING_NAMES = (TRACKING_PLUGIN_NAME, DAEMON_PLUGIN_NAME)


def uninstall_plugin(
    name: str, *, source: str | None = None, keep_capture: bool | None = None
) -> claude_cli.Result:
    selected = source or agent_source()
    if selected not in INSTALLABLE_AGENT_SOURCES:
        return claude_cli.Result(
            ok=False, detail=f"{selected} has no plugin marketplace", reachable=False
        )
    if selected == "pi":
        capture_stays = _settings_capture_on(selected) if keep_capture is None else keep_capture
        if name in _TRACKING_NAMES and capture_stays:
            # Capture rides in the same package: switch tracking off instead.
            return pi_config.set_tracking(False, daemon=daemon_records(selected))
        return pi_config.remove_package_entry()
    return plugin_cli.uninstall(selected, f"{name}@{MARKETPLACE}")


def codex_plugins_kept_on(selection: Selection) -> frozenset[str]:
    """The Probe plugins whose hooks a wizard run may approve: those of the
    capabilities this selection keeps on. Capture turned off leaves the tap
    installed (DISABLE), and its hooks must not be approved in that same run."""
    plugins: set[str] = set()
    if selection.tracking:
        plugins |= {TRACKING_PLUGIN_NAME, DAEMON_PLUGIN_NAME}
    if selection.capture:
        plugins.add(TAP_PLUGIN_NAME)
    return frozenset(plugins)
from probe.cli.wizard.agents import INSTALLABLE_AGENT_SOURCES  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.apply.apply import daemon_records  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.screens.install_steps import _install_run  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.wizard import Selection, plan  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.harness.harnesses.pi.package_install import _install_pi_package, _settings_capture_on  # noqa: E402 -- pieces need each other; the front door loads this one first
