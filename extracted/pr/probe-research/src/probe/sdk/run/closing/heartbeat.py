"""HeartbeatMixin, Run's methods: the beat thread -- run and lease beats, the progress counter,
credential re-reads."""

from __future__ import annotations
import math
import os
import random
import threading
import time
import weakref
from typing import TYPE_CHECKING, Any

from ....foundation.safe_warn import safe_warn as _diagnostics
from ... import errors

if TYPE_CHECKING:  # Run only in annotations: importing it here would loop back into run.py
    from ..run import Run

    from ...client.client import Client



#: The server reaps a beating run after `run_heartbeat_stale_seconds` of silence
#: (default 900, floor 300 — app/core/config.py in research-os). 60s keeps many
#: beats inside even the floor, so one dropped request never looks like death.
_HEARTBEAT_INTERVAL_SECONDS = 60.0


def _heartbeat_interval() -> float:
    """Read PROBE_HEARTBEAT_SECONDS at call time, never at import time.

    ``0`` (or any non-positive value) is the kill switch: no thread is started.
    """
    raw = os.environ.get("PROBE_HEARTBEAT_SECONDS")
    if raw is None:
        return _HEARTBEAT_INTERVAL_SECONDS
    try:
        return float(raw)
    except ValueError:
        return _HEARTBEAT_INTERVAL_SECONDS


def _beat_forever(
    client: "Client",
    run_id: str,
    stop: threading.Event,
    interval: float,
    role: str = "owner",
    write_epoch: int | None = None,
    attached: bool = False,
    handle_ref: "weakref.ref[Run] | None" = None,
    lease: dict | None = None,
) -> None:
    """The heartbeat loop. A module function, not a bound method, so the thread
    pins only the client and the run id — an abandoned Run handle stays collectable.

    ``lease`` (SDK reliability 2.8): beat this writer's LEASE instead of the
    run-level heartbeat, carrying its progress counter, and JITTER every wait
    (the first one included) by +-20% of the interval, so 608 ranks started
    together never beat together. The lease already exists (the create, attach
    or reopen registered it), so a late first beat costs nothing.

    Failures are swallowed: a missed beat self-heals (the stale window is many
    intervals wide) and liveness reporting must never take down the work it is
    reporting on. Beats deliberately bypass the spool — replaying a stale "I was
    alive" later would be a lie.

    OBSERVER BEATS FAIL CLOSED against pre-0106 servers. A server that predates
    ``role`` silently drops the query param and records the beat in
    last_heartbeat_at — the OWNERSHIP column — which would permanently poison
    the crashed-vs-untracked verdict for a run that was only ever watched. The
    capability probe below reads the run first: a 0106+ server always serializes
    an ``observer_heartbeat_at`` key (null or set); an old server's response
    model has no such field. Absent key ⇒ old server ⇒ no beat is ever sent.
    """
    if role == "observer" and lease is None:
        try:
            if "observer_heartbeat_at" not in client.get_run(run_id):
                return
        except Exception:
            return  # can't prove support; not beating is the safe direction
    if lease is not None and stop.wait(random.uniform(0.0, interval)):
        return
    # 0205. Swallowing beat failures self-heals a blip, but an outage longer
    # than the server's stale window is not a blip: the reaper ends the run as
    # 'crashed' while this process is alive and still beating, and every beat
    # after that is a silent no-op against a terminal row. Nothing reconciled
    # it, so a healthy job stayed attached to a dead row for the rest of its
    # life. Count the failures; on the first beat that lands again, check
    # whether we were declared dead while we were away, and if the row is still
    # OURS (same write_epoch -- no newer attempt took it over) put it back.
    failures = 0
    # A recovery that failed TRANSIENTLY (a 503 while every rank's backlog
    # drains, a timeout) is retried on the following beats, up to a cap: one
    # try left a job that outlived an outage `crashed` for the rest of its life
    # although every later beat landed.
    recovery_tries = 0
    # Set when the capped retries ran out on a row that stays `crashed`, so a
    # beat landing on it does not restart the whole cycle every few beats.
    gave_up = False
    while True:
        try:
            row = _beat_once(
                client,
                run_id,
                role=role,
                attached=attached,
                write_epoch=write_epoch,
                lease=lease,
                handle_ref=handle_ref,
            )
            # 2.2: a beat that LANDS on a `crashed` row means something ended
            # this run while its owner is alive and heard -- a writer-gone
            # report that was wrong, or a reaper verdict from before a blip we
            # never saw fail. Same repair as after a failed beat.
            reaped = isinstance(row, dict) and row.get("status") == "crashed"
            if not reaped:
                gave_up = False
            if failures or (reaped and not gave_up):
                recovered = _recover_after_outage(
                    client,
                    run_id,
                    role=role,
                    write_epoch=write_epoch,
                    handle_ref=handle_ref,
                    # Beats kept landing, so no outage explains the verdict:
                    # repair only what the SYSTEM decided (the reaper, a
                    # writer-gone report), never a person's `crashed`.
                    system_verdict_only=not failures,
                )
                if recovered is _RECOVERY_RETRY:
                    recovery_tries += 1
                    if recovery_tries < _MAX_RECOVERY_TRIES:
                        if stop.wait(interval):
                            return
                        continue  # keep `failures`: the repair is still owed
                if recovered is None or recovered is _RECOVERY_RETRY:
                    # Nothing this process can do about THIS crashed row;
                    # a later change of the row (or a new outage) re-arms it.
                    gave_up = reaped
                else:
                    # The receipt's generation. With keep_epoch (1.1) it is the
                    # one we already hold; adopting it anyway (here AND on the
                    # handle, inside _recover_after_outage) keeps this process
                    # writable if a server ever answers with another.
                    write_epoch = recovered
            failures = 0
            recovery_tries = 0
        except errors.ConflictError:
            # 0185's fence answers a SUPERSEDED writer's beat with 409: a
            # relaunch took this run over (2.3) and owns it on a newer epoch.
            # Every later write from this process is refused too, so say so
            # once and stop beating instead of failing quietly forever.
            _diagnostics.warn(
                f"probe: run {run_id} was taken over by a newer attempt; this "
                "process no longer writes to it (its writes are refused). If "
                "this job is still meant to run, relaunch it as its own run."
            )
            return
        except Exception:
            failures += 1
        if stop.wait(interval * random.uniform(0.8, 1.2) if lease is not None else interval):
            return


class _Progress:
    """This writer's PROGRESS counter (SDK reliability 2.8, Signal 1): bumped
    once per training or validation batch -- a non-hardware `log()` or
    `step()`, an integration's batch-end hook, or `Run.progress()` -- and sent
    on every lease beat for the server's stall detector.

    A span (a step, a rollout, a trial) and an artifact upload count too: a
    checkpoint save that uploads is work, not a stall.

    Idle is measured on the MONOTONIC clock, so an outage never fakes a stall
    and a slow network never hides one. The baseline is two numbers kept here
    so the server stores two, not a series: the p99 of the gap between bumps
    over the last 24 h (per-hour log-scale histograms, 1 ms to ~15 h, 25% bins,
    so the memory is fixed however fast the loop runs), and the longest gap
    that was followed by progress again over the WHOLE run (the nightly
    checkpoint or the long eval this run already survived)."""

    _WINDOW_HOURS = 24
    _FLOOR = 0.001
    _RATIO = 1.25
    _BINS = 80

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self.count = 0
        self._last: float | None = None
        #: hour index -> (bin counts, longest gap that hour)
        self._hours: dict[int, tuple[list[int], float]] = {}
        #: The longest gap this writer ever recovered from, over the WHOLE run:
        #: a nightly checkpoint learned once stays learned (a 24 h window would
        #: forget it just before the next one).
        self._longest_ever = 0.0

    def bump(self) -> None:
        now = time.monotonic()
        with self._lock:
            if self._last is not None and now > self._last:
                self._record(now, now - self._last)
            self._last = now
            self.count += 1

    def _record(self, now: float, gap: float) -> None:
        hour = int(now // 3600)
        bins, longest = self._hours.get(hour) or ([0] * (self._BINS + 1), 0.0)
        index = 0 if gap <= self._FLOOR else int(math.log(gap / self._FLOOR, self._RATIO)) + 1
        bins[min(index, self._BINS)] += 1
        self._hours[hour] = (bins, max(longest, gap))
        self._longest_ever = max(self._longest_ever, gap)
        for old in [h for h in self._hours if h <= hour - self._WINDOW_HOURS]:
            del self._hours[old]

    def snapshot(self) -> dict:
        """The beat's progress fields (none before the first bump)."""
        now = time.monotonic()
        with self._lock:
            if self._last is None:
                return {}
            out: dict[str, Any] = {
                "progress": self.count,
                "progress_idle_seconds": round(now - self._last, 3),
            }
            live = {h: v for h, v in self._hours.items() if h > int(now // 3600) - self._WINDOW_HOURS}
            if live:
                merged = [0] * (self._BINS + 1)
                for bins, _ in live.values():
                    merged = [a + b for a, b in zip(merged, bins)]
                total = sum(merged)
                seen = 0
                for index, n in enumerate(merged):
                    seen += n
                    if seen >= 0.99 * total:
                        # The bin's UPPER edge: a conservative (longer) p99.
                        out["progress_gap_p99_seconds"] = round(self._FLOOR * self._RATIO**index, 3)
                        break
            if self._longest_ever > 0:
                out["progress_longest_gap_seconds"] = round(self._longest_ever, 3)
            return out


#: `_recover_after_outage` could not finish for a reason that may pass (see
#: `journal.classify`): the beat loop tries again on its next beats.
_RECOVERY_RETRY: Any = object()
#: Recovery attempts per outage before the loop gives up (about five minutes
#: at the default 60 s beat). The reaper's verdict then stands, as it did.
_MAX_RECOVERY_TRIES = 5


def _lease_beat(
    client: "Client",
    run_id: str,
    lease: dict,
    write_epoch: int | None,
    handle_ref: "weakref.ref[Run] | None",
    *,
    attached: bool = False,
) -> dict:
    """One lease beat (2.8), in the run-level beat's row shape (``status``,
    ``write_epoch``) so the loop's recovery reads it the same way. The
    handle, while it lives, supplies the progress counter and learns which
    protocol the server keeps this run on."""
    handle = handle_ref() if handle_ref is not None else None
    body = {**lease, "write_epoch": write_epoch or 1}
    body.pop("session_id", None)
    if attached:
        # From inside the work (0205): the beat stamps `attached_at`, as the
        # run-level `?attached=true` did -- an OWNER lease included.
        body["attached"] = True
    if handle is not None:
        body.update(handle._progress.snapshot())
    resp = client.beat_writer(run_id, lease["session_id"], body)
    if handle is not None:
        handle._note_lease_answer(resp)
    return {
        "status": resp.get("run_status") if isinstance(resp, dict) else None,
        "write_epoch": resp.get("write_epoch") if isinstance(resp, dict) else None,
    }


def _beat_once(
    client: "Client",
    run_id: str,
    *,
    role: str,
    attached: bool,
    write_epoch: int | None,
    lease: dict | None = None,
    handle_ref: "weakref.ref[Run] | None" = None,
) -> Any:
    """One beat. When the API refuses the CREDENTIAL (plan 2.7), re-read it and
    retry once: a re-login on the box revokes the token this process was built
    with, and a swallowed 401 on every beat after that is how a live run was
    reaped as `crashed` 15 minutes later. A refusal of one request's scope is
    not the credential and is not retried (`key_refusal.credential_refused`)."""
    refused = getattr(getattr(client, "settings", None), "token", None)

    def beat() -> Any:
        if lease is not None:
            return _lease_beat(client, run_id, lease, write_epoch, handle_ref, attached=attached)
        return client.heartbeat_run(run_id, role=role, attached=attached, write_epoch=write_epoch)

    try:
        return beat()
    except errors.RosError as exc:
        from ...settings.key_refusal import credential_refused

        refresh = getattr(client, "refresh_credentials", None)
        if (
            refresh is None
            or not credential_refused(exc.status, str(exc))
            or not refresh(refused=refused)
        ):
            raise
        return beat()


class HeartbeatMixin:
    """Part of Run: its methods run with `self` the Run; compose() folds them into Run."""

    def progress(self) -> None:
        """Say this process made progress (SDK reliability 2.8).

        Every non-hardware ``log()`` and ``step()`` already counts, and so do
        the Lightning and Hugging Face integrations' batch ends. Call this in
        a custom loop that logs rarely -- or inside a long phase that logs
        nothing, such as a checkpoint upload -- so the stall detector, which
        pages when a live process stops advancing, knows it is still moving.
        Cheap (a counter under a lock) and it never raises."""
        try:
            self._progress.bump()
        except Exception:  # noqa: BLE001 -- bookkeeping never touches the work
            pass

    # -- liveness -----------------------------------------------------------
    def start_heartbeat(
        self,
        interval_seconds: float | None = None,
        role: str = "owner",
        *,
        attached: bool | None = None,
    ) -> None:
        """Beat ``POST /v1/runs/{id}/heartbeat`` from a daemon thread until a
        terminal :meth:`set_status` (or the process exits). Idempotent.

        ``Client.create_run`` calls this for every handle it mints, so the rule
        from :meth:`Client.heartbeat_run` — beat for the run's whole life or not
        at all — holds by construction: the beats stop exactly when this process
        stops, and a process that dies without finishing is precisely what the
        server's reaper should flip to 'crashed'. Only start an OWNER beat on a
        handle whose run lives and dies with the current process; a run managed
        from outside (CLI ``run start``) must never owner-beat.

        ``role="observer"`` (0106) is the sanctioned beat for processes that
        watch a run they do not own — the miles exporter sidecar. It asserts
        "something is attached", keeping the run alive while present, and its
        silence resolves to 'untracked' rather than 'crashed'.

        ``attached`` (0205) marks these beats as coming from INSIDE the work, so
        the server stamps ``attached_at``. Defaults to the handle's own flag,
        which ``_wrap_run`` set: a launcher's handle beats without it, a handle
        opened by ``probe.init()`` from PROBE_RUN_ID beats with it. Under a
        wrapped run both processes beat as owners, and this is the only thing
        that tells them apart.

        Interval precedence: explicit argument, then PROBE_HEARTBEAT_SECONDS,
        then the 60s default. Non-positive disables.

        The thread also stops when this handle is garbage-collected (an
        abandoned run's process may still be alive, but nobody can ever finish
        it — letting the reaper end it is the honest outcome) and when the
        owning ``Client`` closes (beats ride its transport).
        """
        if role not in ("owner", "observer"):
            # Fail loudly HERE: the beat loop swallows every exception, so a
            # typo'd role would otherwise 422 silently forever and the run
            # would be reaped despite a "running" heartbeat thread.
            raise ValueError(f"heartbeat role must be 'owner' or 'observer', got {role!r}")
        if self._hb_thread is not None and self._hb_thread.is_alive():
            if getattr(self, "_hb_role", "owner") != role:
                # Role change is explicit, never silent: an owner beat that
                # quietly stayed 'observer' would make a real death read
                # 'untracked', and the reverse keeps asserting ownership after
                # the owner detached. Restart the loop under the new role.
                self.stop_heartbeat()
                if self._hb_thread is not None:
                    self._hb_thread.join(timeout=1.0)
            else:
                return
        interval = _heartbeat_interval() if interval_seconds is None else float(interval_seconds)
        if interval <= 0:
            return
        self._hb_role = role
        # The beat may have to re-read a refused credential (plan 2.7), which
        # needs to know whose it was while it still works.
        learn = getattr(self._client, "_learn_identity", None)
        if learn is not None:
            learn()
        stop = threading.Event()
        thread = threading.Thread(
            target=_beat_forever,
            args=(
                self._client,
                self.id,
                stop,
                interval,
                role,
                self.write_epoch,
                getattr(self, "attached", False) if attached is None else attached,
                # WEAK on purpose: the thread must not pin the handle (its
                # collection is what stops the beat), but a reopen after an
                # outage has to reach the handle's epoch or the process is
                # locked out of the run it just recovered.
                weakref.ref(self),
                # 2.8: beat the writer's lease instead of the run-level beat.
                None
                if self._lease is None
                else {**self._lease, "role": "observer"}
                if role == "observer"
                else self._lease,
            ),
            name=f"probe-run-heartbeat-{self.id[:8]}",
            daemon=True,
        )
        self._hb_stop = stop
        self._hb_thread = thread
        # OWNER beats are the moment this process declares that its lifetime
        # IS the run's lifetime, which is exactly the claim the node agent
        # needs in order to blame a vanished pid on a run. Observers are not
        # registered: an observer never staked its lifetime on anything, and
        # its exit says nothing about the work.
        if role == "owner":
            self._register_with_node_agent()
        # finalize holds the Event (its callback arg), never the Run, so the
        # handle stays collectable and its collection is what ends the beat.
        self._hb_finalizer = weakref.finalize(self, stop.set)
        self._client._register_run_heartbeat(stop)
        thread.start()

    def stop_heartbeat(self) -> None:
        if self._hb_stop is not None:
            self._hb_stop.set()
        if self._hb_finalizer is not None:
            self._hb_finalizer.detach()
        self._hb_stop = None
        self._hb_thread = None
        self._hb_finalizer = None
from probe.sdk.run.closing.outage import _recover_after_outage  # noqa: E402 -- pieces need each other; the front door loads this one first
