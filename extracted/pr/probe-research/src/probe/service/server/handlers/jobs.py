"""desktop.request, statusline.refresh, notes.sync, import.start."""

from __future__ import annotations

import asyncio
import contextlib
import os

from ....foundation.service_api import paths
from ...jobs.imports import valid_job_id
from ...jobs.imports import prepare as prepare_import
from ...actions.management import CALLER_PID_ENV, CALLER_START_ENV
from ...jobs.notesync import MAX_AGENTS as MAX_NOTE_AGENTS
from ....foundation.service_api.vocabularies import (
    Action,
    BusyHolder,
    NOTES_MODES,
    RefusedReason,
    ORIGIN_DESKTOP)
from ....foundation.service_api.env import MAX_HOOK_PATH
from ....foundation.service_api.wire import (
    ErrorCode,
    RpcError,
    invalid_params)
from ....foundation.service_api.params import (
    is_agent_id,
    need_bool,
    need_choice,
    need_env,
    need_int,
    need_path,
    need_sid)
from probe.service.server.connections.connections import Connection
from probe.service.server.policy import log


class JobHandlersMixin:
    """Part of Service: its methods run with `self` the Service; compose() folds them into Service."""
    async def _desktop_request(self, conn: Connection, params: dict) -> dict:
        """`desktop.request` (plan Q6): one of the desktop app's management
        requests, answered as `probe desktop request --json` answers it, by a
        child running the same code (`management.py`). Never for a caller in a
        sandbox (the child reads this user's credentials, with the context it
        chose), nor from a caller that has exited or runs inside a session the
        daemon records (D9: `probe desktop` is refused there too, reads
        included); and no child starts while an update replaces the CLI's
        files under it (`busy`, holder `update`), checked again right before
        it starts."""
        request = params.get("request")
        op = request.get("op") if isinstance(request, dict) else None
        if not isinstance(op, str) or not op or len(op) > 64:
            raise invalid_params('request must be a desktop management request: {"op": ..., ...}')
        origin = params.get("origin")
        if origin is not None and origin != ORIGIN_DESKTOP:
            raise invalid_params(f"origin must be {ORIGIN_DESKTOP} when supplied")
        env = self._context(params)
        await self._refuse_sandboxed(conn)
        self._refuse_gone_caller(conn)
        seen = await asyncio.to_thread(self._caller_seen, conn)
        _inside, daemon = self._caller_session(conn, env, seen)
        if daemon is not None:
            log(f"refused desktop {op!r} from inside session {daemon}, which the Probe daemon records")
            raise RpcError(
                ErrorCode.REFUSED,
                "refused: the Probe app's requests cannot come from inside a coding agent's session the Probe "
                "daemon records; use the Probe app or your own terminal",
                {"reason": RefusedReason.DAEMON_SESSION, "sid": daemon},
            )

        # The caller's own session, registered or not, is resolved by the child
        # from the caller's process (its environment, a harness-process marker
        # above it), as its own `probe` would (`probe.core.run._desktop_refusal`).
        if conn.peer_pid is not None:
            env[CALLER_PID_ENV] = str(conn.peer_pid)
            env[CALLER_START_ENV] = conn.peer_start or ""
        self._desktop_may_start()
        try:
            return await self.management.request(
                request, env, human=origin == ORIGIN_DESKTOP, may_start=self._desktop_may_start
            )
        finally:
            # Answered: what holds the service may have changed.
            self.reevaluate()

    def _desktop_may_start(self) -> None:
        """`busy` while the CLI's files are being replaced under a new child:
        the update cycle applying in place, or a person's Update (`action.run
        update`, which raises no barrier of its own)."""
        if self.updater.applying:
            raise RpcError(
                ErrorCode.BUSY,
                "busy: an update is replacing the Probe CLI",
                {"holder": {"kind": BusyHolder.UPDATE, "cycle_id": self.updater.cycle_id}},
            )
        running = self.actions.running
        if running is not None and running.action == Action.UPDATE:
            raise RpcError(
                ErrorCode.BUSY,
                "busy: an update is replacing the Probe CLI",
                {"holder": self.actions.busy_holder()},
            )

    async def _statusline_refresh(self, conn: Connection, params: dict) -> dict:
        """`statusline.refresh`: refresh `sid`'s status-line marker with the
        folder's next fetch child (`statusline.py`); `{scheduled: true,
        due_in}`, else `{scheduled: false, reason}` and the hook fetches
        itself. `plugin_root` must be a Probe plugin folder of this user's
        with the refresh script; `python` the hook's interpreter (a 3.9 or
        newer, else the service PATH's `python3`); `agent` the session's
        harness id, for its capture reading."""
        sid = need_sid(params)
        agent = params.get("agent")
        if agent is not None and not is_agent_id(agent):
            raise invalid_params("agent must be a harness id")
        raw = need_path(params, "plugin_root")
        asked = params.get("python")
        if asked is not None and (not isinstance(asked, str) or not asked.startswith("/") or len(asked) > MAX_HOOK_PATH):
            raise invalid_params("python must be an absolute path")
        env = self._context(params)
        await self._refuse_sandboxed(conn)

        def check() -> tuple:
            root = os.path.realpath(raw)
            verdict = self.statusline.check(root)
            if verdict is None:
                # A status line installed where no update follow-up looked
                # (another CLAUDE_CONFIG_DIR) redraws when idle too.
                with contextlib.suppress(Exception):
                    self._refresh_interval({"HOME": str(paths.home()), **env})
            return root, verdict, (None if verdict else self.hookhosts.python_for(asked))

        root, verdict, python = await asyncio.to_thread(check)
        if verdict is not None:
            return {"scheduled": False, "reason": verdict}
        if python is None:
            return {"scheduled": False, "reason": "no python 3.9 or newer"}
        return self.statusline.request(root, python, env, sid, agent)

    async def _notes_sync(self, conn: Connection, params: dict) -> dict:
        """`notes.sync`: the team note's sync for the caller's context, once
        per machine and debounced (`notesync.py`). `mode` push | reconcile;
        `rules_for` the `PROBE_AGENT` values whose `probe agent-rules refresh`
        runs first ("" = the CLI's own default); `feedback` a `probe feedback
        flush` after. `{outcome: scheduled | queued}`, else `{outcome: null,
        reason}` and the hook spawns its own."""
        mode = need_choice(params, "mode", NOTES_MODES)
        rules_for = params.get("rules_for", [])
        if (
            not isinstance(rules_for, list)
            or len(rules_for) > MAX_NOTE_AGENTS
            or not all(agent == "" or is_agent_id(agent) for agent in rules_for)
        ):
            raise invalid_params(f"rules_for must be a list of at most {MAX_NOTE_AGENTS} harness ids (or \"\")")
        feedback = need_bool(params, "feedback")
        env = self._context(params)
        await self._refuse_sandboxed(conn)
        return self.notes.request(env, mode, rules_for, feedback)

    async def _import_start(self, conn: Connection, params: dict) -> dict:
        """`import.start`: start an approved import's worker (`imports.py`)
        with the CLI's own environment (`env`, required), and watch it.
        `{started: true, pid, start_time}`, else `{started: false, reason}`:
        `running` (this service runs it: `pid`, `start_time`), `not_a_job`
        (`detail`), `too_many`, `stopping`, `could_not_start: ...`."""
        job_id = params.get("job_id")
        if not valid_job_id(job_id):
            raise invalid_params("job_id must be an import job id (32 hex digits)")
        directory = need_path(params, "directory")
        attempt = need_int(params, "attempt")
        env = need_env(params)
        if not env:
            raise invalid_params("env is required: the worker runs with the CLI's own environment")
        await self._refuse_sandboxed(conn)
        # The folder's real path names the job (with its id): checked, and
        # its log opened, on a thread; `start` re-checks what runs after it.
        fd, directory, why = await asyncio.to_thread(prepare_import, job_id, directory)
        if fd is None:
            return {"started": False, "reason": "not_a_job", "detail": why}
        worker = self.imports.start(job_id, directory, attempt, env, fd)
        if isinstance(worker, dict):
            return worker
        from ....foundation.service_api import procid

        start = await asyncio.to_thread(procid.start_time, worker.pid)  # `ps` on macOS
        return self.imports.started(worker, start or "")
