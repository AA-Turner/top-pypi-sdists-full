#
# Copyright 2026 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from strenum import StrEnum


class PipelineMode(StrEnum):
    """Whether a pipeline is still editable.

    A pipeline is created as ``DRAFT`` and can be re-uploaded freely. Calling
    :meth:`Pipelines.lock <datarobot.pipelines.pipelines.Pipelines.lock>`
    promotes it to ``LOCKED``, which cuts an immutable, numbered version --
    the only thing a schedule can point at. Locking is one-way; further edits
    mean a new draft, usually via ``clone``.
    """

    DRAFT = "draft"
    LOCKED = "locked"


class PipelineVersionStatus(StrEnum):
    """Whether DataRobot has finished parsing a locked version's source.

    Locking is asynchronous: the service re-parses the workflow file and
    rebuilds the task graph. A version is ``PENDING`` until that completes,
    then ``READY``. ``FAILED`` means the source could not be parsed -- most
    often because the file breaks the authoring rules (only imports,
    ``@dr.task`` functions, and exactly one ``@dr.pipeline`` function; no
    top-level assignments). Only a ``READY`` version can be run.
    """

    PENDING = "PENDING"
    READY = "READY"
    FAILED = "FAILED"


class PipelineDispatchStatus(StrEnum):
    """Lifecycle of a single pipeline run.

    ``PENDING`` is accepted but not yet scheduled; ``PREPARING`` is pulling the
    execution image and provisioning compute; ``RUNNING`` means at least one
    task has started. The remaining four are terminal and distinct on purpose:
    ``COMPLETED`` is full success, ``FAILED`` means a task raised,
    ``CANCELLED`` means someone called ``cancel_run``, and ``ERRORED`` is a
    platform-level fault outside the workflow code -- the distinction matters
    because ``ERRORED`` is usually worth retrying unchanged and ``FAILED`` is
    not.

    Note this is the *dispatch* status. Individual tasks carry their own
    :class:`TaskExecutionStatus`, and a dispatch can be ``RUNNING`` while some
    of its tasks are already ``COMPLETED``.
    """

    PENDING = "PENDING"
    PREPARING = "PREPARING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    ERRORED = "ERRORED"


class TaskExecutionStatus(StrEnum):
    """Lifecycle of one task inside a run.

    Mirrors :class:`PipelineDispatchStatus` with one addition: ``RETRYING``,
    which has no dispatch-level equivalent. A task enters it after a transient
    failure and before its next attempt, so seeing it is not itself a problem.
    """

    PENDING = "PENDING"
    RUNNING = "RUNNING"
    RETRYING = "RETRYING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    ERRORED = "ERRORED"


class PipelineDispatchTrigger(StrEnum):
    """What started a run.

    ``API`` is an explicit
    :meth:`Pipelines.run <datarobot.pipelines.pipelines.Pipelines.run>` call;
    ``SCHEDULE`` is a cron schedule firing. Useful for telling a manual test
    run apart from the recurring ones when reading ``list_runs`` output.
    """

    API = "api"
    SCHEDULE = "schedule"


class PipelineInputState(StrEnum):
    """Whether an input set matches the parameters its pipeline declares.

    Validated when the input is created, against the signature of the
    ``@dr.pipeline`` function. ``INVALID`` means a name or type does not line
    up -- a dispatch using it will be rejected, so this is worth checking
    before running rather than after.
    """

    VALID = "VALID"
    INVALID = "INVALID"


class PipelineScheduleStatus(StrEnum):
    """Lifecycle of a cron schedule.

    ``ACTIVE`` schedules fire and cost compute, which is the one worth
    remembering when a test leaves one behind. ``PAUSED`` is retained but
    dormant, and ``DELETED`` is a soft delete -- the record survives for
    audit, so it can still appear in ``list_schedules`` output.
    """

    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    DELETED = "DELETED"


class PipelineImageStatus(StrEnum):
    """Build state of an execution image.

    Images build asynchronously and take a few minutes. A dispatch is rejected
    unless its image has reached ``READY``, so creating one and immediately
    running is the most common first-time mistake -- poll ``list_images``
    until the image leaves ``CREATING``. ``ERROR`` means the build failed,
    usually an unresolvable package; ``get_image_logs`` has the build output.
    """

    CREATING = "CREATING"
    READY = "READY"
    ERROR = "ERROR"
