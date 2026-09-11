"""Jobs — what the platform API calls a script."""

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
from dlthub_sdk.domain.job_runs import JobRuns

if TYPE_CHECKING:
    # Typing only: domain never imports _gen at runtime.
    # Current package
    from dlthub_sdk._gen.api.models import (
        DeployManifestResponse,
        DetailedScriptResponse,
        ScriptResponse,
        TriggeredJob,
        TriggerJobsResponse,
    )

    #: get/list return the detailed model, pause/resume the plain one.
    JobPayload = DetailedScriptResponse | ScriptResponse


class JobType(StrEnum):
    """How a job executes.

    Attributes:
        BATCH: Runs to completion and exits.
        INTERACTIVE: Serves an interactive session.
        STREAM: Runs continuously.
        UNKNOWN: A type this SDK version does not know.
    """

    BATCH = "batch"
    INTERACTIVE = "interactive"
    STREAM = "stream"
    UNKNOWN = "unknown"


#: A manual trigger, in the canonical form dlt's ``manual()`` produces. Every job
#: accepts it: nothing checks a trigger against the job definition's own list.
MANUAL_TRIGGER = "manual:"


class TriggerStatus(StrEnum):
    """What became of a request to run a job.

    Attributes:
        TRIGGERED: A run was created.
        SKIPPED_PAUSED: The job's schedule is suspended.
        SKIPPED_FRESH: Its data is already current.
        SKIPPED_ALREADY_COVERED: Another run already covers this interval.
        SKIPPED_OUT_OF_INTERVAL: Outside the job's configured window.
        SKIPPED_UPSTREAM_PENDING: A job it depends on has not finished.
        SKIPPED_CONCURRENCY_LIMIT: The workspace is at its run limit.
        SKIPPED_ORG_CONCURRENCY_LIMIT: The organization is at its run limit.
        SKIPPED_MINUTES_LIMIT: The plan's compute minutes are exhausted.
        SKIPPED_TRIAL_EXPIRED: The trial has ended.
        SKIPPED_WORKSPACE_ARCHIVED: The workspace is archived.
        UNKNOWN: A status this SDK version does not know.
    """

    TRIGGERED = "triggered"
    SKIPPED_PAUSED = "skipped_paused"
    SKIPPED_FRESH = "skipped_fresh"
    SKIPPED_ALREADY_COVERED = "skipped_already_covered"
    SKIPPED_OUT_OF_INTERVAL = "skipped_out_of_interval"
    SKIPPED_UPSTREAM_PENDING = "skipped_upstream_pending"
    SKIPPED_CONCURRENCY_LIMIT = "skipped_concurrency_limit"
    SKIPPED_ORG_CONCURRENCY_LIMIT = "skipped_org_concurrency_limit"
    SKIPPED_MINUTES_LIMIT = "skipped_minutes_limit"
    SKIPPED_TRIAL_EXPIRED = "skipped_trial_expired"
    SKIPPED_WORKSPACE_ARCHIVED = "skipped_workspace_archived"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class TriggerResult:
    """The outcome of asking a job to run.

    Asking does not guarantee a run: the platform skips a trigger it cannot
    honour and says why, so check :attr:`started` before expecting ``run_id``.

    Attributes:
        job_ref: The job that was asked to run.
        status: Whether a run started, or why it did not.
        reasons: The platform's explanation of a skip, when it gave one.
        trigger: The single trigger the platform picked for this request.
        run_id: The run that started, or ``None`` when none did.
        run_number: That run's number within the workspace, which is how humans
            refer to it. ``None`` for a dry run, which creates no run.
        matched_triggers: Triggers in the job definition that the request matched.
    """

    job_ref: str
    status: TriggerStatus
    reasons: tuple[str, ...]
    trigger: str
    run_id: str | None
    run_number: int | None
    matched_triggers: tuple[str, ...]

    @property
    def started(self) -> bool:
        """Whether a run actually started.

        Returns:
            True only for :attr:`TriggerStatus.TRIGGERED`.
        """
        return self.status is TriggerStatus.TRIGGERED

    @staticmethod
    def _all_from_payload(
        ctx: _Ctx[Any], payload: TriggerJobsResponse
    ) -> tuple[TriggerResult, ...]:
        return tuple(TriggerResult._from_payload(ctx, job) for job in payload.triggered)

    @staticmethod
    def _from_payload(_ctx: _Ctx[Any], payload: TriggeredJob) -> TriggerResult:
        # An omitted status means the job was triggered; the generated model's
        # default says so, but its sentinel would str() into UNKNOWN.
        status = payload.status
        reasons = payload.reasons
        return TriggerResult(
            job_ref=payload.job_ref,
            status=(
                TriggerStatus(str(status))
                if isinstance(status, str)
                else TriggerStatus.TRIGGERED
            ),
            reasons=tuple(reasons) if isinstance(reasons, list) else (),
            trigger=payload.trigger,
            run_id=str(payload.run_id) if payload.run_id else None,
            # The sentinel and None both lack `.number`, so one getattr covers both.
            run_number=(
                number
                if isinstance(number := getattr(payload.run, "number", None), int)
                else None
            ),
            matched_triggers=tuple(payload.matched_triggers),
        )


class DeployManifest(TypedDict):
    """The part of a dlt deployment manifest a deploy reads.

    Read-only and a subset, so dlt's own manifest type satisfies it structurally
    and the SDK needs no dependency on dlt to say what it accepts.

    Attributes:
        engine_version: Manifest engine version the definitions were written for.
        jobs: Job definitions, exactly as the manifest carries them.
    """

    engine_version: ReadOnly[int]
    jobs: ReadOnly[Sequence[Mapping[str, Any]]]


@dataclass(frozen=True)
class DeployReport(Generic[M]):
    """What a manifest deploy did to a workspace's jobs.

    Attributes:
        added: Jobs the manifest introduced.
        updated: Jobs it changed, at their new version.
        unchanged: Jobs it left alone.
        archived: Jobs it removed, which happens only for a module deploy.
        warnings: What the platform validated but did not reject.
        module: The deployment module this deploy claimed, or ``None`` for an
            ad-hoc one.
    """

    added: tuple[Job[M], ...]
    updated: tuple[Job[M], ...]
    unchanged: tuple[Job[M], ...]
    archived: tuple[Job[M], ...]
    warnings: tuple[str, ...]
    module: str | None

    @staticmethod
    def _from_payload(
        ctx: _Ctx[Any], payload: DeployManifestResponse
    ) -> DeployReport[Any]:
        def jobs(rows: Sequence[Any]) -> tuple[Job[Any], ...]:
            return tuple(Job._from_payload(ctx, row) for row in rows)

        return DeployReport(
            added=jobs(payload.added),
            updated=jobs([u.script for u in payload.updated]),
            unchanged=jobs(payload.unchanged),
            archived=jobs(payload.archived),
            warnings=tuple(payload.warnings),
            module=(
                payload.deployment_module
                if isinstance(payload.deployment_module, str)
                else None
            ),
        )


@dataclass(frozen=True, repr=False)
class Job(Entity[M]):
    """A deployed job in a workspace.

    Attributes:
        job_ref: Stable reference the platform and CLI address the job by.
        id: The job's uuid.
        name: Display name, when the job definition sets one.
        job_type: How the job executes.
        paused: Whether the schedule is currently suspended.
        archived: Whether a module deploy has retired the job. An archived job
            keeps its runs but the manifest no longer lists it.
        version: Version of the job definition this reflects.
        public_url: Public trigger URL, when publishing is enabled.
        interactive_url: Where an interactive job's session is reachable, when it
            is one.
        default_trigger: The trigger the platform fires when a caller names none.
            Computed by the platform from the definition.
        triggers: Every trigger this job answers to, as the platform computed
            them from the definition. What a selector matches against.
        next_run_at: When the schedule fires next, or ``None`` when nothing is
            scheduled. The platform keeps advancing this while a job is paused.
        definition: The job definition, exactly as the manifest carries it. Left
            opaque: it is dlt's own nested structure, and the SDK models none of
            it — as with the definitions ``Jobs.deploy_manifest`` accepts.
        created_at: When the job was first deployed.
    """

    job_ref: str
    id: str
    name: str | None
    job_type: JobType
    paused: bool
    archived: bool
    version: int
    public_url: str | None
    interactive_url: str | None
    default_trigger: str | None
    triggers: tuple[str, ...]
    next_run_at: datetime | None
    definition: Mapping[str, Any]
    created_at: datetime

    _identity = ("job_ref", "id")
    _kind = EntityKind.JOB

    @overload
    def pause(self: Job[Sync]) -> Job[Sync]: ...

    @overload
    def pause(self: Job[Async]) -> Awaitable[Job[Async]]: ...

    def pause(self) -> Job[Any] | Awaitable[Job[Any]]:
        """Suspend the job's schedule.

        Returns:
            A fresh snapshot with ``paused`` set; awaitable in async mode.

        Raises:
            Conflict: The job has no schedule to suspend, or is already paused.
            NotFound: The job no longer exists.
        """
        workspace_id = self._ctx.require_workspace()
        job_ref = self.job_ref
        return self._ctx.run(
            lambda t: t.pause_script(workspace_id=workspace_id, job_ref=job_ref),
            Job._from_payload,
        )

    @overload
    def resume(self: Job[Sync]) -> Job[Sync]: ...

    @overload
    def resume(self: Job[Async]) -> Awaitable[Job[Async]]: ...

    def resume(self) -> Job[Any] | Awaitable[Job[Any]]:
        """Resume the job's schedule.

        Returns:
            A fresh snapshot with ``paused`` cleared; awaitable in async mode.

        Raises:
            Conflict: The job has no schedule to resume, or is already running.
            NotFound: The job no longer exists.
        """
        workspace_id = self._ctx.require_workspace()
        job_ref = self.job_ref
        return self._ctx.run(
            lambda t: t.resume_script(workspace_id=workspace_id, job_ref=job_ref),
            Job._from_payload,
        )

    @overload
    def publish(self: Job[Sync]) -> Job[Sync]: ...

    @overload
    def publish(self: Job[Async]) -> Awaitable[Job[Async]]: ...

    def publish(self) -> Job[Any] | Awaitable[Job[Any]]:
        """Expose the job on a public trigger URL.

        Returns:
            A fresh snapshot carrying ``public_url``; awaitable in async mode.

        Raises:
            Conflict: The job cannot be published.
            NotFound: The job no longer exists.
        """
        workspace_id = self._ctx.require_workspace()
        job_ref = self.job_ref
        return self._ctx.run(
            lambda t: t.enable_public_url(workspace_id=workspace_id, job_ref=job_ref),
            Job._from_payload,
        )

    @overload
    def unpublish(self: Job[Sync]) -> Job[Sync]: ...

    @overload
    def unpublish(self: Job[Async]) -> Awaitable[Job[Async]]: ...

    def unpublish(self) -> Job[Any] | Awaitable[Job[Any]]:
        """Withdraw the job's public trigger URL.

        Returns:
            A fresh snapshot with ``public_url`` cleared; awaitable in async mode.

        Raises:
            Conflict: The job is not published.
            NotFound: The job no longer exists.
        """
        workspace_id = self._ctx.require_workspace()
        job_ref = self.job_ref
        return self._ctx.run(
            lambda t: t.disable_public_url(workspace_id=workspace_id, job_ref=job_ref),
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
    ) -> TriggerResult: ...

    @overload
    def start_run(
        self: Job[Async],
        *,
        trigger: str = MANUAL_TRIGGER,
        profile: str | None | Keep = KEEP,
        refresh: bool = False,
        skip_freshness: bool = False,
    ) -> Awaitable[TriggerResult]: ...

    def start_run(
        self,
        *,
        trigger: str = MANUAL_TRIGGER,
        profile: str | None | Keep = KEEP,
        refresh: bool = False,
        skip_freshness: bool = False,
    ) -> TriggerResult | Awaitable[TriggerResult]:
        """Ask the platform to run this job.

        The platform may decline — see :class:`TriggerResult`.

        Args:
            trigger: Which trigger to fire, in canonical form. Defaults to
                ``"manual:"``. Only the form is validated, so a trigger
                the job definition does not declare is still honoured.
            profile: Profile to run under. Omit for the job's default.
            refresh: Reload the pipeline's schema and state before running.
            skip_freshness: Run even if the data is already current.

        Returns:
            What became of the request; awaitable in async mode.

        Raises:
            BadRequest: The trigger is not in canonical form.
            NotFound: No such job in this workspace.
            ScopeMissing: Reached without a workspace in scope.
        """
        workspace_id = self._ctx.require_workspace()
        job_ref = self.job_ref
        return self._ctx.run(
            lambda t: t.create_run(
                workspace_id=workspace_id,
                job_ref=job_ref,
                trigger=trigger,
                profile=profile,
                refresh=refresh,
                skip_freshness=skip_freshness,
            ),
            TriggerResult._from_payload,
        )

    @property
    def runs(self) -> JobRuns[M]:
        """This job's runs.

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
                job_type=JobType(str(payload.script_type)),
                paused=payload.paused if isinstance(payload.paused, bool) else False,
                archived=(
                    payload.archived if isinstance(payload.archived, bool) else False
                ),
                version=payload.version,
                public_url=payload.public_url,
                interactive_url=payload.script_url,
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
                next_run_at=(
                    payload.next_scheduled_run
                    if isinstance(payload.next_scheduled_run, datetime)
                    else None
                ),
                definition=payload.job_definition.to_dict(),
                created_at=payload.date_added,
            ),
        )


class Jobs(Collection[M]):
    """The jobs of one workspace."""

    _entity = Job

    def _listing(self, archived: bool | Keep) -> Listing[DetailedScriptResponse]:
        workspace_id = self._ctx.require_workspace()
        return lambda t, limit, offset: t.list_scripts(
            workspace_id=workspace_id, limit=limit, offset=offset, archived=archived
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

        Unlike :meth:`Job.start_run`, each job fires its own
        ``default_trigger`` — falling back to a manual trigger — so this does
        not take a trigger of its own.

        Args:
            refs: Job refs to trigger. Each resolves to exactly one job.
            selectors: Trigger patterns to match, ``fnmatch``-style — for
                example ``"tag:backfill"``, ``"schedule:*"``, ``"manual:jobs.mod.*"``.
            profile: Profile for every run started. Omit for each job's default.
            refresh: Reload schema and state for the jobs that do start.
            dry_run: Report what would be triggered without starting anything.

        Returns:
            One result per matched job, in the platform's order; awaitable in
            async mode. A job the platform declined is present too, with its
            reason — see :class:`TriggerResult`.

        Raises:
            ValueError: Neither ``refs`` nor ``selectors`` was given.
            ScopeMissing: Reached without a workspace in scope.
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
            TriggerResult._all_from_payload,
        )

    @overload
    def deploy_manifest(
        self: Jobs[Sync],
        manifest: DeployManifest,
        *,
        manifest_hash: str,
        module: str | None = None,
        description: str | None | Keep = KEEP,
        dry_run: bool = False,
    ) -> DeployReport[Sync]: ...

    @overload
    def deploy_manifest(
        self: Jobs[Async],
        manifest: DeployManifest,
        *,
        manifest_hash: str,
        module: str | None = None,
        description: str | None | Keep = KEEP,
        dry_run: bool = False,
    ) -> Awaitable[DeployReport[Async]]: ...

    def deploy_manifest(
        self,
        manifest: DeployManifest,
        *,
        manifest_hash: str,
        module: str | None = None,
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
            module: The deployment module this deploy claims. ``None``, the
                default, is an ad-hoc deploy: jobs are added and updated but
                never archived. Naming one lets the platform archive the jobs
                that module owns and the manifest no longer lists.
            description: Workspace description, applied only for a module
                deploy. Omit to leave it as it is; ``None`` clears it.
            dry_run: Report the plan without persisting it.

        Returns:
            What was added, updated, left alone and archived; awaitable in
            async mode.

        Raises:
            BadRequest: The manifest was rejected — a malformed definition, or
                a profile the workspace has no configuration for.
            Conflict: Another deploy is in flight for this workspace.
            NotAuthorized: The caller may not deploy here, or may not deploy a
                job at the profile it asks for.
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
                module=module,
                description=description,
                dry_run=dry_run,
            ),
            DeployReport._from_payload,
        )

    @overload
    def get(self: Jobs[Sync], *, ref: str) -> Job[Sync]: ...

    @overload
    def get(self: Jobs[Async], *, ref: str) -> Awaitable[Job[Async]]: ...

    def get(self, *, ref: str) -> Job[Any] | Awaitable[Job[Any]]:
        """Return one job by its ref or id.

        Args:
            ref: The job ref, or the job's uuid.

        Returns:
            The job; awaitable in async mode.

        Raises:
            NotFound: No such job in this workspace.
            ScopeMissing: Reached without a workspace in scope.
        """
        workspace_id = self._ctx.require_workspace()
        return self._ctx.run(
            lambda t: t.get_script(workspace_id=workspace_id, job_ref=ref),
            Job._from_payload,
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

        Args:
            archived: Keep only archived jobs, or only live ones. Omit for both,
                which is what the platform returns when nothing filters.
            limit: Return at most this many jobs. ``None`` walks to the end.
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
