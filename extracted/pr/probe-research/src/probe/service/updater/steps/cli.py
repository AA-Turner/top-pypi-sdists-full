"""UpdateStep for the CLI env and plugins: on a quiet machine, the barrier, a second look, the update child."""

from __future__ import annotations

import asyncio
import contextlib
import secrets
import time

from ..quiet import barrier
from ...actions import children, loginenv
from ....foundation.service_api import paths
from ....foundation.service_api.vocabularies import (
    DeferReason,
    StepState,
    REPORT_FOR_CHECK,
    Topic,
    UpdateStep)
from probe.service.updater.install_switch import side_by_side
from probe.service.updater.settings import (
    BARRIER_SETTLE_S,
    CHILD_FORCED,
    FORCED_ENV,
    HOLD_S,
    INCOMPLETE_DETAIL,
    MAX_LOG_BYTES,
    SIDE_BY_SIDE_ENV,
    SKIP_CLI_ENV,
    TRIGGER_ENV,
    UPDATE_LOG_NAME,
    WIZARD_BUSY_EXIT,
    log,
)


class CliStepMixin:
    """Part of Updater: its methods run with `self` the Updater; compose() folds them into Updater."""

    async def _core(self, cycle_id: str, trigger: str) -> dict:
        """Step 1: the CLI's env and the plugins, on a quiet machine only."""
        previous = await self._stop_previous(cycle_id)
        out = await self._core_step(cycle_id, trigger)
        if previous is not None:
            out["stopped_previous"] = previous
        return out

    async def _core_step(self, cycle_id: str, trigger: str) -> dict:
        step = UpdateStep.CLI_AND_PLUGINS
        busy = await self._look_off_loop()
        # `uv tool dir` is a child process: off the loop.
        self.beside = await asyncio.to_thread(side_by_side)
        if self.beside:
            # Nothing a run or a worker runs from is replaced (D6): they keep
            # their version (one finishing an ended session's queue too), and
            # live sessions' workers move after the switch (`_cycle`).
            busy.run = False
            busy.workers = [] if busy.workers is not None else None
            busy.unseen_daemon = False
            # Nor the files a waiting wizard menu runs from (C1): only its
            # lock, held while an action writes, holds a switch off.
            busy.menu = False
        reasons = busy.reasons()
        forced = self._forced(reasons)
        if forced is None:
            first = next(r for r in reasons if not self._past_limit(r))
            return self._defer(cycle_id, first, reasons)
        token = secrets.token_hex(16)
        held = False
        skip_cli = False
        login: dict | None = None
        # Only live sessions' workers are ever asked to stop: one finishing an
        # ended session's queue is waited for (`reasons`), or, past the limit,
        # updated around as before D7.
        # (A worker that cannot be asked, with no pid, is in `reasons`: waited
        # for as before D7, at most DEFER_LIMIT_S.)
        running = [w for w in busy.workers or [] if not w.draining and w.pid is not None]
        daemon = DeferReason.DAEMON_RECORDING
        try:
            if running:
                # The login shell's PATH and settings (D11, D14), for the manifest
                # read and the update child, never stored. Before the barrier: a
                # profile that runs `probe` would wait on it.
                login = await loginenv.child_env(vars=True)
                newer = await self._cli_behind(login)
                if newer is False:
                    # Nothing new for the CLI env the workers run from: leave
                    # them be and update the plugins only (D7).
                    skip_cli = True
                elif newer is None and not self._past_limit(daemon):
                    # Not known whether stopping them would buy anything: wait
                    # (at most DEFER_LIMIT_S), never stop them for nothing.
                    return self._defer(cycle_id, daemon, reasons + [daemon])
                else:
                    try:
                        barrier.hold_workers(token)
                        held = True
                    except OSError as exc:
                        log(f"cannot hold new daemon workers: {exc}")
                        if not self._past_limit(daemon):
                            return self._defer(cycle_id, daemon, reasons + [daemon])
                        forced.append(daemon)
                    if held:
                        self._step(cycle_id, step, StepState.STARTED, stopping_workers=len(running))
                        # A person's action is not refused as busy while the
                        # workers finish their rounds: the slot is the update's
                        # again only once they are gone.
                        self.slot = False
                        self._loop.call_soon(self.changed)  # what waits for the slot may start now
                        left = await self._stop_workers(running)
                        self.slot = True
                        if left:
                            log(f"{len(left)} daemon worker(s) did not hand over within {self.worker_stop_s:.0f} s")
                            if not self._past_limit(daemon):
                                return self._defer(cycle_id, daemon, reasons + [daemon])
                            forced.append(daemon)
                        if self.action_running():
                            # One of a person's actions started meanwhile.
                            action = DeferReason.ACTION_RUNNING
                            return self._defer(cycle_id, action, reasons + [action])
            if login is None:
                login = await loginenv.child_env(vars=True)
            return await self._apply(cycle_id, trigger, token, forced, login, skip_cli, held)
        finally:
            if held:
                barrier.release_workers(token)

    async def _apply(
        self, cycle_id: str, trigger: str, token: str, forced: list, login: dict, skip_cli: bool, held: bool
    ) -> dict:
        """The barrier, the second look, and the update child."""
        step = UpdateStep.CLI_AND_PLUGINS
        # Side by side (D6) or plugins only: nothing a `probe` runs from is
        # replaced, so the barrier holds no start back (plan C6).
        replaces_cli = not (self.beside or skip_cli)
        try:
            barrier.raise_barrier(token, replaces_cli=replaces_cli)
        except OSError as exc:
            self._step(cycle_id, step, StepState.FAILED, detail=f"cannot raise the update barrier: {exc}")
            return {"state": StepState.FAILED, "detail": f"cannot raise the update barrier: {exc}"}
        child: list = []

        def started(process) -> None:
            # From here the barrier is the update child's: it stays up while the
            # child runs even if this service stops under it (a signal, the end
            # of its hold), and goes stale once the child is gone.
            child.append(process)
            # Held while it runs, however long it may (plan B2): a cycle the
            # keeper asked for has no session to keep the service up, and a
            # service stopped idle under its child left the update to finish
            # with nothing watching its time limit.
            self._hold(self._hold_for_child())
            with contextlib.suppress(OSError):
                barrier.raise_barrier(token, pid=process.pid, replaces_cli=replaces_cli)

        lower = True
        try:
            await asyncio.sleep(BARRIER_SETTLE_S)
            again = await self._look_off_loop()
            if self.beside:
                again.run, again.unseen_daemon, again.menu = False, False, False
                again.workers = [] if again.workers is not None else None
            seen = again.reasons()
            if not (skip_cli or held) and any(not w.draining for w in again.workers or []):
                # A live session's worker started after the first look (none ran
                # then, so none was asked to stop): not under it.
                seen.append(DeferReason.DAEMON_RECORDING)
            for reason in seen:
                if reason not in forced and not self._past_limit(reason):
                    # Something new since the first look (a run just started, a
                    # setup took wizard.lock): never updated under, unless it too
                    # has deferred for DEFER_LIMIT_S.
                    return self._defer(cycle_id, reason, seen)
            forced = sorted(set(forced) | set(seen))
            label = ",".join(forced)
            if forced:
                since = min((self._deferred_since(r) or time.time()) for r in forced)
                hours = (time.time() - since) / 3600
                log(f"updating although {label} (deferred {hours:.1f} h, past the {self.defer_limit_s / 3600:.0f} h limit)")
            self._step(cycle_id, step, StepState.STARTED, **({"forced": label} if forced else {}))
            told = [reason for reason in CHILD_FORCED if reason in forced]
            done: dict = {}

            def on_event(event: dict) -> None:
                if event.get("event") == "done":
                    done.update(event)
                self.emit(Topic.UPDATE_STEP, {"cycle_id": cycle_id, "step": step, "event": event})

            log_path = paths.service_dir() / UPDATE_LOG_NAME
            with contextlib.suppress(OSError):
                if log_path.stat().st_size > MAX_LOG_BYTES:
                    log_path.unlink()
            # From the last look to the child's start nothing here awaits, so no
            # hold is admitted in between; from now on `run.hold` refuses one
            # (an in-place update would replace what that run imports from).
            self.applying = not self.beside
            started_at = time.time()
            overran: children.Overran | None = None
            try:
                code = await children.run_events(
                    "update",
                    {},
                    env_extra={
                        **login,
                        TRIGGER_ENV: REPORT_FOR_CHECK.get(trigger, "cli"),
                        barrier.TOKEN_ENV: token,
                        # Only a run past its own limit lets the child skip its
                        # run check: a run that just started never is (D33).
                        # Likewise a setup holding wizard.lock (C1).
                        **({FORCED_ENV: ",".join(told)} if told else {}),
                        **({SKIP_CLI_ENV: "1"} if skip_cli else {}),
                        **({SIDE_BY_SIDE_ENV: "1"} if self.beside else {}),
                    },
                    on_event=on_event,
                    on_start=started,
                    log_path=log_path,
                    # Past it the child is stopped (its group: SIGTERM, then
                    # SIGKILL past the grace) and this step fails, so the next
                    # cycle can run (UPDATE_TIMEOUT_S).
                    timeout=self.update_timeout_s,
                    grace=self.update_stop_grace_s,
                )
            except children.Overran as exc:
                overran = exc
            except OSError as exc:
                self._step(cycle_id, step, StepState.FAILED, detail=f"the update could not start: {exc}")
                return {"state": StepState.FAILED, "detail": f"the update could not start: {exc}"}
            except asyncio.CancelledError:
                # The service stops while the update still runs: the barrier stays
                # (it names the child), and the next service finds the child's
                # wizard.lock and defers -- until the child is past the time
                # limit, when the next service stops it (`overrun_update`).
                lower = not child or child[0].poll() is not None
                raise
            # The child is done: the rest of the cycle (the app's step, the
            # version read) holds the service HOLD_S, as before the child.
            self._hold(HOLD_S)
        finally:
            self.applying = False
            if lower:
                barrier.lower(token)
        if overran is not None:
            return await self._overran(cycle_id, overran, done, started_at, forced=label if forced else None)
        code = 128 - code if code < 0 else code
        outcome = {"exit_code": code, "ok": done.get("ok"), "complete": done.get("complete")}
        if forced:
            outcome["forced"] = label
        if skip_cli:
            outcome["cli"] = "left as it is: daemon workers run from it"
        if code == WIZARD_BUSY_EXIT:
            # The child found a setup holding wizard.lock and recorded the skip itself.
            self._step(cycle_id, step, StepState.DEFERRED, reason=DeferReason.SETUP_RUNNING, exit_code=code)
            return {"state": StepState.DEFERRED, "reason": DeferReason.SETUP_RUNNING, **outcome}
        # A child that wrote no `done` (killed before its first event, say) did
        # not finish: failed, whatever its exit status. Nor did one that says
        # `complete: false` (a step it failed or skipped: a CLI install that
        # left nothing while the plugins moved), though it exits 0: read as
        # done, every surface said `(ok)` and the next try was six hours off.
        finished = code == 0 and done and done.get("ok") is not False and done.get("complete") is not False
        state = StepState.DONE if finished else StepState.FAILED
        if not finished and code == 0 and done and done.get("ok") is not False:
            outcome["detail"] = INCOMPLETE_DETAIL
        self._step(cycle_id, step, state, exit_code=code, ok=done.get("ok"), complete=done.get("complete"),
                   **({"detail": outcome["detail"]} if "detail" in outcome else {}))
        return {"state": state, **outcome}
