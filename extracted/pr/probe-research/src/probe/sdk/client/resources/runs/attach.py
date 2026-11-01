"""RunAttachMixin, Client's methods: attach to an existing run, or explain a near-miss name before
creating one (twin: app/runs)."""

from __future__ import annotations
import difflib
import random
import shlex
import time
import uuid
import warnings
from collections.abc import Iterable

from .... import errors


# Late import to avoid a cycle at module load (Run needs Client, Client returns Run).
from ....run.run import Run  # noqa: E402
from probe.sdk.client.resources.projects.experiment_locator import _walks_once


class RunAttachMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    def attach_run(
        self,
        run: str | dict,
        *,
        heartbeat: bool = True,
        attached: bool = False,
        reopen_if_dead: bool = False,
        session_id: str | None = None,
        resume_from_step: int | None = None,
        write_epoch: int | None = None,
        writer: dict | None = None,
    ) -> Run:
        """A live handle on an EXISTING run row (or id) in this process.

        The counterpart of create, through the same construction boundary
        (`_wrap_run`), so the heartbeat and auto-update-lock story is
        identical. ``resume_from_step`` arms the monotonic-step guard and
        floors the auto-step counters, so a resumed process cannot re-log
        steps the first execution already wrote.

        ``attached`` (0205) marks every beat from this handle as coming from
        INSIDE the work, which is what stamps ``attached_at`` server-side. The
        launcher's own handle leaves it False.

        ``reopen_if_dead`` (0205) is what makes a late start survivable. The
        server's heartbeat is a SILENT no-op on any non-'running' row, so a job
        that reaches its run after the created-sweep -- a queued Slurm job, a
        Modal cold start -- would otherwise beat forever into nothing and never
        learn it. See :meth:`_reopen_for_attach` for which verdicts it will
        reopen and, more importantly, which it refuses."""
        self._mark_run_process()
        data = self.get_run(run) if isinstance(run, str) else run
        armed_by_attach = False
        if reopen_if_dead:
            data = self._reopen_for_attach(data, session_id=session_id)
            # A reopen MINTS a new generation, and that generation is the only
            # one the server will accept writes under. The caller's
            # `write_epoch` (PROBE_RUN_EPOCH, exported by the launcher BEFORE
            # this reopen existed) is now stale by exactly one, so it must not
            # win: applying it fenced every metric, log and span for the rest of
            # the job -- in precisely the queued-start case the reopen is for.
            reopened_epoch = data.get("write_epoch")
            if reopened_epoch is not None:
                write_epoch = int(reopened_epoch)
            data = dict(data)
            reopened_last_step = data.pop("_resume_last_step", None)
            if resume_from_step is None and reopened_last_step is not None:
                # A requeued job restarting from an older checkpoint must drop
                # what the dead attempt already wrote, not splice over it.
                resume_from_step = int(reopened_last_step)
                armed_by_attach = True
        # Settle the epoch BEFORE _wrap_run, not after: _wrap_run starts the
        # beat thread and the synchronous attached-beat below, and both read the
        # handle's epoch. Setting it afterwards left the fence off exactly the
        # beats that keep a superseded run looking alive.
        if write_epoch is not None:
            data = {**data, "write_epoch": int(write_epoch)}
        lease = None
        if heartbeat and self._leases_available():
            # 2.8: this process writes the run under its own lease. An OWNER
            # when its verdict is the run's: a resume or takeover this process
            # reopened, or a job that joined from inside the work (PROBE_RUN_ID)
            # with no finalizing launcher to close it and no non-zero rank --
            # a forwarded PROBE_RUN_ID, a scheduler hand-off. Its release is
            # then a work-ender and it sends no status of its own (review of
            # #2060: a status PATCH after the leases' close overwrote the
            # worst verdict). A `rank` otherwise: a rank of a distributed job,
            # or a job under `probe exec`, whose launcher decides.
            session_id = session_id or str(uuid.uuid4())
            # ``writer``: the lease a reopen this process made already sent (a
            # resume keeps the role it reopened under, a launcher's included).
            lease = writer or _writer_lease(
                "rank" if attached and not self._attached_owns_verdict(data) else "owner",
                session_id,
            )
        handle = self._wrap_run(
            data, heartbeat=heartbeat, attached=attached, session_id=session_id, lease=lease
        )
        if lease is not None:
            # The lease is registered SYNCHRONOUSLY, before this process writes
            # anything (review of the 2.8 design, MED-6); the beat also stamps
            # `attached_at` for a rank and answers which rules the run follows.
            # Every rank of a large job attaches at once, so each first waits a
            # moment scaled to the job's size (at most 2 s) instead of landing
            # 600 inserts on one run in the same instant (review of #2060).
            # Best-effort: a liveness report, never a reason to take down the work.
            try:
                pause = _attach_jitter_seconds(lease.get("world_size"))
                if pause:
                    time.sleep(random.uniform(0.0, pause))
                body = {**lease, "write_epoch": handle.write_epoch or 1}
                if attached:
                    body["attached"] = True
                answer = self.beat_writer(handle.id, session_id, body)
                handle._note_lease_answer(answer)
            except Exception:
                pass
        elif attached:
            # One beat SYNCHRONOUSLY, here, rather than waiting for the loop's
            # first tick. `attached_at` is what the dashboard reads as "the job
            # itself is reporting", and leaving it up to thread scheduling means
            # a job that attaches and immediately finishes never records that it
            # attached at all. Best-effort: a failure here is a liveness report,
            # never a reason to take down the work.
            try:
                self.heartbeat_run(handle.id, attached=True, write_epoch=handle.write_epoch)
            except Exception:
                pass
        if resume_from_step is not None:
            from probe.sdk.hardware.wiring import SUSPECT_RESUME_FLOOR

            if resume_from_step >= SUSPECT_RESUME_FLOOR:
                # A last_step in hardware's epoch range means the server
                # computed the receipt WITHOUT the #364 hardware exclusion.
                # Arming would refuse every training step — fail open with a
                # warning instead (warn-never-gate).
                warnings.warn(
                    f"resume receipt last_step={resume_from_step} is in the "
                    "hardware rail's epoch range — this server predates the "
                    "hardware exclusion (research-os#364); the resume step "
                    "guard is disabled for this attach",
                    stacklevel=2,
                )
            else:
                handle.arm_resume_guard(resume_from_step)
                # Its drop warning then names the exits that work from an
                # attach, since probe.init() joining PROBE_RUN_ID takes no
                # on_conflict (Run._resume_exits).
                handle._resume_via_attach = armed_by_attach
        return handle

    @_walks_once
    def resolve_or_raise(self, kind: str, slug: str, *, project_id: str | None = None) -> dict:
        """Resolve a slug or raise the error that says what to do about it.

        Two outcomes: present (return it) or absent (create it, with near misses
        named). There used to be a third — ARCHIVED, where lookup said "missing"
        and create said "already exists" about the same slug — but archiving is
        gone, so a deleted slug is genuinely free. Both `run()` and the CLI go
        through here so the same failure cannot exit 1 from one surface and 2
        from the other."""
        if kind == "project":
            found = self.resolve_project(slug)
            if found is not None:
                return found
            from ....settings.workspace_limit import annotate_not_found, maybe_hidden_hint

            raise annotate_not_found(
                self._no_such(kind, slug, self.list_projects(limit=200).items),
                maybe_hidden_hint(getattr(self.settings, "workspace_limit", None)),
            )
        # An experiment: in the named project first (one request), then -- only
        # on a miss -- every project's, so an experiment filed elsewhere comes
        # back for `run()` to name the mismatch ("not in project ...") rather
        # than reading as absent, and a real absence names near misses from the
        # whole tenant (slugs are tenant-wide).
        if project_id:
            found = self.resolve_experiment(slug, project_id=project_id)
            if found is not None:
                return found
        found = self.resolve_experiment(slug)
        if found is not None:
            return found
        # A real absence: name the near misses, which needs the whole list.
        raise self._no_such(kind, slug, self._all_slugs("experiment"))

    @staticmethod
    def _near(slug: str, existing: Iterable[dict]) -> list[str]:
        """Existing slugs close enough to ``slug`` to be what the caller meant.

        A mistyped slug is by definition CLOSE to a real one; a genuinely new
        name is not. That asymmetry is what lets one list serve both a hard
        error (when we cannot proceed) and a warning (when we can)."""
        slugs = [row["slug"] for row in existing if row.get("slug")]
        return difflib.get_close_matches(slug, slugs, n=3, cutoff=0.6)

    def _all_slugs(self, kind: str) -> list[dict]:
        """Every row of `kind`, following the cursor.

        The near-miss guard leans on seeing the WHOLE namespace. `limit=200` is
        the schema maximum, and page ordering is unspecified, so stopping at one
        page means the guard silently stops firing past 200 rows — and it is the
        older slugs that drop out of view, which are exactly the ones a typo is
        likely to be a near-miss of. `analysis.compare()` follows the cursor for
        the same reason."""
        if kind != "project":
            # Tenant-wide on purpose: experiment slugs are unique per TENANT, not
            # per project (see resolve_experiment). Scoping this to a project
            # would let a typo of an experiment filed elsewhere sail through.
            return self._tenant_experiments()
        rows: list[dict] = []
        cursor = None
        while True:
            page = self.list_projects(limit=200, cursor=cursor)
            rows.extend(page.items)
            cursor = page.next_cursor
            if not cursor:
                return rows

    def _guard_creatable(self, kind: str, slug: str) -> None:
        """Raise unless `slug` is safe to CREATE (near-miss guard).

        Split out of ensure_* so `run()` can run it BEFORE it commits a parent:
        otherwise a refused experiment leaves a brand-new project behind, which is
        precisely the orphan identity this whole guard exists to prevent."""
        self._refuse_near_miss(kind, slug, self._all_slugs(kind))

    def _refuse_near_miss(self, kind: str, slug: str, existing: Iterable[dict]) -> None:
        """Refuse to CREATE a slug that looks like a typo of an existing one.

        A warning was the obvious first answer and it is the wrong one. The two
        places this fires — a detached ``probe run start`` process and a training
        loop — are both places nobody reads warnings, and this repo has already
        run that experiment: the ``[auto]`` question shipped WITH a fix
        affordance (``probe experiment set``) and it went unused every time. An
        invisible guard is not a guard.

        Refusing costs a caller who genuinely wants a near-identical name one
        explicit ``create_experiment``. Warning costs everyone else a second
        identity that every later comparison reads as a different thing.

        The 0.6 cutoff keeps short version-y names usable — ``v1`` vs ``v2``
        scores 0.5 and passes — so what this catches is long, near-identical
        slugs, which are far likelier to be typos than intent."""
        # An EXACT match is not a typo, it is the row itself — reachable when the
        # listing sees a slug the resolve did not (a create race, or a stale read
        # replica). Refusing there would turn "someone just made this" into a hard
        # error about a name that is already correct.
        near = [n for n in self._near(slug, existing) if n != slug]
        if not near:
            return
        cli_hint = ' --question "..." --project PROJECT_SLUG' if kind == "experiment" else ""
        sdk_hint = ", question=..., project_id=PROJECT_ID" if kind == "experiment" else ""
        raise errors.ValidationError(
            f"refusing to create {kind} {slug!r}: it is a near-miss of "
            f"{', '.join(repr(n) for n in near)}. If you meant the existing one, "
            f"use that slug. If this really is new, create it explicitly — "
            f"`client.create_{kind}({slug!r}{sdk_hint})` or "
            f"`probe {kind} create {shlex.quote(slug)}{cli_hint}`."
        )

    @staticmethod
    def _no_such(kind: str, slug: str, existing: Iterable[dict]) -> errors.NotFoundError:
        """A not-found that names near misses, so a typo says what you meant.

        A mistyped slug is by definition CLOSE to a real one; a genuinely new
        name is not. Suggesting neighbours turns the common case from "what do
        you mean it does not exist" into an obvious one-character fix."""
        near = Client._near(slug, existing)
        hint = f" Did you mean: {', '.join(near)}?" if near else ""
        # The suggested command has to actually RUN. `experiment create` requires
        # --question, so omitting it would print a command that fails on the one
        # field this whole change exists to force. The slug is quoted because it
        # arrives from the caller and this string is presented as copy-pasteable.
        extra = ' --question "..." --project PROJECT_SLUG' if kind == "experiment" else ""
        return errors.NotFoundError(
            f"no {kind} with slug {slug!r}.{hint} "
            f"Create it with `probe {kind} create {shlex.quote(slug)}{extra}` "
            "if it is genuinely new."
        )
from probe.sdk.client.client import Client  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.client.resources.runs.reopen.conflict import _attach_jitter_seconds, _writer_lease  # noqa: E402 -- pieces need each other; the front door loads this one first
