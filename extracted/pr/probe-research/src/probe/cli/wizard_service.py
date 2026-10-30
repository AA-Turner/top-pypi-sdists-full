"""A terminal `probe wizard`'s actions, run by the Probe service (plan Q4).

The desktop app makes its changes through the service's `action.run`: one
mutating slot for the machine, journaled (a lost connection reads the outcome
instead of running it twice), and an update that restarts the service onto
the new code once it lands. `probe wizard --action <a> --yes` does the same
where it can:

    routed       configure (with `--agent`), recorder (with `--who-records`),
                 logout and update, with `--yes`: as `action.run`'s
                 action and params (`probe.core.requests`), which the service's
                 child runs as exactly these flags (`probe.core.actions`)
    streamed     the run's own text as it is written (its log: what it would
                 have printed here, the browser approval's link and code
                 among it); the exit status is the run's
    queued       asked for while an update holds the service's slot: the
                 service runs it once that update lets go (`queued: true`),
                 and this says so before it waits
    Ctrl-C       during the browser approval: `action.cancel`, as SIGINT does
                 in-process; anywhere else the run may be writing, so it goes
                 on (a second Ctrl-C stops following it, never the run)
    in-process   everything else, and whenever the service does not take it:
                   - no service runs, or Windows (none does);
                   - the service would run another CLI's code (`same_cli`: a
                     checkout's, a project venv's, an ephemeral `npx` one);
                   - a credential in the environment (`PROBE_TOKEN`, ...),
                     which a request's context never carries, or a setting a
                     run reads from it (`PROBE_MCP_URL`, `PROBE_WORKSPACE`,
                     `PROBE_PROJECT`: `service_calls.wizard_stays_here`);
                   - a service that does not say its `action.run` refuses a
                     sandboxed caller (`caps` lacks `action.sandbox`: one from
                     before this, still running at the same interpreter path
                     after an in-place update), which would run it outside the
                     caller's sandbox;
                   - an older service or core that refuses the request
                     (invalid params), or no answer before it was sent (once
                     sent, it is the service's: asked again by its
                     client_request_id, never run here as well);
                   - busy (another action, or an Update while an update
                     runs): the in-process run says so itself, from the run
                     lock it cannot take;
                   - refused: from inside a session the Probe daemon records
                     (the in-process path's own checks decide, as before), or
                     from a sandbox (the change must land inside it);
                 and what the action protocol cannot carry: the menu and its
                 prompts (no `--yes`); `--json` (its reader wants this
                 process's event stream, and the desktop app falls back to it
                 when the service refuses: it must not route back there); a
                 website sign-in code; the sign-in flags (`--token`, ...);
                 `--folder`; `--uninstall`; a configure without `--agent`
                 (which agents a bare `--yes` picks is read from this
                 terminal's PATH); a recorder row read without `--who-records`.
"""

from __future__ import annotations

import os
import signal
import sys
import time
from dataclasses import dataclass, field

#: Waiting for `action.run`'s answer (it journals before it answers).
ACCEPT_TIMEOUT_S = 5.0
#: How often the run's events and log are read while it runs.
POLL_S = 0.15
#: A lost connection (the service restarting onto an update): how long to
#: look for a service that can say how the action ended.
RECONNECT_S = 20.0


@dataclass(frozen=True)
class Routed:
    """An `action.run` request a wizard invocation maps onto exactly."""

    action: str
    params: dict = field(default_factory=dict)
    #: `action.run`'s `trigger` (the update action only).
    trigger: str | None = None


def plan(
    *,
    action: str | None,
    yes: bool,
    json_output: bool,
    agents: tuple[str, ...] | None,
    tracking: bool | None,
    capture: bool | None,
    auto_update: bool | None,
    agent_rules: bool | None,
    reinstall: bool,
    who_records: str | None,
    folder: str | None,
    uninstall: bool,
    auth_code: object,
    sign_in_flags: bool,
    update_trigger: str | None = None,
) -> Routed | str:
    """The `action.run` request for this invocation, or why it runs in-process."""
    if json_output is True:
        return "--json: its reader reads this process's own event stream"
    if yes is not True:
        return "interactive: the menu and its prompts need this terminal"
    if isinstance(auth_code, str) or sign_in_flags:
        return "a sign-in code or sign-in flags"
    if folder is not None or uninstall is True:
        return "--folder / --uninstall"
    if who_records is not None:
        if action not in (None, "recorder"):
            # configure takes it only with a website sign-in code; anything
            # else is a usage error the in-process path reports.
            return f"--who-records with --action {action}"
        action = "recorder"
    if action == "configure":
        if not agents:
            return "configure without --agent: the agents are found on this terminal's PATH"
        params: dict = {"agents": list(agents)}
        capabilities = {"tracking": tracking, "capture": capture, "auto_update": auto_update,
                        "agent_rules": agent_rules}
        if reinstall is True:
            if any(value is not None for value in capabilities.values()):
                return "--reinstall with settings flags"
            params["reinstall"] = True
        else:
            params.update({name: value for name, value in capabilities.items() if value is not None})
        return Routed("configure", params)
    if reinstall is True:
        return "--reinstall goes with configure"
    if any(value is not None for value in (tracking, capture, auto_update, agent_rules)) or agents:
        return f"{action}: with configure's flags"
    if action == "recorder":
        if who_records not in ("agent", "daemon"):
            return "recorder without --who-records reads the current setting"
        return Routed("recorder", {"who_records": who_records})
    if action == "uninstall":
        # `probe uninstall` stops the service itself: never one of its actions.
        return "uninstall: it stops the Probe service, so it never runs there"
    if action == "logout":
        return Routed(action)
    if action == "update":
        from probe.service.protocol import REPORT_TRIGGERS

        return Routed("update", trigger=update_trigger if update_trigger in REPORT_TRIGGERS else None)
    return f"{action or 'the menu'}: not an action the service runs"


def run(routed: Routed) -> int | None:
    """Run `routed` on the service, its text streamed here: the run's exit
    status, or None when the service did not take it (run it in-process).
    Once it took it the action is the service's: never run again here."""
    from probe.cli import service_calls

    if os.name != "posix" or not service_calls._reachable() or not service_calls.same_cli():
        return None
    if service_calls.wizard_stays_here():
        return None
    import secrets

    from probe.service import client
    from probe.service.protocol import Client, Method

    request = {
        "action": routed.action,
        "params": routed.params,
        "client_request_id": "cli-" + secrets.token_hex(8),
        "context": service_calls.context(),
    }
    if routed.trigger is not None:
        request["trigger"] = routed.trigger
    version = service_calls._version()
    try:
        conn = client.Connection.open(ACCEPT_TIMEOUT_S)
    except OSError:
        return None  # nothing sent: no service answers
    try:
        hello = conn.hello(Client.CLI, version)
    except (OSError, ValueError, client.ServiceError):
        _close(conn)
        return None  # nothing sent but the hello
    if not _enforces_sandbox(hello):
        # A service from before `caps` (the previous one, still running at the
        # same interpreter path after an in-place update): its `action.run`
        # checks no sandbox, so the action would land outside this caller's.
        _close(conn)
        return None
    deadline = time.monotonic() + RECONNECT_S
    resent = False
    while True:
        try:
            answer = conn.call(Method.ACTION_RUN, request)
            break
        except client.ServiceError:
            _close(conn)
            if not resent:
                # Refused on the first answer: busy, refused (a sandbox, a
                # daemon-recorded session), or params an older service or core
                # refuses. Never journaled, so it runs here.
                return None
            # A refusal of the RESEND says nothing about the first send (an
            # older service checks the caller before it looks the id up).
            return _unconfirmed()
        except (OSError, ValueError):
            # Sent, and no answer: it may have been accepted. Ask again with
            # the same client_request_id (it returns the action it accepted)
            # until a service answers, never run it here meanwhile.
            _close(conn)
            resent = True
            conn = _reopen(version, deadline)
            if conn is None:
                return _unconfirmed()
    action_id = answer.get("action_id") if isinstance(answer, dict) else None
    if not isinstance(action_id, str) or not action_id:
        _close(conn)
        return None
    try:
        return _Follower(conn, action_id, version, queued=answer.get("queued") is True).follow()
    finally:
        _close(conn)


def _enforces_sandbox(hello: object) -> bool:
    """Does the service that answered `hello` refuse a sandboxed `action.run`
    (`protocol.Cap.ACTION_SANDBOX`)? A service from before `caps` does not."""
    from probe.service.protocol import Cap

    caps = hello.get("caps") if isinstance(hello, dict) else None
    return isinstance(caps, list) and Cap.ACTION_SANDBOX in caps


def _unconfirmed() -> int:
    print(
        "probe wizard: the Probe service did not confirm it took this; it may still run it. "
        "`probe status` and `probe doctor` show what happened.",
        file=sys.stderr, flush=True,
    )
    return 1


def _reopen(version: str, deadline: float):
    """A connection (hello done) to a service that answers by `deadline` and
    enforces the sandbox on `action.run` (never resend to one that does not),
    or None. Its calls wait ACCEPT_TIMEOUT_S, as the first send did."""
    from probe.service import client
    from probe.service.protocol import Client

    while time.monotonic() < deadline:
        conn = None
        try:
            conn = client.Connection.open(ACCEPT_TIMEOUT_S)
            if _enforces_sandbox(conn.hello(Client.CLI, version)):
                return conn
            _close(conn)
        except (OSError, ValueError, client.ServiceError):
            _close(conn)
        time.sleep(0.5)
    return None


def _close(conn) -> None:
    if conn is not None:
        conn.close()


class _Follower:
    """Reads one action's events (for its end and the approval wait) and its
    log (for the text), until it is done."""

    def __init__(self, conn, action_id: str, version: str, queued: bool = False) -> None:
        from probe.service import paths

        self.conn = conn
        #: It waits for an update before it starts (`action.run` said `queued`).
        self.queued = queued
        self.action_id = action_id
        self.version = version
        # `<service dir>/actions/<id>.log` (`probe.service.actions`); a service
        # from before the machine key keeps it in the folder above.
        name = f"{action_id}.log"
        self.log_paths = [paths.actions_dir() / name, paths.root_dir() / paths.ACTIONS_DIRNAME / name]
        self.log_path = self.log_paths[0]
        self.offset = 0
        self.since = 0
        self.last_kind: str | None = None
        self.done: dict | None = None
        self.interrupts = 0
        self.told_writing = False
        #: The first Ctrl-C found it still waiting for the update.
        self.told_waiting = False
        #: The last `error` event: said when a run that wrote no log text fails.
        self.error: dict | None = None
        self.cancel_sent = False

    # -- the loop --------------------------------------------------------------

    def follow(self) -> int:
        previous = None
        if hasattr(signal, "SIGINT"):
            try:
                previous = signal.signal(signal.SIGINT, self._on_sigint)
            except ValueError:  # not the main thread: Ctrl-C keeps its default
                previous = None
        if self.queued:
            print("probe wizard: Probe is updating itself; this runs on the Probe service once that update "
                  "finishes.", file=sys.stderr, flush=True)
        try:
            while self.done is None:
                self._tail()
                if not self._read_events():
                    return self._lost()
                if self.done is not None:
                    break
                stop = self._handle_interrupts()
                if stop is not None:
                    return stop
                time.sleep(POLL_S)
            self._tail()
        finally:
            if previous is not None:
                signal.signal(signal.SIGINT, previous)
        if not self.done.get("ok") and not self.offset and self.error and self.error.get("message"):
            # It never wrote a word (it waited, then never started): say why.
            print(f"probe wizard: {self.error['message']}", file=sys.stderr, flush=True)
        code = self.done.get("exit_code")
        if isinstance(code, int) and not isinstance(code, bool):
            return code
        return 0 if self.done.get("ok") else 1

    def _on_sigint(self, _signum, _frame) -> None:
        self.interrupts += 1

    def _handle_interrupts(self) -> int | None:
        """Ctrl-C: cancel the browser approval it waits in, else say it goes
        on; a second one (outside the approval) stops following it."""
        if not self.interrupts:
            return None
        from probe.service.protocol import Method

        if self.last_kind == "device_prompt" and not self.cancel_sent:
            self.cancel_sent = True
            self.interrupts = 0
            try:
                self.conn.call(Method.ACTION_CANCEL, {"action_id": self.action_id})
            except Exception:  # noqa: BLE001 -- it ended meanwhile, or moved on: it says how
                pass
            return None
        if self.cancel_sent and self.last_kind == "device_prompt":
            # Asked to cancel already and still waiting: stop following.
            self.told_writing = True
        if not self.told_writing:
            self.told_writing = True
            self.interrupts = 0  # before the call below: a Ctrl-C during it still counts
            # Not started yet: it may never start without this command (its child
            # checks that the process that asked is still there), so promise nothing.
            self.told_waiting = self.queued and self._still_queued()
            if self.told_waiting:
                said = ("this waits for Probe's update to finish before it starts; press Ctrl-C again to stop "
                        "waiting (it may then not run)")
            else:
                said = ("the Probe service is applying this and it cannot be stopped while it writes; press "
                        "Ctrl-C again to stop following it (it carries on)")
            print(f"probe wizard: {said}.", file=sys.stderr, flush=True)
            return None
        if self.told_waiting:
            print(f"probe wizard: stopped waiting for {self.action_id}; it may still run once the update finishes.",
                  file=sys.stderr, flush=True)
        else:
            print("probe wizard: still running on the Probe service; `probe status` shows when it is done.",
                  file=sys.stderr, flush=True)
        return 130

    def _still_queued(self) -> bool:
        """Is the action still in the service's line for an update (`service.status`
        `actions.queued`)? `action.status` says `queued` until its child starts, a
        moment after it left the line too."""
        from probe.service.protocol import Method

        try:
            status = self.conn.call(Method.STATUS)
        except Exception:  # noqa: BLE001 -- unknown: say what holds for a running one
            return False
        actions = status.get("actions") if isinstance(status, dict) else None
        return isinstance(actions, dict) and self.action_id in (actions.get("queued") or [])

    # -- reading -----------------------------------------------------------------

    def _read_events(self) -> bool:
        """The events after `since`; False when no service can be asked."""
        from probe.service.protocol import Method

        for _ in range(2):
            try:
                page = self.conn.call(Method.ACTION_EVENTS, {"action_id": self.action_id, "since": self.since})
                break
            except Exception:  # noqa: BLE001 -- a lost connection (a restart), or a not_found
                if not self._reconnect():
                    return False
        else:
            return False
        if not isinstance(page, dict):
            return True
        for item in page.get("events") or []:
            if not isinstance(item, dict) or not isinstance(item.get("event"), dict):
                continue
            seq = item.get("seq")
            if isinstance(seq, int):
                self.since = max(self.since, seq)
            event = item["event"]
            self.last_kind = event.get("event") if isinstance(event.get("event"), str) else self.last_kind
            if self.last_kind == "error":
                self.error = event
            if self.last_kind == "done":
                self.done = event
        if page.get("done") and self.done is None:
            self.done = {"ok": False, "exit_code": None}
        return True

    def _reconnect(self) -> bool:
        """A new connection to a service that knows this action (the one that
        restarted onto an update reads its journal): within RECONNECT_S."""
        from probe.service import client
        from probe.service.protocol import Client

        _close(self.conn)
        deadline = time.monotonic() + RECONNECT_S
        ensured = False
        while time.monotonic() < deadline:
            try:
                conn = client.Connection.open(2.0)
                conn.hello(Client.CLI, self.version)
                self.conn = conn
                return True
            except (OSError, ValueError, client.ServiceError):
                if not ensured:
                    # The service stopped (an update's restart): the next one
                    # answers from the action's journal.
                    ensured = True
                    client.ensure()
                time.sleep(0.5)
        return False

    def _lost(self) -> int:
        self._tail()
        print(
            "probe wizard: lost the Probe service before the run finished; `probe status` and "
            "`probe doctor` show where it got to.",
            file=sys.stderr, flush=True,
        )
        return 1

    def _tail(self) -> None:
        """Copy what the run's log gained since the last look to stdout."""
        if not self.offset and not self.log_path.exists():
            self.log_path = next((p for p in self.log_paths if p.exists()), self.log_path)
        try:
            with open(self.log_path, "rb") as handle:
                handle.seek(self.offset)
                chunk = handle.read()
        except OSError:
            return
        if not chunk:
            return
        self.offset += len(chunk)
        out = getattr(sys.stdout, "buffer", None)
        try:
            if out is not None:
                sys.stdout.flush()
                out.write(chunk)
                out.flush()
            else:
                sys.stdout.write(chunk.decode("utf-8", "replace"))
                sys.stdout.flush()
        except (OSError, ValueError):
            pass
