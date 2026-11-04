"""Jobs — the deployed units of work in a workspace."""

from __future__ import annotations

# Python internals
from dataclasses import dataclass
from datetime import datetime
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncIterable,
    Awaitable,
    Generic,
    Iterable,
    Mapping,
    Sequence,
    overload,
)

# Other libraries
from typing_extensions import ReadOnly, TypedDict

# Current package
from dlthub_sdk._glue.base import Collection, Entity
from dlthub_sdk._glue.context import Async, Listing, M, Sync, _Ctx
from dlthub_sdk._glue.enums import EntityKind, StrEnum
from dlthub_sdk._glue.keep import KEEP, Keep
from dlthub_sdk.domain.job_runs import JobRun, JobRuns
from dlthub_sdk.errors import NotFound

if TYPE_CHECKING:
    # Typing only: domain never imports _gen at runtime.
    # Current package
    from dlthub_sdk._gen.api.models import (
        DeployWorkspaceResponse,
        DetailedJobResponse,
        JobResponse,
        ListPageDetailedJobResponse,
        TriggeredJob,
        TriggerJobsResponse,
    )

    #: get/list return the detailed model, pause/resume the plain one.
    JobPayload = DetailedJobResponse | JobResponse


class JobType(StrEnum):
    """How a job executes."""

    BATCH = "batch"
    """Runs to completion and exits."""
    INTERACTIVE = "interactive"
    """Serves an interactive session."""
    STREAM = "stream"
    """Runs continuously."""
    UNKNOWN = "unknown"
    """A type this SDK version does not know."""


#: A manual trigger, in the canonical form dlt's ``manual()`` produces. Every job
#: accepts it: nothing checks a trigger against the job definition's own list.
MANUAL_TRIGGER = "manual:"


class TriggerStatus(StrEnum):
    """What became of a request to run a job."""

    TRIGGERED = "triggered"
    """A run was created."""
    SKIPPED_PAUSED = "skipped_paused"
    """The job's schedule is suspended."""
    SKIPPED_FRESH = "skipped_fresh"
    """A job its freshness constraints depend on is not fresh yet; ``reasons`` names
    which.
    """
    SKIPPED_ALREADY_COVERED = "skipped_already_covered"
    """A completed run already covers this period."""
    SKIPPED_OUT_OF_INTERVAL = "skipped_out_of_interval"
    """Outside the job's configured window."""
    SKIPPED_UPSTREAM_PENDING = "skipped_upstream_pending"
    """A job it depends on is triggered in the same request; this job runs once that one
    completes.
    """
    SKIPPED_CONCURRENCY_LIMIT = "skipped_concurrency_limit"
    """The job already has as many active runs as its concurrency limit allows."""
    SKIPPED_ORG_CONCURRENCY_LIMIT = "skipped_org_concurrency_limit"
    """The organization is at its run limit."""
    SKIPPED_MINUTES_LIMIT = "skipped_minutes_limit"
    """The plan's compute minutes are exhausted."""
    SKIPPED_TRIAL_EXPIRED = "skipped_trial_expired"
    """The trial has ended."""
    SKIPPED_WORKSPACE_ARCHIVED = "skipped_workspace_archived"
    """The workspace is archived."""
    UNKNOWN = "unknown"
    """A status this SDK version does not know."""


@dataclass(frozen=True)
class TriggerResult:
    """The outcome of asking a job to run through :meth:`Jobs.trigger`.

    Asking does not guarantee a run: the platform skips a trigger it cannot
    honour and says why, so check :attr:`started` before expecting ``job_run_id``.
    A dry run creates no run, so ``job_run_id`` is ``None`` there too.
    """

    job_ref: str
    """The job reference of the matched job."""
    job_id: str
    """The ID of the matched job."""
    # doc: sdk
    status: TriggerStatus
    """Whether a run started, or why it did not."""
    reasons: tuple[str, ...]
    """Human-readable reasons for a skip, e.g. which upstream jobs are not fresh; `None`
    when the job was triggered or no reasons were recorded.
    """
    trigger: str
    """The trigger the job fires with."""
    job_run_id: str | None
    """The ID of the created run; `None` in dry-run mode or when skipped."""
    job_run_number: int | None
    """Number of the run within its job, counting up from 1; numbers repeat across jobs.
    """
    matched_triggers: tuple[str, ...]
    """Every trigger that selected this job: its default trigger when named in
    `job_ids`, plus any selector matches.
    """

    @property
    def started(self) -> bool:
        """Whether the platform started a run, or would in a dry run.

        A dry run creates no run, so ``job_run_id`` is ``None`` there too.

        Returns:
            True only for :attr:`TriggerStatus.TRIGGERED`.
        """
        return self.status is TriggerStatus.TRIGGERED

    @staticmethod
    def _all_from_payload(
        ctx: _Ctx[Any], payload: TriggerJobsResponse, refs: Sequence[str] | None
    ) -> tuple[TriggerResult, ...]:
        jobs = [*payload.succeeded, *payload.skipped]
        # A job archived after its ref was resolved; once a run started, reporting it
        # missing would read as though nothing ran.
        if payload.failed and not payload.succeeded:
            answered = {job.job_ref for job in jobs}
            missing = [ref for ref in refs or () if ref not in answered]
            raise NotFound(
                EntityKind.JOB, missing[0] if missing else payload.failed[0].ref
            )
        return tuple(TriggerResult._from_payload(ctx, job) for job in jobs)

    @staticmethod
    def _from_payload(_ctx: _Ctx[Any], payload: TriggeredJob) -> TriggerResult:
        # An omitted status means the job was triggered; the generated model's
        # default says so, but its sentinel would str() into UNKNOWN.
        status = payload.status
        reasons = payload.reasons
        return TriggerResult(
            job_ref=payload.job_ref,
            job_id=str(payload.job_id),
            status=(
                TriggerStatus(str(status))
                if isinstance(status, str)
                else TriggerStatus.TRIGGERED
            ),
            reasons=tuple(reasons) if isinstance(reasons, list) else (),
            trigger=payload.trigger,
            job_run_id=str(payload.job_run_id) if payload.job_run_id else None,
            # The sentinel and None both lack `.number`, so one getattr covers both.
            job_run_number=(
                number
                if isinstance(number := getattr(payload.job_run, "number", None), int)
                else None
            ),
            matched_triggers=tuple(payload.matched_triggers),
        )


class DeployManifest(TypedDict):
    """The part of a dlt deployment manifest a deploy reads.

    Read-only and a subset, so dlt's own manifest type satisfies it structurally
    and the SDK needs no dependency on dlt to say what it accepts.
    """

    engine_version: ReadOnly[int]
    """Manifest engine version the definitions were written for."""
    jobs: ReadOnly[Sequence[Mapping[str, Any]]]
    """Job definitions, exactly as the manifest carries them."""


@dataclass(frozen=True)
class DeployReport(Generic[M]):
    """What a manifest deploy did to a workspace's jobs."""

    added: tuple[Job[M], ...]
    """Jobs the manifest introduced."""
    updated: tuple[Job[M], ...]
    """Jobs it changed, at their new version."""
    unchanged: tuple[Job[M], ...]
    """Jobs it left alone."""
    archived: tuple[Job[M], ...]
    """Jobs it removed, which happens only for a module deploy."""
    warnings: tuple[str, ...]
    """Always empty at present."""
    deployment_module: str | None
    """The deployment module the deploy was scoped to."""

    @staticmethod
    def _from_payload(
        ctx: _Ctx[Any], payload: DeployWorkspaceResponse
    ) -> DeployReport[Any]:
        def jobs(rows: Sequence[Any]) -> tuple[Job[Any], ...]:
            return tuple(Job._from_payload(ctx, row) for row in rows)

        def done(outcome: str) -> tuple[Job[Any], ...]:
            return jobs(
                [s.job for s in payload.job_receipt.succeeded if s.outcome == outcome]
            )

        return DeployReport(
            added=done("created"),
            updated=done("updated"),
            unchanged=jobs([s.job for s in payload.job_receipt.skipped]),
            archived=done("archived"),
            warnings=tuple(payload.warnings),
            deployment_module=(
                payload.deployment_module
                if isinstance(payload.deployment_module, str)
                else None
            ),
        )


@dataclass(frozen=True, repr=False)
class Job(Entity[M]):
    """A deployed job in a workspace."""

    job_ref: str
    """Canonical job reference, unique per workspace."""
    id: str
    """Unique ID (a UUID)."""
    name: str | None
    """Display name for the job."""
    job_type: JobType
    """The type of the job: batch, interactive, or stream."""
    is_paused: bool
    """Whether the job's scheduled runs are paused. The scheduler does not start it,
    including a scheduled run that was waiting for its upstream jobs; manual runs,
    runs started by a trigger request, and runs started by another job's success or
    failure still run. Only a job with `next_scheduled_run_at` can be paused, and a
    deploy that removes the schedule clears the pause.
    """
    is_archived: bool
    """Whether the job is archived. Archived jobs cannot be run and their public URL
    stops working.
    """
    version: int
    """Version number, starting at 1 and incremented by each update to the job: a job's
    current version, or a job version's own number.
    """
    public_url: str | None
    """The public URL where the job can be accessed without authentication; `None` when
    the job is not published. It does not work while the job is archived.
    """
    job_url: str | None
    """The URL of the job in the web app for an interactive job; `None` otherwise."""
    default_trigger: str | None
    """The trigger fired when a run is started without naming one, computed from the job
    definition.
    """
    triggers: tuple[str, ...]
    """Every trigger the job answers to, computed from its definition; selectors match
    against these.
    """
    next_scheduled_run_at: datetime | None
    """When the job is next scheduled to run; `None` if it has no schedule."""
    # doc: sdk
    job_definition: Mapping[str, Any]
    """The job definition from the manifest, migrated to the platform's current format.
    Left opaque: it is dlt's own nested structure, and the SDK models none of it — as
    with the definitions ``Jobs.deploy_manifest`` accepts.
    """
    created_at: datetime
    """When it was created."""

    _identity = ("job_ref", "id")
    _kind = EntityKind.JOB

    @overload
    def pause(self: Job[Sync]) -> Job[Sync]: ...

    @overload
    def pause(self: Job[Async]) -> Awaitable[Job[Async]]: ...

    def pause(self) -> Job[Any] | Awaitable[Job[Any]]:
        """Suspend the job's schedule.

        Pausing a paused job changes nothing.

        Returns:
            A fresh snapshot with ``is_paused`` set; awaitable in async mode.

        Raises:
            BadRequest: The request was rejected as invalid; `message`, `code` and
                `fields` say why.
            Conflict: The current state does not allow the call, e.g. the workspace is
                archived; `code` and `message` say why.
            NotFound: The job no longer exists.
        """
        workspace_id = self._ctx.require_workspace()
        job_id = self.id
        return self._ctx.run(
            lambda t: t.pause_job(workspace_id=workspace_id, job_id=job_id),
            Job._from_payload,
        )

    @overload
    def resume(self: Job[Sync]) -> Job[Sync]: ...

    @overload
    def resume(self: Job[Async]) -> Awaitable[Job[Async]]: ...

    def resume(self) -> Job[Any] | Awaitable[Job[Any]]:
        """Resume the job's schedule.

        Resuming a job that is not paused changes nothing.

        Returns:
            A fresh snapshot with ``is_paused`` cleared; awaitable in async mode.

        Raises:
            Conflict: The current state does not allow the call, e.g. the workspace is
                archived; `code` and `message` say why.
            NotFound: The job no longer exists.
        """
        workspace_id = self._ctx.require_workspace()
        job_id = self.id
        return self._ctx.run(
            lambda t: t.resume_job(workspace_id=workspace_id, job_id=job_id),
            Job._from_payload,
        )

    @overload
    def publish(self: Job[Sync]) -> Job[Sync]: ...

    @overload
    def publish(self: Job[Async]) -> Awaitable[Job[Async]]: ...

    def publish(self) -> Job[Any] | Awaitable[Job[Any]]:
        """Expose the job on a public trigger URL.

        Calling it again issues a new URL and invalidates the previous one.

        Returns:
            A fresh snapshot carrying ``public_url``; awaitable in async mode.

        Raises:
            Conflict: The current state does not allow the call, e.g. the workspace is
                archived; `code` and `message` say why.
            NotFound: The job no longer exists.
        """
        workspace_id = self._ctx.require_workspace()
        job_id = self.id
        return self._ctx.run(
            lambda t: t.publish_job(workspace_id=workspace_id, job_id=job_id),
            Job._from_payload,
        )

    @overload
    def unpublish(self: Job[Sync]) -> Job[Sync]: ...

    @overload
    def unpublish(self: Job[Async]) -> Awaitable[Job[Async]]: ...

    def unpublish(self) -> Job[Any] | Awaitable[Job[Any]]:
        """Withdraw the job's public trigger URL.

        Unpublishing a job that is not published changes nothing.

        Returns:
            A fresh snapshot with ``public_url`` cleared; awaitable in async mode.

        Raises:
            Conflict: The current state does not allow the call, e.g. the workspace is
                archived; `code` and `message` say why.
            NotFound: The job no longer exists.
        """
        workspace_id = self._ctx.require_workspace()
        job_id = self.id
        return self._ctx.run(
            lambda t: t.unpublish_job(workspace_id=workspace_id, job_id=job_id),
            Job._from_payload,
        )

    @overload
    def archive(self: Job[Sync]) -> Job[Sync]: ...

    @overload
    def archive(self: Job[Async]) -> Awaitable[Job[Async]]: ...

    def archive(self) -> Job[Any] | Awaitable[Job[Any]]:
        """Retire the job so it can no longer run, manually or on schedule.

        Its schedule, default trigger and pause are cleared. List it with
        ``archived=True``. Archiving an archived job changes nothing.

        Returns:
            A fresh snapshot with ``is_archived`` set; awaitable in async mode.

        Raises:
            Conflict: The current state does not allow the call, e.g. the workspace is
                archived; `code` and `message` say why.
            NotFound: The job no longer exists.
        """
        workspace_id = self._ctx.require_workspace()
        job_id = self.id
        return self._ctx.run(
            lambda t: t.archive_job(workspace_id=workspace_id, job_id=job_id),
            Job._from_payload,
        )

    @overload
    def unarchive(self: Job[Sync]) -> Job[Sync]: ...

    @overload
    def unarchive(self: Job[Async]) -> Awaitable[Job[Async]]: ...

    def unarchive(self) -> Job[Any] | Awaitable[Job[Any]]:
        """Let an archived job run again.

        Its schedule and default trigger are restored from its definition; a
        pause is not. Unarchiving a live job changes nothing.

        Returns:
            A fresh snapshot with ``is_archived`` cleared; awaitable in async mode.

        Raises:
            Conflict: The current state does not allow the call, e.g. the workspace is
                archived; `code` and `message` say why.
            NotFound: The job no longer exists.
        """
        workspace_id = self._ctx.require_workspace()
        job_id = self.id
        return self._ctx.run(
            lambda t: t.unarchive_job(workspace_id=workspace_id, job_id=job_id),
            Job._from_payload,
        )

    @overload
    def start_run(
        self: Job[Sync],
        *,
        trigger: str = MANUAL_TRIGGER,
        profile: str | None | Keep = KEEP,
        refresh: bool = False,
        skip_freshness: bool = False,
    ) -> JobRun[Sync]: ...

    @overload
    def start_run(
        self: Job[Async],
        *,
        trigger: str = MANUAL_TRIGGER,
        profile: str | None | Keep = KEEP,
        refresh: bool = False,
        skip_freshness: bool = False,
    ) -> Awaitable[JobRun[Async]]: ...

    def start_run(
        self,
        *,
        trigger: str = MANUAL_TRIGGER,
        profile: str | None | Keep = KEEP,
        refresh: bool = False,
        skip_freshness: bool = False,
    ) -> JobRun[Any] | Awaitable[JobRun[Any]]:
        """Start a run of this job.

        A run the platform declines to start raises, with its ``code`` naming why
        and the platform's reasons in ``fields``.

        Args:
            trigger: Which trigger to fire, in canonical form. Defaults to
                ``"manual:"``. Only the form is validated, so a trigger
                the job definition does not declare is still honoured.
            profile: Profile to run under. Omit for the job's default.
            refresh: Start as a refresh: the job's progress goes back to its
                interval start and the run receives ``refresh=True`` in its run
                context; what to reload is up to the job's code. Downstream jobs
                that depend on its freshness are reset too. Ignored when the job's
                ``refresh_propagation`` is ``"block"``.
            skip_freshness: Start even when the upstream jobs this job's
                freshness constraints name are not fresh.

        Returns:
            The run that started; awaitable in async mode.

        Raises:
            BadRequest: The request was rejected as invalid; `message`, `code` and
                `fields` say why.
            Conflict: The platform declined to start a run, e.g. an upstream is
                not fresh, the job is outside its interval, or a concurrency
                limit is reached; ``code`` says which. Also raised when the
                workspace is archived.
            NotAuthorized: The caller lacks the access this call needs; `message` says
                why.
            NotFound: No such job in this workspace.
            ScopeMissing: Reached without a workspace in scope.
        """
        workspace_id = self._ctx.require_workspace()
        job_id = self.id
        return self._ctx.run(
            lambda t: t.create_run(
                workspace_id=workspace_id,
                job_id=job_id,
                trigger=trigger,
                profile=profile,
                refresh=refresh,
                skip_freshness=skip_freshness,
            ),
            JobRun._from_payload,
        )

    @property
    def runs(self) -> JobRuns[M]:
        """This job's runs.

        Listing, counting and :meth:`JobRuns.latest` default to this job.

        Returns:
            A collection scoped to this job, so its methods need no ``job_id``.
        """
        return JobRuns(self._ctx)

    @staticmethod
    def _from_payload(ctx: _Ctx[Any], payload: JobPayload) -> Job[Any]:
        return Job._bind(
            ctx.narrow(job_id=str(payload.id)),
            Job(
                job_ref=payload.job_ref,
                id=str(payload.id),
                name=payload.name if isinstance(payload.name, str) else None,
                job_type=JobType(str(payload.job_type)),
                is_paused=payload.is_paused
                if isinstance(payload.is_paused, bool)
                else False,
                is_archived=(
                    payload.is_archived
                    if isinstance(payload.is_archived, bool)
                    else False
                ),
                version=payload.version,
                public_url=payload.public_url,
                job_url=payload.job_url,
                default_trigger=(
                    payload.default_trigger
                    if isinstance(payload.default_trigger, str)
                    else None
                ),
                triggers=(
                    tuple(payload.triggers)
                    if isinstance(payload.triggers, list)
                    else ()
                ),
                next_scheduled_run_at=(
                    payload.next_scheduled_run_at
                    if isinstance(payload.next_scheduled_run_at, datetime)
                    else None
                ),
                job_definition=payload.job_definition.to_dict(),
                created_at=payload.created_at,
            ),
        )


class Jobs(Collection[M]):
    """The jobs of one workspace."""

    _entity = Job

    def _listing(self, archived: bool | Keep) -> Listing[DetailedJobResponse]:
        workspace_id = self._ctx.require_workspace()
        return lambda t, limit, offset: t.list_jobs(
            workspace_id=workspace_id,
            limit=limit,
            offset=offset,
            archived=archived,
            ref=None,
        )

    @overload
    def trigger(
        self: Jobs[Sync],
        *,
        refs: Sequence[str] | None = None,
        selectors: Sequence[str] | None = None,
        profile: str | None | Keep = KEEP,
        refresh: bool = False,
        dry_run: bool = False,
    ) -> tuple[TriggerResult, ...]: ...

    @overload
    def trigger(
        self: Jobs[Async],
        *,
        refs: Sequence[str] | None = None,
        selectors: Sequence[str] | None = None,
        profile: str | None | Keep = KEEP,
        refresh: bool = False,
        dry_run: bool = False,
    ) -> Awaitable[tuple[TriggerResult, ...]]: ...

    def trigger(
        self,
        *,
        refs: Sequence[str] | None = None,
        selectors: Sequence[str] | None = None,
        profile: str | None | Keep = KEEP,
        refresh: bool = False,
        dry_run: bool = False,
    ) -> tuple[TriggerResult, ...] | Awaitable[tuple[TriggerResult, ...]]:
        """Ask several jobs to run, by ref or by selector.

        Unlike :meth:`Job.start_run`, this does not take a trigger of its own.
        A job named in ``refs`` fires its ``default_trigger`` (or a manual
        trigger when it has none); a job matched by ``selectors`` fires the
        trigger it matched, preferring its ``default_trigger`` when that matched
        too.

        Args:
            refs: Job refs to trigger. Each resolves to exactly one job.
            selectors: Trigger patterns to match, ``fnmatch``-style — for
                example ``"tag:backfill"``, ``"schedule:*"``, ``"manual:jobs.mod.*"``.
            profile: Profile for every run started. Omit for each job's default.
            refresh: Start the jobs that do start as a refresh, as for
                :meth:`Job.start_run`. Downstream jobs that depend on their
                freshness are reset too. Ignored for a job whose
                ``refresh_propagation`` is ``"block"``.
            dry_run: Report what would be triggered without starting anything.

        Returns:
            One result per matched job; awaitable in async mode. Started jobs
            come first, then skipped ones, each in the platform's dependency
            order. A job the platform declined is present too, with its reason
            — see :class:`TriggerResult`.

        Raises:
            Conflict: The current state does not allow the call, e.g. the workspace is
                archived; `code` and `message` say why.
            NotAuthorized: The caller lacks the access this call needs; `message` says
                why.
            NotFound: A ref names no job in this workspace, or only an archived
                one.
            ScopeMissing: Reached without a workspace in scope.
            ValueError: Neither ``refs`` nor ``selectors`` was given.
        """
        if not refs and not selectors:
            raise ValueError("pass refs, selectors, or both — one must be non-empty")
        workspace_id = self._ctx.require_workspace()
        # Snapshot: in async mode the lambda does not run until the coroutine is
        # awaited, by which time the caller may have mutated what they passed.
        wanted = None if refs is None else list(refs)
        patterns = None if selectors is None else list(selectors)
        return self._ctx.run(
            lambda t: t.trigger_jobs(
                workspace_id=workspace_id,
                job_refs=wanted,
                selectors=patterns,
                profile=profile,
                refresh=refresh,
                dry_run=dry_run,
            ),
            lambda ctx, payload: TriggerResult._all_from_payload(ctx, payload, wanted),
        )

    @overload
    def deploy_manifest(
        self: Jobs[Sync],
        manifest: DeployManifest,
        *,
        manifest_hash: str,
        deployment_module: str | None = None,
        description: str | None | Keep = KEEP,
        dry_run: bool = False,
    ) -> DeployReport[Sync]: ...

    @overload
    def deploy_manifest(
        self: Jobs[Async],
        manifest: DeployManifest,
        *,
        manifest_hash: str,
        deployment_module: str | None = None,
        description: str | None | Keep = KEEP,
        dry_run: bool = False,
    ) -> Awaitable[DeployReport[Async]]: ...

    def deploy_manifest(
        self,
        manifest: DeployManifest,
        *,
        manifest_hash: str,
        deployment_module: str | None = None,
        description: str | None | Keep = KEEP,
        dry_run: bool = False,
    ) -> DeployReport[Any] | Awaitable[DeployReport[Any]]:
        """Reconcile the workspace's jobs against a deployment manifest.

        The job definitions are passed through as the manifest carries them.
        Upload the code with :meth:`Deployments.upload` first — this registers
        what runs, not what it runs from.

        Args:
            manifest: The manifest to deploy, as dlt built it. Its jobs and
                engine version travel together, so the two cannot be crossed.
            manifest_hash: Content hash of that manifest, from dlt's
                ``generate_manifest_hash``.
            deployment_module: The deployment module this deploy claims. ``None``, the
                default, is an ad-hoc deploy: jobs are added and updated but
                never archived. Naming one lets the platform archive the jobs
                that module owns and the manifest no longer lists.
            description: Workspace description, applied only when ``deployment_module``
                is ``"__deployment__"``. Omit, or pass ``None``, to leave it as
                it is.
            dry_run: Report the plan without persisting it. Jobs in a dry-run
                report that are not yet deployed carry a placeholder ``id`` and
                cannot be acted on.

        Returns:
            What was added, updated, left alone and archived; awaitable in
            async mode.

        Raises:
            BadRequest: The request was rejected as invalid; `message`, `code` and
                `fields` say why.
            Conflict: The current state does not allow the call, e.g. the workspace is
                archived; `code` and `message` say why.
            NotAuthorized: The caller lacks the access this call needs; `message` says
                why.
            ScopeMissing: Reached without a workspace in scope.
            ValueError: The manifest lists no jobs.
        """
        definitions = list(manifest["jobs"])
        if not definitions:
            raise ValueError("the manifest lists no jobs to deploy")
        engine_version = manifest["engine_version"]
        workspace_id = self._ctx.require_workspace()
        return self._ctx.run(
            lambda t: t.deploy_manifest(
                workspace_id=workspace_id,
                jobs=definitions,
                manifest_hash=manifest_hash,
                engine_version=engine_version,
                deployment_module=deployment_module,
                description=description,
                dry_run=dry_run,
            ),
            DeployReport._from_payload,
        )

    @overload
    def get(self: Jobs[Sync], *, id: str) -> Job[Sync]: ...

    @overload
    def get(self: Jobs[Async], *, id: str) -> Awaitable[Job[Async]]: ...

    def get(self, *, id: str) -> Job[Any] | Awaitable[Job[Any]]:
        """Return one job by id.

        Args:
            id: The job's uuid. To look a job up by its ref, use
                :meth:`get_by_ref`.

        Returns:
            The job; awaitable in async mode.

        Raises:
            BadRequest: The request was rejected as invalid; `message`, `code` and
                `fields` say why.
            NotFound: No such job in this workspace.
            ScopeMissing: Reached without a workspace in scope.
        """
        workspace_id = self._ctx.require_workspace()
        return self._ctx.run(
            lambda t: t.get_job(workspace_id=workspace_id, job_id=id),
            Job._from_payload,
        )

    @overload
    def get_by_ref(self: Jobs[Sync], ref: str) -> Job[Sync]: ...

    @overload
    def get_by_ref(self: Jobs[Async], ref: str) -> Awaitable[Job[Async]]: ...

    def get_by_ref(self, ref: str) -> Job[Any] | Awaitable[Job[Any]]:
        """Return one job by its ref, archived or not.

        Args:
            ref: The job ref, e.g. ``jobs.load``.

        Returns:
            The job; awaitable in async mode.

        Raises:
            NotFound: No job in this workspace has that ref.
            ScopeMissing: Reached without a workspace in scope.
        """
        workspace_id = self._ctx.require_workspace()

        def parse(ctx: _Ctx[Any], payload: ListPageDetailedJobResponse) -> Job[Any]:
            if not payload.items:
                raise NotFound(EntityKind.JOB, ref)
            return Job._from_payload(ctx, payload.items[0])

        return self._ctx.run(
            lambda t: t.list_jobs(
                workspace_id=workspace_id, limit=1, offset=0, archived=KEEP, ref=ref
            ),
            parse,
        )

    @overload
    def count(self: Jobs[Sync], *, archived: bool | Keep = KEEP) -> int: ...

    @overload
    def count(self: Jobs[Async], *, archived: bool | Keep = KEEP) -> Awaitable[int]: ...

    def count(self, *, archived: bool | Keep = KEEP) -> int | Awaitable[int]:
        """Return how many jobs the workspace has, without fetching them.

        Args:
            archived: As for :meth:`list`.

        Returns:
            The job count; awaitable in async mode. Saturates at 10,001, so a
            value equal to that means "at least this many".

        Raises:
            ScopeMissing: Reached without a workspace in scope.
        """
        return self._ctx.count(self._listing(archived))

    @overload
    def list(
        self: Jobs[Sync],
        *,
        archived: bool | Keep = KEEP,
        limit: int | None = None,
        offset: int = 0,
    ) -> Iterable[Job[Sync]]: ...

    @overload
    def list(
        self: Jobs[Async],
        *,
        archived: bool | Keep = KEEP,
        limit: int | None = None,
        offset: int = 0,
    ) -> AsyncIterable[Job[Async]]: ...

    def list(
        self,
        *,
        archived: bool | Keep = KEEP,
        limit: int | None = None,
        offset: int = 0,
    ) -> Iterable[Job[Any]] | AsyncIterable[Job[Any]]:
        """Yield the jobs in the workspace, paging lazily.

        Platform errors are raised when iteration begins, not by this call.

        Args:
            archived: Keep only archived jobs, or only live ones. Omit for both,
                which is what the platform returns when nothing filters.
            limit: Return at most this many jobs. ``None`` walks to the end, or
                to row 10,100, past which the platform does not page.
            offset: Skip this many jobs, server-side.

        Returns:
            An iterable of jobs; async-iterable in async mode.

        Raises:
            ScopeMissing: Reached without a workspace in scope.
            ValueError: A negative ``limit`` or ``offset``.
        """
        return self._ctx.page(
            self._listing(archived), Job._from_payload, limit=limit, offset=offset
        )
