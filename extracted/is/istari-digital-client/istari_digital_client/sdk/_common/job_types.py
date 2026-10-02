"""Rich job domain type returned by the Jobs manager."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from istari_digital_client.sdk._base import Archivable, ClientHaving, Shareable
from istari_digital_client.sdk._generated.v2.models.job import Job as _GenJob

if TYPE_CHECKING:
    from istari_digital_client.sdk._common.jobs import Jobs


class Job(_GenJob, ClientHaving, Archivable, Shareable):
    if TYPE_CHECKING:
        _mgr: Jobs
    """Rich job object returned by the Jobs manager.

    Fields: id, resource_id (str | None — the resource the job runs against),
    created (datetime), created_by_id (str),
    function (FunctionVersion), file (File — the parameters file),
    assigned_agent_id (str | None), assigned_agent_pool_id (str | None),
    status_history (list), archive_status_history (list).
    Convenience properties: resource_id, status (last JobStatus entry), status_name
    (str: "Created" | "Pending" | "Claimed" | "Validating" | "Running" |
    "Uploading" | "Completed" | "Failed" | "Canceled"),
    archive_status_name (str: "Active" | "Archived" | None).
    Object methods: archive(), restore(), update_status(), poll().
    """

    @property
    def resource_id(self) -> Any:
        """The id of the resource this job runs against.

        The underlying v2 field is named ``model_id`` (deprecated — models and
        artifacts are unified as resources); this exposes it under the current
        ``resource_id`` name.
        """
        return self.model_id

    @property
    def status(self) -> Any:
        """The most recent JobStatus entry from ``status_history``.

        Returns the last element of ``status_history``, which carries the current state
        of the job. The entry has a ``name`` attribute whose value is one of:
        "Created" | "Pending" | "Claimed" | "Validating" | "Running" | "Uploading" |
        "Completed" | "Failed" | "Canceled".
        Returns ``None`` if ``status_history`` is empty, which should not occur for a
        job returned by the API.
        """
        if self.status_history:
            return self.status_history[-1]
        return None

    @property
    def status_name(self) -> Any:
        """The current job status as a plain string.

        Shorthand for ``job.status.name``. Returns the ``JobStatusName`` value, one of:
        "Created" | "Pending" | "Claimed" | "Validating" | "Running" | "Uploading" |
        "Completed" | "Failed" | "Canceled" | "Unknown". Returns ``None`` if
        ``status_history`` is empty.
        Compare with the string value (``job.status_name == "Completed"``) or the enum
        (``job.status_name == JobStatusName.COMPLETED``) — both work.
        """
        s = self.status
        if s is None:
            return None
        return getattr(s.name, "value", s.name)

    @property
    def archive_status_name(self) -> Any:
        """The current archive state of the job as a plain string.

        Returns the ``ArchiveStatusName`` value of the last entry in
        ``archive_status_history``: "Active" | "Archived". Returns ``None`` if
        ``archive_status_history`` is empty (job has never had its archive state
        recorded). Compares equal to both the string value and the enum member.
        """
        if self.archive_status_history:
            last = self.archive_status_history[-1].name
            return getattr(last, "value", last)
        return None

    def update_status(
        self,
        status: Any,
        *,
        agent_id: str | None = None,
        message: Any = None,
    ) -> "Job":
        """Transition this job to a new status and return the refreshed Job.

        Mutates: true

        ``status`` accepts any ``JobStatusName`` value (or its string, matched
        case-insensitively): "Created" | "Pending" | "Claimed" | "Validating" |
        "Running" | "Uploading" | "Completed" | "Failed" | "Canceled" | "Unknown".
        The SDK coerces the value to the enum; the API validates whether the
        transition is permitted from the job's current status. In practice callers
        drive the states an agent owns:
        - "Running" — marks the job as actively executing.
        - "Completed" — marks the job as successfully finished (terminal).
        - "Failed" — marks the job as failed (terminal).
        - "Canceled" — marks the job as canceled (terminal).
        Transitioning to a terminal status ("Completed", "Failed", "Canceled") ends
        the job; ``poll()`` will return immediately for jobs already in a terminal state.

        ``agent_id`` optionally identifies the agent performing the transition.
        ``message`` is an optional structured status message forwarded to the API.

        Returns the updated Job with the new entry appended to ``status_history``.

        Raises NotFoundError if the job no longer exists.
        Raises ConflictError if the requested transition is not permitted from the
        current status.
        """
        return self._mgr._update_job_status(
            self, status, agent_id=agent_id, message=message
        )

    def poll(self, *, interval: float = 5.0, timeout: float | None = None) -> Any:
        """Block until the job reaches a terminal status and return the final status name.

        Aliases: wait await status

        Polls the job's current state every ``interval`` seconds (default 5). The wait
        ends when the job reaches one of the terminal statuses: "Completed", "Failed",
        or "Canceled". Returns the terminal status name as a plain string, e.g.
        "Completed".

        ``timeout`` is the maximum number of seconds to wait before giving up; pass
        ``None`` (the default) to wait indefinitely.

        Raises TimeoutError if ``timeout`` seconds elapse before a terminal status
        is reached.
        """
        return self._mgr._poll_until_terminal(
            self.id, interval=interval, timeout=timeout
        )


__all__ = ["Job"]
