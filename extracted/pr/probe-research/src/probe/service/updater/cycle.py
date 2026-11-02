"""one update cycle: run the UpdateSteps in order, defer with reasons, then restart this service onto a new CLI (with the guard)."""

from __future__ import annotations

import asyncio
import contextlib
import os
import sys
import time

from ..actions import children, loginenv
from ...foundation.service_api import paths
from ...foundation.service_api.vocabularies import (
    StepState,
    StopReason,
    Topic,
    UpdateStep)
from probe.service.updater.install_switch import _env_moved, _switched, runtime_follows_switch
from probe.service.updater.quiet.quiet import behind, record_skip
from probe.service.updater.settings import LIMITED, VERSION_TIMEOUT_S, _installs_closed_app, log


def preload() -> None:
    """Import, now, every module the rest of a cycle (and the service after
    it) would otherwise import later -- from files `uv tool upgrade` is about
    to replace (plan R2). The service exits after a cycle that changed its
    version, so nothing loads from the new files into the old process."""
    import calendar  # noqa: F401
    import plistlib  # noqa: F401
    if os.name != "nt":
        import fcntl  # noqa: F401
    import subprocess  # noqa: F401

    from .. import guard  # noqa: F401  -- the switch's guard; the update child's environment
    from ..actions import loginenv  # noqa: F401
    from probe.shared.updates import installs  # noqa: F401  -- side-by-side installs (D6)

    from probe.shared.updates import version_policy  # noqa: F401
    from probe.shared.updates import autoupdate  # noqa: F401
    from probe._shared import oscompat  # noqa: F401
    from probe.foundation.durable import run_lock  # noqa: F401
    from probe.core import requests  # noqa: F401  -- action.run checks its params with it
    from probe.foundation.harness_registry import harness_registry as registry  # noqa: F401  -- a request context's session variables

    from ..server.policy import session_env_names

    session_env_names()

    # The whole old client, as `guard`'s `from . import client` loaded it before agent:16.
    from ...foundation.service_api import calls, cli, procid, service_api, start  # noqa: F401

    if _installs_closed_app():
        from . import app as appinstall  # the closed app's install (step 2), and what it imports

        appinstall.preload()


class CycleMixin:
    """Part of Updater: its methods run with `self` the Updater; compose() folds them into Updater."""

    # -- the cycle ---------------------------------------------------------------

    def _step(self, cycle_id: str, step: str, state: str, **detail: object) -> None:
        self.step = step if state == StepState.STARTED else self.step
        self.emit(Topic.UPDATE_STEP, {"cycle_id": cycle_id, "step": step, "state": state, **detail})

    async def _cycle(self, cycle_id: str, trigger: str) -> None:
        log(f"cycle {cycle_id} started ({trigger})")
        self.emit(Topic.UPDATE_STARTED, {"cycle_id": cycle_id, "trigger": trigger})
        steps: dict = {}
        deferred: str | None = None
        restart = False
        try:
            preload()
            try:
                core = await self._core(cycle_id, trigger)
            finally:
                self.slot = False
                # The actions queued behind this step run now, while the later
                # steps do (on the loop: nothing they raise ends this cycle).
                self._loop.call_soon(self.changed)
            steps[UpdateStep.CLI_AND_PLUGINS] = core
            if core["state"] == StepState.DEFERRED:
                deferred = str(core["reason"])
                self.emit(Topic.UPDATE_DEFERRED, {"cycle_id": cycle_id, "reason": deferred, "trigger": trigger})
            steps[UpdateStep.APP] = await self._app(cycle_id, trigger)
            if core["state"] in (StepState.DONE, StepState.FAILED):
                steps[UpdateStep.SELF], restart = await self._self(cycle_id)
                if restart and (self.beside or await asyncio.to_thread(_switched)):
                    # Watched by the guard (D5), which moves live sessions'
                    # workers once the new version runs: a rejected one keeps
                    # them where they are. The first switch too (it waited for
                    # a quiet machine, so it was not `beside`).
                    to_version = steps[UpdateStep.SELF].get("to_version")
                    if isinstance(to_version, str):
                        self.guard_pending = to_version
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # noqa: BLE001 -- a bug costs this cycle, never the service
            log(f"cycle {cycle_id} failed: {exc!r}")
            steps["error"] = repr(exc)[:500]
        app = steps.get(UpdateStep.APP)
        record = self.state.get("app")
        if (
            isinstance(app, dict)
            and app.get("state") == StepState.DELEGATED
            and isinstance(record, dict)
            and record.get("state") != StepState.DELEGATED
            and record.get("delegated_at") == app.get("delegated_at")
        ):
            # The app reported while the cycle's later steps ran: its result is the step.
            steps[UpdateStep.APP] = self._app_step(record)
        ok = deferred is None and all(
            isinstance(s, dict) and s.get("state") != StepState.FAILED for s in steps.values()
        ) and "error" not in steps
        core_failed = isinstance(steps.get(UpdateStep.CLI_AND_PLUGINS), dict) \
            and steps[UpdateStep.CLI_AND_PLUGINS].get("state") == StepState.FAILED
        # Failed while the release manifest got no answer at all: the machine is
        # offline, which is no failure of the update's (`update_failed`).
        offline = not ok and deferred is None and core_failed and await self._offline()
        now = time.time()
        result = {"cycle_id": cycle_id, "at": now, "trigger": trigger, "ok": ok, "steps": steps, "restart": restart}
        if offline:
            result["offline"] = True
        if deferred is None:
            self.state["last_check"] = now
            self.state["last_result"] = result
            # What that check left installed: a later move BACK (`moved_back`)
            # makes the next check due at once.
            self_step = steps.get(UpdateStep.SELF)
            checked = self_step.get("to_version") if isinstance(self_step, dict) else None
            self.state["checked_cli"] = checked if isinstance(checked, str) and checked else self.installed_now()
            # Cycles in a row that ended not ok, online: the watch's `update_failed` (plan B2).
            streak = self.state.get("failed_in_a_row")
            streak = streak if isinstance(streak, int) else 0
            self.state["failed_in_a_row"] = 0 if ok else streak if offline else streak + 1
            self.state.pop("deferred_since", None)
            self.pending = None
        else:
            self.state["last_deferred"] = {"at": now, "reason": deferred, "trigger": trigger}
            # The streaks DEFER_LIMIT_S is counted from (D7, D33), per reason:
            # every reason this look saw goes on (or starts); one it did not see
            # has ended.
            core_step = steps.get(UpdateStep.CLI_AND_PLUGINS)
            seen = core_step.get("reasons") if isinstance(core_step, dict) else None
            seen = seen if isinstance(seen, list) else [deferred]
            streaks = self._streaks()
            self.state["deferred_since"] = {r: streaks.get(r, now) for r in seen if r in LIMITED}
            self.pending = trigger
            record_skip(deferred, trigger)
        core_step = steps.get(UpdateStep.CLI_AND_PLUGINS)
        installed = (
            isinstance(core_step, dict)
            and core_step.get("state") in (StepState.DONE, StepState.FAILED)
            and "exit_code" in core_step
        )
        if installed and restart:
            self.state["followup"] = {"at": now, "cycle_id": cycle_id}
        elif installed:
            self.state["followed_version"] = self.version  # followed up below, by this service
        self._save()
        self.cycle_id = None
        self.step = None
        self.emit(Topic.UPDATE_DONE, {**result, "deferred": deferred})
        log(f"cycle {cycle_id} done (ok {ok}, deferred {deferred}, restart {restart})")
        if installed:
            # The update child ran (a failed one may have moved the plugins
            # all the same): open sessions follow what it installed.
            try:
                self.followup(restart)
            except Exception as exc:  # noqa: BLE001 -- never costs the cycle
                log(f"cycle {cycle_id}: the follow-up failed: {exc!r}")
        self._arm()
        # `task` is still this one until it returns: clear the hold first.
        self.hold_until = 0.0
        self._loop.call_soon(self.changed)
        if restart:
            # The guard starts when this service really stops (`before_exit`),
            # which waits for a running action: started now, it would watch a
            # service still serving and read it as one that will not go.
            self._loop.call_soon(self.stop, StopReason.UPDATE)

    def before_exit(self, reason: str) -> None:
        """The service is stopping: after a switch (its own restart, or a stop
        for another reason before that came), start the switch's guard now (D5)."""
        if self.guard_pending:  # whatever stops it now, the next one is the new version
            to_version, self.guard_pending = self.guard_pending, None
            self._spawn_guard(to_version)

    def _defer(self, cycle_id: str, reason: str, reasons: list | None = None) -> dict:
        """A deferral, with every reason the look saw (each one's streak goes on)."""
        self._step(cycle_id, UpdateStep.CLI_AND_PLUGINS, StepState.DEFERRED, reason=reason)
        return {"state": StepState.DEFERRED, "reason": reason, "reasons": list(reasons or [reason])}

    async def _offline(self) -> bool:
        """Did the release manifest's read find no network at all just now (a
        name that did not resolve, no route: `probe.foundation.tls.network_down`), through
        the login shell's proxy? False when it answered anything, or when that
        cannot be told (an older CLI's read)."""
        try:
            login = await loginenv.child_env(vars=True)
            code, value = await children.run_read(
                "version", {"latest": True}, env_extra=login, timeout=VERSION_TIMEOUT_S
            )
        except Exception:  # noqa: BLE001 -- unknown: counted as before
            return False
        return code == 0 and isinstance(value, dict) and value.get("reachable") is False

    async def _cli_behind(self, login: dict) -> bool | None:
        """Is the installed CLI older than the newest release (the manifest
        itself, through the login shell's proxy)? None: unknown."""
        try:
            code, value = await children.run_read(
                "version", {"latest": True}, env_extra=login, timeout=VERSION_TIMEOUT_S
            )
        except OSError:
            return None
        if code != 0 or not isinstance(value, dict):
            return None
        return behind(value.get("cli_version"), value.get("cli_latest"))

    def after_update_action(self) -> None:
        """A person's Update (`action.run update`) ran outside a cycle: read
        the CLI version a fresh process imports and, when it moved, restart
        as a cycle's self step would. This service is old code then, and
        anything it imported later would come from the new files."""
        if self._loop is None:
            return
        task = self._loop.create_task(self._after_update_action())
        self._side_tasks.add(task)
        task.add_done_callback(self._side_tasks.discard)

    async def _after_update_action(self) -> None:
        try:
            code, value = await children.run_read("version", {}, timeout=VERSION_TIMEOUT_S)
        except OSError as exc:
            log(f"version check after the update action could not start: {exc}")
            return
        installed = value.get("cli_version") if isinstance(value, dict) else None
        if code == 0 and isinstance(installed, str) and installed:
            installed = await asyncio.to_thread(runtime_follows_switch, installed)  # None: no restart
        moved = code == 0 and isinstance(installed, str) and bool(installed) and (
            installed != self.version or await asyncio.to_thread(_env_moved))
        if moved:
            self.mark_followup(None)
        try:
            self.followup(moved)
        except Exception as exc:  # noqa: BLE001
            log(f"the follow-up of the update action failed: {exc!r}")
        if moved:
            log(f"the update action installed {installed} (this service is {self.version}): restarting")
            # Watched like a cycle's switch (D5) when it was one.
            with contextlib.suppress(Exception):
                from probe.shared.updates import installs

                if installs.active() is not None:
                    self.guard_pending = installed
            self.stop(StopReason.UPDATE)

    def _spawn_guard(self, to_version: str) -> None:
        """Before this service exits for `to_version`, start the guard (D5)
        from THIS version's interpreter: it starts the new service, watches it,
        and switches back when it will not run. The interpreter of the version
        it would return to: this one's version env, or after the first switch
        (this service still runs through the moved folder's old path) the
        moved folder itself (`probe.shared.updates.installs.installs.previous`). Never raises."""
        try:
            from probe.shared.updates import installs

            from ...foundation.service_api import procid

            python = sys.executable
            if not installs.running_from_versions(sys.prefix):
                prior = installs.previous()
                if prior is None:
                    log("no guard: no version to switch back to")
                    return
                python = str(installs.env_python(prior))
            to_env = installs.active()
            import subprocess

            log_fd = os.open(paths.log_path(), os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
            try:
                subprocess.Popen(  # noqa: S603 -- the previous version's interpreter, our own module
                    [python, "-I", "-m", "probe.service.guard", "--from", self.version,
                     "--to", to_version, "--old-python", python, "--old-pid", str(os.getpid()),
                     "--old-start", procid.start_time(os.getpid()) or "",
                     *(["--to-env", str(to_env)] if to_env is not None else [])],
                    stdin=subprocess.DEVNULL,
                    stdout=log_fd,
                    stderr=log_fd,
                    cwd=str(paths.service_dir()),
                    env=dict(os.environ),
                    start_new_session=True,
                    close_fds=True,
                )
            finally:
                os.close(log_fd)
            log(f"guard started for {to_version}")
        except Exception as exc:  # noqa: BLE001 -- the update stands; it is only unwatched
            log(f"could not start the guard: {exc!r}")

    async def _self(self, cycle_id: str) -> tuple[dict, bool]:
        """Step 3: did step 1 install a new CLI? Then this service is old code."""
        step = UpdateStep.SELF
        try:
            code, value = await children.run_read("version", {}, timeout=VERSION_TIMEOUT_S)
        except OSError as exc:
            code, value = None, None
            log(f"version check could not start: {exc}")
        installed = value.get("cli_version") if isinstance(value, dict) else None
        if code != 0 or not isinstance(installed, str) or not installed:
            self._step(cycle_id, step, StepState.FAILED, detail="could not read the installed CLI version")
            return {"state": StepState.FAILED, "detail": "could not read the installed CLI version"}, False
        followed = await asyncio.to_thread(runtime_follows_switch, installed)
        installed = followed or installed
        restart = followed is not None and (installed != self.version or await asyncio.to_thread(_env_moved))
        detail = {"from_version": self.version, "to_version": installed, "restart": restart}
        self._step(cycle_id, step, StepState.DONE, **detail)
        return {"state": StepState.DONE, **detail}, restart
