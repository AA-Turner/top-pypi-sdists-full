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

from typing import Any, Dict, List, Optional, Type, TypeVar

import trafaret as t

from datarobot._compat import String
from datarobot._experimental.pipelines.enums import PipelineScheduleStatus
from datarobot.enums import enum_to_list
from datarobot.models.api_object import APIObject
from datarobot.utils import rawdict
from datarobot.utils.pagination import unpaginate

TPipelineSchedule = TypeVar("TPipelineSchedule", bound="PipelineSchedule")

_BASE_PATH = "pipelines/"


class PipelineSchedule(APIObject):
    """A recurring schedule for a locked pipeline version.

    Attributes
    ----------
    schedule_id : str
        The schedule ID.
    pipeline_id : str
        The pipeline this schedule belongs to.
    version : int
        The pipeline version this schedule dispatches.
    image_id : str
        The execution image the scheduled dispatch runs on.
    image_version : int
        The execution image version snapshotted at create time.
    cron_expression : str
        Cron expression defining the schedule.
    timezone : str
        Timezone for the cron expression.
    status : str
        Schedule status (ACTIVE, PAUSED, DELETED).
    created_at : str
        When the schedule was created.
    updated_at : str
        When the schedule was last updated.
    """

    _converter = t.Dict({
        t.Key("id", to_name="schedule_id"): String(),
        t.Key("pipeline_id"): String(),
        t.Key("version"): t.Int(),
        t.Key("image_id", optional=True, default=None): t.Or(String(), t.Null()),
        t.Key("image_version", optional=True, default=None): t.Or(t.Int(), t.Null()),
        t.Key("cron_expression"): String(),
        t.Key("timezone"): String(),
        t.Key("status"): t.Enum(*enum_to_list(PipelineScheduleStatus)),
        t.Key("created_at", optional=True, default=None): t.Or(String(), t.Null()),
        t.Key("updated_at", optional=True, default=None): t.Or(String(), t.Null()),
    }).allow_extra("*")

    def __init__(
        self,
        schedule_id: str,
        pipeline_id: str,
        version: int,
        cron_expression: str,
        timezone: str,
        status: PipelineScheduleStatus,
        image_id: Optional[str] = None,
        image_version: Optional[int] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.schedule_id = schedule_id
        self.pipeline_id = pipeline_id
        self.version = version
        self.image_id = image_id
        self.image_version = image_version
        self.cron_expression = cron_expression
        self.timezone = timezone
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self) -> str:
        return f"PipelineSchedule(schedule_id={self.schedule_id!r}, cron={self.cron_expression!r})"

    @classmethod
    def _schedules_path(cls, pipeline_id: str) -> str:
        # Schedules are flat under the pipeline (the version to fire lives in
        # the schedule row, not the URL).
        return f"{_BASE_PATH}{pipeline_id}/schedules/"

    @classmethod
    def create(
        cls: Type[TPipelineSchedule],
        pipeline_id: str,
        version_id: int,
        cron_expression: str,
        pipeline_input_id: str,
        image_id: str,
        image_version: int,
        timezone: str = "UTC",
    ) -> TPipelineSchedule:
        """Create a recurring schedule for a locked pipeline version.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        version_id : int
            The locked version number to schedule.
        cron_expression : str
            Cron expression (e.g., '0 9 * * *' for daily at 9am).
        pipeline_input_id : str
            The input set ID to use for each scheduled run.
        image_id : str
            The execution image ID the scheduled dispatch runs on.
        image_version : int
            The execution image version to snapshot for the schedule.
        timezone : str, optional
            Timezone for the cron expression. Default 'UTC'.

        Returns
        -------
        schedule : PipelineSchedule
        """
        path = cls._schedules_path(pipeline_id)
        response = cls._client.post(
            path,
            data=rawdict({
                "cron_expression": cron_expression,
                "pipeline_version_id": version_id,
                "pipeline_input_id": pipeline_input_id,
                "image_id": image_id,
                "image_version": image_version,
                "timezone": timezone,
            }),
        )
        return cls.from_server_data(response.json())

    @classmethod
    def list(
        cls: Type[TPipelineSchedule],
        pipeline_id: str,
    ) -> List[TPipelineSchedule]:
        """List schedules for a pipeline (across all versions).

        Transparently follows pagination and returns the complete result set.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.

        Returns
        -------
        schedules : list of PipelineSchedule
        """
        path = cls._schedules_path(pipeline_id)
        return [cls.from_server_data(item) for item in unpaginate(path, None, cls._client)]

    @classmethod
    def get(
        cls: Type[TPipelineSchedule],
        pipeline_id: str,
        schedule_id: str,
    ) -> TPipelineSchedule:
        """Get a schedule by ID.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        schedule_id : str
            The schedule ID.

        Returns
        -------
        schedule : PipelineSchedule
        """
        path = cls._schedules_path(pipeline_id)
        response = cls._client.get(f"{path}{schedule_id}/")
        return cls.from_server_data(response.json())

    def update(
        self: TPipelineSchedule,
        cron_expression: Optional[str] = None,
        timezone: Optional[str] = None,
    ) -> TPipelineSchedule:
        """Update this schedule.

        Parameters
        ----------
        cron_expression : str, optional
            New cron expression.
        timezone : str, optional
            New timezone.

        Returns
        -------
        schedule : PipelineSchedule
            The updated schedule.
        """
        path = self._schedules_path(self.pipeline_id)
        data: Dict[str, Any] = {}
        if cron_expression is not None:
            data["cron_expression"] = cron_expression
        if timezone is not None:
            data["timezone"] = timezone
        response = self._client.patch(f"{path}{self.schedule_id}/", data=rawdict(data))
        updated = self.from_server_data(response.json())
        self.__dict__.update(updated.__dict__)
        return self

    def delete(self) -> None:
        """Delete this schedule and its underlying K8s CronJob."""
        path = self._schedules_path(self.pipeline_id)
        self._client.delete(f"{path}{self.schedule_id}/")
