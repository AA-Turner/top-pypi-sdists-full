"""Jobs manager (Istari common-user surface).

``Jobs`` does ``create`` / ``get`` / ``list`` / ``archive`` / ``restore``
against the v2 API, returning rich Job objects that own the per-job verbs
(``update_status``, ``poll``, …).
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

from istari_digital_client.sdk._base import Page, coerce_enum
from istari_digital_client.sdk._common._capabilities import _SupportsAccess
from istari_digital_client.sdk._common.job_types import Job
from istari_digital_client.sdk._exceptions import NotFoundError, PermissionDeniedError
from istari_digital_client.sdk._generated.v2.models.archive_status import ArchiveStatus
from istari_digital_client.sdk._generated.v2.models.job_status_name import JobStatusName
from istari_digital_client.sdk._generated.v2.models.new_job import NewJob


_TERMINAL_STATUSES = frozenset(
    {JobStatusName.COMPLETED, JobStatusName.FAILED, JobStatusName.CANCELED}
)


class Jobs(_SupportsAccess):
    """Manager for jobs: create / get / list / archive / restore.

    Reached via ``istari.jobs``. All methods identify jobs by UUID string.

    Sub-managers: none (Jobs is a leaf collection).

    Usage::

        # 1. Submit a job with a parameters dict
        job = istari.jobs.create(
            resource_id="<resource-uuid>",
            function="my_function",
            parameters={"key": "value"},
        )

        # 2. Poll until the job completes (blocks; raises TimeoutError after 120s)
        final_status = job.poll(timeout=120)

        # 3. Check the outcome
        if jobs.get(job.id).status_name == "Completed":
            print("Job finished successfully")
        else:
            print("Job ended with status:", final_status)

        # 4. Archive the finished job
        job.archive()
    """

    def _acl_ref(self, obj: Any) -> tuple[str, str]:
        """A job's v2 identity: kind ``"job"`` + ``job.id``."""
        return "job", obj.id

    def _archive(self, obj: Any, *, reason: str | None = None) -> None:
        self._call(self._engine.v2_api.archive_job, obj.id)

    def _restore(self, obj: Any, *, reason: str | None = None) -> None:
        self._call(self._engine.v2_api.restore_job, obj.id)

    # ------------------------------------------------------------------ #
    # CRUD                                                                 #
    # ------------------------------------------------------------------ #

    def create(
        self,
        *,
        resource_id: str,
        function: str,
        parameters: dict | None = None,
        parameters_file: str | Path | None = None,
        function_version: str | None = None,
        tool_name: str | None = None,
        tool_version: str | None = None,
        operating_system: Any | None = None,
        assigned_agent_id: str | None = None,
        assigned_agent_pool_id: str | None = None,
    ) -> Job:
        """Submit a new job against a resource and return the created Job.

        Mutates: true

        Aliases: run execute launch submit

        ``resource_id`` is the UUID of the target resource (a model or artifact);
        ``function`` is the name of the function to invoke.

        Parameter file precedence: if ``parameters_file`` is provided it is uploaded
        as-is to storage; otherwise ``parameters`` (a dict, defaulting to ``{}``) is
        JSON-serialised to a temporary file, uploaded, and the temp file is deleted.
        Do not pass both — ``parameters_file`` takes priority and ``parameters`` is
        ignored when it is set.

        ``function_version``, ``tool_name``, ``tool_version``, ``operating_system``,
        ``assigned_agent_id``, and ``assigned_agent_pool_id`` are optional and forwarded
        unchanged to the API.

        Returns a Job with fields: id, resource_id (str | None), created (datetime),
        created_by_id (str), function (FunctionVersion), file (File — the parameters
        file), assigned_agent_id (str | None), assigned_agent_pool_id (str | None),
        status_history (list), archive_status_history (list).
        Convenience properties: status_name (str: "Pending" | "Running" | "Completed" |
        "Failed" | "Canceled"), archive_status_name (str: "Active" | "Archived").
        Object methods: archive(), restore(), update_status(), poll().

        If ``resource_id`` is actually a *file* id (a common mix-up — running a job
        against the wrong kind of id is answered by the registry with a misleading
        403, which is the real cause of the "weird permissions bug"), it is
        transparently resolved to its resource and the submission is retried once.

        Raises NotFoundError if resource_id does not exist.
        """
        if parameters_file is not None:
            file_rev = self._engine.storage.upload(str(parameters_file))
        else:
            tmp = None
            try:
                with tempfile.NamedTemporaryFile(
                    suffix=".json", delete=False, mode="w"
                ) as f:
                    # Capture the name BEFORE writing: the file exists on disk the
                    # moment NamedTemporaryFile(delete=False) returns, so if
                    # json.dump raises (non-serializable parameters), the finally
                    # block must still be able to unlink it.
                    tmp = f.name
                    json.dump(parameters or {}, f)
                file_rev = self._engine.storage.upload(tmp)
            finally:
                if tmp and os.path.exists(tmp):
                    os.unlink(tmp)

        # The v2 path param is still named ``model_id`` (deprecated); the value is
        # a resource id — models/artifacts are unified as resources.
        job_kwargs: dict[str, Any] = dict(
            function_name=function,
            new_job=NewJob(revision=file_rev),
            function_version=function_version,
            tool_name=tool_name,
            tool_version=tool_version,
            operating_system=operating_system,
            assigned_agent_id=assigned_agent_id,
            assigned_agent_pool_id=assigned_agent_pool_id,
        )
        try:
            dto = self._call(
                self._engine.v2_api._create_model_job,
                model_id=resource_id,
                **job_kwargs,
            )
        except (PermissionDeniedError, NotFoundError):
            # A wrong-kind id (e.g. a file id) is answered with a misleading
            # 403/404; resolve it to its owning resource id and retry once.
            resolved = self._resource_id_from_file_id(resource_id)
            if resolved is None:
                raise
            dto = self._call(
                self._engine.v2_api._create_model_job,
                model_id=resolved,
                **job_kwargs,
            )
        return Job._bind(dto, mgr=self)

    def get(self, job_id: str) -> Job:
        """Fetch a single job by its UUID and return the full Job object.

        Returns a Job with fields: id, resource_id (str | None), created (datetime),
        created_by_id (str), function (FunctionVersion), file (File — the parameters
        file), assigned_agent_id (str | None), assigned_agent_pool_id (str | None),
        status_history (list), archive_status_history (list).
        Convenience properties: status_name (str: "Pending" | "Running" | "Completed" |
        "Failed" | "Canceled"), archive_status_name (str: "Active" | "Archived").
        Object methods: archive(), restore(), update_status(), poll().

        Raises NotFoundError if no job with that id exists.
        """
        dto = self._call(self._engine.v2_api.get_job, job_id)
        return Job._bind(dto, mgr=self)

    def list(
        self,
        *,
        resource_id: str | None = None,
        status_name: Any | None = None,
        all_users: bool | None = None,
        assigned_agent_pool_id: str | None = None,
        name: str | None = None,
        page: int | None = None,
        size: int | None = None,
        archive_status: str | None = None,
        sort: str | None = None,
    ) -> Page[Job]:
        """List jobs and return an auto-paging sequence of Job objects.

        Iterate the returned Page directly — subsequent offset pages are fetched
        automatically.

        All filters are optional (enum-valued filters are accepted case-insensitively):
        - ``resource_id`` narrows to jobs for one resource.
        - ``status_name`` filters by job state: "Created" | "Pending" | "Claimed" |
          "Validating" | "Running" | "Uploading" | "Completed" | "Failed" |
          "Canceled".
        - ``name`` does a substring match on the job name.
        - ``archive_status`` filters by archive state: "active" | "archived" | "all".
        - ``sort`` controls ordering (pass a sort expression string).

        Each Job in the page has fields: id, resource_id (str | None), created (datetime),
        created_by_id (str), function (FunctionVersion), file (File — the parameters
        file), assigned_agent_id (str | None), assigned_agent_pool_id (str | None),
        status_history (list), archive_status_history (list).
        Convenience properties: status_name, archive_status_name.
        Object methods: archive(), restore(), update_status(), poll().
        """

        status_name_enum = coerce_enum(JobStatusName, status_name, param="status_name")
        archive_status_enum = coerce_enum(
            ArchiveStatus, archive_status, param="archive_status"
        )

        def fetch(page_num: int) -> Any:
            return self._call(
                self._engine.v2_api.list_jobs,
                # v2 filter param is still ``model_id`` (deprecated); value is a resource id.
                model_id=resource_id,
                status_name=status_name_enum,
                all_users=all_users,
                assigned_agent_pool_id=assigned_agent_pool_id,
                name=name,
                page=page_num,
                size=size,
                archive_status=archive_status_enum,
                sort=sort,
            )

        return self._paginate_offset(
            fetch, lambda d: Job._bind(d, mgr=self), start_page=page or 1
        )

    def archive(self, job_id: str) -> None:
        """Archive a job by its UUID.

        Mutates: true

        Archived jobs are excluded from default ``list`` results (use
        ``archive_status="ARCHIVED"`` to include them). To archive via the rich
        object, call ``job.archive()`` on the Job instance instead.

        Raises NotFoundError if no job with that id exists.
        Raises ConflictError if the job is already archived.
        """
        self._call(self._engine.v2_api.archive_job, job_id)

    def restore(self, job_id: str) -> Job:
        """Restore a previously archived job and return the updated Job.

        Mutates: true

        Returns a Job with all fields populated (see ``get()`` for the field list).

        Raises NotFoundError if no job with that id exists.
        Raises ConflictError if the job is already active (archive_status_name is "ACTIVE").
        """
        dto = self._call(self._engine.v2_api.restore_job, job_id)
        return Job._bind(dto, mgr=self)

    # ------------------------------------------------------------------ #
    # Status helpers (called back by Job)                                  #
    # ------------------------------------------------------------------ #

    def _update_job_status(
        self,
        job: Job,
        status: Any,
        *,
        agent_id: str | None = None,
        message: Any = None,
    ) -> Job:
        dto = self._call(
            self._engine.v2_api.update_job_status,
            job.id,
            coerce_enum(JobStatusName, status, param="status"),
            agent_id=agent_id,
            job_status_message=message,
        )
        return Job._bind(dto, mgr=self)

    def _poll_until_terminal(
        self,
        job_id: str,
        *,
        interval: float = 5.0,
        timeout: float | None = None,
    ) -> Any:
        """Poll the job until a terminal status is reached.

        Checks every ``interval`` seconds. Terminal statuses that end the wait:
        "COMPLETED", "FAILED", "CANCELED".

        Returns the final status name string when a terminal status is reached.

        Raises TimeoutError if ``timeout`` seconds elapse before a terminal status
        is reached. Pass ``timeout=None`` (the default) to wait indefinitely.
        """
        import time

        deadline = (time.monotonic() + timeout) if timeout is not None else None
        while True:
            raw = self._call(self._engine.v2_api.get_job, job_id)
            current = raw.status_history[-1].name if raw.status_history else None
            if current in _TERMINAL_STATUSES:
                return current
            if deadline is not None and time.monotonic() >= deadline:
                raise TimeoutError(
                    f"Job {job_id!r} did not reach a terminal status within {timeout}s"
                )
            time.sleep(interval)
