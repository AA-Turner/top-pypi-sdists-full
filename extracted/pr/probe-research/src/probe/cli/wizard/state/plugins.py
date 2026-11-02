"""which Probe plugins the selected agent reports installed: its own record (PluginInstaller ledger) or its CLI."""

from __future__ import annotations
from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from pathlib import Path

from probe.shared.harness.harnesses import pi as pi_config
from probe.shared.harness import plugins as plugin_cli
from probe.shared.harness.harnesses.claude_code.plugin_ledger import _claude_ledger_ids
from probe.shared.harness.harnesses.codex.plugin_ids import _codex_plugin_ids


@dataclass(frozen=True)
class PluginState:
    """What Claude Code reports installed, AND whether it managed to answer.

    THE TWO ARE DIFFERENT and collapsing them is a bug. An empty `names` used
    to mean three unrelated things at once -- the plugins are genuinely absent,
    `claude` is not on this machine, or the query timed out -- so any caller
    that treated "empty" as "not installed" would tell someone on a GPU pod
    that their setup failed. `verified` separates "we looked and they are not
    there" from "we could not look".
    """

    names: frozenset[str] = frozenset()
    verified: bool = True
    #: Why it could not look, when it could not (None when it did, or when
    #: there is no list to read, as for pi).
    error: str | None = None

    def __contains__(self, name: str) -> bool:
        return name in self.names

    def __iter__(self):
        return iter(self.names)

    def __len__(self) -> int:
        return len(self.names)

    def missing(self, wanted) -> list[str]:
        """Names VERIFIED absent. Empty when we could not check -- an
        unanswerable question must not read as a negative answer."""
        if not self.verified:
            return []
        return [name for name in wanted if name not in self.names]


def installed_plugins(*, source: str | None = None, local: bool = False) -> PluginState:
    """Plugin names the selected coding agent reports as installed.

    `local` reads the record the agent's own `plugin list` reads instead of
    running it (`probe status` without --refresh): Claude Code's install ledger,
    Codex's config.toml (`_local_plugins`). pi and Kimi Code are file reads
    either way.

    ``verified=False`` when its CLI is absent (normal on a GPU pod and never
    an error) or the query could not complete.

    pi is neither: it is a source this module KNOWS has no plugin CLI at all
    (plugin_cli.py's own docstring scopes that module to claude/codex; see
    setup.py's INSTALLABLE_AGENT_SOURCES for the wizard-facing side of the
    same fact -- not imported here, that would be circular, since setup.py
    imports FROM this module). Falling through to plugin_cli.list_plugins("pi")
    would resolve its binary as "claude" (plugin_cli.binary_name()'s own
    codex-or-claude default) and silently report on CLAUDE'S plugins under
    pi's name.

    pi DOES have a real, checkable install signal though (plan D7): its own
    settings.json `packages` entry, read via `pi_config.package_entry_installed`
    -- a direct file read, not a subprocess that can merely time out. That is
    reflected in `names` (so `capture_plugin_name(selected) in plugins`, what
    doctor.py/`Capabilities.capture_plugin_installed` actually check, stops
    being pinned False forever), but `verified` stays False regardless, on
    purpose: a positive read (`package_entry_installed()` True) is a fact we
    can stand behind, but a negative one collapses several different causes
    together (genuinely absent, malformed settings.json, an unresolvable
    package root -- see that function's own docstring) the way a `claude
    plugin list` timeout does NOT. `verified=True` here would let a stale or
    unreadable settings.json read as "verified absent" downstream -- the
    wizard's post-install pass/fail gate in main.py -- rather than "unknown",
    which is the wrong failure mode for a check this cheap to get wrong.
    """
    selected = source or agent_source()
    if selected == "pi":
        # One package carries both halves. Capture rides on the entry; tracking
        # too unless the entry switches it off (`probeTracking: false`). Read as
        # pi resolves it, project over global, from the current folder.
        merged = pi_config.merged_package_entry(cwd=Path.cwd())
        if not merged.installed:
            return PluginState(verified=False)
        names = {TAP_PLUGIN_NAME}
        if not merged.tracking_off:
            names.add(tracking_plugin_name(selected))
        return PluginState(names=frozenset(names), verified=False)
    if (local or _read_records.get()) and selected in LOCAL_PLUGIN_RECORDS:
        return _local_plugins(selected)
    result = plugin_cli.list_plugins(selected)
    if not result.reachable:
        return PluginState(verified=False, error=result.detail or None)
    names: set[str] = set()
    for line in result.detail.splitlines():
        # `probe-research` is a PREFIX of `probe-research-tap`, so a line naming
        # the tap contains both. Longest match wins per line, otherwise having
        # only the tap installed would read as tracking being on too.
        tap_name = capture_plugin_name(selected)
        if selected == "codex" and LEGACY_CODEX_TAP_PLUGIN_ID in line:
            names.add(LEGACY_CODEX_TAP_PLUGIN_ID)
        elif tap_name in line:
            names.add(tap_name)
        elif DAEMON_PLUGIN_NAME in line:
            # Also a longer name that CONTAINS `probe-research`: the lean
            # plugin must not read as the full one.
            names.add(DAEMON_PLUGIN_NAME)
        elif TRACKING_PLUGIN_NAME in line:
            names.add(TRACKING_PLUGIN_NAME)
    # A non-zero exit with readable output still tells us what IS installed, but
    # not reliably what is not -- so parse it and decline to call it verified.
    return PluginState(
        names=frozenset(names), verified=result.ok, error=None if result.ok else (result.detail or None)
    )


#: Whether `installed_plugins` reads each agent's own record in place of its
#: `plugin list` (`plugin_records`).
_read_records: ContextVar[bool] = ContextVar("probe_plugin_records", default=False)


@contextmanager
def plugin_records(on: bool = True) -> Iterator[None]:
    """In this block, `installed_plugins` reads each agent's own plugin record,
    the file its `plugin list` reads (`_local_plugins`, as `probe status` does),
    instead of starting the agent's CLI; `on=False` turns that back off. The wizard reads every agent's state on
    entry and again after every change, and each `plugin list` is a Node start
    (~0.6 s on a fast Linux box, more on a laptop); the records take
    milliseconds and say the same."""
    token = _read_records.set(on)
    try:
        yield
    finally:
        _read_records.reset(token)


#: The agents whose `plugin list` is a subprocess, and the file it reads.
LOCAL_PLUGIN_RECORDS = {plugin_cli.CLAUDE: _claude_ledger_ids, plugin_cli.CODEX: _codex_plugin_ids}


def _local_plugins(source: str) -> PluginState:
    """`installed_plugins` from the agent's own record, with no subprocess.

    Mirrors the CLI path on purpose: no binary on PATH reads unverified, as
    `plugin list` would (so the default and --refresh status agree), and an
    unreadable record reads unverified with the reason, never as "nothing
    installed". Names are matched whole, so the tap and the daemon plugin never
    read as the tracking plugin they contain."""
    if not plugin_cli.available(source):
        return PluginState(verified=False, error=f"`{plugin_cli.binary_name(source)}` not found on PATH")
    try:
        ids = LOCAL_PLUGIN_RECORDS[source]()
    except Exception as exc:  # noqa: BLE001 - an unreadable record is "could not look"
        return PluginState(verified=False, error=f"could not read its plugin record ({type(exc).__name__}: {exc})")
    tap_name = capture_plugin_name(source)
    known = {tap_name, DAEMON_PLUGIN_NAME, TRACKING_PLUGIN_NAME}
    names: set[str] = set()
    for plugin_id in ids:
        if source == plugin_cli.CODEX and plugin_id == LEGACY_CODEX_TAP_PLUGIN_ID:
            names.add(LEGACY_CODEX_TAP_PLUGIN_ID)
            continue
        name = plugin_id.split("@", 1)[0]
        if name in known:
            names.add(name)
    return PluginState(names=frozenset(names), verified=True)
from probe.cli.wizard.state.agent_identity import agent_source, capture_plugin_name, tracking_plugin_name  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.state.state import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    DAEMON_PLUGIN_NAME,
    LEGACY_CODEX_TAP_PLUGIN_ID,
    TAP_PLUGIN_NAME,
    TRACKING_PLUGIN_NAME,
)
