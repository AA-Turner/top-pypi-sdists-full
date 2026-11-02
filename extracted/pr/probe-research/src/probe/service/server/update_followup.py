"""after an update or a recorder change: run the follow-ups, move onto the newest tap, resume recorders."""

from __future__ import annotations

import asyncio
import contextlib
import time

from ...foundation.service_api import paths
from ..jobs.notesync import MAX_AGENTS as MAX_NOTE_AGENTS
from ..sessions.recorders.tap import SETTLE_S as TAP_SETTLE_S
from ...foundation.service_api.vocabularies import (
    StopReason,
    Mode)
from probe.service.server.policy import log
#: After an update, how many times the follow-up asks again about a newer tap
#: folder its agent may still be writing (`_follow_tap`), TAP_SETTLE_S apart.
FOLLOW_TAP_TRIES = 3
#: Claude Code config folders `_refresh_interval` looks at in one service process.
MAX_INTERVAL_FOLDERS = 64


class UpdateFollowupMixin:
    """Part of Service: its methods run with `self` the Service; compose() folds them into Service."""

    def _recorders_changed(self) -> None:
        self.status_cache.invalidate()
        self.hints.changed()
        self.reevaluate()

    def _imports_changed(self) -> None:
        """An import worker started or ended: one fewer is, for a deferred
        update, as a run's end is (`_run_gone`)."""
        count = len(self.imports.workers)
        fewer = count < self._import_count
        self._import_count = count
        self.status_cache.invalidate()
        if fewer:
            self.updater.session_ended()
        self.reevaluate()

    def _resume_recorders(self) -> None:
        if self.stop_reason is not None:
            return
        try:
            resumed = self.recorders.resume(self._register_saved)
        except Exception as exc:  # noqa: BLE001 -- capture falls back to `tap watch` on the next prompt
            log(f"recorder: resuming failed: {exc!r}")
            resumed = 0
        if resumed:
            log(f"recorder: {resumed} session(s) resumed")
            self.hints.changed()
        self.reevaluate()
        # The service before this one installed a new CLI and restarted onto it:
        # this one, the new code, follows the update up (its recorders resumed
        # on the newest installed tap already: `RecorderHost.resume`).
        with contextlib.suppress(Exception):
            if self.updater.take_followup():
                self._follow_update(tap=False)

    # -- after an update ------------------------------------------------------

    def _update_followup(self, restart: bool) -> None:
        """An update installed something (`Updater.followup`): what open
        sessions read follows it now (`followup.py`, plan C9). When this
        service restarts onto a new CLI first, it only wants the newest
        installed tap for the next one (`follow_installed`, saved); the next
        service does the rest (`take_followup`). Else, on the loop's next turn
        (never inside the cycle's own task): the renderer, the managed block,
        and a restart onto a newer installed tap."""
        if restart:
            with contextlib.suppress(Exception):
                wanted = self.recorders.follow_installed()
                if wanted is not None:
                    log(f"recorder: the next service loads tap {wanted[1]}, installed by this update")
            return
        if self._loop is not None:
            self._loop.call_soon(self._follow_update, True)

    def _follow_update(self, tap: bool = True) -> None:
        """The follow-up itself (see `followup.py`): the status-line renderer
        from the installed plugin copy and, for an install from before it,
        `statusLine.refreshInterval` in Claude Code's settings (on a thread),
        the note sync with every
        agent's `agent-rules refresh` in each context the recorded sessions run
        in (`notes.sync` reconcile: the managed block), and, with `tap`, a
        restart onto the newest installed tap when it is newer than the one
        loaded (the recorders pause about a second and resume from their saved
        progress: nothing is lost or sent twice). Never raises."""
        if self.stop_reason is not None:
            return
        from ..updater import followup
        from ...foundation.service_api.vocabularies import NotesMode
        from ...foundation.service_api.params import is_agent_id

        recorded = self.recorders.contexts()
        contexts = followup.contexts([r.get("env") for r in recorded])
        # Each recorded agent's own instruction file; the CLI's default one
        # when nothing is recorded here.
        agents = sorted({r["harness"] for r in recorded if is_agent_id(r.get("harness"))})[:MAX_NOTE_AGENTS] or [""]

        def renderer() -> None:
            for context in contexts:
                env = {"HOME": str(paths.home()), **context}
                changed = followup.sync_renderer(env)
                if changed:
                    log(f"update follow-up: the status line renderer refreshed ({', '.join(changed)})")
                self._refresh_interval(env)

        task = asyncio.ensure_future(asyncio.to_thread(renderer))
        self._warming.add(task)
        task.add_done_callback(self._warming.discard)
        for context in contexts:
            with contextlib.suppress(Exception):
                self.notes.request(context, NotesMode.RECONCILE, agents, False)
        log(f"update follow-up: the managed block refreshes in {len(contexts)} context(s)")
        if tap:
            self._follow_tap()

    def _follow_tap(self, tries: int = FOLLOW_TAP_TRIES) -> None:
        """A restart onto the newest installed tap when it is newer than the
        one loaded (`follow_installed`). A newer folder its agent may still be
        writing (Codex: a few seconds after its install, `recorders._settled`)
        is asked about again once it would have settled, at most `tries`
        times. Never raises."""
        if self.stop_reason is not None:
            return
        with contextlib.suppress(Exception):
            wanted = self.recorders.follow_installed()
            if wanted is not None:
                log(f"recorder: tap {wanted[1]} is installed (this service runs {self.recorders.tap_version}): "
                    "restarting onto it")
                self._restart_for_update(StopReason.TAP_UPDATE)
            elif self.recorders.settling and tries > 1 and self._loop is not None:
                self._loop.call_later(TAP_SETTLE_S + 1.0, self._follow_tap, tries - 1)

    def _statusline_readings(self) -> dict:
        """sid -> what a status line's capture reading is taken from here, for
        every session this service knows (`statusline.StatuslineRefresher`
        follows them): its registered mode and its recorder's `(alive,
        recording, off)` as `service.status` says them, either None when there
        is none; `statusline.OFF` for a session Probe is off for (registered
        off, or its recorder holding it off)."""
        from ..jobs.statusline import OFF

        out: dict = {s.sid: (s.mode, None) for s in list(self.registry.sessions.values())}
        for row in self.recorders.public():
            sid = row["sid"]
            out[sid] = (out.get(sid, (None, None))[0], (row["alive"], row["recording"], row["off"]))
        return {sid: OFF if reading[0] == Mode.OFF or (reading[1] and reading[1][2]) else reading
                for sid, reading in out.items()}

    def _refresh_interval(self, env: dict) -> None:
        """`followup.ensure_refresh_interval` for a context's Claude Code, once
        per its config folder in this process, at most MAX_INTERVAL_FOLDERS of
        them (a thread: it reads files)."""
        from ..updater import followup

        folder = str(followup.claude_dir(env))
        with self._interval_lock:  # the update follow-up's thread and requests' threads
            if folder in self._interval_folders or len(self._interval_folders) >= MAX_INTERVAL_FOLDERS:
                return
            self._interval_folders.add(folder)
        if followup.ensure_refresh_interval(env, seen_dir=paths.service_dir() / followup.REFRESH_INTERVAL_DIRNAME):
            log(f"the status line in {folder} redraws every {followup.REFRESH_INTERVAL_S} s")

    def _recorder_claimed(self, sid: str) -> None:
        """A recorder took (or let go of) its session's claim, on its own
        thread: the hint lane looks again now. It reads only sessions whose
        recorder holds the claim (`hints.followed`), and a lone session's
        `session.record` woke it before the claim was taken: it then slept with
        no timer, and that session's first prompt got its hint ~17 s late
        (live test E, 2026-10-24)."""
        loop = self._loop
        if loop is not None:
            with contextlib.suppress(RuntimeError):
                loop.call_soon_threadsafe(self.hints.changed)

    def _register_saved(self, params: dict) -> None:
        """A resumed recorder's session, unless the registry kept it. One that
        is off is registered `off`: it never keeps this service alive."""
        sid = params.get("sid")
        if any(s.sid == sid for s in self.registry.sessions.values()):
            return
        mode = Mode.OFF if self._session_off(params) else params.get("mode")
        self._register(None, {**params, "mode": mode, "generation": int(time.time() * 1000)})

    def _session_off(self, params: dict) -> bool:
        """Is Probe off for this session (`capture_gate`): its switch reads
        `off`, or it was seen off and is not on again yet?"""
        from ..sessions import capture_gate

        with contextlib.suppress(Exception):
            if capture_gate.is_open(capture_gate.gaps_of(params)):
                return True
            return self.recorders.off(params)
        return False

    def _recorder_held(self, params: dict) -> None:
        """A recorded session's switch turned it off (its recorder holds it now):
        registered `off` under a new generation, so `session.list` and `probe
        doctor` say so and it keeps nothing alive. Its tap's own registration
        ended with its loop; the tap registers it again once the switch is on."""
        if self.stop_reason is not None:
            return
        with contextlib.suppress(Exception):
            self._register(None, {**params, "mode": Mode.OFF, "generation": int(time.time() * 1000)})
