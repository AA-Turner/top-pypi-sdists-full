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

from typing import Dict, List, Optional, Union

import trafaret as t

from datarobot.models.api_object import APIObject
from datarobot.models.notebooks.enums import NotebookType, RunType, ScheduledRunStatus

scheduled_job_param_trafaret = t.Dict({t.Key("name"): t.String, t.Key("value"): t.String})


scheduled_job_payload_trafaret = t.Dict(
    {
        t.Key("uid"): t.String,
        t.Key("org_id"): t.String,
        t.Key("use_case_id"): t.String,
        t.Key("notebook_id"): t.String,
        t.Key("notebook_name"): t.String,
        t.Key("run_type"): t.Enum(*list(RunType)),
        t.Key("notebook_type"): t.Enum(*list(NotebookType)),
        t.Key("parameters"): t.List(scheduled_job_param_trafaret),
        t.Key("notebook_path", optional=True): t.String,
        t.Key("use_case_name", optional=True): t.String,
    }
).ignore_extra("*")

scheduled_run_revision_metadata_trafaret = t.Dict(
    {
        t.Key("id", optional=True): t.String,
        t.Key("name", optional=True): t.String,
    }
)


# TODO: [NB-4787] We are using trafaret's "ignore_extra" very liberally and this is a subset of properties
notebook_scheduled_run_trafaret = t.Dict(
    {
        t.Key("id"): t.String,
        t.Key("use_case_id"): t.String,
        t.Key("status"): t.Enum(*list(ScheduledRunStatus)),
        t.Key("payload"): scheduled_job_payload_trafaret,
        t.Key("title", optional=True): t.String,
        t.Key("start_time", optional=True): t.String,
        t.Key("end_time", optional=True): t.String,
        t.Key("revision", optional=True): scheduled_run_revision_metadata_trafaret,
        t.Key("duration", optional=True): t.Int,
        t.Key("run_type", optional=True): t.Enum(*list(RunType)),
        t.Key("notebook_type", optional=True): t.Enum(*list(NotebookType)),
    }
).ignore_extra("*")


class ScheduledJobParam(APIObject):
    """
    DataRobot Schedule Job Parameter.

    Attributes
    ----------

    name : str
        The name of the parameter.
    value : str
        The value of the parameter.
    """

    _converter = scheduled_job_param_trafaret

    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value


class ScheduledJobPayload(APIObject):
    """
    DataRobot Schedule Job Payload.

    Attributes
    ----------

    uid : str
        The ID of the user who created the notebook schedule.
    org_id : str
        The ID of the user's organization who created the notebook schedule.
    use_case_id : str
        The ID of the Use Case that the notebook belongs to.
    notebook_id : str
        The ID of the notebook being run on a schedule.
    notebook_name : str
        The name of the notebook being run on a schedule.
    run_type : RunType
        The type of the run - either manual (triggered via UI or API) or scheduled.
    notebook_type: NotebookType
        The type of the notebook - either plain or codespace.
    parameters : List[ScheduledJobParam]
        The parameters being used in the notebook schedule. Can be an empty list.
    notebook_path : Optional[str]
        The path of the notebook to execute within the codespace. Optional. Required if notebook is in a codespace.
    use_case_name : Optional[str]
        The name of the Use Case that the notebook belongs to.
    """

    _converter = scheduled_job_payload_trafaret

    def __init__(
        self,
        uid: str,
        org_id: str,
        use_case_id: str,
        notebook_id: str,
        notebook_name: str,
        run_type: RunType,
        notebook_type: NotebookType,
        parameters: List[Dict[str, str]],
        notebook_path: Optional[str] = None,
        use_case_name: Optional[str] = None,
    ):
        self.uid = uid
        self.org_id = org_id
        self.use_case_id = use_case_id
        self.notebook_id = notebook_id
        self.notebook_name = notebook_name
        self.run_type = run_type
        self.notebook_type = notebook_type
        self.parameters = [ScheduledJobParam.from_server_data(param) for param in parameters]
        self.notebook_path = notebook_path
        self.use_case_name = use_case_name


class ScheduledRunRevisionMetadata(APIObject):
    """
    DataRobot Notebook Revision Metadata specifically for a scheduled run.

    Both id and name can be null if for example the job is still running or has failed.

    Attributes
    ----------

    id : Optional[str]
        The ID of the Notebook Revision. Optional.
    name : Optional[str]
        The name of the Notebook Revision. Optional.
    """

    _converter = scheduled_run_revision_metadata_trafaret

    def __init__(
        self,
        id: Optional[str] = None,
        name: Optional[str] = None,
    ):
        self.id = id
        self.name = name


class NotebookScheduledRun(APIObject):
    """
    DataRobot Notebook Scheduled Run. A historical run of a notebook schedule.

    Attributes
    ----------

    id : str
        The ID of the scheduled notebook job.
    use_case_id : str
        The Use Case ID of the scheduled notebook job.
    status : str
        The status of the run.
    payload : ScheduledJobPayload
        The payload used for the background job.
    title : Optional[str]
        The title of the job. Optional.
    start_time : Optional[str]
        The start time of the job. Optional.
    end_time : Optional[str]
        The end time of the job. Optional.
    revision : ScheduledRunRevisionMetadata
        Notebook revision data - ID and name.
    duration : Optional[int]
        The job duration in seconds. May be None for example while the job is running. Optional.
    run_type : Optional[RunType]
        The type of the run - either manual (triggered via UI or API) or scheduled. Optional.
    notebook_type: Optional[NotebookType]
        The type of the notebook - either plain or codespace. Optional.
    """

    _converter = notebook_scheduled_run_trafaret

    def __init__(
        self,
        id: str,
        use_case_id: str,
        status: ScheduledRunStatus,
        payload: Dict[str, Union[str, List[Dict[str, str]]]],
        title: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        revision: Optional[Dict[str, Optional[str]]] = None,
        duration: Optional[int] = None,
        run_type: Optional[RunType] = None,
        notebook_type: Optional[NotebookType] = None,
    ):
        self.id = id
        self.use_case_id = use_case_id
        self.status = status
        self.payload = ScheduledJobPayload.from_server_data(payload)
        self.title = title
        self.start_time = start_time
        self.end_time = end_time
        self.revision = (
            ScheduledRunRevisionMetadata.from_server_data(revision) if revision else None
        )
        self.duration = duration
        self.run_type = run_type
        self.notebook_type = notebook_type
