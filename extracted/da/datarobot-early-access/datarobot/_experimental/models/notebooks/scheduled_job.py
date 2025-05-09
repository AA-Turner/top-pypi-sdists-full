#
# Copyright 2025 DataRobot, Inc. and its affiliates.
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

import time
from typing import Dict, List, Optional, Union

import trafaret as t

from datarobot._experimental.models.notebooks.enums import ScheduledRunStatus
from datarobot._experimental.models.notebooks.scheduled_run import (
    NotebookScheduledRun,
    scheduled_job_payload_trafaret,
    ScheduledJobPayload,
)
from datarobot.models.api_object import APIObject
from datarobot.utils.pagination import unpaginate

# TODO: [NB-4787] We are using trafaret's "ignore_extra" very liberally and this is a subset of properties
notebook_scheduled_job_trafaret = t.Dict(
    {
        t.Key("id"): t.String,
        t.Key("enabled"): t.Bool,
        t.Key("next_run_time", optional=True): t.String,
        t.Key("run_type"): t.String,
        t.Key("notebook_type"): t.String,
        t.Key("job_payload"): scheduled_job_payload_trafaret,
        t.Key("title", optional=True): t.String,
        t.Key("schedule", optional=True): t.String,
        t.Key("schedule_localized", optional=True): t.String,
        t.Key("last_successful_run", optional=True): t.String,
        t.Key("last_failed_run", optional=True): t.String,
        t.Key("last_run_time", optional=True): t.String,
    }
).ignore_extra("*")


class NotebookScheduledJob(APIObject):
    """
    DataRobot Notebook Schedule. A scheduled job that runs a notebook.

    Attributes
    ----------

    id : str
        The ID of the scheduled notebook job.
    enabled : bool
        Whether job is enabled or not.
    run_type : RunType
        The type of the run - either manual (triggered via UI or API) or scheduled.
    notebook_type: NotebookType
        The type of the notebook - either plain or codespace.
    job_payload : ScheduledJobPayload
        The payload used for the background job.
    next_run_time : Optional[str]
        The next time the job is scheduled to run (assuming it is enabled).
    title : Optional[str]
        The title of the job. Optional.
    schedule : Optional[str]
        Cron-like string to define how frequently job should be run. Optional.
    schedule_localized : Optional[str]
        A human-readable localized version of the schedule. Example in English is 'At 42 minutes past the hour'.
        Optional.
    last_successful_run : Optional[str]
        The last time the job was run successfully. Optional.
    last_failed_run : Optional[str]
        The last time the job failed. Optional.
    last_run_time : Optional[str]
        The last time the job was run (failed or successful). Optional.
    """

    _path = "api-gw/nbx/scheduling/"

    _converter = notebook_scheduled_job_trafaret

    def __init__(
        self,
        id: str,
        enabled: bool,
        run_type: str,
        notebook_type: str,
        job_payload: Dict[str, Union[str, List[Dict[str, str]]]],
        next_run_time: Optional[str] = None,
        title: Optional[str] = None,
        schedule: Optional[str] = None,
        schedule_localized: Optional[str] = None,
        last_successful_run: Optional[str] = None,
        last_failed_run: Optional[str] = None,
        last_run_time: Optional[str] = None,
    ):
        self.id = id
        self.enabled = enabled
        self.next_run_time = next_run_time
        self.run_type = run_type
        self.notebook_type = notebook_type
        self.job_payload = ScheduledJobPayload.from_server_data(job_payload)
        self.title = title
        self.schedule = schedule
        self.schedule_localized = schedule_localized
        self.last_successful_run = last_successful_run
        self.last_failed_run = last_failed_run
        self.last_run_time = last_run_time

    @property
    def use_case_id(self) -> str:
        return self.job_payload.use_case_id

    @classmethod
    def get(cls, use_case_id: str, scheduled_job_id: str) -> NotebookScheduledJob:
        """
        Retrieve a single notebook schedule.

        Parameters
        ----------
        scheduled_job_id : str
            The ID of the notebook schedule you want to retrieve.

        Returns
        -------
        notebook_schedule : NotebookScheduledJob
            The requested notebook schedule.

        Examples
        --------
        .. code-block:: python

            from datarobot._experimental.models.notebooks.scheduled_job import NotebookScheduledJob

            notebook_schedule = NotebookScheduledJob.get(
                use_case_id="654ad653c6c1e889e8eab12e",
                scheduled_job_id="65734fe637157200e28bf688",
            )
        """
        url = f"{cls._client.domain}/{cls._path}{scheduled_job_id}/"
        r_data = cls._client.get(url, params={"use_case_id": use_case_id})
        return NotebookScheduledJob.from_server_data(r_data.json())

    def get_most_recent_run(self) -> Optional[NotebookScheduledRun]:
        """
        Retrieve the most recent run for the notebook schedule.

        Returns
        -------
        notebook_scheduled_run : Optional[NotebookScheduledRun]
            The most recent run for the notebook schedule, or None if no runs have been made.

        Examples
        --------
        .. code-block:: python

            from datarobot._experimental.models.notebooks.scheduled_job import NotebookScheduledJob

            notebook_schedule = NotebookScheduledJob.get(
                use_case_id="654ad653c6c1e889e8eab12e",
                scheduled_job_id="65734fe637157200e28bf688",
            )
            most_recent_run = notebook_schedule.get_most_recent_run()
        """
        runs = self.get_job_history()
        return runs[0] if runs else None

    def get_job_history(self) -> List[NotebookScheduledRun]:
        """
        Retrieve list of historical runs for the notebook schedule. Gets the most recent runs first.

        Returns
        -------
        notebook_scheduled_runs : List[NotebookScheduledRun]
            The list of historical runs for the notebook schedule.

        Examples
        --------
        .. code-block:: python

            from datarobot._experimental.models.notebooks.scheduled_job import NotebookScheduledJob

            notebook_schedule = NotebookScheduledJob.get(
                use_case_id="654ad653c6c1e889e8eab12e",
                scheduled_job_id="65734fe637157200e28bf688",
            )
            notebook_scheduled_runs = notebook_schedule.get_job_history()
        """
        url = f"{self._client.domain}/{self._path}/runHistory/"
        params = {
            "order_by": "-startTime",
            "use_case_id": self.use_case_id,
            "job_ids": self.id,
        }
        r_data = unpaginate(url, params, self._client)
        return [NotebookScheduledRun.from_server_data(data) for data in r_data]

    def wait_for_completion(self, max_wait: int = 600) -> str:
        """
        Wait for the completion of a scheduled notebook and return the revision ID corresponding to the run's output.

        Parameters
        ----------
        max_wait : int
            The number of seconds to wait before giving up.

        Returns
        -------
        revision_id : str
            Returns either revision ID or message describing current state.

        Examples
        --------
        .. code-block:: python

            from datarobot._experimental.models.notebooks.notebook import Notebook

            notebook = Notebook.get(notebook_id='6556b00dcc4ea0bb7ea48121')
            manual_run = notebook.run()
            revision_id = manual_run.wait_for_completion()
        """
        status = None
        start_time = time.time()
        while (
            status not in ScheduledRunStatus.terminal_statuses()
            and time.time() < start_time + max_wait
        ):
            time.sleep(5)
            job_run = self.get_most_recent_run()
            if job_run:
                status = job_run.status
        if status and status in ScheduledRunStatus.terminal_statuses():
            if job_run and job_run.revision and job_run.revision.id:
                return job_run.revision.id
            else:
                return f"Revision ID not available for notebook schedule with status: {status}"
        else:
            return f"Notebook schedule has not yet completed. Its current status: {status}"
