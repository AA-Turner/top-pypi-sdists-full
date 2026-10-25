"""`probe status --json`: this device's ONE Probe install, as one JSON object.

The desktop app (and any agent) reads this to show the state the terminal
wizard's menu shows. The two are front ends over one install, so nothing here
reads state of its own: every field comes from what the menu renders --
`doctor.collect` per agent (the struct the menu header draws), `setup`'s
`detectable_sources`, `machine_recorder` and `version_verdict`,
`session_marker`'s default and recorder reads, the config's active context, the
daemon readers `probe doctor` prints, and `wizard_lock` for a run in progress.

DEFAULT: LOCAL ONLY. The config, the agents' own install records and marker
files: no network call and no subprocess (no `claude plugin list`, no `codex
plugin list`, no `ps`), so the app can ask on every focus. TWO exceptions.
`codex_hooks`: where Probe's Codex plugins are installed and a Codex binary is
on PATH, Codex itself is asked which of Probe's hooks it will run (`codex
app-server`, ~0.2-0.6s, never more than 2s), at most once per 10 minutes, again
after a Probe plugin update or a change to Codex's config, the answer kept on
disk between (`probe.cli.codex_hooks.status_snapshot`). Nothing else Probe has
can see a hook Codex silently skips. `service`: the Probe service, which owns
this machine's local Probe work, is asked what it holds, over its Unix socket
on this machine (never the network), within 1 s in all, and never started:
with no service socket file there (none runs), no socket is opened at all.
`--refresh` adds what the menu asks, all of it inside ONE budget of `--timeout` seconds from the start
(`claude_cli.bounded`): the agents' own CLIs -- every agent's `plugin list` at
once, Codex's `mcp list`, `--version`, pi's `--help` -- a hung binary asked
once and killed with its process group; the server's one `POST
/v1/device-state` (a server that predates it: `/v1/me` and the capture
credentials the old way, once for every agent); and the API's verdict on the
MCP read token. The server and the token check start first and are read after
the agents. A check the budget cuts is an `error` on that check, never a hang.
An agent that is not on this machine has no CLI to ask: it is read from its
files under --refresh too.

Exit 0 whatever the state -- signed out, nothing installed, a corrupt config:
state is data. A usage error exits 2.

SCHEMA (v1). Change it only by adding fields; anything else bumps
`SCHEMA_VERSION`. `tests/test_status_json.py` pins these names.

    {
      "v": 1,
      "refreshed": bool,
      "cli": {"version": str, "install_method": str | null},
      "account": {
        "signed_in": bool | null,
        "email": str | null,
        "context": str | null,
        "base_url": str | null,
        "credential_valid": bool | null,
        "workspace_limit": LIMIT | null
      },
      "agents": [
        {
          "agent": str,
          "label": str,
          "installed": bool,
          "configured": bool | null,
          "plugin_installed": bool | null,
          "capture_on": bool | null,
          "mcp_state": str | null,
          "mcp_detail": str | null,
          "recorder": str | null,
          "plugins": CHECK
        }
      ],
      "who_records": str | null,
      "session_default": {"state": str | null, "env_override": str | null},
      "auto_update": {"enabled": bool, "last_attempt": str | null},
      "versions": {
        "status": str,
        "manifest_age_s": int | null,
        "components": [{"kind": str, "installed": str | null, "latest": str | null, "status": str}]
      },
      "daemon": {
        "key_held": bool | null,
        "ai_libraries": str | null,
        "model_tokens_today": int | null,
        "reader_tokens_today": int,
        "recent_errors": [str]
      },
      "wizard_running": bool | null,
      "codex_hooks": {
        "state": str,
        "untrusted": [str],
        "checked_at": int | null,
        "unheard_session": str | null
      },
      "service": {
        "reach": str,
        "running": bool | null,
        "error": str | null,
        "version": str | null,
        "pid": int | null,
        "state": str | null,
        "started_at": float | null,
        "sessions": [{"sid": str, "harness": str, "mode": str, "alive": bool, "agent_live": bool | null,
                      "receipts": {"last_line": int | null, "received_bytes": int | null,
                                   "received_at": float | null, "pending_bytes": int | null,
                                   "pending_lines": int | null, "pending_batch": bool | null,
                                   "finalized": bool | null, "retrying": bool | null,
                                   "scope": {"backend": str | null, "customer": str | null}}}],
        "harnesses": [{"harness": str, "scope": {"backend": str | null, "customer": str | null},
                       "sessions": int | null, "alive": int | null,
                       "received_at": float | null, "pending_bytes": int | null,
                       "pending_lines": int | null, "pending_batches": int | null}],
        "recorders": [{"sid": str, "alive": bool, "recording": bool | null, "last": str, "failures": int}],
        "hook_hosts": [{"root": str, "pid": int}],
        "runs": [{"run": str, "pid": int, "since": float}],
        "imports": [{"job_id": str, "pid": int, "since": float}],
        "update": {
          "enabled": bool | null,
          "in_progress": bool | null,
          "step": str | null,
          "last_check": float | null,
          "last_ok": bool | null,
          "next_check": float | null,
          "deferred_reason": str | null,
          "deferred_at": float | null,
          "deferred_since": float | null
        }
      },
      "checks": {"device_state": CHECK, "mcp_token": CHECK},
      "errors": [{"field": str, "message": str}]
    }

    CHECK = {"state": str | null, "checked": bool, "error": str | null}
    LIMIT = {"id": str | null, "name": str | null, "slug": str | null, "team_items": str}

What the values mean:

- `account.workspace_limit`: this computer's workspace limit (`probe workspace
  limit`), from the config and `PROBE_WORKSPACE_LIMIT` -- local, no network, so an
  environment slug shows as `slug` with `id` null; null for the whole team.
- `account.signed_in`: a CLI token resolves (the active context, or
  PROBE_TOKEN). `email` and `credential_valid` (accepted / refused / null
  unknown) are the server's answer, so only `--refresh` fills them: the config
  stores no email.
- `agents`: every agent Probe can set up, in registry order. `installed`: its
  binary is on PATH (without --refresh a pi binary on PATH is taken at its
  word). `configured`: Probe
  was set up for THIS agent -- its plugins, capture pairing or rules
  (`Capabilities.agent_configured`). Deliberately not the menu's
  `Capabilities.configured`, which also counts the device's own evidence
  (the sign-in, automatic updates, the updater's last attempt) and so reads
  true for every agent on a signed-in device, pi never set up included.
  `plugin_installed`: the Probe plugin its Who records profile carries.
  `mcp_state`: `McpState` (on | login-needed | daemon | not-installed |
  not-offered | unknown); `mcp_detail`: the words `probe doctor` prints for it,
  with why it is unknown ("unknown: not checked: ..." for a Codex OAuth login,
  which only `codex mcp list` reads, so only --refresh). `recorder`: agent |
  daemon, null for an agent with no daemon profile. The state fields are null
  when reading that agent failed (`errors`) and when the config could not be.
- `agents[].plugins`: `state` verified | unverified -- whether
  `plugin_installed` was read (from the agent's own record by default, from its
  CLI with --refresh) or could not be, so false means unknown; `checked`: its
  CLI answered (--refresh only); `error`: why unverified.
- `who_records`: agent | daemon, the menu's Who records row
  (`setup.machine_recorder`).
- `session_default.state`: on | read | off for a new session, as the menu's
  Defaults row; `env_override`: the state an environment variable holds it at.
- `versions.status`: `VersionStatus` (current | update | needed | required |
  unknown) for the CLI, plugin and tap, graded against the cached manifest.
- `daemon.ai_libraries`: the Pydantic AI version the daemon runs on, "missing",
  or null when it could not be read.
- `wizard_running`: a `probe wizard` (terminal or app) holds the run lock now;
  null when that could not be told.
- `codex_hooks`: whether Codex runs Probe's hooks. Codex trusts each hook by a
  hash of its entry and silently skips one it has not approved, so a Probe
  update that changes an entry switches it off until the person types /hooks in
  Codex and approves it. `state`: `HooksState` (approved | needs_approval |
  unknown | none): `none` when no Probe plugin is installed in Codex (or none
  is enabled), `unknown` when Codex could not be asked and no session says
  otherwise. `untrusted`: the hook keys Codex named as waiting for approval
  (`<plugin>@<marketplace>:hooks/hooks.json:<event>:<group>:<index>`), empty
  when it was not asked. `checked_at`: when Codex answered (epoch seconds; the
  answer may be up to 10 minutes old), null when it was not asked.
  `unheard_session`: the newest Codex session that expected Probe's hooks and
  never ran them (from the hooks' own heartbeat files), else null. Codex's
  answer decides `state`; without one, an `unheard_session` means
  needs_approval.
- `service`: what this machine's Probe service says (`service.status` and
  `session.list`). `reach`: `service_calls.Reach` (answered | not_running |
  refused | unreachable | unsupported); `running` is true when it answered,
  false when none runs (it starts with the next coding-agent session, or
  `probe service start`), null when that could not be told (`error` says
  why). `state`: discovering | running | grace. `sessions`: every session it
  has registered, with its Probe `mode` (daemon | inline | off), whether it
  is `alive` (never for mode off: such a session holds nothing up),
  `agent_live`: whether its agent still runs, whatever its mode (null when
  that cannot be told), and its delivery `receipts` from its recorder's transcript
  journal (null when no live recorder holds the session in one): the server's receipt cursor
  (`last_line`, `received_bytes`), when it last took the transcript
  (`received_at`, epoch seconds; null from a tap before 0.10.6), and what waits
  (`pending_bytes` and `pending_lines` past that cursor, `pending_batch` staged),
  and `scope`: the account of the journal it came from (`backend`, the base
  URL's host; `customer`), to show only the signed-in account's.
  `harnesses`: the same per agent and scope (null for sessions without receipts), over its listed sessions
  (sums over the sessions where they are known, the latest `received_at`).
  `recorders`: the sessions it records itself (`alive`: its recorder's
  thread runs, also while it waits to try again; `recording`: it holds the
  session now, so it is the one recording it, null from a tap before 0.10.5;
  `last`: how its recorder last ended, `failures`: restarts after a failure). `hook_hosts`: its
  warm hook hosts, one per plugin folder. `runs`: the runs a `probe exec` holds
  (the updater does not update under them). `imports`: the approved imports
  whose worker it started and watches (`probe wizard --action imports` has
  their progress). `update`: its updater -- a cycle
  `in_progress` (its `step`), the last check and whether it was ok, the next
  one, and the reason the last cycle was deferred (`deferred_reason`, since
  `deferred_since`). Everything but `reach` is null or empty unless it answered.
- `checks.device_state.state`: answered | unsupported (the server predates the
  call; the account was asked the old way) | unreachable; null without --refresh.
  `checks.mcp_token.state`: ok | rejected | unreachable | no_token; null
  without --refresh. Either is null with an `error` when the budget ran out
  first or it was not asked (a `config` error).
- `errors`: what could not be read -- a corrupt config, a corrupt
  `autoupdate.json` (`auto_update` then reads off, as the menu shows it), an
  agent's unreadable plugin record, a failed read of one agent. A field it
  names may then show a default, so an `errors` entry is never a fresh device.

A `config` error (the config exists and cannot be read, or is not a JSON
object) INVALIDATES everything read from it, which is null instead of a
default: the whole `account`; every agent's `configured`, `plugin_installed`,
`capture_on`, `mcp_state`, `mcp_detail` and `recorder` (Who records picks the
plugin looked for; the config holds Claude Code's capture credential and the
read token), with `plugins` unverified; `who_records`; `session_default.state`
(unless an environment variable holds it); `daemon.key_held`. With --refresh
neither the server nor the token check is asked: both `checks` say why.
"""

from __future__ import annotations

import concurrent.futures
import contextvars
import dataclasses
import functools
import json
import threading
import time
from collections.abc import Callable
from typing import Any, TypeVar

from probe._compat import StrEnum

#: Bumped only for a change a reader written against the old shape would misread.
SCHEMA_VERSION = 1

#: `--refresh`'s default budget: the seconds the whole refreshed read may take.
DEFAULT_TIMEOUT_S = 10.0

#: How long past the budget a bounded agent-CLI call may take to come back:
#: its own timeout fires at the budget, and the kill of its process group and
#: the read of its last output follow.
_KILL_GRACE_S = 1.0

#: Why a field or a check a config that cannot be read leaves unknown.
_CONFIG_UNREADABLE = "the config could not be read"

_T = TypeVar("_T")


class PluginsState(StrEnum):
    VERIFIED = "verified"
    UNVERIFIED = "unverified"


class TokenCheck(StrEnum):
    """`checks.mcp_token.state` beyond the API's own ok | rejected | unreachable."""

    NO_TOKEN = "no_token"
    UNREACHABLE = "unreachable"


def _check(state: str | None = None, *, checked: bool = False, error: str | None = None) -> dict:
    return {"state": None if state is None else str(state), "checked": checked, "error": error}


def _error(field: str, message: str) -> dict:
    return {"field": field, "message": message}


@dataclasses.dataclass(frozen=True)
class _Budget:
    """`--refresh --timeout`: ONE budget for the whole read, from its start.
    The agent-CLI calls share it through `claude_cli.bounded`."""

    timeout: float
    deadline: float

    @classmethod
    def starting(cls, timeout: float) -> _Budget:
        return cls(timeout, time.monotonic() + timeout)

    def left(self) -> float:
        return max(0.0, self.deadline - time.monotonic())

    def timed_out(self) -> str:
        from probe.cli import claude_cli

        return f"timed out after {claude_cli.seconds(self.timeout)}"


def _start(fn: Callable[[], _T]) -> concurrent.futures.Future:
    """`fn()` on a daemon thread, in a copy of this context (so it shares the
    `claude_cli.bounded` budget). A daemon thread, not an executor: a check
    that never answers must not hold the process open at exit."""
    future: concurrent.futures.Future = concurrent.futures.Future()
    context = contextvars.copy_context()

    def run() -> None:
        try:
            future.set_result(context.run(fn))
        except BaseException as exc:  # noqa: BLE001 - reported to the waiter
            future.set_exception(exc)

    threading.Thread(target=run, name="probe-status-check", daemon=True).start()
    return future


def _wait(future: concurrent.futures.Future, budget: _Budget, *, grace: float = 0.0) -> tuple[Any, str | None]:
    """(value, None), or (None, why) once the budget (plus `grace`) is spent.
    A late answer is dropped, never recorded by the caller."""
    try:
        return future.result(timeout=budget.left() + grace), None
    except concurrent.futures.TimeoutError:
        return None, budget.timed_out()
    except Exception as exc:  # noqa: BLE001 - a status read never raises
        return None, f"{type(exc).__name__}: {exc}"


class _Server:
    """The server's half of every agent's snapshot, asked ONCE and bounded by
    the budget: the wizard's one `POST /v1/device-state`, sent at the start and
    read after the agents' own checks. A server that predates it
    (`unsupported`) is asked the old way -- `/v1/me` and each capture
    credential's status, all at once, as soon as the call says so -- once for
    every agent, never once per agent (`doctor.collect` alone would, each under
    the SDK's own timeouts). The state it resolves to carries a verdict for
    every agent holding a capture credential (`doctor.with_server_state`)."""

    def __init__(self, budget: _Budget, *, settings=None, reason: str | None = None) -> None:
        from probe.cli import capabilities
        from probe.cli import setup as wizard

        self._budget = budget
        self._settings = settings
        self._state = None
        self._request = None
        self._unasked = reason
        #: What the call itself answered (`checks.device_state`).
        self.reported = None
        if reason is not None:
            return
        try:
            self._request = capabilities.device_state_request(
                settings.base_url, settings.token, wizard.INSTALLABLE_AGENT_SOURCES
            )
        except Exception as exc:  # noqa: BLE001 - the status must render without it
            self._pending = capabilities.answered_already(
                capabilities.DeviceState(capabilities.DeviceStateOutcome.UNREACHABLE, error=str(exc))
            )
        else:
            # No manifest fallback: an older server's Versions row stays as
            # cached, rather than adding another request.
            self._pending = capabilities.start_device_state(self._request, deadline=budget.deadline)
        self._resolving = _start(self._resolve)

    def __call__(self):
        from probe.cli.capabilities import DeviceState, DeviceStateOutcome

        if self._state is None:
            if self._unasked is not None:
                self._state = DeviceState(DeviceStateOutcome.UNREACHABLE, error=self._unasked)
            else:
                state, error = _wait(self._resolving, self._budget, grace=_KILL_GRACE_S)
                self._state = state or DeviceState(DeviceStateOutcome.UNREACHABLE, error=error)
        return self._state

    def check(self) -> dict:
        from probe.cli.capabilities import DeviceStateOutcome

        if self._unasked is not None:
            return _check(error=self._unasked)
        state = self.reported
        if state is None:
            return _check(error=self._budget.timed_out())
        if state.outcome is DeviceStateOutcome.UNREACHABLE:
            return _check(state.outcome.value, error=state.error or "no answer")
        return _check(state.outcome.value, checked=True)

    def _resolve(self):
        from probe.cli.capabilities import DeviceStateOutcome

        state = self._pending()
        self.reported = state
        if state.outcome is DeviceStateOutcome.UNSUPPORTED:
            return self._the_old_way()
        if state.answered and self._request is not None and self._request.elsewhere:
            # Credentials paired to another server never rode in the call.
            return dataclasses.replace(state, capture={**state.capture, **self._capture(self._request.elsewhere)})
        return state

    def _the_old_way(self):
        from probe.cli import capabilities, doctor
        from probe.cli import setup as wizard

        login = _start(functools.partial(doctor._check_login, self._settings))  # noqa: SLF001
        paired = [source for source in wizard.INSTALLABLE_AGENT_SOURCES if capabilities.capture_token_sources(source)]
        capture = self._capture(paired)
        answer, _ = _wait(login, self._budget)
        return capabilities.DeviceState(
            capabilities.DeviceStateOutcome.ANSWERED,
            account_email=(answer.logged_in_as or None) if answer is not None else None,
            account_valid=answer.api_credential_valid if answer is not None else None,
            capture=capture,
        )

    def _capture(self, sources) -> dict:
        from probe.cli import capabilities

        asked = {
            source: _start(functools.partial(capabilities.verify_capture_credential, source))
            for source in sources
        }
        return {source: _wait(future, self._budget)[0] for source, future in asked.items()}


class _TokenVerdict:
    """The API's verdict on the read token, asked at the start and read after
    the agents' own checks; recorded for `check_mcp` -- as the menu's
    `refresh_mcp_token_verdict` does -- only when it came in time."""

    def __init__(self, budget: _Budget, *, reason: str | None = None) -> None:
        from probe.cli import capabilities

        self._budget = budget
        self._unasked = reason
        # Read while the agents are: no verdict yet, whatever this process
        # recorded before. The answer is recorded once it is in (`resolve`).
        capabilities.record_mcp_token_verdict(None, None)
        self._token = None
        if reason is None:
            try:
                self._token = capabilities.cli_mcp_token()
            except Exception as exc:  # noqa: BLE001 - a status read never raises
                self._unasked = f"not asked: the read token could not be read ({type(exc).__name__})"
        self._pending = (
            _start(functools.partial(capabilities.ask_mcp_token_verdict, self._token)) if self._token else None
        )

    def resolve(self) -> dict:
        from probe.cli import capabilities

        if self._unasked is not None:
            return _check(error=self._unasked)
        if self._pending is None:
            capabilities.record_mcp_token_verdict(None, None)
            return _check(TokenCheck.NO_TOKEN)
        state, error = _wait(self._pending, self._budget)
        if state is None:
            capabilities.record_mcp_token_verdict(None, None)
            return _check(error=error)
        capabilities.record_mcp_token_verdict(self._token, state)
        if state == TokenCheck.UNREACHABLE:
            return _check(state, error="the API could not be reached")
        return _check(state, checked=True)


def _not_asked_yet():
    """The server's half while an agent's own checks run: asked once,
    afterwards, for every agent (`_Server`, `doctor.with_server_state`)."""
    from probe.cli.capabilities import DeviceState, DeviceStateOutcome

    return DeviceState(DeviceStateOutcome.UNREACHABLE, error="asked once for every agent")


def _collect(source: str, *, asked: bool, plugins=None) -> Any:
    """One agent's `Capabilities`: its own CLI asked (the wizard's
    `_collect_agent`, the server's half left for `_Server`) when `asked`, else
    the same collector reading files only."""
    from probe.cli import capabilities, doctor

    with capabilities.agent_target(source):
        if not asked:
            return doctor.collect(local=True)
        with doctor.device_state_scope(_not_asked_yet):
            return doctor.collect(plugins=plugins)


def _plugin_list(future: concurrent.futures.Future | None, budget: _Budget):
    """A plugin list asked on its own thread (`installed_plugins`). The call is
    bounded by the budget itself, so it is waited on a little past it."""
    from probe.cli.capabilities import PluginState

    if future is None:
        return None
    plugins, error = _wait(future, budget, grace=_KILL_GRACE_S)
    return plugins if plugins is not None else PluginState(verified=False, error=error)


def _with_token_verdict(source: str, caps):
    """The read-token verdict, which came in after the agents were read: an
    MCP sending a token the API refused needs a login (`check_mcp`)."""
    from probe.cli import capabilities
    from probe.cli.capabilities import McpCredential

    if caps is None or not capabilities.mcp_token_rejected():
        return caps
    with capabilities.agent_target(source):
        kind, check = capabilities.check_mcp(source, codex_auth=caps.mcp_authenticated)
    if check is not None and check.credential == McpCredential.REJECTED:
        return dataclasses.replace(caps, mcp_kind=kind, mcp_check=check)
    return caps


def _agent_row(source: str, caps, *, installed: bool, asked: bool, config_readable: bool) -> dict:
    from probe.cli import capabilities
    from probe.cli import setup as wizard
    from probe.sdk import session_marker

    row = {
        "agent": source,
        "label": wizard.agent_label(source),
        "installed": installed,
        "configured": None,
        "plugin_installed": None,
        "capture_on": None,
        "mcp_state": None,
        "mcp_detail": None,
        "recorder": session_marker.recorder(source) if source in wizard.RECORDER_SOURCES else None,
        "plugins": _check(),
    }
    if not config_readable:
        # Who records picks the plugin looked for, the config holds Claude
        # Code's capture credential and the read token: none of it is known.
        row.update(recorder=None, plugins=_check(PluginsState.UNVERIFIED, error=f"not read: {_CONFIG_UNREADABLE}"))
        return row
    if caps is None:
        return row
    row.update(
        configured=caps.agent_configured,
        plugin_installed=caps.tracking_plugin_installed,
        capture_on=caps.capture_on,
        mcp_state=str(caps.mcp_state),
        mcp_detail=caps.mcp_status(),
        plugins=_check(
            PluginsState.VERIFIED if caps.plugins_verified else PluginsState.UNVERIFIED,
            checked=bool(asked and source in capabilities.LOCAL_PLUGIN_RECORDS and caps.plugins_verified),
            error=caps.plugins_error,
        ),
    )
    return row


def _session_default(*, config_readable: bool) -> dict:
    """The menu's Defaults row (`setup.tracking_default_row`) as data. An
    environment override holds it whatever the config says."""
    from probe.cli import setup as wizard
    from probe.sdk import session_marker

    held = session_marker.state_env_override()
    override = None if held is None else session_marker.state_label(wizard.setting_state(held))
    if not config_readable and override is None:
        return {"state": None, "env_override": None}
    return {
        "state": session_marker.state_label(wizard.setting_state(session_marker.default_session_state())),
        "env_override": override,
    }


def _versions(caps) -> dict:
    from probe.cli import setup as wizard
    from probe.cli.versions import VersionStatus

    if caps is None:
        return {"status": VersionStatus.UNKNOWN.value, "manifest_age_s": None, "components": []}
    rows, verdict = wizard.version_verdict(caps)
    age = caps.version_manifest_age_s
    return {
        "status": str(verdict),
        "manifest_age_s": None if age is None else int(age),
        "components": [
            {"kind": row.kind, "installed": row.installed, "latest": row.latest, "status": str(row.status)}
            for row in rows
        ],
    }


def _daemon(caps, *, config_readable: bool) -> dict:
    """What `doctor._daemon_rows` prints that is known locally, as data."""
    from probe.cli import companion, doctor
    from probe.cli import setup as wizard

    return {
        # The daemon's key is a field of the config's context.
        "key_held": wizard.companion_token_held() if config_readable else None,
        "ai_libraries": None if caps is None else caps.daemon_ai_libraries,
        "model_tokens_today": companion.tokens_today(),
        "reader_tokens_today": doctor._reader_tokens_today(),  # noqa: SLF001 - doctor's own reader
        "recent_errors": doctor.daemon_error_lines(),
    }


def _autoupdate_error() -> str | None:
    """Why `autoupdate.json` cannot be read, when it exists and cannot: its
    reader then answers "off" (`autoupdate.load`), as the menu shows it."""
    from probe.cli import autoupdate

    path = autoupdate.state_path()
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except (OSError, ValueError) as exc:
        return f"{path} could not be read ({exc})"
    return None if isinstance(loaded, dict) else f"{path} is not a JSON object"


def snapshot(*, refresh: bool = False, timeout: float = DEFAULT_TIMEOUT_S) -> dict:
    """The status object (SCHEMA above). Never raises for a state it finds.
    With `refresh`, everything it asks shares ONE budget of `timeout` seconds."""
    from probe.cli import claude_cli

    if not refresh:
        return _snapshot(None)
    budget = _Budget.starting(timeout)
    with claude_cli.bounded(timeout):
        return _snapshot(budget)


def _snapshot(budget: _Budget | None) -> dict:
    from probe.cli import capabilities, doctor, plugin_cli, wizard_lock
    from probe.cli import setup as wizard
    from probe.harness import get_registry
    from probe.sdk.config import ConfigUnreadable, current_context_name, load_file, resolve

    refresh = budget is not None
    errors: list[dict] = []
    config_readable = True
    try:
        # The strict read writers use: a reader's `{}` for a corrupt file is
        # exactly the "fresh device" this must never silently report.
        load_file(strict=True)
    except ConfigUnreadable as exc:
        config_readable = False
        errors.append(_error("config", str(exc)))
    try:
        settings = resolve()
    except Exception as exc:  # noqa: BLE001 - a status read never raises
        settings = None
        errors.append(_error("account", f"{type(exc).__name__}: {exc}"))
    autoupdate_error = _autoupdate_error()
    if autoupdate_error is not None:
        errors.append(_error("auto_update", autoupdate_error))

    server = token = hooks = None
    plugin_lists: dict[str, concurrent.futures.Future] = {}
    if refresh:
        # Codex's own answer about Probe's hooks, when it is due (`codex_hooks`
        # in the SCHEMA), inside the same budget.
        hooks = _start(_codex_hooks)
        # Everything that waits starts now and is read after the agents: the
        # server's call, the token check, and every agent's plugin list at once.
        unasked = None if config_readable else f"not asked: {_CONFIG_UNREADABLE}"
        server = _Server(
            budget,
            settings=settings,
            reason=unasked or (None if settings is not None else "not asked: the account could not be resolved"),
        )
        token = _TokenVerdict(budget, reason=unasked)
        plugin_lists = {
            source: _start(functools.partial(capabilities.installed_plugins, source=source))
            for source in capabilities.LOCAL_PLUGIN_RECORDS
            if plugin_cli.available(source)
        }

    # With --refresh, pi's `--help` sniff runs here, alongside the lists.
    detected = wizard.detectable_sources(sniff=refresh)
    caps_by_source: dict[str, Any] = {}
    asked_sources: set[str] = set()
    for source in wizard.INSTALLABLE_AGENT_SOURCES:
        # An agent not on this machine has no CLI to ask: its files are all
        # there is, as in the default read.
        asked = refresh and source in detected
        try:
            caps = _collect(
                source, asked=asked, plugins=_plugin_list(plugin_lists.get(source), budget) if asked else None
            )
        except Exception as exc:  # noqa: BLE001 - one agent's failure is that agent's row
            errors.append(_error(f"agents.{source}", f"{type(exc).__name__}: {exc}"))
            continue
        caps_by_source[source] = caps
        if asked:
            asked_sources.add(source)
        elif source in detected and caps.plugins_error:
            # Its binary is here, so the error is its unreadable record.
            errors.append(_error(f"agents.{source}.plugin_installed", caps.plugins_error))

    checks = {"device_state": _check(), "mcp_token": _check()}
    email = credential_valid = None
    if refresh:
        state = server()
        checks["device_state"] = server.check()
        checks["mcp_token"] = token.resolve()
        has_token = bool(settings is not None and settings.token)
        base_url = None if settings is None else settings.base_url
        for source in asked_sources:
            caps_by_source[source] = doctor.with_server_state(
                caps_by_source[source], state, has_token=has_token, base_url=base_url
            )
        caps_by_source = {source: _with_token_verdict(source, caps) for source, caps in caps_by_source.items()}
        login = doctor._login_from_state(state, has_token=has_token, base_url=base_url)  # noqa: SLF001
        email, credential_valid = login.logged_in_as or None, login.api_credential_valid

    agents = [
        _agent_row(
            source,
            caps_by_source.get(source),
            installed=source in detected,
            asked=source in asked_sources,
            config_readable=config_readable,
        )
        for source in wizard.INSTALLABLE_AGENT_SOURCES
    ]

    # The device-wide rows come off ONE snapshot, as the menu takes them: its
    # first agent, the first one found here, else Claude Code.
    first = caps_by_source.get(next(iter(detected), get_registry().default)) or next(
        iter(caps_by_source.values()), None
    )
    if refresh and first is not None:
        # Graded after the server's answer, which refreshes the cached manifest.
        rows, age = doctor._version_comparison()  # noqa: SLF001
        first = dataclasses.replace(first, version_rows=rows, version_manifest_age_s=age)
    running = wizard_lock.running()
    if running is None:
        errors.append(_error("wizard_running", f"could not probe {wizard_lock.lock_path()}"))
    if hooks is None:
        codex = _codex_hooks()
    else:
        codex, late = _wait(hooks, budget, grace=_KILL_GRACE_S)
        if codex is None:
            from probe.cli import codex_hooks

            codex = codex_hooks.blank_snapshot(codex_hooks.HooksState.UNKNOWN)
            errors.append(_error("codex_hooks", late or "no answer"))
    try:
        context = current_context_name()
    except Exception:  # noqa: BLE001 - the reader falls back to the default
        context = "default"
    if config_readable:
        account = {
            "signed_in": bool(settings is not None and settings.token),
            "email": email,
            "context": context,
            "base_url": None if settings is None else settings.base_url,
            "credential_valid": credential_valid,
            "workspace_limit": (
                None if settings is None or settings.workspace_limit is None else settings.workspace_limit.as_json()
            ),
        }
    else:
        account = dict.fromkeys(("signed_in", "email", "context", "base_url", "credential_valid", "workspace_limit"))
    return {
        "v": SCHEMA_VERSION,
        "refreshed": refresh,
        "cli": {
            "version": first.cli_version if first is not None and first.cli_version else _cli_version(),
            "install_method": None if first is None or first.install_method is None else str(first.install_method),
        },
        "account": account,
        "agents": agents,
        "who_records": wizard.machine_recorder() if config_readable else None,
        "session_default": _session_default(config_readable=config_readable),
        "auto_update": {
            "enabled": bool(first is not None and first.auto_update_enabled),
            "last_attempt": None if first is None else first.last_update_attempt_summary,
        },
        "versions": _versions(first),
        "daemon": _daemon(first, config_readable=config_readable),
        "wizard_running": running,
        "codex_hooks": codex,
        "service": _service(),
        "checks": checks,
        "errors": errors,
    }


def _service() -> dict:
    """`service` (SCHEMA): the Probe service's own answer, bounded, never started."""
    from probe.cli import service_calls

    return service_calls.view()


def _codex_hooks() -> dict:
    """`codex_hooks` (SCHEMA): asks Codex at most once per its cache's TTL."""
    from probe.cli import codex_hooks

    return codex_hooks.status_snapshot()


def _cli_version() -> str:
    from probe.cli import versions

    return versions.cli_version()


def _limit_word(limit) -> str:
    if not isinstance(limit, dict):
        return "none (the whole team)"
    name = limit.get("name") or limit.get("slug") or limit.get("id") or "unknown"
    return f"{name} (team-wide items {'hidden' if limit.get('team_items') == 'hide' else 'shown'})"


def human_lines(state: dict) -> list[str]:
    """A few lines for a person; `--json` is the contract, `probe doctor` the detail."""

    def word(value) -> str:
        return "unknown" if value is None else ("yes" if value is True else "no" if value is False else str(value))

    account = state["account"]
    if account["signed_in"] is None:
        who = "unknown"
    else:
        who = account["email"] or ("signed in" if account["signed_in"] else "not signed in")
    lines = [
        f"Probe CLI          {state['cli']['version']} ({state['cli']['install_method'] or 'unknown install'})",
        f"Account            {who} · {word(account['context'])} · {word(account['base_url'])}",
        f"Who records        {word(state['who_records'])}",
        f"New sessions       {word(state['session_default']['state'])}"
        + (" (held by an environment variable)" if state["session_default"]["env_override"] else ""),
        f"Automatic updates  {'on' if state['auto_update']['enabled'] else 'off'}",
        f"Versions           {state['versions']['status']}",
        f"Setup running      {word(state['wizard_running'])}",
    ]
    if isinstance(account.get("workspace_limit"), dict):
        # Only when limited: the whole team is the default and says nothing new.
        lines.insert(2, f"Workspace limit    {_limit_word(account['workspace_limit'])}")
    if "service" in state:
        from probe.cli import service_calls

        lines.append(f"Probe service      {service_calls.summary(state['service'])}")
    found = [row for row in state["agents"] if row["installed"]]
    for row in found:
        lines.append(
            f"{row['label']:<18} plugin {word(row['plugin_installed'])}"
            f" · capture {'unknown' if row['capture_on'] is None else 'on' if row['capture_on'] else 'off'}"
            f" · MCP {row['mcp_state'] or 'unknown'}" + (f" · records: {row['recorder']}" if row["recorder"] else "")
        )
    if not found:
        lines.append("Coding agents      none found on this device")
    from probe.cli import codex_hooks

    hooks = codex_hooks.status_line(state.get("codex_hooks"))
    if hooks:
        lines.append(f"Codex hooks        {hooks}")
    lines.extend(f"! {error['field']}: {error['message']}" for error in state["errors"])
    return lines
