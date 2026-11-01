"""ReopenConflictMixin, Client's methods: the on_conflict policy: create, resume or rewind an
incumbent run, with writer leases and attach jitter (twin: app/runs)."""

from __future__ import annotations
import os
import socket
import sys
import uuid
from dataclasses import dataclass
from typing import Any
from ..... import agent_session

from ..... import errors


# Late import to avoid a cycle at module load (Run needs Client, Client returns Run).
from .....run.run import Run  # noqa: E402

@dataclass(frozen=True)
class Rewind:
    """``on_conflict`` policy object (0185): resume the incumbent from a
    checkpoint, DISCARDING its step-indexed record from ``step`` onward.

    The parameterized member of the policy vocabulary — the four string
    policies need no arguments, a rewind needs its step, and carrying the step
    ON the policy means the two can never disagree. ``step`` matches W&B
    muscle memory: everything from it (inclusive) is rewritten, so a loop may
    re-log the checkpoint step itself or start one above it.

    Destructive by explicit request only, and the request is also the consent:
    a ``completed`` incumbent — the deliberate stop-then-rewind flow — reopens
    under a Rewind where a plain resume keeps refusing it. Keep-both belongs
    to :meth:`Client.fork_run`; from-scratch retries to ``"supersede"``.
    """

    step: int

    def __post_init__(self) -> None:
        if isinstance(self.step, bool) or not isinstance(self.step, int) or self.step < 0:
            raise errors.ValidationError(
                f"Rewind(step={self.step!r}): the rewind step must be a "
                "non-negative integer — the first step the relaunch will "
                "rewrite."
            )


def _repin_bracket_lease(run_id: str, write_epoch: object) -> None:
    """A reopen from THIS machine moved the run to a new epoch: carry it into
    the `probe run start` bracket's lease, if this machine holds a live one.

    The lease pins the epoch every later run-scoped CLI write stamps (0185),
    and since 1.10 that includes `probe run end`. The measured shape: `run
    start` pins 1, the quiet bracket is reaped `untracked`, the job's own
    `probe.init()` attaches and reopens (epoch 2), and `probe run end` then
    sent 1 and was refused (sync exit 1, async dead-lettered). A reopen made
    by the bracket's own job is not a newer attempt to fence out.

    Only a LIVE lease that already pins an epoch is touched: a run with no
    bracket must not grow a lease file. A reopen on ANOTHER machine cannot
    reach this file; see the PR notes. Never raises."""
    try:
        from probe.foundation.durable import run_lock

        if run_lock.lease_write_epoch(str(run_id)) is not None:
            run_lock.touch_lease(str(run_id), write_epoch=int(write_epoch))
    except Exception:  # noqa: BLE001 -- best-effort, like the lease tier itself
        pass


#: SDK reliability 2.8: the server takes per-writer leases (0271).
_LEASES_FEATURE = "run_writer_leases"
#: (rank, world size, local rank) environment variables, most specific first,
#: the same schemes `fluent._GLOBAL_RANK_VARS` reads.
_LEASE_RANK_VARS = (
    ("RANK", "WORLD_SIZE", "LOCAL_RANK"),
    ("SLURM_PROCID", "SLURM_NTASKS", "SLURM_LOCALID"),
    ("OMPI_COMM_WORLD_RANK", "OMPI_COMM_WORLD_SIZE", "OMPI_COMM_WORLD_LOCAL_RANK"),
)


def _env_int(name: str) -> int | None:
    raw = (os.environ.get(name) or "").strip()
    return int(raw) if raw.isdigit() else None


#: The attach beat's spread: this many seconds per rank of the job, capped.
_ATTACH_JITTER_PER_RANK = 0.005
_ATTACH_JITTER_MAX = 2.0


def _attach_jitter_seconds(world_size: object) -> float:
    """How long a rank may wait before its attach beat: 0 for a single process,
    ~0.3 s for 64 ranks, 2 s from 400 ranks up."""
    try:
        size = int(world_size or 0)
    except (TypeError, ValueError):
        return 0.0
    if size <= 1:
        return 0.0
    return min(_ATTACH_JITTER_MAX, _ATTACH_JITTER_PER_RANK * size)


def _writer_lease(role: str, session_id: str) -> dict:
    """Who this process is, as a lease (sent on create/attach/reopen and on
    every lease beat). Rank fields come from the launcher's environment."""
    from .....run.closing.heartbeat import _heartbeat_interval

    lease: dict[str, Any] = {
        "session_id": str(session_id),
        "role": role,
        "host": socket.gethostname()[:255] or None,
        "pid": os.getpid(),
        "interactive": "ipykernel" in sys.modules,
    }
    interval = _heartbeat_interval()
    if interval > 0:
        lease["interval_seconds"] = float(interval)
    for rank_var, size_var, local_var in _LEASE_RANK_VARS:
        rank = _env_int(rank_var)
        if rank is None:
            continue
        lease["rank"] = rank
        size = _env_int(size_var)
        if size:
            lease["world_size"] = size
        local = _env_int(local_var)
        if local is not None:
            lease["local_rank"] = local
        break
    return lease


class ReopenConflictMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    def _create_run_with_policy(
        self,
        create,
        run_kw: dict,
        name: str,
        on_conflict: str | Rewind,
        *,
        experiment_id: str | None,
        project_id: str | None,
        max_attempts: int = 5,
    ) -> Run:
        """``create()``, except an external_id 409 is resolved by policy.

        RESUME reopens the incumbent in place — same identity, same curve —
        which is only honest when the relaunch continues from a checkpoint;
        the step guard on the returned handle enforces that. SUPERSEDE opens a
        NEW run as ``external_id-rN`` carrying ``parent_relation="retry"``
        plus ``retry_of``/``retry_attempt`` foreign keys, for the relaunch
        that replays from step 0 (appending that into a half-dead run would
        splice two executions into one curve — the W&B ``resume="allow"``
        failure mode). Either way a dead incumbent's partial record survives:
        resume continues it, supersede tags it ``superseded``."""
        try:
            return create(run_kw, name)
        except errors.ConflictError as conflict:
            base = run_kw.get("external_id")
            if on_conflict == "error" or base is None:
                raise
            existing_id = conflict.existing_id
        old = None
        if existing_id:
            # The SERVER already resolved the incumbent, on the real key --
            # `SELECT id FROM runs WHERE source = $1 AND external_id = $2`, which
            # is the (customer_id, source, external_id) uniqueness the 409 came
            # from. Ask it rather than re-deriving the answer from a listing.
            try:
                old = self.get_run(existing_id)
            except errors.NotFoundError:
                old = None  # raced with a delete; fall through to the scan
        if old is None:
            # Older backends send a bare 409. Match on BOTH halves of the key:
            # external_id alone is not unique -- ingest and sdk runs share the
            # namespace by design -- so this used to be able to hand back a
            # different source's run and resume or supersede the wrong one.
            source = (run_kw.get("source") or "api").strip().lower()
            page = self.list_runs(experiment_id=experiment_id, project_id=project_id)
            old = next(
                (
                    r
                    for r in page.items
                    if r.get("external_id") == base
                    and str(r.get("source") or "").strip().lower() == source
                ),
                None,
            )
        if old is None:
            # The 409 is real but the incumbent is not on the first page (or
            # belongs to another source). Acting on it blind would resume or
            # supersede the wrong thing, so the original conflict stands.
            raise errors.ConflictError(
                f"run {base!r} conflicts but its incumbent is not visible "
                "here — resolve the collision by hand",
            )
        status = old.get("status")
        if isinstance(on_conflict, Rewind):
            # Rewind = resume from an earlier checkpoint. `completed` is
            # ALLOWED here — the deliberate stop-then-rewind flow ends cleanly
            # first, and naming the destructive step is the consent the plain
            # resume's 409 exists to demand. A live writer still refuses.
            takeover = status == "running" and self._supports_takeover()
            if status not in self._DEAD_RUN_STATUSES and status != "completed" and not takeover:
                raise errors.ConflictError(
                    f"run {base!r} is {status} and its writer may still be "
                    "alive — rewind refuses to hijack an open run. End it (or "
                    "let the reaper mark it crashed), then relaunch."
                )
            # Preflight BEFORE any state changes: a pre-0185 server silently
            # drops the unknown body field, reopens the run, and deletes
            # nothing — the worst failure shape a destructive request can
            # have. One cheap GET turns that skew into a loud no-op error.
            self._require_feature(
                "run_rewind",
                "this server predates run rewind (0185): a reopen would "
                "silently ignore rewind_to_step and delete nothing. Upgrade "
                'research-os, or use on_conflict="supersede" / fork_run().',
            )
            return self._resume_run(
                old, run_kw, rewind_to_step=on_conflict.step, takeover=takeover
            )
        if on_conflict in ("auto", "resume"):
            if status in self._DEAD_RUN_STATUSES:
                return self._resume_run(old, run_kw)
            if status == "running" and self._supports_takeover():
                # 2.3: a requeued job whose previous pod is gone but not yet
                # reaped. The server takes the run over only once it has been
                # silent long enough to be dead, and says how long to wait.
                return self._resume_run(old, run_kw, takeover=True)
            if status == "completed":
                raise errors.ConflictError(
                    f"run {base!r} already completed — resuming would append "
                    "onto a good record. Repeat it deliberately with "
                    'on_conflict="supersede", or rewind it from a checkpoint '
                    "with on_conflict=probe.Rewind(step=N)."
                )
            raise errors.ConflictError(
                f"run {base!r} is {status} and its writer may still be alive "
                "— refusing to hijack an open run. If it is truly dead, wait "
                "for the reaper to mark it crashed, or supersede explicitly."
            )
        for n in range(2, max_attempts + 2):
            retry_id = f"{base}-r{n}"
            retry_kw = dict(
                run_kw,
                external_id=retry_id,
                parent_run_id=old["id"],
                parent_relation="retry",
                # The SDK derived this parent (an id collision), nobody
                # declared it: stored as observed, not as a person's claim.
                parent_provenance="observed_call",
            )
            if name == base and retry_kw.get("authored_by") is None:
                # `retry_id` below is a string the SDK composed (`<base>-r2`),
                # so it declares itself -- same rule as `fork_run`, and only
                # when the caller has not already said. Without it a nightly
                # `on_conflict="supersede"` from a bare terminal locks
                # `nightly-eval-r2` as human-chosen, forever.
                retry_kw["authored_by"] = agent_session.AUTHORSHIP_AGENT
            try:
                run = create(retry_kw, retry_id if name == base else name)
                break
            except errors.ConflictError:
                continue
        else:
            raise errors.ConflictError(
                f"no free retry slot for {base!r} after {max_attempts} "
                "attempts — the run has been superseded that many times "
                "already, which is worth a look before retrying again",
            )
        # link() is the sanctioned foreign-keys surface (create_run does not
        # take them); per-key new-wins, so this cannot clobber anything.
        run.link(retry_of=old["id"], retry_attempt=n)
        if old.get("status") in self._DEAD_RUN_STATUSES:
            tags = sorted({*(old.get("tags") or []), "superseded"})
            # sync=True, for two reasons that compound. `tags` is a whole-list
            # REPLACE built from a row read a moment ago, so a delayed replay
            # would overwrite whatever the old run acquired in between. And the
            # op would carry the OLD run's run_ref, which the NEW run's finish()
            # barrier -- scoped to its own id -- never covers, so it could sit
            # queued indefinitely while the run it marks looks merely dead.
            self.write("PATCH", f"/v1/runs/{old['id']}", {"tags": tags}, sync=True)
        return run

    @staticmethod
    def _attached_owns_verdict(row: dict) -> bool:
        """Whether a job attaching to ``row`` from inside the work owns the
        run's verdict: no finalizing `probe exec` launcher names this run, and
        this process is not a non-zero rank of a distributed job."""
        from .....fluent.attach import _nonzero_global_rank
        from .....run.launch.execute import EXEC_FINALIZES_ENV

        finalized = (os.environ.get(EXEC_FINALIZES_ENV) or "").strip() == str(row.get("id"))
        return not finalized and _nonzero_global_rank() is None

    def _leases_available(self) -> bool:
        """Whether this client's server takes per-writer leases (2.8). A failed
        preflight reads as "no": the run-level heartbeat, as before."""
        try:
            return self.supports_feature(_LEASES_FEATURE)
        except Exception:  # noqa: BLE001 -- never a reason for a run not to open
            return False

    def _lease_for_create(
        self, body: dict, *, heartbeat: bool, awaiting_attach: bool, launcher: bool
    ) -> tuple[str | None, dict | None]:
        """Ask for a `leases` run when this process will beat for it: adds
        `liveness_protocol` + `writer` to the create body. Returns the session
        and lease the handle must carry, or (None, None).

        A HAND-OFF (`awaiting_attach`: `probe exec -- sbatch`,
        `--detached-launcher`) asks for `leases` too, with NO writer: the job's
        ranks each register their own lease when they attach (`attach_run`),
        and the run closes by the lease rules like any other (plan 2.8: every
        rank holds a lease). Without it the run stayed legacy, where the ranks'
        writer-gone reports change nothing and a scancel'd job waited for the
        900 s reaper. The submitter holds no lease on purpose: it exits the
        moment the scheduler accepts the job, so its release would end the run
        as `completed` before the work starts (a launcher's release waives the
        rank slots), and a lease it never released would expire into a false
        `writer_lost` on every job queued or running past an hour. The
        created-sweep still ends a hand-off nobody attaches to. A hand-off
        whose opener beats the run itself (`heartbeat=True`) stays legacy: its
        run-level heartbeat would flip the run anyway."""
        if awaiting_attach:
            if not heartbeat and self._leases_available():
                body["liveness_protocol"] = "leases"
            return None, None
        if not heartbeat or not self._leases_available():
            return None, None
        session_id = str(uuid.uuid4())
        lease = _writer_lease("launcher" if launcher else "owner", session_id)
        body["liveness_protocol"] = "leases"
        body["writer"] = lease
        return session_id, lease

    def _supports_takeover(self) -> bool:
        """Whether the server takes over a silent `running` run (2.3). A
        failed preflight reads as "no": today's ConflictError, not a new
        failure mode at init."""
        try:
            return self.supports_feature("run_reopen_takeover")
        except errors.RosError:
            return False
