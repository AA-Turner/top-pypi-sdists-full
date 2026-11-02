"""action.run, update.check_now, daemon.host, recorders.finish, run.hold/release, manifest.refresh."""

from __future__ import annotations

import asyncio
import concurrent.futures

from ...actions import caller
from ...actions.management import CALLER_PID_ENV, CALLER_START_ENV
from ...sessions.runholds import Hold
from ....foundation.service_api.vocabularies import (
    Action,
    CHECK_TRIGGERS,
    RefusedReason,
    CheckTrigger,
    need_app_check)
from ....foundation.service_api.wire import (
    ErrorCode,
    RpcError,
    invalid_params)
from ....foundation.service_api.params import (
    need_owner,
    need_str,
    need_wait)
from ...updater.cycle import preload
from probe.service.server.connections.connections import Connection
from probe.service.server.policy import log


class RunHandlersMixin:
    """Part of Service: its methods run with `self` the Service; compose() folds them into Service."""

    async def _action_run(self, conn: Connection, params: dict) -> dict:
        """`action.run`: never for a caller in a sandbox (`Cap.ACTION_SANDBOX`),
        as every other method that runs work: the change would land outside
        it. The caller's own confinement decides, never the client kind its
        hello names (a label anyone can send); the desktop app, which is never
        sandboxed, is unaffected, and a refused CLI runs the action itself,
        inside its sandbox. A `client_request_id` this service accepted
        already gets its action before any check (`ActionManager.existing`;
        it starts nothing): a retry never reads as refused because something
        changed since (the endpoint it signed out of)."""
        known = self.actions.existing(params)
        if known is not None:
            return known
        env = self._context(params)
        self._refuse_gone_caller(conn)
        await self._refuse_sandboxed(conn)
        return self._action_run_now(conn, params, env)

    def _action_run_now(self, conn: Connection, params: dict, env: dict) -> dict:
        _inside, daemon = self._caller_session(conn, env)
        if daemon is not None:
            log(f"refused {params.get('action')!r} from inside session {daemon}, which the Probe daemon records")
            raise RpcError(
                ErrorCode.REFUSED,
                "refused: Probe's settings cannot be changed from inside a coding agent's session the "
                "Probe daemon records; run it from your own terminal or the Probe app",
                {"reason": RefusedReason.DAEMON_SESSION, "sid": daemon},
            )
        if conn.peer_pid is not None:
            # The child resolves the caller's own session from its process too
            # (its environment, a harness-process marker above it), registered
            # or not, as `desktop.request`'s does (#3360; `probe.core.run`).
            env[CALLER_PID_ENV] = str(conn.peer_pid)
            env[CALLER_START_ENV] = conn.peer_start or ""
        if params.get("action") == Action.UPDATE:
            # Before the files it imports from are replaced (R2), as a cycle does.
            try:
                preload()
            except Exception as exc:  # noqa: BLE001 -- a person's Update still runs
                log(f"preload before the update action failed: {exc!r}")
        return self.actions.run(params, env)

    def _check_now(self, conn: Connection, params: dict) -> dict:
        trigger = params.get("trigger", CheckTrigger.CLI)
        if trigger not in CHECK_TRIGGERS:
            raise invalid_params(f"trigger must be one of {sorted(CHECK_TRIGGERS)}")
        return self.updater.check_now(trigger, need_app_check(params, trigger))

    async def _daemon_host(self, conn: Connection, params: dict) -> dict:
        """`daemon.host`: where the daemon host listens, started if need be, for an
        old tap's `probe daemon worker` (the proxy, `probe.daemon.host.proxy`), which
        then runs its session there. Refused: no host here (off, Windows)."""
        await self._refuse_sandboxed(conn)
        host = self.workers.daemon_host
        if host is None or not host.available():
            raise RpcError(ErrorCode.REFUSED, "refused: no daemon host here", {"reason": "daemon_host_off"})
        try:
            # Its own small pool: proxies all ask at once after a restart, and a host
            # start can take START_TIMEOUT_S; the loop's shared executor serves every
            # other `to_thread` (the caller checks, the mailboxes).
            if self._host_pool is None:
                self._host_pool = concurrent.futures.ThreadPoolExecutor(max_workers=2, thread_name_prefix="daemon-host")
            return await asyncio.get_running_loop().run_in_executor(self._host_pool, host.address)
        except Exception as exc:  # noqa: BLE001 -- the proxy runs the worker itself
            raise RpcError(ErrorCode.REFUSED, f"refused: the daemon host is unavailable ({exc})",
                           {"reason": "daemon_host_unavailable"}) from None

    async def _recorders_finish(self, conn: Connection, params: dict) -> dict:
        """`recorders.finish` (`probe capture off` for one agent): every
        recorder of `harness` finishes, as `session.finish` does for one;
        `{finished: [sid], unfinished: [sid]}`, the second still finishing
        after `wait` seconds."""
        harness = need_str(params, "harness", max_len=64)
        wait = need_wait(params)
        await self._refuse_sandboxed(conn)
        sessions = self.registry.sessions

        def harness_of(sid: str) -> str | None:
            session = sessions.get(sid)
            return session.harness if session is not None else None

        answer = await self.recorders.finish_harness(harness, wait, harness_of)
        asked = len(answer["finished"]) + len(answer["unfinished"])
        if asked:
            # The stopper's side of the record (`probe.cli.capture.capture` journals the
            # `tap watch` processes it signals; these it asks here).
            log(
                f"recorders.finish: {asked} recorder(s) of {harness} asked to finish (caller pid "
                f"{conn.peer_pid}); {len(answer['unfinished'])} still finishing after {wait:g} s"
            )
        return answer

    async def _run_hold(self, conn: Connection, params: dict) -> dict:
        """`run.hold`: a `probe exec` holds `run` for as long as `owner` runs.
        `{held: true}`, else `{held: false, reason}` (`owner_gone`,
        `not_caller`, `too_many`, `updating`): its run lock still says it runs.
        Never for a caller in a sandbox (or one the kernel will not name): its
        hold would persist outside it and keep updates off."""
        run = need_str(params, "run", max_len=256)
        owner = need_owner(params)
        if owner is None:
            raise invalid_params("owner must be {pid, start_time}: a hold ends with its process")
        await self._refuse_sandboxed(conn)
        peer = conn.peer_pid

        def check() -> str | None:
            if self.runs.owner_alive(owner["pid"], owner["start_time"]) is False:
                return "owner_gone"
            # The caller holds for itself (or a process it runs under), never
            # for an unrelated one it could keep updates off for.
            if peer is not None and owner["pid"] != peer and (owner["pid"], owner["start_time"]) not in (
                caller.ancestry(peer)
            ):
                return "not_caller"
            return None

        # `ps` on macOS: off the loop.
        refused = await asyncio.to_thread(check)
        if refused is not None:
            return {"held": False, "reason": refused}
        if self.updater.applying:
            # The update's last look is behind it: it would never see this hold.
            return {"held": False, "reason": "updating"}
        hold, new = self.runs.add(run, owner)
        if hold is None:
            return {"held": False, "reason": "too_many"}
        if new:
            self._watch_hold(hold)
            log(f"run {run} held by pid {owner['pid']}")
            self.status_cache.invalidate()
        return {"held": True}

    async def _run_release(self, conn: Connection, params: dict) -> dict:
        """`run.release`: the caller's holds of `run` go from the listing (only
        `owner`'s, when named). `{released: n}`; releasing what is not held,
        or not the caller's, is not an error. Only a hold whose owner is the
        caller or a process it runs under is released, as `run.hold` admits
        it; never from a caller in a sandbox.

        Its process still holds updates off until it exits (`runs.releasing`,
        watched as the hold was): the releasing `probe exec` is still cleaning
        up, importing from the env an update replaces. The deferred update is
        retried at that exit, not now."""
        run = need_str(params, "run", max_len=256)
        owner = params.get("owner")
        pid = None
        if owner is not None:
            pid = owner.get("pid") if isinstance(owner, dict) else None
            if not isinstance(pid, int) or isinstance(pid, bool) or pid <= 1:
                raise invalid_params("owner must be {pid, start_time} or left out")
        await self._refuse_sandboxed(conn)
        chain = set(await asyncio.to_thread(caller.ancestry, conn.peer_pid))  # `ps` on macOS
        gone = self.runs.release(run, chain, pid)
        if gone:
            log(f"run {run} released (its process still holds updates off until it exits)")
            self.status_cache.invalidate()
        return {"released": len(gone)}

    def _watch_hold(self, hold: Hold) -> None:
        if self.watcher is None:
            return
        self.watcher.watch(hold.key, hold.owner["pid"], hold.owner["start_time"], lambda: self._hold_exited(hold))

    def _hold_exited(self, hold: Hold) -> None:
        if self.runs.drop(hold):
            log(f"run {hold.run}: its process {hold.owner['pid']} exited")
            self._run_gone()

    def _run_gone(self) -> None:
        """A run is over: a deferred update gets another try, as when a session ends."""
        self.status_cache.invalidate()
        self.updater.session_ended()

    async def _manifest_refresh(self, conn: Connection, params: dict) -> dict:
        """`manifest.refresh`: the CLI's cached release manifest, refreshed by
        a child with the request's context; `{outcome, done, result}`."""
        env = self._context(params)
        wait = need_wait(params)
        await self._refuse_sandboxed(conn)
        return await self.manifest.refresh(env, wait=wait)
