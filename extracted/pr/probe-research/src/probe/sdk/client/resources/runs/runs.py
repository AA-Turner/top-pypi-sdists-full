"""RunsResource (client.runs, typed reads) and RunsMixin, Client's methods: run(), the open door --
create, resume or attach, wrap the Run handle, auto snapshot (twin: app/runs)."""

from __future__ import annotations

import builtins
import os
import sys
import warnings
from collections.abc import Iterator
from datetime import datetime
from typing import Any

from pydantic import BaseModel
from ....values import values as _coerce
from ....values.times import to_iso_time
from ....values.run_type import to_run_type
from .....generated.models import (
    RunBundle,
    RunCountsOut,
    RunDetailOut,
    RunLineage,
    RunListLightOut,
    RunListLightRowOut,
    RunListRowOut,
    RunPageDetailOut,
    RunReproduce,
    SpanOut,
    TrialListOut,
    TrialOut,
    WriterOut,
)
from ....delivery.transport.transport import Page
from ...resource import Resource

from .... import errors
from ....delivery.transport.deadlines import pause_patience, without_patience


# Late import to avoid a cycle at module load (Run needs Client, Client returns Run).
from ....run.run import Run  # noqa: E402
from probe.sdk.client.ids import _id_ref, is_new_slug, to_kebab_slug
from probe.sdk.client.resources.runs.logs import LogsResource
from probe.sdk.client.resources.runs.ordering import DEFAULT_ORDER, parse_run_order
from probe.sdk.client.resources.runs.listing import RECENT_ORDER
from probe.sdk.client.resources.runs.table import RunTable
from probe.sdk.client.resources.projects.experiment_locator import _walks_once
from probe.sdk.client.resources.runs.home import (
    ProjectFromEnv,
    explain_missing_home,
    find_missing_home,
    mark_home_source,
    print_notice,
    resolve_run_home,
)


class RunsMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    def _wrap_run(
        self,
        data: dict,
        *,
        heartbeat: bool,
        attached: bool = False,
        session_id: str | None = None,
        lease: dict | None = None,
        lease_registered: bool = False,
        lease_protocol: str | None = None,
    ) -> Run:
        run = Run(self, data)
        run._lease_registered = lease_registered
        # Which rules the run follows, as far as this process knows: `leases`
        # for a create that carried the lease, else unknown until a lease beat
        # answers (an unknown protocol closes the pre-2.8 way).
        run._lease_protocol = lease_protocol
        # The writer session BEFORE the beat starts: a lease beat names it, and
        # 2.2's writer-gone report and the capture record carry the same id.
        if session_id is not None:
            run.session_id = str(session_id)
        # 2.8: this handle writes under a lease (its beats and its close go to
        # /writers/{session}); None keeps the run-level heartbeat.
        run._lease = lease
        # The OOM count at open, for a wrapper's `finish(exit_code=-9)` (`_status_for_exit`).
        from ....run.launch.oom import OomCounter

        run._oom_counter = OomCounter()
        # 0205. Marks every beat this handle sends as coming from inside the
        # work. Set only by the env-attach path; a launcher's handle leaves it
        # False so its beats keep the run live without claiming the job itself
        # ever reported.
        run.attached = attached
        # A handle minted here is presumed to live and die with this process, so
        # it beats by default and the server's reaper can flip it to 'crashed'
        # when the process dies. Pass heartbeat=False when the run is DETACHED —
        # created here but executed and finished from somewhere else (CLI
        # `run start`, the miles exporter) — because beating briefly and then
        # going silent gets a legitimately-running run reaped.
        #
        # `heartbeat` also decides which tier of the auto-update run lock applies,
        # and it is exactly the right question: a run that lives and dies with
        # this process can hold an flock the kernel releases on death, while a
        # detached one has no process to hold anything and needs a renewable
        # lease. This is the single construction boundary, so every path that
        # opens a run — client.run(), probe.init(), a directly built handle —
        # is covered by it.
        run._hold_run_lock(process_bound=heartbeat)
        if heartbeat:
            # OUTSIDE `probe.init()`'s retry budget (plan 2.5): where a thread
            # inherits its creator's context (free-threaded 3.14), a beat thread
            # started inside it would carry init's deadline for the whole run.
            with without_patience():
                run.start_heartbeat(attached=attached)
        # Every run open in this process counts when deciding whether spawned
        # workers may be bound to one (lineage plan 3, F5): a second run --
        # recording or not -- and a worker's reads belong to neither for sure.
        from ....run.launch import open_runs as _open_runs

        _open_runs.opened(run)
        return run

    @staticmethod
    def _opened(run: Run) -> Run:
        """Tell this session's Probe daemon a run just opened (R3.1).

        Every create door ends here, so `probe.init()`, `Client.run()`, `probe
        run start`, `probe exec`, children and forks all announce, exactly once.
        Fire-and-forget: no daemon, no session or any error changes nothing."""
        from ....diagnostics import mark_run_opened_during
        from ....run.launch import daemon_channel

        # Created maybe inside an `except` (a retry wrapper): that error is not this run's death.
        mark_run_opened_during(run)
        daemon_channel.run_started(getattr(run, "data", None))
        return run

    @_walks_once
    def run(
        self,
        *,
        experiment: str | None = None,
        question: str | None = None,
        name: str | None = None,
        project: str | ProjectFromEnv | None = None,
        experiment_name: str | None = None,
        on_conflict: str | Rewind = "auto",
        hw: bool | None = None,
        snapshot: bool | None = None,
        # Named here rather than left to `**run_kw`. They ALWAYS worked through it
        # -- `_run_impl` splats run_kw straight into `create_run` -- but appeared in
        # no signature, so the only way to learn the door existed was to read
        # `create_run`. Fleet-wide that showed up as one organic hand-declared
        # lineage edge in the whole history, and six runs that wrote
        # `parent_run_id` into `foreign_keys` instead, where no query can follow it.
        parent_run_id: str | None = None,
        parent_relation: str | None = None,
        capture_reads: bool | None = None,
        outputs: str | os.PathLike | None = None,
        capture_outputs: bool | None = None,
        intent: str | None = None,
        ignore: str | list[str] | tuple[str, ...] | None = None,
        workspace: str | None = None,
        started_at: str | datetime | None = None,
        run_type: str | None = None,
        **run_kw,
    ) -> Run:
        """Open a run — full resolution/creation/``on_conflict`` semantics in
        ``client/resources/runs/DESIGN.md`` ("Opening a run"). ``workspace`` (a slug or an id) is where a
        NEW project is filed; without it, this computer's workspace (``probe
        workspace use``, ``PROBE_WORKSPACE``). A team with several workspaces and
        none set files into your home workspace, and raises ``WorkspaceRequired``
        before anything is created when you have none. ``started_at`` (ISO 8601 with an
        offset, or an aware datetime) is a re-logged past run's real start; close it with
        ``run.set_status(status, ended_at=...)``. ``run_type="rl"`` declares an RL training or agent-eval
        run (RL tabs and Trials); omitted, the run reads ``general`` until RL data marks it. ``hw=True`` (or ``PROBE_HW=1``) also
        starts the opt-in hardware collector when this process is the
        node-local leader. Best-effort by contract: a broken collector never
        touches the run (agent/src/probe/sdk/hardware/DESIGN.md). ``snapshot``
        controls the open-time auto-snapshot: ``None`` follows
        ``PROBE_AUTO_SNAPSHOT`` (default on), ``False`` skips, ``True`` forces.

        Output capture (D17, :mod:`probe.sdk.capture.outputs`): a run this process owns
        captures what it writes to the working directory -- or to ``outputs``,
        for runs that share a folder -- and everything it prints, when it
        closes. ``capture_outputs=False`` (or ``PROBE_CAPTURE_OUTPUTS=0``) opts
        out. A detached run (``heartbeat=False``, ``awaiting_attach``) captures
        nothing: this process is not the work.

        Every run has a home, found by slug or id, never by name. A new ``project`` slug
        creates the project (kind ``general``); an ``experiment`` is created only with
        ``question=``. ``project=probe.FROM_ENV`` opens it in ``PROBE_PROJECT``, else this
        session's project (``probe session home``), else ``probe project use``
        (``home.py``), waiting for this session's daemon to pick one when none is set. With
        nothing named it asks the person at a terminal, or raises ``ProjectRequired`` with the
        line to add before any request. ``intent`` is free
        text saying what the run is meant to show; it rides in the run's
        ``metadata.intent`` (the run schema has no field for it), and the daemon
        files and describes the run by it.

        ``ignore`` adds gitignore-style patterns to the ``.probeignore`` file at
        the git toplevel and to ``PROBE_IGNORE`` (plan (n)): matching files are
        left out of code capture, output capture and read capture. It only
        excludes -- a credential stays withheld whatever it says -- and an
        explicit ``log_artifact`` or ``snapshot(include=...)`` still wins.
        Inside a ``probe exec`` child (``probe.init(ignore=...)`` joining the
        launcher's run) the patterns reach the launcher's read and output
        capture, but not its code snapshot, taken before the child started:
        put those in ``.probeignore`` or ``PROBE_IGNORE`` (it warns).
        """
        self._mark_run_process()
        # This process is doing a researcher's run: the scrubber may cache
        # (plan (k); off in every multi-tenant process, see redaction.py).
        from .... import redaction as _redaction

        _redaction.enable_scrub_cache()
        if intent is not None:
            if not isinstance(intent, str) or not intent.strip():
                raise errors.ValidationError(
                    "intent= is empty. Say what this run is meant to show, or drop it."
                )
            run_kw["metadata"] = {**(run_kw.get("metadata") or {}), "intent": intent.strip()}
        if run_kw.get("config") is not None:
            # Plan (c): coerce at the door too, so the retry detection in
            # `_run_impl` compares the config the server will store, not the
            # Namespace or DictConfig it was built from.
            run_kw["config"] = _coerce.to_config(run_kw["config"])
        if started_at is not None:
            # Checked before any request, so a bad time creates no project either.
            started_at = to_iso_time(started_at, label="started_at")
        if run_type is not None:
            # Checked before any request, so a typo creates no project either.
            run_kw["run_type"] = to_run_type(run_type)
        if ignore is not None:
            # Checked before the run exists, so a bad value opens nothing.
            from ....recording_rules import recording_rules as _ignore

            try:
                ignore = _ignore.normalize(ignore)
            except ValueError as exc:
                raise errors.ValidationError(str(exc)) from None
        handle = self._run_impl(
            experiment=experiment,
            question=question,
            name=name,
            project=project,
            experiment_name=experiment_name,
            on_conflict=on_conflict,
            snapshot=snapshot,
            ignore=ignore,
            workspace=workspace,
            # Only forwarded when set: `_run_impl` splats run_kw into `create_run`,
            # and an unconditional `parent_run_id=None` would make every ordinary
            # run look like it declared a null parent.
            **({"parent_run_id": parent_run_id} if parent_run_id is not None else {}),
            **({"parent_relation": parent_relation} if parent_relation is not None else {}),
            **({"started_at": started_at} if started_at is not None else {}),
            **run_kw,
        )
        from probe.sdk.hardware import wiring as hw_integration

        # The run is open. What follows is best-effort capture, never part of
        # opening it, so it is carved out of `probe.init()`'s retry budget.
        with without_patience():
            handle._hw_monitor = hw_integration.maybe_start(self, handle, hw)
            # Read capture is on by default only through `probe.init()`, where the
            # process IS the run's work. Here it is an explicit opt-in: a CLI or a
            # service opening runs on someone's behalf must not record its own
            # config reads as the run's inputs.
            if capture_reads:
                from ....capture import lineage as _inputs

                _inputs.start(
                    handle.id,
                    capture_reads=True,
                    capture_outputs=capture_outputs,
                    client=self,
                    ignore=handle._ignore_rules(),
                )
            if run_kw.get("heartbeat", True) and not run_kw.get("awaiting_attach"):
                handle._start_capture(outputs=outputs, capture_outputs=capture_outputs)
        return handle

    def _run_impl(
        self,
        *,
        experiment: str | None = None,
        question: str | None = None,
        name: str | None = None,
        project: str | ProjectFromEnv | None = None,
        experiment_name: str | None = None,
        on_conflict: str | Rewind = "auto",
        snapshot: bool | None = None,
        ignore: str | list[str] | tuple[str, ...] | None = None,
        workspace: str | None = None,
        **run_kw,
    ) -> Run:
        """Open a run inside an experiment or straight under a project. Resolution,
        ``question=``, ``on_conflict`` and ``snapshot``: DESIGN.md."""
        # project=FROM_ENV: PROBE_PROJECT, this session's project, `probe project use` (home.py).
        home = resolve_run_home(project, experiment, self.settings)
        project, experiment = home.project, home.experiment
        _check_run_arguments(on_conflict, experiment, question, project or home.is_from_env, experiment_name)
        if home.source is None:
            # Still none: the person's pick (asked), under FROM_ENV the daemon's (waited for), or
            # ProjectRequired. Waiting on them is not waiting on the server: init's budget stands still.
            with pause_patience():
                home = find_missing_home(self, home=home)
            project, experiment = home.project, home.experiment
        if not experiment:
            # Before a new project is created for it: a project-direct run joins no group.
            _refuse_group_without_experiment(run_kw, "a project-direct run")
        self.ensure_authenticated()
        mark_home_source(home, run_kw)
        with explain_missing_home(home):
            project_row = self._resolve_run_project(project, experiment, question, workspace, run_kw)
            project_id = project_row["id"] if project_row is not None else None
            exp = None if not experiment else self._resolve_run_experiment(
                experiment, experiment_name, question, project, project_id, run_kw
            )
        if exp is None:
            # Project-direct (0054): the run attaches straight to the project.
            _refuse_group_without_experiment(run_kw, "a project-direct run")
            self._maybe_attach_retry_parent(run_kw, project_id=project_id)
            handle = self._create_run_with_policy(
                lambda kw, nm: self.create_project_run(project_id, nm, **kw),
                run_kw,
                name,
                on_conflict,
                experiment_id=None,
                project_id=project_id,
                home_project_id=project_id,
            )
            print_notice(home, (project_row or {}).get("slug"))
            self._maybe_auto_snapshot(handle, snapshot, ignore)
            return handle
        self._maybe_attach_retry_parent(run_kw, experiment_id=exp["id"])
        handle = self._create_run_with_policy(
            lambda kw, nm: self.create_run(exp["id"], nm, project_id=exp.get("project_id"), **kw),
            run_kw,
            name,
            on_conflict,
            experiment_id=exp["id"],
            project_id=None,
            home_project_id=exp.get("project_id"),
        )
        print_notice(home, exp.get("slug"))
        self._maybe_auto_snapshot(handle, snapshot, ignore)
        return handle

    def _resolve_run_project(
        self,
        project: str | None,
        experiment: str | None,
        question: str | None,
        workspace: str | None,
        run_kw: dict,
    ) -> dict | None:
        """The project a run opens under. A new slug creates it (R23), unless an existing
        experiment is named beside it, which a new project cannot hold (DESIGN.md)."""
        # A project named by an id must exist: never created, whatever `question=` says.
        by_id, slug = self._project_named(project) if project else (None, None)
        known = None
        # Refuse an uncreatable experiment slug BEFORE ensure_project commits a parent,
        # else a refused experiment leaves an orphan project behind.
        if experiment and question is not None:
            # Read-only: the project may not exist yet (ensure_project below
            # creates it), and then the lookup is tenant-wide.
            known = by_id or (self.resolve_project(slug) if slug else None)
            if (
                self.resolve_experiment(experiment, project_id=known["id"] if known else None)
                is None
            ):
                if known is None and not _id_ref(experiment) and not is_new_slug(experiment):
                    # The server would refuse it only after the new project exists (D25).
                    raise errors.ValidationError(
                        f"{experiment!r} is not a slug: a new experiment slug is lowercase words "
                        f"joined by '-', like {to_kebab_slug(experiment) or 'lr-sweep'!r}. Nothing was created."
                    )
                self._guard_creatable("experiment", experiment)
        if not project:
            return None
        if by_id is not None:
            return by_id
        if experiment and question is None:
            # The experiment must exist, so it is filed elsewhere: say so, create nothing.
            return self.resolve_or_raise("project", slug)
        found = known if experiment else self.resolve_project(slug)
        if found is not None:
            return found
        # A new slug is created, kind `general`, near-typos refused; `workspace` files it. Said
        # aloud: a slug that is a typo but no near miss would otherwise make a project unseen.
        created = self.ensure_project(
            slug,
            authored_by=run_kw.get("authored_by"),
            **({"workspace_id": workspace} if workspace else {}),
        )
        _say_created_project(slug)
        return created

    def _resolve_run_experiment(
        self,
        experiment: str,
        experiment_name: str | None,
        question: str | None,
        project: str | None,
        project_id: str | None,
        run_kw: dict,
    ) -> dict:
        """The experiment a run opens in; created only with ``question=`` (DESIGN.md)."""
        if question is not None:
            exp = self.ensure_experiment(
                experiment,
                experiment_name,  # never the slug as a name (DESIGN.md)
                question=question,
                project_id=project_id,
                authored_by=run_kw.get("authored_by"),  # inherits the run's authorship
            )
        else:
            exp = self.resolve_or_raise("experiment", experiment, project_id=project_id)
        # A project that is not the experiment's own is a mistake, not a no-op.
        if project_id and exp.get("project_id") not in (None, project_id):
            raise errors.ValidationError(
                f"experiment {experiment!r} is not in project {project!r}. "
                "Drop the project argument, or name the one it actually belongs to."
            )
        return exp

    @staticmethod
    def _maybe_auto_snapshot(handle: Run, snapshot: bool | None, ignore: Any = None) -> None:
        """Auto-snapshot hook for ``run()`` (design D3). ``snapshot=None``
        follows ``PROBE_AUTO_SNAPSHOT`` (default on); best-effort like
        ``execute()``'s hook -- failure warns rather than losing the run.
        Capture is never a gate, opt-in or otherwise (maintainer decision
        2026-08-06).

        Also where every freshly opened handle takes its ``ignore=`` patterns
        (plan (n)): all three ways `_run_impl` opens a run pass through here,
        and the snapshot below must already honour them."""
        handle._set_ignore(ignore)
        auto = (
            snapshot
            if snapshot is not None
            else (os.environ.get("PROBE_AUTO_SNAPSHOT", "1") != "0")
        )
        if auto:
            try:
                # Best-effort capture is not part of opening the run: carved out
                # of `probe.init()`'s retry budget (plan 2.5), so it keeps its
                # own timeouts however long the create took.
                with without_patience():
                    # In-process: THIS interpreter is the env. No network on this thread:
                    # everything is queued, the record POSTed off it (`_snapshot_at_open`).
                    handle._snapshot_at_open()
            except Exception as exc:
                warnings.warn(
                    f"auto-snapshot failed; run continues uncaptured: {exc}",
                    stacklevel=2,
                )


class RunsResource(Resource):
    """`client.runs`: typed run reads. A listed run is `RunDetailOut` (`RunListRowOut` with `latest_metrics`), or
    `RunListLightOut` / `RunListLightRowOut` with `view="light"`; one run is `RunPageDetailOut`."""

    __slots__ = ()

    def get(self, run_id: str) -> RunPageDetailOut:
        """One run as `GET /v1/runs/{run}` serves it (`Client.get_run`)."""
        return self._to_model(RunPageDetailOut, self._client.get_run(run_id))

    def list(self, **filters: Any) -> Page:
        """A page of runs: `Client.list_runs`'s keywords (`project_id=`, `filter=`, `order=`, `latest_metrics=`,
        `view=`, `limit=`, `cursor=`, ...), its items typed by `view` and `latest_metrics`."""
        page = self._client.list_runs(**filters)
        return self._to_typed_page(_get_row_model(filters), page)

    def iter(self, **filters: Any) -> Iterator[RunDetailOut | RunListRowOut | RunListLightOut | RunListLightRowOut]:
        """Every run `list` would list with these filters, walking every page (`Client.iter_runs`). An `order`
        other than `-created_at` loads every matching row and sorts them locally before the first is yielded."""
        model = _get_row_model(filters)
        for row in self._client.iter_runs(**filters):
            yield self._to_model(model, row)

    def count(self, **filters: Any) -> RunCountsOut:
        """How many runs `list` would list with these filters, in all and per status (`Client.count_runs`)."""
        return self._to_model(RunCountsOut, self._client.count_runs(**filters))

    def table(self, **filters: Any) -> RunTable:
        """Every run `iter` yields with these filters as a `RunTable`: `.rows`, and `.to_pandas()` with columns
        `id, name, status, created_at, config.<path>..., metric.<key>...` (the keys of `latest_metrics=[...]`)."""
        return RunTable(rows=builtins.list(self.iter(**filters)))

    def list_spans(
        self,
        run_id: str,
        *,
        span_type: str | None = None,
        parent_span_id: str | None = None,
        step_from: int | None = None,
        step_to: int | None = None,
        limit: int | None = None,
    ) -> builtins.list[SpanOut]:
        """A run's trajectory spans (`Client.run_spans`)."""
        rows = self._client.run_spans(
            run_id, span_type=span_type, parent_span_id=parent_span_id, step_from=step_from,
            step_to=step_to, limit=limit,
        )
        return self._to_models(SpanOut, rows)

    def get_span(self, span_id: str) -> SpanOut:
        """`Client.get_span` as a `SpanOut`."""
        return self._to_model(SpanOut, self._client.get_span(span_id))

    def list_trials(
        self, run_ref: str, *, cursor: str | None = None, limit: int | None = None,
    ) -> Page:
        """`Client.list_run_trials` with its items as `TrialListOut`; `next_cursor` unchanged."""
        return self._to_typed_page(
            TrialListOut,
            self._client.list_run_trials(run_ref, cursor=cursor, limit=limit),
        )

    def get_trial(self, trial_id: str) -> TrialOut:
        """`Client.get_trial` as a `TrialOut`."""
        return self._to_model(TrialOut, self._client.get_trial(trial_id))

    def get_bundle(self, run_id: str, *, source_read_contract: str | None = None) -> RunBundle:
        """`Client.run_bundle` as a `RunBundle`."""
        return self._to_model(
            RunBundle,
            self._client.run_bundle(run_id, source_read_contract=source_read_contract),
        )

    def get_reproduction(self, run_id: str) -> RunReproduce:
        """`Client.run_reproduce` as a `RunReproduce`."""
        return self._to_model(RunReproduce, self._client.run_reproduce(run_id))

    def get_lineage(self, run_id: str) -> RunLineage:
        """`Client.run_lineage` as a `RunLineage`."""
        return self._to_model(RunLineage, self._client.run_lineage(run_id))

    def list_writers(self, run_id: str) -> builtins.list[WriterOut]:
        """`Client.list_writers` as `WriterOut`s."""
        return self._to_models(WriterOut, self._client.list_writers(run_id))

    @property
    def logs(self) -> LogsResource:
        """A run's printed output: `client.runs.logs.get(run)` is a `RunLogOut`."""
        return LogsResource(self._client)

from probe.sdk.client.resources.runs.reopen.conflict import Rewind  # noqa: E402 -- pieces need each other; the front door loads this one first


def _check_run_arguments(
    on_conflict: str | Rewind,
    experiment: str | None,
    question: str | None,
    project: str | bool | None,
    experiment_name: str | None,
) -> None:
    """Refuse argument combinations ``run()`` cannot honour, before any request. ``project``
    is truthy when one is named or ``FROM_ENV`` will supply it."""
    if not isinstance(on_conflict, Rewind) and on_conflict not in (
        "auto",
        "error",
        "supersede",
        "resume",
    ):
        raise errors.ValidationError(
            f'on_conflict={on_conflict!r} is not a policy. Use "auto" '
            '(resume a dead incumbent, else 409), "resume" (demand it), '
            '"supersede" (retry lineage under a fresh -rN external_id), '
            '"error" (the bare 409), or probe.Rewind(step=N) — resume '
            "from an earlier checkpoint, overwriting the run's record "
            "from step N onward (0185)."
        )
    if experiment_name is not None and question is None:
        raise errors.ValidationError(
            "experiment_name only titles an experiment run() CREATES, and "
            "creation needs a question. Pass question=, or rename an "
            "existing experiment with update_experiment()."
        )
    if question is not None and not experiment:
        raise errors.ValidationError(
            "question= creates an experiment, so it needs an experiment "
            "slug. A project-direct run has no experiment to hold one."
        )
    if question is not None and not project:
        raise errors.ValidationError(
            "creating an experiment needs a project. Pass project=\"<slug>\" (a new slug "
            "creates the project), or project=probe.FROM_ENV."
        )
    if question is not None and not question.strip():
        # `question=args.question or ""` lands here; an empty string once committed a
        # PROJECT before failing on the experiment (DESIGN.md).
        raise errors.ValidationError(
            "question= is empty. Creating an experiment needs one that says "
            "something: what do you expect this to show? Pass a real "
            "question, or drop the argument to open an existing experiment."
        )


def _say_created_project(slug: str) -> None:
    """One stderr line for a project a run's new slug created (R23); never raises."""
    try:
        print(f"probe: created project {slug} for this run (kind general)", file=sys.stderr, flush=True)
    except (OSError, ValueError):
        pass


def _refuse_group_without_experiment(run_kw: dict, who: str) -> None:
    """Run groups are experiment-anchored: refuse a group on a run with no experiment."""
    if run_kw.get("group_id") is not None:
        raise errors.ValidationError(
            "a group needs an experiment: run groups are "
            f"experiment-anchored, so {who} cannot join "
            "one. Name the experiment or drop the group."
        )
    run_kw.pop("group_id", None)


def _get_row_model(filters: dict) -> type[BaseModel]:
    """The row model `GET /v1/runs` answers for these keywords: light or full, with `latest_metrics` or not (an
    ordered `iter` by a metric asks for it)."""
    order = filters.get("order")
    has_metrics = bool(filters.get("latest_metrics")) or (
        order not in (None, "", DEFAULT_ORDER, RECENT_ORDER) and parse_run_order(order).metric_key is not None
    )
    if filters.get("view") == "light":
        return RunListLightRowOut if has_metrics else RunListLightOut
    return RunListRowOut if has_metrics else RunDetailOut
